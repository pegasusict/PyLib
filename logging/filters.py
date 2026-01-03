import logging
import os


class ProcessContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.pid = os.getpid()
        return True
