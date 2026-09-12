# Autéllo Barskiy

Закрытый контур приёма заявок частного автоателье: витрина, FastAPI и PostgreSQL работают в одном Docker Compose. Браузер видит только Nginx. Запись в базу идёт через backend.

## Состав контура

- Nginx — публичная точка входа, статика из `frontend/dist` и обратный прокси на API
- FastAPI — заявки, метрики сессии и настройки витрины
- PostgreSQL — хранилище, порт наружу не публикуется
- pgAdmin — просмотр таблиц
- Watchtower — обновление помеченных контейнеров
- Docker Registry — приватный реестр образов

## Требования

- Docker Engine и плагин Docker Compose
- Node.js 20+ и npm — только если нужно пересобрать витрину

## Быстрый запуск

```bash
cp .env.example .env
```

Заполните пароли в `.env`. Если порты `80` или `8000` заняты, задайте свободные значения `NGINX_HTTP_PORT` и `BACKEND_PORT`.

```bash
cd frontend
npm install
npm run build
cd ..

docker compose up -d --build

# Приватный реестр и Watchtower включаются отдельно:
# cd registry && ./create-user.sh admin '<пароль>' && cd ..
# docker compose --profile ops up -d
```

## Точки доступа

| Сервис        | Адрес                                      |
|---------------|--------------------------------------------|
| Витрина       | `http://<host>/`                           |
| Кабинет услуг | `http://<host>/admin`                      |
| Swagger       | `http://<host>/docs` и `http://<host>:<BACKEND_PORT>/docs` |
| pgAdmin       | `http://<host>:<PGADMIN_PORT>/`            |
| Registry      | `http://<host>:<REGISTRY_PORT>/v2/`        |

Postgres доступен только по имени сервиса `db` внутри сети `internal`. Backend ходит к нему по `POSTGRES_HOST=db`.

### pgAdmin

1. Войдите с `PGADMIN_DEFAULT_EMAIL` и `PGADMIN_DEFAULT_PASSWORD`.
2. Откройте сервер **Autello PostgreSQL**:
   - Host: `db`
   - Port: `5432`
   - Username / Password: `POSTGRES_USER` и `POSTGRES_PASSWORD`

## API

Клиентская страница вызывает API через `/api/...`. Nginx снимает префикс и передаёт запрос в backend.

| Метод | Путь | Назначение |
| --- | --- | --- |
| GET | `/health` | Проверка сервиса |
| GET/POST | `/admin-settings` | Список и создание услуг |
| GET/PUT/DELETE | `/admin-settings/{id}` | Карточка услуги |
| GET/POST | `/applications` | Список и создание заявок |
| GET/PUT/DELETE | `/applications/{id}` | Карточка заявки |
| GET/POST | `/behavior-metrics` | Метрики сессии |

Логи backend:

```bash
docker logs -f backend
```

## Сети

- `edge` — Nginx, backend, pgAdmin, Registry
- `internal` — PostgreSQL и служебный трафик между backend и `db`

## Сборка витрины

Исходники лежат в `frontend/src`. Сборка пишет HTML, JS и CSS в `frontend/dist`. Стили выносятся через `mini-css-extract-plugin`, Nginx отдаёт их как статику с корня сайта.
