from django.contrib import admin
from .models import IngredientUnit, IngredientType, Ingredient


admin.site.register(IngredientUnit)
admin.site.register(IngredientType)
admin.site.register(Ingredient)
