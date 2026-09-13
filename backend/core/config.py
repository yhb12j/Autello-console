import os


class Settings:
    postgres_host: str = os.getenv("POSTGRES_HOST", "db")
    postgres_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    postgres_db: str = os.getenv("POSTGRES_DB", "autello_orders")
    postgres_user: str = os.getenv("POSTGRES_USER", "autello")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "change_me")
    secret_key: str = os.getenv("SECRET_KEY", "change_me_secret")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "720"))


settings = Settings()
