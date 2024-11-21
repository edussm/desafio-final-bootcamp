from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy import create_engine as _create_engine
from sqlalchemy.engine import URL, Engine
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import text

from app.utils.config import settings

EXTENSIONS = ["uuid-ossp"]


naming_convention = {
    "ix": "ix_ct_%(table_name)s_%(column_0_N_name)s",
    "uq": "uq_ct_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_ct_%(table_name)s_%(constraint_name)s",
    "fk": "fk_ct_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_ct_%(table_name)s",
}


class Base(DeclarativeBase, AsyncAttrs):
    metadata = MetaData(naming_convention=naming_convention)


def create_pg_url(
    drivername: str = "postgresql",
    username: str = "postgres",
    password: str = "postgres",
    host: str = "localhost",
    port: str = "5432",
    database: str = "postgres",
) -> URL:
    return URL.create(
        drivername=drivername,
        username=username,
        password=password,
        host=host,
        port=port,
        database=database,
    )


def create_pg_url_from_env(
    drivername: str | None = None,
    username: str | None = None,
    password: str | None = None,
    host: str | None = None,
    port: str | None = None,
    database: str | None = None,
) -> URL:
    return create_pg_url(
        drivername=drivername or settings.POSTGRES_DRIVERNAME,
        username=username or settings.POSTGRES_USER,
        password=password or settings.POSTGRES_PASSWORD,
        host=host or settings.POSTGRES_HOST,
        port=port or settings.POSTGRES_PORT,
        database=database or settings.POSTGRES_DB,
    )


def create_engine(url: URL, **kwargs) -> Engine:
    return _create_engine(url, **kwargs)


def create_async_engine(url: URL, **kwargs) -> AsyncEngine:
    pool_size_env = settings.POSTGRES_POOL_SIZE
    pool_size = int(kwargs.pop("pool_size", pool_size_env))
    return _create_async_engine(
        url,
        future=True,
        pool_size=pool_size,
        **kwargs,
    )


async def create_db_and_tables_async(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def create_db_and_tables_sync(engine: Engine):
    with engine.begin() as conn:
        Base.metadata.create_all(conn)


async def create_extensions(engine):
    async with engine.connect() as conn:
        for extension in EXTENSIONS:
            await conn.execute(text(f'CREATE EXTENSION IF NOT EXISTS "{extension}"'))


engine = create_async_engine(create_pg_url_from_env(), echo=False, pool_pre_ping=True)

local_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with local_session() as session:
        yield session
