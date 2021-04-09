from scrape import food_page, helpers
from scrape.wikipedia import wiki_http as http
from review.models import WikiCategory, WikiCategoryAssignment, WikiFood


# logic to scrape a page with a table of foods

def scrape_page(page_url, column, parent_category):
    ''' scrapes pages with the structure:
        1) h2 = name
        2) p = description
        3) table = list
    '''
    soup = http.request(page_url)

    parent, created = WikiCategory.objects.get_or_create(
        name=parent_category,
        description=helpers.scape_description(page_url, soup),
        wiki_url=page_url,
    )
    if created:
        parent.save()

    # each table is a category
    for table in soup.select(':not(.navbox) > table'):

        category, created = WikiCategory.objects.get_or_create(
            name=category_name(table),
            description=category_description(table),
            wiki_url=page_url,
            parent_category=parent
        )
        if created:
            category.save()

        for food in category_foods(table, column):
            cassignment, created = WikiCategoryAssignment.objects.get_or_create(
                food=food, category=category)
            if created:
                cassignment.save()
            passignment, created = WikiCategoryAssignment.objects.get_or_create(
                food=food, category=parent)
            if created:
                passignment.save()


def category_name(table):
    # scrapes the preceeding H2 text as the category name
    helpers.remove_superscripts(table)

    for sibling in table.previous_siblings:
        if sibling.name == 'h2':
            return helpers.scrub_string(sibling.text)


def category_foods(table, column=1):
    foods = []
    for anchor in [row.select_one(f'td:nth-child({column}) a') for row in table.select('tbody tr')]:
        if anchor and 'redlink=1' not in anchor["href"]:
            foods.append(food_page.create_food_from_anchor(anchor))
    return foods


def category_description(table):
    # scrapes the preceeding paragraph as a description of the category
    helpers.remove_superscripts(table)

    for sibling in table.previous_siblings:
        if sibling.name == 'p':
            return helpers.scrub_string(sibling.text)
