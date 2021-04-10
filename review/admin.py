from django.contrib import admin

from review.models import WikiCategory, WikiFood, WikiCategoryAssignment, UsdaFood, UsdaWikiPairing, UsdaNutrient, UsdaFoodNutrient, UsdaFoodPortion, Scrapable

admin.site.register(WikiCategory)
admin.site.register(WikiFood)
admin.site.register(WikiCategoryAssignment)
admin.site.register(UsdaFood)
admin.site.register(UsdaWikiPairing)
admin.site.register(UsdaNutrient)
admin.site.register(UsdaFoodNutrient)
admin.site.register(UsdaFoodPortion)
admin.site.register(Scrapable)
