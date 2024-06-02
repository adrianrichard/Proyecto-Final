import tkinter as tk
from tkinter import ttk
from tkinter import *
from datetime import datetime, timedelta
import sqlite3
from tkinter import  messagebox, Frame
#from editarturno import Editar

class Turno:
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ventana_turno = tk.Tk()
        self.ventana_turno.title("Turnos")
        self.ventana_turno.geometry('450x600')
        
        self.widgets()
    
    def cargar_turnos(self):
        try:
            self.conn= sqlite3.connect('turnos.db')
            self.cur= self.conn.cursor()
            # Leer los datos de la tabla
            self.cur.execute('SELECT * FROM turnos ORDER BY hora')
            turnos_dados = self.cur.fetchall()
            self.conn.close()
        except:
            print('no abre BD')
                
        # Cerrar la conexión
        
        self.tabla_turnos.delete(*self.tabla_turnos.get_children())
                
        start_time = datetime.strptime("08:00", "%H:%M")
        # Intervalo de 30 minutos
        time_interval = timedelta(minutes=30)
        for i in range(0, 25):
            current_time = start_time + i * time_interval
            for turno in turnos_dados:
                if(current_time.strftime("%H:%M") == turno[3]):
                    self.tabla_turnos.tag_configure('anotado', font=("Arial", 10, 'bold'), background="sky blue")
                    self.tabla_turnos.insert("", "end", values=(current_time.strftime("%H:%M"), turno[4], turno[5], turno[6]), tags=('anotado',))                    
            else:
                self.tabla_turnos.insert(parent='', index='end', values=(current_time.strftime("%H:%M"), '', '', ''))
        #return turnos

    # def agregar_turno(self):
    #     print("guardado")
    
    def cancelar_turno(self):
        self.ventana_secundaria.destroy()
        
    def editar_turno(self, event):
        self.ventana_secundaria = tk.Toplevel(self.ventana_turno, background='gray')
        self.ventana_secundaria.title("Ventana Secundaria")
        self.ventana_secundaria.geometry('400x300')
        self.ventana_secundaria.grab_set_global() # Obliga a las ventanas estar deshabilitadas y deshabilitar todos los eventos e interacciones con la ventana
        self.ventana_secundaria.focus_set() # Mantiene el foco cuando se abre la ventana.
        # #print('hola')
        #item = self.tabla_turnos.focus()
        
        self.turno_seleccionado = self.tabla_turnos.selection()[0]
        #print(self.turno_seleccionado)
        self.data = self.tabla_turnos.item(self.turno_seleccionado)
        self.horario = self.data['values'][0]
        self.paciente = self.data['values'][1]
        self.prestacion = self.data['values'][2]
        self.odontologo = self.data['values'][3]
        Label(self.ventana_secundaria, text="EDITAR TURNO", font=("Arial", 15, 'bold'), bg="gray90", width=60).pack(pady=10)
        Label(self.ventana_secundaria, text="FECHA: DD/MM/AAAA   -"+"   HORARIO: "+self.horario, font=("Arial", 10, 'bold'), bg="gray90", width=60).pack()

        self.nombre_entry = Entry(self.ventana_secundaria, justify=CENTER)
        self.nombre_entry.pack(pady=(10,10))        
        self.nombre_entry.insert(0, "Paciente")
        if (self.paciente != ''):
            self.nombre_entry.delete(0, END)
            self.nombre_entry.insert(0, self.paciente)
        self.nombre_entry.focus_set()
        prestaciones = ["Consulta", "Extracción", "Tratamiento de conducto", "Reparación", "Limpieza"]
        self.selector_prestacion = ttk.Combobox(self.ventana_secundaria, state="readonly", values=prestaciones, width=25, justify=CENTER, background="white")
        self.selector_prestacion.pack(pady=8)
        self.selector_prestacion.set("Prestación")
        if (self.prestacion != ''):            
            self.selector_prestacion.set(self.prestacion)
        self.selector_prestacion.bind("<<ComboboxSelected>>", lambda e: self.ventana_secundaria.focus())
        odontologos = ["Militello", "Macua", "Ramirez"]
        self.selector_odontologo= ttk.Combobox(self.ventana_secundaria, state="readonly", values=odontologos, width=25, justify=CENTER, background="white")
        self.selector_odontologo.pack(pady=8)
        self.selector_odontologo.set("Odontólogo")
        if (self.odontologo != ''):            
            self.selector_odontologo.set(self.odontologo)
        self.selector_odontologo.bind("<<ComboboxSelected>>", lambda e: self.ventana_secundaria.focus())
      
             
        
        self.button_frame = Frame(self.ventana_secundaria, bg="gray")
        self.button_frame.pack(pady=10)
        
        Button(self.button_frame, text='confirm', command=self.guardar_turno, bg="#BDC1BE").grid(row=0, column=0, padx=10)
        Button(self.button_frame, text='cancelar',  command=self.cancelar_turno, bg="#BDC1BE").grid(row=0, column=1, padx = 10)
        
    def guardar_turno(self):
        #print(self.valores)
        self.valores = {
            "paciente": self.nombre_entry.get(),
            "horario": self.horario,
            "prestacion": self.selector_prestacion.get(),
            "odontologo": self.selector_odontologo.get()
        }   
        style = ttk.Style()
        if self.valores["paciente"] == "Paciente" or self.valores["prestacion"] == "Prestación" or self.valores["odontologo"] == "Odontologo":
            style.configure("TCombobox", fieldbackground="red", background="white")
            self.nombre_entry.configure(bg="red")
            self.aviso = Label(self.button_frame, text="Complete la información", bg="#BDC1BE", fg="red", font="Helvetica 10")
            self.aviso.grid(pady=10,row=1, column=0, columnspan=2, padx = 10)
        else:
            print('datos completos')    

        # """ Reconfigure red zones if triggered """
        # self.nombre_entry.configure(bg="white")
        # style.configure("TCombobox", fieldbackground="white", background="white")    
        # tiempo_frame = Frame(self.ventana_secundaria)
        # tiempo_frame.pack(pady=8)

        # horas = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        # self.selector_hora = ttk.Combobox(tiempo_frame, values=horas, state="readonly", justify=CENTER, background="white", width=10)
        # self.selector_hora.set("Hora")
        # self.selector_hora.grid(row=0, column=0)

        # minutos = ["00","30"]
        # #minutos.extend([str(num * 10) for num in range(1, 6)])
        # self.selector_minuto = ttk.Combobox(tiempo_frame, state="readonly", values=minutos, justify=CENTER, background="white", width=10)
        # self.selector_minuto.set("00")
        # self.selector_minuto.grid(row=0, column=1, sticky=E)
        # self.selector_hora.bind("<<ComboboxSelected>>", lambda e: self.ventana_secundaria.focus())
        # self.selector_minuto.bind("<<ComboboxSelected>>", lambda e: self.ventana_secundaria.focus())
        
        
        
        #valores = self.data['values'] #VALORES DE LA TABLA
        #
        #self.tabla_turnos.item(selected_item, text="blub", values=(valores[0], "Pedro", "Pedro", "Pedro"))
        #print(valores)
        #editar=Editar()
        #editar.prueba(valores)
        
    def widgets(self):
        self.frame_tabla = ttk.Frame(self.ventana_turno)
        #self.frame_tabla.grid(column=0,row=1)
        self.frame_tabla.grid(columnspan= 4, row= 0, sticky= 'nsew')
        Label(self.frame_tabla, text="TURNOS", font=('Helvetica', 10, 'bold')).grid(columnspan= 4, column= 0, row= 0, pady=5)
        
        self.tabla_turnos = ttk.Treeview(self.frame_tabla, columns= ("Horario", "Paciente", "Prestacion", "Odontologo"), show= 'headings', height=27, selectmode ='browse')
        self.tabla_turnos.grid(column= 0, row= 2, columnspan= 4, sticky= 'nsew')
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure a new Treeview Heading style
        self.style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'), background="gray")
        self.style.configure("Treeview",            
            foreground="black",
            rowheight=20
            )
        
        # Change selected color
        self.style.map('Treeview', background=[('selected', 'green')])

        # Definir los encabezados de las columnas
        self.tabla_turnos.heading("Horario", text= "Horario")
        self.tabla_turnos.heading("Paciente", text= "Paciente")
        self.tabla_turnos.heading("Prestacion", text= "Prestacion")
        self.tabla_turnos.heading("Odontologo", text= "Odontologo")

        # Ajustar el ancho de las columnas
        self.tabla_turnos.column("Horario", width= 80)
        self.tabla_turnos.column("Paciente", width= 100)
        self.tabla_turnos.column("Prestacion", width= 100)
        self.tabla_turnos.column("Odontologo", width= 100)
        
        # cargar filas al Treeview
        self.cargar_turnos()        
        self.tabla_turnos.bind("<Double-1>", self.editar_turno)
       #self.frame_tabla.grid_columnconfigure(0, weight=1)
        
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
