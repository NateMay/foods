from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import  redirect, render
from django.urls import reverse_lazy
from django.views import View
from review.forms import CatScrapableForm, ScrapeFoodForm, QuickScrapeCategoryForm
from review.models import Scrapable, WikiCategoryAssignment, WikiFood, WikiCategory
import json
from scripts.food_scrape.page_scripts import food_page, single_table_category, table_categories, ul_categories, helpers


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

        save_categories(categories, name)

        return redirect(reverse_lazy('review:review_landing'))



class Batch(View):

    def get(self, request):

        return render(request, 'review/batch.html', {
            'pages': Scrapable.objects.filter(isCategory=True, duration__isnull=True),
            'form': CatScrapableForm(),
        })

    def post(self, request):
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
        # Scrapable
        # Scrapable(
        #     name = page[0],
        #     wiki_url = page[1],
        #     type = 'single_table_category',
        # )


class ScrapeCategory(View):
    def get(self, request, pk=None):

        page = Scrapable.objects.get(pk=pk)

        if page.type == 'single_table_category':
            save_categories(single_table_category.scrape_page(
                page.url, page.name), page.name)
        elif page.type == 'table_categories':
            save_categories(table_categories.scrape_page(
                page.url, page.column), page.name)
        elif page.type == 'ul_categories':
            save_categories(ul_categories.scrape_page(page.url), page.name)

        return redirect(reverse_lazy('review:batch'))


def save_categories(categories, name):
    for scrpaed_cat in categories:
        category = WikiCategory(
            name=name,
            description=scrpaed_cat.get('description'),
            wiki_url=scrpaed_cat.get('wiki_url')
        )
        category.save()

        if scrpaed_cat.get('foods'):
            for scraped_food in scrpaed_cat.get('foods'):
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
