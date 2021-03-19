from django.contrib import admin

from foods.models import WikiScrapeCategory, WikiScrapeFood

admin.site.register(WikiScrapeCategory)
admin.site.register(WikiScrapeFood)