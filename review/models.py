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

    def __str__(self):
        return self.name


class WikiCategoryAssignment(models.Model):
    food = models.ForeignKey(WikiScrapeFood, on_delete=models.CASCADE)
    category = models.ForeignKey(WikiScrapeCategory, on_delete=models.CASCADE)










class FdcCategory(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
        validators=[MinLengthValidator(
            2, "Category names must be longer than 1 character")]
    )

class FdcFood(models.Model):
    fdcId = models.CharField(max_length=20)
    foodClass = models.CharField(max_length=20)
    description = models.CharField(max_length=20000)

    # 'Survey (FNDDS)' | 'Branded' | 'Foundation' | 'SR Legacy'
    foodType = models.CharField(max_length=200) 
    foodCode = models.CharField(max_length=20) # FNDDS id
    totalRefuse = models.CharField(max_length=20)
    ingredients = models.CharField(max_length=20000)
    scientificName = models.CharField(max_length=500)

    # GTIN or UPC code identifying the food. Only applies to Branded Foods.
    gtinUpc = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    categories = models.ManyToManyField('FdcCategory', through='FdcCategoryAssignment')
    foods = models.ManyToManyField('WikiScrapeFood', through='FdcWikiPairing')
    # nutrients # not sure how to reference
    # foodMeasures?: FdcFoodMeasure[]
    
    # finalFoodInputFoods?: FinalFoodInputFoods[]
    # foodComponents?: any[] // ??

# The FDC API provides an arrat of category strings...not sure what I should do with them just yet
class FdcCategoryAssignment(models.Model):
    food = models.ForeignKey(FdcFood, on_delete=models.CASCADE)
    category = models.ForeignKey(FdcCategory, on_delete=models.CASCADE)

class FdcWikiPairing(models.Model):
    fdc_food = models.ForeignKey(FdcFood, on_delete=models.CASCADE)
    wiki_food = models.ForeignKey(WikiScrapeFood, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class FdcFoodNutrient(models.Model):
    food = models.ForeignKey('FdcFood',on_delete=models.CASCADE)

    type = models.CharField(max_length=100)
    # id = models.CharField(max_length=5)
    value = models.CharField(max_length=20)
    lastUpdated = models.CharField(max_length=50)
    # nutrient: FdcNutrient from here down
    nutrient_id = models.IntegerField(null=True)
    number = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    rank = models.IntegerField(null=True)
    isNutrientLabel = models.BooleanField()
    indentLevel = models.IntegerField(null=True)
    shortestName = models.CharField(max_length=200)
    nutrientUnit = models.CharField(max_length=50)

class FdcFoodMeasure(models.Model):
    food = models.ForeignKey('FdcFood',on_delete=models.CASCADE)
    
    # id = models.IntegerField(null=True)
    modifier = models.CharField(max_length=100)
    gramWeight = models.CharField(max_length=20)
    disseminationText = models.CharField(max_length=2000)
    rank = models.IntegerField(null=True)

    # measureUnit: FdcMeasureUnit from here down
    # id = models.IntegerField(null=True)
    name = models.CharField(max_length=200)
    abbreviation = models.CharField(max_length=40)
