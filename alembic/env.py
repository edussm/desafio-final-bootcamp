from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from alembic import context
from app.model.base import PersistableModel

# Importar o Base
from app.utils.database import create_pg_url_from_env

# Configuração do logger
config = context.config
fileConfig(config.config_file_name)

# Definir o target_metadata
target_metadata = PersistableModel.metadata

# Definir URL de conexão
DATABASE_URL = create_pg_url_from_env()


# Criar o motor assíncrono
def get_engine() -> AsyncEngine:
    return create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )


async def run_migrations_online():
    connectable = get_engine()

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations():
    if context.is_offline_mode():
        context.configure(url=DATABASE_URL, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
    else:
        import asyncio

        asyncio.run(run_migrations_online())


run_migrations()
