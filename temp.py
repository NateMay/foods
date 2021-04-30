

from wikipedia import wiki_api
from wikipedia.helpers import scrub_string, remove_superscripts
from pydash import py_
import re


def getNames(soup):
    return {
        'pageTitle': scrub_string(soup.find('h1').text).replace(' as food', ''),
        'scientific': getScientificName(soup),
        'infoboxName': getInfoboxName(soup),
        'bolds': getBoldedNames(soup)
    }


def getBoldedNames(soup):
    # other names for the food are bolded in the first paragraph
    paragraphs = soup.select('.mw-parser-output p:not(.mw-empty-elt)')
    firstParagraphBolds = paragraphs[0].select('b')
    return py_.uniq(py_.map(firstParagraphBolds, lambda b: b.text))


def getInfoboxName(soup):
    # the info box appears in the top right and highlight a name in green at the top
    infoboxName = soup.select_one('.mw-parser-output table.infobox th i')
    if infoboxName:
        return scrub_string(infoboxName.text)


def getScientificName(soup):
    # The scientific name can be found in the infobox
    binomial = soup.select_one('.mw-parser-output table.infobox .binomial')
    if binomial:
        return scrub_string(binomial.select_one('i').text)
    else:
        return getScientificNameFromTable(soup)


def getScientificNameFromTable(soup):
    # In many cases there is a full table of the scientific taxonomy heirarchy
    for row in soup.select('table.infobox tr'):
        lower = row.text.lower()

        if 'genus' in lower and not 'subgenus' in lower:
            genus = row.select('td')[1].text.strip()
            abbrevation = f'{genus[0].upper()}.'

        if 'species' in lower and not 'subspecies' in lower:
            species = row.select('td')[1].text.replace(abbrevation, '')
            species = re.sub(r'^.*?×', '×', species).replace('×', '').strip()

    try:
        return f'{genus} {species}'
    except:
        return None


def getDescription(soup):
    description = ''

    # looks through the table of contents for any food-related sections
    for anchor in soup.select('#toc a'):

        foodSections = ['as food', 'culinary', 'consumption']
        if py_.some(foodSections, lambda l: l in anchor.text.lower()):

            header = soup.find(id=anchor['href'][1:]).parent

            for sib in header.next_siblings:
                if sib.name == 'p':
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


#############
pages = [
    # 'https://en.wikipedia.org/wiki/Bouea_macrophylla',
    # 'https://en.wikipedia.org/wiki/Garcinia_gummi-gutta',
    # 'https://en.wikipedia.org/wiki/Calamansi',
    # 'https://en.wikipedia.org/wiki/Boysenberry',
    # 'https://en.wikipedia.org/wiki/Chicken_as_food',
    'https://en.wikipedia.org/wiki/Scallop'
]

# for page in pages:
#     soup = wiki_api.request(page)
#     remove_superscripts(soup)
#     print(getDescription(soup))

# for names in getNames(soup):
# print(getNames(soup))
# getSection(soup, 'Culinary')

# from pexels.pexels_api import get_images
from pixabay.pixabay_api import get_images

for image in get_images('apple'):
    print(image)
