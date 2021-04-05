import re
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from pydash import py_
from review.forms import FoodForm, UsdaPairForm, ScrapeFoodForm, ScrapeCategoryForm
from review.models import UsdaFoodNutrient, UsdaWikiPairing, WikiCategoryAssignment, WikiScrapeFood, WikiScrapeCategory
from review.unsplash.unsplash_api import get_images
from review.usda.usda_http import get_usda_results, make_usda_food

from scripts.food_scrape.page_scripts import food_page, single_table_category, table_categories, ul_categories, helpers

class ReviewLanding(LoginRequiredMixin, View):
    def get(self, req):
        context = {}
        return render(req, 'review/landing.html', context)


class FoodListView(ListView):
    template_name = 'review/scraped_food_list.html'
    model = WikiScrapeFood

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        term = self.request.GET.get('filter')
        if term:
            context['term'] = term
            context['wikiscrapefood_list'] = py_.filter(
                context['wikiscrapefood_list'], lambda food: term in food.name.lower())
        return context


class UsdaPairingView(View):
    
    template_name = 'review/usda_pairing_form.html'
    model = WikiScrapeFood

    def get(self, request, pk):
        food = WikiScrapeFood.objects.get(pk=pk)

        return render(request, self.template_name, {
            'food': food,
            'form': UsdaPairForm(),
            'usda_foods': get_usda_results(food.name)
        })

    def post(self, request, pk=None):

        food = get_object_or_404(WikiScrapeFood, id=pk)
        form = UsdaPairForm(request.POST)
    

        if not form.is_valid():
            return render(request, self.template_name, {
                'form': form,
                'food': food,
                'usda_foods': get_usda_results(food.name)
            })

        UsdaWikiPairing(
            wiki_food= food,
            usda_food= make_usda_food(request.POST.get('fdc'))
        ).save()

        food.paired = True

        food.save()
        
        return redirect(reverse_lazy('review:complete_food', kwargs={'pk': pk}))
        # return redirect(reverse_lazy('review:review_landing'))


class FoodMetadataUpdate(LoginRequiredMixin, View):
    template_name = 'review/food_metadata_form.html'

    def get(self, request, pk):
        food = WikiScrapeFood.objects.get(pk=pk)
        return render(request, self.template_name, {
            'form': FoodForm(instance=get_object_or_404(WikiScrapeFood, id=pk)),
            'food': food,
            'images': get_images(re.sub(r'[^A-Za-z0-9 ]+', '' ,food.name), 1)
        })
    

    def post(self, request, pk=None):

        food = get_object_or_404(WikiScrapeFood, id=pk)
        form = FoodForm(request.POST, instance=food)

        if not form.is_valid():
            return render(request, self.template_name, {
                'form': form,
                'food': food
            })

        food = form.save(commit=False)
        food.categories.set(form.cleaned_data['categories'])
        food.save()

        return redirect(reverse_lazy('review:complete_food', kwargs={'pk': pk}))


class CompleteFoodView(View):
    model = WikiScrapeFood
    template_name = 'review/complete_food.html'
    

    def get(self, request, pk=None):
        food = WikiScrapeFood.objects.get(id=pk)
        usda = food.usdawikipairing_set.all()[0].usda_food;
        
        return render(request, self.template_name, {
            'food': food,
            'usda': usda,
            'foodNutrients': UsdaFoodNutrient.objects.filter(usda_food=usda.id),
        })


class CompletedListView(View):
    template_name = 'review/completed_foods.html'

    def get(self, request, ):
        completed = UsdaWikiPairing.objects.all()

        for pair in completed:
            nutrients = {}
            for nutr in UsdaFoodNutrient.objects.filter(usda_food=pair.usda_food.id):
                key = re.sub(r'[^a-zA-Z0-9]', '', nutr.nutrient.name)
                nutrients[key] = {
                    'nutrient': nutr.nutrient.name,
                    'amount': nutr.amount,
                    'unit': nutr.nutrient.unitName,
                }
            pair.set_data('nutrients', nutrients)

        return render(request, self.template_name, {
            'completed': completed
        })


class ScrapeFood(View):
    template_name = 'review/new_food_scrape.html'

    def get(self, request):
        return render(request, self.template_name, {'form': ScrapeFoodForm()})

    def post(self, request):

        # food = get_object_or_404(WikiScrapeFood, id=pk)
        form = ScrapeFoodForm(request.POST)

        if not form.is_valid():
            print('not valid')
            return render(request, self.template_name, {'form': form})

        scrape = food_page.create_food_url(request.POST.get('url'))
        food = WikiScrapeFood(
            name=scrape.name,
            description=scrape.description,
            wiki_url=scrape.wiki_url,
            img_src=scrape.image_src
        )
        food.save()

        return redirect(reverse_lazy('review:food_usda', kwargs={'pk': food.id}))


class ScrapeCategories(View):
    template_name = 'review/new_category_scrape.html'

    def get(self, request):
        return render(request, self.template_name, {'form': ScrapeCategoryForm()})

    def post(self, request):

        # food = get_object_or_404(WikiScrapeFood, id=pk)
        form = ScrapeCategoryForm(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        stype = request.POST.get('category_scrape_type')
        url = request.POST.get('url')
        name = request.POST.get('name')
        categories = None
        if stype == 'table':
            categories = single_table_category.scrape_page(url, name)
        elif stype == 'tables':
            categories = table_categories.scrape_page(url, 1)
        elif stype == 'list':
            categories = ul_categories.scrape_page(url)
        elif stype == 'single':
            categories = [{
                'description': helpers.scape_description(url),
                'wiki_url': url,
            }]

        for scrpaed_cat in categories:
            category = WikiScrapeCategory(
                name=name,
                description=scrpaed_cat.get('description'),
                wiki_url=scrpaed_cat.get('wiki_url')
            )
            category.save()

            if scrpaed_cat.get('foods'):
                for scraped_food in scrpaed_cat.get('foods'):
                    food = WikiScrapeFood(
                        name=scraped_food.name,
                        description=scraped_food.description,
                        wiki_url=scraped_food.image_src,
                        img_src=scraped_food.wiki_url,
                    )
                    food.save()
                    WikiCategoryAssignment(
                        food=food,
                        category=category
                    )

        return redirect(reverse_lazy('review:review_landing'))


class CategoryList(ListView):
    template_name = 'review/category_list.html'
    model = WikiScrapeCategory

