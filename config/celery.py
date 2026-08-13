import os
from celery import Celery

# Принудительно устанавливаем брокер
BROKER_URL = 'redis://redis:6379/0'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_production')

app = Celery('config', broker=BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
