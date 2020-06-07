from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import DetailView, ListView
from recipes.models import Ingredient


def index(request):
    """ Index page """
    context = {}
    return render(request, 'recipes/index.html', context)


class IngredientView(DetailView):
    model = Ingredient
    template_name = 'recipes/ingredient.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class IngredientListView(ListView):
    model = Ingredient
    template_name = 'recipes/ingredient_list.html'

    def get_queryset(self):
         """
         Excludes any questions that aren't published yet.
         """
         return Ingredient.objects.filter() 


