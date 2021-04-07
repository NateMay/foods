import re
from django.shortcuts import render
from django.views import View
from review.models import  UsdaFoodNutrient, UsdaWikiPairing, WikiFood



class CompleteFoodView(View):
    model = WikiFood
    template_name = 'review/complete_food.html'

    def get(self, request, pk=None):
        food = WikiFood.objects.get(id=pk)
        usda = food.usdawikipairing_set.all()[0].usda_food

        return render(request, self.template_name, {
            'food': food,
            'usda': usda,
            'foodNutrients': UsdaFoodNutrient.objects.filter(usda_food=usda.fdc_id),
        })


class CompletedListView(View):
    template_name = 'review/completed_foods.html'

    def get(self, request, ):
        completed = UsdaWikiPairing.objects.all()

        for pair in completed:
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

