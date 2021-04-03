from scripts.food_scrape.page_scripts import helpers, food_page
from scripts.food_scrape.wikipedia import wiki_http as http
from scripts.food_scrape.models import WikiCategory
from scripts.food_scrape.pages import PAGES_TO_SCRAPE, WIKI_BASE

# logic for pages which have a single, giant table of foods


def scrape():
    return [
        scrape_page(f'{WIKI_BASE}{category[1]}', category[0]) 
        for category 
        in PAGES_TO_SCRAPE.get('single_table_category')
    ]


def scrape_page(page_url, category_name):
    # scrapes pages with (effectively) 1 large table

    soup = http.request(page_url)

    # remove footnote superscripts
    for superscript in soup.select('sup'):
        superscript.extract()

    foods = []
    # get the table
    for table in soup.select('.mw-parser-output table.wikitable'):
        # get the food links
        for anchor in table.select('tbody tr td:first-child a'):
            # ony the good ones
            if anchor and 'redlink=1' not in anchor["href"]:
                # create a food from the link
                foods.append(food_page.create_food_from_anchor(anchor))

    # store the foods within their category
    return WikiCategory(category_name, helpers.scape_description(page_url, soup), page_url, foods)
