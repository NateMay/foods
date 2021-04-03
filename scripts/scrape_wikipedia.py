#################################
# Name: Nate May
# Uniqname: natmay
# https://en.wikipedia.org/wiki/Lists_of_foods
#################################


from scripts.food_scrape import db

# scraping script for each page type
from scripts.food_scrape.page_scripts import ul_categories, table_categories, single_table_category, manual_categories

__version__ = '0.1.0'

# Scraping control flow - Allows me to "turn off" portions of
# scraping and database logic during development
SHOULD = {
    'reset_db': True,

    # # sections of the scraping logic
    # 'single_table_category': True,  # 1175 foods
    # 'manual_categories': True,  # 30 foods
    'table_categories': True,  # 836 foods
    # 'ul_categories': True, # 772 foods

    # 'dishes': False # not implemented
}

def run():


    if SHOULD.get('reset_db'):
        db.drop_tables()
        db.create_tables()

    if SHOULD.get('single_table_category'):
        db.insert_all(single_table_category.scrape())

    if SHOULD.get('manual_categories'):
        db.insert_all(manual_categories.scrape())

    if SHOULD.get('table_categories'):
        print('yes')
        db.insert_all(table_categories.scrape())

    if SHOULD.get('ul_categories'):
        db.insert_all(ul_categories.scrape())

    # if SHOULD.get('dishes'):
    #     db.insert_all(dishes.scrape())

    exit()
