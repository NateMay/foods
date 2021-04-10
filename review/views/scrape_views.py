from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import  redirect, render
from django.urls import reverse_lazy
from django.views import View
from review.forms import CatScrapableForm, ScrapeFoodForm, QuickScrapeCategoryForm
from review.models import Scrapable, WikiCategoryAssignment, WikiFood, WikiCategory
import json
from scrape import single_table_category, table_categories, ul_categories, food_page, helpers


class ScrapeFood(View):
    template_name = 'review/new_food_scrape.html'

    def get(self, request):
        return render(request, self.template_name, {'form': ScrapeFoodForm()})

    def post(self, request):

        # food = get_object_or_404(WikiFood, id=pk)
        form = ScrapeFoodForm(request.POST)

        if not form.is_valid():
            print('not valid')
            return render(request, self.template_name, {'form': form})

        scrape = food_page.create_food_url(request.POST.get('url'))
        food = WikiFood(
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
        return render(request, self.template_name, {'form': QuickScrapeCategoryForm()})

    def post(self, request):

        # food = get_object_or_404(WikiFood, id=pk)
        form = QuickScrapeCategoryForm(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        stype = request.POST.get('category_scrape_type')
        url = request.POST.get('url')
        name = request.POST.get('name')
        
        if stype == 'table':
            single_table_category.scrape_page(url, name)
        elif stype == 'tables':
            table_categories.scrape_page(url, 1)
        elif stype == 'list':
            ul_categories.scrape_page(url)
        elif stype == 'single':
            cat, created = WikiCategory.objects.get_or_create(
                name=name,
                description = helpers.scape_description(url),
                wiki_url = url,
            )
            if created: cat.save()
            

        return redirect(reverse_lazy('review:category_scrape'))


class ScrapeCategory(View):
    def post(self, request, pk=None):
        scrape(pk)
        return redirect(reverse_lazy('review:batch'))

class Batch(View):

    def get(self, request):

        return render(request, 'review/batch.html', {
            'pages': Scrapable.objects.filter(isCategory=True, scraped=False),
            'form': CatScrapableForm(),
        })

    def post(self, request, pk=None):
        filename = '/Users/nathanielmay/Code/python/review/scrape/scrappable.json'
        scrappables = open(filename, 'r')
        dumped_json_cache = json.dumps(scrappables)
        scrape_type = request.POST.get('type')

        if scrape_type == 'table_categories':
            dumped_json_cache['table_categories'].append()
        elif scrape_type == 'ul_categories':
            dumped_json_cache['ul_categories'].append()
        elif scrape_type == 'single_table_category':
            dumped_json_cache['single_table_category'].append()

        fw = open(filename, "w")
        fw.write(dumped_json_cache)
        fw.close()


class ScrapeCategory(View):
    def get(self, request, pk=None):
        scrape(pk)
        return redirect(reverse_lazy('review:batch'))


def scrape(pk):

    page = Scrapable.objects.get(pk=pk)

    if page.type == 'single_table_category':
        single_table_category.scrape_page(page.url, page.name)

    elif page.type == 'table_categories':
        table_categories.scrape_page(page.url, page.column, page.name)

    elif page.type == 'ul_categories':
        ul_categories.scrape_page(page.url, page.name)

    page.scraped = True
    page.save()


def save_categories(categories, name):
    for scraped_cat in categories:
        category = WikiCategory(
            name=name,
            description=scraped_cat.get('description'),
            wiki_url=scraped_cat.get('wiki_url')
        )
        category.save()

        if scraped_cat.get('foods'):
            for scraped_food in scraped_cat.get('foods'):
                food = WikiFood(
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
