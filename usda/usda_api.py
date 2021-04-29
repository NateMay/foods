from caches.cache import Cache
from pydash import py_
import requests
import json
from review.models import UsdaNutrient, UsdaFood, UsdaFoodNutrient, UsdaFoodPortion
from mysecrets import USDA_APIKEY

USDA_CACHE = Cache('usda/usda_cache.json')

################
#### Search ####
################
SEARCH_ENDPOINT = 'https://api.nal.usda.gov/fdc/v1/foods/search'

# Hit the search API for the Food Data Central database
def search(search_term):
    
    response = USDA_CACHE.get_item(search_term)
    
    if not response:
        response = requests.get(
            f'{SEARCH_ENDPOINT}?query={search_term}&api_key={USDA_APIKEY}').json()
        USDA_CACHE.cache_item(search_term, response)

    return USDA_CACHE.get_item(search_term)


################
#### Create ####
################
FOOD_ENDPOINT = 'https://api.nal.usda.gov/fdc/v1/food'

# Get the full details of a food and create a model model instance
def make_usda_food(fdcid):
    try:
        instance = UsdaFood.objects.get(fdcId=fdcid)
        instance.delete()
    except:
        pass

    response = USDA_CACHE.get_item(fdcid)

    if not response:
        # https://api.nal.usda.gov/fdc/v1/food/748967?format=full&api_key=USDA_APIKEY
        response = requests.get(
            f'{FOOD_ENDPOINT}/{fdcid}?format=full&api_key={USDA_APIKEY}').json()
        USDA_CACHE.cache_item(fdcid, response)

    response = USDA_CACHE.get_item(fdcid)

    cat = response.get('wweiaFoodCategory', {}).get('wweiaFoodCategoryDescription')
    if not cat:
        cat = response.get('foodCategory', {}).get('description')

    usda_food = UsdaFood(
        fdc_id = response.get('fdcId'),
        foodClass = response.get('foodClass'),
        dataType = response.get('dataType'),
        description = response.get('description'),
        foodCode = response.get('foodCode'),
        totalRefuse = response.get('totalRefuse'),
        ingredients = response.get('ingredients'),
        scientificName = response.get('scientificName'),
        gtinUpc = response.get('gtinUpc'),
        category = cat
    )
    usda_food.save()

    for foodNutrient in response['foodNutrients']:
        if foodNutrient.get('amount'):
            nutrient = get_or_create_nutrient(foodNutrient['nutrient'])
            UsdaFoodNutrient(
                amount = foodNutrient.get('amount'),
                nutrient = nutrient,
                usda_food = usda_food 
            ).save()
    print(response.keys())

    for portion in response.get('foodPortions'):
        UsdaFoodPortion(
            portionDescription= portion.get('portionDescription') or portion.get('modifier'),
            modifier= portion.get('modifier'),
            gramWeight= portion.get('gramWeight'),
            sequenceNumber= portion.get('sequenceNumber'),
            usda_food= usda_food
        ).save()

    return usda_food


def get_or_create_nutrient(nutr):
    try:
        nutrient = UsdaNutrient.objects.get(
            number=nutr.get('number'), unitName=nutr.get('unitName'))
    except:
        nutrient = UsdaNutrient(
            number=nutr.get('number'), name=nutr.get('name'), rank=nutr.get('rank'), unitName=nutr.get('unitName'))
        nutrient.save()
    return nutrient
