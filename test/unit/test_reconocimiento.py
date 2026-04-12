import numpy as np

from src.backend.servicios.reconocimiento import comparar_encoding_con_estudiantes, encoding_a_json


def test_encoding_a_json_y_reconstruccion_compatible():
    vector = np.array([0.1, 0.2, 0.3], dtype=np.float64)
    data = encoding_a_json(vector)

    assert "[0.1, 0.2, 0.3]" in data


def test_comparar_encoding_encuentra_mejor_match():
    unknown = np.array([0.1, 0.2, 0.3], dtype=np.float64)

    rows = [
        {
            "id": 1,
            "nombre": "A",
            "codigo": "U1",
            "programa": "Ing",
            "rostro_encoding": "[0.9, 0.8, 0.7]",
        },
        {
            "id": 2,
            "nombre": "B",
            "codigo": "U2",
            "programa": "Ing",
            "rostro_encoding": "[0.1, 0.2, 0.31]",
        },
    ]

    result = comparar_encoding_con_estudiantes(unknown, rows)

    assert result is not None
    assert result["id"] == 2
