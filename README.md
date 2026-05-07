# FastAPI Project

Коледжний проєкт: FastAPI, PostgreSQL (async SQLAlchemy), Alembic, JWT + cookies, Docker, Prometheus/Grafana, pytest на окремій БД.

## Можливості (вимоги лаб)

- **Лаб 1–2:** Poetry, `.gitignore`, гілки; Docker Compose — `fastapi` + `postgres`, volume `.:/app`, `uvicorn --reload`.
- **Лаб 3–4:** Роутери, Pydantic, GET/POST/PUT/DELETE; ≥5 моделей зі зв’язками 1:1 та 1:N; async CRUD; Alembic; seed-дані (`python -m app.db.seed`).
- **Лаб 5:** Реєстрація/логін, JWT і HTTP-only cookie, паролі лише bcrypt; захищені ендпоїнти (`/auth/me`, список користувачів, створення замовлення).
- **Лаб 6:** Pytest на `TEST_DATABASE_URL` (PostgreSQL), підміна `get_db`.
- **Лаб 7:** Prometheus + Grafana + postgres-exporter + cadvisor у Compose; кастомна метрика `ecommerce_orders_total_value` на `/metrics`.
- **Лаб 8:** Заготовка workflow — `.github/workflows/deploy-aws-template.yml`; налаштуйте AWS і секрети під свій акаунт.

## Структура

```
├── app/
│   ├── main.py
│   ├── api/v1/endpoints/   # auth, users, profiles, categories, products, orders, order-items
│   ├── core/               # config, security, exceptions
│   ├── crud/
│   ├── db/
│   ├── models/             # User, UserProfile, Category, Product, Order, OrderItem
│   ├── schemas/
│   ├── metrics.py
│   └── utils/
├── alembic/
├── monitoring/             # prometheus.yml, Grafana provisioning
├── tests/
├── docker-compose.yml
├── docker-entrypoint.sh    # alembic upgrade + seed + uvicorn --reload
├── Dockerfile
├── pyproject.toml
└── .env.example
```

## Швидкий старт (Docker)

1. Скопіюйте `.env.example` у `.env` за потреби.
2. `docker compose up --build` (на Docker Desktop для Windows сервіс `cadvisor` може потребувати WSL2/Linux; за потреби тимчасово закоментуйте його в `docker-compose.yml`).
3. API: http://localhost:8000/docs  
4. Prometheus: http://localhost:9090  
5. Grafana: http://localhost:3000 (admin / admin за замовчуванням)

## Локально (Poetry)

```bash
poetry install
cp .env.example .env
# PostgreSQL + створіть БД fastapi_test для тестів (див. scripts/init-multiple-dbs.sh у контейнері)
poetry run alembic upgrade head
poetry run python -m app.db.seed
poetry run uvicorn app.main:app --reload
```

## Тести

Потрібна PostgreSQL і БД `fastapi_test`, схема через Alembic:

```bash
set DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/fastapi_test
set TEST_DATABASE_URL=%DATABASE_URL%
poetry run alembic upgrade head
poetry run pytest
```

CI: `.github/workflows/ci.yml`.

## Автор

Boryslaw Humenuik

## License

MIT
