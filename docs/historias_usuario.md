# Historias de Usuario

## HU-01 Registro de estudiantes
Como administrador academico, quiero registrar estudiantes con nombre, codigo y programa para habilitar su identificacion en el sistema.

Criterios de aceptacion:
- Se debe poder registrar un estudiante con datos obligatorios completos.
- El codigo institucional no puede repetirse.
- El sistema debe exigir una foto valida con rostro detectable.

## HU-02 Captura de rostro
Como estudiante, quiero capturar mi rostro desde webcam para asociarlo a mi perfil sin usar hardware externo.

Criterios de aceptacion:
- La pagina debe solicitar permisos de camara.
- La captura debe almacenarse temporalmente para su envio al backend.
- Debe mostrarse retroalimentacion clara si la camara falla.

## HU-03 Reconocimiento de ingreso
Como estudiante, quiero ser reconocido al ingresar para registrar asistencia de forma automatica.

Criterios de aceptacion:
- El sistema debe recibir imagen desde webcam.
- Debe comparar contra rostros registrados.
- Si hay coincidencia valida, debe registrar asistencia con fecha y hora.

## HU-04 Consulta de historial
Como administrador academico, quiero consultar el historial de asistencias para monitorear entradas por estudiante.

Criterios de aceptacion:
- El historial debe mostrar fecha/hora, nombre, codigo y programa.
- La consulta debe entregar resultados ordenados de mas reciente a mas antiguo.
- Debe existir opcion de actualizar historial desde la interfaz.
