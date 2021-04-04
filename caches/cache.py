
import json

class Cache():

    cache_filename = 'No filename provided'

    def __init__(self, cache_filename) -> None:
        self.cache_filename = cache_filename

    def save_cache(self, cache_dict):
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
        fw = open(self.cache_filename, "w")
        fw.write(dumped_json_cache)
        fw.close()


    def open_cache(self):
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
            cache_file = open(self.cache_filename, 'r')
            cache_contents = cache_file.read()
            cache_dict = json.loads(cache_contents)
            cache_file.close()
        except:
            cache_dict = {}
        return cache_dict
    
    def get_item(self, key):
        return self.open_cache().get(key)

    def cache_item(self, key, value):
        cache = self.open_cache()
        cache[key] = value
        self.save_cache(cache)
        