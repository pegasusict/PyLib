from pydantic import BaseModel

class LoggingConfig(BaseModel):
    level: str = "DEBUG"
    file: str = "log.log"


class GeneralConfig(BaseModel):
    ...


class DatabaseConfig(BaseModel):
    backend: str = "sqlite" | "mysql" | "mariadb",
    database: str = "app.db",
    host: str = "localhost",
    port: int = 3306,
    username: str = "user",
    password: str = "secret",
    pool_size: int = 10,
    max_overflow: int = 20,
    echo: bool = False,


class AppConfig(BaseModel):
    version: str
    general: GeneralConfig
    database: DatabaseConfig
    logging: LoggingConfig
