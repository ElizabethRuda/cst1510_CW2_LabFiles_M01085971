#!/usr/bin/env python3
"""
Простой скрипт для проверки тестовых пользователей
"""

# Тестовые пользователи
test_users = {
    "admin": "Admin123!",
    "test": "Test123!",
    "user": "User123!"
}

print("=" * 50)
print("Тестовые учетные записи для входа:")
print("=" * 50)
print()

for username, password in test_users.items():
    print(f"Логин: {username:10} | Пароль: {password}")

print()
print("=" * 50)
print("Инструкция:")
print("1. Запустите: streamlit run Home.py")
print("2. Если видите ошибку 'Invalid username or password':")
print("   - Нажмите кнопку 'Инициализировать тестовых пользователей'")
print("   - Или перезапустите приложение (Ctrl+C и снова streamlit run)")
print("3. Введите логин и пароль из таблицы выше")
print("=" * 50)


