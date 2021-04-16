from django.shortcuts import render
from django.views import View


class ReviewLanding(View):
    def get(self, req):
        context = {}
        return render(req, 'review/landing.html', context)

