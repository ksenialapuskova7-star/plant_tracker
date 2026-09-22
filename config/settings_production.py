from .settings import *

DEBUG = False

ALLOWED_HOSTS = ['195.62.48.118', 'Ksemm.pythonanywhere.com',
                 'www.Ksemm.pythonanywhere.com', 'localhost', '127.0.0.1']

# SQLite для PythonAnywhere
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

TELEGRAM_BOT_TOKEN = '8969448431:AAGd-conCfZno-UVfGga5RohTRR1dEdtmRY'

CELERY_BROKER_URL = 'sqla+sqlite:///celery.sqlite'
CELERY_RESULT_BACKEND = 'db+sqlite:///celery.sqlite'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True