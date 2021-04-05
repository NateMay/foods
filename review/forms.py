from django import forms
from review.models import WikiScrapeFood, UsdaWikiPairing
from django.contrib.admin.widgets import FilteredSelectMultiple


class FoodForm(forms.ModelForm):

    class Meta:
        model = WikiScrapeFood
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
class ScrapeCategoryForm(ScrapeFoodForm):
    name = forms.CharField(max_length=1000, required=True)
    category_scrape_type = forms.Select(choices = SCRAPE_TYPE_CHOICES)
