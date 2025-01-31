from os import environ

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV = environ.get("ENV", "prod")
ENV_FILE = {"dev": ".env.dev", "prod": ".env", "test": ".env.test"}

try:
    env_file = ENV_FILE[ENV]
except KeyError:
    raise ValueError("ENV must be either 'dev', 'prod' or 'test'")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file, extra="ignore")

    # postgres
    POSTGRES_DRIVERNAME: str = Field("postgresql+asyncpg")
    POSTGRES_USER: str = Field("postgres")
    POSTGRES_PASSWORD: str = Field("postgres")
    POSTGRES_DB: str = Field("postgres")
    POSTGRES_HOST: str = Field("localhost")
    POSTGRES_PORT: int | str = Field("5432")
    POSTGRES_ECHO: bool = Field(False)
    POSTGRES_POOL_SIZE: int = Field(3)

    # logging
    LOG_LEVEL: str = Field("INFO")


settings = Settings()
