// index.js
const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');
require('dotenv').config();
// Capturar errores globales para evitar que Node se cierre sin avisar
process.on('unhandledRejection', (reason, promise) => {
  console.error(' Promesa no manejada:', reason);
});
process.on('uncaughtException', (err) => {
  console.error(' Excepción no capturada:', err);
});


// Crear la aplicación Express
const app = express();
const PORT = process.env.PORT || 3000;

// Middlewares
app.use(cors()); // Permite peticiones desde otros dominios
app.use(express.json()); // Permite recibir datos en formato JSON

// Configuración de la conexión a la base de datos
const connection = mysql.createConnection({
  host: 'metro.proxy.rlwy.net',
  user: 'root',
  password: 'lqKfOsuasKPBmoicqdirzbeQJFxDWbzn',
  database: 'railway',
  port: 39110
});

// Conectar a la base de datos
connection.connect((err) => {
  if (err) {
    console.error(' desde api.js Error conectando a la base de datos:', err);
    return;
  }
  console.log(' Conectado a la base de datos MySQL');
});

// Mapa de claves primarias según la tabla
const primaryKeys = {
  usuarios: "ID_usuario",
  sesiones: "ID_sesion",
  configuraciones: "ID_config",
  juegos: "ID_juego",
  resultados: "ID_resultado",
  grados: "ID_grado",
  acciones: "ID_Accion",
  historial_resultados:"id"
};

// -------------------- RUTAS DE LA API --------------------

// Ruta de prueba
app.get('/', (req, res) => {
  res.json({ mensaje: '¡API funcionando correctamente!' });
});

// Obtener todos los registros de una tabla
app.get('/api/:tabla', (req, res) => {
  const tabla = req.params.tabla;

  connection.query(`SELECT * FROM ${tabla}`, (error, results) => {
    if (error) {
      return res.status(500).json({ error: error.message });
    }
    res.json(results);
  });
});

// Obtener un registro específico por ID
app.get('/api/:tabla/:id', (req, res) => {
  const { tabla, id } = req.params;
  const pk = primaryKeys[tabla] || "id";

  connection.query(`SELECT * FROM ${tabla} WHERE ${pk} = ?`, [id], (error, results) => {
    if (error) {
      return res.status(500).json({ error: error.message });
    }

    if (results.length === 0) {
      return res.status(404).json({ mensaje: 'Registro no encontrado' });
    }

    res.json(results[0]);
  });
});

// Crear un nuevo registro
app.post('/api/:tabla', (req, res) => {
  const tabla = req.params.tabla;
  const datos = req.body;

  //Verificación especial para la tabla "sesiones"
  if (tabla === 'sesiones') {
    const { ID_usuario } = datos;

    if (!ID_usuario) {
      return res.status(400).json({ error: 'Falta ID_usuario' });
    }

    // Verificar si ya existe una sesión para ese usuario
    connection.query(
      'SELECT * FROM sesiones WHERE ID_usuario = ?',
      [ID_usuario],
      (error, results) => {
        if (error) {
          return res.status(500).json({ error: error.message });
        }

        if (results.length > 0) {
          //  Ya existe una sesión, devolvemos la existente
          return res.json({
            mensaje: 'Sesión ya existente',
            id: results[0].ID_sesion
          });
        }

        //  Si no hay sesión, se crea una nueva
        const campos = Object.keys(datos).join(', ');
        const valores = Object.values(datos);
        const placeholders = valores.map(() => '?').join(', ');

        connection.query(
          `INSERT INTO ${tabla} (${campos}) VALUES (${placeholders})`,
          valores,
          (error, results) => {
            if (error) {
              return res.status(500).json({ error: error.message });
            }
            res.json({
              mensaje: 'Sesión creada exitosamente',
              id: results.insertId
            });
          }
        );
      }
    );

    return; // Importante: evita seguir al bloque genérico
  }

  // 🧩 Bloque genérico para otras tablas
  const campos = Object.keys(datos).join(', ');
  const valores = Object.values(datos);
  const placeholders = valores.map(() => '?').join(', ');

  connection.query(
    `INSERT INTO ${tabla} (${campos}) VALUES (${placeholders})`,
    valores,
    (error, results) => {
      if (error) {
        return res.status(500).json({ error: error.message });
      }
      res.json({
        mensaje: 'Registro creado exitosamente',
        id: results.insertId
      });
    }
  );
});

// Actualizar un registro
app.put('/api/:tabla/:id', (req, res) => {
  const { tabla, id } = req.params;
  const datos = req.body;
  const pk = primaryKeys[tabla] || "id";

  const campos = Object.keys(datos).map(campo => `${campo} = ?`).join(', ');
  const valores = Object.values(datos);

  connection.query(
    `UPDATE ${tabla} SET ${campos} WHERE ${pk} = ?`,
    [...valores, id],
    (error, results) => {
      if (error) {
        return res.status(500).json({ error: error.message });
      }

      if (results.affectedRows === 0) {
        return res.status(404).json({ mensaje: 'Registro no encontrado' });
      }

      res.json({ mensaje: 'Registro actualizado exitosamente' });
    }
  );
});

// Eliminar un registro
app.delete('/api/:tabla/:id', (req, res) => {
  const { tabla, id } = req.params;
  const pk = primaryKeys[tabla] || "id";

  connection.query(
    `DELETE FROM ${tabla} WHERE ${pk} = ?`,
    [id],
    (error, results) => {
      if (error) {
        return res.status(500).json({ error: error.message });
      }

      if (results.affectedRows === 0) {
        return res.status(404).json({ mensaje: 'Registro no encontrado' });
      }

      res.json({ mensaje: 'Registro eliminado exitosamente' });
    }
  );
});

// -------------------- Manejo de errores --------------------
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Algo salió mal en el servidor' });
});

// Ruta no encontrada
app.use((req, res) => {
  res.status(404).json({ error: 'Ruta no encontrada' });
});

// Iniciar el servidor
app.listen(PORT, () => {
  console.log(`🚀 Servidor ejecutándose en http://localhost:${PORT}`);
});
