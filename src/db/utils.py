import traceback

from alembic import command
from alembic.config import Config
from sqlalchemy import Connection

from .database_session_manager import sessionmanager


def run_upgrade(connection: Connection, cfg: Config):
    cfg.attributes["connection"] = connection
    command.upgrade(cfg, "head")


async def run_migrations():
    alembic_config = Config("alembic.ini")
    async with sessionmanager.connect() as conn:
        try:
            await conn.run_sync(run_upgrade, alembic_config)
        except Exception as e:
            print(type(e))
            print(traceback.format_exc())
