

'https://api.unsplash.com/search/photos?page=1&query=office&client_id=DPXHrltsoPOIzP4zYL6S9ScKloDkVSJQEmu4LqBjjI4'

from mysecrets import UPSPLASH_ACCESS
from caches.cache import Cache
import requests
from pydash import py_


class UnsplashImage():
    def __init__(self, photo) -> None:
        self.width = photo.get('width'),
        self.height = photo.get('height'),
        self.color = photo.get('color')
        self.blur_hash = photo.get('blur_hash')
        self.description = photo.get('description')
        self.alt_description = photo.get('alt_description')

        self.raw = photo.get('urls').get('raw'),
        self.full = photo.get('urls').get('full'),
        self.regular = photo.get('urls').get('regular'),
        # self.small = resp.get('urls').get('small'),
        # self.thumb = resp.get('urls').get('thumb'),

        self.unsplash_page = photo.get('links.html')
        # self.categories = photo.get('categories')
        self.username = photo.get('user.username')

        #  possible category information here
        self.ancestryCategory = photo.get('tags.source.ancestry.category.slug')
        self.ancestrySubcategory = photo.get('tags.source.ancestry.subcategory.slug')


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

