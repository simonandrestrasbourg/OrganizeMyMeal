from django.urls import path, include

from . import views

app_name = 'core'
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup, name='signup'),
]
