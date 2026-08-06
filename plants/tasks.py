from celery import shared_task
from django.utils import timezone
from django.conf import settings
import requests


@shared_task
def send_reminders():
    from .models import Reminder
    
    today = timezone.now().date()
    reminders = Reminder.objects.filter(
        is_active=True,
        next_reminder_date__lte=today
    )
    
    for reminder in reminders:
        action = reminder.custom_action_name or reminder.get_action_type_display()
        text = f"🌿 {reminder.plant.name}\n📋 Действие: {action}\n📅 Дата: {today}"
        
        if reminder.notes:
            text += f"\n📝 {reminder.notes}"
        
        # Отправка в Telegram
        if reminder.user.notification_telegram and reminder.user.telegram_id:
            send_telegram_notification.delay(reminder.user.telegram_id, text)
        
        # Обновление даты следующего напоминания
        if reminder.frequency == 'once':
            reminder.is_active = False
        elif reminder.frequency == 'daily':
            reminder.next_reminder_date = today + timezone.timedelta(days=reminder.interval_days)
        elif reminder.frequency == 'weekly':
            reminder.next_reminder_date = today + timezone.timedelta(days=7 * reminder.interval_days)
        elif reminder.frequency == 'monthly':
            reminder.next_reminder_date = today + timezone.timedelta(days=30 * reminder.interval_days)
        
        reminder.save()


@shared_task
def send_telegram_notification(chat_id, text):
    token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    try:
        response = requests.post(
            url,
            json={'chat_id': chat_id, 'text': text},
            timeout=30,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        print(f"✅ Telegram отправлен: {response.status_code}")
        return response.json()
    except Exception as e:
        print(f"❌ Ошибка Telegram: {e}")
        return None

@shared_task
def send_reminders():
    from .models import Reminder
    
    today = timezone.now().date()
    reminders = Reminder.objects.filter(
        is_active=True,
        next_reminder_date__lte=today
    )
    
    for reminder in reminders:
        action = reminder.custom_action_name or reminder.get_action_type_display()
        text = f"🌿 {reminder.plant.name}\n📋 Действие: {action}\n📅 Дата: {today}"
        
        if reminder.notes:
            text += f"\n📝 {reminder.notes}"
        
        if reminder.user.notification_telegram and reminder.user.telegram_id:
            send_telegram_notification.delay(reminder.user.telegram_id, text)
        
        if reminder.frequency == 'once':
            reminder.is_active = False
        elif reminder.frequency == 'daily':
            reminder.next_reminder_date = today + timezone.timedelta(days=reminder.interval_days)
        elif reminder.frequency == 'weekly':
            reminder.next_reminder_date = today + timezone.timedelta(days=7 * reminder.interval_days)
        elif reminder.frequency == 'monthly':
            reminder.next_reminder_date = today + timezone.timedelta(days=30 * reminder.interval_days)
        
        reminder.save()