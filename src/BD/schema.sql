PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS estudiantes (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	nombre TEXT NOT NULL,
	codigo TEXT NOT NULL UNIQUE,
	programa TEXT NOT NULL,
	rostro_encoding TEXT NOT NULL,
	creado_en TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS asistencias (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	estudiante_id INTEGER NOT NULL,
	fecha_hora TEXT NOT NULL,
	FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id)
);

CREATE INDEX IF NOT EXISTS idx_asistencias_estudiante
	ON asistencias (estudiante_id);

CREATE INDEX IF NOT EXISTS idx_asistencias_fecha
	ON asistencias (fecha_hora DESC);

