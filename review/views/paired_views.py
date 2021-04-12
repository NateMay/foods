import re
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.views import View
from review.models import UsdaFoodNutrient, UsdaWikiPairing, WikiFood
from pydash import py_
from algolia.upload import create

class PairedFoodView(View):
    model = WikiFood
    template_name = 'review/paired_food.html'

    def get(self, request, pk=None):
        pair = UsdaWikiPairing.objects.get(pk=pk)
        print(';jhvadjlhvadjv')
        print(pair.wiki_food)
        print(pair.usda_food)
        return render(request, self.template_name, {
            'pair': pair,
            'foodNutrients': UsdaFoodNutrient.objects.filter(usda_food=pair.usda_food),
        })

    def post(self, request, pk=None):
        create(request.POST.get('pair_id'))
        return redirect(reverse_lazy('review:indexed'))


class PairedListView(View):
    template_name = 'review/paired_foods.html'

    def get(self, request, ):
        term = self.request.GET.get('filter') or ''

        not_indexed = UsdaWikiPairing.objects.filter(indexed=False)
        paired = py_.filter(
            not_indexed, lambda pair: term.lower() in pair.wiki_food.name.lower())

        for pair in paired:
            # process the nutrition data for the template
            nutrients = {}
            for nutr in UsdaFoodNutrient.objects.filter(usda_food=pair.usda_food.fdc_id):
                key = re.sub(r'[^a-zA-Z0-9]', '', nutr.nutrient.name)
                nutrients[key] = {
                    'nutrient': nutr.nutrient.name,
                    'amount': nutr.amount,
                    'unit': nutr.nutrient.unitName,
                }

            pair.set_data('nutrients', nutrients)

        return render(request, self.template_name, {
            'paired': paired,
            'term': term
        })

    def post(self, request):
        create(request.POST.get('pair_id'))
        return redirect(reverse_lazy('review:paired'))

class IndexedListView(View):
    template_name = 'review/indexed_foods.html'
    def get(self, request):
        term = self.request.GET.get('filter') or ''
        all_indexed = UsdaWikiPairing.objects.filter(indexed=True)
        filtered_indexed = py_.filter(
            all_indexed, lambda pair: term.lower() in pair.wiki_food.name.lower())

        return render(request, self.template_name, {
            'foods': filtered_indexed,
            'term': term
        })
