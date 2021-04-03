from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from review.forms import FoodForm
from review.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from pydash import py_
import requests
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from review.models import WikiScrapeFood

ENDPOINT = 'https://api.nal.usda.gov/fdc/v1/foods/search'
APIKEY = 'NVguQkLzba5lX36C0GNpZBCyBAvtHZ5lLbxE5RKp'

NUTRIENT_SHORT_LIST = ['301', '303', '324', '601', '606', '203', '204', '208', '291', '307', '539', '605']

SOURCES = ['Survey (FNDDS)', 'SR Legacy', 'Foundation']
class ReviewLanding(LoginRequiredMixin, View):
    def get(self, req):
        context = {}
        return render(req, 'review/landing.html', context)


class FoodListView(ListView):
    model = WikiScrapeFood

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        term = self.request.GET.get('filter')
        if term:
            context['term'] = term
            context['wikiscrapefood_list'] = py_.filter(
                context['wikiscrapefood_list'], lambda food: term in food.name.lower())
        return context


class FoodView(DetailView):
    model = WikiScrapeFood

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        food_name = context['wikiscrapefood'].name

        context["usda_foods"] = requests.get(
            f'{ENDPOINT}?query={food_name}&api_key={APIKEY}'
        ).json().get('foods')

        context["usda_foods"] = py_.filter(context["usda_foods"], lambda f: f.get('dataType') in SOURCES)
        
        for food in context["usda_foods"]:
            food['short_list'] = py_.filter(food.get('foodNutrients'), lambda n: n.get('nutrientNumber') in NUTRIENT_SHORT_LIST)
        return context



class FoodUpdate(LoginRequiredMixin, View):
    template_name = 'review/wikiscrapefood_form.html'
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
            print('form.is_valid(): ', form.is_valid())
            print('errors: ', form.errors)
            return render(request, self.template_name, {
                'form': form,
                'food': food
            })

        food = form.save(commit=False)
        food.save()
        success_url = reverse_lazy('review:food_update', kwargs={'pk': pk})
        return redirect(self.success_url)
