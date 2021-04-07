import re
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from pydash import py_
from review.forms import  FoodForm
from review.models import WikiFood, WikiCategory
from review.unsplash.unsplash_api import get_images

from scripts.food_scrape.pages import PAGES_TO_SCRAPE


class FoodListView(ListView):
    template_name = 'review/scraped_food_list.html'
    model = WikiFood

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        term = self.request.GET.get('filter')
        if term:
            context['term'] = term
            context['wikifood_list'] = py_.filter(
                context['wikifood_list'], lambda food: term in food.name.lower())
        return context


class FoodMetadataUpdate(LoginRequiredMixin, View):
    template_name = 'review/food_metadata_form.html'

    def get(self, request, pk):
        food = WikiFood.objects.get(pk=pk)
        return render(request, self.template_name, {
            'form': FoodForm(instance=get_object_or_404(WikiFood, id=pk)),
            'food': food,
            'images': get_images(re.sub(r'[^A-Za-z0-9 ]+', '', food.name), 1)
        })

    def post(self, request, pk=None):

        food = get_object_or_404(WikiFood, id=pk)
        form = FoodForm(request.POST, instance=food)
        form.categories = None
        print(form)
        if not form.is_valid():
            return render(request, self.template_name, {
                'form': form,
                'food': food
            })

        food = form.save(commit=False)
        food.categories.set(form.cleaned_data['categories'])
        food.save()

        return redirect(reverse_lazy('review:complete_food', kwargs={'pk': pk}))



class CategoryList(ListView):
    template_name = 'review/category_list.html'
    model = WikiCategory

