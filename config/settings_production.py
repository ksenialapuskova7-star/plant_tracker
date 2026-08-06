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