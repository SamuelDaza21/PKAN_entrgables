import argparse

from utils import compare_encodings, extract_face_encoding_from_file


def main():
	parser = argparse.ArgumentParser(
		description="Compara dos imagenes de rostro y muestra distancia facial."
	)
	parser.add_argument("referencia", help="Ruta de la imagen de referencia")
	parser.add_argument("candidato", help="Ruta de la imagen a comparar")
	parser.add_argument(
		"--tolerancia",
		type=float,
		default=0.48,
		help="Umbral maximo de distancia para coincidencia",
	)
	args = parser.parse_args()

	ref_encoding = extract_face_encoding_from_file(args.referencia)
	cand_encoding = extract_face_encoding_from_file(args.candidato)

	if ref_encoding is None:
		raise SystemExit("No se detecto rostro en la imagen de referencia.")
	if cand_encoding is None:
		raise SystemExit("No se detecto rostro en la imagen candidata.")

	is_match, distance = compare_encodings(ref_encoding, cand_encoding, args.tolerancia)
	print(f"Coincidencia: {'SI' if is_match else 'NO'}")
	print(f"Distancia: {distance:.4f}")


if __name__ == "__main__":
	main()

