import sqlite3
import shutil
import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# Función para guardar una copia de la base de datos con la fecha actual en el nombre
def guardar_copia_bd(ruta_origen):
    try:
        fecha_actual = datetime.now().strftime("%Y%m%d")
        base_nombre = f"{ruta_origen.split('.')[0]}_copia_{fecha_actual}"
        ruta_copia = f"{base_nombre}.db"

        # Verificar si el archivo ya existe y agregar un número incremental
        contador = 1
        while os.path.exists(ruta_copia):
            ruta_copia = f"{base_nombre}_{contador}.db"
            contador += 1

        # Hacer la copia del archivo
        shutil.copy(ruta_origen, ruta_copia)

        messagebox.showinfo("Éxito", f"Copia de seguridad guardada como: {ruta_copia}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar la copia de seguridad: {e}")

# Función para cargar una base de datos SQLite
def cargar_base_datos(ruta_bd):
    try:
        with sqlite3.connect(ruta_bd) as conn:
            messagebox.showinfo("Éxito", f"Base de datos '{ruta_bd}' cargada correctamente.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al cargar la base de datos: {e}")

# Función que llama a cargar la base de datos desde la tabla seleccionada
def ejecutar_cargar_bd():
    ruta_bd = entry_ruta.get()
    if ruta_bd and os.path.exists(ruta_bd):
        cargar_base_datos(ruta_bd)
    else:
        messagebox.showwarning("Advertencia", "Debe seleccionar una base de datos válida desde la tabla.")

# Función para listar todas las bases de datos en la carpeta de origen y mostrarlas en una tabla
def listar_bases_datos():
    carpeta_origen = filedialog.askdirectory(title="Seleccionar carpeta")
    if carpeta_origen:
        bases_datos = [f for f in os.listdir(carpeta_origen) if f.endswith(".db")]
        
        # Limpiar la tabla si ya tiene datos
        for row in tabla.get_children():
            tabla.delete(row)
        
        # Insertar las bases de datos en la tabla
        for idx, base_datos in enumerate(bases_datos):
            tabla.insert("", "end", values=(idx+1, base_datos, carpeta_origen))

        if not bases_datos:
            messagebox.showinfo("Información", "No se encontraron bases de datos en la carpeta seleccionada.")

# Función para seleccionar la base de datos desde la tabla
def seleccionar_desde_tabla(event):
    selected_item = tabla.selection()
    if selected_item:
        item = tabla.item(selected_item)
        base_datos = item['values'][1]  # Obtener el nombre de la base de datos
        carpeta_origen = item['values'][2]  # Obtener la ruta de la carpeta de la base de datos
        ruta_bd = os.path.join(carpeta_origen, base_datos)
        entry_ruta.delete(0, tk.END)
        entry_ruta.insert(0, ruta_bd)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Gestión de Base de Datos")
ventana.geometry("500x400")

# Etiqueta para la ruta de la base de datos
label_ruta = tk.Label(ventana, text="Ruta de la base de datos:")
label_ruta.pack(pady=10)

# Campo de entrada para mostrar la ruta seleccionada
entry_ruta = tk.Entry(ventana, width=50)
entry_ruta.pack(padx=10)

# Botón para listar las bases de datos en una carpeta
btn_listar_bd = tk.Button(ventana, text="Listar bases de datos en carpeta", command=listar_bases_datos)
btn_listar_bd.pack(pady=5)

# Tabla para mostrar las bases de datos encontradas
tabla = ttk.Treeview(ventana, columns=("ID", "Nombre", "Carpeta"), show="headings", height=5)
tabla.heading("ID", text="ID")
tabla.heading("Nombre", text="Nombre de la Base de Datos")
tabla.heading("Carpeta", text="Carpeta de Origen")
tabla.column("Carpeta", width=200)  # Ajustar ancho de columna de carpeta
tabla.pack(padx=10, pady=10)

# Bind para seleccionar la base de datos desde la tabla al hacer doble clic
tabla.bind("<Double-1>", seleccionar_desde_tabla)

# Botón para guardar una copia de la base de datos
btn_guardar_copia = tk.Button(ventana, text="Guardar copia de seguridad", command=lambda: guardar_copia_bd(entry_ruta.get()))
btn_guardar_copia.pack(pady=5)

# Botón para cargar la base de datos
btn_cargar_bd = tk.Button(ventana, text="Cargar base de datos", command=ejecutar_cargar_bd)
btn_cargar_bd.pack(pady=5)

# Iniciar el loop principal de la interfaz
ventana.mainloop()
