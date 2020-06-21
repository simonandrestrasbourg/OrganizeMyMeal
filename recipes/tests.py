import datetime
from django.test import TestCase
from ingredients.models import Ingredient, IngredientType, IngredientUnit
from recipes.models import Recipe, RecipeIngredientRel
from django.db.models.deletion import ProtectedError
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

    def create_recipe(self, **kwars):
        """ Helper to create easily a recipe."""
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
        return new_recipe

    def test_create_recipe(self):
        """ Can create a recipe."""
        new_recipe = self.create_recipe()
        self.assertEqual(new_recipe.name, 'Spaghetti Carbonara')
        self.assertEqual(len(new_recipe.ingredients.values()), 2)
        self.assertEqual(new_recipe.ingredients.values()[0]['name'], 'Pasta')

    def test_edit_recipe(self):
        """ Can edit a recipe."""
        new_recipe = self.create_recipe()
        new_recipe.duration = 25
        RecipeIngredientRel.objects.create(ingredient=fetch_ingredient('Pepper'), recipe=new_recipe, quantity=350)
        self.assertEqual(new_recipe.duration, 25)
        self.assertEqual(len(new_recipe.ingredients.values()), 3)

    def test_delete_recipe(self):
        """ Can delete a recipe.
        RecipeIngredientRel FK have to be deleted with but no Ingredient."""
        new_recipe = self.create_recipe()
        carbo_pasta_rel = RecipeIngredientRel.objects.filter(recipe__name='Spaghetti Carbonara')
        self.assertEqual(len(carbo_pasta_rel), 2)
        new_recipe.delete()
        # After delete the recipe, all Rel object is delete
        carbo_pasta_rel = RecipeIngredientRel.objects.filter(recipe__name='Spaghetti Carbonara')
        self.assertEqual(len(carbo_pasta_rel), 0)
        # But ingredient is steel here
        pasta = Ingredient.objects.filter(name='Pasta')
        self.assertEqual(len(pasta), 1)

    def test_delete_rel_ingredient_recipe(self):
        """ Can delete a rel between ingredient to a recipe.
        The recipe and the ingredients have to exist after"""
        new_recipe = self.create_recipe()
        Pasta_rel = RecipeIngredientRel.objects.filter(ingredient__name='Pasta')
        Pasta_rel.delete()
        self.assertEqual(len(new_recipe.ingredients.values()), 1)
        pasta = Ingredient.objects.filter(name='Pasta')
        self.assertEqual(len(pasta), 1)

    def test_delete_ingredient_recipe(self):
        """ Can't delete a ingredient related to a recipe.
        Need to delete first all RecipeIngredientRel to permit delete ingredient."""
        new_recipe = self.create_recipe()
        pasta = Ingredient.objects.filter(name='Pasta')
        # If we try to delete that ingredient the orm raise an error
        self.assertRaises(ProtectedError, pasta.delete)
        # so we need to delete all rel between the ingredient and the recipe
        Pasta_rel = RecipeIngredientRel.objects.filter(ingredient__name='Pasta')
        Pasta_rel.delete()
        pasta.delete()
        self.assertEqual(len(Ingredient.objects.filter(name='Pasta')), 0)