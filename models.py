from database import obtener_conexion


class Tarea:
    """Representa una tarea de la lista."""

    def __init__(self, tarea_id, titulo, completada, creada_en):
        self.id = tarea_id
        self.titulo = titulo
        self.completada = bool(completada)
        self.creada_en = creada_en

    @staticmethod
    def _desde_fila(fila):
        if not fila:
            return None
        datos = dict(fila)
        datos['tarea_id'] = datos.pop('id')
        return Tarea(**datos)

    @staticmethod
    def crear(titulo, ruta_bd=None):
        """Inserta una tarea nueva y la devuelve."""
        conexion = obtener_conexion(ruta_bd)
        with conexion:
            cursor = conexion.execute(
                "INSERT INTO tareas (titulo) VALUES (?)", (titulo,)
            )
            tarea_id = cursor.lastrowid
        fila = conexion.execute(
            "SELECT * FROM tareas WHERE id = ?", (tarea_id,)
        ).fetchone()
        conexion.close()
        return Tarea._desde_fila(fila)

    @staticmethod
    def obtener_todas(ruta_bd=None):
        """Devuelve todas las tareas ordenadas por fecha de creacion."""
        conexion = obtener_conexion(ruta_bd)
        filas = conexion.execute(
            "SELECT * FROM tareas ORDER BY creada_en DESC"
        ).fetchall()
        conexion.close()
        return [Tarea._desde_fila(fila) for fila in filas]

    @staticmethod
    def obtener_por_id(tarea_id, ruta_bd=None):
        """Devuelve una tarea por identificador o None."""
        conexion = obtener_conexion(ruta_bd)
        fila = conexion.execute(
            "SELECT * FROM tareas WHERE id = ?", (tarea_id,)
        ).fetchone()
        conexion.close()
        return Tarea._desde_fila(fila)

    @staticmethod
    def actualizar(tarea_id, titulo, ruta_bd=None):
        """Actualiza el titulo de una tarea."""
        conexion = obtener_conexion(ruta_bd)
        with conexion:
            cursor = conexion.execute(
                "UPDATE tareas SET titulo = ? WHERE id = ?", (titulo, tarea_id)
            )
        conexion.close()
        return cursor.rowcount > 0

    @staticmethod
    def alternar_completada(tarea_id, ruta_bd=None):
        """Alterna el estado completado de una tarea."""
        conexion = obtener_conexion(ruta_bd)
        with conexion:
            cursor = conexion.execute(
                "UPDATE tareas SET completada = NOT completada WHERE id = ?",
                (tarea_id,)
            )
        conexion.close()
        return cursor.rowcount > 0

    @staticmethod
    def eliminar(tarea_id, ruta_bd=None):
        """Elimina una tarea."""
        conexion = obtener_conexion(ruta_bd)
        with conexion:
            cursor = conexion.execute(
                "DELETE FROM tareas WHERE id = ?", (tarea_id,)
            )
        conexion.close()
        return cursor.rowcount > 0

    @property
    def title(self):
        return self.titulo

    @property
    def completed(self):
        return self.completada

    @property
    def created_at(self):
        return self.creada_en

    def a_diccionario(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'completada': self.completada,
            'creada_en': self.creada_en,
        }

    @staticmethod
    def create(title, db_path=None):
        return Tarea.crear(title, db_path)

    @staticmethod
    def get_all(db_path=None):
        return Tarea.obtener_todas(db_path)

    @staticmethod
    def get_by_id(task_id, db_path=None):
        return Tarea.obtener_por_id(task_id, db_path)

    @staticmethod
    def update(task_id, title, db_path=None):
        return Tarea.actualizar(task_id, title, db_path)

    @staticmethod
    def toggle_completed(task_id, db_path=None):
        return Tarea.alternar_completada(task_id, db_path)

    @staticmethod
    def delete(task_id, db_path=None):
        return Tarea.eliminar(task_id, db_path)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.titulo,
            'completed': self.completada,
            'created_at': self.creada_en,
        }


Task = Tarea
