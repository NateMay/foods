from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from review.models import WikiScrapeFood
from review.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from pydash import py_
import requests

# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.urls import reverse_lazy
# from review.forms import
# from review.models import Food, Category

class ReviewLanding(LoginRequiredMixin, View):
    def get(self, req):
        context = {}
        return render(req, 'review/landing.html', context)

class FoodListView(OwnerListView):
    model = WikiScrapeFood

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        term = self.request.GET.get('filter')
        if term:
            context['term'] = term
            context['wikiscrapefood_list'] = py_.filter(context['wikiscrapefood_list'], lambda food: term in food.name.lower())
        return context

class FoodView(OwnerDetailView):
    model = WikiScrapeFood

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        endPoint = 'https://api.nal.usda.gov/fdc/v1/foods/search'
        apiKey = 'NVguQkLzba5lX36C0GNpZBCyBAvtHZ5lLbxE5RKp'
        food = context['wikiscrapefood'].name
        term = self.request.GET.get('filter')
        context["usda_results"] = requests.get(f'{endPoint}?query={term or food}&api_key={apiKey}').json()
        print(context["usda_results"].get('foods'))
        return context
