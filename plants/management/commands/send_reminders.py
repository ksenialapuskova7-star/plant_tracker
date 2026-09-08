from django.core.management.base import BaseCommand
from plants.tasks import send_reminders


class Command(BaseCommand):
    help = 'Отправляет напоминания о поливе, удобрении и пересадке'

    def handle(self, *args, **options):
        self.stdout.write('🔄 Отправка напоминаний...')
        send_reminders()
        self.stdout.write(self.style.SUCCESS('✅ Напоминания отправлены!'))
