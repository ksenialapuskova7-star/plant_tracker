from django.urls import path
from . import views

app_name = 'plants'

urlpatterns = [
    path('', views.plant_list, name='list'),
    path('create/', views.plant_create, name='create'),
    path('<int:pk>/', views.plant_detail, name='detail'),
    path('<int:pk>/edit/', views.plant_edit, name='edit'),
    path('<int:pk>/delete/', views.plant_delete, name='delete'),
    path('<int:pk>/add-care/', views.add_care, name='add_care'),
]