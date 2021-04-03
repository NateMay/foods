from scripts.food_scrape.page_scripts import helpers, food_page
from scripts.food_scrape.pages import PAGES_TO_SCRAPE
from scripts.food_scrape.models import WikiCategory


def scrape():
    return [create_category(name, data) for name, data in PAGES_TO_SCRAPE.get('manual_categories').items()]


def create_category(name, data):
    wiki_url = helpers.add_base_url(data.get('page_url'))
    foods = [ food_page.food_from_route(route) for route in data.get('foods')]
    return WikiCategory(name, helpers.scape_description(wiki_url), wiki_url, foods)
