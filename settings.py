from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    host: str
    port: str
    user: str
    passwd: str
    db_name: str
    cloudfront_prefix: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="backend_"
    )

    @property
    def _connection_str(self) -> str:
        return f"{self.user}:{self.passwd}@{self.host}:{self.port}/{self.db_name}"

    @property
    def sync_connection_str(self) -> str:
        return "postgresql+psycopg2://" + self._connection_str

    @property
    def async_connection_str(self) -> str:
        return "postgresql+asyncpg://" + self._connection_str


settings = AppSettings()
