from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


class _Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="POSTGRES_")
    engine: str = "+asyncpg"
    db: str
    password: str
    user: str
    host: str
    port: str

    @property
    def async_dsn(self):
        return f"postgresql{self.engine}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    @property
    def sync_dsn(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


settings = _Settings()  # type: ignore



engine = create_async_engine(settings.async_dsn)

sync_engine = create_engine(settings.sync_dsn)

session_maker = async_sessionmaker(engine)
