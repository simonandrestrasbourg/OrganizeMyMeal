from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import DetailView
from recipes.models import Ingredient


def index(request):
    """ Index page """
    context = {}
    return render(request, 'recipes/index.html', context)


class IngredientView(DetailView):
    model = Ingredient

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredient_list'] = Ingredient.objects.all()
        return context
