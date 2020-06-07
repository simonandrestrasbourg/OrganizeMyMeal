from django.contrib import admin
from django import forms
from durationwidget.widgets import TimeDurationWidget
from .models import IngredientUnit, IngredientType, Ingredient

class IngredientAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(IngredientAdminForm, self).__init__(*args, **kwargs)
        self.fields['conservation_time'].widget = TimeDurationWidget(
            show_days=True, show_hours=False, show_minutes=False, show_seconds=False)

class IngredientAdmin(admin.ModelAdmin):
    form = IngredientAdminForm
    fields = ['pub_date', 'name', 'type', 'unit',
              'conservation_time']

admin.site.register(Ingredient, IngredientAdmin)

admin.site.register(IngredientUnit)
admin.site.register(IngredientType)
