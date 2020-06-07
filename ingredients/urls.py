from django.urls import path

from . import views

app_name = 'ingredients'
urlpatterns = [
    path('', views.index, name='index'),
    path('ingredient/', views.IngredientListView.as_view(), name='ingredient-list'),
    path('ingredient/<int:pk>/', views.IngredientView.as_view(), name='ingredient'),
    path('ingredient_edit/<int:pk>/', views.IngredientEditView.as_view(), name='ingredient_edit'),
    path('ingredient_save/<int:pk>/', views.IngredientSaveView.as_view(), name='ingredient_save'),
]
