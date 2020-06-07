from django.urls import path

from . import views

app_name = 'recipes'
urlpatterns = [
    path('', views.index, name='index'),
    path('ingredient/<int:pk>/', views.IngredientView.as_view(), name='ingredient'),
]
