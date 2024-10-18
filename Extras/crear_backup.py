import sqlite3
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import os

def conectar():
    db = sqlite3.connect('testDB.db')
    cur = db.cursor()
    return db.cursor()

def crear_backup():
    print('prueba')
    db = sqlite3.connect('testDB.db')
    cur = db.cursor()
    query="insert into * from listaBD"
    cur.execute(query)

def listar_BD():
    db = sqlite3.connect('testDB.db')
    cur = db.cursor()
    cur.execute("select * from listaBD")
    lista_BD=cur.fetchall()
    #print('listaBD',lista_BD)

    for row in tabla.get_children():
        tabla.delete(row)
    for _, base_datos in enumerate(lista_BD):
            tabla.insert("", "end", values=(base_datos[1], base_datos[2]))

ventana = tk.Tk()
ventana.title("Gestión de Base de Datos")
ventana.geometry("500x400")
#cursor=conectar()
# # Etiqueta para la ruta de la base de datos
# label_ruta = tk.Label(ventana, text="Ruta de la base de datos:")
# label_ruta.pack(pady=10)

# # Campo de entrada para mostrar la ruta seleccionada
# entry_ruta = tk.Entry(ventana, width=50)
# entry_ruta.pack(padx=10)

# Botón para listar las bases de datos en una carpeta
btn_listar_bd = tk.Button(ventana, text="Listar bases de datos en carpeta", command=listar_BD)
btn_listar_bd.pack(pady=5)

# Tabla para mostrar las bases de datos encontradas
tabla = ttk.Treeview(ventana, columns=("Nombre", "Fecha"), show="headings", height=5)
#tabla.heading("ID", text="ID")
tabla.heading("Nombre", text="Nombre BD")
tabla.heading("Fecha", text="Fecha de creación")
#tabla.column("Carpeta", width=200)  # Ajustar ancho de columna de carpeta
tabla.pack(padx=10, pady=10)

# Bind para seleccionar la base de datos desde la tabla al hacer doble clic
#tabla.bind("<Double-1>", seleccionar_desde_tabla)

# Botón para guardar una copia de la base de datos
btn_guardar_copia = tk.Button(ventana, text="Crear copia de seguridad", command= crear_backup)
btn_guardar_copia.pack(pady=5)

# Botón para cargar la base de datos
#btn_cargar_bd = tk.Button(ventana, text="Cargar base de datos", command=ejecutar_cargar_bd)
#btn_cargar_bd.pack(pady=5)

# Iniciar el loop principal de la interfaz

ventana.mainloop()
    

    
    # #Insertar las bases de datos en la tabla
    # for idx, base_datos in enumerate(bases_datos):
    #     tabla.insert("", "end", values=(idx+1, base_datos, carpeta_origen))

    