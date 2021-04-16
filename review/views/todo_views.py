from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class TodoPage(LoginRequiredMixin, View):
    def get(self, req):
        return render(req, 'review/todo.html', {
            'todos': [
                {
                    'task': 'Improve scraping',
                    'children': [
                      'Scrape names from url fragments',
                      'Look for common name and scientific name',
                      'Refined the description scrape to remove pronunciation ugliness',
                      'Figure out why some foods are duplicate',
                      'Non-destructive page scraping',
                      'Fix mushroom scrape'
                    ]
                },
                {
                    'task': 'Find more souces of food data',
                    'children': [
                      'Check data policy after IP class',
                      'Store alternative names and descriptions',
                    ]
                },
                {
                    'task': 'Images',
                    'children': [
                      'Create Images table'
                      'Add more photo API',
                      'Auto crop?',
                    ]
                },
                {
                    'task': 'Use Machine Learning to:',
                    'children': [
                      'Pick the best Image',
                      'Pick the best Name',
                      'Pick the best Description',
                      'Pair the nutrition data'
                    ]
                },
                {
                    'task': 'Algolia / Index',
                    'children': [
                       'Add categories to index',
                       'Add non-destructive update option'
                    ]
                },
                {
                    'task': 'Batch',
                    'children': [
                      'Make batch scraping non-blocking',
                      'Provide some sort of loading indcator or bage icon to indicate complete'
                    ]
                },
                {
                    'task': 'Scrape recipes',
                    'children': [
                      'Pair the recipe ingrediaents with foods',
                      'Use recipes to determine default food portion'
                    ]
                },
            ]
        })
