from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _


####################
# Wikipedia Models #
####################


class WikiCategory(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
        validators=[MinLengthValidator(2)]
    )
    description = models.CharField(max_length=30000)
    wiki_url = models.CharField(max_length=1000, null=True)
    parent_category = models.ForeignKey(
        'WikiCategory', on_delete=models.SET_NULL, null=True)
    foods = models.ManyToManyField(
        'WikiFood', through='WikiCategoryAssignment', blank=True)

    def __str__(self):
        return self.name


class WikiFood(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
        validators=[MinLengthValidator(2)]
    )
    description = models.CharField(max_length=30000)
    wiki_url = models.CharField(max_length=1000, unique=True)
    img_src = models.CharField(max_length=1000, null=True)
    categories = models.ManyToManyField(
        'WikiCategory', through='WikiCategoryAssignment', blank=True)

    def __str__(self):
        return self.name


class WikiFoodName(models.Model):

    class Meta:
        unique_together = (('name', 'type', 'food'),)

    food = models.ForeignKey(WikiFood, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)

    class NameType(models.TextChoices):
        INFOBOX = 'IN', _('infobox')
        SCIENTIFIC = 'SC', _('scientific')
        BOLD = 'BL', _('bold')
        PAGETITLE = 'PT', _('pageTitle')

    type = models.CharField(
        max_length=2,
        choices=NameType.choices,
        default=NameType.INFOBOX,
    )


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
    foodCode = models.CharField(max_length=20, null=True)  # FNDDS id
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
    nutrient = models.ForeignKey(UsdaNutrient, on_delete=models.CASCADE)
    usda_food = models.ForeignKey(UsdaFood, on_delete=models.CASCADE)

    def __str__(self):
        return self.usda_food.description + ' | ' + str(self.amount) + ' ' + self.nutrient.unitName + ' ' + self.nutrient.name


class UsdaFoodPortion(models.Model):

    class Meta:
        unique_together = (('portionDescription', 'usda_food'),)

    portionDescription = models.CharField(max_length=200, null=True)
    modifier = models.CharField(max_length=100)
    gramWeight = models.CharField(max_length=20)
    sequenceNumber = models.PositiveIntegerField(null=True)
    usda_food = models.ForeignKey(UsdaFood, on_delete=models.CASCADE)

    def __str__(self):
        return self.portionDescription


####################
# Photo API Models #
####################

class UnsplashPhoto(models.Model):

    @property
    def src(self):
        return self.full

    @property
    def thumb(self):
        return self.thumb

    class Meta:
        unique_together = (('search_term', 'order', 'food'),)

    source = 'unsplash'
    food = models.ForeignKey(WikiFood, on_delete=models.CASCADE)
    # Search term used to discover this photo
    search_term = models.CharField(max_length=100)
    order = models.IntegerField()  # The order in which the photo was provided
    total = models.IntegerField()  # The total number of photos found from this search
    width = models.IntegerField()
    height = models.IntegerField()
    color = models.CharField(max_length=20)
    blur_hash = models.CharField(
        max_length=500, null=True)  # https://blurha.sh/
    description = models.CharField(max_length=1500, null=True)
    alt_description = models.CharField(max_length=1500, null=True)
    raw = models.CharField(max_length=500, null=True)
    full = models.CharField(max_length=500, null=True)
    thumb = models.CharField(max_length=500, null=True)
    small = models.CharField(max_length=500, null=True)
    regular = models.CharField(max_length=500, null=True)
    unsplash_page = models.CharField(max_length=500, null=True)
    username = models.CharField(max_length=100, null=True)
    ancestryCategory = models.CharField(max_length=100, null=True)
    ancestrySubcategory = models.CharField(max_length=100, null=True)


class PexelsPhoto(models.Model):

    @property
    def src(self):
        return self.original

    @property
    def thumb(self):
        return self.tiny

    class Meta:
        unique_together = (('search_term', 'order', 'food'),)

    source = 'pexels'
    food = models.ForeignKey(WikiFood, on_delete=models.CASCADE)
    # Search term used to discover this photo
    search_term = models.CharField(max_length=100)
    order = models.IntegerField()  # The order in which the photo was provided
    total = models.IntegerField()  # The total number of photos found from this search
    pexels_id = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    url = models.CharField(max_length=100)
    photographer = models.CharField(max_length=30)
    photographer_url = models.CharField(max_length=100)
    photographer_id = models.IntegerField()
    avg_color = models.CharField(max_length=10)
    original = models.CharField(max_length=200)

    large2x = models.CharField(max_length=200)
    small = models.CharField(max_length=200)
    tiny = models.CharField(max_length=200)
    # large = models.CharField(max_length=200)
    # medium = models.CharField(max_length=200)
    # portrait = models.CharField(max_length=200)
    # landscape = models.CharField(max_length=200)


class PixabayPhoto(models.Model):

    @property
    def src(self):
        return self.imageURL

    @property
    def thumb(self):
        return self.previewURL
    class Meta:
        unique_together = (('search_term', 'order', 'food'),)

    source = 'pixabay'
    food = models.ForeignKey(WikiFood, on_delete=models.CASCADE)
    # Search term used to discover this photo
    search_term = models.CharField(max_length=100)
    order = models.IntegerField()  # The order in which the photo was provided
    total = models.IntegerField()  # The total number of photos found from this search

    pageURL = models.CharField(max_length=100)
    pixabay_id = models.IntegerField()
    tags = models.CharField(max_length=100)
    previewWidth = models.IntegerField()
    previewHeight = models.IntegerField()
    webformatWidth = models.IntegerField()
    webformatHeight = models.IntegerField()
    largeImageURL = models.CharField(max_length=200)  # this is the best one
    imageURL = models.CharField(max_length=200)
    imageWidth = models.IntegerField()
    imageHeight = models.IntegerField()
    imageSize = models.IntegerField()
    views = models.IntegerField()
    downloads = models.IntegerField()
    favorites = models.IntegerField()
    likes = models.IntegerField()
    comments = models.IntegerField()
    user_id = models.IntegerField()
    user = models.CharField(max_length=30)
    previewURL = models.CharField(max_length=200)
    # fullHDURL = models.CharField(max_length=200)
    # webformatURL = models.CharField(max_length=200)


##################################
# Model to hold Scrappable pages #
##################################

class Scrapable(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=1000, unique=True)
    column = models.PositiveSmallIntegerField(null=True, default=0)
    isCategory = models.BooleanField(default=True)
    type = models.CharField(max_length=20)

    scraped = models.BooleanField(default=False)
    food_count = models.PositiveIntegerField(null=True)

    @property
    def uri(self):
        return self.url.split('/')[-1].replace('_', ' ')


#####################################
# Finalized Food and Nutrition Data #
#####################################

class CompiledFood(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
        validators=[MinLengthValidator(2)]
    )
    description = models.CharField(max_length=30000, blank=True, null=True)
    img_src = models.CharField(max_length=1000)
    usda_food = models.ForeignKey(UsdaFood, on_delete=models.CASCADE)
    wiki_url = models.CharField(max_length=1000, null=True)
    categories = models.ManyToManyField(
        'CompiledCategory', through='CompiledCategoryAssignment')


class CompiledCategory(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
        validators=[MinLengthValidator(2)]
    )
    description = models.CharField(max_length=30000, blank=True, null=True)
    parent_category = models.ForeignKey(
        'CompiledCategory', on_delete=models.SET_NULL, null=True)
    foods = models.ManyToManyField(
        'CompiledFood', through='CompiledCategoryAssignment')
    

    def __str__(self):
        return self.name

class CompiledCategoryAssignment(models.Model):
    class Meta:
        unique_together = (('food', 'category'),)

    food = models.ForeignKey(CompiledFood, on_delete=models.CASCADE)
    category = models.ForeignKey(CompiledCategory, on_delete=models.CASCADE)


class CompiledFoodName(models.Model):

    class Meta:
        unique_together = (('name', 'type', 'food'),)

    food = models.ForeignKey(CompiledFood, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)

    class NameType(models.TextChoices):
        INFOBOX = 'IN', _('infobox')
        SCIENTIFIC = 'SC', _('scientific')
        BOLD = 'BL', _('bold')
        PAGETITLE = 'PT', _('pageTitle')

    type = models.CharField(
        max_length=2,
        choices=NameType.choices,
        default=NameType.INFOBOX,
    )
