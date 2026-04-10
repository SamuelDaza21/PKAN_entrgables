# Historias de Usuario — To-Do List XP

## Iteración 1

| ID | Historia | Prioridad | Estimación |
|----|----------|-----------|------------|
| HU-1 | Como **usuario** quiero **crear una nueva tarea** para **registrar mis actividades pendientes** | Alta | 2 h |
| HU-2 | Como **usuario** quiero **ver la lista de todas mis tareas** para **conocer qué tengo pendiente** | Alta | 1 h |
| HU-3 | Como **usuario** quiero **marcar una tarea como completada** para **saber qué ya terminé** | Alta | 1 h |
| HU-4 | Como **usuario** quiero **editar el título de una tarea** para **corregir o actualizar su descripción** | Media | 1 h |
| HU-5 | Como **usuario** quiero **eliminar una tarea** para **limpiar mi lista de elementos irrelevantes** | Media | 1 h |

## Iteración 2

| ID | Historia | Prioridad | Estimación |
|----|----------|-----------|------------|
| HU-6 | Como **usuario** quiero **persistir mis tareas en una base de datos** para **no perderlas al cerrar la app** | Alta | 2 h |
| HU-7 | Como **usuario** quiero **ver un contador de tareas completadas vs pendientes** para **tener un resumen rápido** | Baja | 0.5 h |

## Criterios de Aceptación

### HU-1: Crear tarea
- El formulario valida que el título no esté vacío.
- Tras enviar, la tarea aparece inmediatamente en la lista.
- La tarea se persiste en SQLite.

### HU-2: Ver lista de tareas
- Se muestran todas las tareas ordenadas por fecha de creación (más reciente primero).
- Si no hay tareas se muestra un mensaje de estado vacío.

### HU-3: Marcar como completada
- El estado se refleja visualmente (tachado + icono).
- Se puede desmarcar la tarea.

### HU-4: Editar tarea
- Se muestra un formulario inline al pulsar "Editar".
- El nuevo título se guarda al enviar.

### HU-5: Eliminar tarea
- Se pide confirmación antes de borrar.
- La tarea desaparece de la lista tras confirmar.

### HU-6: Persistencia SQLite
- Al reiniciar la aplicación las tareas se mantienen.

### HU-7: Contador de tareas
- El encabezado muestra: Total / Completadas / Pendientes.
