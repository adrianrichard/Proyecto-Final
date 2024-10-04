import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Función para calcular la edad
def calcular_edad():
    try:
        # Obtener la fecha ingresada por el usuario
        fecha_nacimiento = datetime.strptime(entry_fecha.get(), "%d-%m-%Y")
        hoy = datetime.today()
        edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

        # Mostrar la edad en la etiqueta
        etiqueta_edad.config(text=f"Tienes {edad} años.")
    except ValueError:
        messagebox.showerror("Error", "Formato de fecha incorrecto. Use AAAA-MM-DD.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Calculadora de Edad")

# Etiqueta y campo de entrada para la fecha de nacimiento
etiqueta_fecha = tk.Label(ventana, text="Fecha de nacimiento (AAAA-MM-DD):")
etiqueta_fecha.pack()

entry_fecha = tk.Entry(ventana)
entry_fecha.pack()

# Botón para calcular la edad
boton_calcular = tk.Button(ventana, text="Calcular Edad", command=calcular_edad)
boton_calcular.pack()

# Etiqueta para mostrar la edad
etiqueta_edad = tk.Label(ventana, text="")
etiqueta_edad.pack()

# Iniciar el bucle principal de la ventana
ventana.mainloop()
otra opción en lugar de usar validatecommand?