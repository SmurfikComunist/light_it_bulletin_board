from pydantic import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str
    HOSTNAME: str
    SERVER_PORT: int
    DEBUG: bool


settings: Settings = Settings(_env_file=".env")
