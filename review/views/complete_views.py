import re
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.views import View
from review.models import UsdaFoodNutrient, UsdaWikiPairing, WikiFood
from pydash import py_
from algolia.upload import create

class CompleteFoodView(View):
    model = WikiFood
    template_name = 'review/complete_food.html'

    def get(self, request, pk=None):

    
        pair = UsdaWikiPairing.objects.get(pk=pk)
        return render(request, self.template_name, {
            'pair': pair,
            'foodNutrients': UsdaFoodNutrient.objects.filter(usda_food=pair.usda_food),
        })

    def post(self, request, pk=None):
        print('id ---- ', request.POST.get('pair_id'))
        create(request.POST.get('pair_id'))
        return redirect(reverse_lazy('review:indexed'))


class CompletedListView(View):
    template_name = 'review/completed_foods.html'

    def get(self, request, ):
        term = self.request.GET.get('filter') or ''

        not_indexed = UsdaWikiPairing.objects.filter(indexed=False)
        completed = py_.filter(
            not_indexed, lambda pair: term.lower() in pair.wiki_food.name.lower())

        for pair in completed:
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
            'completed': completed,
            'term': term
        })

    def post(self, request):
        create(request.POST.get('pair_id'))
        return redirect(reverse_lazy('review:completed'))

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
