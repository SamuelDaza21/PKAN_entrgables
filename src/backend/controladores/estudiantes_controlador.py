from datetime import datetime

from config.db import get_connection
from modelos.estudiante import Estudiante
from servicios.reconocimiento import (
    comparar_encoding_con_estudiantes,
    encoding_a_json,
    obtener_encoding_desde_base64,
)


def _validar_campos_estudiante(payload):
    required = ["nombre", "codigo", "programa", "fotoBase64"]
    missing = [field for field in required if not payload.get(field)]
    if missing:
        raise ValueError(f"Campos requeridos faltantes: {', '.join(missing)}")


def registrar_estudiante(payload):
    _validar_campos_estudiante(payload)

    encoding = obtener_encoding_desde_base64(payload["fotoBase64"])
    if encoding is None:
        raise ValueError("No se detecto un rostro valido en la imagen.")

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO estudiantes (nombre, codigo, programa, rostro_encoding)
            VALUES (?, ?, ?, ?)
            """,
            (
                payload["nombre"].strip(),
                payload["codigo"].strip(),
                payload["programa"].strip(),
                encoding_a_json(encoding),
            ),
        )
        connection.commit()

        estudiante_row = connection.execute(
            "SELECT id, nombre, codigo, programa FROM estudiantes WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()

    return Estudiante.from_row(estudiante_row).to_dict()


def listar_estudiantes():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, nombre, codigo, programa FROM estudiantes ORDER BY id DESC"
        ).fetchall()

    return [Estudiante.from_row(row).to_dict() for row in rows]


def reconocer_y_registrar_asistencia(payload):
    if not payload.get("fotoBase64"):
        raise ValueError("Se requiere fotoBase64 para el reconocimiento.")

    encoding = obtener_encoding_desde_base64(payload["fotoBase64"])
    if encoding is None:
        raise ValueError("No se detecto ningun rostro en la imagen.")

    with get_connection() as connection:
        estudiantes_rows = connection.execute(
            "SELECT id, nombre, codigo, programa, rostro_encoding FROM estudiantes"
        ).fetchall()

        match = comparar_encoding_con_estudiantes(encoding, estudiantes_rows)
        if match is None:
            return None

        fecha_hora = datetime.now().isoformat(timespec="seconds")
        cursor = connection.execute(
            """
            INSERT INTO asistencias (estudiante_id, fecha_hora)
            VALUES (?, ?)
            """,
            (match["id"], fecha_hora),
        )
        connection.commit()

    return {
        "asistencia_id": cursor.lastrowid,
        "fecha_hora": fecha_hora,
        "estudiante": {
            "id": match["id"],
            "nombre": match["nombre"],
            "codigo": match["codigo"],
            "programa": match["programa"],
        },
        "distancia": match["distancia"],
    }


def historial_asistencias(limit=100):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT a.id, a.fecha_hora, e.nombre, e.codigo, e.programa
            FROM asistencias a
            JOIN estudiantes e ON e.id = a.estudiante_id
            ORDER BY a.fecha_hora DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [
        {
            "id": row["id"],
            "fecha_hora": row["fecha_hora"],
            "nombre": row["nombre"],
            "codigo": row["codigo"],
            "programa": row["programa"],
        }
        for row in rows
    ]


