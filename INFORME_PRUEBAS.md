# Informe de Pruebas

## Pruebas existentes actualmente

El proyecto cuenta con tres grupos de pruebas automatizadas:

1. `tests/test_models.py`: valida el modelo `Tarea` y sus operaciones CRUD, incluyendo creación, consulta, actualización, alternancia de estado, eliminación y serialización.
2. `tests/test_routes.py`: valida la API JSON mediante peticiones HTTP sobre los endpoints de tareas.
3. `tests/test_integration.py`: valida flujos completos que combinan varias operaciones y comprueban la respuesta de la interfaz HTML principal.

## Clasificación de las pruebas

### 1. Pruebas del modelo

- **Tipo principal:** pruebas unitarias.
- **Caja:** principalmente **caja blanca**.
- **Por qué:** ejercitan métodos concretos del modelo (`crear`, `obtener_todas`, `obtener_por_id`, `actualizar`, `alternar_completada`, `eliminar`) con conocimiento directo de su interfaz interna y del comportamiento esperado sobre una base de datos temporal.

### 2. Pruebas de rutas API

- **Tipo principal:** pruebas funcionales de API o pruebas de componente.
- **Caja:** mayormente **caja negra**, con un matiz de **caja gris**.
- **Por qué:** verifican códigos de estado y cuerpos JSON a través del cliente de pruebas de Flask, como lo haría un consumidor externo. A la vez, parchean la clase del modelo para aislar la base de datos del entorno real, lo que introduce conocimiento interno de la implementación.

### 3. Pruebas de integración

- **Tipo principal:** pruebas de integración.
- **Caja:** **caja gris**.
- **Por qué:** validan flujos completos entre modelo, base de datos y endpoints. No son puramente de caja negra porque conocen cómo inyectar una base de datos temporal y sustituyen la clase del modelo dentro de la aplicación.

### 4. Pruebas de humo

- **Sí existen parcialmente.**
- **Por qué:** comprobaciones como que la página principal responda `200` o que la API liste tareas sin error funcionan como smoke tests básicos, ya que confirman que la aplicación arranca y responde en operaciones esenciales.

## ¿Son suficientes?

La suite actual es **buena para un MVP pequeño**, pero **no es suficiente** para considerar el proyecto completamente cubierto.

Cobertura fuerte:

- CRUD del modelo.
- Respuestas principales de la API JSON.
- Algunos flujos integrados de persistencia.
- Disponibilidad básica de la vista HTML principal.

Cobertura débil o ausente:

- Validación detallada de la interfaz HTML: no se comprueba que crear, editar o eliminar desde formularios HTML renderice correctamente los cambios en pantalla.
- Casos borde de entrada: títulos con espacios, longitud extrema, caracteres especiales o entradas repetidas.
- Compatibilidad heredada: no hay pruebas específicas para las rutas y claves antiguas en inglés que se mantienen por compatibilidad.
- Persistencia real sobre la base `todo.db`: se prueban bases temporales, pero no la migración del esquema anterior en una base existente.
- Manejo de errores no funcionales: por ejemplo, fallos de base de datos o solicitudes mal formadas más allá de la ausencia de título.

## Recomendaciones de mejora

1. Agregar pruebas de rutas HTML que verifiquen creación, edición, cambio de estado y eliminación mediante formularios reales.
2. Añadir pruebas de migración de base de datos para validar la transición desde la tabla antigua `tasks` hacia `tareas`.
3. Incorporar pruebas de casos borde sobre títulos vacíos, espacios únicamente, cadenas largas y caracteres Unicode.
4. Crear pruebas explícitas de compatibilidad para las rutas y claves heredadas en inglés mientras sigan disponibles.
5. Medir cobertura con `pytest --cov` para detectar vacíos reales antes de ampliar la suite.

## Términos no traducidos y justificación

Se mantienen algunos términos técnicos estándar porque forman parte del ecosistema de desarrollo o de contratos ampliamente reconocidos:

- **Flask**, **SQLite**, **JSON** y **README**: son nombres técnicos establecidos.
- La carpeta `tests` y los nombres de archivo principales se conservaron para evitar fricción con herramientas, imports y estructura existente del proyecto.
- También se mantienen rutas y claves heredadas en inglés de forma transitoria para no romper integraciones existentes, aunque la interfaz principal y la documentación ahora usan español.