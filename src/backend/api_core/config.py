from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENV: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: str
    model_config = SettingsConfigDict(
        env_file="None",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
