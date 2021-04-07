from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class ReviewLanding(LoginRequiredMixin, View):
    def get(self, req):
        context = {}
        return render(req, 'review/landing.html', context)
