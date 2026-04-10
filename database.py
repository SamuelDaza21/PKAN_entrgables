import os
import sqlite3

RUTA_BD = os.path.join(os.path.dirname(__file__), 'todo.db')


def obtener_conexion(ruta_bd=None):
    """Devuelve una conexion a la base de datos SQLite."""
    ruta = ruta_bd if ruta_bd is not None else RUTA_BD
    conexion = sqlite3.connect(ruta)
    conexion.row_factory = sqlite3.Row
    return conexion


def inicializar_bd(ruta_bd=None):
    """Crea la tabla principal y migra el esquema anterior si existe."""
    conexion = obtener_conexion(ruta_bd)
    with conexion:
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS tareas (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo     TEXT    NOT NULL,
                completada INTEGER NOT NULL DEFAULT 0,
                creada_en  TEXT    NOT NULL DEFAULT (datetime('now'))
            )
        """)

        tabla_legacy = conexion.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'tasks'"
        ).fetchone()

        if tabla_legacy:
            conexion.execute("""
                INSERT OR IGNORE INTO tareas (id, titulo, completada, creada_en)
                SELECT id, title, completed, created_at
                FROM tasks
            """)
            conexion.execute("DROP TABLE tasks")
    conexion.close()


get_connection = obtener_conexion
init_db = inicializar_bd
