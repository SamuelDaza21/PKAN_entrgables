# 📝 Lista de Tareas — Taller XP

Sistema de gestión de tareas desarrollado con **Python + Flask + SQLite**, aplicando la metodología **Extreme Programming (XP)**.

Desarrollado por **Samuel Daza & Jayber**.

---

## 🚀 Instalación y ejecución

### Requisitos previos
- Python 3.8+
- pip

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/SamuelDaza21/To-Do-List.git
cd To-Do-List

# 2. (Opcional) Crear entorno virtual
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
python app.py
```

Abrir el navegador en: **http://127.0.0.1:5000**

---

## 🧪 Ejecutar pruebas

```bash
python -m pytest tests/ -v
```

Resultado esperado: **las pruebas deben finalizar sin errores**.

---

## 📂 Estructura del proyecto

```
To-Do-List/
├── app.py                  ← Aplicación Flask (rutas HTML + API JSON)
├── database.py             ← Configuración SQLite y migración básica
├── models.py               ← Modelo de datos Tarea (CRUD)
├── requirements.txt        ← Dependencias Python
├── tests/
│   ├── test_models.py      ← Pruebas unitarias del modelo
│   ├── test_routes.py      ← Pruebas de rutas API
│   └── test_integration.py ← Pruebas de integración
├── templates/
│   └── index.html          ← Interfaz web
├── static/
│   └── style.css           ← Estilos
├── INFORME_PRUEBAS.md      ← Análisis de cobertura y recomendaciones
├── HISTORIAS_USUARIO.md    ← Historias priorizadas
├── DISEÑO.md               ← Arquitectura y diagrama
├── REFLEXION_XP.md         ← Análisis del proceso XP
└── README.md               ← Este archivo
```

---

## ✅ Funcionalidades MVP

| # | Funcionalidad | Estado |
|---|---------------|--------|
| 1 | Crear nueva tarea | ✅ |
| 2 | Ver lista de tareas | ✅ |
| 3 | Marcar tarea como completada | ✅ |
| 4 | Editar descripción de tarea | ✅ |
| 5 | Eliminar tarea | ✅ |
| 6 | Persistencia en SQLite | ✅ |
| 7 | Contador de tareas (total/completadas/pendientes) | ✅ |

---

## 🔗 API JSON

| Método | Endpoint principal | Descripción |
|--------|--------------------|-------------|
| GET | `/api/tareas` | Listar todas las tareas |
| POST | `/api/tareas` | Crear tarea (`{"titulo": "..."}`) |
| GET | `/api/tareas/<id>` | Obtener una tarea |
| PUT | `/api/tareas/<id>` | Actualizar título |
| POST | `/api/tareas/<id>/cambiar-estado` | Cambiar estado completado |
| DELETE | `/api/tareas/<id>` | Eliminar tarea |

También se mantienen rutas y claves heredadas en inglés para no romper integraciones existentes durante la transición.

---

## 📚 Documentación XP

- [Historias de Usuario](HISTORIAS_USUARIO.md)
- [Requerimientos del Sistema](REQUERIMIENTOS.md)
- [Diseño del Sistema](DISEÑO.md)
- [Reflexión XP](REFLEXION_XP.md)
- [Informe de Pruebas](INFORME_PRUEBAS.md)

