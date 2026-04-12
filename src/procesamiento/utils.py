import base64
from pathlib import Path

import numpy as np

try:
	import cv2
except ImportError:  # pragma: no cover
	cv2 = None

try:
	import face_recognition
except ImportError:  # pragma: no cover
	face_recognition = None


def _check_dependencies():
	if cv2 is None or face_recognition is None:
		raise RuntimeError(
			"Se requieren las librerias opencv-python y face-recognition."
		)


def load_image_as_rgb(image_path):
	_check_dependencies()

	if not Path(image_path).exists():
		raise FileNotFoundError(f"No existe la imagen: {image_path}")

	bgr = cv2.imread(str(image_path))
	if bgr is None:
		raise ValueError(f"No se pudo leer la imagen: {image_path}")

	return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)


def extract_face_encoding_from_file(image_path):
	rgb = load_image_as_rgb(image_path)
	locations = face_recognition.face_locations(rgb)
	if not locations:
		return None

	encodings = face_recognition.face_encodings(rgb, locations)
	return encodings[0] if encodings else None


def extract_face_encoding_from_base64(image_base64):
	_check_dependencies()

	clean_data = image_base64.split(",", 1)[1] if "," in image_base64 else image_base64
	image_bytes = base64.b64decode(clean_data)
	np_array = np.frombuffer(image_bytes, dtype=np.uint8)
	bgr = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

	if bgr is None:
		return None

	rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
	locations = face_recognition.face_locations(rgb)
	if not locations:
		return None

	encodings = face_recognition.face_encodings(rgb, locations)
	return encodings[0] if encodings else None


def compare_encodings(reference_encoding, candidate_encoding, tolerance=0.48):
	distance = float(np.linalg.norm(reference_encoding - candidate_encoding))
	return distance <= tolerance, distance

