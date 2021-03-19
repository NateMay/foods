from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.urls import reverse_lazy

# from foods.forms import
# from foods.models import Food, Category

class FoodLanding(LoginRequiredMixin, View):
    # def get(self, req):
    #     return render(req, 'cats/cat_list.html', {
    #         'count': Breed.objects.all().count(),
    #         'cat_list': Cat.objects.all()
    #     })
    def get(self, req):
        context = {}
        return render(req, 'foods/landing.html', context)