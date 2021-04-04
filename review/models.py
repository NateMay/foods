from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
# Many-to-many relationships - https://docs.djangoproject.com/en/3.1/topics/db/examples/many_to_many/


class WikiScrapeCategory(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
        validators=[MinLengthValidator(
            2, "Category names must be longer than 1 character")]
    )
    description = models.CharField(max_length=30000)
    wiki_url = models.CharField(max_length=1000)
    # parent_category = models.ForeignKey(
    #     'WikiScrapeCategory', on_delete=models.SET_NULL, null=True)
    foods = models.ManyToManyField('WikiScrapeFood', through='WikiCategoryAssignment')

    def __str__(self):
        return self.name


class WikiScrapeFood(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
        validators=[MinLengthValidator(2, "Food names must be longer than 1 character")]
    )
    description = models.CharField(max_length=30000)
    wiki_url = models.CharField(max_length=1000)
    img_src = models.CharField(max_length=1000, null=True)
    categories = models.ManyToManyField('WikiScrapeCategory', through='WikiCategoryAssignment')
    paired = models.BooleanField(null=True)

    def __str__(self):
        return self.name


class WikiCategoryAssignment(models.Model):
    food = models.ForeignKey(WikiScrapeFood, on_delete=models.CASCADE)
    category = models.ForeignKey(WikiScrapeCategory, on_delete=models.CASCADE)












class UsdaFood(models.Model):
    fdcId = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=20000)

    # 'Survey (FNDDS)' | 'Branded' | 'Foundation' | 'SR Legacy'
    foodClass = models.CharField(max_length=200) 
    foodCode = models.CharField(max_length=20, null=True) # FNDDS id
    totalRefuse = models.CharField(max_length=20, null=True)
    ingredients = models.CharField(max_length=20000, null=True)
    scientificName = models.CharField(max_length=500, null=True)

    # GTIN or UPC code identifying the food. Only applies to Branded Foods.
    gtinUpc = models.CharField(max_length=20, null=True)
    # finalFoodInputFoods?: FinalFoodInputFoods[]
    # foodComponents?: any[] // ??

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # foods = models.ManyToManyField('WikiScrapeFood', through='FdcWikiPairing')
    
    # nutrients # not sure how to reference

    def __str__(self):
        return self.description
    

# The FDC API provides an arrat of category strings...not sure what I should do with them just yet

class UsdaWikiPairing(models.Model):

    class Meta:
        unique_together = (('usda_food', 'wiki_food'),)

    usda_food = models.ForeignKey(UsdaFood, on_delete=models.CASCADE)
    wiki_food = models.ForeignKey(WikiScrapeFood, on_delete=models.CASCADE)

    def __str__(self):
        return self.usda_food + ' - ' + self.wiki_food

class UsdaNutrient(models.Model):
    class Meta:
        unique_together = (('number', 'unitName'),)

    number = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    rank = models.IntegerField(null=True)
    unitName = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UsdaFoodNutrient(models.Model):
    amount = models.FloatField()
    nutrient = models.ForeignKey('UsdaNutrient',on_delete=models.CASCADE)
    usda_food = models.ForeignKey('UsdaFood',on_delete=models.CASCADE)

    def __str__(self):
        return self.quanity + ' ' + self.name

class UsdaFoodPortion(models.Model):
    portionDescription = models.CharField(max_length=200, null=True) 
    modifier = models.CharField(max_length=100)
    gramWeight = models.CharField(max_length=20)
    sequenceNumber = models.IntegerField(null=True)
    usda_food = models.ForeignKey('UsdaFood',on_delete=models.CASCADE)

    def __str__(self):
        return self.portionDescription
