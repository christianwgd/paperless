from django.urls import path
from . import views

app_name = 'settings'


urlpatterns = [
    path('settings/', views.settings, name='edit'),
]
