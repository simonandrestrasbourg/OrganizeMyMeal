from django.db import models
from ingredients.models import Ingredient


class Recipe(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=200, unique=True)
    duration = models.IntegerField()
    short_description = models.TextField()
    content = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredientRel', related_name='recipe')


class RecipeIngredientRel(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.SET_NULL, null=True, related_name='recipes')
    quantity = models.IntegerField()

