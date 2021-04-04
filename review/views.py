import re
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from pydash import py_
from review.forms import FoodForm, UsdaPairForm
from review.models import UsdaFoodNutrient, UsdaWikiPairing, WikiScrapeFood
from review.unsplash.unsplash_api import get_images
from review.usda.usda_http import get_usda_results, make_usda_food


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
    success_url = reverse_lazy('review:foods')

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
