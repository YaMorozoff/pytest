FastAPI Orders & Auth System 🚀
Простой и мощный бэкенд для системы заказов с полноценной JWT-авторизацией, упакованный в Docker.

🛠 Технологии
Framework: FastAPI

Language: Python 3.14 (uv as package manager)

Database: PostgreSQL + SQLAlchemy 2.0

Migrations: Alembic

Security: JWT (python-jose), Bcrypt для хеширования паролей

Infrastructure: Docker & Docker Compose

✨ Основные возможности
Auth: Регистрация и логин с выдачей JWT-токенов.

Security: Защищенные маршруты (только авторизованные пользователи могут создавать заказы).

Orders CRUD: Создание, чтение, обновление и удаление заказов с привязкой к current_user.

Relationships: Автоматическая подгрузка данных о продуктах внутри заказов (Eager Loading).

Validation: Строгая валидация данных через Pydantic.

🚀 Быстрый старт

1. Клонирование репозитория
   Bash
   git clone https://github.com/yourusername/pytest.git
   cd pytest
2. Настройка окружения
   Создайте файл .env в корне проекта (или проверьте настройки в docker-compose.yml):

POSTGRES_USER=yan
POSTGRES_PW=azazel
POSTGRES_DB=postgres
PGADMIN_MAIL=morozoff.ian@yandex.ru
PGADMIN_PW=azazel

3. Заранее установить uv и make, сделать uv sync

4. Все сервисы (API, DB, pgAdmin) поднимаются одной командой:

docker-compose up -d

5. Применение миграций
   После того как контейнеры запустятся, создайте структуру таблиц в базе данных:
   docker exec -it myapp uv run alembic upgrade head

6. Swagger
   http://localhost:8000/docs#/

7. Запуск теста
   docker exec -it myapp env PYTHONPATH=/workspace/app uv run python -m pytest app/tests/test_auth.py

Bash
docker exec -it myapp uv run alembic upgrade head
📖 API Документация
После запуска документация доступна по адресу:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

Основные эндпоинты:
POST /auth/register — Регистрация нового пользователя.

POST /auth/login — Получение JWT-токена.

GET /orders/ — Список заказов текущего пользователя (требует токен).

POST /orders/ — Создание заказа (автоматическая привязка к user_id из токена).

🏗 Структура проекта
Plaintext
.
├── app/
│ ├── main.py # Точка входа в приложение
│ ├── models.py # Модели SQLAlchemy
│ ├── schemas.py # Схемы Pydantic
│ ├── database.py # Настройка подключения к БД
│ ├── security.py # Логика JWT и хеширования
│ ├── crud/ # Логика работы с БД (создание, удаление и т.д.)
│ └── routers/ # Контроллеры (auth, users, orders)
├── alembic/ # Миграции базы данных
├── docker-compose.yml # Описание контейнеров
└── pyproject.toml # Зависимости (uv)
🛠 Команды для разработки
Пересборка: docker-compose up -d --build

Просмотр логов: docker-compose logs -f myapp

Создание новой миграции:
docker exec -it myapp uv run alembic revision --autogenerate -m "description"

📋 План развития (Roadmap)
[x] JWT Авторизация

[x] CRUD Заказов

[ ] Роли пользователей (Admin/User)

[ ] Пагинация для списка продуктов

[ ] Покрытие тестами через Pytest
