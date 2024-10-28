from datetime import *
from functools import partial
from tkinter import *
from tkinter import ttk
import tkinter as tk
#import sqlite3
from tkinter import  messagebox
from paginas.datehandler.datehandler import DateHandler as dH
from paginas.daytoplevel import DayTopWindow
import util.config as utl
from bd.conexion import Conexion

from pathlib import Path

fuente= 'Arial'
color_fuente = 'black'
color_fondo2 = 'gray90'
fuenteb= utl.definir_fuente_bold()
fuenten= utl.definir_fuente()

class TKCalendar():

    def __init__(self):
        super().__init__()

        self.botones_fecha = []
        self.dias_turno = []
        self.toplevel = None
        self.encabezado = None
        self.db = Conexion()

        self.anio = datetime.now().year  # Devuelve entero de 4-digit (anio)
        self.mes = datetime.now().month  # Devuelve entero(mes)
        self.fechas = []
        self.marcar_dia_turno()

        """ Clases soporte """
        self.dh = dH()

    def marcar_dia_turno(self):
        """Carga el mes y lo transforma a string"""
        mes_turno = str(self.mes)
        """si el mes es menor a 10, le agrega el 0 (cero)"""
        if self.mes < 10:
            mes_turno= "0"+mes_turno
        """Carga el año y lo transforma a string"""
        anio_turno= str(self.anio)
        #date_str = start_date.strftime('%d-%m-%Y')
        #print(mes_turno)
        
        self.dias_turno = []
        self.conn = self.db.conectar()
        self.cur = self.conn.cursor()
        try:                    
            self.query = f"SELECT strftime('%d', fecha) FROM turnos WHERE strftime('%Y', fecha)=? AND strftime('%m', fecha)= ?"
            self.cur.execute(self.query, (anio_turno, mes_turno, ))
            self.dias_turno  = [fila[0] for fila in self.cur.fetchall()]
            self.conn.commit()
            #print(self.dias_turno)
            
        except:
            messagebox.showinfo("Turnos","Error al cargar turnos")
        
    def crear_encabezado(self, frame):
        """ Crea el encabezado """
        encabezado_texto = f"{self.dh.month_num_to_string(self.mes)} {self.anio}"
        self.encabezado = Label(frame, text= encabezado_texto,  font= (fuente, 15), justify= CENTER)
        self.encabezado.grid(row= 0, column= 0, columnspan= 7, sticky= EW, ipady= 10)

        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sabado", "Domingo"]
        for i, j in enumerate(dias):
            Label(frame, text= dias[i], bd= 1, font= (fuente, 12, "bold"), relief= SOLID).grid(row= 1, column= i, sticky= NSEW, ipady= 10)

        Button(frame, text="<", command= self.mes_anterior, fg= 'white', font = fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, width= 5).grid(row= 0, column= 1)
        Button(frame, text=">", command= self.mes_siguiente, fg= 'white', font = fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, width= 5).grid(row= 0, column= 5)

    def crear_botones_fechas(self, frame):
        """ Crea botones de fechas mes actual """
        coords = [(i, j) for i in range(2, 8) for j in range(0, 7)]
        for coord in coords:
            btn = tk.Button(frame, font= (fuente, 10), bg= "green", relief= SUNKEN, bd= 2, height= 4, width= 10)
            btn.grid(row= coord[0], column= coord[1], sticky= NSEW)
            self.botones_fecha.append(btn)

    def actualizar_encabezado(self):
        """ Actualiza el encabezado del mes """
        self.encabezado.configure(text=f"{self.dh.month_num_to_string(self.mes)} {self.anio}")

    def actualizar_botones_fechas(self):
        
        """ Set button text to date numbers """
        self.fechas = self.dh.date_list(self.anio, self.mes)  # Devuelve 35 dias (5 semanas)
        self.fechas.extend([0 for _ in range(42 - len(self.fechas))])  # agrega ceros en las fechas porque son 42 botones de fecha

        for i, j in enumerate(self.fechas):  # Configura el texto del boton para mostrar la fecha
            if j == 0:
                self.botones_fecha[i].configure(text= "", state= DISABLED, bg= "#808080") #botones sin fecha
                #print(i)
            else:
                if i == 6 or i == 13 or i == 20 or i == 27 or i == 34:
                    self.botones_fecha[i].configure(text= j, state= DISABLED, bg= "gray90") #DIA DOMINGO
                else:    
                    self.botones_fecha[i].configure(text= j, command= partial(self.info_dia, j), bg= "white", state= NORMAL)
                    for dia in self.dias_turno:
                        #print(type(dia), type(j))
                        if j == int(dia) :
                            #print(j, dia, i)
                            self.botones_fecha[i].configure(bg="sky blue")
            if i == 40:
                self.botones_fecha[i].configure(text= "TURNOS\nASIGNADOS", state= DISABLED, bg= "sky blue", disabledforeground= "black")#Marca si hay turnos
            if i == 41:
                self.botones_fecha[i].configure(text= "DÍA ACTUAL", state= DISABLED, bg= "orange", disabledforeground= "black")#Marca la fecha actual
            if j == datetime.today().day \
                    and self.mes == datetime.today().month \
                    and self.anio == datetime.today().year:
                self.botones_fecha[i].configure(bg= "orange")
            

    def configurar_filas_columnas(self, frame):
        """ Configura filas y columnas para expandandirlas al tamaño de la ventana """
        [frame.rowconfigure(i, weight= 1) for i in range(frame.grid_size()[1])]
        [frame.columnconfigure(i, weight= 1) for i in range(frame.grid_size()[0])]

    def mes_siguiente(self):
        """ Aumenta el mes y reconfigura la interface del calendario """
        self.mes += 1
        if self.mes == 13:
            self.mes = 1
            self.anio += 1
        self.marcar_dia_turno()
        self.actualizar_botones_fechas()
        self.actualizar_encabezado()

    def mes_anterior(self):
        """ Disminuye el mes y reconfigura la interface del calendario """
        self.mes -= 1
        if self.mes == 0:
            self.mes = 12
            self.anio -= 1
        self.marcar_dia_turno()
        self.actualizar_botones_fechas()
        self.actualizar_encabezado()

    def info_dia(self, dia):
        """ Abre una ventana para guardar la cita """
        try:
            self.toplevel.destroy()
            self.toplevel = DayTopWindow(dia, self.mes, self.anio)
            self.marcar_dia_turno()
            self.actualizar_botones_fechas()
        except AttributeError:
            self.toplevel = DayTopWindow(dia, self.mes, self.anio)
            self.marcar_dia_turno()
            self.actualizar_botones_fechas()