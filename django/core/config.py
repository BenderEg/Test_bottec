from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env',
                                      env_file_encoding='utf-8',
                                      extra='ignore')
    postgres_password: str
    postgres_user: str
    postgres_db: str
    host: str
    port: int
    red_host: str
    red_port: int
    red_db: int = 0
    securitykey: str
    debug: bool
    allowed_hosts: str
    log_level: str = 'DEBUG'
    server_link: str

    @property
    def allowed_hosts_list(self):
        return self.allowed_hosts.split(',')

settings = Settings()