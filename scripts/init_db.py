from _config.settings import BASE_DIR
from review.models import Scrapable
import json
from django.contrib.auth.models import User;
from django.core.management import call_command
import subprocess
from pathlib import Path
import time

def run():
  
  subprocess.Popen(f'rm {BASE_DIR}/db.sqlite3', shell=True)
  subprocess.Popen(f'rm -rfv {BASE_DIR}/review/migrations', shell=True)  
  subprocess.Popen(f'mkdir {BASE_DIR}/review/migrations', shell=True)
  subprocess.Popen(f'touch {BASE_DIR}/review/migrations/__init__.py', shell=True)
  
  call_command("makemigrations", interactive=False)
  time.sleep(2) 
  call_command("migrate", interactive=False)
  # proc.terminate()

  try:
    User.objects.create_superuser('n8', 'natmay@umich.edu', 'Mj39lK9sy')
  except: 
    print('user already exists')

  scrappable_file = open(f'{BASE_DIR}/scrape/scrappable.json', 'r')
  scrappables = json.loads(scrappable_file.read())
  scrappable_file.close()

  for page in scrappables.get('category_pages'):
    Scrapable(
      name=page[0],
      url=page[1],
      type=page[2],
      column=page[3],
      isCategory=True,
    ).save()
    

# TODO
# for category in scrappables_dict.get('manual_categories'):
# for category in scrappables_dict.get('dishes'):
