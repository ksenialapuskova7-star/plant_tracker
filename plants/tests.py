from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Plant, Reminder, CareLog

User = get_user_model()


class PlantModelTest(TestCase):
    """Тесты модели Plant"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )

    def test_create_plant(self):
        """Тест создания растения"""
        plant = Plant.objects.create(
            user=self.user,
            name='Кактус',
            watering_frequency='weekly'
        )
        self.assertEqual(plant.name, 'Кактус')
        self.assertEqual(str(plant), 'Кактус')
        self.assertEqual(plant.user.username, 'testuser')

    def test_plant_str_method(self):
        """Тест строкового представления"""
        plant = Plant.objects.create(
            user=self.user,
            name='Монстера'
        )
        self.assertEqual(str(plant), 'Монстера')

class ReminderModelTest(TestCase):
    """Тесты модели Reminder"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.plant = Plant.objects.create(
            user=self.user,
            name='Фикус'
        )

    def test_create_reminder(self):
        """Тест создания напоминания"""
        now = timezone.now()
        reminder = Reminder.objects.create(
            user=self.user,
            plant=self.plant,
            action_type='watering',
            frequency='daily',
            reminder_date=now.date(),
            reminder_time=now.time()
        )
        self.assertEqual(reminder.plant.name, 'Фикус')
        self.assertTrue(reminder.is_active)
        # Проверяем только часть строки, а не всё полностью
        self.assertIn('Фикус', str(reminder))
        self.assertIn('Полив', str(reminder))
        def test_reminder_str_method(self):
            """Тест строкового представления напоминания"""
            reminder = Reminder.objects.create(
                user=self.user,
                plant=self.plant,
                action_type='custom',
                custom_action_name='Опрыскивание',
                frequency='weekly',
                reminder_date=timezone.now().date(),
                reminder_time=timezone.now().time()
            )
            self.assertIn('Опрыскивание', str(reminder))


class CareLogModelTest(TestCase):
    """Тесты модели CareLog"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.plant = Plant.objects.create(
            user=self.user,
            name='Монстера'
        )

    def test_create_care_log(self):
        """Тест создания записи ухода"""
        log = CareLog.objects.create(
            plant=self.plant,
            action_type='watering',
            notes='Полив 500 мл'
        )
        self.assertEqual(log.plant.name, 'Монстера')
        self.assertEqual(log.action_type, 'watering')
        self.assertEqual(log.notes, 'Полив 500 мл')

    def test_care_log_str_method(self):
        """Тест строкового представления записи ухода"""
        log = CareLog.objects.create(
            plant=self.plant,
            action_type='fertilizing',
            notes='Удобрение'
        )
        self.assertIn('Монстера', str(log))
        self.assertIn('Удобрение', str(log))


class PlantViewTest(TestCase):
    """Тесты представлений растений"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.plant = Plant.objects.create(
            user=self.user,
            name='Тестовое растение'
        )

    def test_plant_list_view(self):
        """Тест списка растений"""
        response = self.client.get(reverse('plants:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plants/list.html')
        self.assertContains(response, 'Тестовое растение')

    def test_plant_detail_view(self):
        """Тест детальной страницы растения"""
        response = self.client.get(reverse('plants:detail', kwargs={'pk': self.plant.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plants/detail.html')

    def test_plant_detail_view_404(self):
        """Тест 404 для несуществующего растения"""
        response = self.client.get(reverse('plants:detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)


class AuthTest(TestCase):
    """Тесты аутентификации"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )

    def test_login_required(self):
        """Тест, что неавторизованный пользователь перенаправляется на логин"""
        response = self.client.get(reverse('plants:list'))
        self.assertEqual(response.status_code, 302)

    def test_login_success(self):
        """Тест успешного входа"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('plants:list'))
        self.assertEqual(response.status_code, 200)