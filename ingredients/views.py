from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView, UpdateView, CreateView
from ingredients.models import Ingredient, IngredientForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin


class IngredientView(PermissionRequiredMixin, DetailView):
    model = Ingredient
    template_name = 'ingredients/ingredient.html'
    success_url = reverse_lazy('ingredients:ingredient-list')
    form_class = IngredientForm
    permission_required = ('ingredients.view_ingredient',)


class IngredientListView(PermissionRequiredMixin, ListView):
    model = Ingredient
    template_name = 'ingredients/ingredient_list.html'
    permission_required = ('ingredients.view_ingredient',)

    def get_queryset(self):
         """
         Excludes any questions that aren't published yet.
         """
         return Ingredient.objects.filter() 


class IngredientNewView(PermissionRequiredMixin, CreateView):
    model = Ingredient
    template_name = 'ingredients/ingredient_new.html'
    fields = ['name', 'type', 'unit', 'conservation_day']
    success_url = reverse_lazy('ingredients:ingredient-list')
    permission_required = ('ingredients.view_ingredient', 'ingredients.add_ingredient',)


class IngredientEditView(PermissionRequiredMixin, UpdateView):
    model = Ingredient
    template_name = 'ingredients/ingredient_edit.html'
    success_url = reverse_lazy('ingredients:ingredient-list')
    form_class = IngredientForm
    permission_required = ('ingredients.view_ingredient', 'ingredients.change_ingredient',)
