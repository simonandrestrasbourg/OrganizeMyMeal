from django.db import models
from ingredients.models import Ingredient


class Recipe(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=200, unique=True)
    duration = models.IntegerField()
    short_description = models.TextField()
    content = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', related_name='ingredient')


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='recipe_ingredient', on_delete=models.SET_NULL, null=True)
    ingredient = models.ForeignKey(Ingredient, related_name='recipe_ingredient', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField()
