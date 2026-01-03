class DatabaseError(RuntimeError):
    pass


class DatabaseNotInitialized(DatabaseError):
    pass
