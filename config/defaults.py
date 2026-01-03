CONFIG_VERSION = "1.0"

DEFAULT_CONFIG = {
    "version": "1.0",
    "general": {},
    "logging": {
        "level": "INFO",
        "format": "json" | "text",
        "stdout": True,
        "file": {
            "path": "/var/log/app.log",
            "rotate": "size" | "time",
            "max_bytes": 10_000_000,
            "backup_count": 5,
        },
        "multiprocess": {
            "enabled": True,
            "queue_size": 10_000,
        },


    },
    "paths": {},
    "extensions": {},
    "database" : {
        "backend": "sqlite" | "mysql" | "mariadb",
        "database": "app.db",
        "host": "localhost",
        "port": 3306,
        "username": "user",
        "password": "secret",
        "pool_size": 10,
        "max_overflow": 20,
        "echo": False,
    }

}
