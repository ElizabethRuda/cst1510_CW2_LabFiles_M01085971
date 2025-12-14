# 📋 План улучшений проекта на основе требований CW2

## ✅ Что уже сделано

- ✅ Week 7: Security & File Persistence (Hashing) - `auth.py` с bcrypt
- ✅ Week 8: Data Pipeline & CRUD (SQL) - База данных SQLite, CRUD операции
- ✅ Week 9: Web Interface, MVC & Visualization - Streamlit, Plotly графики
- ✅ Все три домена реализованы (Tier 3 - High Distinction)
- ✅ Интерактивные визуализации
- ✅ Фильтры и аналитика

## ❌ Что нужно добавить

### 1. Week 10: AI Integration (КРИТИЧНО!)

**Требование:** Интеграция ChatGPT API для AI Assistant

**Что нужно:**
- [ ] Создать функцию для вызова OpenAI API
- [ ] Добавить AI Assistant в дашборды (минимум один домен)
- [ ] Chat box для вопросов по данным
- [ ] Обработка ошибок API
- [ ] Environment variable для API key

**Файлы для создания:**
- `app/services/ai_service.py` - сервис для работы с OpenAI
- Обновить `pages/Dashboard.py` - добавить AI чат
- `.env.example` - пример файла с API key

### 2. Week 11: OOP Refactoring (КРИТИЧНО!)

**Требование:** Рефакторинг в OOP структуру

**Что нужно:**
- [ ] Создать классы для сущностей:
  - `User` класс
  - `SecurityIncident` класс
  - `Dataset` класс
  - `ITTicket` класс
- [ ] Рефакторинг процедурного кода в методы классов
- [ ] Перенос бизнес-логики в классы
- [ ] UML Class Diagram

**Файлы для создания:**
- `app/models/user.py`
- `app/models/incident.py`
- `app/models/dataset.py`
- `app/models/ticket.py`

### 3. Report Requirements (1000-1500 слов)

**Структура отчета:**
- [ ] Section 1: Introduction and Project Scope
- [ ] Section 2: System Architecture and Implementation
  - [ ] Data Flow Diagram (DFD) или MVC Diagram
  - [ ] UML Class Diagram или ER Diagram
- [ ] Section 3: High-Value Analysis and Insights
  - [ ] Problem Statement для каждого домена
  - [ ] Analysis and Findings с скриншотами
  - [ ] Actionable Recommendations
- [ ] Section 4: Reflection and Conclusion
- [ ] Appendix: Running Instructions

### 4. Дополнительные улучшения

- [ ] Улучшить документацию (README.md)
- [ ] Добавить docstrings во все функции
- [ ] Создать UML диаграммы
- [ ] Добавить примеры использования
- [ ] Улучшить error handling

---

## 🎯 Приоритеты

### Высокий приоритет (обязательно):
1. **AI Integration** - Week 10 requirement
2. **OOP Refactoring** - Week 11 requirement
3. **Report** - обязательная часть оценки (35%)

### Средний приоритет:
4. UML/ER Diagrams для отчета
5. Улучшение документации
6. High-Value Analysis

### Низкий приоритет:
7. Дополнительные фичи
8. Улучшение UI/UX

---

## 📊 Оценка текущего состояния

**Tier Level:** Tier 3 (High Distinction) - ✅ Все три домена реализованы

**Marking Criteria:**
- Report and Technical Explanation (35%): ⚠️ Нужен отчет
- Software Functionality (40%): ✅ 90% - не хватает AI
- Code Quality (15%): ⚠️ 70% - нужен OOP рефакторинг
- Analytical Insights (10%): ✅ 80% - есть, но нужно оформить в отчет

**Текущая оценка:** ~75-80% (Merit/Distinction)
**Потенциальная оценка с улучшениями:** 85-100% (High Distinction)

---

## 🚀 План действий

### Шаг 1: AI Integration (Week 10)
1. Создать `app/services/ai_service.py`
2. Добавить AI чат в Dashboard
3. Настроить environment variables
4. Тестирование

### Шаг 2: OOP Refactoring (Week 11)
1. Создать модели (User, Incident, Dataset, Ticket)
2. Рефакторинг существующего кода
3. Создать UML диаграмму
4. Обновить документацию

### Шаг 3: Report
1. Написать Section 1-4
2. Создать диаграммы (DFD, UML, ER)
3. Добавить скриншоты
4. Проверить word count (1000-1500)

### Шаг 4: Final Polish
1. Улучшить документацию
2. Добавить примеры
3. Финальное тестирование
4. Подготовка к submission

