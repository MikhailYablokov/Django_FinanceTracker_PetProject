# Финансовый Трекер / Financial Tracker

[English version below](#english-version)

## Описание проекта

Финансовый Трекер - это веб-приложение на Django, разработанное для эффективного управления личными финансами. Этот проект создан в качестве учебного опыта для углубления знаний в веб-разработке и Django.

### Ключевые особенности:

- Система аутентификации пользователей
- Управление финансовыми транзакциями (создание, редактирование, удаление)
- Категоризация доходов и расходов
- Визуализация финансовых данных
- Отслеживание истории транзакций
- Базовая аналитика финансов

## Технологический стек

- Python 3.x
- Django 3.x
- HTML5, CSS3, JavaScript
- Bootstrap 5
- SQLite (для разработки)

## Установка и запуск

1. Клонируйте репозиторий:
   git clone https://github.com/MikhailYablokov/Django_FinanceTracker_PetProject.git

2. Создайте и активируйте виртуальное окружение:
   python -m venv venv
   source venv/bin/activate  # Для Windows: venv\Scripts\activate

3. Установите зависимости:
   pip install -r requirements.txt
   
4. Перейдите в директорию проекта:
   cd src

6. Примените миграции:
   python manage.py migrate

7. Запустите сервер разработки:
   python manage.py runserver

8. Откройте в браузере: http://localhost:8000


# English Version

## Project Description

Financial Tracker is a Django-based web application designed for effective personal finance management. This project was created as a learning experience to deepen knowledge in web development and Django.

### Key Features:

- User authentication system
- Financial transaction management (create, edit, delete)
- Income and expense categorization
- Financial data visualization
- Transaction history tracking
- Basic financial analytics

## Technology Stack

- Python 3.x
- Django 3.x
- HTML5, CSS3, JavaScript
- Bootstrap 5
- SQLite (for development)

## Installation and Setup

1. Clone the repository:
   git clone https://github.com/MikhailYablokov/Django_FinanceTracker_PetProject.git

2. Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Navigate to the project directory:
   cd src

5. Apply migrations:
   python manage.py migrate

6. Run the development server:
   python manage.py runserver

7. Open in browser: http://localhost:8000

