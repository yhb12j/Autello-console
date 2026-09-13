# Autéllo Barskiy

Закрытый контур приёма заявок частного автоателье. Браузер видит только Nginx на 443. Backend и PostgreSQL остаются во внутренней сети. Порты 8000 и 5432 снаружи отвечают отказом.

## Состав контура

- Nginx — HTTPS-вход, статика из `frontend/dist`, обратный прокси на API
- FastAPI — заявки, анонимные метрики сессии, услуги и JWT-кабинет
- PostgreSQL — хранилище без публикации рабочего порта наружу

## Требования

- Docker Engine и плагин Docker Compose
- Node.js 20+ и npm — только если нужно пересобрать витрину

## Быстрый запуск

```bash
cp .env.example .env
```

Заполните `POSTGRES_PASSWORD` и `SECRET_KEY`. Ключ можно получить так:

```bash
openssl rand -hex 32
```

```bash
cd frontend
npm install
npm run build
cd ..

docker compose up -d --build
```

Первый вход в кабинет создаёт единственного оператора. После этого регистрация закрывается.

## Точки доступа

| Сервис   | Адрес                    |
|----------|--------------------------|
| Витрина  | `https://<host>/`        |
| Кабинет  | `https://<host>/admin`   |
| Swagger  | `https://<host>/docs`    |

Прямые обращения на `8000` и `5432` получают `403`. Если эти порты на хосте заняты, задайте `CLOSED_API_PORT` и `CLOSED_DB_PORT` в `.env`.

## API

Клиент ходит в `/api/...`. Nginx снимает префикс и передаёт запрос в backend.

| Метод | Путь | Назначение |
| --- | --- | --- |
| GET | `/health` | Проверка сервиса |
| GET/POST | `/auth/check`, `/auth/register`, `/auth/login`, `/auth/token` | Контур входа |
| GET | `/auth/me`, `/auth/verify` | Текущий оператор и проверка JWT |
| GET/POST/PUT/DELETE | `/admin-settings` | Услуги витрины |
| POST | `/applications` | Новая заявка |
| GET | `/applications`, `/applications/queue` | Список и ранжированная очередь |
| POST | `/behavior-metrics` | Анонимные метрики сессии |
| GET | `/behavior-metrics`, `/behavior-metrics/summary` | Журнал и сводка |

Изменение услуг, чтение заявок и сводка метрик требуют Bearer-токен.

## Схема операторов

```sql
CREATE TABLE IF NOT EXISTS admins (
    id SERIAL PRIMARY KEY,
    login VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(180),
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

Тестовые заявки: `scripts/seed-applications.sql`.

## Логи

```bash
docker logs -f backend
```

## Сети

- `edge` — Nginx
- `internal` — backend и `db`

## Сборка витрины

Исходники лежат в `frontend/src`. Сборка пишет HTML, JS и CSS в `frontend/dist`.
