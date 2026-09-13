import time
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import Json, RealDictCursor

from .config import settings


def get_connection():
    return psycopg2.connect(
        host=settings.postgres_host,
        port=settings.postgres_port,
        dbname=settings.postgres_db,
        user=settings.postgres_user,
        password=settings.postgres_password,
        cursor_factory=RealDictCursor,
    )


@contextmanager
def get_db():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def wait_for_db(attempts: int = 30, delay: float = 1.0) -> None:
    last_error = None
    for _ in range(attempts):
        try:
            conn = get_connection()
            conn.close()
            return
        except psycopg2.Error as exc:
            last_error = exc
            time.sleep(delay)
    raise RuntimeError(f"PostgreSQL is unavailable: {last_error}")


def serialize_row(row):
    if row is None:
        return None
    payload = dict(row)
    for key, value in payload.items():
        if hasattr(value, "isoformat"):
            payload[key] = value.isoformat()
    return payload


def as_json(value):
    if value is None:
        return Json(None)
    return Json(value)


def init_tables() -> None:
    from models.admin import Admin
    from models.admin_setting import AdminSetting
    from models.application import Application
    from models.behavior_metric import BehaviorMetric

    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(Application.CREATE_SQL)
            cursor.execute(AdminSetting.CREATE_SQL)
            cursor.execute(Admin.CREATE_SQL)
            cursor.execute(BehaviorMetric.CREATE_SQL)
            cursor.execute(BehaviorMetric.MIGRATE_SQL)
