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
