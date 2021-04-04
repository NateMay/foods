from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from review.forms import FoodForm, UsdaPairForm
from review.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from pydash import py_
import requests
from django.urls import reverse_lazy
from review.usda.usda_http import get_usda_results, make_usda_food
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from review.models import WikiScrapeFood, UsdaWikiPairing

ENDPOINT = 'https://api.nal.usda.gov/fdc/v1/foods/search'
APIKEY = 'NVguQkLzba5lX36C0GNpZBCyBAvtHZ5lLbxE5RKp'

NUTRIENT_SHORT_LIST = ['301', '303', '324', '601', '606', '203', '204', '208', '291', '307', '539', '605']

SOURCES = ['Survey (FNDDS)', 'SR Legacy', 'Foundation']
class ReviewLanding(LoginRequiredMixin, View):
    def get(self, req):
        context = {}
        return render(req, 'review/landing.html', context)


class FoodListView(ListView):
    template_name = 'review/scraped_food_list.html'
    model = WikiScrapeFood

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        term = self.request.GET.get('filter')
        if term:
            context['term'] = term
            context['wikiscrapefood_list'] = py_.filter(
                context['wikiscrapefood_list'], lambda food: term in food.name.lower())
        return context


class UsdaPairingView(LoginRequiredMixin, View):
    
    template_name = 'review/usda_pairing_form.html'
    model = WikiScrapeFood

    def get(self, request, pk):
        food = WikiScrapeFood.objects.get(pk=pk)

        return render(request, self.template_name, {
            'food': food,
            'form': UsdaPairForm(),
            'usda_foods': get_usda_results(food.name)
        })

    def post(self, request, pk=None):

        food = get_object_or_404(WikiScrapeFood, id=pk)
        form = UsdaPairForm(request.POST)
    

        if not form.is_valid():
            return render(request, self.template_name, {
                'form': form,
                'food': food,
                'usda_foods': get_usda_results(food.name)
            })

        UsdaWikiPairing(
            wiki_food= food,
            usda_food= make_usda_food(request.POST.get('fdc'))
        ).save()

        food.paired = True

        food.save()
        
        return redirect(reverse_lazy('review:food_usda', kwargs={'pk': pk}))
        # return redirect(reverse_lazy('review:review_landing'))


class FoodMetadataUpdate(LoginRequiredMixin, View):
    template_name = 'review/food_metadata_form.html'
    success_url = reverse_lazy('review:foods')

    def get(self, request, pk):
        return render(request, self.template_name, {
            'form': FoodForm(instance=get_object_or_404(WikiScrapeFood, id=pk)),
            'food': WikiScrapeFood.objects.get(pk=pk),
        })
    

    def post(self, request, pk=None):

        food = get_object_or_404(WikiScrapeFood, id=pk)
        form = FoodForm(request.POST, instance=food)

        if not form.is_valid():
            return render(request, self.template_name, {
                'form': form,
                'food': food
            })

        food = form.save(commit=False)
        food.categories.set(form.cleaned_data['categories'])
        food.save()

        return redirect(reverse_lazy('review:food_metadata', kwargs={'pk': pk}))

