from scrape.wikipedia import wiki_http as http
from scrape import helpers
from review.models import WikiFood

# Logic for scraping a food page

def create_food_from_anchor(anchor):
    # recieves an anchor link, retuns a food object for it
    return create_food_url(helpers.anchor_link(anchor))


def food_from_route(route):
    # recieves an href value, retuns a food object for it
    return create_food_url(helpers.add_base_url(route))


def create_food_url(page_url):
    # contructs a WikiFood object by scraping a food page
    soup = http.request(page_url)

    food, created = WikiFood.objects.get_or_create(
        name = helpers.scrub_string(soup.find('h1').text).replace(' as food', ''),
        description = helpers.scape_description(page_url, soup),
        img_src = helpers.scape_primary_image(soup),
        wiki_url = page_url
    )
    if created: food.save()
    return food
