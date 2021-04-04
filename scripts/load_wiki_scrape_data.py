# python3 manage.py runscript load_wiki_scrape_data

from numpy import isnan
from review.models import WikiScrapeCategory, WikiScrapeFood, WikiCategoryAssignment, FdcCategory, UsdaFood, FdcCategoryAssignment, UsdaWikiPairing, UsdaNutrient, UsdaFoodMeasure
import pandas as pd
import sqlite3
from pydash import py_
import os

# https://docs.djangoproject.com/en/3.1/howto/legacy-databases/
# https://docs.djangoproject.com/en/3.1/ref/django-admin/#django-admin-inspectdb

# stores the category with the original id for later lookup
def rip_category_data(wiki_categories):
    categories = []
    for _, row in wiki_categories.iterrows():
        categories.append({
            'id': row.id,
            'category': WikiScrapeCategory.objects.get_or_create(
                name=row['name'],
                description=row['description'],
                wiki_url=row['wiki_url'])[0],
            'parent_id': int(row.parent_category) if ~isnan(row.parent_category) else None
        })
    return categories

# stores the food with the original id for later lookup


def rip_food_data(wiki_foods):
    foods = []
    for _, row in wiki_foods.iterrows():
        foods.append({
            'id': row.id,
            'food': WikiScrapeFood.objects.get_or_create(
                name=row['name'],
                description=row['description'],
                wiki_url=row['wiki_url'],
                img_src=row['image_src'])[0],
        })
    return foods


def delete_all():
    try:
        WikiScrapeCategory.objects.all().delete()
        WikiScrapeFood.objects.all().delete()
        WikiCategoryAssignment.objects.all().delete()
        FdcCategory.objects.all().delete()
        UsdaFood.objects.all().delete()
        FdcCategoryAssignment.objects.all().delete()
        UsdaWikiPairing.objects.all().delete()
        UsdaNutrient.objects.all().delete()
        UsdaFoodMeasure.objects.all().delete()
    except Exception:
        print('no object yet')
        pass


def run():
    # setup
    connection = sqlite3.connect(os.path.abspath(
        '.') + '/scraped_data.sqlite')
        
    delete_all()

    # intermediate data structures for bridging the M2M relationships
    categories = rip_category_data(pd.read_sql_query(
        "SELECT * from wiki_category", connection))

    foods = rip_food_data(pd.read_sql_query(
        "SELECT * from wiki_food", connection))

    # loop through wiki_food_category to create the Junction Table
    for _, row in pd.read_sql_query("SELECT * from wiki_food_category", connection).iterrows():

        a = WikiCategoryAssignment(
            # Use the id values in wiki_food_category to lookup the food and category
            # objects created in rip_category_data() & rip_food_data()
            food=py_.find(foods, lambda f: f.get('id')
                          == row.food_id).get('food'),
            category=py_.find(categories, lambda c: c.get(
                'id') == row.category_id).get('category'),
        )
        # !!! ERROR: django.db.utils.OperationalError: no such table: foods_categoryassignment
        a.save()
