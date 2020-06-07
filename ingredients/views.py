from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView, UpdateView
from ingredients.models import Ingredient
from ingredients.models import IngredientForm
from django.urls import reverse_lazy


def index(request):
    """ Index page """
    context = {}
    return render(request, 'ingredients/index.html', context)


class IngredientSaveView(DetailView):
    model = Ingredient
    template_name = 'ingredients/ingredient_save.html'


class IngredientEditView(UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'ingredients/ingredient_edit.html'
    success_url = reverse_lazy('ingredient')


class IngredientView(DetailView):
    model = Ingredient
    template_name = 'ingredients/ingredient.html'


class IngredientListView(ListView):
    model = Ingredient
    template_name = 'ingredients/ingredient_list.html'

    def get_queryset(self):
         """
         Excludes any questions that aren't published yet.
         """
         return Ingredient.objects.filter() 


