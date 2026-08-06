from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # email теперь НЕ уникальный и НЕ обязательный
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    telegram_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Telegram ID")
    notification_email = models.BooleanField(default=True, verbose_name="Уведомления по email")
    notification_telegram = models.BooleanField(default=False, verbose_name="Уведомления в Telegram")
    
    # 👇 Вход по username (как в стандартном Django)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # email теперь НЕ обязательный
    
    def __str__(self):
        return self.username