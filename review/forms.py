from django import forms
from review.models import WikiScrapeFood, WikiScrapeCategory
from django.contrib.admin.widgets import FilteredSelectMultiple


class FoodForm(forms.ModelForm):

    class Meta:
        model = WikiScrapeFood
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'cols': 30, 'rows': 20}),
            # 'categories': FilteredSelectMultiple("verbose name", is_stacked=False)
        }


    class Media:
        css = {'all': ('/static/admin/css/widgets.css',), }
        js = ('/admin/jsi18n',)
