from django.contrib import admin
from .models import Plant, CareLog


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'health_status', 'last_watered', 'created_at']
    list_filter = ['health_status', 'light_preference', 'watering_frequency']
    search_fields = ['name', 'scientific_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CareLog)
class CareLogAdmin(admin.ModelAdmin):
    list_display = ['plant', 'action_type', 'date']
    list_filter = ['action_type', 'date']