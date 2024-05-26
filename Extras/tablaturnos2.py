import tkinter as tk
from tkinter import ttk
from tkinter import *
from datetime import datetime, timedelta
import sqlite3
from tkinter import  messagebox, Frame

def crear_BD():
    conn= sqlite3.connect('turnos.db')
    cur= conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS turnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            fecha DATE NOT NULL,
            hora TIME NOT NULL,
            paciente TEXT NOT NULL,
            prestacion TEXT NOT NULL,
            odontologo TEXT NOT NULL
        )
        ''')
# Insertar datos en la tabla
def insertar_turno():
    conn= sqlite3.connect('testDB.db')
    cur= conn.cursor()
    cur.executemany('''
        INSERT INTO eventos (nombre, fecha, hora, paciente, prestacion, odontologo)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', eventos)
    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

def cargar_turnos():
    conn= sqlite3.connect('testDB.db')
    cur= conn.cursor()
    # Leer los datos de la tabla
    cur.execute('SELECT * FROM eventos')
    eventos = cur.fetchall()
    # Mostrar los datos
    for evento in eventos:
        print(evento)
    # Cerrar la conexión
    conn.close()

def salir(self):
        answer = messagebox.askokcancel(title='Salir', message='¿Desea salir?', icon='warning')
        if answer:
            self.ventana_secundaria.destroy()
eventos = [
    ('Evento 1', '2024-05-24', '10:00:00', 'Paciente 1', 'Limpieza', 'Dr. A'),
    ('Evento 2', '2024-05-25', '11:00:00', 'Paciente 2', 'Extracción', 'Dr. B'),
    ('Evento 3', '2024-05-26', '12:00:00', 'Paciente 3', 'Ortodoncia', 'Dr. C'),
]
def abrir_ventana_secundaria(self):
    ventana_secundaria = tk.Toplevel(root)
    ventana_secundaria.title("Ventana Secundaria")
    ventana_secundaria.grab_set_global() # Obliga a las ventanas estar deshabilitadas y deshabilitar todos los eventos e interacciones con la ventana
    ventana_secundaria.focus_set()
    # Crear widgets en la ventana secundaria
    tk.Label(ventana_secundaria, text="Esta es la ventana secundaria").grid(column=0, row=0, padx=10, pady=10)
    tk.Button(ventana_secundaria, text="Guardar", command=ventana_secundaria.destroy).grid(column=0, row=1,padx=10, pady=10)
    # Botón para cerrar la ventana secundaria
    tk.Button(ventana_secundaria, text="Cerrar", command=salir).grid(column=1, row=1, padx=10, pady=10)

# Crear la ventana principal
root = tk.Tk()
root.title("Turnos")

# Crear un Frame para contener el Treeview y la barra de desplazamiento
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=False)
crear_BD()
# Crear el Treeview
tree = ttk.Treeview(frame, columns=("Horario", "Paciente", "Prestacion", "Odontologo"), show='headings', height=20)

# Definir los encabezados de las columnas
tree.heading("Horario", text="Horario")
tree.heading("Paciente", text="Paciente")
tree.heading("Prestacion", text="Prestacion")
tree.heading("Odontologo", text="Odontologo")

# Ajustar el ancho de las columnas
tree.column("Horario", width=100)
tree.column("Paciente", width=100)
tree.column("Prestacion", width=100)
tree.column("Odontologo", width=100)

def cargar_tabla():
# cargar filas al Treeview
    start_time = datetime.strptime("08:00", "%H:%M")
    # Intervalo de 30 minutos
    time_interval = timedelta(minutes=30)
    #tree.delete(*root.get_children())
    for i in range(1, 21):
        current_time = start_time + i * time_interval
        tree.insert("", "end", values=(current_time.strftime("%H:%M"), f"Fila {i} Col2", f"Fila {i} Col3", f"Fila {i} Col4"))

# Crear la barra de desplazamiento vertical
scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)

# Ubicar el Treeview y la barra de desplazamiento en el Frame
tree.grid(row=1, column=0, sticky='nsew', columnspan=4)
scrollbar.grid(row=1, column=5, sticky='ns')
cargar_tabla()
# Configurar el Frame para expandir el Treeview y la barra de desplazamiento
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
tree.bind("<Double-1>", abrir_ventana_secundaria)
# Button(frame, text="Agregar turno", bg="#D1D6D3", bd= 2, borderwidth= 2, width=10).grid(row=0, column=0, padx=(10,10), pady=(5,5))
# Button(frame, text="Eliminar turno", bg="#D1D6D3", bd= 2, borderwidth= 2, width=10).grid(row=0, column=1, padx=(10,10), pady=(5,5))
# Button(frame, text="Editar turno", bg="#D1D6D3", bd= 2, borderwidth= 2, width=10).grid(row=0, column=2, padx=(10,10), pady=(5,5))
# Button(frame, text="Salir", bg="orange", bd= 2, borderwidth= 2, width=10).grid(row=0, column=3, padx=(10,10), pady=(5,5))

# Ejecutar la aplicación
root.mainloop()
# def crear_BD():
#CREAR BASE DE DATOS
