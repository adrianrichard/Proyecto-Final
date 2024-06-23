import tkinter as tk
from tkinter import Frame, Label, Button, Toplevel
import sqlite3
from tkinter import *

from PIL import ImageGrab
from datetime import datetime
from dienteodontograma import Diente
pacientes=[]
color_index = 0
colores = ['white', 'blue', 'red']
buttons = []
class Odontograma:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ventana_odontograma = tk.Tk()
        self.ventana_odontograma.geometry('750x600')
        self.fecha_actual = datetime.now().date()
        self.fecha_actual = self.fecha_actual.strftime("%d-%m-%Y")
        Label(self.ventana_odontograma, text='Odontograma', font='Arial 20 bold').grid(column=0, row=0)

        self.cargar_paciente()
        nombre=self.pacientes[0][1]
        apellido=self.pacientes[0][0]
        obra_social=self.pacientes[0][4]
        dni=self.pacientes[0][2]
        self.frame_datos_paciente=Frame(self.ventana_odontograma, border=1, borderwidth=2)
        self.frame_datos_paciente.grid(column=0, row=1)
        Label(self.frame_datos_paciente, text='Nombre Completo: '+apellido+', '+nombre, font='Arial 15').grid(column=0, row=0, sticky='e', padx=(5,15))
        Label(self.frame_datos_paciente, text='Obra Social: '+obra_social,  font='Arial 15').grid(column=1, row=0, sticky='e', padx=(5,15))
        Label(self.frame_datos_paciente, text='D.N.I.: '+str(dni),  font='Arial 15').grid(column=2, row=0, sticky='e', padx=(5,15))
        self.ancho = 700
                
        self.frame_dientes = Frame(self.ventana_odontograma)
        self.frame_dientes.grid(column=0, row=2, pady=(10,10))
        self.cargar_ultimo_odontograma()
        self.guardar_dientes()
        self.cargar_dientes()
        self.canvas = tk.Canvas(self.frame_dientes, width=700, height=400)
        self.canvas.pack()
        self.colores=["red", "yellow", "blue","white"]
        self.crear_dientes()
        
        self.ventana_odontograma.mainloop()
    
    def cargar_paciente(self):
        try:
            self.miConexion=sqlite3.connect("../bd/DBpaciente.sqlite3")
            self.miCursor=self.miConexion.cursor()
            sql = "SELECT Apellido, Nombre, DNI, Telefono, ObraSocial FROM Paciente ORDER BY Apellido"
            self.miCursor.execute(sql)
            self.pacientes = self.miCursor.fetchall()
            self.miConexion.commit()
            #print(pacientes)
        except:
            print("error")
        #print(self.pacientes[0][2])
        datos= self.pacientes[0][2], self.fecha_actual, 'Militello'
        #print(datos)
    
    def cargar_ultimo_odontograma(self):
        try:
            self.miConexion=sqlite3.connect("../bd/DBpaciente.sqlite3")
            self.miCursor=self.miConexion.cursor()
            sql = "SELECT ID_odontograma from Odontograma ORDER BY ID_odontograma DESC LIMIT 1"
            self.miCursor.execute(sql)
            self.miConexion.commit()
            self.ID_odonto_actual= self.miCursor.fetchone()
            #print(self.ID_odonto_actual[0])
        except:
            print("error diente")
        return self.ID_odonto_actual[0]
    
    def editar_diente(self, numero):
        print('prueba', numero)
        #diente= Diente()
    
    def guardar_dientes(self):
        try:
            self.miConexion=sqlite3.connect("../bd/DBpaciente.sqlite3")
            self.miCursor=self.miConexion.cursor()
            sql = "INSERT INTO Diente VALUES (?,?,?,?,?,?,?,?,?)"
            datos= 32, self.ID_odonto_actual[0], 'blue', 'red', 'yellow', 'green', 'gray', 'white', 'white'
            self.miCursor.execute(sql, datos)
            self.miConexion.commit()
            #self.ID_odonto_actual= self.miCursor.fetchone()
            #print(self.ID_odonto_actual[0])
        except:
            print("error guardar")
            
    def cargar_dientes(self):
        print('crear vector con los dientes')
        try:
            self.miConexion=sqlite3.connect("../bd/DBpaciente.sqlite3")
            self.miCursor=self.miConexion.cursor()
            sql = "SELECT * from Diente ORDER BY ID_odontograma"
            self.miCursor.execute(sql)
            self.miConexion.commit()
            self.dientes= self.miCursor.fetchall()
            print(self.dientes)
        except:
            print("error diente")
    
    def buscar_valor(self, valor):
        indice=0
        try:
            for diente in self.dientes:
                if  diente[0] == valor:
                    return indice
                else:
                    indice+=1
        except ValueError:
            return None
    def change_cursor_enter(self, event):
        # Cambiar el cursor al pasar sobre un cuadrado
        self.canvas.config(cursor="hand2")

    def change_cursor_leave(self, event):
        # Restaurar el cursor al salir del cuadrado
        self.canvas.config(cursor="")

    def editar_diente(self, numero):
        print('prueba', numero)
        #Diente()
        #del diente

    def crear_dientes(self):
        width = 30
        height = 30
        padding = 10
        num_buttons = 8
        x1=0
        extraido=False
        corona=False
        #canvas.create_text(30, 15, text=18, fill="black", font=('Helvetica 10 bold'))
        
        #primera hilera de dientes
        hilera1=18
        for i in range(num_buttons):
            x1 = x1 + padding
            y1 = 30
            x2 = x1 + width
            y2 = y1 + height
            
            tag_diente='D'+str(hilera1)
            print(tag_diente)
            
            # D18=self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x1 + width - width/3.0, y1 + height - height/3.0, fill="green", tags="D18")
            # self.canvas.tag_bind('D18', '<Enter>', change_cursor_enter)
            # self.canvas.tag_bind('D18', '<Leave>', change_cursor_leave)
            indice = self.buscar_valor(hilera1)
            #print("INDICE",indice)
            self.texto1=self.canvas.create_text(x1+ width/2, 15, text=hilera1, fill="black", font=('Helvetica 10 bold'))
            if(indice is not None):
                #print(indice)
                if self.dientes[indice][7] == 'red' or self.dientes[indice][7] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white", tags=tag_diente)
                    self.canvas.create_oval(x1+5,y1+5,x2-5,y2-5, width=5, outline=self.dientes[0][7])
                    # self.canvas.tag_bind(tag_diente, '<Enter>', self.change_cursor_enter)
                    # self.canvas.tag_bind(tag_diente, '<Leave>', self.change_cursor_leave)
                elif self.dientes[indice][8] == 'red' or self.dientes[indice][8] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white", tags=tag_diente)
                    self.canvas.create_line(x1+5,y1+5,x2-5,y2-5, fill=self.dientes[indice][8], width=5)
                    self.canvas.create_line(x1+5,y2-5,x2-5,y1+5, fill=self.dientes[indice][8], width=5)
                else:
                    #self.texto1=self.canvas.create_text(x1+ width/2, 15, text=hilera1, fill="black", font=('Helvetica 10 bold'))
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill=self.dientes[indice][2], outline = "black")#DISTAL
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill=self.dientes[indice][3], outline = "black")#VESTIBULAR
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill=self.dientes[indice][4], outline = "black")#MEDIAL
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill=self.dientes[indice][5], outline = "black")#INTERIOR
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill=self.dientes[indice][6], tags=tag_diente)#OCLUSAL
            else:
                
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
                self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white", tags=tag_diente)
            self.canvas.tag_bind(tag_diente, '<Enter>', self.change_cursor_enter)
            self.canvas.tag_bind(tag_diente, '<Leave>', self.change_cursor_leave)
            self.canvas.tag_bind(tag_diente, '<Button-1>', lambda event, numero=hilera1: self.editar_diente(numero))
            x1=x2
            hilera1-=1
        
        #linea horizontal
        self.canvas.create_line(0, y2+padding, self.ancho-40, y2+padding, width=2)
        x1=x1+10
        #linea vertical
        self.canvas.create_line(x1, 0, x1, 270, width=2)
        
        #2da hilera
        hilera2=21
        for i in range(num_buttons):
            x1 = x1 + padding
            y1 = 30
            x2 = x1 + width
            y2 = y1 + height
            indice = self.buscar_valor(hilera2)
            #print('hilera2',indice)
            self.texto2=self.canvas.create_text(x1+ width/2, 15, text=hilera2, fill="black", font=('Helvetica 10 bold'))            
            
            if(indice is not None):
                #print(indice)
                if self.dientes[indice][7] == 'red' or self.dientes[indice][7] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
                    self.canvas.create_oval(x1+5,y1+5,x2-5,y2-5, width=5, outline=self.dientes[indice][7])
                elif self.dientes[indice][8] == 'red' or self.dientes[indice][8] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
                    self.canvas.create_line(x1+5,y1+5,x2-5,y2-5, fill=self.dientes[indice][8], width=5)
                    self.canvas.create_line(x1+5,y2-5,x2-5,y1+5, fill=self.dientes[indice][8], width=5)
                else:
                    #self.texto1=self.canvas.create_text(x1+ width/2, 15, text=hilera1, fill="black", font=('Helvetica 10 bold'))
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill=self.dientes[indice][4], outline = "black")# MEDIAL
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill=self.dientes[indice][3], outline = "black")#VESTIBULAR
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill=self.dientes[indice][2], outline = "black")#DISTAL
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill=self.dientes[indice][5], outline = "black")#INTERIOR
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill=self.dientes[indice][6])#OCLUSAL
            else:
                #self.texto1=self.canvas.create_text(x1+ width/2, 15, text=hilera1, fill="black", font=('Helvetica 10 bold'))
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
                self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
            x1=x2
            hilera2+=1
        y1=y2+20
        x1=0
        
        #4ta hilera
        hilera4=48
        for i in range(num_buttons):
            x1 = x1 + padding       
            x2 = x1 + width
            y2 = y1 + height
            indice = self.buscar_valor(hilera4)
            #print('hilera2',indice)
            self.texto4=self.canvas.create_text(x1+ width/2, y2+15, text=hilera4, fill="black", font=('Helvetica 10 bold'))
                
            if(indice is not None):
                #print(indice)
                if self.dientes[indice][7] == 'red' or self.dientes[indice][7] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
                    self.canvas.create_oval(x1+5,y1+5,x2-5,y2-5, width=5, outline=self.dientes[indice][7])
                elif self.dientes[indice][8] == 'red' or self.dientes[indice][8] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
                    self.canvas.create_line(x1+5,y1+5,x2-5,y2-5, fill=self.dientes[indice][8], width=5)
                    self.canvas.create_line(x1+5,y2-5,x2-5,y1+5, fill=self.dientes[indice][8], width=5)
                else:
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill=self.dientes[indice][2], outline = "black")#DISTAL
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill=self.dientes[indice][5], outline = "black")#INTERIOR
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill=self.dientes[indice][4], outline = "black")#MEDIAL
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill=self.dientes[indice][3], outline = "black")#VESTIBULAR
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill=self.dientes[indice][6])#OCLUSAL
            else:
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
                self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
            x1=x2
            hilera4-=1
        x1=x1+10
        #3ra hilera
        hilera3=31
        for i in range(num_buttons):
            x1 = x1 + padding
            x2 = x1 + width
            y2 = y1 + height
            indice = self.buscar_valor(hilera3)
            self.texto3=self.canvas.create_text(x1+ width/2, y2+15, text=hilera3, fill="black", font=('Helvetica 10 bold'))
            #hilera3+=1
            if(indice is not None):
                #print(indice)
                if self.dientes[indice][7] == 'red' or self.dientes[indice][7] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
                    self.canvas.create_oval(x1+5,y1+5,x2-5,y2-5, width=5, outline=self.dientes[indice][7])
                elif self.dientes[indice][8] == 'red' or self.dientes[indice][8] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
                    self.canvas.create_line(x1+5,y1+5,x2-5,y2-5, fill=self.dientes[indice][8], width=5)
                    self.canvas.create_line(x1+5,y2-5,x2-5,y1+5, fill=self.dientes[indice][8], width=5)
                else:
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill=self.dientes[indice][5], outline = "black")#MEDIAL
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill=self.dientes[indice][4], outline = "black")#INTERIOR
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill=self.dientes[indice][3], outline = "black")#DISTAL
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill=self.dientes[indice][2], outline = "black")#VESTIBULAR
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill=self.dientes[indice][6])#OCLUSAL
            else:
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
                self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
            x1=x2
            hilera3+=1
        x1=120
        y1=y2 + 60
        hilera5=55
        for i in range(num_buttons-3):
            x1 = x1 + padding
            x2 = x1 + width
            y2 = y1 + height
            indice = self.buscar_valor(hilera5)
            self.texto5=self.canvas.create_text(x1+ width/2, y1-15, text=hilera5, fill="black", font=('Helvetica 10 bold'))
            #hilera3+=1
            if(indice is not None):
                #print(indice)
                if self.dientes[indice][7] == 'red' or self.dientes[indice][7] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
                    self.canvas.create_oval(x1+5,y1+5,x2-5,y2-5, width=5, outline=self.dientes[indice][7])
                elif self.dientes[indice][8] == 'red' or self.dientes[indice][8] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
                    self.canvas.create_line(x1+5,y1+5,x2-5,y2-5, fill=self.dientes[indice][8], width=5)
                    self.canvas.create_line(x1+5,y2-5,x2-5,y1+5, fill=self.dientes[indice][8], width=5)
                else:
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill=self.dientes[indice][2], outline = "black")#DISTAL
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill=self.dientes[indice][3], outline = "black")#VESTIBULAR
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill=self.dientes[indice][4], outline = "black")#MEDIAL
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill=self.dientes[indice][5], outline = "black")#INTERIOR
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill=self.dientes[indice][6])#OCLUSAL
            else:
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
                self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
            x1=x2
            hilera5-=1

        x1=x2+11
        #y1= 195
        hilera6=61
        for i in range(num_buttons-3):
            x1 = x1 + padding
            x2 = x1 + width
            y2 = y1 + height
            indice = self.buscar_valor(hilera6)
            self.texto6=self.canvas.create_text(x1+ width/2, y1-15, text=hilera6, fill="black", font=('Helvetica 10 bold'))
            #hilera3+=1
            if(indice is not None):
                #print(indice)
                if self.dientes[indice][7] == 'red' or self.dientes[indice][7] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
                    self.canvas.create_oval(x1+5,y1+5,x2-5,y2-5, width=5, outline=self.dientes[indice][7])
                elif self.dientes[indice][8] == 'red' or self.dientes[indice][8] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
                    self.canvas.create_line(x1+5,y1+5,x2-5,y2-5, fill=self.dientes[indice][8], width=5)
                    self.canvas.create_line(x1+5,y2-5,x2-5,y1+5, fill=self.dientes[indice][8], width=5)
                else:
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill=self.dientes[indice][4], outline = "black")# MEDIAL
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill=self.dientes[indice][3], outline = "black")#VESTIBULAR
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill=self.dientes[indice][2], outline = "black")#DISTAL
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill=self.dientes[indice][5], outline = "black")#INTERIOR
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill=self.dientes[indice][6])#OCLUSAL
            else:
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
                self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
            x1=x2
            hilera6+=1
        x1=120
        y1=y2 + 10
        hilera8=85
        for i in range(num_buttons-3):
            x1 = x1 + padding
            x2 = x1 + width
            y2 = y1 + height
            indice = self.buscar_valor(hilera8)
            #print('hilera2',indice)
            self.texto8=self.canvas.create_text(x1+ width/2, y2+15, text=hilera8, fill="black", font=('Helvetica 10 bold'))
                
            if(indice is not None):
                #print(indice)
                if self.dientes[indice][7] == 'red' or self.dientes[indice][7] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
                    self.canvas.create_oval(x1+5,y1+5,x2-5,y2-5, width=5, outline=self.dientes[indice][7])
                elif self.dientes[indice][8] == 'red' or self.dientes[indice][8] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
                    self.canvas.create_line(x1+5,y1+5,x2-5,y2-5, fill=self.dientes[indice][8], width=5)
                    self.canvas.create_line(x1+5,y2-5,x2-5,y1+5, fill=self.dientes[indice][8], width=5)
                else:
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill=self.dientes[indice][2], outline = "black")#DISTAL
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill=self.dientes[indice][5], outline = "black")#INTERIOR
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill=self.dientes[indice][4], outline = "black")#MEDIAL
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill=self.dientes[indice][3], outline = "black")#VESTIBULAR
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill=self.dientes[indice][6])#OCLUSAL
            else:
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
                self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
            x1=x2
            hilera8-=1
        x1=x2+11
        y1= y2-height
        hilera7=71
        for i in range(num_buttons-3):
            x1 = x1 + padding
            x2 = x1 + width
            y2 = y1 + height
            indice = self.buscar_valor(hilera7)
            self.texto3=self.canvas.create_text(x1+ width/2, y2+15, text=hilera7, fill="black", font=('Helvetica 10 bold'))
            #hilera3+=1
            if(indice is not None):
                #print(indice)
                if self.dientes[indice][7] == 'red' or self.dientes[indice][7] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
                    self.canvas.create_oval(x1+5,y1+5,x2-5,y2-5, width=5, outline=self.dientes[indice][7])
                elif self.dientes[indice][8] == 'red' or self.dientes[indice][8] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
                    self.canvas.create_line(x1+5,y1+5,x2-5,y2-5, fill=self.dientes[indice][8], width=5)
                    self.canvas.create_line(x1+5,y2-5,x2-5,y1+5, fill=self.dientes[indice][8], width=5)
                else:
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill=self.dientes[indice][5], outline = "black")#MEDIAL
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill=self.dientes[indice][4], outline = "black")#INTERIOR
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill=self.dientes[indice][3], outline = "black")#DISTAL
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill=self.dientes[indice][2], outline = "black")#VESTIBULAR
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill=self.dientes[indice][6])#OCLUSAL
            else:
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
                self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
                self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
            x1=x2
            hilera7+=1
        x1=padding
        y1=30
    
    # D18=self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x1 + width - width/3.0, y1 + height - height/3.0, fill="green", tags="D18")
    # self.canvas.tag_bind('D18', '<Enter>', change_cursor_enter)
    # self.canvas.tag_bind('D18', '<Leave>', change_cursor_leave)
    # self.canvas.tag_bind('D18', '<Button-1>', editar_diente)
    # self.canvas.tag_bind('D18', '<Button-1>', lambda event, numero=18: editar_diente(numero))
    # D17=self.canvas.create_rectangle(x1 + width +padding+ width/3.0, y1 + height/3.0, x1 +padding+ 2*width - width/3.0, y1 + height - height/3.0, fill="green", tags="D17")
    # self.canvas.tag_bind('D17', '<Enter>', change_cursor_enter)
    # self.canvas.tag_bind('D17', '<Leave>', change_cursor_leave)
    # self.canvas.tag_bind('D17', '<Button-1>', lambda event, numero=17: editar_diente(numero))

'''        
#def button_click(event, index):
    #canvas.itemconfig(buttons[index], fill="red")
#def cargar_dientes():

def editar_diente( numero):
    print('prueba', numero)
    diente= Diente()
    
# def cambiar_color(cara, c):
#     global color_index, canvas
#     color_index = (color_index + 1) % len(colores2)
#     color_actual = colores2[color_index]
#     print('hola')
#     c.canvas.itemconfig(cara, fill="red")
#     #label_color_actual.config(text=f"Color actual: {color_actual.capitalize()}")
 '''       

'''
self.crear_dientes()
canvas.delete(self.texto1)
# canvas.delete(texto2)
# canvas.delete(texto3)
# canvas.delete(texto1)
# canvas.delete(texto1)
# canvas.delete(texto1)

#cargar_dientes()
#capture_screenshot()
'''
if __name__ == "__main__":
    Odontograma()    