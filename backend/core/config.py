import os


class Settings:
    postgres_host: str = os.getenv("POSTGRES_HOST", "db")
    postgres_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    postgres_db: str = os.getenv("POSTGRES_DB", "autello_orders")
    postgres_user: str = os.getenv("POSTGRES_USER", "autello")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "change_me")


settings = Settings()
