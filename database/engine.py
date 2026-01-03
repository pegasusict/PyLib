from __future__ import annotations

import os
from typing import Mapping

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.engine import Engine
from sqlalchemy.pool import NullPool

from .types import DatabaseBackend


def _sqlite_url(db: str, async_: bool) -> str:
    return f"sqlite+aiosqlite:///{db}" if async_ else f"sqlite:///{db}"


def _mysql_url(cfg: Mapping, async_: bool) -> str:
    driver = "asyncmy" if async_ else "pymysql"
    return (
        f"mysql+{driver}://{cfg['username']}:{cfg['password']}"
        f"@{cfg.get('host','localhost')}:{cfg.get('port',3306)}"
        f"/{cfg['database']}"
    )


def create_sync_engine(cfg: Mapping) -> Engine:
    backend = DatabaseBackend(cfg["backend"])
    echo = bool(cfg.get("echo", False))

    if backend is DatabaseBackend.SQLITE:
        return create_engine(
            _sqlite_url(cfg["database"], async_=False),
            future=True,
            echo=echo,
            connect_args={"check_same_thread": False},
            poolclass=NullPool if os.name != "nt" else None,
        )

    if backend in (DatabaseBackend.MYSQL, DatabaseBackend.MARIADB):
        return create_engine(
            _mysql_url(cfg, async_=False),
            future=True,
            echo=echo,
            pool_size=int(cfg.get("pool_size", 10)),
            max_overflow=int(cfg.get("max_overflow", 20)),
            pool_pre_ping=True,
        )

    raise ValueError(f"Unsupported backend: {backend}")


def create_async_engine_(cfg: Mapping) -> AsyncEngine:
    backend = DatabaseBackend(cfg["backend"])
    echo = bool(cfg.get("echo", False))

    if backend is DatabaseBackend.SQLITE:
        return create_async_engine(
            _sqlite_url(cfg["database"], async_=True),
            future=True,
            echo=echo,
            poolclass=NullPool,
        )

    if backend in (DatabaseBackend.MYSQL, DatabaseBackend.MARIADB):
        return create_async_engine(
            _mysql_url(cfg, async_=True),
            future=True,
            echo=echo,
            pool_size=int(cfg.get("pool_size", 10)),
            max_overflow=int(cfg.get("max_overflow", 20)),
            pool_pre_ping=True,
        )

    raise ValueError(f"Unsupported backend: {backend}")
