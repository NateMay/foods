from pydash import py_
import requests
import json
from review.models import UsdaNutrient, UsdaFood, UsdaFoodNutrient, UsdaFoodPortion

SEARCH_ENDPOINT = 'https://api.nal.usda.gov/fdc/v1/foods/search'
APIKEY = 'NVguQkLzba5lX36C0GNpZBCyBAvtHZ5lLbxE5RKp'

CACHE_FILENAME = 'review/usda/usda_cache.json'
CACHE = {}


def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk

    Parameters
    ----------
    cache_dict: dict
        The dictionary to save

    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME, "w")
    fw.write(dumped_json_cache)
    fw.close()


def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary. If the cache file doesn't exist,
    creates a new cache dictionary

    Parameters
    ----------
    None

    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


def search(search_term):
    # Hit the search API for the Food Data Central database
    
    RESPNSE_CACHE = open_cache()

    if search_term in RESPNSE_CACHE:
        print('Using Cache for: ', search_term)
    else:
        print('Fetching for: ', search_term)
        RESPNSE_CACHE[search_term] = requests.get(
            f'{SEARCH_ENDPOINT}?query={search_term}&api_key={APIKEY}').json()
        save_cache(RESPNSE_CACHE)

    return RESPNSE_CACHE.get(search_term)


NUTRIENT_SHORT_LIST = ['301', '303', '324', '601',
                       '606', '203', '204', '208', '291', '307', '539', '605']
SOURCES = ['Survey (FNDDS)', 'SR Legacy', 'Foundation']


def get_usda_results(term):
    # get a usda search result and prep it for the modal UI
    usda_foods = search(term).get('foods')

    # filter out branded foods
    usda_foods = py_.filter(
        usda_foods, lambda f: f.get('dataType') in SOURCES)

    # make short list of nutrients
    for usda in usda_foods:
        usda['short_list'] = py_.filter(usda.get('foodNutrients'), lambda n: n.get(
            'nutrientNumber') in NUTRIENT_SHORT_LIST)

    return usda_foods


FOOD_ENDPOINT = 'https://api.nal.usda.gov/fdc/v1/food'


def make_usda_food(fdcid):
    try:
        instance = UsdaFood.objects.get(fdcId=fdcid)
        instance.delete()
    except:
        pass

    RESPNSE_CACHE = open_cache()

    if fdcid in RESPNSE_CACHE:
        print('Using Cache for: ', fdcid)
    else:
        print('Fetching for: ', fdcid)
        RESPNSE_CACHE[fdcid] = requests.get(
            f'{FOOD_ENDPOINT}/{fdcid}?format=full&api_key={APIKEY}').json()
        save_cache(RESPNSE_CACHE)

    response = RESPNSE_CACHE.get(fdcid)


    

    usda_food = UsdaFood(
        fdcId = response.get('fdcId'),
        foodClass = response.get('foodClass'),
        description = response.get('description'),
        foodCode = response.get('foodCode'),
        totalRefuse = response.get('totalRefuse'),
        ingredients = response.get('ingredients'),
        scientificName = response.get('scientificName'),
        gtinUpc = response.get('gtinUpc'),
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
