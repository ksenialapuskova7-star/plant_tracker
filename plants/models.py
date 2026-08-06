from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Plant(models.Model):
    class HealthStatus(models.TextChoices):
        HEALTHY = 'healthy', 'Здоровое'
        NEEDS_WATER = 'needs_water', 'Нужен полив'
        NEEDS_FERTILIZER = 'needs_fertilizer', 'Нужно удобрение'
        SICK = 'sick', 'Больное'
        DYING = 'dying', 'Умирает'
    
    class LightPreference(models.TextChoices):
        DIRECT_SUN = 'direct_sun', 'Прямое солнце'
        BRIGHT_INDIRECT = 'bright_indirect', 'Яркий рассеянный'
        PARTIAL_SHADE = 'partial_shade', 'Полутень'
        SHADE = 'shade', 'Тень'
    
    class WateringFrequency(models.TextChoices):
        DAILY = 'daily', 'Ежедневно'
        EVERY_2_DAYS = 'every_2_days', 'Каждые 2 дня'
        EVERY_3_DAYS = 'every_3_days', 'Каждые 3 дня'
        WEEKLY = 'weekly', 'Раз в неделю'
        EVERY_2_WEEKS = 'every_2_weeks', 'Раз в 2 недели'
        MONTHLY = 'monthly', 'Раз в месяц'
        AS_NEEDED = 'as_needed', 'По мере необходимости'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plants', verbose_name="Владелец")
    name = models.CharField(max_length=100, verbose_name="Название растения")
    scientific_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Латинское название")
    photo = models.ImageField(upload_to='plants/', blank=True, null=True, verbose_name="Фото")
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name="Местоположение")
    
    light_preference = models.CharField(max_length=20, choices=LightPreference.choices, default=LightPreference.BRIGHT_INDIRECT, verbose_name="Предпочтение по свету")
    watering_frequency = models.CharField(max_length=20, choices=WateringFrequency.choices, default=WateringFrequency.WEEKLY, verbose_name="Частота полива")
    watering_volume = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(10)], verbose_name="Объём воды (мл)")
    fertilizer_frequency = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1)], verbose_name="Удобрение (дней)")
    repot_frequency = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1)], verbose_name="Пересадка (дней)")
    
    temperature_min = models.FloatField(blank=True, null=True, verbose_name="Минимальная температура °C")
    temperature_max = models.FloatField(blank=True, null=True, verbose_name="Максимальная температура °C")
    humidity_preference = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(10), MaxValueValidator(100)], verbose_name="Влажность воздуха %")
    needs_misting = models.BooleanField(default=False, verbose_name="Нуждается в опрыскивании")
    is_toxic = models.BooleanField(default=False, verbose_name="Токсично для животных/детей")
    
    dormant_period_start = models.DateField(blank=True, null=True, verbose_name="Начало периода покоя")
    dormant_period_end = models.DateField(blank=True, null=True, verbose_name="Конец периода покоя")
    
    purchased_at = models.DateField(blank=True, null=True, verbose_name="Дата покупки")
    last_watered = models.DateField(blank=True, null=True, verbose_name="Последний полив")
    last_fertilized = models.DateField(blank=True, null=True, verbose_name="Последнее удобрение")
    last_repotted = models.DateField(blank=True, null=True, verbose_name="Последняя пересадка")
    
    health_status = models.CharField(max_length=20, choices=HealthStatus.choices, default=HealthStatus.HEALTHY, verbose_name="Состояние здоровья")
    notes = models.TextField(blank=True, null=True, verbose_name="Заметки")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Растение"
        verbose_name_plural = "Растения"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class CareLog(models.Model):
    class ActionType(models.TextChoices):
        WATERING = 'watering', 'Полив'
        FERTILIZING = 'fertilizing', 'Удобрение'
        REPOTTING = 'repotting', 'Пересадка'
        MISTING = 'misting', 'Опрыскивание'
        PRUNING = 'pruning', 'Обрезка'
        TREATMENT = 'treatment', 'Лечение'
        OTHER = 'other', 'Другое'
    
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='care_logs', verbose_name="Растение")
    action_type = models.CharField(max_length=20, choices=ActionType.choices, verbose_name="Тип действия")
    date = models.DateField(auto_now_add=True, verbose_name="Дата")
    notes = models.TextField(blank=True, null=True, verbose_name="Примечания")
    
    class Meta:
        verbose_name = "Запись в журнале"
        verbose_name_plural = "Журнал ухода"
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.plant.name} — {self.get_action_type_display()} ({self.date})"

class Reminder(models.Model):
    class ActionType(models.TextChoices):
        WATERING = 'watering', 'Полив'
        FERTILIZING = 'fertilizing', 'Удобрение'
        REPOTTING = 'repotting', 'Пересадка'
        MISTING = 'misting', 'Опрыскивание'
        PRUNING = 'pruning', 'Обрезка'
        CUSTOM = 'custom', 'Своё действие'

    class Frequency(models.TextChoices):
        ONCE = 'once', 'Разово'
        DAILY = 'daily', 'Ежедневно'
        WEEKLY = 'weekly', 'Еженедельно'
        MONTHLY = 'monthly', 'Ежемесячно'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reminders',
        verbose_name="Пользователь"
    )
    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        related_name='reminders',
        verbose_name="Растение"
    )
    action_type = models.CharField(
        max_length=20,
        choices=ActionType.choices,
        verbose_name="Тип действия"
    )
    custom_action_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Своё название действия"
    )
    frequency = models.CharField(
        max_length=20,
        choices=Frequency.choices,
        default=Frequency.ONCE,
        verbose_name="Периодичность"
    )
    interval_days = models.PositiveIntegerField(
        default=1,
        verbose_name="Интервал (дни)"
    )
    reminder_date = models.DateField(
        verbose_name="Дата напоминания"
    )
    reminder_time = models.TimeField(
        default='09:00',
        verbose_name="Время напоминания"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активно"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Заметки"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Напоминание"
        verbose_name_plural = "Напоминания"
        ordering = ['reminder_date', 'reminder_time']

    def __str__(self):
        action = self.custom_action_name or self.get_action_type_display()
        return f"{self.plant.name} — {action} ({self.reminder_date} {self.reminder_time})"