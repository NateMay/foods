from django import forms
from review.models import Scrapable, WikiCategory, WikiFood, UsdaWikiPairing
from django.contrib.admin.widgets import FilteredSelectMultiple


class FoodForm(forms.Form):
    
    name = forms.CharField(max_length=200, required=True)
    description = forms.CharField(max_length=30000, widget=forms.Textarea(attrs={'cols': 30, 'rows': 20}))
    
    
    # categories = FilteredSelectMultiple("Categories", is_stacked=False)
    categories = forms.ModelMultipleChoiceField(queryset=WikiCategory.objects.all(),
                                                          label="Something",
                                                          widget=FilteredSelectMultiple("Categories", is_stacked=False),
                                                          )
    img_src = forms.CharField(max_length=1000, required=True)
    usda_food= forms.CharField(max_length=20, required=True)
    wiki_url = forms.CharField(max_length=1000, required=True)
    names: FilteredSelectMultiple("Names", is_stacked=False)
    scientific_name = forms.CharField(max_length=500, required=True)

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',), }
        js = ('/admin/jsi18n',)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = WikiCategory
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'cols': 30, 'rows': 20}),
            'parent_category': forms.Select(attrs={'class':'form-control'})
            # 'categories': FilteredSelectMultiple("Categories", is_stacked=False)
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
    ("table_categories", "Several Tables of Categories"),
    ("ul_categories", "Unordered List"),
    ("single_table_category", "Single Table"),
)


class CatScrapableForm(forms.ModelForm):
    class Meta:
        model = Scrapable
        fields = ['name', 'url', 'column', 'type']
        widgets = {
            'type': forms.Select(choices=PAGE_TYPE_CHOICES)
        }
