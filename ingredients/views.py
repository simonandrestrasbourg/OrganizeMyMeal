from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView, UpdateView, CreateView
from ingredients.models import Ingredient, IngredientForm
from django.urls import reverse_lazy


class IngredientView(DetailView):
    model = Ingredient
    template_name = 'ingredients/ingredient.html'
    success_url = reverse_lazy('ingredients:ingredient-list')
    form_class = IngredientForm


class IngredientListView(ListView):
    model = Ingredient
    template_name = 'ingredients/ingredient_list.html'

    def get_queryset(self):
         """
         Excludes any questions that aren't published yet.
         """
         return Ingredient.objects.filter() 


class IngredientNewView(CreateView):
    model = Ingredient
    template_name = 'ingredients/ingredient_new.html'
    fields = ['name', 'type', 'unit', 'conservation_day']
    success_url = reverse_lazy('ingredients:ingredient-list')


class IngredientEditView(UpdateView):
    model = Ingredient
    template_name = 'ingredients/ingredient_edit.html'
    success_url = reverse_lazy('ingredients:ingredient-list')
    form_class = IngredientForm