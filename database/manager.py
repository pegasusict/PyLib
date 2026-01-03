from __future__ import annotations

import os
import threading
from typing import Optional

from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import Session

from .engine import create_sync_engine, create_async_engine_
from .session import (
    create_sync_session_factory,
    create_async_session_factory,
)
from .exceptions import DatabaseNotInitialized


class DatabaseManager:
    _instance: Optional["DatabaseManager"] = None
    _lock = threading.Lock()

    def __new__(cls) -> "DatabaseManager":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def initialize(self, config: dict) -> None:
        with self._lock:
            self._config = config
            self._pid = os.getpid()

            self._engine = create_sync_engine(config)
            self._async_engine = create_async_engine_(config)

            self._session_factory = create_sync_session_factory(self._engine)
            self._async_session_factory = create_async_session_factory(self._async_engine)

            self._initialized = True

    def _check_fork(self) -> None:
        if os.getpid() != self._pid:
            self._engine.dispose()
            self._async_engine.sync_engine.dispose()

            self._engine = create_sync_engine(self._config)
            self._async_engine = create_async_engine_(self._config)

            self._session_factory = create_sync_session_factory(self._engine)
            self._async_session_factory = create_async_session_factory(self._async_engine)

            self._pid = os.getpid()

    @property
    def engine(self) -> Engine:
        if not self._initialized:
            raise DatabaseNotInitialized()
        self._check_fork()
        return self._engine

    @property
    def async_engine(self) -> AsyncEngine:
        if not self._initialized:
            raise DatabaseNotInitialized()
        self._check_fork()
        return self._async_engine

    def session(self) -> Session:
        self._check_fork()
        return self._session_factory()

    def async_session(self) -> AsyncSession:
        self._check_fork()
        return self._async_session_factory()

    def dispose(self) -> None:
        if self._initialized:
            self._engine.dispose()
            self._async_engine.sync_engine.dispose()
