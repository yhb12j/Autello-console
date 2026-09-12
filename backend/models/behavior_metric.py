from core.database import as_json, serialize_row


class BehaviorMetric:
    """
    CREATE TABLE IF NOT EXISTS behavior_metrics (
        id SERIAL PRIMARY KEY,
        application_id INTEGER NOT NULL UNIQUE REFERENCES applications(id) ON DELETE CASCADE,
        time_on_page_seconds INTEGER NOT NULL DEFAULT 0,
        buttons_clicked JSONB NOT NULL DEFAULT '[]'::jsonb,
        hover_zones JSONB NOT NULL DEFAULT '[]'::jsonb,
        return_count INTEGER NOT NULL DEFAULT 1,
        extra_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """

    CREATE_SQL = """
    CREATE TABLE IF NOT EXISTS behavior_metrics (
        id SERIAL PRIMARY KEY,
        application_id INTEGER NOT NULL UNIQUE REFERENCES applications(id) ON DELETE CASCADE,
        time_on_page_seconds INTEGER NOT NULL DEFAULT 0,
        buttons_clicked JSONB NOT NULL DEFAULT '[]'::jsonb,
        hover_zones JSONB NOT NULL DEFAULT '[]'::jsonb,
        return_count INTEGER NOT NULL DEFAULT 1,
        extra_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """


class BehaviorMetricCRUD:
    @staticmethod
    def list_all(conn):
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM behavior_metrics ORDER BY id DESC")
            return [serialize_row(row) for row in cursor.fetchall()]

    @staticmethod
    def get_by_id(conn, item_id: int):
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM behavior_metrics WHERE id = %s", (item_id,))
            return serialize_row(cursor.fetchone())

    @staticmethod
    def get_by_application_id(conn, application_id: int):
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM behavior_metrics WHERE application_id = %s",
                (application_id,),
            )
            return serialize_row(cursor.fetchone())

    @staticmethod
    def create(conn, data: dict):
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO behavior_metrics (
                    application_id,
                    time_on_page_seconds,
                    buttons_clicked,
                    hover_zones,
                    return_count,
                    extra_payload
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING *
                """,
                (
                    data["application_id"],
                    int(data.get("time_on_page_seconds") or 0),
                    as_json(data.get("buttons_clicked") or []),
                    as_json(data.get("hover_zones") or []),
                    int(data.get("return_count") or 1),
                    as_json(data.get("extra_payload") or {}),
                ),
            )
            return serialize_row(cursor.fetchone())

    @staticmethod
    def update(conn, item_id: int, data: dict):
        current = BehaviorMetricCRUD.get_by_id(conn, item_id)
        if current is None:
            return None
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE behavior_metrics
                SET time_on_page_seconds = %s,
                    buttons_clicked = %s,
                    hover_zones = %s,
                    return_count = %s,
                    extra_payload = %s
                WHERE id = %s
                RETURNING *
                """,
                (
                    int(data.get("time_on_page_seconds", current["time_on_page_seconds"]) or 0),
                    as_json(data.get("buttons_clicked", current["buttons_clicked"]) or []),
                    as_json(data.get("hover_zones", current["hover_zones"]) or []),
                    int(data.get("return_count", current["return_count"]) or 1),
                    as_json(data.get("extra_payload", current["extra_payload"]) or {}),
                    item_id,
                ),
            )
            return serialize_row(cursor.fetchone())

    @staticmethod
    def delete(conn, item_id: int) -> bool:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM behavior_metrics WHERE id = %s", (item_id,))
            return cursor.rowcount > 0
