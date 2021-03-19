from django.db import models
from django.core.validators import MinLengthValidator

# Many-to-many relationships - https://docs.djangoproject.com/en/3.1/topics/db/examples/many_to_many/

class WikiScrapeCategory(models.Model):
    name = models.CharField(
            max_length=200,
            blank=False,
            validators=[MinLengthValidator(2, "Category names must be longer than 1 character")]
    )
    description = models.CharField(max_length=30000)
    wiki_url = models.CharField(max_length=1000)
    parent_category = models.ForeignKey('WikiScrapeCategory', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class WikiScrapeFood(models.Model):
    name = models.CharField(
            max_length=200,
            blank=False,
            validators=[MinLengthValidator(2, "Food names must be longer than 1 character")]
    )
    description = models.CharField(max_length=30000)
    wiki_url = models.CharField(max_length=1000)
    img_src = models.CharField(max_length=1000)
    categories = models.ManyToManyField(WikiScrapeCategory)

    def __str__(self):
        return self.name