from contextlib import contextmanager
from pathlib import Path
import sqlite3
from typing import Iterator

from app.config import get_settings


def _schema_path() -> Path:
    return Path(__file__).with_name("schema.sql")


def init_db() -> None:
    settings = get_settings()
    settings.database_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(settings.database_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(_schema_path().read_text(encoding="utf-8"))
        connection.commit()


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    settings = get_settings()
    settings.database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(settings.database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()
