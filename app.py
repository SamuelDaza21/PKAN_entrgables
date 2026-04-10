from flask import Flask, jsonify, redirect, render_template, request, url_for

from database import inicializar_bd
from models import Tarea

app = Flask(__name__)


@app.before_request
def preparar_aplicacion():
    """Asegura que la base de datos exista antes de atender la solicitud."""
    inicializar_bd()


def obtener_titulo_desde_solicitud():
    titulo_formulario = request.form.get('titulo')
    titulo_legacy = request.form.get('title')
    datos_json = request.get_json(silent=True) or {}
    titulo_json = datos_json.get('titulo')
    titulo_json_legacy = datos_json.get('title')
    return (titulo_formulario or titulo_legacy or titulo_json or titulo_json_legacy or '').strip()


def usar_formato_api_legacy():
    return request.path.startswith('/api/tasks')


def serializar_tarea(tarea):
    return tarea.to_dict() if usar_formato_api_legacy() else tarea.a_diccionario()


def error_api(mensaje_es, mensaje_en):
    mensaje = mensaje_en if usar_formato_api_legacy() else mensaje_es
    return jsonify({'error': mensaje})


def mensaje_api(mensaje_es, mensaje_en):
    mensaje = mensaje_en if usar_formato_api_legacy() else mensaje_es
    return jsonify({'message': mensaje})


# Rutas HTML

@app.route('/')
def inicio():
    tareas = Tarea.obtener_todas()
    return render_template('index.html', tareas=tareas)


@app.route('/tasks/create', methods=['POST'])
@app.route('/tasks/create', methods=['POST'])
@app.route('/tareas/crear', methods=['POST'])
def crear_tarea():
    titulo = obtener_titulo_desde_solicitud()
    if titulo:
        Tarea.crear(titulo)
    return redirect(url_for('inicio'))


@app.route('/tasks/<int:task_id>/toggle', methods=['POST'])
@app.route('/tasks/<int:task_id>/toggle', methods=['POST'])
@app.route('/tareas/<int:tarea_id>/cambiar-estado', methods=['POST'])
def cambiar_estado_tarea(tarea_id):
    Tarea.alternar_completada(tarea_id)
    return redirect(url_for('inicio'))


@app.route('/tasks/<int:task_id>/edit', methods=['POST'])
@app.route('/tasks/<int:task_id>/edit', methods=['POST'])
@app.route('/tareas/<int:tarea_id>/editar', methods=['POST'])
def editar_tarea(tarea_id):
    titulo = obtener_titulo_desde_solicitud()
    if titulo:
        Tarea.actualizar(tarea_id, titulo)
    return redirect(url_for('inicio'))


@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
@app.route('/tareas/<int:tarea_id>/eliminar', methods=['POST'])
def eliminar_tarea(tarea_id):
    Tarea.eliminar(tarea_id)
    return redirect(url_for('inicio'))


# API JSON

@app.route('/api/tasks', methods=['GET'])
@app.route('/api/tasks', methods=['GET'])
@app.route('/api/tareas', methods=['GET'])
def api_listar_tareas():
    return jsonify([serializar_tarea(tarea) for tarea in Tarea.obtener_todas()])


@app.route('/api/tasks', methods=['POST'])
@app.route('/api/tasks', methods=['POST'])
@app.route('/api/tareas', methods=['POST'])
def api_crear_tarea():
    titulo = obtener_titulo_desde_solicitud()
    if not titulo:
        return error_api('Se requiere el titulo.', 'title is required'), 400
    tarea = Tarea.crear(titulo)
    return jsonify(serializar_tarea(tarea)), 201


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
@app.route('/api/tareas/<int:tarea_id>', methods=['GET'])
def api_obtener_tarea(tarea_id):
    tarea = Tarea.obtener_por_id(tarea_id)
    if tarea is None:
        return error_api('Tarea no encontrada.', 'not found'), 404
    return jsonify(serializar_tarea(tarea))


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@app.route('/api/tareas/<int:tarea_id>', methods=['PUT'])
def api_actualizar_tarea(tarea_id):
    titulo = obtener_titulo_desde_solicitud()
    if not titulo:
        return error_api('Se requiere el titulo.', 'title is required'), 400
    actualizada = Tarea.actualizar(tarea_id, titulo)
    if not actualizada:
        return error_api('Tarea no encontrada.', 'not found'), 404
    return jsonify(serializar_tarea(Tarea.obtener_por_id(tarea_id)))


@app.route('/api/tasks/<int:task_id>/toggle', methods=['POST'])
@app.route('/api/tasks/<int:task_id>/toggle', methods=['POST'])
@app.route('/api/tareas/<int:tarea_id>/cambiar-estado', methods=['POST'])
def api_cambiar_estado_tarea(tarea_id):
    actualizada = Tarea.alternar_completada(tarea_id)
    if not actualizada:
        return error_api('Tarea no encontrada.', 'not found'), 404
    return jsonify(serializar_tarea(Tarea.obtener_por_id(tarea_id)))


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@app.route('/api/tareas/<int:tarea_id>', methods=['DELETE'])
def api_eliminar_tarea(tarea_id):
    eliminada = Tarea.eliminar(tarea_id)
    if not eliminada:
        return error_api('Tarea no encontrada.', 'not found'), 404
    return mensaje_api('Tarea eliminada.', 'deleted')


if __name__ == '__main__':
    import os as _os
    inicializar_bd()
    app.run(debug=_os.getenv('FLASK_DEBUG', '0') == '1')
