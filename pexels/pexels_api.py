from review.models import PexelsPhoto
from mysecrets import PEXELS_APIKEY
from caches.cache import Cache
import requests
from pydash import py_

PEXELS_CACHE = Cache('pexels/pexels_cache.json')

# https://www.pexels.com/api/documentation/#photos-search__parameters
BASE = 'https://api.pexels.com/v1/search'

def get_pexels_photos(food, page=1):
    term = food.name
    key = f'{term}||{page}'
    response = PEXELS_CACHE.get_item(key)

    if not response:
        query_params = f'?page={page}&per_page=30&query={term}'
        response = requests.get(
            f'{BASE}{query_params}', headers={"Authorization":PEXELS_APIKEY}).json()
        PEXELS_CACHE.cache_item(key, response)

    return py_.map(response.get('photos'), lambda photo, i: PexelsPhoto.objects.get_or_create(
        food=food,
        search_term = term,
        # engineered features for ML
        order = response.get('page') * i,
        total = response.get('total_results'),
        pexels_id = photo.get('id'),
        width = photo.get('width'),
        height = photo.get('height'),
        url = photo.get('url'),
        photographer = photo.get('photographer'),
        photographer_url = photo.get('photographer_url'),
        photographer_id = photo.get('photographer_id'),
        avg_color = photo.get('avg_color'),
        original = py_.get(photo, 'src.original'),
        large2x = py_.get(photo, 'src.large2x'),
        small = py_.get(photo, 'src.small'),
        tiny = py_.get(photo, 'src.tiny'),
        # large = py_.get(photo, 'src.large'),
        # medium = py_.get(photo, 'src.medium'),
        # portrait = py_.get(photo, 'src.portrait'),
        # landscape = py_.get(photo, 'src.landscape'),
    )[0])

