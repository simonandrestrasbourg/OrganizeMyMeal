import datetime
import unittest
from django.test import TestCase
from .models import Ingredient, IngredientType, IngredientUnit
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from .admin import IngredientAdminForm


class TestIngredient(TestCase):
    fixtures = ['ingredients_fixture.json']

    def test_first_ingrediant_conservation_time_max(self):
        """ Verify conservation time is equal to datetime.delta python module."""
        IngredientObj = Ingredient.objects.get(pk=1)
        self.assertEqual(IngredientObj.conservation_time, datetime.timedelta(days=11574, seconds=6399))

    def test_first_ingrediant_conservation_time_middle(self):
        """ Verify conservation time is equal to datetime.delta python module."""
        IngredientObj = Ingredient.objects.get(pk=4)
        self.assertEqual(IngredientObj.conservation_time, datetime.timedelta(seconds=10000))

    def test_ingredient_conservation_date_is_positiv(self):
        """ We don't want conservation date can be negativ """
        GramUnit = IngredientUnit.objects.filter(ingredient_unit_text="Gram").first()
        MeatType = IngredientType.objects.filter(ingredient_type_text="Meat").first()
        Porc = Ingredient(
            conservation_time=datetime.timedelta(days=-25, seconds=0),
            ingredient_text="Porc",
            ingredient_unit=GramUnit,
            ingredient_type=MeatType,
            pub_date=datetime.datetime.now())
        with self.assertRaises(ValidationError) as cm:
           Porc.full_clean()

    def test_delete_ingredient_type(self):
        """ Cannot delete ingredient type when have Ingredient using it."""
        MeatType = IngredientType.objects.filter(ingredient_type_text="Meat").first()
        IngredientObjs = Ingredient.objects.filter(ingredient_type=MeatType)
        self.assertEqual(len(IngredientObjs), 2)
        with self.assertRaises(ProtectedError) as cm:
            MeatType.delete()

    def test_delete_ingredient_unit(self):
        """ Cannot delete ingredient unit when have Ingredient using it."""
        GramUnit = IngredientUnit.objects.filter(ingredient_unit_text="Gram").first()
        IngredientObjs = Ingredient.objects.filter(ingredient_unit=GramUnit)
        self.assertEqual(len(IngredientObjs), 6)
        with self.assertRaises(ProtectedError) as cm:
            GramUnit.delete()

    def test_delete_ingredient(self):
        """ When delete ingredient we want keep unit and type"""
        IngredientObj = Ingredient.objects.get(pk=1)
        IngredientTypeObj = IngredientObj.ingredient_type
        IngredientUnitObj = IngredientObj.ingredient_unit
        IngredientObj.delete()
        self.assert_(IngredientTypeObj)
        self.assert_(IngredientUnitObj)

    def test_client_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_client_ingredient_list(self):
        response = self.client.get('/ingredient/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['ingredient_list']), 12)

    def test_client_ingredient(self):
        response = self.client.get('/ingredient/4/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'].ingredient_text, "Fresh cream")
