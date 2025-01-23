from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_user: str
    postgres_database: str
    postgres_password: str
    postgres_host: str
    echo_database: bool = False

    model_config = SettingsConfigDict(env_file=".env")


def get_settings() -> Settings:
    return Settings()  # pyright: ignore [reportCallIssue] Can be safely ignored as the arguments are automatically calculated by Pydantic
