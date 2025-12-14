# 🌐 Как открыть приложение в браузере

## ✅ Отчет создан!

**Файл отчета:** `Streamlit_Visualization/CW2_REPORT.md`

Отчет содержит:
- ✅ Section 1: Introduction and Project Scope
- ✅ Section 2: System Architecture and Implementation
- ✅ Section 3: High-Value Analysis and Insights (с конкретными рекомендациями)
- ✅ Section 4: Reflection and Conclusion
- ✅ Appendix: Running Instructions

**Word Count:** ~1,200 слов (в пределах требований 1000-1500)

---

## 🚀 Запуск приложения в браузере

### Вариант 1: Запуск вручную

```bash
cd /home/stud/123/Streamlit_Visualization
streamlit run Home.py
```

Приложение автоматически откроется в браузере по адресу:
- **Local URL:** http://localhost:8501
- **Network URL:** http://192.168.x.x:8501

### Вариант 2: Если приложение уже запущено

Просто откройте в браузере:
```
http://localhost:8501
```

### Вариант 3: Запуск с указанием порта

```bash
cd /home/stud/123/Streamlit_Visualization
streamlit run Home.py --server.port=8501
```

---

## 🔐 Данные для входа

**Логин:** `admin`  
**Пароль:** `Admin123!`

Или используйте другие тестовые аккаунты:
- `test` / `Test123!`
- `user` / `User123!`

---

## 📊 Что увидите в приложении

### После входа:

1. **Главная страница Dashboard:**
   - Ключевые метрики (Total Incidents, Active, Critical, Datasets, Tickets)
   - Переключатель темы (Light/Dark Mode)

2. **Вкладки:**
   - 🛡️ **Cyber Incidents** - инциденты с фильтрами и графиками
   - 📚 **Datasets** - метаданные датасетов
   - 🎫 **IT Tickets** - тикеты с аналитикой
   - 📈 **Analytics** - общая статистика
   - 🤖 **AI Assistant** - чат с ChatGPT (если настроен API key)

3. **Функции:**
   - Интерактивные графики Plotly
   - Фильтры по всем параметрам
   - Временные линии
   - Таблицы данных

---

## 🎨 Версии дизайна

### Light Mode (Белый):
- Классический светлый дизайн
- Стандартные цвета
- Подходит для дневной работы

### Dark Mode (Космический):
- Темная тема с градиентами
- Зеленый, фиолетовый, бордовый
- Космические элементы 🛸 🚀

**Переключение:** Кнопка в сайдбаре "🌙 Switch to Dark Mode"

---

## 🤖 AI Assistant

Для использования AI Assistant:

1. **Получить API key:**
   - Зайти на https://platform.openai.com/api-keys
   - Создать новый ключ

2. **Установить:**
   ```bash
   export OPENAI_API_KEY=your_key_here
   ```

3. **Использовать:**
   - Перейти на вкладку "🤖 AI Assistant"
   - Задать вопрос или использовать quick actions

---

## 📝 Отчет

**Файл:** `Streamlit_Visualization/CW2_REPORT.md`

Отчет готов к использованию. Нужно только:
- [ ] Заменить [Your Name], [Student ID] на реальные данные
- [ ] Добавить скриншоты графиков (опционально)
- [ ] Вставить диаграммы из UML_DIAGRAM.txt и DFD_DIAGRAM.txt

---

## 🐛 Если не открывается

1. **Проверить, что приложение запущено:**
   ```bash
   ps aux | grep streamlit
   ```

2. **Проверить порт:**
   ```bash
   netstat -tlnp | grep 8501
   ```

3. **Перезапустить:**
   ```bash
   pkill -f streamlit
   cd /home/stud/123/Streamlit_Visualization
   streamlit run Home.py
   ```

4. **Проверить зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

---

## ✅ Готово!

Приложение готово к использованию. Откройте браузер и перейдите по адресу:
**http://localhost:8501**

Удачи! 🚀

