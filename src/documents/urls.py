from django.urls import path
from . import views

app_name = 'documents'


urlpatterns = [
    path('list/', views.DocumentFilterView.as_view(), name='list'),
    path('detail/<int:pk>/', views.DocumentDetailView.as_view(), name='detail'),
]
