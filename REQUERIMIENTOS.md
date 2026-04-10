# Requerimientos del Sistema — To-Do List

## 1. Objetivo

Este documento define los requerimientos funcionales y no funcionales del proyecto To-Do List, tomando como base las historias de usuario de [HISTORIAS_USUARIO.md](HISTORIAS_USUARIO.md), la implementación actual en Flask y SQLite, y las pruebas automatizadas del sistema.

## 2. Alcance del sistema

La aplicación permite gestionar una lista de tareas personales mediante una interfaz web y una API JSON. El sistema cubre las operaciones principales de crear, listar, editar, completar y eliminar tareas, manteniendo la información persistida en una base de datos SQLite.

## 3. Actores

- Usuario final: persona que administra sus tareas desde la interfaz web.
- Cliente API: consumidor técnico que interactúa con los endpoints JSON del sistema.

## 4. Requerimientos funcionales

### RF-01. Crear tarea
- El sistema debe permitir registrar una nueva tarea ingresando un título.
- El sistema debe aceptar la creación de tareas desde la interfaz web y desde la API JSON.
- El sistema debe almacenar cada nueva tarea en la base de datos con un identificador único.
- El sistema debe asignar por defecto el estado pendiente a toda tarea recién creada.
- El sistema no debe crear tareas cuando el título esté vacío.

### RF-02. Listar tareas
- El sistema debe mostrar todas las tareas registradas en la página principal.
- El sistema debe exponer un endpoint API para consultar la colección completa de tareas.
- El sistema debe listar las tareas ordenadas por fecha de creación, de la más reciente a la más antigua.
- El sistema debe poder responder con una lista vacía cuando no existan tareas registradas.

### RF-03. Consultar tarea individual
- El sistema debe permitir consultar una tarea específica por su identificador mediante la API.
- El sistema debe devolver los datos de la tarea, incluyendo id, título, estado de completado y fecha de creación.
- El sistema debe responder con un error controlado cuando se solicite una tarea inexistente.

### RF-04. Cambiar estado de una tarea
- El sistema debe permitir marcar una tarea como completada.
- El sistema debe permitir desmarcar una tarea ya completada para volverla a estado pendiente.
- El sistema debe reflejar visualmente el estado de completado en la interfaz.
- El sistema debe exponer una operación en la API para alternar el estado de completado de una tarea.
- El sistema debe responder con un error controlado cuando se intente cambiar el estado de una tarea inexistente.

### RF-05. Editar tarea
- El sistema debe permitir modificar el título de una tarea existente.
- El sistema debe permitir editar la tarea desde la interfaz web y desde la API JSON.
- El sistema no debe aceptar la actualización si el nuevo título está vacío.
- El sistema debe responder con un error controlado cuando se intente editar una tarea inexistente.

### RF-06. Eliminar tarea
- El sistema debe permitir eliminar una tarea existente desde la interfaz web.
- El sistema debe permitir eliminar una tarea existente desde la API JSON.
- El sistema debe remover definitivamente la tarea de la base de datos.
- El sistema debe dejar de mostrar la tarea en listados posteriores una vez eliminada.
- El sistema debe responder con un error controlado cuando se intente eliminar una tarea inexistente.

### RF-07. Persistencia de datos
- El sistema debe persistir las tareas en una base de datos SQLite local.
- El sistema debe conservar las tareas aunque la aplicación se cierre y vuelva a iniciarse.
- El sistema debe crear automáticamente la estructura de base de datos necesaria si esta no existe.

### RF-08. Contador de tareas
- El sistema debe mostrar un resumen del total de tareas.
- El sistema debe mostrar la cantidad de tareas completadas.
- El sistema debe mostrar la cantidad de tareas pendientes.
- El resumen debe estar visible en el encabezado o zona principal de la interfaz.

### RF-09. Compatibilidad de rutas API
- El sistema debe mantener endpoints principales en español bajo el prefijo `/api/tareas`.
- El sistema debe conservar compatibilidad con rutas heredadas en inglés para evitar romper integraciones existentes.
- El sistema debe aceptar claves de entrada tanto en español como en inglés para el título de la tarea cuando corresponda.

### RF-10. Navegación principal
- El sistema debe disponer de una página principal accesible desde la ruta `/`.
- El sistema debe cargar en esa vista el listado actualizado de tareas.
- El sistema debe redirigir al usuario nuevamente a la página principal luego de operaciones HTML como crear, editar, completar o eliminar.

## 5. Requerimientos no funcionales

### RNF-01. Usabilidad
- La interfaz debe ser simple y comprensible para un usuario sin conocimientos técnicos.
- Las acciones principales del sistema deben estar visibles desde la página principal.
- El estado de una tarea completada debe distinguirse claramente del de una tarea pendiente.

### RNF-02. Rendimiento
- El sistema debe responder de forma inmediata para operaciones CRUD sobre volúmenes pequeños y medianos de tareas, propios de una aplicación personal.
- Las operaciones de listado, creación, edición, cambio de estado y eliminación deben ejecutarse sin demoras perceptibles en un entorno local.

### RNF-03. Persistencia y confiabilidad
- La información de las tareas debe conservarse de manera consistente en SQLite después de cada operación.
- El sistema debe inicializar la base de datos antes de atender solicitudes para reducir fallos por ausencia de esquema.
- El sistema debe migrar automáticamente la tabla heredada `tasks` hacia la estructura actual `tareas` cuando corresponda.

### RNF-04. Mantenibilidad
- El proyecto debe estar organizado por responsabilidades separadas para aplicación, acceso a datos, vistas, estilos y pruebas.
- El código debe ser lo suficientemente claro para facilitar correcciones y ampliaciones futuras.
- La documentación del proyecto debe describir instalación, ejecución, estructura y artefactos XP.

### RNF-05. Testabilidad
- El sistema debe contar con pruebas automatizadas unitarias, de rutas e integración.
- Los cambios funcionales relevantes deben poder verificarse mediante la suite de pruebas existente.
- La arquitectura debe permitir ejecutar pruebas con bases de datos temporales independientes del archivo productivo.

### RNF-06. Portabilidad
- El sistema debe poder ejecutarse en cualquier entorno con Python 3.8+ y las dependencias del archivo `requirements.txt`.
- La solución debe usar tecnologías estándar y de fácil instalación en entornos académicos o locales.

### RNF-07. Seguridad básica
- El sistema debe validar entradas mínimas para impedir operaciones inválidas, como títulos vacíos.
- El acceso a datos debe realizarse mediante consultas parametrizadas para reducir riesgo de inyección SQL.
- Cuando una operación no pueda completarse por inexistencia del recurso, el sistema debe responder con códigos de estado HTTP apropiados en la API.

### RNF-08. Interoperabilidad
- La API debe intercambiar información en formato JSON.
- La representación de las tareas debe mantenerse consistente entre las respuestas del sistema.
- El sistema debe soportar formatos de respuesta compatibles con consumidores en español y con integraciones heredadas en inglés.

## 6. Trazabilidad con historias de usuario

| Historia de usuario | Requerimientos relacionados |
|---|---|
| HU-1 Crear tarea | RF-01, RF-07, RNF-01, RNF-07 |
| HU-2 Ver lista de tareas | RF-02, RF-10, RNF-01, RNF-02 |
| HU-3 Marcar como completada | RF-04, RNF-01, RNF-03 |
| HU-4 Editar tarea | RF-05, RNF-01, RNF-07 |
| HU-5 Eliminar tarea | RF-06, RNF-01, RNF-03 |
| HU-6 Persistencia SQLite | RF-07, RNF-03, RNF-06 |
| HU-7 Contador de tareas | RF-08, RNF-01 |

## 7. Supuestos y restricciones

- El sistema está orientado a un uso local o académico y no contempla autenticación de usuarios.
- La base de datos utilizada por defecto es SQLite y se almacena localmente en el proyecto.
- El proyecto trabaja con una sola entidad principal: tarea.
- La aplicación está diseñada como un MVP y puede evolucionar en iteraciones posteriores.