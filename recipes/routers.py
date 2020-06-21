from rest_framework import routers
from recipes.viewsets import RecipeViewSet


router = routers.DefaultRouter()
router.register(r'recipe', RecipeViewSet)
