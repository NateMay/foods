from bs4 import BeautifulSoup
import requests
import json

CACHE_FILENAME = 'scripts/food_scrape/wikipedia/wiki_cache.json'
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


def request(url):
    '''Requests a url or gets the html from the cache

    Parameters
    ----------
    url: string
        address of the website to scrape

    Returns
    -------
    BeautifulSoup
        a BeautifulSoup object of the parsed html
    '''
    RESPNSE_CACHE = open_cache()

    if url in RESPNSE_CACHE:
        print('Using Cache for: ', url)
    else:
        print('Fetching: ', url)
        RESPNSE_CACHE[url] = requests.get(url).text
        save_cache(RESPNSE_CACHE)

    return BeautifulSoup(RESPNSE_CACHE.get(url), 'html.parser')
