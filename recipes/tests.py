import datetime
from django.test import TestCase
from ingredients.models import Ingredient, IngredientType, IngredientUnit
from recipes.models import Recipe, RecipeIngredientRel
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission


def fetch_ingredient(name):
    return Ingredient.objects.filter(name=name).first()


class TestRecipe(TestCase):
    fixtures = ['ingredients_fixture.json']

    def setUp(self):
        self.user_fields = {
            'username': "user",
            'password': "user"
        }
        self.user = User.objects.create_user(**self.user_fields)
        view_perm = Permission.objects.get(codename="view_ingredient")
        add_perm = Permission.objects.get(codename="add_ingredient")
        change_perm = Permission.objects.get(codename="change_ingredient")
        self.user.user_permissions.add(view_perm)
        self.user.user_permissions.add(add_perm)
        self.user.user_permissions.add(change_perm)
        self.user.save()

    def test_create_recipe(self):
        """ Can create a recipe."""
        recipes_carbonara = {
            'name': 'Spaghetti Carbonara',
            'duration': 35,
            'short_description': 'Carbonara with fresh cream',
            'content': """
1. Put pasta on cooking
2. Thinly slice the onions and made them cook in pan"
3. Put slice of bacon"
4. Prepare the fresh cream, eggs, salt, pepper in a bowl and mix."
5. When pasta is ready integrate them to the cream""",
        }
        new_recipe = Recipe(**recipes_carbonara)
        new_recipe.save()
        RecipeIngredientRel.objects.create(ingredient=fetch_ingredient('Pasta'), recipe=new_recipe, quantity=350)
        RecipeIngredientRel.objects.create(ingredient=fetch_ingredient('bacon'), recipe=new_recipe, quantity=25)
        self.assertEqual(new_recipe.name, 'Spaghetti Carbonara')
        self.assertEqual(len(new_recipe.ingredients.values()), 2)
        self.assertEqual(new_recipe.ingredients.values()[0]['name'], 'Pasta')

    def test_edit_recipe(self):
        """ Can edit a recipe."""

    def test_delete_recipe(self):
        """ Can delete a recipe.
        RecipeIngredientRel FK have to be deleted with but no Ingredient."""

    def test_delete_ingredient_recipe(self):
        """ Can't delete a ingredient related to a recipe.
        Need to delete first all RecipeIngredientRel to permit delete ingredient."""

