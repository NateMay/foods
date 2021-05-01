
from mysecrets import PIXABAY_APIKEY
from review.models import PixabayPhoto
from caches.cache import Cache
import requests
from pydash import py_


PEXELS_CACHE = Cache('pixabay/pixabay_cache.json')

# https://pixabay.com/api/docs/
# https://pixabay.com/api/?page=1&per_page=30&q=term_string&image_type=photo&key=<API KEY>
BASE = 'https://pixabay.com/api/'


def get_pixabay_photos(food, page=1):
    term = food.name
    key = f'{term}||{page}'
    response = PEXELS_CACHE.get_item(key)

    if not response:
        query_params = dictToQuery({
            'q': term,
            'page': page,
            'per_page': 30,
            'image_type': 'photo',
            'key': PIXABAY_APIKEY
        })
        # query_params = f'?page={page}&per_page=30&q={term}&image_type=photo&key={PIXABAY_APIKEY}'
        response = requests.get(
            f'{BASE}?{query_params}').json()
        PEXELS_CACHE.cache_item(key, response)

    return py_.map(response.get('hits'), lambda photo, i: PixabayPhoto.objects.get_or_create(
        food=food,
        search_term = term,
        # engineered features for ML
        order = i,
        total = response.get('total'),

        pageURL = photo.get('pageURL'),
        pixabay_id = photo.get('id'),
        tags = photo.get('tags'),
        previewWidth = photo.get('previewWidth'),
        previewHeight = photo.get('previewHeight'),
        webformatWidth = photo.get('webformatWidth'),
        webformatHeight = photo.get('webformatHeight'),
        largeImageURL = photo.get('largeImageURL'),
        imageURL = photo.get('imageURL'),
        imageWidth = photo.get('imageWidth'),
        imageHeight = photo.get('imageHeight'),
        imageSize = photo.get('imageSize'),
        views = photo.get('views'),
        downloads = photo.get('downloads'),
        favorites = photo.get('favorites'),
        likes = photo.get('likes'),
        comments = photo.get('comments'),
        user_id = photo.get('user_id'),
        user = photo.get('user'),
        previewURL = photo.get('previewURL'),
        # webformatURL = photo.get('webformatURL'),
        # fullHDURL = photo.get('fullHDURL'),
    )[0])

def dictToQuery(d):
  query = ''
  for key in d.keys():
    query += str(key) + '=' + str(d[key]) + "&"
  return query
