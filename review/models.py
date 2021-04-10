from django.db import models
from django.core.validators import MinLengthValidator

####################
# Wikipedia Models #
####################
class WikiCategory(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
        validators=[MinLengthValidator(
            2, "Category names must be longer than 1 character")]
    )
    description = models.CharField(max_length=30000)
    wiki_url = models.CharField(max_length=1000, null=True)
    parent_category = models.ForeignKey(
        'WikiCategory', on_delete=models.SET_NULL, null=True)
    foods = models.ManyToManyField('WikiFood', through='WikiCategoryAssignment', blank=True)

    def __str__(self):
        return self.name

class WikiFood(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
        validators=[MinLengthValidator(2, "Food names must be longer than 1 character")]
    )
    description = models.CharField(max_length=30000)
    wiki_url = models.CharField(max_length=1000, unique=True)
    img_src = models.CharField(max_length=1000, null=True)
    categories = models.ManyToManyField('WikiCategory', through='WikiCategoryAssignment', blank=True)
    reviewed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class WikiCategoryAssignment(models.Model):
    class Meta:
        unique_together = (('food', 'category'),)

    food = models.ForeignKey(WikiFood, on_delete=models.CASCADE)
    category = models.ForeignKey(WikiCategory, on_delete=models.CASCADE)

###############
# USDA Models #
###############

# 'Survey (FNDDS)' | 'Branded' | 'Foundation' | 'SR Legacy'
# class UsdaDBSource(models.Model):
#     source = models.CharField(max_length=200) 

class UsdaFood(models.Model):
    fdc_id = models.CharField(max_length=20, unique=True, primary_key=True)
    description = models.CharField(max_length=20000)

    # 'Survey (FNDDS)' | 'Branded' | 'Foundation' | 'SR Legacy'
    dataType = models.CharField(max_length=200) 
    foodClass = models.CharField(max_length=200) 
    foodCode = models.CharField(max_length=20, null=True) # FNDDS id
    totalRefuse = models.CharField(max_length=20, null=True)
    ingredients = models.CharField(max_length=20000, null=True)
    scientificName = models.CharField(max_length=500, null=True)
    category = models.CharField(max_length=500, null=True)

    # GTIN or UPC code identifying the food. Only applies to Branded Foods.
    gtinUpc = models.CharField(max_length=20, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # finalFoodInputFoods?: FinalFoodInputFoods[]
    # foodComponents?: any[] // ??

    def __str__(self):
        return self.fdc_id

class UsdaWikiPairing(models.Model):

    class Meta:
        unique_together = (('usda_food', 'wiki_food'),)

    usda_food = models.ForeignKey(UsdaFood, on_delete=models.CASCADE)
    wiki_food = models.ForeignKey(WikiFood, on_delete=models.CASCADE)
    indexed = models.BooleanField(default=False)
    data = {}

    def set_data(self, key, value):
        self.data = {key: value}

    def __str__(self):
        return self.wiki_food.name

class UsdaNutrient(models.Model):
    class Meta:
        unique_together = (('number', 'unitName'),)

    number = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    rank = models.PositiveSmallIntegerField(null=True)
    unitName = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UsdaFoodNutrient(models.Model):
    amount = models.FloatField()
    nutrient = models.ForeignKey(UsdaNutrient,on_delete=models.CASCADE)
    usda_food = models.ForeignKey(UsdaFood,on_delete=models.CASCADE)

    def __str__(self):
        return self.usda_food.description + ' | ' + str(self.amount) + ' ' + self.nutrient.unitName + ' ' + self.nutrient.name

class UsdaFoodPortion(models.Model):

    class Meta:
        unique_together = (('portionDescription', 'usda_food'),)

    portionDescription = models.CharField(max_length=200, null=True) 
    modifier = models.CharField(max_length=100)
    gramWeight = models.CharField(max_length=20)
    sequenceNumber = models.PositiveIntegerField(null=True)
    usda_food = models.ForeignKey(UsdaFood,on_delete=models.CASCADE)

    def __str__(self):
        return self.portionDescription

class Scrapable(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=1000, unique=True)
    column = models.PositiveSmallIntegerField(null=True)
    isCategory = models.BooleanField(default=True)
    type = models.CharField(max_length=20)

    scraped = models.BooleanField(default=False)
    food_count = models.PositiveIntegerField(null=True)

    @property
    def uri(self):
        return self.url.split('/')[-1].replace('_', ' ')

