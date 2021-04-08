from review.models import WikiCategoryAssignment, WikiCategory
from scripts.food_scrape.wikipedia import wiki_http as http
from scrape import food_page, helpers
# logic for pages which have a single, giant table of foods

def scrape_page(page_url, category_name):
    # scrapes pages with (effectively) 1 large table

    soup = http.request(page_url)

    # remove footnote superscripts
    for superscript in soup.select('sup'):
        superscript.extract()

    category, created = WikiCategory.objects.get_or_create(
        name = category_name,
        description = helpers.scape_description(page_url, soup),
        wiki_url = page_url,
    )

    if created: category.save()

    # get the table
    for table in soup.select('.mw-parser-output table.wikitable'):
        # get the food links
        for anchor in table.select('tbody tr td:first-child a'):
            # ony the good ones
            if anchor and 'redlink=1' not in anchor["href"]:
                # create a food from the link

                WikiCategoryAssignment(
                    food = food_page.create_food_from_anchor(anchor),
                    category = category
                )
                 
    return 'success'
