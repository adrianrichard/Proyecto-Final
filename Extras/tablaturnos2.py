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
        self.ventana_turno.geometry('600x600')
        self.sin_turno = True
        self.widgets()

    def cargar_turnos(self):
        try:
            self.conn= sqlite3.connect('turnos.db')
            self.cur= self.conn.cursor()
            # Leer los datos de la tabla
            self.cur.execute('SELECT * FROM turno ORDER BY hora')
            self.turnos_dados = self.cur.fetchall()
            #print(self.turnos_dados[0])
            self.conn.close()
        except:
            print('no hay turnos')            

        # Cerrar la conexión

        self.tabla_turnos.delete(*self.tabla_turnos.get_children())

        start_time = datetime.strptime("08:00", "%H:%M")
        # Intervalo de 30 minutos
        time_interval = timedelta(minutes=30)
        self.j=0
        for i in range(0, 25):
            current_time = start_time + i * time_interval
            #for turno in turnos_dados:
            if self.turnos_dados:
                if(current_time.strftime("%H:%M") == self.turnos_dados[self.j][1] and self.j < len(self.turnos_dados)):
                    self.tabla_turnos.tag_configure('anotado', font=("Arial", 10, 'bold'), background="sky blue")
                    self.tabla_turnos.insert("", "end", values=(current_time.strftime("%H:%M"), self.turnos_dados[self.j][2], self.turnos_dados[self.j][3], self.turnos_dados[self.j][4]), tags=('anotado',))
                    if(self.j+1 < len(self.turnos_dados)):
                        self.j=self.j+1
                else:                
                    self.tabla_turnos.insert(parent='', index='end', values=(current_time.strftime("%H:%M"), '', '', ''))
            else:                
                self.tabla_turnos.insert(parent='', index='end', values=(current_time.strftime("%H:%M"), '', '', ''))

    def cancelar_turno(self):
        self.ventana_secundaria.destroy()

    def editar_turno(self, event):
        self.ventana_secundaria = tk.Toplevel(self.ventana_turno, background='gray')
        self.ventana_secundaria.title("Ventana Secundaria")
        self.ventana_secundaria.geometry('400x300')
        self.ventana_secundaria.grab_set_global() # Obliga a las ventanas estar deshabilitadas y deshabilitar todos los eventos e interacciones con la ventana
        self.ventana_secundaria.focus_set() # Mantiene el foco cuando se abre la ventana.
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
        prestaciones = ["CONSULTA", "EXTRACCIÓN", "TRATAMIENTO DE CONDUCTO", "LIMPIEZA"]
        self.selector_prestacion = ttk.Combobox(self.ventana_secundaria, state="readonly", values=prestaciones, width=25, justify=CENTER, background="white")
        self.selector_prestacion.pack(pady=8)
        self.selector_prestacion.set("Prestación")
        if (self.prestacion != ''):
            self.selector_prestacion.set(self.prestacion)
        self.selector_prestacion.bind("<<ComboboxSelected>>", lambda e: self.ventana_secundaria.focus())
        odontologos = ["MILITELLO", "MACUA", "RAMIREZ"]
        self.selector_odontologo= ttk.Combobox(self.ventana_secundaria, state= "readonly", values= odontologos, width= 25, justify= CENTER, background="white")
        self.selector_odontologo.pack(pady=8)
        self.selector_odontologo.set("Odontólogo")
        if (self.odontologo != ''):
            self.selector_odontologo.set(self.odontologo)
        self.selector_odontologo.bind("<<ComboboxSelected>>", lambda e: self.ventana_secundaria.focus())

        self.button_frame = Frame(self.ventana_secundaria, bg="gray")
        self.button_frame.pack(pady=10)

        Button(self.button_frame, text= 'Guardar', command= self.guardar_turno, bg= "#BDC1BE", width= 10).grid(row= 0, column= 0, padx= 10)
        Button(self.button_frame, text= 'Eliminar', command= self.eliminar_turno, bg= "#BDC1BE", width= 10).grid(row= 0, column= 1, padx= 10)
        Button(self.button_frame, text= 'Salir', command= self.cancelar_turno, bg= "orange red", width= 10).grid(row= 0, column= 2, padx= 10)

    def guardar_turno(self):
        self.valores = {            
            "horario": self.horario,
            "paciente": self.nombre_entry.get(),            
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
            #print('datos completos', self.horario)
            self.conn= sqlite3.connect('turnos.db')
            self.cur= self.conn.cursor()
            # if(self.sin_turno):
            #     self.cur.execute('SELECT * FROM turno')
            #     cant_turnos=len(self.cur.fetchall())
            #     print(cant_turnos)
            if self.turnos_dados:
                try:
                    print('si ya está ocupado')
                    datos =  self.nombre_entry.get().upper(), self.selector_prestacion.get().upper(), self.selector_odontologo.get().upper(), self.horario
                    sql="UPDATE turno SET paciente=?, prestacion=?, odontologo=? where hora=?"
                    self.cur.execute(sql, datos)
                    self.conn.commit()
                except:
                    print('desocupado')
                    datos = '20/10/2024', self.horario, self.nombre_entry.get().upper(), self.selector_prestacion.get().upper(), self.selector_odontologo.get().upper()
                    sql="INSERT INTO turno VALUES(?, ?, ?, ?, ?)"
                    self.cur.execute(sql, datos)
                    self.conn.commit()
            else: #si no hay ningún turno
                datos = '20/10/2024', self.horario, self.nombre_entry.get().upper(), self.selector_prestacion.get().upper(), self.selector_odontologo.get().upper()
                sql="INSERT INTO turno VALUES(?, ?, ?, ?, ?)"
                self.cur.execute(sql, datos)
                self.conn.commit()
        
        self.conn.close()
        self.cargar_turnos()
        self.ventana_secundaria.destroy()        
    
    def eliminar_turno(self):
        #print(self.horario)
        hora=self.horario
        try:
            self.conn= sqlite3.connect('turnos.db')
            self.cur= self.conn.cursor()
            #sql="DELETE FROM turnos WHERE hora= ?"
            self.cur.execute("DELETE FROM turno WHERE hora= ?", (hora,))
            self.conn.commit()
            self.conn.close()
        except:
            print('El turno no está guardado')
        self.cargar_turnos()
        
    def widgets(self):
        self.frame_tabla = ttk.Frame(self.ventana_turno)
        #self.frame_tabla.grid(column=0,row=1)
        self.frame_tabla.grid(columnspan= 4, row= 0, sticky= 'nsew')
        Label(self.frame_tabla, text="TURNOS", font=('Helvetica', 10, 'bold')).grid(columnspan= 4, column= 0, row= 0, pady=5)
        
        self.tabla_turnos = ttk.Treeview(self.frame_tabla, columns= ("Horario", "Paciente", "Prestacion", "Odontologo"), show= 'headings', height=25, selectmode ='browse')
        self.tabla_turnos.grid(column= 0, row= 2, columnspan= 4, sticky= 'nsew', padx=5, pady=5)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure a new Treeview Heading style
        self.style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'), foreground='white',background="sea green")
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
        self.tabla_turnos.column("Horario", width= 70)
        self.tabla_turnos.column("Paciente", width= 150)
        self.tabla_turnos.column("Prestacion", width= 200)
        self.tabla_turnos.column("Odontologo", width= 150)
        
        # cargar filas al Treeview
        self.cargar_turnos()
        self.tabla_turnos.bind("<Double-1>", self.editar_turno)
       #self.frame_tabla.grid_columnconfigure(0, weight=1)
        
        self.ventana_turno.mainloop()

if __name__ == "__main__":
    Turno()       
