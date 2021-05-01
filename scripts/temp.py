# from unsplash.unsplash_api import get_unsplash_photos
# from pexels.pexels_api import get_pexels_photos
# from pixabay.pixabay_api import get_pixabay_photos
# from wikipedia.helpers import scrub_string, remove_superscripts
# from wikipedia import wiki_api, helpers
# from pydash import py_
# import re
# from review.models import WikiFood, WikiFoodName


# def get_names(soup):
    
#     return {
#         # remove parenthesis and "as food" suffix
#         'page_title': scrub_string(re.sub(r" ?\([^)]+\)", "", soup.find('h1').text)).replace(' as food', ''),
#         'scientific': get_scientific_name(soup),
#         'infobox_name': get_infobox_name(soup),
#         'bolds': get_bolded_names(soup)
#     }


# def best_guess_common_name(names):
    
#     if not names.get('scientific'): return names.get('page_title')
#     if names.get('scientific') != names.get('page_title'): return names.get('page_title')
#     if names.get('scientific') != names.get('infobox_name'): return names.get('infobox_name')
#     try:
#         if names.get('scientific') != names.get('bolds')[0]: return names.get('bolds')[0]
#     except: pass
#     return names.get('page_title')


# def get_bolded_names(soup):
#     # other names for the food are bolded in the first paragraph
#     paragraphs = soup.select('.mw-parser-output p:not(.mw-empty-elt)')
#     # firstParagraphBolds = paragraphs[0].select('b')
#     firstParagraph = paragraphs[0]
#     # print('firstParagraph')
#     # print(firstParagraph)
#     aliasIndicators = ['known as', 'common name']
#     if py_.some(aliasIndicators, lambda l: l in firstParagraph.text.lower()):
#         return filter(None, py_.uniq(py_.map(firstParagraph.select('b'), lambda b: b.text)))


# def get_infobox_name(soup):
#     # the info box appears in the top right and highlight a name in green at the top
#     infobox_name = soup.select_one('.mw-parser-output table.infobox th i')
#     if infobox_name:
#         return scrub_string(infobox_name.text)


# def get_scientific_name(soup):
#     # The scientific name can be found in the infobox
#     binomial = soup.select_one('.mw-parser-output table.infobox .binomial')
#     if binomial:
#         return scrub_string(binomial.select_one('i').text)
#     else:
#         return get_scientific_name_from_table(soup)


# def get_scientific_name_from_table(soup):
#     # In many cases there is a full table of the scientific taxonomy heirarchy
#     for row in soup.select('table.infobox tr'):
#         lower = row.text.lower()

#         if 'genus' in lower and not 'subgenus' in lower:
#             genus = row.select('td')[1].text.strip()
#             abbrevation = f'{genus[0].upper()}.'

#         if 'species' in lower and not 'subspecies' in lower:
#             species = row.select('td')[1].text.replace(abbrevation, '')
#             species = re.sub(r'^.*?×', '×', species).replace('×', '').strip()

#     try:
#         return f'{genus} {species}'
#     except:
#         return None


# def get_description(soup):
#     description = ''

#     # looks through the table of contents for any food-related sections
#     for anchor in soup.select('#toc a'):

#         foodSections = ['As food', 'culinary', 'Culinary', 'consumption', 'Consumption', 'Food']
#         if py_.some(foodSections, lambda l: l in anchor.text):

#             header = soup.find(id=anchor['href'][1:]).parent

#             for sib in header.next_siblings:
#                 if sib.name == 'p':
#                     description += sib.text
#                 if sib.name == header.name:
#                     break

#             return scrub_string(description)

#     # If there are no dedicated food sections, just get the intro paragraphs
#     for child in soup.select_one('.mw-parser-output').children:
#         if child.name in ['h1', 'h2', 'h3']:
#             break
#         if child.name == 'p':
#             description += child.text
#     return scrub_string(description)


# def store_names(food, names):
#     WikiFoodName.objects.get_or_create(
#         name=names.get('page_title'), 
#         food=food,
#         type=WikiFoodName.NameType.PAGETITLE
#     )[0].save()
#     if names.get('infobox_name'): WikiFoodName.objects.get_or_create(
#         name=names.get('infobox_name'), 
#         food=food,
#         type=WikiFoodName.NameType.INFOBOX
#     )[0].save()
#     if names.get('scientific'): WikiFoodName.objects.get_or_create(
#         name=names.get('scientific'), 
#         food=food,
#         type=WikiFoodName.NameType.SCIENTIFIC
#     )[0].save()

#     if names.get('bolds'): 
#         for bold in names.get('bolds'):
#             bold = WikiFoodName.objects.get_or_create(
#                 name=bold,
#                 food=food,
#                 type=WikiFoodName.NameType.BOLD
#             )[0].save()



# def run():
#     for page in [
#         'https://en.wikipedia.org/wiki/Bouea_macrophylla',
#         'https://en.wikipedia.org/wiki/Garcinia_gummi-gutta',
#         'https://en.wikipedia.org/wiki/Calamansi',
#         'https://en.wikipedia.org/wiki/Boysenberry',
#         'https://en.wikipedia.org/wiki/Chicken_as_food',
#         'https://en.wikipedia.org/wiki/Scallop',
#         'https://en.wikipedia.org/wiki/Lamb_and_mutton',
#         'https://en.wikipedia.org/wiki/Venison'
#     ]: scrape_wiki_food(page)
