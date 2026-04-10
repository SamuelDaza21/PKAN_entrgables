"""Pruebas de la API JSON de Flask."""
import os
import sys
import json
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import app as flask_app
from database import inicializar_bd


class RutasTestCase(unittest.TestCase):
    """Pruebas sobre los endpoints /api/tareas."""

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix='.db')
        inicializar_bd(self.db_path)

        flask_app.app.config['TESTING'] = True
        self.client = flask_app.app.test_client()

        import models as m
        ruta_bd = self.db_path

        self._tarea_original = flask_app.Tarea

        class TareaParcheada(m.Tarea):
            @staticmethod
            def crear(titulo, ruta_bd_interna=None):
                return m.Tarea.crear(titulo, ruta_bd)

            @staticmethod
            def obtener_todas(ruta_bd_interna=None):
                return m.Tarea.obtener_todas(ruta_bd)

            @staticmethod
            def obtener_por_id(tarea_id, ruta_bd_interna=None):
                return m.Tarea.obtener_por_id(tarea_id, ruta_bd)

            @staticmethod
            def actualizar(tarea_id, titulo, ruta_bd_interna=None):
                return m.Tarea.actualizar(tarea_id, titulo, ruta_bd)

            @staticmethod
            def alternar_completada(tarea_id, ruta_bd_interna=None):
                return m.Tarea.alternar_completada(tarea_id, ruta_bd)

            @staticmethod
            def eliminar(tarea_id, ruta_bd_interna=None):
                return m.Tarea.eliminar(tarea_id, ruta_bd)

        flask_app.Tarea = TareaParcheada

    def tearDown(self):
        flask_app.Tarea = self._tarea_original
        os.close(self.db_fd)
        os.unlink(self.db_path)

    # ── GET /api/tasks ────────────────────────────────────────────────────

    def test_listar_tareas_devuelve_200(self):
        respuesta = self.client.get('/api/tareas')
        self.assertEqual(respuesta.status_code, 200)

    def test_listar_tareas_devuelve_lista_vacia(self):
        respuesta = self.client.get('/api/tareas')
        datos = json.loads(respuesta.data)
        self.assertEqual(datos, [])

    # ── POST /api/tasks ───────────────────────────────────────────────────

    def test_crear_tarea_devuelve_201(self):
        respuesta = self.client.post(
            '/api/tareas',
            data=json.dumps({'titulo': 'Nueva tarea'}),
            content_type='application/json'
        )
        self.assertEqual(respuesta.status_code, 201)

    def test_crear_tarea_devuelve_datos(self):
        respuesta = self.client.post(
            '/api/tareas',
            data=json.dumps({'titulo': 'Tarea API'}),
            content_type='application/json'
        )
        datos = json.loads(respuesta.data)
        self.assertEqual(datos['titulo'], 'Tarea API')
        self.assertFalse(datos['completada'])

    def test_crear_tarea_sin_titulo_devuelve_400(self):
        respuesta = self.client.post(
            '/api/tareas',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(respuesta.status_code, 400)

    # ── GET /api/tasks/<id> ───────────────────────────────────────────────

    def test_obtener_tarea_individual_devuelve_200(self):
        creada = json.loads(self.client.post(
            '/api/tareas',
            data=json.dumps({'titulo': 'Buscar tarea'}),
            content_type='application/json'
        ).data)
        respuesta = self.client.get(f"/api/tareas/{creada['id']}")
        self.assertEqual(respuesta.status_code, 200)

    def test_obtener_tarea_inexistente_devuelve_404(self):
        respuesta = self.client.get('/api/tareas/9999')
        self.assertEqual(respuesta.status_code, 404)

    # ── PUT /api/tasks/<id> ───────────────────────────────────────────────

    def test_actualizar_tarea_devuelve_200(self):
        creada = json.loads(self.client.post(
            '/api/tareas',
            data=json.dumps({'titulo': 'Antes'}),
            content_type='application/json'
        ).data)
        respuesta = self.client.put(
            f"/api/tareas/{creada['id']}",
            data=json.dumps({'titulo': 'Después'}),
            content_type='application/json'
        )
        self.assertEqual(respuesta.status_code, 200)

    def test_actualizar_tarea_cambia_titulo(self):
        creada = json.loads(self.client.post(
            '/api/tareas',
            data=json.dumps({'titulo': 'Viejo título'}),
            content_type='application/json'
        ).data)
        self.client.put(
            f"/api/tareas/{creada['id']}",
            data=json.dumps({'titulo': 'Nuevo título'}),
            content_type='application/json'
        )
        obtenida = json.loads(self.client.get(f"/api/tareas/{creada['id']}").data)
        self.assertEqual(obtenida['titulo'], 'Nuevo título')

    # ── POST /api/tasks/<id>/toggle ───────────────────────────────────────

    def test_cambiar_estado_alterna_completada(self):
        creada = json.loads(self.client.post(
            '/api/tareas',
            data=json.dumps({'titulo': 'Prueba de cambio'}),
            content_type='application/json'
        ).data)
        respuesta = self.client.post(f"/api/tareas/{creada['id']}/cambiar-estado")
        datos = json.loads(respuesta.data)
        self.assertTrue(datos['completada'])

    # ── DELETE /api/tasks/<id> ────────────────────────────────────────────

    def test_eliminar_tarea_devuelve_200(self):
        creada = json.loads(self.client.post(
            '/api/tareas',
            data=json.dumps({'titulo': 'A eliminar'}),
            content_type='application/json'
        ).data)
        respuesta = self.client.delete(f"/api/tareas/{creada['id']}")
        self.assertEqual(respuesta.status_code, 200)

    def test_eliminar_tarea_la_quita_del_listado(self):
        creada = json.loads(self.client.post(
            '/api/tareas',
            data=json.dumps({'titulo': 'Eliminar esta'}),
            content_type='application/json'
        ).data)
        self.client.delete(f"/api/tareas/{creada['id']}")
        respuesta = self.client.get('/api/tareas')
        tareas = json.loads(respuesta.data)
        ids = [t['id'] for t in tareas]
        self.assertNotIn(creada['id'], ids)

    def test_eliminar_tarea_inexistente_devuelve_404(self):
        respuesta = self.client.delete('/api/tareas/9999')
        self.assertEqual(respuesta.status_code, 404)


if __name__ == '__main__':
    unittest.main()
