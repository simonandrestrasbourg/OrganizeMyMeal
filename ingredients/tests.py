import datetime
import unittest
from django.test import TestCase
from .models import Ingredient, IngredientType, IngredientUnit
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from .admin import IngredientAdminForm


class TestIngredient(TestCase):
    fixtures = ['ingredients_fixture.json']

    def test_first_ingredient_conservation_day(self):
        """ Verify conservation time is equal to datetime.delta python module."""
        IngredientObj = Ingredient.objects.get(pk=1)
        self.assertEqual(IngredientObj.conservation_day, 10)

    def test_ingredient_conservation_date_is_positive(self):
        """ We don't want conservation date can be negative """
        GramUnit = IngredientUnit.objects.filter(name="Gram").first()
        MeatType = IngredientType.objects.filter(name="Meat").first()
        Porc = Ingredient(
            conservation_day=-7,
            name="Porc",
            unit=GramUnit,
            type=MeatType,
            pub_date=datetime.datetime.now())
        with self.assertRaises(ValidationError) as cm:
           Porc.full_clean()

    def test_create_ingredient_pub_date(self):
        """ pub_date have value by default"""
        GramUnit = IngredientUnit.objects.filter(name="Gram").first()
        MeatType = IngredientType.objects.filter(name="Meat").first()
        Porc = Ingredient(
            conservation_day=7,
            name="Porc",
            unit=GramUnit,
            type=MeatType)
        self.assertEqual(Porc.pub_date.year, 2020)

    def test_create_ingredient_name_unique(self):
        """ Test unique constraint on Ingredient.name """
        GramUnit = IngredientUnit.objects.filter(name="Gram").first()
        MeatType = IngredientType.objects.filter(name="Meat").first()
        Porc = Ingredient(
            conservation_day=7,
            name="Porc",
            unit=GramUnit,
            type=MeatType,
            pub_date=datetime.datetime.now())
        Porc.full_clean()
        Porc.save()
        with self.assertRaises(ValidationError) as cm:
            Porc2 = Ingredient(
                conservation_day=7,
                name="Porc",
                unit=GramUnit,
                type=MeatType,
            )
            Porc2.full_clean()
            Porc2.save()

    def test_delete_type(self):
        """ Cannot delete ingredient type when have Ingredient using it."""
        MeatType = IngredientType.objects.filter(name="Meat").first()
        IngredientObjs = Ingredient.objects.filter(type=MeatType)
        self.assertEqual(len(IngredientObjs), 2)
        with self.assertRaises(ProtectedError) as cm:
            MeatType.delete()

    def test_delete_unit(self):
        """ Cannot delete ingredient unit when have Ingredient using it."""
        GramUnit = IngredientUnit.objects.filter(name="Gram").first()
        IngredientObjs = Ingredient.objects.filter(unit=GramUnit)
        self.assertEqual(len(IngredientObjs), 6)
        with self.assertRaises(ProtectedError) as cm:
            GramUnit.delete()

    def test_delete_ingredient(self):
        """ When delete ingredient we want keep unit and type"""
        IngredientObj = Ingredient.objects.get(pk=1)
        IngredientTypeObj = IngredientObj.type
        IngredientUnitObj = IngredientObj.unit
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
        self.assertEqual(response.context['object'].name, "Fresh cream")

    def test_client_ingredient_edit(self):
        response = self.client.get('/ingredient_edit/4/')
        self.assertEqual(response.status_code, 200)
        ingredient = response.context['object']
        self.assertEqual(ingredient.name, "Fresh cream")
