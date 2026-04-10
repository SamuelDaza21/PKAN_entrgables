# Reflexión XP — Lista de Tareas

## ¿Qué ventajas encontramos en XP?

1. **Feedback rápido (TDD):** Escribir pruebas antes de codificar nos obligó a pensar en los casos borde desde el principio. Descubrimos errores de lógica antes de terminar el código de producción.

2. **Código simple:** El principio *"lo más simple que funcione"* nos evitó agregar funcionalidades innecesarias. La arquitectura resultó limpia y fácil de mantener.

3. **Programación en parejas:** Trabajar en equipo (Samuel + Jayber) permitió que los errores se detectaran en tiempo real. El "piloto" codificaba mientras el "copiloto" revisaba la lógica y los estándares.

4. **Integración continua:** Los commits frecuentes hicieron que el repositorio siempre estuviera en un estado funcional, sin grandes "merges de terror".

5. **Iteraciones cortas:** Dividir el trabajo en dos iteraciones (CRUD básico → persistencia + UI) nos permitió entregar valor incremental y ajustar prioridades.

## ¿Qué dificultades tuvimos?

1. **Configurar el entorno de pruebas:** Aislar cada test con una base de datos temporal requirió entender cómo pasar `ruta_bd` a los métodos del modelo, lo cual tomó tiempo al inicio.

2. **Mantener el diseño simple:** La tentación de agregar más funcionalidades (filtros, prioridades, fechas límite) fue constante. Tuvimos que recordarnos el principio YAGNI (*You Aren't Gonna Need It*).

3. **Coordinar los commits:** Al trabajar en paralelo hubo momentos en que los cambios se solapaban. Las convenciones de mensajes de commit ayudaron a mantener el historial ordenado.

4. **Tiempo:** La entrega en 24 horas forzó priorizar las historias de mayor valor y posponer mejoras estéticas.

## ¿Cómo mejoraríamos el proceso?

1. **Más iteraciones:** Con más tiempo haríamos al menos 3–4 ciclos XP, añadiendo funcionalidades como filtros por estado, búsqueda y fechas límite.

2. **CI/CD real:** Configurar GitHub Actions para ejecutar las pruebas automáticamente en cada push, garantizando que el código en `main` siempre esté verde.

3. **Refactoring continuo:** Algunas funciones del modelo podrían refactorizarse para compartir la lógica de conexión más eficientemente.

4. **Pruebas end-to-end:** Agregar pruebas con Playwright o Selenium para validar la interfaz HTML completa, no solo los endpoints de la API.

5. **Retrospectivas formales:** Al finalizar cada iteración, documentar qué salió bien, qué salió mal y qué cambiamos, como dicta el proceso XP.

---

*Desarrollado por Samuel Daza & Jayber — Taller de Metodología XP*
