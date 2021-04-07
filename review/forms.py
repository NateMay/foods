from django import forms
from review.models import Scrapable, WikiFood, UsdaWikiPairing
from django.contrib.admin.widgets import FilteredSelectMultiple


class FoodForm(forms.ModelForm):

    class Meta:
        model = WikiFood
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'cols': 30, 'rows': 20}),
            'categories': FilteredSelectMultiple("Categories", is_stacked=False)
        }

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',), }
        js = ('/admin/jsi18n',)

class UsdaPairForm(forms.Form):
    # food = forms.CharField(max_length=100)
    fdc = forms.CharField(max_length=100, required=True)


class ScrapeFoodForm(forms.Form):
    url = forms.CharField(max_length=1000, required=True)

SCRAPE_TYPE_CHOICES =(
    ("single", "Single Category"),
    ("table", "Single Table"),
    ("tables", "Tables"),
    ("list", "<ul> List"),
)


class QuickScrapeCategoryForm(ScrapeFoodForm):
    name = forms.CharField(max_length=1000, required=True)
    category_scrape_type = forms.Select(choices = SCRAPE_TYPE_CHOICES)


PAGE_TYPE_CHOICES = (
    ("table_categories", "Singl Table of Categories"),
    ("ul_categories", "Single Table"),
    ("single_table_category", "Tables"),
)


class CatScrapableForm(forms.ModelForm):
    class Meta:
        model = Scrapable
        fields = ['name', 'url', 'column', 'type']
        widgets = {
            'type': forms.Select(choices=PAGE_TYPE_CHOICES)
        }
