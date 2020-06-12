from django.contrib import admin
from .models import Recipe, RecipeIngredientRel

admin.site.register(Recipe)
admin.site.register(RecipeIngredientRel)