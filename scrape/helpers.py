from scripts.food_scrape.wikipedia import wiki_http as http
from scripts.food_scrape.pages import WIKI_BASE
import re


def scrub_string(value):
    # gets a content of text ready fo the database
    remove_edit_btn = value.replace('[edit]', '')
    to_single_quotes = remove_edit_btn.replace('"', "'")
    remove_citations = re.sub('\[\d{0,2}\]', '', to_single_quotes)
    return remove_citations.strip()


def remove_superscripts(table):
    for superscript in table.select('sup'):
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
        soup = http.request(page_url)

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
        bigs = list(filter(pluck_bigs, soup.select('.mw-parser-output img[width]')))

        if len(bigs) == 0:
            return ''

        first = bigs[0]

        return first['src'][2:] if first and first['src'] else ''
