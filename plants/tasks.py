from celery import shared_task
from django.utils import timezone
from django.conf import settings
import requests


@shared_task
def send_reminders():
    from .models import Plant
    
    today = timezone.now().date()
    plants = Plant.objects.all()
    
    frequency_map = {
        'daily': 1,
        'every_2_days': 2,
        'every_3_days': 3,
        'weekly': 7,
        'every_2_weeks': 14,
        'monthly': 30,
    }
    
    for plant in plants:
        messages = []
        
        if plant.last_watered:
            days = (today - plant.last_watered).days
            interval = frequency_map.get(plant.watering_frequency, 7)
            if days >= interval:
                messages.append(f"💧 Полив! Прошло {days} дней")
        
        if plant.fertilizer_frequency and plant.last_fertilized:
            days = (today - plant.last_fertilized).days
            if days >= plant.fertilizer_frequency:
                messages.append(f"🧪 Удобрение! Прошло {days} дней")
        
        if plant.repot_frequency and plant.last_repotted:
            days = (today - plant.last_repotted).days
            if days >= plant.repot_frequency:
                messages.append(f"🔄 Пересадка! Прошло {days} дней")
        
        if messages:
            text = f"🌿 {plant.name}\n" + "\n".join(messages)
            
            if plant.user.notification_telegram and plant.user.telegram_id:
                send_telegram_notification.delay(plant.user.telegram_id, text)


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