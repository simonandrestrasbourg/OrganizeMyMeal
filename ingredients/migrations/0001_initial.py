# Generated by Django 3.0.7 on 2020-06-04 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_text', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='IngredientUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_text', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('conservation_time', models.DurationField()),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ingredients.IngredientType')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ingredients.IngredientUnit')),
            ],
        ),
    ]
