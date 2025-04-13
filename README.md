# Repair Service

Курсовой проект **Repair Service** – это система для управления ремонтными заявками, предназначенная для удобного взаимодействия клиентов, администраторов и мастеров. Приложение позволяет пользователям оставлять заявки на ремонт, а администраторам и мастерам — отслеживать и управлять процессом выполнения работ.

## Описание проекта

**Repair Service** – это веб-приложение для организации и управления ремонтными работами. Проект позволяет пользователям:
- Регистрироваться и создавать заявки на ремонт;
- Просматривать статус своих заявок;
- Получать уведомления о ходе выполнения ремонта.

Для администраторов и мастеров проект предоставляет удобные инструменты для:
- Управления заявками;
- Назначения мастеров на выполнение работ;
- Изменения статусов заявок и ведения истории ремонтов.

## Особенности

- **Удобство использования:** интуитивно понятный интерфейс для клиентов и администраторов.
- **Гибкая архитектура:** возможность масштабирования и добавления новых функциональных модулей.
- **Интеграция с базами данных:** хранение данных о заявках, пользователях и истории ремонтов.
- **Безопасность:** защита данных с помощью современных методов аутентификации и авторизации.

## Технологии

- **Язык программирования:** Python  
- **Веб-фреймворк:** Flask
- **База данных:** PostgreSQL
- **ORM:** SQLAlchemy
- **Контейнеризация:** Docker

## Структура проекта
- repair_service/
├── .venv/                # Виртуальное окружение
├── app/                  # Основной код приложения
│   ├── __init__.py       # Инициализация приложения
│   ├── models.py         # Модели базы данных
│   ├── routes.py         # Роуты и представления
│   ├── templates/        # HTML-шаблоны
│   └── static/           # Статические файлы (CSS, JS, изображения)
├── migrations/           # Миграции базы данных (если используются)
├── requirements.txt      # Список зависимостей
├── .env                  # Переменные окружения

## Установка и запуск

```bash
git clone https://github.com/loxsvetoch/repair_service.git
cd repair_service
python3 -m venv .venv
source .venv/bin/activate  # для Linux/MacOS
pip install -r requirements.txt
# миграция БД
flask db upgrade
#запуск
flask run
```

