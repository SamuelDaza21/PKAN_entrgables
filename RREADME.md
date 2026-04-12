# Sistema de Registro Biométrico (Facial)

Aplicación web desarrollada en Python que permite registrar la entrada de estudiantes mediante reconocimiento facial.

## Tecnologías
- Python
- Flask
- OpenCV
- face_recognition
- SQLite
- HTML, CSS, JavaScript

## Funcionalidades
- Registro de estudiantes
- Captura de rostro
- Reconocimiento facial
- Registro de asistencia

## Ejecución

```bash
pip install -r requirements.txt
python src/backend/app.py



🧠 Notas IMPORTANTES (esto te salva el proyecto)
🔥 1. face_recognition puede fallar al instalar

En Windows a veces da problemas → solución:

pip install cmake
pip install dlib
pip install face-recognition
🔥 2. NO guardes imágenes directamente

Mejor guarda:

encoding facial (más eficiente)
o ruta de imagen
🔥 3. Flujo REAL que debes implementar
Registro:
cámara → imagen → encoding → guardar
Login:
cámara → encoding → comparar → acceso