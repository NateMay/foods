from wikipedia import wiki_api
from wikipedia import helpers
from review.models import WikiFood
from unsplash.unsplash_api import get_unsplash_photos
from pexels.pexels_api import get_pexels_photos
from pixabay.pixabay_api import get_pixabay_photos
from wikipedia.helpers import best_guess_common_name, get_description, get_names, remove_superscripts, store_names
# Logic for scraping a food page

def create_food_from_anchor(anchor):
    # recieves an anchor link, retuns a food object for it
    return scrape_wiki_food(helpers.anchor_link(anchor))


def food_from_route(route):
    # recieves an href value, retuns a food object for it
    return scrape_wiki_food(helpers.add_base_url(route))


def scrape_wiki_food(page_url):
    # contructs a WikiFood object by scraping a food page
    soup = wiki_api.request(page_url)
    remove_superscripts(soup)

    names = get_names(soup)

    food, created = WikiFood.objects.get_or_create(
        name = best_guess_common_name(names),
        description = get_description(soup),
        img_src = helpers.scape_primary_image(soup),
        wiki_url = page_url
    )
    if created: food.save()

    store_names(food, names)

    for p in get_pixabay_photos(food): p.save()
    for p in get_pexels_photos(food): p.save()
    for p in get_unsplash_photos(food): p.save()

    return food
