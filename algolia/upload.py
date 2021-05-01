from review.models import UsdaFood, UsdaFoodPortion, UsdaWikiPairing
from algoliasearch.search_client import SearchClient
from mysecrets import ALGOLIA_APIKEY, ALGOLIA_APPID

client = SearchClient.create(ALGOLIA_APPID, ALGOLIA_APIKEY)
index = client.init_index('dev_dietstats')

def create(pair_id):
  
  pair = UsdaWikiPairing.objects.get(pk=pair_id)
  
  portion = UsdaFoodPortion.objects.get(usda_food=pair.usda_food.fdc_id, sequenceNumber=1)

  idx_food = {
    'name': pair.wiki_food.name,
    'img_src': pair.wiki_food.img_src,
    'description': pair.wiki_food.description,
    'amount': 1, 
    'unit': portion.portionDescription.replace('1 ', ''), 
  }

  index.save_objects([idx_food], {'autoGenerateObjectIDIfNotExist': True})

  pair.indexed = True
  pair.save()
