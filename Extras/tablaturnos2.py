import tkinter as tk
from tkinter import ttk
from tkinter import *
from datetime import datetime, timedelta
import sqlite3
from tkinter import  messagebox, Frame
from editarturno import Editar

class Turno:
    
    def __init__(self):
        self.ventana_turno = tk.Tk()
        self.ventana_turno.title("Turnos")
        self.ventana_turno.geometry('500x500')
        
        self.widgets()
    
    def abrir_ventana_secundaria(self):
        editar=Editar()
        editar.prueba()
        
    def widgets(self):
        self.frame_tabla = ttk.Frame(self.ventana_turno)
        #self.frame_tabla.grid(column=0,row=1)
        self.frame_tabla.grid(columnspan= 4, row= 0, sticky= 'nsew')
        Label(self.frame_tabla, text="PRUEBA").grid(columnspan= 4,column=0, row=0)
        self.tabla_turnos = ttk.Treeview(self.frame_tabla, columns=("Horario", "Paciente", "Prestacion", "Odontologo"), show='headings', height=20)
        self.tabla_turnos.grid(column=0, row=2, columnspan=4, sticky='nsew')
        # Definir los encabezados de las columnas
        self.tabla_turnos.heading("Horario", text="Horario")
        self.tabla_turnos.heading("Paciente", text="Paciente")
        self.tabla_turnos.heading("Prestacion", text="Prestacion")
        self.tabla_turnos.heading("Odontologo", text="Odontologo")

        # Ajustar el ancho de las columnas
        self.tabla_turnos.column("Horario", width=80)
        self.tabla_turnos.column("Paciente", width=100)
        self.tabla_turnos.column("Prestacion", width=100)
        self.tabla_turnos.column("Odontologo", width=100)
        # cargar filas al Treeview
        start_time = datetime.strptime("08:00", "%H:%M")
        # Intervalo de 30 minutos
        time_interval = timedelta(minutes=30)
        for i in range(1, 21):
            current_time = start_time + i * time_interval
            self.tabla_turnos.insert("", "end", values=(current_time.strftime("%H:%M"), f"Fila {i} Col2", f"Fila {i} Col3", f"Fila {i} Col4"))
        self.tabla_turnos.bind("<Double-1>", self.abrir_ventana_secundaria)
        
        self.ventana_turno.mainloop()
        
    # def crear_BD(self):
    #     self.conn= sqlite3.connect('turnos.db')
    #     self.cur= self.conn.cursor()
    #     self.cur.execute('''
    #         CREATE TABLE IF NOT EXISTS turnos (
    #             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #             nombre TEXT NOT NULL,
    #             fecha DATE NOT NULL,
    #             hora TIME NOT NULL,
    #             paciente TEXT NOT NULL,
    #             prestacion TEXT NOT NULL,
    #             odontologo TEXT NOT NULL
    #         )
    #         ''')
if __name__ == "__main__":
    Turno()       
#     # Insertar datos en la tabla
#     def insertar_turno(self):
#         self.conn= sqlite3.connect('testDB.db')
#         self.cur= self.conn.cursor()
#         self.cur.executemany('''
#             INSERT INTO eventos (nombre, fecha, hora, paciente, prestacion, odontologo)
#             VALUES (?, ?, ?, ?, ?, ?)
#             ''', eventos)
#     # Confirmar los cambios y cerrar la conexión
#         self.conn.commit()
#         self.conn.close()

# def cargar_turnos(self):
#     self.conn= sqlite3.connect('testDB.db')
#     self.cur= self.conn.cursor()
#     # Leer los datos de la tabla
#     self.cur.execute('SELECT * FROM eventos')
#     eventos = self.cur.fetchall()
#     # Mostrar los datos
#     for evento in eventos:
#         print(evento)
#     # Cerrar la conexión
#     self.conn.close()

# def salir(self):
#     editar = Editar()
#     editar.prueba()
#         # answer = messagebox.askokcancel(title='Salir', message='¿Desea salir?', icon='warning')
#         # if answer:
#         #     self.ventana_secundaria.destroy()
# eventos = [
#     ('Evento 1', '2024-05-24', '10:00:00', 'Paciente 1', 'Limpieza', 'Dr. A'),
#     ('Evento 2', '2024-05-25', '11:00:00', 'Paciente 2', 'Extracción', 'Dr. B'),
#     ('Evento 3', '2024-05-26', '12:00:00', 'Paciente 3', 'Ortodoncia', 'Dr. C'),
# ]
# def abrir_ventana_secundaria(self):
#     self.ventana_secundaria = tk.Toplevel(self.root)
#     self.ventana_secundaria.title("Ventana Secundaria")
#     self.ventana_secundaria.grab_set_global() # Obliga a las ventanas estar deshabilitadas y deshabilitar todos los eventos e interacciones con la ventana
#     self.ventana_secundaria.focus_set()
#     # Crear widgets en la ventana secundaria
#     tk.Label(self.ventana_secundaria, text="Esta es la ventana secundaria").grid(column=0, row=0, padx=10, pady=10)
#     tk.Button(self.ventana_secundaria, text="Guardar", command=self.ventana_secundaria.destroy).grid(column=0, row=1,padx=10, pady=10)
#     # Botón para cerrar la ventana secundaria
#     tk.Button(self.ventana_secundaria, text="Cerrar", command=self.salir).grid(column=1, row=1, padx=10, pady=10)

# # Crear la ventana principal
#     self.root = tk.Tk()
#     self.root.title("Turnos")

# # Crear un Frame para contener el Treeview y la barra de desplazamiento
#     self.frame = ttk.Frame(self.root)
#     self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=False)
#     #crear_BD()
# # Crear el Treeview
#     self.tree = ttk.Treeview(self.frame, columns=("Horario", "Paciente", "Prestacion", "Odontologo"), show='headings', height=20)

# # Definir los encabezados de las columnas
#     self.tree.heading("Horario", text="Horario")
#     self.tree.heading("Paciente", text="Paciente")
#     self.tree.heading("Prestacion", text="Prestacion")
#     self.tree.heading("Odontologo", text="Odontologo")

# # Ajustar el ancho de las columnas
#     self.tree.column("Horario", width=100)
#     self.tree.column("Paciente", width=100)
#     self.tree.column("Prestacion", width=100)
#     self.tree.column("Odontologo", width=100)

#     def cargar_tabla(self):
# # cargar filas al Treeview
#         start_time = datetime.strptime("08:00", "%H:%M")
#     # Intervalo de 30 minutos
#         time_interval = timedelta(minutes=30)
#     #tree.delete(*root.get_children())
#         for i in range(1, 21):
#             current_time = start_time + i * time_interval
#             self.tree.insert("", "end", values=(current_time.strftime("%H:%M"), f"Fila {i} Col2", f"Fila {i} Col3", f"Fila {i} Col4"))

# # Crear la barra de desplazamiento vertical
#     scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
#     self.tree.configure(yscroll=scrollbar.set)

# # Ubicar el Treeview y la barra de desplazamiento en el Frame
#     self.tree.grid(row=1, column=0, sticky='nsew', columnspan=4)
#     scrollbar.grid(row=1, column=5, sticky='ns')
#     cargar_tabla()
# # Configurar el Frame para expandir el Treeview y la barra de desplazamiento
#     self.frame.grid_rowconfigure(0, weight=1)
#     self.frame.grid_columnconfigure(0, weight=1)
#     #self.tree.bind("<Double-1>", abrir_ventana_secundaria)
# # Button(frame, text="Agregar turno", bg="#D1D6D3", bd= 2, borderwidth= 2, width=10).grid(row=0, column=0, padx=(10,10), pady=(5,5))
# # Button(frame, text="Eliminar turno", bg="#D1D6D3", bd= 2, borderwidth= 2, width=10).grid(row=0, column=1, padx=(10,10), pady=(5,5))
# # Button(frame, text="Editar turno", bg="#D1D6D3", bd= 2, borderwidth= 2, width=10).grid(row=0, column=2, padx=(10,10), pady=(5,5))
# # Button(frame, text="Salir", bg="orange", bd= 2, borderwidth= 2, width=10).grid(row=0, column=3, padx=(10,10), pady=(5,5))

# # Ejecutar la aplicación
#     self.root.mainloop()
# # def crear_BD():
# #CREAR BASE DE DATOS
