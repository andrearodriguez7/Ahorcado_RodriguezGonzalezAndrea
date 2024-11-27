import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from Conexion import Conexion


class JuegoAhorcadoConInterfaz:
    def __init__(self, root, conexion):
        self.root = root
        self.conexion = conexion
        self.root.title("Juego del Ahorcado de Andrea")
        self.root.config(bg="#c0e8dd")

        # Establece el tamaño de la ventana principal
        self.root.geometry("600x850")

        # Esto inicia el juego
        self.intentos = 6
        self.palabra = ""
        self.letras_adivinadas = []
        self.tema_seleccionado = None
        self.nombre_jugador = None  # Guardar el nombre del jugador
        self.partidas_jugadas = 0  # Contador de partidas jugadas

        # Crea la interfaz gráfica
        self.crear_widgets()

    def crear_widgets(self):
        # Etiqueta de bienvenida
        self.bienvenida_label = tk.Label(self.root, text="¡Bienvenido al Juego del Ahorcado de Andrea!", font=("Times New Roman", 20), bg="#87ac95")
        self.bienvenida_label.pack(pady=30)

        # Botón para iniciar el juego
        self.iniciar_button = tk.Button(self.root, text="Empezar el juego", command=self.pedir_nombre, font=("Times New Roman", 14), bg="#859f98", fg="white", width=20, height=2)
        self.iniciar_button.pack(pady=20)

        # Etiqueta para mostrar la palabra oculta
        self.palabra_label = tk.Label(self.root, text="", font=("Times New Roman", 16), bg="#f0f0f0")
        self.palabra_label.pack(pady=30)

        # Campo de entrada para la letra
        self.entrada_letra = tk.Entry(self.root, font=("Times New Roman", 16), width=10)
        self.entrada_letra.pack(pady=20)

        # Botón para enviar la letra
        self.adivinacion_button = tk.Button(self.root, text="Adivinar Letra", command=self.adivinar, font=("Times New Roman", 14), bg="#008CBA", fg="white", width=20, height=2)
        self.adivinacion_button.pack(pady=20)

        # Etiqueta para mostrar los intentos restantes
        self.intentos_label = tk.Label(self.root, text="Intentos restantes: 6", font=("Times New Roman", 16), bg="#87ac95")
        self.intentos_label.pack(pady=10)

        # Etiqueta para mostrar la imagen del ahorcado
        self.imagen_label = tk.Label(self.root)
        self.imagen_label.pack(pady=20)

        # Etiqueta para mostrar las partidas jugadas
        self.partidas_label = tk.Label(self.root, text="Partidas jugadas: 0", font=("Times New Roman", 16), bg="#f0f0f0")
        self.partidas_label.pack(pady=20)

    def pedir_nombre(self):
        # Pedir el nombre del jugador antes de iniciar el juego
        def guardar_nombre():
            nombre = entrada_nombre.get().strip()
            if nombre:
                self.nombre_jugador = nombre
                self.partidas_jugadas = self.conexion.obtener_partidas_jugadas(nombre)  # Esto nos permite recuper las partidas jugadas desde la base de datos
                self.conexion.guardar_jugador(nombre)  # Esto nos permite guardar el nombre del jugador en la base de datos
                self.ventana_nombre.destroy()
                self.mostrar_menu_tematicas()
            else:
                messagebox.showerror("Error", "Por favor, ingresa un nombre válido.")

        # Crear una ventana emergente para pedir el nombre
        self.ventana_nombre = tk.Toplevel(self.root)
        self.ventana_nombre.title("Ingresa tu nombre")
        self.ventana_nombre.geometry("400x200")

        # Etiqueta
        etiqueta_nombre = tk.Label(self.ventana_nombre, text="Ingresa tu nombre:", font=("Times New Roman", 14))
        etiqueta_nombre.pack(pady=10)

        # Campo de entrada para el nombre
        entrada_nombre = tk.Entry(self.ventana_nombre, font=("Times New Roman", 14), width=20)
        entrada_nombre.pack(pady=10)

        # Botón para confirmar el nombre
        boton_guardar = tk.Button(self.ventana_nombre, text="Guardar Nombre", command=guardar_nombre, font=("Times New Roman", 14), bg="#617d6b", fg="white", width=20, height=2)
        boton_guardar.pack(pady=20)

    def mostrar_menu_tematicas(self):
        # Mostrar el menú para que el usuario elija la temática
        def tema_seleccionado(tema):
            # Método que configura la temática seleccionada
            self.tema_seleccionado = tema
            self.iniciar_juego()

        # Crear una ventana para elegir la temática
        self.ventana_tematicas = tk.Toplevel(self.root)
        self.ventana_tematicas.title("Elige una temática")
        self.ventana_tematicas.geometry("400x300")

        # Botones para las temáticas
        self.boton_frutas = tk.Button(self.ventana_tematicas, text="Frutas", command=lambda: tema_seleccionado("frutas"), font=("Times New Roman", 16), bg="#c4e5bb", fg="white", width=20, height=2)
        self.boton_frutas.pack(pady=15)

        self.boton_nombres = tk.Button(self.ventana_tematicas, text="Nombres", command=lambda: tema_seleccionado("nombres_personas"), font=("Times New Roman", 16), bg="#a0e08e", fg="white", width=20, height=2)
        self.boton_nombres.pack(pady=15)

        self.boton_conceptos = tk.Button(self.ventana_tematicas, text="Conceptos Informáticos", command=lambda: tema_seleccionado("conceptos_informaticos"), font=("Times New Roman", 16), bg="#6e9961", fg="white", width=20, height=2)
        self.boton_conceptos.pack(pady=15)

    def iniciar_juego(self):
        # Método para comenzar el juego.
        self.intentos = 6
        self.elegir_palabra()
        self.actualizar_pantalla()

    def elegir_palabra(self):
        # Elegir una palabra aleatoria de la temática seleccionada desde la base de datos.
        self.palabra = self.conexion.obtener_palabra_aleatoria(self.tema_seleccionado)
        if self.palabra:
            self.letras_adivinadas = ["_"] * len(self.palabra)
        else:
            messagebox.showerror("Error", "No hay palabras disponibles para esta temática.")
            self.letras_adivinadas = []

    def actualizar_pantalla(self):
        # Actualizar los elementos visuales en la interfaz.
        self.palabra_label.config(text=" ".join(self.letras_adivinadas))
        self.intentos_label.config(text=f"Intentos restantes: {self.intentos}")
        self.partidas_label.config(text=f"Partidas jugadas: {self.partidas_jugadas}")
        self.mostrar_imagen()

    def mostrar_imagen(self):
        # Mostrar la imagen del ahorcado que toque
        try:
            imagen = Image.open(f"intento_{self.intentos}.png")
            imagen = imagen.resize((200, 200))
            self.imagen = ImageTk.PhotoImage(imagen)
            self.imagen_label.config(image=self.imagen)
        except FileNotFoundError:
            self.imagen_label.config(text="Imagen no encontrada.")

    def adivinar(self):
        # Método para manejar la adivinación del jugador.
        letra = self.entrada_letra.get().lower()

        if len(letra) != 1 or not letra.isalpha():
            messagebox.showerror("Error", "Por favor, introduce solo una letra válida.")
            self.entrada_letra.delete(0, tk.END)
            return

        if letra in self.letras_adivinadas:
            messagebox.showwarning("Advertencia", "Ya adivinaste esa letra.")
            self.entrada_letra.delete(0, tk.END)
            return

        if letra in self.palabra:
            for i in range(len(self.palabra)):
                if self.palabra[i] == letra:
                    self.letras_adivinadas[i] = letra
            messagebox.showinfo("¡Bien hecho!", f"La letra '{letra}' está en la palabra.")
        else:
            self.intentos -= 1
            messagebox.showerror("Incorrecto", f"La letra '{letra}' no está en la palabra.")

        self.actualizar_pantalla()

        if "_" not in self.letras_adivinadas:
            messagebox.showinfo("¡Felicidades!", "¡Has adivinado la palabra!")
            self.conexion.guardar_resultado(self.nombre_jugador, self.tema_seleccionado, self.palabra, True)  # Guardamos el resultado
            self.partidas_jugadas += 1
            self.conexion.actualizar_partidas_jugadas(self.nombre_jugador, self.partidas_jugadas)  # Actualizamos las partidas jugadas
            self.iniciar_juego()

        elif self.intentos == 0:
            messagebox.showerror("Perdiste", f"¡Perdiste! La palabra era: {self.palabra}")
            self.conexion.guardar_resultado(self.nombre_jugador, self.tema_seleccionado, self.palabra, False)  # Guardar el resultado
            self.partidas_jugadas += 1
            self.conexion.actualizar_partidas_jugadas(self.nombre_jugador, self.partidas_jugadas)  # Actualizamos las partidas jugadas
            self.iniciar_juego()

        self.entrada_letra.delete(0, tk.END)


if __name__ == "__main__":
    conexion = Conexion()
    conexion.conectar()

    root = tk.Tk()
    juego = JuegoAhorcadoConInterfaz(root, conexion)
    root.mainloop()

    conexion.desconectar()
