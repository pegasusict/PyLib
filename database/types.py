from enum import StrEnum


class DatabaseBackend(StrEnum):
    SQLITE = "sqlite"
    MYSQL = "mysql"
    MARIADB = "mariadb"
