from .settings import *

DEBUG = False

ALLOWED_HOSTS = ['195.62.48.118', 'Ksemm.pythonanywhere.com', 'www.Ksemm.pythonanywhere.com', 'localhost', '127.0.0.1']


# База данных — SQLite (для бесплатного тарифа)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'plant_tracker'),
        'USER': os.getenv('DB_USER', 'plant_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'plant_pass'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    }
}

# Статика
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Медиа
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Безопасность
#SECURE_SSL_REDIRECT = True
#SESSION_COOKIE_SECURE = True
#CSRF_COOKIE_SECURE = True

# Telegram
TELEGRAM_BOT_TOKEN = '8969448431:AAGd-conCfZno-UVfGga5RohTRR1dEdtmRY'

# Celery с SQLite
# Celery + Redis
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
# Telegram
TELEGRAM_BOT_TOKEN = '8969448431:AAGd-conCfZno-UVfGga5RohTRR1dEdtmRY'
