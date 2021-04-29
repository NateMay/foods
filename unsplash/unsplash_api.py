

'https://api.unsplash.com/search/photos?page=1&query=office&client_id=DPXHrltsoPOIzP4zYL6S9ScKloDkVSJQEmu4LqBjjI4'

from mysecrets import UPSPLASH_ACCESS
from caches.cache import Cache
import requests
from pydash import py_


class UnsplashImage():
    def __init__(self, result) -> None:
        self.width = result.get('width'),
        self.height = result.get('height'),
        self.color = result.get('color')
        self.blur_hash = result.get('blur_hash')
        self.description = result.get('description')
        self.alt_description = result.get('alt_description')
        print()
        self.urls = {
            'raw': result.get('urls').get('raw'),
            'full': result.get('urls').get('full'),
            'regular': result.get('urls').get('regular'),
            'small': result.get('urls').get('small'),
            'thumb': result.get('urls').get('thumb'),
        }
        self.unsplash_page = result.get('links.html')
        self.categories = result.get('categories')
        self.user = {
            'username': result.get('user.username'),
        }
        self.ancestry = {
            'type': result.get('tags.source.ancestry.type.slug'),
            'category': result.get('tags.source.ancestry.category.slug'),
            'subcategory': result.get('tags.source.ancestry.subcategory.slug'),
        }


UNSPLASH_CACHE = Cache('unsplash/unsplash_cache.json')
BASE = 'https://api.unsplash.com/search/photos?'


def get_images(term, page=1):
    key = f'{term}||{page}'
    response = UNSPLASH_CACHE.get_item(key)

    if not response:
        response = requests.get(
            f'{BASE}?page={page}&query={term}&client_id={UPSPLASH_ACCESS}').json()
        UNSPLASH_CACHE.cache_item(key, response)

    return py_.map(response.get('results'), lambda r: UnsplashImage(r))

    # images = []
    # for result in response.results:
    #     images.append(UnsplashImage(result))
