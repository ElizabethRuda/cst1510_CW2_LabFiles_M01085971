#!/usr/bin/env python3
"""
Комплексные тесты для Intelligence Platform
Проверка всех компонентов перед сдачей
"""

import sys
import os
from pathlib import Path

# Добавляем пути к проекту
CURRENT_DIR = Path(__file__).resolve().parent  # Streamlit_Visualization/
PROJECT_ROOT = CURRENT_DIR.parents[0]  # 123/
STREAMLIT_DIR = CURRENT_DIR  # Streamlit_Visualization/

# Добавляем оба пути для импортов
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(STREAMLIT_DIR) not in sys.path:
    sys.path.insert(0, str(STREAMLIT_DIR))

import unittest
from datetime import datetime

# Импорты моделей
from app.models.user import User
from app.models.incident import SecurityIncident
from app.models.dataset import Dataset
from app.models.ticket import ITTicket

# Импорты репозиториев
from app.repositories.incident_repository import IncidentRepository

# Импорты для работы с БД
from app.data.db import connect_database
from app.data.incidents import get_all_incidents, create_incident, delete_incident
from app.data.datasets import get_all_datasets, create_dataset
from app.data.tickets import get_all_tickets, create_ticket


class TestUserModel(unittest.TestCase):
    """Тесты для класса User"""
    
    def test_password_hashing(self):
        """Тест хеширования пароля"""
        password = "TestPassword123!"
        hash1 = User.hash_password(password)
        hash2 = User.hash_password(password)
        
        # Хеши должны быть разными (из-за соли)
        self.assertNotEqual(hash1, hash2)
        # Но оба должны быть строками
        self.assertIsInstance(hash1, str)
        self.assertIsInstance(hash2, str)
    
    def test_password_verification(self):
        """Тест проверки пароля"""
        password = "TestPassword123!"
        user = User("testuser", User.hash_password(password), "user")
        
        # Правильный пароль
        self.assertTrue(user.verify_password(password))
        # Неправильный пароль
        self.assertFalse(user.verify_password("WrongPassword"))
    
    def test_role_checking(self):
        """Тест проверки ролей"""
        admin = User("admin", "hash", "admin")
        analyst = User("analyst", "hash", "analyst")
        user = User("user", "hash", "user")
        
        self.assertTrue(admin.is_admin())
        self.assertFalse(admin.is_analyst())
        
        self.assertTrue(analyst.is_analyst())
        self.assertFalse(analyst.is_admin())
        
        self.assertFalse(user.is_admin())
        self.assertFalse(user.is_analyst())


class TestSecurityIncidentModel(unittest.TestCase):
    """Тесты для класса SecurityIncident"""
    
    def test_incident_creation(self):
        """Тест создания инцидента"""
        incident = SecurityIncident(
            title="Test Incident",
            severity="High",
            status="open",
            date="2024-12-01"
        )
        
        self.assertEqual(incident.title, "Test Incident")
        self.assertEqual(incident.severity, "High")
        self.assertEqual(incident.status, "open")
        self.assertEqual(incident.date, "2024-12-01")
    
    def test_severity_validation(self):
        """Тест валидации серьезности"""
        # Валидная серьезность
        incident = SecurityIncident("Test", "Critical", "open")
        self.assertEqual(incident.severity, "Critical")
        
        # Невалидная серьезность - должна стать Medium по умолчанию
        incident = SecurityIncident("Test", "Invalid", "open")
        self.assertEqual(incident.severity, "Medium")
    
    def test_status_methods(self):
        """Тест методов проверки статуса"""
        critical = SecurityIncident("Test", "Critical", "open")
        high = SecurityIncident("Test", "High", "open")
        medium = SecurityIncident("Test", "Medium", "resolved")
        
        self.assertTrue(critical.is_critical())
        self.assertFalse(high.is_critical())
        
        self.assertTrue(critical.is_high_priority())
        self.assertTrue(high.is_high_priority())
        self.assertFalse(medium.is_high_priority())
        
        self.assertTrue(critical.is_open())
        self.assertFalse(medium.is_open())
    
    def test_status_update(self):
        """Тест обновления статуса"""
        incident = SecurityIncident("Test", "High", "open")
        self.assertTrue(incident.is_open())
        
        incident.update_status("in_progress")
        self.assertEqual(incident.status, "in_progress")
        self.assertTrue(incident.is_open())
        
        incident.resolve()
        self.assertEqual(incident.status, "resolved")
        self.assertFalse(incident.is_open())
        
        incident.close()
        self.assertEqual(incident.status, "closed")


class TestDatasetModel(unittest.TestCase):
    """Тесты для класса Dataset"""
    
    def test_dataset_creation(self):
        """Тест создания датасета"""
        dataset = Dataset(
            name="Test Dataset",
            source="Network Sensors",
            category="Security",
            size=1024 * 1024 * 500  # 500 MB
        )
        
        self.assertEqual(dataset.name, "Test Dataset")
        self.assertEqual(dataset.source, "Network Sensors")
        self.assertEqual(dataset.category, "Security")
        self.assertEqual(dataset.size, 524288000)
    
    def test_size_calculations(self):
        """Тест расчетов размера"""
        # 500 MB
        dataset = Dataset("Test", "Source", "Category", 524288000)
        self.assertAlmostEqual(dataset.get_size_gb(), 0.5, places=1)
        
        # 2 GB
        dataset = Dataset("Test", "Source", "Category", 2147483648)
        self.assertAlmostEqual(dataset.get_size_gb(), 2.0, places=1)
    
    def test_large_dataset_detection(self):
        """Тест определения больших датасетов"""
        # Большой датасет (>100MB)
        large = Dataset("Large", "Source", "Category", 150 * 1024 * 1024)
        self.assertTrue(large.is_large())
        
        # Маленький датасет
        small = Dataset("Small", "Source", "Category", 50 * 1024 * 1024)
        self.assertFalse(small.is_large())


class TestITTicketModel(unittest.TestCase):
    """Тесты для класса ITTicket"""
    
    def test_ticket_creation(self):
        """Тест создания тикета"""
        ticket = ITTicket(
            ticket_id="TICKET-001",
            title="Test Ticket",
            priority="High",
            status="open",
            category="Hardware"
        )
        
        self.assertEqual(ticket.ticket_id, "TICKET-001")
        self.assertEqual(ticket.title, "Test Ticket")
        self.assertEqual(ticket.priority, "High")
        self.assertEqual(ticket.status, "open")
        self.assertEqual(ticket.category, "Hardware")
    
    def test_priority_escalation(self):
        """Тест эскалации приоритета"""
        ticket = ITTicket("T-001", "Test", "Low", "open")
        self.assertEqual(ticket.priority, "Low")
        
        ticket.escalate_priority()
        self.assertEqual(ticket.priority, "Medium")
        
        ticket.escalate_priority()
        self.assertEqual(ticket.priority, "High")
        
        ticket.escalate_priority()
        self.assertEqual(ticket.priority, "Critical")
        
        # Нельзя эскалировать выше Critical
        ticket.escalate_priority()
        self.assertEqual(ticket.priority, "Critical")
    
    def test_resolution_time_calculation(self):
        """Тест расчета времени решения"""
        ticket = ITTicket(
            "T-001",
            "Test",
            "High",
            "resolved",
            created_date="2024-12-01",
            resolved_date="2024-12-05"
        )
        
        days = ticket.get_resolution_time_days()
        self.assertEqual(days, 4)


class TestDatabaseOperations(unittest.TestCase):
    """Тесты для операций с базой данных"""
    
    @classmethod
    def setUpClass(cls):
        """Настройка перед всеми тестами"""
        cls.conn = connect_database()
    
    @classmethod
    def tearDownClass(cls):
        """Очистка после всех тестов"""
        if cls.conn:
            cls.conn.close()
    
    def test_database_connection(self):
        """Тест подключения к базе данных"""
        self.assertIsNotNone(self.conn)
    
    def test_get_all_incidents(self):
        """Тест получения всех инцидентов"""
        incidents = get_all_incidents(self.conn)
        self.assertIsInstance(incidents, list)
        # Должны быть данные в базе
        if len(incidents) > 0:
            self.assertIsInstance(incidents[0], tuple)
            self.assertGreaterEqual(len(incidents[0]), 4)
    
    def test_create_incident(self):
        """Тест создания инцидента"""
        test_title = f"Test Incident {datetime.now().timestamp()}"
        incident_id = create_incident(
            self.conn,
            test_title,
            "Medium",
            "open",
            "2024-12-14"
        )
        
        self.assertIsNotNone(incident_id)
        self.assertIsInstance(incident_id, int)
        
        # Удаляем тестовый инцидент
        delete_incident(self.conn, incident_id)
    
    def test_get_all_datasets(self):
        """Тест получения всех датасетов"""
        datasets = get_all_datasets(self.conn)
        self.assertIsInstance(datasets, list)
    
    def test_create_dataset(self):
        """Тест создания датасета"""
        test_name = f"Test Dataset {datetime.now().timestamp()}"
        dataset_id = create_dataset(
            self.conn,
            test_name,
            "Test Source",
            "Test Category",
            1024 * 1024,
            "2024-12-14"
        )
        
        self.assertIsNotNone(dataset_id)
        self.assertIsInstance(dataset_id, int)
    
    def test_get_all_tickets(self):
        """Тест получения всех тикетов"""
        tickets = get_all_tickets(self.conn)
        self.assertIsInstance(tickets, list)


class TestIncidentRepository(unittest.TestCase):
    """Тесты для IncidentRepository"""
    
    def test_repository_initialization(self):
        """Тест инициализации репозитория"""
        repo = IncidentRepository()
        self.assertIsNotNone(repo)
    
    def test_get_all_incidents(self):
        """Тест получения всех инцидентов через репозиторий"""
        repo = IncidentRepository()
        incidents = repo.get_all()
        
        self.assertIsInstance(incidents, list)
        # Если есть инциденты, проверяем что это объекты SecurityIncident
        if len(incidents) > 0:
            self.assertIsInstance(incidents[0], SecurityIncident)
            self.assertIsNotNone(incidents[0].id)
            self.assertIsNotNone(incidents[0].title)
    
    def test_get_critical_incidents(self):
        """Тест получения критических инцидентов"""
        repo = IncidentRepository()
        critical = repo.get_critical_incidents()
        
        self.assertIsInstance(critical, list)
        # Все должны быть критическими
        for incident in critical:
            self.assertTrue(incident.is_critical())
    
    def test_get_open_incidents(self):
        """Тест получения открытых инцидентов"""
        repo = IncidentRepository()
        open_incidents = repo.get_open_incidents()
        
        self.assertIsInstance(open_incidents, list)
        # Все должны быть открытыми
        for incident in open_incidents:
            self.assertTrue(incident.is_open())


class TestIntegration(unittest.TestCase):
    """Интеграционные тесты"""
    
    def test_full_workflow(self):
        """Тест полного рабочего процесса"""
        # 1. Создание пользователя
        password = "TestPass123!"
        user = User("testuser", User.hash_password(password), "user")
        self.assertTrue(user.verify_password(password))
        
        # 2. Создание инцидента
        incident = SecurityIncident(
            title="Integration Test Incident",
            severity="High",
            status="open",
            date="2024-12-14"
        )
        self.assertTrue(incident.is_high_priority())
        self.assertTrue(incident.is_open())
        
        # 3. Обновление статуса
        incident.update_status("in_progress")
        self.assertEqual(incident.status, "in_progress")
        
        # 4. Создание датасета
        dataset = Dataset(
            name="Integration Test Dataset",
            source="Test Source",
            category="Test Category",
            size=1024 * 1024 * 200  # 200 MB
        )
        self.assertTrue(dataset.is_large())
        
        # 5. Создание тикета
        ticket = ITTicket(
            ticket_id="INT-TEST-001",
            title="Integration Test Ticket",
            priority="Medium",
            status="open"
        )
        self.assertEqual(ticket.priority, "Medium")
        ticket.escalate_priority()
        self.assertEqual(ticket.priority, "High")


def run_all_tests():
    """Запуск всех тестов"""
    print("=" * 70)
    print("🧪 КОМПЛЕКСНОЕ ТЕСТИРОВАНИЕ INTELLIGENCE PLATFORM")
    print("=" * 70)
    print()
    
    # Создаем test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Добавляем все тесты
    suite.addTests(loader.loadTestsFromTestCase(TestUserModel))
    suite.addTests(loader.loadTestsFromTestCase(TestSecurityIncidentModel))
    suite.addTests(loader.loadTestsFromTestCase(TestDatasetModel))
    suite.addTests(loader.loadTestsFromTestCase(TestITTicketModel))
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestIncidentRepository))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Выводим итоги
    print()
    print("=" * 70)
    print("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("=" * 70)
    print(f"Всего тестов: {result.testsRun}")
    print(f"✅ Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Провалено: {len(result.failures)}")
    print(f"⚠️  Ошибок: {len(result.errors)}")
    
    if result.wasSuccessful():
        print()
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("✅ Проект готов к сдаче!")
    else:
        print()
        print("⚠️  ЕСТЬ ПРОБЛЕМЫ, ТРЕБУЕТСЯ ИСПРАВЛЕНИЕ")
        if result.failures:
            print("\nПроваленные тесты:")
            for test, traceback in result.failures:
                print(f"  - {test}")
        if result.errors:
            print("\nОшибки:")
            for test, traceback in result.errors:
                print(f"  - {test}")
    
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

