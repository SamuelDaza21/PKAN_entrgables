import base64
import json

import numpy as np

try:
    import cv2
except ImportError:  # pragma: no cover
    cv2 = None

try:
    import face_recognition
except ImportError:  # pragma: no cover
    face_recognition = None


MATCH_TOLERANCE = 0.48


def _check_dependencies():
    if cv2 is None or face_recognition is None:
        raise RuntimeError(
            "OpenCV y face_recognition deben estar instalados para procesar rostros."
        )


def obtener_encoding_desde_base64(image_base64):
    """Decode a base64 image and return its first face encoding."""
    _check_dependencies()

    if not image_base64:
        return None

    raw_data = image_base64.split(",", 1)[1] if "," in image_base64 else image_base64
    image_bytes = base64.b64decode(raw_data)
    np_array = np.frombuffer(image_bytes, np.uint8)

    image_bgr = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    if image_bgr is None:
        return None

    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(image_rgb)
    if not face_locations:
        return None

    encodings = face_recognition.face_encodings(image_rgb, face_locations)
    return encodings[0] if encodings else None


def encoding_a_json(face_encoding):
    return json.dumps(face_encoding.tolist())


def json_a_encoding(serialized_encoding):
    return np.array(json.loads(serialized_encoding), dtype=np.float64)


def comparar_encoding_con_estudiantes(unknown_encoding, estudiantes_rows):
    """Find the best match against stored encodings."""
    if unknown_encoding is None:
        return None

    mejor_match = None
    menor_distancia = 10.0

    for row in estudiantes_rows:
        if not row["rostro_encoding"]:
            continue

        known_encoding = json_a_encoding(row["rostro_encoding"])
        distancia = float(np.linalg.norm(unknown_encoding - known_encoding))

        if distancia < menor_distancia:
            menor_distancia = distancia
            mejor_match = row

    if mejor_match is None:
        return None

    if menor_distancia > MATCH_TOLERANCE:
        return None

    return {
        "id": mejor_match["id"],
        "nombre": mejor_match["nombre"],
        "codigo": mejor_match["codigo"],
        "programa": mejor_match["programa"],
        "distancia": round(menor_distancia, 4),
    }


