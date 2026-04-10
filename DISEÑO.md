# Diseño Simple — Lista de Tareas XP

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────┐
│                  CLIENTE                    │
│          HTML + CSS (index.html)            │
│  (formularios, lista de tareas, acciones)   │
└───────────────┬─────────────────────────────┘
                │  HTTP (GET / POST)
┌───────────────▼─────────────────────────────┐
│             SERVIDOR WEB                    │
│           Flask — app.py                    │
│  Rutas HTML: /  /tareas/crear  /tareas/<id> │
│  Rutas API:  /api/tareas /api/tareas/<id>   │
└───────────────┬─────────────────────────────┘
                │  Llama a métodos estáticos
┌───────────────▼─────────────────────────────┐
│              CAPA DE MODELO                 │
│            models.py — Tarea                │
│ crear / obtener_todas / obtener_por_id      │
│ actualizar / alternar_completada / eliminar │
└───────────────┬─────────────────────────────┘
                │  SQL (INSERT / SELECT / UPDATE / DELETE)
┌───────────────▼─────────────────────────────┐
│          BASE DE DATOS                      │
│       database.py + todo.db (SQLite)        │
│  Tabla: tareas (id, titulo, completada,     │
│                 creada_en)                  │
└─────────────────────────────────────────────┘
```

## Diagrama de Clases (simplificado)

```
Tarea
────────────────────────────────
+ id         : int
+ titulo     : str
+ completada : bool
+ creada_en  : str
────────────────────────────────
+ crear(titulo)              → Tarea
+ obtener_todas()            → list[Tarea]
+ obtener_por_id(id)         → Tarea | None
+ actualizar(id, titulo)     → bool
+ alternar_completada(id)    → bool
+ eliminar(id)               → bool
+ a_diccionario()            → dict
```

## Estructura de Carpetas

```
To-Do-List/
├── app.py              ← Controlador Flask (rutas HTML + API)
├── database.py         ← Gestión de conexión SQLite y migración
├── models.py           ← Lógica de negocio (CRUD de tareas)
├── requirements.txt
├── tests/
│   ├── __init__.py
│   ├── test_models.py      ← Pruebas unitarias del modelo
│   ├── test_routes.py      ← Pruebas de rutas API
│   └── test_integration.py ← Pruebas de integración
├── templates/
│   └── index.html      ← Vista única (SPA simple)
├── static/
│   └── style.css
├── HISTORIAS_USUARIO.md
├── DISEÑO.md           ← (este archivo)
├── REFLEXION_XP.md
└── README.md
```

## Decisiones de Diseño

| Decisión | Justificación XP |
|----------|-----------------|
| Una sola tabla SQLite | Diseño más simple posible (principio YAGNI) |
| Métodos estáticos en Tarea | Facilita el testing con BD temporal sin mocks complejos |
| Rutas HTML + API JSON | Permite pruebas de integración sin Selenium |
| `ruta_bd` como parámetro | Inyección de dependencia simple para tests aislados |
| Flask sin ORM | Menos dependencias, mayor control, más simple |
| Compatibilidad heredada en inglés | Evita romper clientes o pruebas antiguas durante la transición al español |
