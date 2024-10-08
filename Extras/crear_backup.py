import sqlite3
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

# Función para guardar una copia de la base de datos con la fecha actual en el nombre
def guardar_copia_bd(ruta_origen):
    try:
        # Obtener la fecha actual en formato YYYYMMDD
        fecha_actual = datetime.now().strftime("%Y%m%d")

        # Crear el nombre del archivo de la copia con la fecha
        ruta_copia = f"{ruta_origen.split('.')[0]}_copia_{fecha_actual}.db"

        # Hacer la copia del archivo
        shutil.copy(ruta_origen, ruta_copia)

        messagebox.showinfo("Éxito", f"Copia de seguridad guardada como: {ruta_copia}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar la copia de seguridad: {e}")

# Función para cargar una base de datos SQLite
def cargar_base_datos(ruta_bd):
    try:
        # Crear una conexión a la base de datos
        conn = sqlite3.connect(ruta_bd)
        messagebox.showinfo("Éxito", f"Base de datos '{ruta_bd}' cargada correctamente.")
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al cargar la base de datos: {e}")

# Función para abrir un cuadro de diálogo para seleccionar un archivo de base de datos
def seleccionar_archivo():
    archivo = filedialog.askopenfilename(
        title="Seleccionar base de datos",
        filetypes=(("Archivos SQLite", "*.db"), ("Todos los archivos", "*.*"))
    )
    if archivo:
        entry_ruta.delete(0, tk.END)
        entry_ruta.insert(0, archivo)

# Función que llama a guardar la copia
def ejecutar_guardar_copia():
    ruta_bd = entry_ruta.get()
    if ruta_bd:
        guardar_copia_bd(ruta_bd)
    else:
        messagebox.showwarning("Advertencia", "Debe seleccionar una base de datos primero.")

# Función que llama a cargar la base de datos
def ejecutar_cargar_bd():
    ruta_bd = entry_ruta.get()
    if ruta_bd:
        cargar_base_datos(ruta_bd)
    else:
        messagebox.showwarning("Advertencia", "Debe seleccionar una base de datos primero.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Gestión de Base de Datos")
ventana.geometry("400x200")

# Etiqueta para la ruta de la base de datos
label_ruta = tk.Label(ventana, text="Ruta de la base de datos:")
label_ruta.pack(pady=10)

# Campo de entrada para mostrar la ruta seleccionada
entry_ruta = tk.Entry(ventana, width=50)
entry_ruta.pack(padx=10)

# Botón para seleccionar la base de datos
btn_seleccionar = tk.Button(ventana, text="Seleccionar base de datos", command=seleccionar_archivo)
btn_seleccionar.pack(pady=5)

# Botón para guardar una copia de la base de datos
btn_guardar_copia = tk.Button(ventana, text="Guardar copia de seguridad", command=ejecutar_guardar_copia)
btn_guardar_copia.pack(pady=5)

# Botón para cargar la base de datos
btn_cargar_bd = tk.Button(ventana, text="Cargar base de datos", command=ejecutar_cargar_bd)
btn_cargar_bd.pack(pady=5)

# Iniciar el loop principal de la interfaz
ventana.mainloop()
