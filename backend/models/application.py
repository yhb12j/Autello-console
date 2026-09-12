from core.database import serialize_row


class Application:
    """
    CREATE TABLE IF NOT EXISTS applications (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(120) NOT NULL,
        last_name VARCHAR(120) NOT NULL,
        patronymic VARCHAR(120) DEFAULT '',
        phone VARCHAR(64) NOT NULL,
        email VARCHAR(180) NOT NULL,
        business_info TEXT NOT NULL DEFAULT '',
        business_niche VARCHAR(180) NOT NULL DEFAULT '',
        company_size VARCHAR(80) NOT NULL DEFAULT '',
        business_size VARCHAR(80) NOT NULL DEFAULT '',
        role VARCHAR(40) NOT NULL DEFAULT '',
        task_volume VARCHAR(180) NOT NULL DEFAULT '',
        need_volume VARCHAR(180) NOT NULL DEFAULT '',
        deadline VARCHAR(120) NOT NULL DEFAULT '',
        task_type VARCHAR(180) NOT NULL DEFAULT '',
        product VARCHAR(240) NOT NULL DEFAULT '',
        budget VARCHAR(80) NOT NULL DEFAULT '',
        contact_method VARCHAR(80) NOT NULL DEFAULT '',
        convenient_time VARCHAR(120) NOT NULL DEFAULT '',
        comment TEXT NOT NULL DEFAULT '',
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """

    CREATE_SQL = """
    CREATE TABLE IF NOT EXISTS applications (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(120) NOT NULL,
        last_name VARCHAR(120) NOT NULL,
        patronymic VARCHAR(120) DEFAULT '',
        phone VARCHAR(64) NOT NULL,
        email VARCHAR(180) NOT NULL,
        business_info TEXT NOT NULL DEFAULT '',
        business_niche VARCHAR(180) NOT NULL DEFAULT '',
        company_size VARCHAR(80) NOT NULL DEFAULT '',
        business_size VARCHAR(80) NOT NULL DEFAULT '',
        role VARCHAR(40) NOT NULL DEFAULT '',
        task_volume VARCHAR(180) NOT NULL DEFAULT '',
        need_volume VARCHAR(180) NOT NULL DEFAULT '',
        deadline VARCHAR(120) NOT NULL DEFAULT '',
        task_type VARCHAR(180) NOT NULL DEFAULT '',
        product VARCHAR(240) NOT NULL DEFAULT '',
        budget VARCHAR(80) NOT NULL DEFAULT '',
        contact_method VARCHAR(80) NOT NULL DEFAULT '',
        convenient_time VARCHAR(120) NOT NULL DEFAULT '',
        comment TEXT NOT NULL DEFAULT '',
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """


class ApplicationCRUD:
    COLUMNS = (
        "first_name",
        "last_name",
        "patronymic",
        "phone",
        "email",
        "business_info",
        "business_niche",
        "company_size",
        "business_size",
        "role",
        "task_volume",
        "need_volume",
        "deadline",
        "task_type",
        "product",
        "budget",
        "contact_method",
        "convenient_time",
        "comment",
    )

    @staticmethod
    def list_all(conn):
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM applications ORDER BY id DESC")
            return [serialize_row(row) for row in cursor.fetchall()]

    @staticmethod
    def get_by_id(conn, item_id: int):
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM applications WHERE id = %s", (item_id,))
            return serialize_row(cursor.fetchone())

    @staticmethod
    def create(conn, data: dict):
        values = [data.get(column, "") or "" for column in ApplicationCRUD.COLUMNS]
        placeholders = ", ".join(["%s"] * len(ApplicationCRUD.COLUMNS))
        columns = ", ".join(ApplicationCRUD.COLUMNS)
        with conn.cursor() as cursor:
            cursor.execute(
                f"""
                INSERT INTO applications ({columns})
                VALUES ({placeholders})
                RETURNING *
                """,
                values,
            )
            return serialize_row(cursor.fetchone())

    @staticmethod
    def update(conn, item_id: int, data: dict):
        assignments = []
        values = []
        for column in ApplicationCRUD.COLUMNS:
            if column in data and data[column] is not None:
                assignments.append(f"{column} = %s")
                values.append(data[column])
        if not assignments:
            return ApplicationCRUD.get_by_id(conn, item_id)
        values.append(item_id)
        with conn.cursor() as cursor:
            cursor.execute(
                f"""
                UPDATE applications
                SET {", ".join(assignments)}
                WHERE id = %s
                RETURNING *
                """,
                values,
            )
            return serialize_row(cursor.fetchone())

    @staticmethod
    def delete(conn, item_id: int) -> bool:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM applications WHERE id = %s", (item_id,))
            return cursor.rowcount > 0
