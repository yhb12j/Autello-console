from core.database import serialize_row


class BehaviorMetric:
    """
    CREATE TABLE IF NOT EXISTS behavior_metrics (
        id SERIAL PRIMARY KEY,
        time_on_page INTEGER NOT NULL DEFAULT 0,
        buttons_clicked TEXT NOT NULL DEFAULT '',
        cursor_positions TEXT NOT NULL DEFAULT '',
        return_frequency INTEGER NOT NULL DEFAULT 0,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """

    CREATE_SQL = """
    CREATE TABLE IF NOT EXISTS behavior_metrics (
        id SERIAL PRIMARY KEY,
        time_on_page INTEGER NOT NULL DEFAULT 0,
        buttons_clicked TEXT NOT NULL DEFAULT '',
        cursor_positions TEXT NOT NULL DEFAULT '',
        return_frequency INTEGER NOT NULL DEFAULT 0,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """

    MIGRATE_SQL = """
    ALTER TABLE behavior_metrics DROP CONSTRAINT IF EXISTS behavior_metrics_application_id_fkey;
    ALTER TABLE behavior_metrics DROP CONSTRAINT IF EXISTS behavior_metrics_application_id_key;
    ALTER TABLE behavior_metrics ADD COLUMN IF NOT EXISTS time_on_page INTEGER NOT NULL DEFAULT 0;
    ALTER TABLE behavior_metrics ADD COLUMN IF NOT EXISTS cursor_positions TEXT NOT NULL DEFAULT '';
    ALTER TABLE behavior_metrics ADD COLUMN IF NOT EXISTS return_frequency INTEGER NOT NULL DEFAULT 0;
    ALTER TABLE behavior_metrics ALTER COLUMN buttons_clicked DROP DEFAULT;
    ALTER TABLE behavior_metrics ALTER COLUMN buttons_clicked TYPE TEXT USING COALESCE(buttons_clicked::text, '');
    ALTER TABLE behavior_metrics ALTER COLUMN buttons_clicked SET DEFAULT '';
    ALTER TABLE behavior_metrics ALTER COLUMN application_id DROP NOT NULL;
    ALTER TABLE behavior_metrics ALTER COLUMN application_id SET DEFAULT 0;
    """


class BehaviorMetricCRUD:
    @staticmethod
    def list_all(conn, skip: int = 0, limit: int = 100):
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, time_on_page, buttons_clicked, cursor_positions, return_frequency, created_at
                FROM behavior_metrics
                ORDER BY id DESC
                OFFSET %s LIMIT %s
                """,
                (skip, limit),
            )
            return [serialize_row(row) for row in cursor.fetchall()]

    @staticmethod
    def create(conn, data: dict):
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO behavior_metrics (
                    time_on_page,
                    buttons_clicked,
                    cursor_positions,
                    return_frequency
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id, time_on_page, buttons_clicked, cursor_positions, return_frequency, created_at
                """,
                (
                    int(data.get("time_on_page") or 0),
                    str(data.get("buttons_clicked") or ""),
                    str(data.get("cursor_positions") or ""),
                    int(data.get("return_frequency") or 0),
                ),
            )
            return serialize_row(cursor.fetchone())

    @staticmethod
    def summary(conn):
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    COALESCE(AVG(time_on_page) FILTER (WHERE created_at >= NOW() - INTERVAL '1 day'), 0) AS avg_day,
                    COALESCE(MAX(time_on_page) FILTER (WHERE created_at >= NOW() - INTERVAL '1 day'), 0) AS max_day,
                    COALESCE(AVG(time_on_page) FILTER (WHERE created_at >= NOW() - INTERVAL '7 day'), 0) AS avg_week,
                    COALESCE(MAX(time_on_page) FILTER (WHERE created_at >= NOW() - INTERVAL '7 day'), 0) AS max_week,
                    COALESCE(AVG(time_on_page) FILTER (WHERE created_at >= NOW() - INTERVAL '30 day'), 0) AS avg_month,
                    COALESCE(MAX(time_on_page) FILTER (WHERE created_at >= NOW() - INTERVAL '30 day'), 0) AS max_month,
                    COUNT(*) AS total
                FROM behavior_metrics
                """
            )
            row = serialize_row(cursor.fetchone()) or {}
            cursor.execute(
                """
                SELECT cursor_positions
                FROM behavior_metrics
                WHERE cursor_positions <> ''
                ORDER BY id DESC
                LIMIT 400
                """
            )
            points = [item["cursor_positions"] for item in cursor.fetchall()]
        return {**row, "cursor_samples": points}
