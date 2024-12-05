CREATE DATABASE Ahorcado;
USE Ahorcado;

-- Tabla usuario
CREATE TABLE IF NOT EXISTS usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);
drop table usuario;
ALTER TABLE usuario ADD COLUMN partidas_jugadas INT DEFAULT 0;


-- Tabla resultados
CREATE TABLE resultados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_jugador INT, 
    tema VARCHAR(255),
    palabra VARCHAR(255),
    gano BOOLEAN,
    FOREIGN KEY (id_jugador) REFERENCES usuario(id) 
);
drop table resultados;

-- Tabla partidas
CREATE TABLE partidas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jugador_id INT,
    resultado VARCHAR(50),
    FOREIGN KEY (jugador_id) REFERENCES usuario(id)
);
drop table partidas;

-- Tabla tematicas
CREATE TABLE IF NOT EXISTS tematicas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    categoria ENUM('frutas', 'nombres_personas', 'conceptos_informaticos') NOT NULL
);
drop table tematicas;

-- Insertar registros en tabla tematicas con las tres categorías
-- Frutas
INSERT INTO tematicas (nombre, categoria) VALUES
    ('mango', 'frutas'),
    ('platano', 'frutas'),
    ('fresa', 'frutas'),
    ('kiwi', 'frutas'),
    ('sandia', 'frutas'),
    ('naranja', 'frutas'),
    ('melon', 'frutas'),
    ('pera', 'frutas'),
    ('cereza', 'frutas'),
    ('uva', 'frutas');

-- Nombres de personas
INSERT INTO tematicas (nombre, categoria) VALUES
    ('andrea', 'nombres_personas'),
    ('david', 'nombres_personas'),
    ('lucas', 'nombres_personas'),
    ('sara', 'nombres_personas'),
    ('antonio', 'nombres_personas'),
    ('claudia', 'nombres_personas'),
    ('daniel', 'nombres_personas'),
    ('helena', 'nombres_personas'),
    ('marco', 'nombres_personas'),
    ('diogenes', 'nombres_personas');

-- Conceptos informáticos
INSERT INTO tematicas (nombre, categoria) VALUES
    ('python', 'conceptos_informaticos'),
    ('algoritmo', 'conceptos_informaticos'),
    ('variable', 'conceptos_informaticos'),
    ('funcion', 'conceptos_informaticos'),
    ('compilador', 'conceptos_informaticos'),
    ('depuracion', 'conceptos_informaticos'),
    ('bucle', 'conceptos_informaticos'),
    ('estructura de datos', 'conceptos_informaticos'),
    ('base de datos', 'conceptos_informaticos'),
    ('framework', 'conceptos_informaticos');

-- Consultas para ver el contenido
SELECT * FROM tematicas;
SELECT * FROM resultados;
SELECT * FROM partidas;

-- Consulta para poder ver a los jugadores
SELECT u.nombre AS nombre_jugador, r.tema, r.palabra, r.gano
FROM resultados r
JOIN usuario u ON r.id_jugador = u.id;

