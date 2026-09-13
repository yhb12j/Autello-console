from core.database import serialize_row


class Admin:
    """
    CREATE TABLE IF NOT EXISTS admins (
        id SERIAL PRIMARY KEY,
        login VARCHAR(80) NOT NULL UNIQUE,
        email VARCHAR(180),
        password_hash VARCHAR(255) NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """

    CREATE_SQL = """
    CREATE TABLE IF NOT EXISTS admins (
        id SERIAL PRIMARY KEY,
        login VARCHAR(80) NOT NULL UNIQUE,
        email VARCHAR(180),
        password_hash VARCHAR(255) NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """


class AdminCRUD:
    @staticmethod
    def count(conn) -> int:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS total FROM admins")
            row = cursor.fetchone()
            return int(row["total"] if row else 0)

    @staticmethod
    def get_by_login(conn, login: str):
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM admins WHERE login = %s", (login,))
            return serialize_row(cursor.fetchone())

    @staticmethod
    def create(conn, data: dict):
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO admins (login, email, password_hash)
                VALUES (%s, %s, %s)
                RETURNING id, login, email, created_at
                """,
                (data["login"], data.get("email"), data["password_hash"]),
            )
            return serialize_row(cursor.fetchone())
