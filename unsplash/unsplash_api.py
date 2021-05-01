



from mysecrets import UPSPLASH_APIKEY
from caches.cache import Cache
from review.models import UnsplashPhoto
import requests
from pydash import py_


UNSPLASH_CACHE = Cache('unsplash/unsplash_cache.json')

# https://api.unsplash.com/search/photos?page=1&query=office&client_id=<API KEY>
BASE = 'https://api.unsplash.com/search/photos'


def get_unsplash_photos(food, page=1):
    term = food.name
    key = f'{term}||{page}'
    response = UNSPLASH_CACHE.get_item(key)

    if not response:
        query_params = f'?page={page}&query={term}&client_id={UPSPLASH_APIKEY}'
        response = requests.get(
            f'{BASE}{query_params}').json()
        UNSPLASH_CACHE.cache_item(key, response)

    return py_.map(response.get('results'), lambda photo, i: UnsplashPhoto.objects.get_or_create(
        food=food,
        search_term = term,
        order = i * page,
        total = response.get('total'),
        width = photo.get('width'),
        height = photo.get('height'),
        color = photo.get('color'),
        blur_hash = photo.get('blur_hash'),
        description = photo.get('description'),
        alt_description = photo.get('alt_description'),
        raw = py_.get(photo, 'urls.raw'),
        full = py_.get(photo, 'urls.full'),
        small = py_.get(photo, 'urls.small'),
        thumb = py_.get(photo, 'urls.thumb'),
        regular = py_.get(photo, 'urls.regular'),
        unsplash_page = py_.get(photo, 'links.html'),
        username = py_.get(photo, 'user.username'),
        ancestryCategory = py_.get(photo, 'tags[0].source.ancestry.category.slug'),
        ancestrySubcategory = py_.get(photo, 'tags[0].source.ancestry.subcategory.slug'),
    )[0])
