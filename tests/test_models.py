"""
Pruebas unitarias para el modelo Task.
Se utiliza una base de datos en memoria para aislar cada test.
"""
import os
import sys
import tempfile
import unittest

# Asegurar que el directorio raíz del proyecto esté en el path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from database import inicializar_bd
from models import Tarea


class TareaModeloTestCase(unittest.TestCase):
    """HU-1 a HU-5: pruebas unitarias sobre el modelo Tarea."""

    def setUp(self):
        """Crear una BD temporal para cada test."""
        self.db_fd, self.db_path = tempfile.mkstemp(suffix='.db')
        inicializar_bd(self.db_path)

    def tearDown(self):
        """Eliminar la BD temporal."""
        os.close(self.db_fd)
        os.unlink(self.db_path)

    # ── HU-1: Crear tarea ──────────────────────────────────────────────────

    def test_crear_tarea_devuelve_objeto_tarea(self):
        """Se puede crear una tarea y obtener un objeto Tarea."""
        tarea = Tarea.crear("Comprar leche", self.db_path)
        self.assertIsInstance(tarea, Tarea)

    def test_crear_tarea_tiene_titulo_correcto(self):
        """El título de la tarea creada es correcto."""
        tarea = Tarea.crear("Estudiar Flask", self.db_path)
        self.assertEqual(tarea.titulo, "Estudiar Flask")

    def test_crear_tarea_no_esta_completada_por_defecto(self):
        """Una tarea recién creada no está completada."""
        tarea = Tarea.crear("Leer libro", self.db_path)
        self.assertFalse(tarea.completada)

    def test_crear_tarea_asigna_id(self):
        """La tarea creada recibe un ID mayor que cero."""
        tarea = Tarea.crear("Hacer ejercicio", self.db_path)
        self.assertGreater(tarea.id, 0)

    # ── HU-2: Ver lista de tareas ─────────────────────────────────────────

    def test_obtener_todas_devuelve_lista_vacia_si_no_hay_tareas(self):
        """obtener_todas devuelve lista vacía si no hay tareas."""
        tareas = Tarea.obtener_todas(self.db_path)
        self.assertEqual(tareas, [])

    def test_obtener_todas_devuelve_todas_las_tareas_creadas(self):
        """obtener_todas devuelve todas las tareas creadas."""
        Tarea.crear("Tarea 1", self.db_path)
        Tarea.crear("Tarea 2", self.db_path)
        tareas = Tarea.obtener_todas(self.db_path)
        self.assertEqual(len(tareas), 2)

    def test_obtener_por_id_devuelve_tarea_correcta(self):
        """obtener_por_id devuelve la tarea con el ID indicado."""
        creada = Tarea.crear("Ir al gimnasio", self.db_path)
        obtenida = Tarea.obtener_por_id(creada.id, self.db_path)
        self.assertEqual(obtenida.titulo, "Ir al gimnasio")

    def test_obtener_por_id_devuelve_none_si_no_existe(self):
        """obtener_por_id devuelve None si la tarea no existe."""
        resultado = Tarea.obtener_por_id(9999, self.db_path)
        self.assertIsNone(resultado)

    # ── HU-3: Marcar tarea como completada ───────────────────────────────

    def test_alternar_completada_marca_tarea_como_lista(self):
        """alternar_completada pone completada=True en una tarea pendiente."""
        tarea = Tarea.crear("Revisar correos", self.db_path)
        Tarea.alternar_completada(tarea.id, self.db_path)
        actualizada = Tarea.obtener_por_id(tarea.id, self.db_path)
        self.assertTrue(actualizada.completada)

    def test_alternar_completada_regresa_a_pendiente(self):
        """Llamar alternar dos veces regresa a completada=False."""
        tarea = Tarea.crear("Llamar al banco", self.db_path)
        Tarea.alternar_completada(tarea.id, self.db_path)
        Tarea.alternar_completada(tarea.id, self.db_path)
        actualizada = Tarea.obtener_por_id(tarea.id, self.db_path)
        self.assertFalse(actualizada.completada)

    def test_alternar_completada_devuelve_true_si_existe(self):
        """alternar_completada retorna True cuando la tarea existe."""
        tarea = Tarea.crear("Pagar servicios", self.db_path)
        resultado = Tarea.alternar_completada(tarea.id, self.db_path)
        self.assertTrue(resultado)

    def test_alternar_completada_devuelve_false_si_no_existe(self):
        """alternar_completada retorna False cuando la tarea no existe."""
        resultado = Tarea.alternar_completada(9999, self.db_path)
        self.assertFalse(resultado)

    # ── HU-4: Editar tarea ───────────────────────────────────────────────

    def test_actualizar_cambia_titulo(self):
        """update cambia el título de la tarea."""
        tarea = Tarea.crear("Titulo original", self.db_path)
        Tarea.actualizar(tarea.id, "Titulo actualizado", self.db_path)
        actualizada = Tarea.obtener_por_id(tarea.id, self.db_path)
        self.assertEqual(actualizada.titulo, "Titulo actualizado")

    def test_actualizar_devuelve_true_si_existe(self):
        """update retorna True cuando la tarea existe."""
        tarea = Tarea.crear("Tarea editable", self.db_path)
        resultado = Tarea.actualizar(tarea.id, "Nuevo título", self.db_path)
        self.assertTrue(resultado)

    def test_actualizar_devuelve_false_si_no_existe(self):
        """update retorna False cuando la tarea no existe."""
        resultado = Tarea.actualizar(9999, "Nada", self.db_path)
        self.assertFalse(resultado)

    # ── HU-5: Eliminar tarea ─────────────────────────────────────────────

    def test_eliminar_quita_tarea(self):
        """delete elimina la tarea de la BD."""
        tarea = Tarea.crear("Tarea a eliminar", self.db_path)
        Tarea.eliminar(tarea.id, self.db_path)
        self.assertIsNone(Tarea.obtener_por_id(tarea.id, self.db_path))

    def test_eliminar_devuelve_true_si_existe(self):
        """delete retorna True cuando la tarea existe."""
        tarea = Tarea.crear("Borrar esto", self.db_path)
        resultado = Tarea.eliminar(tarea.id, self.db_path)
        self.assertTrue(resultado)

    def test_eliminar_devuelve_false_si_no_existe(self):
        """delete retorna False cuando la tarea no existe."""
        resultado = Tarea.eliminar(9999, self.db_path)
        self.assertFalse(resultado)

    # ── to_dict ──────────────────────────────────────────────────────────

    def test_a_diccionario_contiene_claves_requeridas(self):
        """a_diccionario incluye todas las claves necesarias."""
        tarea = Tarea.crear("Revisar PR", self.db_path)
        datos = tarea.a_diccionario()
        for clave in ('id', 'titulo', 'completada', 'creada_en'):
            self.assertIn(clave, datos)


if __name__ == '__main__':
    unittest.main()
