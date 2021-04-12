from bs4 import BeautifulSoup
from caches.cache import Cache
import requests
import json

WIKI_CACHE = Cache('scrape/wikipedia/wiki_cache.json')


def request(url):

    response = WIKI_CACHE.get_item(url)
    
    if not response:
        print('Fetching: ', url)
        response = requests.get(url).text
        print('Caching: ', url)
        WIKI_CACHE.cache_item(url, response)
    else:
        print('Uncaching: ', url)

    return BeautifulSoup(WIKI_CACHE.get_item(url), 'html.parser')

