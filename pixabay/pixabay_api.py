
from mysecrets import PIXABAY_APIKEY
from caches.cache import Cache
import requests
from pydash import py_

# https://pixabay.com/api/docs/


class PixabayImage():
    def __init__(self, photo, order, total) -> None:
        self.order = order
        self.total = total

        self.pageURL = photo.get('pageURL')
        self.pixabay_id = photo.get('id')
        self.type = photo.get('type')
        self.tags = photo.get('tags')
        self.previewURL = photo.get('previewURL')
        self.previewWidth = photo.get('previewWidth')
        self.previewHeight = photo.get('previewHeight')
        self.webformatURL = photo.get('webformatURL')
        self.webformatWidth = photo.get('webformatWidth')
        self.webformatHeight = photo.get('webformatHeight')
        self.largeImageURL = photo.get('largeImageURL')
        self.fullHDURL = photo.get('fullHDURL')
        self.imageURL = photo.get('imageURL')
        self.imageWidth = photo.get('imageWidth')
        self.imageHeight = photo.get('imageHeight')
        self.imageSize = photo.get('imageSize')
        self.views = photo.get('views')
        self.downloads = photo.get('downloads')
        self.favorites = photo.get('favorites')
        self.likes = photo.get('likes')
        self.comments = photo.get('comments')
        self.user_id = photo.get('user_id')
        self.user = photo.get('user')
        self.userImageURL = photo.get('userImageURL')

    def __str__(self) -> str:
        return f'({self.order} of {self.total}) {self.imageURL}'


# https://pixabay.com/api/?key=<KEY>&q=yellow+flowers&image_type=photo
PEXELS_CACHE = Cache('pixabay/pixabay_cache.json')
BASE = 'https://pixabay.com/api/'


def get_images(term, page=1):

    key = f'{term}||{page}'
    response = PEXELS_CACHE.get_item(key)

    if not response:
        response = requests.get(
            f'{BASE}?page={page}&per_page=30&q={term}&image_type=photo&key={PIXABAY_APIKEY}').json()
        PEXELS_CACHE.cache_item(key, response)

    # engineered features of ML
    total_results = response.get('total')

    return py_.map(response.get('hits'), lambda r, i: PixabayImage(r, i, total_results))
