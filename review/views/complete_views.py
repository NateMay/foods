import re
from django.shortcuts import render
from django.views import View
from review.models import  UsdaFoodNutrient, UsdaWikiPairing, WikiFood


class CompleteFoodView(View):
    model = WikiFood
    template_name = 'review/complete_food.html'

    def get(self, request, pk=None):
        
        pair = UsdaWikiPairing.objects.get(id=pk)
        return render(request, self.template_name, {
            'food': pair.wiki_food,
            'usda': pair.usda_food,
            'foodNutrients': UsdaFoodNutrient.objects.filter(usda_food=pair.usda_food.fdc_id),
        })


class CompletedListView(View):
    template_name = 'review/completed_foods.html'

    def get(self, request, ):
        completed = UsdaWikiPairing.objects.all()
    
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
            'completed': completed
        })
