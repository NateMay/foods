import re
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from pydash import py_
from review.forms import FoodForm, CategoryForm
from review.models import PexelsPhoto, PixabayPhoto, UnsplashPhoto, WikiFood, WikiCategory, WikiFoodName
from unsplash.unsplash_api import get_unsplash_photos
from itertools import chain

class FoodListView(LoginRequiredMixin, ListView):
    template_name = 'review/scraped_food_list.html'
    model = WikiFood

    def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        context = {
            'wikifood_list':WikiFood.objects.all().order_by('name')
        }
        
        term = self.request.GET.get('filter') or ''
        if term:
            context['term'] = term
            context['wikifood_list'] = py_.filter(
                context['wikifood_list'], lambda food: term.lower() in food.name.lower())
        return context


class CategoriesListView(LoginRequiredMixin, ListView):
    template_name = 'review/scraped_category_list.html'
    model = WikiCategory

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        term = self.request.GET.get('filter') or ''
        if term:
            context['term'] = term
            context['wikicategory_list'] = py_.filter(
                context['wikicategory_list'], lambda category: term.lower() in category.name.lower())
        return context


class FoodMetadataUpdate(LoginRequiredMixin, View):
    template_name = 'review/food_metadata_form.html'

    def get(self, request, pk):
        food = WikiFood.objects.get(pk=pk)
        
        return render(request, self.template_name, {
            
            'form': FoodForm(initial={
                'name': food.name,
                'description':food.description,
                'categories':food.categories.all(),
                'img_src':food.img_src,
                'wiki_url':food.wiki_url,
                'names':self.common_names(pk),
                'scientific_name':self.scientific_name(pk)
            }),
            'food': food,
            'images': self.all_images(food),
            # 'images': get_unsplash_photos(re.sub(r'[^A-Za-z0-9 ]+', '', food.name), 1)
        })

    def common_names(self, pk):
        return WikiFoodName.objects.filter(food=pk)
    
    def scientific_name(self, pk):
        name = WikiFoodName.objects.filter(food=pk, type='SC')
        return name[0] if name and name[0] else ''

    def all_images(self, food):
        return list(chain(
            UnsplashPhoto.objects.filter(food_id=food.id),
            PexelsPhoto.objects.filter(food_id=food.id),
            PixabayPhoto.objects.filter(food_id=food.id)
        ))

    def post(self, request, pk=None):

        food = get_object_or_404(WikiFood, id=pk)
        form = FoodForm(request.POST, instance=food)
        form.categories = None
        if not form.is_valid():
            return render(request, self.template_name, {
                'form': form,
                'food': food
            })

        food = form.save(commit=False)
        food.categories.set(form.cleaned_data['categories'])
        food.reviewed = True
        food.save()

        # try:
        #     UsdaWikiPairing.objects.get(wiki_food=pk)
        #     return redirect(reverse_lazy('review:paired_food', kwargs={'pk': pk}))
        # except:
        return redirect(reverse_lazy('review:pair_usda', kwargs={'pk': pk}))


class CategoryMetadataUpdate(LoginRequiredMixin, View):
    template_name = 'review/category_metadata_form.html'

    def get(self, request, pk):
 
        return render(request, self.template_name, {
            'form': CategoryForm(instance=get_object_or_404(WikiCategory, id=pk)),
            'category': WikiCategory.objects.get(pk=pk),
        })

    def post(self, request, pk=None):

        category = get_object_or_404(WikiCategory, id=pk)
        form = CategoryForm(request.POST, instance=category)

        if not form.is_valid():
            return render(request, self.template_name, {
                'form': form,
                'category': category
            })

        category = form.save(commit=False)
        category.save()

        # try:
        #     UsdaWikiPairing.objects.get(wiki_category=pk)
        #     return redirect(reverse_lazy('review:paired_category', kwargs={'pk': pk}))
        # except:
        return redirect(reverse_lazy('review:wiki_category', kwargs={'pk': pk}))
