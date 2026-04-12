from dataclasses import dataclass


@dataclass
class Estudiante:
    id: int
    nombre: str
    codigo: str
    programa: str

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            nombre=row["nombre"],
            codigo=row["codigo"],
            programa=row["programa"],
        )

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "codigo": self.codigo,
            "programa": self.programa,
        }


