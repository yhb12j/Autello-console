from core.database import serialize_row


class AdminSetting:
    """
    CREATE TABLE IF NOT EXISTS admin_settings (
        id SERIAL PRIMARY KEY,
        services VARCHAR(240) NOT NULL,
        budget_range VARCHAR(120) NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """

    CREATE_SQL = """
    CREATE TABLE IF NOT EXISTS admin_settings (
        id SERIAL PRIMARY KEY,
        services VARCHAR(240) NOT NULL,
        budget_range VARCHAR(120) NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """


class AdminSettingCRUD:
    @staticmethod
    def list_all(conn):
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM admin_settings ORDER BY id ASC")
            return [serialize_row(row) for row in cursor.fetchall()]

    @staticmethod
    def get_by_id(conn, item_id: int):
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM admin_settings WHERE id = %s", (item_id,))
            return serialize_row(cursor.fetchone())

    @staticmethod
    def create(conn, data: dict):
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO admin_settings (services, budget_range)
                VALUES (%s, %s)
                RETURNING *
                """,
                (str(data["services"]), str(data["budget_range"])),
            )
            return serialize_row(cursor.fetchone())

    @staticmethod
    def update(conn, item_id: int, data: dict):
        current = AdminSettingCRUD.get_by_id(conn, item_id)
        if current is None:
            return None
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE admin_settings
                SET services = %s,
                    budget_range = %s,
                    updated_at = NOW()
                WHERE id = %s
                RETURNING *
                """,
                (
                    str(data.get("services", current["services"])),
                    str(data.get("budget_range", current["budget_range"])),
                    item_id,
                ),
            )
            return serialize_row(cursor.fetchone())

    @staticmethod
    def delete(conn, item_id: int) -> bool:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM admin_settings WHERE id = %s", (item_id,))
            return cursor.rowcount > 0
