"""Pruebas de integración para flujos completos de la aplicación."""
import os
import sys
import json
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import app as flask_app
from database import inicializar_bd
from models import Tarea


class IntegracionTestCase(unittest.TestCase):
    """Flujos completos que combinan varias operaciones."""

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix='.db')
        inicializar_bd(self.db_path)
        flask_app.app.config['TESTING'] = True

        ruta_bd = self.db_path

        class TareaParcheada(Tarea):
            @staticmethod
            def crear(titulo, ruta_bd_interna=None):
                return Tarea.crear(titulo, ruta_bd)

            @staticmethod
            def obtener_todas(ruta_bd_interna=None):
                return Tarea.obtener_todas(ruta_bd)

            @staticmethod
            def obtener_por_id(tarea_id, ruta_bd_interna=None):
                return Tarea.obtener_por_id(tarea_id, ruta_bd)

            @staticmethod
            def actualizar(tarea_id, titulo, ruta_bd_interna=None):
                return Tarea.actualizar(tarea_id, titulo, ruta_bd)

            @staticmethod
            def alternar_completada(tarea_id, ruta_bd_interna=None):
                return Tarea.alternar_completada(tarea_id, ruta_bd)

            @staticmethod
            def eliminar(tarea_id, ruta_bd_interna=None):
                return Tarea.eliminar(tarea_id, ruta_bd)

        self._tarea_original = flask_app.Tarea
        flask_app.Tarea = TareaParcheada
        self.client = flask_app.app.test_client()

    def tearDown(self):
        flask_app.Tarea = self._tarea_original
        os.close(self.db_fd)
        os.unlink(self.db_path)

    # ── Helper ────────────────────────────────────────────────────────────

    def _api_crear(self, titulo):
        respuesta = self.client.post(
            '/api/tareas',
            data=json.dumps({'titulo': titulo}),
            content_type='application/json'
        )
        return json.loads(respuesta.data)

    # ── Flujo completo CRUD ───────────────────────────────────────────────

    def test_ciclo_completo_crud(self):
        """Crear → Editar → Completar → Eliminar."""
        # 1. Crear
        tarea = Tarea.crear("Integración: comprar pan", self.db_path)
        self.assertEqual(tarea.titulo, "Integración: comprar pan")

        # 2. Editar
        Tarea.actualizar(tarea.id, "Integración: comprar pan integral", self.db_path)
        actualizada = Tarea.obtener_por_id(tarea.id, self.db_path)
        self.assertEqual(actualizada.titulo, "Integración: comprar pan integral")

        # 3. Completar
        Tarea.alternar_completada(tarea.id, self.db_path)
        completada = Tarea.obtener_por_id(tarea.id, self.db_path)
        self.assertTrue(completada.completada)

        # 4. Eliminar
        Tarea.eliminar(tarea.id, self.db_path)
        self.assertIsNone(Tarea.obtener_por_id(tarea.id, self.db_path))

    def test_varias_tareas_persisten(self):
        """Varias tareas conviven correctamente en la BD."""
        titulos = ["Tarea A", "Tarea B", "Tarea C"]
        for titulo in titulos:
            Tarea.crear(titulo, self.db_path)
        todas_las_tareas = Tarea.obtener_todas(self.db_path)
        self.assertEqual(len(todas_las_tareas), 3)
        titulos_recuperados = {tarea.titulo for tarea in todas_las_tareas}
        self.assertEqual(titulos_recuperados, set(titulos))

    def test_tareas_completadas_persisten_tras_listado(self):
        """El estado completado persiste entre llamadas."""
        tarea = Tarea.crear("Persistir estado", self.db_path)
        Tarea.alternar_completada(tarea.id, self.db_path)
        todas_las_tareas = Tarea.obtener_todas(self.db_path)
        encontrada = next(x for x in todas_las_tareas if x.id == tarea.id)
        self.assertTrue(encontrada.completada)

    def test_eliminar_solo_quita_tarea_objetivo(self):
        """Eliminar una tarea no afecta a las demás."""
        tarea_1 = Tarea.crear("Tarea 1", self.db_path)
        tarea_2 = Tarea.crear("Tarea 2", self.db_path)
        Tarea.eliminar(tarea_1.id, self.db_path)
        restantes = Tarea.obtener_todas(self.db_path)
        ids = [tarea.id for tarea in restantes]
        self.assertNotIn(tarea_1.id, ids)
        self.assertIn(tarea_2.id, ids)

    def test_crear_por_api_y_verificar_en_listado(self):
        """Crear vía API y verificar en el listado."""
        Tarea.crear("Tarea API", self.db_path)
        todas_las_tareas = Tarea.obtener_todas(self.db_path)
        titulos = [tarea.titulo for tarea in todas_las_tareas]
        self.assertIn("Tarea API", titulos)

    def test_inicio_html_devuelve_200(self):
        """La página principal responde 200."""
        respuesta = self.client.get('/')
        self.assertEqual(respuesta.status_code, 200)

    def test_inicio_html_contiene_titulo(self):
        """La página principal contiene el título de la app."""
        respuesta = self.client.get('/')
        self.assertIn('Lista de Tareas'.encode('utf-8'), respuesta.data)


if __name__ == '__main__':
    unittest.main()
