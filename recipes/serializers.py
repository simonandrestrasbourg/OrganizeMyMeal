from rest_framework import serializers
from recipes.models import Recipe, RecipeIngredientRel


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
