from pathlib import Path
import sqlite3
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
BACKEND_DIR = ROOT_DIR / "src" / "backend"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app import create_app  # noqa: E402
import config.db as db_config  # noqa: E402


def _crear_db_temporal(tmp_path):
    db_file = tmp_path / "test_sistema_huella.db"
    db_config.DB_PATH = db_file
    db_config.SCHEMA_PATH = ROOT_DIR / "src" / "BD" / "schema.sql"
    db_config.init_db()
    return db_file


def test_get_estudiantes_vacio(tmp_path):
    _crear_db_temporal(tmp_path)
    app = create_app(testing=True, initialize_db=False)

    client = app.test_client()
    response = client.get("/api/estudiantes")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["ok"] is True
    assert isinstance(payload["data"], list)


def test_get_asistencias_vacio(tmp_path):
    _crear_db_temporal(tmp_path)
    app = create_app(testing=True, initialize_db=False)

    client = app.test_client()
    response = client.get("/api/asistencias")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["ok"] is True
    assert payload["data"] == []
