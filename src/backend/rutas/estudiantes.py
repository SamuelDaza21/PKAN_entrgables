from flask import Blueprint, jsonify, request

from controladores.estudiantes_controlador import (
    historial_asistencias,
    listar_estudiantes,
    reconocer_y_registrar_asistencia,
    registrar_estudiante,
)


estudiantes_bp = Blueprint("estudiantes", __name__, url_prefix="/api")


@estudiantes_bp.route("/estudiantes", methods=["POST"])
def crear_estudiante():
    try:
        data = request.get_json(force=True)
        estudiante = registrar_estudiante(data)
        return jsonify({"ok": True, "data": estudiante}), 201
    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400
    except Exception as exc:  # pragma: no cover
        return jsonify({"ok": False, "error": f"Error interno: {exc}"}), 500


@estudiantes_bp.route("/estudiantes", methods=["GET"])
def obtener_estudiantes():
    estudiantes = listar_estudiantes()
    return jsonify({"ok": True, "data": estudiantes})


@estudiantes_bp.route("/reconocimiento", methods=["POST"])
def reconocer_estudiante():
    try:
        data = request.get_json(force=True)
        resultado = reconocer_y_registrar_asistencia(data)
        if resultado is None:
            return jsonify({"ok": False, "error": "No hubo coincidencias."}), 404

        return jsonify({"ok": True, "data": resultado}), 200
    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400
    except Exception as exc:  # pragma: no cover
        return jsonify({"ok": False, "error": f"Error interno: {exc}"}), 500


@estudiantes_bp.route("/asistencias", methods=["GET"])
def obtener_asistencias():
    raw_limit = request.args.get("limit", "100")

    try:
        limit = int(raw_limit)
    except ValueError:
        return jsonify({"ok": False, "error": "El parametro limit debe ser numerico."}), 400

    data = historial_asistencias(limit=max(1, min(limit, 500)))
    return jsonify({"ok": True, "data": data})


