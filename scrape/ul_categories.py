from scrape.wikipedia import wiki_http
from scrape import helpers, food_page

from review.models import WikiCategory, WikiCategoryAssignment

# scapes pages that have several categories, but the foods are
# in a <ul>

def scrape_page(page_url, parent_category):
    ''' scrapes pages with the structure:
        1) h2 = name
        2) p = description
        3) ul = list
    '''
    soup = wiki_http.request(page_url)

    parent, created = WikiCategory.objects.get_or_create(
        name=parent_category,
        description=helpers.scape_description(page_url, soup),
        wiki_url=page_url,
    )
    if created:
        parent.save()

    # remove footnote superscripts
    for superscript in soup.select('sup'):
        superscript.extract()

    # scrape from the table of contents
    for anchor in soup.select('#toc ul > li > a'):

        #  ignore irrelevant sections
        idstr = anchor['href'][1:]
        if idstr in ['See_also', 'Notes', 'References']:
            break

        h2 = soup.find(id=idstr).parent
        # selector: 'p, div' did not work
        description = h2.find_next_sibling("p") or h2.find_next_sibling("div")


        category, created = WikiCategory.objects.get_or_create(
            name = h2.text.replace('[edit]', ''),
            description = description.text.strip(),
            wiki_url = page_url,
            parent_category = parent
        )
        if created:
            category.save()

        for food in getUlFoods(h2):
            assign, created = WikiCategoryAssignment.objects.get_or_create(
                food=food,
                category=category
            )
        if created: assign.save()

    


def getUlFoods(h2):
    # recieves the h2 element and return an list of links to 
    # the foods in the list following it
    return [
        food_page.create_food_from_anchor(anchor)
        for anchor
        in h2.find_next_sibling("ul").select('li > a:first-child')
    ]
