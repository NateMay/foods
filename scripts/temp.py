from algoliasearch.search_client import SearchClient

from mysecrets import ALGOLIA_APIKEY, ALGOLIA_APPID
 
def run():
  client = SearchClient.create(ALGOLIA_APPID, ALGOLIA_APIKEY)
  index = client.init_index('dev_dietstats')
  # index.save_objects({'test_key': 'test_value'}, {'autoGenerateObjectIDIfNotExist': True})


