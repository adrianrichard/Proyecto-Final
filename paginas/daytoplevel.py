import util.config as utl
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from datetime import *
#import sqlite3
from tkinter import Button
from paginas.datehandler.datehandler import DateHandler
from bd.conexion import Conexion


fuenteb= utl.definir_fuente_bold()
fuenten= utl.definir_fuente()
class DayTopWindow(Toplevel):

    def __init__(self, dia: int, mes: int, anio: int):
        super().__init__()

        self.attributes = ("-topmost", True)
        utl.centrar_ventana(self, 700, 580)
        self.title("Agenda de turnos")
        self.resizable(width= True, height= False)
        self.turnos_box = None
        self.configure(bg= "#D1D6D3")
        self.grab_set_global()
        self.focus_set()
        self.extension = None
        self.confirmation = None
        self.fuenten= utl.definir_fuente()
        self.fuenteb= utl.definir_fuente_bold()
        self.db = Conexion()
        self.conn= self.db.conectar()

        self.dia = dia
        self.mes = mes
        self.anio = anio

        self.crear_encabezado()
        self.crear_botones_cambio_fecha()
        self.cargar_odontologos()
        self.crear_lista_turnos()
        self.cargar_turnos()

    def crear_encabezado(self):
        """ Crea encabezado """
        encabezado_texto = f"{self.dia}/{self.mes}/{self.anio}"
        self.encabezado = Label(self, text= encabezado_texto, font= "Arial 15", justify= CENTER, borderwidth= 3, bd= 3, bg= "#D1D6D3")
        self.encabezado.grid(row= 0, column= 1, ipady= 3)

    def configurar_encabezado(self):
        """ Actualiza el header de la fecha """
        self.encabezado_texto = f"{self.dia}/{self.mes}/{self.anio}"
        self.encabezado.configure(text= self.encabezado_texto)

    def crear_botones_cambio_fecha(self):
        """ Crea botones para cambiar fecha """
        Button(self, text= ">", command= self.avanzar_dia,fg= 'white', font = fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, width= 5).grid(row= 0, column= 2)
        Button(self, text= "<", command= self.retroceder_dia, fg= 'white', font = fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, width= 5).grid(row= 0, column= 0)
        Button(self, text= "Salir", font= self.fuenteb, bg= "orange", width= 8, command= self.destroy).grid(row= 0, column= 3, pady= (5,5))

    def crear_lista_turnos(self):
        estilo_tabla2 = ttk.Style(self)
        estilo_tabla2.theme_use("alt")
        estilo_tabla2.configure("TablaTurnos.Treeview", font= fuenten, foreground= 'black', rowheight= 20)
        estilo_tabla2.configure('TablaTurnos.Treeview.Heading', background= '#1F704B', foreground= 'white', padding= 3, font= fuenteb)
        self.frame_tabla = ttk.Frame(self)
        self.frame_tabla.grid(column= 0, columnspan= 4, row= 2, sticky= 'nsew')
        self.tabla_turnos = ttk.Treeview(self.frame_tabla, columns= ("Horario", "Paciente", "Prestacion", "Odontologo"), show= 'headings', height= 25, selectmode ='browse', style="TablaTurnos.Treeview")
        self.tabla_turnos.grid(column= 0, row= 2, columnspan= 4, sticky= 'nsew', padx= 5, pady= 5)

        # Definir los encabezados de las columnas
        self.tabla_turnos.heading("Horario", text= "Horario")
        self.tabla_turnos.heading("Paciente", text= "Paciente")
        self.tabla_turnos.heading("Prestacion", text= "Prestacion")
        self.tabla_turnos.heading("Odontologo", text= "Odontologo")

        # Ajustar el ancho de las columnas
        self.tabla_turnos.column("Horario", width= 70, anchor= 'center')
        self.tabla_turnos.column("Paciente", width= 200)
        self.tabla_turnos.column("Prestacion", width= 250)
        self.tabla_turnos.column("Odontologo", width= 200)

        self.tabla_turnos.bind("<Double-1>", self.editar_turno)

    def cargar_turnos(self):
        start_date = date(self.anio, self.mes, self.dia)        
        self.cur= self.conn.cursor()
        try:
            self.cur.execute("SELECT Turnos.Hora, Turnos.Paciente, Odontologos.Apellido_odontologo, Turnos.Prestacion FROM Odontologos JOIN Turnos ON Odontologos.Matricula = Turnos.Odontologo WHERE Turnos.Fecha=? ORDER BY Turnos.Hora", (start_date,))
            self.turnos_dados = self.cur.fetchall()
            self.conn.commit()
        except:
            messagebox.showinfo("Turnos", "No hay turnos")

        start_time = datetime.strptime("08:00", "%H:%M")
        # Intervalo de 30 minutos
        time_interval = timedelta(minutes= 30)
        self.j = 0
        self.tabla_turnos.delete(*self.tabla_turnos.get_children())
        for i in range(0, 25):
            current_time = start_time + i * time_interval
            if not self.turnos_dados:
                self.tabla_turnos.insert(parent= '', index= 'end', values=(current_time.strftime("%H:%M"), '', '', ''))
            else:
                if(current_time.strftime("%H:%M") == self.turnos_dados[self.j][0] and self.j < len(self.turnos_dados)):
                    
                    self.tabla_turnos.insert("", "end", values=(current_time.strftime("%H:%M"), self.turnos_dados[self.j][1], self.turnos_dados[self.j][3], self.turnos_dados[self.j][2]), tags=('anotado',))
                    self.tabla_turnos.tag_configure('anotado', font=fuenteb, background="green")
                    if(self.j+1 < len(self.turnos_dados)):
                        self.j=self.j+1
                else:
                    self.tabla_turnos.insert(parent='', index='end', values=(current_time.strftime("%H:%M"), '', '', ''))
            self.tabla_turnos.tag_configure('anotado', font=fuenteb, background="green")

    def editar_turno(self, event):
        region = self.tabla_turnos.identify("region", event.x, event.y)
        if region == "heading":  # Si el doble clic es en el encabezado
            messagebox.showwarning("Advertencia", "Debe seleccionar un horario")
            return
        self.ventana_secundaria = tk.Toplevel(self, background= 'gray')
        self.ventana_secundaria.title("Ventana Secundaria")
        self.ventana_secundaria.geometry('400x300')
        utl.centrar_ventana(self.ventana_secundaria, 400, 300)
        self.ventana_secundaria.grab_set_global() # Obliga a las ventanas estar deshabilitadas y deshabilitar todos los eventos e interacciones con la ventana
        self.ventana_secundaria.focus_set() # Mantiene el foco cuando se abre la ventana.
        
        self.turno_seleccionado = self.tabla_turnos.selection()[0]
        self.data = self.tabla_turnos.item(self.turno_seleccionado)
        self.horario = self.data['values'][0]
        self.paciente = self.data['values'][1]
        self.prestacion = self.data['values'][2]
        self.odontologo = self.data['values'][3]

        Label(self.ventana_secundaria, text= "EDITAR TURNO", font= ("Arial", 15, 'bold'), bg= "gray90", width= 60).pack(pady= 10)
        Label(self.ventana_secundaria, text= f"FECHA: {self.dia}/{self.mes}/{self.anio} - HORARIO: "+self.horario, font= ("Arial", 13, 'bold'), bg= "gray90", width= 60).pack()

        self.nombre_entry = Entry(self.ventana_secundaria, justify= CENTER)
        self.nombre_entry.pack(pady= (10,10))
        self.nombre_entry.insert(0, "Paciente")
        if (self.paciente != ''):
            self.nombre_entry.delete(0, END)
            self.nombre_entry.insert(0, self.paciente)
        self.nombre_entry.focus_set()
        prestaciones = ["CONSULTA", "EXTRACCIÓN", "TRATAMIENTO DE CONDUCTO", "LIMPIEZA"]
        self.selector_prestacion = ttk.Combobox(self.ventana_secundaria, state= "readonly", values= prestaciones, width= 25, justify= CENTER, background= "white")
        self.selector_prestacion.pack(pady= 8)
        self.selector_prestacion.set("Prestación")
        if (self.prestacion != ''):
            self.selector_prestacion.set(self.prestacion)
        self.selector_prestacion.bind("<<ComboboxSelected>>", lambda e: self.ventana_secundaria.focus())
        #odontologos = ["MILITELLO", "MACUA", "RAMIREZ"]
        self.selector_odontologo= ttk.Combobox(self.ventana_secundaria, state= "readonly", values= self.odontologos, width= 25, justify= CENTER, background= "white")
        self.selector_odontologo.pack(pady= 8)
        self.selector_odontologo.set("Odontólogo")
        if (self.odontologo != ''):
            self.selector_odontologo.set(self.odontologo)
        self.selector_odontologo.bind("<<ComboboxSelected>>", lambda e: self.ventana_secundaria.focus())

        self.button_frame = Frame(self.ventana_secundaria, bg= "gray")
        self.button_frame.pack(pady= 10)

        Button(self.button_frame, text= 'Guardar', command= self.guardar_turno, bg= "#BDC1BE", width= 10).grid(row= 0, column= 0, padx= 10)
        Button(self.button_frame, text= 'Eliminar', command= self.eliminar_turno, bg= "#BDC1BE", width= 10).grid(row= 0, column= 1, padx= 10)
        Button(self.button_frame, text= 'Salir', command= self.cancelar_turno, font= self.fuenteb, bg= "orange", width= 8).grid(row= 0, column= 2, padx= 10)

    def cancelar_turno(self):
        answer = messagebox.askokcancel(title='Salir', message='¿Desea salir sin guardar?', icon='warning')
        if answer:
            self.grab_set_global()
            self.focus_set()            
            self.ventana_secundaria.destroy()

    def eliminar_turno(self):
        start_date = date(self.anio, self.mes, self.dia)
        #self.conn=  self.db.conectar()
        self.cur= self.conn.cursor()        
        hora= self.horario
        answer = messagebox.askokcancel(title='Eliminar', message='¿Desea eliminar el turno?', icon='warning')
        if answer:
            try:
                self.cur.execute("DELETE FROM turnos WHERE fecha= ? AND hora= ?", (start_date, hora,))
                self.conn.commit()
                #self.conn.close()
                self.grab_set_global()
                self.focus_set()                
                self.ventana_secundaria.destroy()
            except:
                messagebox.showerror("Eliminar", "No se pudo eliminar.")
        self.cargar_turnos()

    def guardar_turno(self):
        """El día se carga en formato YYYY/MM/DD para luego poder usar los métodos de SQLite"""
        start_date = date(self.anio, self.mes, self.dia)
        self.conn=  self.db.conectar()
        self.cur= self.conn.cursor()
        odontologo= self.selector_odontologo.get()
        self.matricula=""
        #print(odontologo)
        try:
            sql = "SELECT Matricula FROM Odontologos WHERE Apellido_odontologo LIKE ?"
            self.cur.execute(sql, (odontologo,))
            self.matricula = self.cur.fetchone()[0]
            
        except:
            messagebox.showerror("Guardar", "No existe el odontólogo")
        #print(matricula[0])
        print(start_date)
        print(self.horario)
        print(self.nombre_entry.get().upper())
        print(self.matricula)
        datos = start_date, self.horario, self.nombre_entry.get().upper(), self.matricula, self.selector_prestacion.get().upper()
        print (datos)
        if self.nombre_entry.get().upper() != "PACIENTE" and self.selector_prestacion.get().upper() != "PRESTACIÓN" and self.selector_odontologo.get().upper() != "ODONTÓLOGO":
            answer = messagebox.askokcancel(title='Guardar', message='¿Desea guardar el turno?', icon='warning')
            if answer:
                try:
                    sql="REPLACE INTO turnos VALUES(?, ?, ?, ?, ?)"
                    self.cur.execute(sql, datos)
                    self.conn.commit()
                    #self.conn.close()
                    self.grab_set_global()
                    self.focus_set()                
                    self.ventana_secundaria.destroy()
                    self.cargar_turnos()
                except:                    
                    messagebox.showerror("Guardar", "No se pudo guardar.")                            
        else: 
            """"Si no se coloca el nombre del paciente o se elije prestación u odontólogo"""
            if self.nombre_entry.get().upper() == "PACIENTE":
                messagebox.showerror("Paciente", "Ingrese nombre paciente")
            elif self.selector_prestacion.get().upper() == "PRESTACIÓN":
                messagebox.showerror("Prestación", "Elija la prestación")
            elif self.selector_odontologo.get().upper() == "ODONTÓLOGO":
                messagebox.showerror("Odontólogo", "Elija odontólogo")

    def cargar_odontologos(self):
        self.cur= self.conn.cursor()
        self.lista_odontologos = []
        self.odontologos = []
        try:
            self.cur.execute("SELECT Apellido_odontologo FROM odontologos")
            self.lista_odontologos = self.cur.fetchall()
            self.odontologos = [odontologo[0] for odontologo in self.lista_odontologos]
            #print(apellidos)
            self.conn.commit()
        except:
            messagebox.showinfo("Odontologos", "No hay odontologos cargados")
            
    def avanzar_dia(self):
        """ AVANZAR 1 DIA """
        cant_dias = DateHandler().days_in_month(self.mes, self.anio)
        self.dia += 1
        if self.dia > cant_dias:
            self.dia = 1
            self.mes += 1
            if self.mes > 12:
                self.mes = 1
                self.anio += 1
        self.configurar_encabezado()
        self.cargar_turnos()

        if self.extension:
            self.extension.main_frame.destroy()
            self.extension = None

    def retroceder_dia(self):
        """ RETROCEDER 1 DIA """
        self.dia -= 1
        if self.dia < 1:
            self.mes -= 1
            if self.mes < 1:
                self.anio -= 1
            self.dia = DateHandler().days_in_month(self.mes, self.anio)
        self.configurar_encabezado()
        self.cargar_turnos()

        if self.extension:
            self.extension.main_frame.destroy()
            self.extension = None
