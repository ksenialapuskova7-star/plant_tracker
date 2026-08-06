from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_active']
    search_fields = ['email', 'username']
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('phone', 'avatar', 'telegram_id', 'notification_email', 'notification_telegram')}),
    )