from _config.settings import BASE_DIR
from review.models import Scrapable, WikiCategory, WikiCategoryAssignment
import json
from django.contrib.auth.models import User;
from django.core.management import call_command
from wikipedia import food_page, helpers
import subprocess
from pathlib import Path
import time

def run():
  
  # subprocess.Popen(f'rm {BASE_DIR}/db.sqlite3', shell=True)
  # subprocess.Popen(f'rm -rfv {BASE_DIR}/review/migrations', shell=True)  
  # subprocess.Popen(f'mkdir {BASE_DIR}/review/migrations', shell=True)
  # subprocess.Popen(f'touch {BASE_DIR}/review/migrations/__init__.py', shell=True)
  
  # call_command("makemigrations", interactive=False)
  # call_command("migrate", interactive=False)


  try:
    User.objects.create_superuser('n8', 'natmay@umich.edu', 'Mj39lK9sy')
  except: 
    print('user already exists')

  scrappable_file = open(f'{BASE_DIR}/wikipedia/scrappable.json', 'r')
  scrappables = json.loads(scrappable_file.read())
  scrappable_file.close()

  for page in scrappables.get('category_pages'):
    Scrapable.objects.get_or_create(
      name=page[0],
      url=page[1],
      type=page[2],
      column=page[3],
      isCategory=True,
    )[0].save()

  for name, details in scrappables.get('manual_categories').items():
    
    category, created = WikiCategory.objects.get_or_create(
        name = name,
        description = helpers.scape_description(details.get('page_url')),
        wiki_url = details.get('page_url'),
    )
    for food in details.get('foods'):
      food = food_page.scrape_wiki_food(food)
      assign, created = WikiCategoryAssignment.objects.get_or_create(
        food=food,
        category=category
      )
      if created: assign.save()
    

  # for category in scrappables.get('dishes'):
    # print(category[0])
