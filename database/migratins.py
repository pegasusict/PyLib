# from sqlmodel import SQLModel
from alembic import command
from alembic.config import Config
from pathlib import Path


def run_migrations(
    alembic_ini: Path,
    engine,
) -> None:
    cfg = Config(str(alembic_ini))
    cfg.attributes["connection"] = engine.connect()

    try:
        command.upgrade(cfg, "head")
    finally:
        cfg.attributes["connection"].close()
