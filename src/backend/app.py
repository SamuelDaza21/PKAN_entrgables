from pathlib import Path

from flask import Flask, send_from_directory

from config.db import init_db
from rutas.estudiantes import estudiantes_bp


def create_app(testing=False, initialize_db=True):
    frontend_root = Path(__file__).resolve().parents[1] / "frontend"
    plantilla_dir = frontend_root / "Plantilla"

    app = Flask(__name__)
    app.config["TESTING"] = testing

    if initialize_db:
        init_db()

    app.register_blueprint(estudiantes_bp)

    @app.get("/")
    def home():
        return send_from_directory(plantilla_dir, "index.html")

    @app.get("/estilo/<path:resource>")
    def estilos(resource):
        return send_from_directory(frontend_root / "estilo", resource)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)


