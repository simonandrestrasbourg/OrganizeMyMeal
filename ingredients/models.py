from django.db import models
import datetime
from django.utils import timezone
from django import forms


class IngredientUnit(models.Model):
    """ Classify ingredient by quantity unit.
    Most of ingredient have unity like gram, centilitre...
    That model have to be configured only by admin.
    """
    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class IngredientType(models.Model):
    """ Classify ingredient by type of ingredient.
    Most of ingredient can be vegetables, condiments, meat...
    That model have to be configured only by admin.
    """
    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

from django.core.exceptions import ValidationError

def validate_duration_time_not_negative(value):
    """ TODO: unittest """
    if value <= datetime.timedelta(days=0):
        raise ValidationError(
            '%(value)s have to be positive',
            params={'value': value},
        )


def get_pub_date():
    return datetime.datetime.now()

class Ingredient(models.Model):
    """ Store ingredient and classify them by quantity unit and type.
    That model have to be configured by website user and validated 
    by admin in a delay of one week.
    """

    def __str__(self):
        return self.name

    name = models.CharField(max_length=200, unique=True)
    type = models.ForeignKey(IngredientType, on_delete=models.PROTECT)
    unit = models.ForeignKey(IngredientUnit, on_delete=models.PROTECT)
    conservation_time = models.DurationField(validators=[validate_duration_time_not_negative])
    pub_date = models.DateTimeField('date published', default=get_pub_date)

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'type', 'unit', 'conservation_time']
