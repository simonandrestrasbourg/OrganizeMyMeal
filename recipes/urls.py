from django.urls import path, include
from .routers import router
from django.views.generic import TemplateView


app_name = 'recipes'
urlpatterns = [
    path('api/', include(router.urls)),
    path('recipes/', TemplateView.as_view(template_name='recipes/index.html'), name='recipes'),
]
