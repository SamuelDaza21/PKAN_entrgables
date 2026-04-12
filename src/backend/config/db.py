import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_PATH = PROJECT_ROOT / "src" / "BD" / "sistema_huella.db"
SCHEMA_PATH = PROJECT_ROOT / "src" / "BD" / "schema.sql"


def get_connection():
    """Create a SQLite connection with rows as dict-like objects."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Initialize database schema if it does not exist."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")

    with get_connection() as connection:
        connection.executescript(schema_sql)
        connection.commit()


