from django.contrib import admin
from .models import Category, Plant, PlantPhoto

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'color', 'user']
    list_filter = ['user']
    search_fields = ['name']

@admin.register(PlantPhoto)
class PlantPhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'plant', 'caption', 'order']
    list_filter = ['plant']