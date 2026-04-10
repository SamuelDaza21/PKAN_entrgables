# Contenido Base Para Diagramas UML — To-Do List

## 1. Propósito

Este archivo contiene la información necesaria para elaborar el diagrama de clases y el diagrama de casos de uso del proyecto To-Do List, de acuerdo con la implementación actual en Flask, SQLite y las historias de usuario del sistema.

## 2. Convención de modificadores de acceso

- `+` Público
- `-` Privado

## 3. Diagrama de Clases

### 3.1 Clase principal de dominio

#### Clase: Tarea

**Descripción:** representa una tarea dentro de la lista.

**Atributos**

| Modificador | Nombre | Tipo |
|---|---|---|
| + | id | Integer |
| + | titulo | String |
| + | completada | Boolean |
| + | creada_en | DateTime |

**Métodos**

| Modificador | Nombre | Parámetros | Tipo de retorno |
|---|---|---|---|
| + | __init__ | tarea_id: Integer, titulo: String, completada: Boolean, creada_en: DateTime | None |
| - | _desde_fila | fila: Row | Tarea \| None |
| + | crear | titulo: String, ruta_bd: String \| None | Tarea |
| + | obtener_todas | ruta_bd: String \| None | List<Tarea> |
| + | obtener_por_id | tarea_id: Integer, ruta_bd: String \| None | Tarea \| None |
| + | actualizar | tarea_id: Integer, titulo: String, ruta_bd: String \| None | Boolean |
| + | alternar_completada | tarea_id: Integer, ruta_bd: String \| None | Boolean |
| + | eliminar | tarea_id: Integer, ruta_bd: String \| None | Boolean |
| + | a_diccionario | sin parámetros | Dictionary |
| + | title | sin parámetros | String |
| + | completed | sin parámetros | Boolean |
| + | created_at | sin parámetros | DateTime |
| + | create | title: String, db_path: String \| None | Tarea |
| + | get_all | db_path: String \| None | List<Tarea> |
| + | get_by_id | task_id: Integer, db_path: String \| None | Tarea \| None |
| + | update | task_id: Integer, title: String, db_path: String \| None | Boolean |
| + | toggle_completed | task_id: Integer, db_path: String \| None | Boolean |
| + | delete | task_id: Integer, db_path: String \| None | Boolean |
| + | to_dict | sin parámetros | Dictionary |

### 3.2 Clase utilitaria de persistencia

#### Clase: GestorBD

**Descripción:** representa la responsabilidad de conexión e inicialización de la base de datos SQLite. En el código fuente actual esta responsabilidad está implementada en `database.py` mediante funciones.

**Atributos**

| Modificador | Nombre | Tipo |
|---|---|---|
| + | RUTA_BD | String |

**Métodos**

| Modificador | Nombre | Parámetros | Tipo de retorno |
|---|---|---|---|
| + | obtener_conexion | ruta_bd: String \| None | Connection |
| + | inicializar_bd | ruta_bd: String \| None | None |

### 3.3 Clase de control de la aplicación

#### Clase: ControladorTareas

**Descripción:** concentra la lógica de las rutas HTML y API. En la implementación actual esta responsabilidad está distribuida en funciones dentro de `app.py`.

**Atributos**

| Modificador | Nombre | Tipo |
|---|---|---|
| + | app | Flask |

**Métodos**

| Modificador | Nombre | Parámetros | Tipo de retorno |
|---|---|---|---|
| + | preparar_aplicacion | sin parámetros | None |
| + | obtener_titulo_desde_solicitud | sin parámetros | String |
| + | usar_formato_api_legacy | sin parámetros | Boolean |
| + | serializar_tarea | tarea: Tarea | Dictionary |
| + | error_api | mensaje_es: String, mensaje_en: String | Response |
| + | mensaje_api | mensaje_es: String, mensaje_en: String | Response |
| + | inicio | sin parámetros | Response |
| + | crear_tarea | sin parámetros | Response |
| + | cambiar_estado_tarea | tarea_id: Integer | Response |
| + | editar_tarea | tarea_id: Integer | Response |
| + | eliminar_tarea | tarea_id: Integer | Response |
| + | api_listar_tareas | sin parámetros | Response |
| + | api_crear_tarea | sin parámetros | Response |
| + | api_obtener_tarea | tarea_id: Integer | Response |
| + | api_actualizar_tarea | tarea_id: Integer | Response |
| + | api_cambiar_estado_tarea | tarea_id: Integer | Response |
| + | api_eliminar_tarea | tarea_id: Integer | Response |

### 3.4 Relaciones para el diagrama de clases

- `ControladorTareas` usa a `Tarea` para ejecutar las operaciones CRUD.
- `Tarea` depende de `GestorBD` para acceder a SQLite.
- `GestorBD` administra la conexión con la base de datos `todo.db`.

### 3.5 Versión textual corta del diagrama de clases

```text
ControladorTareas --> Tarea
Tarea --> GestorBD

Clase Tarea
+ id: Integer
+ titulo: String
+ completada: Boolean
+ creada_en: DateTime
+ crear(titulo: String, ruta_bd: String | None): Tarea
+ obtener_todas(ruta_bd: String | None): List<Tarea>
+ obtener_por_id(tarea_id: Integer, ruta_bd: String | None): Tarea | None
+ actualizar(tarea_id: Integer, titulo: String, ruta_bd: String | None): Boolean
+ alternar_completada(tarea_id: Integer, ruta_bd: String | None): Boolean
+ eliminar(tarea_id: Integer, ruta_bd: String | None): Boolean
+ a_diccionario(): Dictionary

Clase GestorBD
+ RUTA_BD: String
+ obtener_conexion(ruta_bd: String | None): Connection
+ inicializar_bd(ruta_bd: String | None): None

Clase ControladorTareas
+ app: Flask
+ inicio(): Response
+ crear_tarea(): Response
+ cambiar_estado_tarea(tarea_id: Integer): Response
+ editar_tarea(tarea_id: Integer): Response
+ eliminar_tarea(tarea_id: Integer): Response
+ api_listar_tareas(): Response
+ api_crear_tarea(): Response
+ api_obtener_tarea(tarea_id: Integer): Response
+ api_actualizar_tarea(tarea_id: Integer): Response
+ api_cambiar_estado_tarea(tarea_id: Integer): Response
+ api_eliminar_tarea(tarea_id: Integer): Response
```

## 4. Diagrama de Casos de Uso

### 4.1 Actores

| Actor | Descripción |
|---|---|
| Usuario | Persona que gestiona sus tareas desde la interfaz web. |
| Cliente API | Sistema externo o consumidor técnico que usa la API JSON. |

### 4.2 Casos de uso principales

| Código | Caso de uso | Actor principal |
|---|---|---|
| CU-01 | Crear tarea | Usuario, Cliente API |
| CU-02 | Ver lista de tareas | Usuario, Cliente API |
| CU-03 | Consultar tarea individual | Cliente API |
| CU-04 | Editar tarea | Usuario, Cliente API |
| CU-05 | Cambiar estado de tarea | Usuario, Cliente API |
| CU-06 | Eliminar tarea | Usuario, Cliente API |
| CU-07 | Ver resumen de tareas | Usuario |
| CU-08 | Validar título de tarea | Sistema |
| CU-09 | Buscar tarea por ID | Sistema |
| CU-10 | Confirmar eliminación | Usuario |

### 4.3 Relaciones `include`

Las siguientes relaciones representan pasos obligatorios o reutilizados por varios casos de uso:

| Caso base | Relación | Caso incluido |
|---|---|---|
| Crear tarea | `<<include>>` | Validar título de tarea |
| Editar tarea | `<<include>>` | Validar título de tarea |
| Consultar tarea individual | `<<include>>` | Buscar tarea por ID |
| Cambiar estado de tarea | `<<include>>` | Buscar tarea por ID |
| Editar tarea | `<<include>>` | Buscar tarea por ID |
| Eliminar tarea | `<<include>>` | Buscar tarea por ID |
| Ver lista de tareas | `<<include>>` | Ver resumen de tareas |

### 4.4 Relaciones `extend`

Las siguientes relaciones representan comportamientos opcionales o dependientes de una condición:

| Caso base | Relación | Caso extendido | Condición |
|---|---|---|---|
| Eliminar tarea | `<<extend>>` | Confirmar eliminación | Cuando la eliminación se realiza desde la interfaz web |
| Ver lista de tareas | `<<extend>>` | Mostrar mensaje de lista vacía | Cuando no existen tareas registradas |
| Cambiar estado de tarea | `<<extend>>` | Desmarcar tarea completada | Cuando la tarea ya estaba completada |

### 4.5 Asociación actor-caso de uso

#### Usuario
- Crear tarea
- Ver lista de tareas
- Editar tarea
- Cambiar estado de tarea
- Eliminar tarea
- Ver resumen de tareas
- Confirmar eliminación

#### Cliente API
- Crear tarea
- Ver lista de tareas
- Consultar tarea individual
- Editar tarea
- Cambiar estado de tarea
- Eliminar tarea

### 4.6 Versión textual corta del diagrama de casos de uso

```text
Actor Usuario
- Crear tarea
- Ver lista de tareas
- Editar tarea
- Cambiar estado de tarea
- Eliminar tarea
- Ver resumen de tareas

Actor Cliente API
- Crear tarea
- Ver lista de tareas
- Consultar tarea individual
- Editar tarea
- Cambiar estado de tarea
- Eliminar tarea

Crear tarea <<include>> Validar título de tarea
Editar tarea <<include>> Validar título de tarea
Consultar tarea individual <<include>> Buscar tarea por ID
Cambiar estado de tarea <<include>> Buscar tarea por ID
Editar tarea <<include>> Buscar tarea por ID
Eliminar tarea <<include>> Buscar tarea por ID
Ver lista de tareas <<include>> Ver resumen de tareas

Confirmar eliminación <<extend>> Eliminar tarea
Mostrar mensaje de lista vacía <<extend>> Ver lista de tareas
Desmarcar tarea completada <<extend>> Cambiar estado de tarea
```

## 5. Recomendación para dibujarlo

- Si el docente quiere reflejar exactamente el código implementado, usa `Tarea` como clase real principal y representa `GestorBD` y `ControladorTareas` como clases de apoyo o estereotipos `<<utility>>` y `<<control>>`.
- Si el enfoque es más académico, puedes usar las tres cajas `ControladorTareas`, `Tarea` y `GestorBD` para que el diagrama muestre claramente presentación, lógica y persistencia.
- En el diagrama de casos de uso, el actor principal del sistema es `Usuario`; `Cliente API` se recomienda solo si deseas representar también la interfaz programática del proyecto.