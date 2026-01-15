from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Incident Intelligence Platform"
    PORT: int = 8000

    # Logging
    LOG_LEVEL: str = "INFO"

    # Environment
    ENV: str = "dev"

    # Security
    JWT_SECRET: str

    # Database
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
