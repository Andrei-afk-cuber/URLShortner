# URLShortner

Простой сервис для сокращения ссылок на FastAPI и PostgreSQL. Принимает длинный URL, возвращает короткий код, перенаправляет по нему на оригинальный адрес и считает количество переходов.

## Возможности

- Создание короткого кода для URL с валидацией входных данных
- Редирект на оригинальный адрес (HTTP 307)
- Счётчик переходов по каждой ссылке
- Эндпоинт статистики по коду
- Health check для мониторинга
- Асинхронная работа с PostgreSQL (SQLAlchemy + asyncpg)
- Миграции через Alembic
- Тесты на pytest, которые запускаются перед стартом приложения

## Стек

- Python, FastAPI, Uvicorn
- SQLAlchemy (async) + asyncpg
- PostgreSQL
- Alembic
- Pydantic / pydantic-settings
- pytest + pytest-asyncio
- Docker / Docker Compose

## Структура проекта

```
URLShortner/
├── alembic/              # миграции БД
├── app/
│   ├── main.py           # FastAPI-приложение и эндпоинты
│   ├── crud.py           # работа с БД
│   ├── database.py       # подключение к БД и зависимость сессии
│   └── schemas.py        # Pydantic-схемы
├── tests/                # тесты
├── .env.example          # пример переменных окружения
├── alembic.ini
├── docker-compose.yaml
├── Dockerfile
├── pytest.ini
└── requirements.txt
```

## Быстрый старт (Docker Compose)

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/Andrei-afk-cuber/URLShortner.git
cd URLShortner
```

### 2. Создайте файл `.env`

```bash
cp .env.example .env
```

| Переменная     | Описание                    | Значение по умолчанию |
|----------------|-----------------------------|-----------------------|
| `DB_USER`      | Пользователь PostgreSQL     | `postgres`            |
| `DB_PASSWORD`  | Пароль PostgreSQL           | `password`            |
| `DB_HOST`      | Хост базы данных            | `localhost`           |
| `DB_PORT`      | Порт основной БД            | `5432`                |
| `DB_TEST_PORT` | Порт тестовой БД            | `5433`                |
| `DB_NAME`      | Имя базы данных             | `postgres`            |

> Смените пароль перед использованием вне локальной разработки.

### 3. Запустите проект

```bash
docker compose up --build
```

Сервисы запускаются в таком порядке:

1. `test_db` — тестовая база данных
2. `test` — прогон тестов (`pytest`); если тесты падают, остальные сервисы не стартуют
3. `db` — основная база данных
4. `migration` — применение миграций (`alembic upgrade head`)
5. `app` — запуск сервиса

После запуска сервис доступен на http://localhost:8000, а Swagger UI — на http://localhost:8000/docs.

## Локальный запуск без Docker

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# поднимите PostgreSQL (например, только сервис db) и настройте .env
alembic upgrade head
uvicorn app.main:app --reload
```

## API

| Метод | Путь             | Описание                                         | Ответ                          |
|-------|------------------|--------------------------------------------------|--------------------------------|
| GET   | `/health`        | Проверка работоспособности                       | `200`, `{"status": "ok"}`      |
| POST  | `/shorten`       | Создать короткий код для URL                     | `201`, код в теле (text/plain) |
| GET   | `/{code}`        | Редирект на оригинальный URL, +1 к счётчику      | `307` + заголовок `Location`   |
| GET   | `/stats/{code}`  | Статистика по ссылке                             | `200`, JSON                    |

### Примеры

Создание короткой ссылки:

```bash
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://example.com/very/long/link"}'
# -> abc123
```

<!-- TODO: проверьте имя поля в схеме LinkBase (original_url / url) -->

Переход по короткой ссылке:

```bash
curl -i http://localhost:8000/abc123
```

Статистика:

```bash
curl http://localhost:8000/stats/abc123
```

## Тесты

Через Docker Compose:

```bash
docker compose up --build test
```

Локально (нужна запущенная тестовая БД на порту `DB_TEST_PORT`):

```bash
pytest
```

## Миграции

```bash
# создать миграцию после изменения моделей
alembic revision --autogenerate -m "описание изменений"

# применить миграции
alembic upgrade head
```