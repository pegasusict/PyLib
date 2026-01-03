import logging
import logging.handlers
import multiprocessing
from pathlib import Path
from typing import Iterable


def build_handlers(cfg: dict) -> Iterable[logging.Handler]:
    handlers: list[logging.Handler] = []

    if cfg.get("stdout", True):
        h = logging.StreamHandler()
        handlers.append(h)

    file_cfg = cfg.get("file")
    if file_cfg:
        path = Path(file_cfg["path"])
        path.parent.mkdir(parents=True, exist_ok=True)

        if file_cfg.get("rotate") == "time":
            h = logging.handlers.TimedRotatingFileHandler(
                path,
                when="midnight",
                backupCount=int(file_cfg.get("backup_count", 7)),
            )
        else:
            h = logging.handlers.RotatingFileHandler(
                path,
                maxBytes=int(file_cfg.get("max_bytes", 10_000_000)),
                backupCount=int(file_cfg.get("backup_count", 5)),
            )
        handlers.append(h)

    return handlers


def build_multiprocess_handler(
    queue: multiprocessing.Queue,
) -> logging.Handler:
    return logging.handlers.QueueHandler(queue)
