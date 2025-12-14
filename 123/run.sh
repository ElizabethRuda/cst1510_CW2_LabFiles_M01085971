#!/bin/bash

# Скрипт для запуска Intelligence Platform Dashboard

echo "🚀 Запуск Intelligence Platform Dashboard..."
echo ""

# Проверка наличия Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python3."
    exit 1
fi

# Проверка наличия pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 не найден. Установите pip3."
    exit 1
fi

# Установка зависимостей
echo "📦 Установка зависимостей..."
pip3 install -r requirements.txt

# Запуск приложения
echo ""
echo "✅ Запуск Streamlit приложения..."
echo "📊 Приложение откроется в браузере автоматически"
echo ""
streamlit run app.py

