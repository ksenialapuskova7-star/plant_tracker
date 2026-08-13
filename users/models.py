from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    telegram_username = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name="Telegram username"
    )
    telegram_id = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name="Telegram ID"
    )
    notification_telegram = models.BooleanField(
        default=False, 
        verbose_name="Уведомления в Telegram"
    )
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.username