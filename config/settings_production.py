from .settings import *

DEBUG = False

ALLOWED_HOSTS = ['Ksemm.pythonanywhere.com', 'www.Ksemm.pythonanywhere.com']

# База данных — SQLite (для бесплатного тарифа)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Статика
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Медиа
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Безопасность
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Telegram
TELEGRAM_BOT_TOKEN = '8969448431:AAGd-conCfZno-UVfGga5RohTRR1dEdtmRY'

# Celery с SQLite
CELERY_BROKER_URL = 'sqla+sqlite:///celery.sqlite'
CELERY_RESULT_BACKEND = 'db+sqlite:///celery.sqlite'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Moscow'