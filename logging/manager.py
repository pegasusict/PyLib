from __future__ import annotations

import logging
import logging.handlers
import multiprocessing
import os
import threading
from typing import Optional

from .types import LogFormat
from .formatters import TextFormatter, JsonFormatter
from .filters import ProcessContextFilter
from .handlers import build_handlers, build_multiprocess_handler
from .exceptions import LoggingError


class LoggingManager:
    _instance: Optional["LoggingManager"] = None
    _lock = threading.Lock()

    def __new__(cls) -> "LoggingManager":
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

            self._queue = None
            self._listener = None

            root = logging.getLogger()
            root.handlers.clear()
            root.setLevel(config.get("level", "INFO"))

            formatter = (
                JsonFormatter()
                if LogFormat(config.get("format", "text")) is LogFormat.JSON
                else TextFormatter()
            )

            for h in build_handlers(config):
                h.setFormatter(formatter)
                h.addFilter(ProcessContextFilter())
                root.addHandler(h)

            mp_cfg = config.get("multiprocess", {})
            if mp_cfg.get("enabled"):
                self._queue = multiprocessing.Queue(
                    maxsize=int(mp_cfg.get("queue_size", 10_000))
                )

                mp_handler = build_multiprocess_handler(self._queue)
                root.handlers.clear()
                root.addHandler(mp_handler)

                self._listener = logging.handlers.QueueListener(
                    self._queue,
                    *build_handlers(config),
                    respect_handler_level=True,
                )
                self._listener.start()

            self._initialized = True

    def _check_fork(self) -> None:
        if os.getpid() != self._pid:
            # Reinitialize logging after fork
            self.initialize(self._config)

    def get_logger(self, name: str) -> logging.Logger:
        if not self._initialized:
            raise LoggingError("LoggingManager not initialized")

        self._check_fork()
        return logging.getLogger(name)
