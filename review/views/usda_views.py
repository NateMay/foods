from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from pydash import py_
from review.forms import UsdaPairForm
from review.models import UsdaWikiPairing, WikiFood

from review.usda.usda_http import get_usda_results, make_usda_food



class UsdaPairingView(View):

    template_name = 'review/usda_pairing_form.html'
    model = WikiFood

    def get(self, request, pk):
        food = WikiFood.objects.get(pk=pk)

        return render(request, self.template_name, {
            'food': food,
            'form': UsdaPairForm(),
            'usda_foods': get_usda_results(food.name)
        })

    def post(self, request, pk=None):

        food = get_object_or_404(WikiFood, id=pk)
        form = UsdaPairForm(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {
                'form': form,
                'food': food,
                'usda_foods': get_usda_results(food.name)
            })

        UsdaWikiPairing(
            wiki_food=food,
            usda_food=make_usda_food(request.POST.get('fdc'))
        ).save()

        food.paired = True

        food.save()

        return redirect(reverse_lazy('review:complete_food', kwargs={'pk': pk}))
        # return redirect(reverse_lazy('review:review_landing'))
