from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file='../../.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    token: str
    red_host: str
    red_port: int
    red_db: int
    postgres_password: str
    postgres_user: str
    postgres_db: str
    host: str
    port: int
    echo: bool = True
    log_level: str = 'DEBUG'
    categories: int = 10
    cache_exp: int = 3600
    server_link: str

settings = Settings()