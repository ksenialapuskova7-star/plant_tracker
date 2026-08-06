import os
import sys

# Добавляем путь к проекту
path = '/home/Ksemm/plant_tracker'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_production')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()