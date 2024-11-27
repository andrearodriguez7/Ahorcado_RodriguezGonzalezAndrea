import mysql.connector
from mysql.connector import Error
import random

class Conexion:
    def __init__(self):
        self.host = "localhost"
        self.database = "Ahorcado"
        self.user = "root"
        self.password = ""
        self.connection = None

    def conectar(self):
        # Esto nos permite conectar a la base de datos.
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Conexión exitosa a la base de datos.")
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def desconectar(self):
        # Esto nos permite desconectar de la base de datos.
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada.")

    def obtener_palabras(self, categoria):
        # Obtenemos las palabras de la base de datos según la categoría seleccionada.
        if not self.connection or not self.connection.is_connected():
            print("No hay conexión activa.")
            return []

        cursor = self.connection.cursor()
        query = "SELECT nombre FROM tematicas WHERE categoria = %s"
        try:
            cursor.execute(query, (categoria,))
            palabras = [row[0] for row in cursor.fetchall()]
            return palabras
        except Error as e:
            print(f"Error al obtener palabras: {e}")
            return []

    def guardar_jugador(self, nombre):
        # Guardamos un nuevo jugador en la base de datos, solo si no existe.
        if not self.connection or not self.connection.is_connected():
            print("No hay conexión activa.")
            return

        cursor = self.connection.cursor()
        # Verificamos si el jugador ya existe
        query_check = "SELECT id FROM usuario WHERE nombre = %s"
        cursor.execute(query_check, (nombre,))
        if cursor.fetchone():
            print(f"El jugador {nombre} ya existe en la base de datos.")
            return  # No guardamos si el jugador ya existe

        query = "INSERT INTO usuario (nombre, partidas_jugadas) VALUES (%s, %s)"
        try:
            cursor.execute(query, (nombre, 0))  # Guardamos el jugador con 0 partidas jugadas
            self.connection.commit()
            print(f"Jugador {nombre} guardado.")
        except Error as e:
            print(f"Error al guardar jugador: {e}")

    def obtener_id_jugador(self, nombre):
        # Obtenemos el ID del jugador según su nombre.
        if not self.connection or not self.connection.is_connected():
            print("No hay conexión activa.")
            return None

        cursor = self.connection.cursor()
        query = "SELECT id FROM usuario WHERE nombre = %s"
        try:
            cursor.execute(query, (nombre,))
            jugador_id = cursor.fetchone()
            return jugador_id[0] if jugador_id else None
        except Error as e:
            print(f"Error al obtener el ID del jugador: {e}")
            return None

    def obtener_partidas_jugadas(self, nombre):
        # Obtenemos el número de partidas jugadas de un jugador.
        if not self.connection or not self.connection.is_connected():
            print("No hay conexión activa.")
            return 0

        cursor = self.connection.cursor()
        query = "SELECT partidas_jugadas FROM usuario WHERE nombre = %s"
        try:
            cursor.execute(query, (nombre,))
            partidas = cursor.fetchone()
            return partidas[0] if partidas else 0
        except Error as e:
            print(f"Error al obtener partidas jugadas: {e}")
            return 0

    def actualizar_partidas_jugadas(self, nombre, partidas_jugadas):
        # Actualizamos el número de partidas jugadas de un jugador.
        if not self.connection or not self.connection.is_connected():
            print("No hay conexión activa.")
            return

        cursor = self.connection.cursor()
        query = "UPDATE usuario SET partidas_jugadas = %s WHERE nombre = %s"
        try:
            cursor.execute(query, (partidas_jugadas, nombre))
            self.connection.commit()
            print(f"Partidas jugadas de {nombre} actualizadas a {partidas_jugadas}.")
        except Error as e:
            print(f"Error al actualizar partidas jugadas: {e}")

    def guardar_resultado(self, nombre_jugador, tema, palabra, gano):
        # Guardamos el resultado de la partida con el nombre del jugador.
        if not self.connection or not self.connection.is_connected():
            print("No hay conexión activa.")
            return

        # Primero obtenemos el ID del jugador
        jugador_id = self.obtener_id_jugador(nombre_jugador)
        if not jugador_id:
            print(f"No se pudo encontrar el ID del jugador {nombre_jugador}.")
            return

        cursor = self.connection.cursor()
        query = "INSERT INTO resultados (id_jugador, tema, palabra, gano) VALUES (%s, %s, %s, %s)"
        try:
            cursor.execute(query, (jugador_id, tema, palabra, gano))
            self.connection.commit()
            print(f"Resultado guardado para el jugador {nombre_jugador}.")
        except Error as e:
            print(f"Error al guardar resultado: {e}")

    def obtener_estadisticas(self, nombre):
        # Obtenemos estadísticas de partidas de un jugador.
        if not self.connection or not self.connection.is_connected():
            print("No hay conexión activa.")
            return

        cursor = self.connection.cursor()
        query = """
            SELECT nombre, 
                   SUM(CASE WHEN gano = TRUE THEN 1 ELSE 0 END) AS ganadas,
                   SUM(CASE WHEN gano = FALSE THEN 1 ELSE 0 END) AS perdidas
            FROM usuario
            LEFT JOIN resultados ON usuario.id = resultados.id_jugador
            WHERE nombre = %s
            GROUP BY nombre
        """
        cursor.execute(query, (nombre,))
        stats = cursor.fetchone()
        if stats:
            print(f"Jugador: {stats[0]} - Ganadas: {stats[1]} - Perdidas: {stats[2]}")
        else:
            print("Jugador no encontrado.")

    def obtener_palabra_aleatoria(self, categoria):
        # Obtenemos una palabra aleatoria de la categoría seleccionada.
        palabras = self.obtener_palabras(categoria)
        if palabras:
            return random.choice(palabras).lower()
        else:
            print("No hay palabras disponibles para esta categoría.")
            return None




