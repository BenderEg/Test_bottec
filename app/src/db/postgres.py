from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from core.config import settings


Base = declarative_base(metadata=MetaData(schema="content"))

dsn = f'''postgresql+asyncpg://{
    settings.postgres_user}:{settings.postgres_password}@{
        settings.host}:{settings.port}/{settings.postgres_db}'''
engine = create_async_engine(dsn, echo=settings.echo, future=True)
async_session = sessionmaker(engine, class_=AsyncSession,
                             expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session