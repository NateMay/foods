
from mysecrets import PEXELS_APIKEY
from caches.cache import Cache
import requests
from pydash import py_


class PexelsImage():
    def __init__(self, photo, order, total) -> None:
        # print(resp)
        self.order = order
        self.total = total

        self.pexels_id = photo.get('id')
        self.width = photo.get('width')
        self.height = photo.get('height')
        self.url = photo.get('url')
        self.photographer = photo.get('photographer')
        self.photographer_url = photo.get('photographer_url')
        self.photographer_id = photo.get('photographer_id')
        self.avg_color = photo.get('avg_color')

        self.original = photo.get('src').get('original'),
        # self.large2x = resp.get('src').get('large2x'),
        # self.large = resp.get('src').get('large'),
        # self.medium = resp.get('src').get('medium'),
        # self.small = resp.get('src').get('small'),
        # self.portrait = resp.get('src').get('portrait'),
        # self.landscape = resp.get('src').get('landscape'),
        # self.tiny = resp.get('src').get('tiny'),


    def __str__(self) -> str:
        return f'({self.order} of {self.total}) {self.original}'
        

# https://www.pexels.com/api/documentation/#photos-search__parameters
PEXELS_CACHE = Cache('pexels/pexels_cache.json')
BASE = 'https://api.pexels.com/v1/search'


def get_images(term, page=1):

    key = f'{term}||{page}'
    response = PEXELS_CACHE.get_item(key)

    if not response:
        response = requests.get(
            f'{BASE}?page={page}&per_page=30&query={term}', headers={"Authorization":PEXELS_APIKEY}).json()
        PEXELS_CACHE.cache_item(key, response)

    # engineered features of ML
    total_results = response.get('total_results')
    page = response.get('page')

    return py_.map(response.get('photos'), lambda r, i: PexelsImage(r, page * i, total_results))

