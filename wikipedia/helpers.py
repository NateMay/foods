import re
from pydash import py_
from review.models import WikiFoodName
from wikipedia import wiki_api

WIKI_BASE = 'https://en.wikipedia.org'


def scrub_string(value):
    # gets a content of text ready fo the database
    remove_edit_btn = value.replace('[edit]', '')
    to_single_quotes = remove_edit_btn.replace('"', "'")
    remove_citations = re.sub('\[\d{0,2}\]', '', to_single_quotes)
    return remove_citations.strip()


def remove_superscripts(soup):
    for superscript in soup.select('sup'):
        superscript.extract()


def anchor_link(anchor):
    # handles irregularity in href structures
    return anchor["href"] if 'http' in anchor["href"] else add_base_url(anchor["href"])


def add_base_url(route):
    # composes href into a link
    return f'{WIKI_BASE}{route}'


def description_from_route(route):
    # uses anchor tag to scrape the description from a food page
    return scape_description(add_base_url(route))


def scape_description(page_url, soup=None):
    # scrapes the description from a food page

    if 'redlink=1' in page_url:
        return ''

    if not soup:
        soup = wiki_api.request(page_url)

    as_food = soup.select_one("#As_food")

    return scrape_as_food_section(soup, as_food) if as_food else scrape_primary_page_description(soup)


def scrape_as_food_section(soup, as_food):
    # Pages like "Chicken" are an animal and a food...
    # This picks out the Chicken "As Food" section
    return get_section_paragraphs(soup, as_food.parent.next_siblings)


def scrape_primary_page_description(soup):
    # When there is not "As Food" section, get the main page desc.
    content = soup.select_one('.mw-parser-output')
    return get_section_paragraphs(soup, content.children) if content else ''


def isHeader(el):
    return el.name == 'h2' or el.name == 'h3'


def get_section_paragraphs(soup, iterable):
    # Conacatenates the <p> text content for any page section
    paras = []

    for element in iterable:
        if element.name == 'p':
            paras.append(element.text)
        elif element == soup.find(id="toc") or len(paras) >= 4 or isHeader(element):
            break

    return scrub_string('\n'.join(paras))


def add_https(func):
    def inner(soup):
        src = func(soup)
        if not src:
            return None
        else:
            return f'https://{src}'
    return inner


def pluck_bigs(image):
    return int(image["width"]) > 120 and int(image["height"]) > 120


@add_https
def scape_primary_image(soup):
    # scrapes the url of the first image

    if not soup.select_one('.mw-parser-output'):
        return ''
    as_food = soup.select_one("#As_food")

    if as_food:
        return as_food.find_next('img')['src'][2:]
    else:
        bigs = list(filter(pluck_bigs, soup.select(
            '.mw-parser-output img[width]')))

        if len(bigs) == 0:
            return ''

        first = bigs[0]

        return first['src'][2:] if first and first['src'] else ''


def get_names(soup):
    return {
        # remove parenthesis and "as food" suffix
        'page_title': scrub_string(re.sub(r" ?\([^)]+\)", "", soup.find('h1').text)).replace(' as food', ''),
        'scientific': get_scientific_name(soup),
        'infobox_name': get_infobox_name(soup),
        'bolds': get_bolded_names(soup)
    }


def best_guess_common_name(names):
    # perhaps this could be improved with machine learning,
    # probably decision tree: depth ~ 3
    scientific = names.get('scientific')
    page_title = names.get('page_title')
    infobox = names.get('infobox_name')
    bolds = names.get('bolds')

    if not scientific:
        return page_title

    # if not scientific name is found
    if scientific != page_title:
        return page_title
    if scientific != infobox:
        return infobox
    try:
        if scientific != bolds[0]:
            return bolds[0]
    except:
        pass
    return page_title


def get_bolded_names(soup):
    # other names for the food are bolded in the first paragraph
    paragraphs = soup.select('.mw-parser-output p:not(.mw-empty-elt)')
    firstParagraph = paragraphs[0]
    aliasIndicators = ['known as', 'common name']
    if py_.some(aliasIndicators, lambda l: l in firstParagraph.text.lower()):
        return filter(None, py_.uniq(py_.map(firstParagraph.select('b'), lambda b: b.text)))


def get_infobox_name(soup):
    # the info box appears in the top right and highlight a name in green at the top
    infobox_name = soup.select_one('.mw-parser-output table.infobox th i')
    if infobox_name:
        return scrub_string(infobox_name.text)


def get_scientific_name(soup):
    # The scientific name can be found in the infobox
    binomial = soup.select_one('.mw-parser-output table.infobox .binomial')
    if binomial:
        return scrub_string(binomial.select_one('i').text)
    else:
        return get_scientific_name_from_table(soup)


def get_scientific_name_from_table(soup):
    # In many cases there is a full table of the scientific taxonomy heirarchy
    for row in soup.select('table.infobox tr'):
        lower = row.text.lower()
        tds = row.select('td')
        if len(tds) < 2: break

        if 'genus' in lower and not 'subgenus' in lower:
            genus = tds[1].text.strip()
            abbrevation = f'{genus[0].upper()}.'

        if 'species' in lower and not 'subspecies' in lower:
            species = tds[1].text.replace(abbrevation, '')
            species = re.sub(r'^.*?×', '×', species).replace('×', '').strip()

    try:
        return f'{genus} {species}'
    except:
        return None


def get_description(soup):
    description = ''

    # looks through the table of contents for any food-related sections
    for anchor in soup.select('#toc a'):

        foodSections = ['As food', 'culinary', 'Culinary',
                        'consumption', 'Consumption', 'Food']
        if py_.some(foodSections, lambda l: l in anchor.text):

            header = soup.find(id=anchor['href'][1:]).parent

            for sib in header.next_siblings:
                if sib.name == 'p':
                    description += '\n'
                    description += sib.text
                if sib.name == header.name:
                    break

            return scrub_string(description)

    # If there are no dedicated food sections, just get the intro paragraphs
    for child in soup.select_one('.mw-parser-output').children:
        if child.name in ['h1', 'h2', 'h3']:
            break
        if child.name == 'p':
            description += child.text
    return scrub_string(description)


def store_names(food, names):
    WikiFoodName.objects.get_or_create(
        name=names.get('page_title'),
        food=food,
        type=WikiFoodName.NameType.PAGETITLE
    )[0].save()
    if names.get('infobox_name'):
        WikiFoodName.objects.get_or_create(
            name=names.get('infobox_name'),
            food=food,
            type=WikiFoodName.NameType.INFOBOX
        )[0].save()
    if names.get('scientific'):
        WikiFoodName.objects.get_or_create(
            name=names.get('scientific'),
            food=food,
            type=WikiFoodName.NameType.SCIENTIFIC
        )[0].save()

    if names.get('bolds'):
        for bold in names.get('bolds'):
            bold = WikiFoodName.objects.get_or_create(
                name=bold,
                food=food,
                type=WikiFoodName.NameType.BOLD
            )[0].save()
