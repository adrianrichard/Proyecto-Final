
#from tkinter import Frame, Label, Button, Toplevel
import sqlite3
from tkinter import *
import tkinter as tk
from PIL import ImageGrab
from datetime import datetime
from dienteodontograma import Diente
from gui_app import App
from functools import partial

pacientes=[]
color_index = 0
colores = ['white', 'blue', 'red', 'green']
buttons = []
class Odontograma:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ventana_odontograma = tk.Tk()
        self.ventana_odontograma.geometry('700x600')
        self.ventana_odontograma.grid_columnconfigure(0, weight= 1)
        self.fecha_actual = datetime.now().date()
        self.fecha_actual = self.fecha_actual.strftime("%d-%m-%Y")
        Label(self.ventana_odontograma, text= 'Odontograma', font= 'Arial 20 bold').grid(column= 0, row= 0)

        self.cargar_paciente()
        nombre=self.pacientes[0][1]
        apellido=self.pacientes[0][0]
        obra_social=self.pacientes[0][4]
        dni=self.pacientes[0][2]
        self.frame_datos_paciente=Frame(self.ventana_odontograma, border= 1, borderwidth= 2, bg= "gray90")
        self.frame_datos_paciente.grid(column= 0, row= 1, sticky= "nsew")
        Label(self.frame_datos_paciente, text= 'Nombre Completo: '+apellido+', '+nombre, font= 'Arial 12', bg= "gray90").grid(column= 0, row= 0, sticky= 'e', padx= (10, 15))
        Label(self.frame_datos_paciente, text= 'Obra Social: '+obra_social,  font= 'Arial 12', bg= "gray90").grid(column= 1, row= 0, sticky= 'e', padx= (5,15))
        Label(self.frame_datos_paciente, text= 'D.N.I.: '+str(dni),  font= 'Arial 12', bg= "gray90").grid(column= 2, row= 0, sticky= 'e', padx= (5,15))
        self.ancho = 700
                
        self.frame_dientes = Frame(self.ventana_odontograma)
        self.frame_dientes.grid(column= 0, row= 2, pady= (10,10))
        self.cargar_ultimo_odontograma()
        #self.guardar_diente()
        self.cargar_dientes()
        self.canvas = tk.Canvas(self.frame_dientes, width= 700, height= 400)
        self.canvas.pack()
        self.colores=["red", "green", "blue", "white"]
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
        self.ventana_secundaria = tk.Tk()
        self.ventana_secundaria.title("Editar diente")
        self.ventana_secundaria.geometry('300x350')
        Label(self.ventana_secundaria, text= "EDITAR DIENTE", font= ("Arial", 15, 'bold'), fg= 'white', bg= "gray", width= 60).pack(pady= 10)
        Label(self.ventana_secundaria, text= "DIENTE "+str(numero), font= ("Arial", 12, 'bold'), fg= 'white', bg= "gray", width= 60).pack()
        diente_frame = Frame(self.ventana_secundaria)
        diente_frame.pack(pady= (10, 10))
        botones_frame = Frame(self.ventana_secundaria)
        botones_frame.pack(pady= (10, 10))
        Button(botones_frame, text= 'X Roja', command= partial(self.extraccion, numero,'red'), bg= "red", width= 5).grid(row= 0, column= 0, padx= 10)
        Button(botones_frame, text= 'X Azul', command= partial(self.extraccion, numero, 'blue'), bg= "blue", width= 5).grid(row= 0, column= 1, padx= 10)
        Button(botones_frame, text= 'O Roja', command= partial(self.corona, numero,'red'), bg= "red", width= 5).grid(row= 0, column= 2, padx= 10)
        Button(botones_frame, text= 'O Azul', command= partial(self.corona, numero, 'blue'), bg= "blue", width= 5).grid(row= 0, column= 3, padx= 10)
        Button(botones_frame, text= 'CANCELAR', command= self.cancelar, width= 7).grid(row= 1, column= 2, padx= 10, pady=(10, 0))
        Button(botones_frame, text= 'GUARDAR', command= self.guardar_diente, width= 7).grid(row= 1, column= 1, padx= 10, pady=(10, 0))

        self.canvas2 = tk.Canvas(diente_frame, width= 400, height= 150)
        self.canvas2.pack()
        self.diente=[numero, 'white','white','white','white','white','white','white']
        width = 100
        height = 100
        x1 = 100
        y1 = 25
        x2 = x1 + width
        y2 = y1 + height
        #LETRAS
        if numero == 11 or numero == 12 or numero == 13 or numero == 14 or numero == 15 or numero == 16 or numero == 17 or numero == 18 \
            or numero == 51 or numero == 52 or numero == 53 or numero == 54 or numero == 55:
            self.canvas2.create_text(x1+ width/2, 15, text= 'V', fill= "black", font= ('Helvetica 10 bold'))
            self.canvas2.create_text(x1-10, 25+ width/2, text= 'D', fill= "black", font= ('Helvetica 10 bold'))
            self.canvas2.create_text(x1+ width/2, 35+ height, text= 'P', fill= "black", font= ('Helvetica 10 bold'))
            self.canvas2.create_text(x1+ width+10, 25+ width/2, text= 'M', fill= "black", font= ('Helvetica 10 bold'))
        if numero == 21 or numero == 22 or numero == 23 or numero == 24 or numero == 25 or numero == 26 or numero == 27 or numero == 28 \
            or numero == 61 or numero == 62 or numero == 63 or numero == 64 or numero == 65:
            self.canvas2.create_text(x1+ width/2, 15, text= 'V', fill= "black", font= ('Helvetica 10 bold'))
            self.canvas2.create_text(x1-10, 25+ width/2, text= 'M', fill= "black", font= ('Helvetica 10 bold'))
            self.canvas2.create_text(x1+ width/2, 35+ height, text= 'P', fill= "black", font= ('Helvetica 10 bold'))
            self.canvas2.create_text(x1+ width+10, 25+ width/2, text= 'D', fill= "black", font= ('Helvetica 10 bold'))
        if numero == 31 or numero == 32 or numero == 33 or numero == 34 or numero == 35 or numero == 36 or numero == 37 or numero == 38 \
            or numero == 71 or numero == 72 or numero == 73 or numero == 74 or numero == 75:
            self.canvas2.create_text(x1+ width/2, 15, text= 'L', fill= "black", font= ('Helvetica 10 bold'))
            self.canvas2.create_text(x1-10, 25+ width/2, text= 'M', fill= "black", font= ('Helvetica 10 bold'))
            self.canvas2.create_text(x1+ width/2, 35+ height, text= 'V', fill= "black", font= ('Helvetica 10 bold'))
            self.canvas2.create_text(x1+ width+10, 25+ width/2, text= 'D', fill= "black", font= ('Helvetica 10 bold'))
        if numero == 41 or numero == 42 or numero == 43 or numero == 44 or numero == 45 or numero == 46 or numero == 47 or numero == 48 \
            or numero == 81 or numero == 82 or numero == 83 or numero == 84 or numero == 85:
            self.canvas2.create_text(x1+ width/2, 15, text= 'L', fill= "black", font= ('Helvetica 10 bold'))
            self.canvas2.create_text(x1-10, 25+ width/2, text= 'D', fill= "black", font= ('Helvetica 10 bold'))
            self.canvas2.create_text(x1+ width/2, 35+ height, text= 'V', fill= "black", font= ('Helvetica 10 bold'))
            self.canvas2.create_text(x1+ width+10, 25+ width/2, text= 'M', fill= "black", font= ('Helvetica 10 bold'))
                
        for diente in self.dientes:
            if diente[0] == numero:
                if diente[7] == 'red' or diente[7] == 'blue':
                    self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= 'white', outline = "black", tags= 'C1')
                    self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= 'white', outline = "black", tags= 'C2')
                    self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C3')
                    self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C4')
                    self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= 'white', tags= 'CO')
                    self.canvas2.create_oval(x1+5, y1+5, x2-5, y2-5, width= 5, outline= diente[7])
                elif diente[8] == 'red' or diente[8] == 'blue':
                    self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= 'white', outline = "black", tags= 'C1')
                    self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= 'white', outline = "black", tags= 'C2')
                    self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C3')
                    self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C4')
                    self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= 'white', tags= 'CO')
                    self.canvas2.create_line(x1+5, y1+5, x2-5, y2-5, fill= diente[8], width= 5)
                    self.canvas2.create_line(x1+5, y2-5, x2-5, y1+5, fill= diente[8], width= 5)
                else:
                    self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= diente[2], outline = "black", tags= 'C1')
                    self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= diente[3], outline = "black", tags= 'C2')
                    self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= diente[4], outline = "black", tags= 'C3')
                    self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= diente[5], outline = "black", tags= 'C4')
                    self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= diente[6], tags= 'CO')
                self.canvas2.tag_bind('C1', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C1'))
                self.canvas2.tag_bind('C2', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C2'))
                self.canvas2.tag_bind('C3', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C3'))
                self.canvas2.tag_bind('C4', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C4'))
                self.canvas2.tag_bind('CO', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'CO'))
                break
            else:
                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= 'white', outline = "black", tags= 'C1')
                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= 'white', outline = "black", tags= 'C2')
                self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C3')
                self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C4')
                self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= 'white', tags= 'CO')
    
            self.canvas2.tag_bind('C1', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C1'))
            self.canvas2.tag_bind('C2', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C2'))
            self.canvas2.tag_bind('C3', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C3'))
            self.canvas2.tag_bind('C4', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C4'))
            self.canvas2.tag_bind('CO', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'CO'))

    def corona(self, numero, color):
        #print(color)
        width = 100
        height = 100
        x1 = 100
        y1 = 25
        x2 = x1 + width
        y2 = y1 + height
        self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= 'white', outline = "black", tags= 'C1')
        self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= 'white', outline = "black", tags= 'C2')
        self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C3')
        self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C4')
        self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= 'white', tags= 'CO')
        self.canvas2.create_oval(x1+5, y1+5, x2-5, y2-5, width= 5, outline= color)
        self.diente_modificado=[numero, 'white', 'white', 'white', 'white', 'white', 'white', color]
    
    def extraccion(self, numero, color):
        #print(color)
        width = 100
        height = 100
        x1 = 100
        y1 = 25
        x2 = x1 + width
        y2 = y1 + height
        self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= 'white', outline = "black", tags= 'C1')
        self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= 'white', outline = "black", tags= 'C2')
        self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C3')
        self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C4')
        self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= 'white', tags= 'CO')
        self.canvas2.create_line(x1+5, y1+5, x2-5, y2-5, fill= color, width= 5)
        self.canvas2.create_line(x1+5, y2-5, x2-5, y1+5, fill= color, width= 5)
        self.diente_modificado=[numero, 'white', 'white', 'white', 'white', 'white', color, 'white']
    
    def cancelar(self):
        self.ventana_secundaria.destroy()
        self.crear_dientes()
        
    def guardar_diente(self):
        try:
            self.miConexion = sqlite3.connect("../bd/DBpaciente.sqlite3")
            self.miCursor = self.miConexion.cursor()
            sql = "INSERT INTO Diente VALUES (?,?,?,?,?,?,?,?,?)"
            datos= self.diente[0], self.ID_odonto_actual[0], self.diente[1], self.diente[2], self.diente[3], self.diente[4], self.diente[5], self.diente[6], self.diente[7]
            self.miCursor.execute(sql, datos)
            self.miConexion.commit()
            #self.ID_odonto_actual= self.miCursor.fetchone()
            #print(self.ID_odonto_actual[0])
        except:
            print("error guardar")
        self.cargar_dientes()
        self.crear_dientes()

    def cargar_dientes(self):
        print('crear vector con los dientes')
        try:
            self.miConexion = sqlite3.connect("../bd/DBpaciente.sqlite3")
            self.miCursor = self.miConexion.cursor()
            sql = "SELECT * from Diente ORDER BY ID_odontograma"
            self.miCursor.execute(sql)
            self.miConexion.commit()
            self.dientes= self.miCursor.fetchall()
            #print(self.dientes)
        except:
            print("error diente")

    def buscar_valor(self, valor):
        indice = 0
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
        self.canvas.config(cursor= "hand2")

    def change_cursor_leave(self, event):
        # Restaurar el cursor al salir del cuadrado
        self.canvas.config(cursor= "")

    def cambiar_color(self, event, numero, tag):
        item = self.canvas2.find_closest(event.x, event.y)
        current_color = self.canvas2.itemcget(item, "fill")
        i=0
    # Cambiar el color del cuadrado según su estado actual
        if current_color == "white":
            self.canvas2.itemconfig(item, fill="red")
        elif current_color == "red":
            self.canvas2.itemconfig(item, fill="blue")
        elif current_color == "blue":
            self.canvas2.itemconfig(item, fill="green")
        elif current_color == "green":
            self.canvas2.itemconfig(item, fill="white")
        color_actual=self.canvas2.itemcget(item, "fill")
        if tag =='C1':
            i=1
            self.diente[1]=color_actual
        if tag =='C2':
            i=2
            self.diente[2]=color_actual
        if tag =='C3':
            i=3
            self.diente[3]=color_actual
        if tag =='C4':
            i=4
            self.diente[4]=color_actual
        if tag =='CO':
            i=5
            self.diente[5]=color_actual
                       
        #print (numero, tag, self.diente[i])
    
    # def guardar_diente(self):
    #     print('prueba')
    #     #self.cara_d.canvasitemcget

    def crear_dientes(self):
        width = 30
        height = 30
        padding = 10
        num_buttons = 8
        x1 = 0

        #primera hilera de dientes
        hilera1 = 18
        for i in range(num_buttons):
            x1 = x1 + padding
            y1 = 30
            x2 = x1 + width
            y2 = y1 + height

            tag_diente = 'D' + str(hilera1)

            indice = self.buscar_valor(hilera1)
            self.texto1 = self.canvas.create_text(x1+ width/2, 15, text= hilera1, fill= "black", font= ('Helvetica 10 bold'))
            if(indice is not None):
                #print(indice)
                if self.dientes[indice][7] == 'red' or self.dientes[indice][7] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, width= 2, outline= self.dientes[indice][7])
                elif self.dientes[indice][8] == 'red' or self.dientes[indice][8] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_line(x1+5, y1+5, x2-5, y2-5, fill= self.dientes[indice][8], width= 2)
                    self.canvas.create_line(x1+5, y2-5, x2-5, y1+5, fill= self.dientes[indice][8], width= 2)
                else:
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= self.dientes[indice][2], outline = "black")#DISTAL
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= self.dientes[indice][3], outline = "black")#VESTIBULAR
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][4], outline = "black")#MEDIAL
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][5], outline = "black")#INTERIOR
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= self.dientes[indice][6], tags= tag_diente)#OCLUSAL
            else:                
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
            self.canvas.tag_bind(tag_diente, '<Enter>', self.change_cursor_enter)
            self.canvas.tag_bind(tag_diente, '<Leave>', self.change_cursor_leave)
            self.canvas.tag_bind(tag_diente, '<Button-1>', lambda event, numero= hilera1: self.editar_diente(numero))
            x1 = x2
            hilera1-=1
        
        #linea horizontal
        self.canvas.create_line(0, y2+padding, self.ancho-40, y2+padding, width= 2)
        x1 = x1+10
        #linea vertical
        self.canvas.create_line(x1, 0, x1, 270, width= 2)
        
        #2da hilera
        hilera2 = 21
        for i in range(num_buttons):
            x1 = x1 + padding
            y1 = 30
            x2 = x1 + width
            y2 = y1 + height
            indice = self.buscar_valor(hilera2)
            #print('hilera2',indice)
            self.texto2= self.canvas.create_text(x1+ width/2, 15, text= hilera2, fill= "black", font= ('Helvetica 10 bold'))            
            tag_diente = 'D' + str(hilera2)
            if(indice is not None):
                #print(indice)
                if self.dientes[indice][7] == 'red' or self.dientes[indice][7] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, width= 2, outline= self.dientes[indice][7])
                elif self.dientes[indice][8] == 'red' or self.dientes[indice][8] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_line(x1+5, y1+5, x2-5, y2-5, fill= self.dientes[indice][8], width= 2)
                    self.canvas.create_line(x1+5, y2-5, x2-5, y1+5, fill= self.dientes[indice][8], width= 2)
                else:
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= self.dientes[indice][4], outline = "black")# MEDIAL
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= self.dientes[indice][3], outline = "black")#VESTIBULAR
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][2], outline = "black")#DISTAL
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][5], outline = "black")#INTERIOR
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= self.dientes[indice][6], tags= tag_diente)#OCLUSAL
            else:
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
            x1 = x2
            self.canvas.tag_bind(tag_diente, '<Enter>', self.change_cursor_enter)
            self.canvas.tag_bind(tag_diente, '<Leave>', self.change_cursor_leave)
            self.canvas.tag_bind(tag_diente, '<Button-1>', lambda event, numero= hilera2: self.editar_diente(numero))
            hilera2+=1
        y1 = y2+20
        x1 = 0

        #4ta hilera
        hilera4 = 48
        for i in range(num_buttons):
            x1 = x1 + padding
            x2 = x1 + width
            y2 = y1 + height
            indice = self.buscar_valor(hilera4)
            #print('hilera2',indice)
            self.texto4 = self.canvas.create_text(x1+ width/2, y2+15, text= hilera4, fill= "black", font=('Helvetica 10 bold'))
            tag_diente = 'D' + str(hilera4)
            if(indice is not None):
                #print(indice)
                if self.dientes[indice][7] == 'red' or self.dientes[indice][7] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, width= 2, outline= self.dientes[indice][7])
                elif self.dientes[indice][8] == 'red' or self.dientes[indice][8] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_line(x1+5, y1+5, x2-5, y2-5, fill= self.dientes[indice][8], width= 2)
                    self.canvas.create_line(x1+5, y2-5, x2-5, y1+5, fill= self.dientes[indice][8], width= 2)
                else:
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= self.dientes[indice][2], outline = "black")#DISTAL
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= self.dientes[indice][5], outline = "black")#INTERIOR
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][4], outline = "black")#MEDIAL
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][3], outline = "black")#VESTIBULAR
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= self.dientes[indice][6], tags= tag_diente)#OCLUSAL
            else:
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
            x1 = x2
            self.canvas.tag_bind(tag_diente, '<Enter>', self.change_cursor_enter)
            self.canvas.tag_bind(tag_diente, '<Leave>', self.change_cursor_leave)
            self.canvas.tag_bind(tag_diente, '<Button-1>', lambda event, numero= hilera4: self.editar_diente(numero))
            hilera4-=1
        x1 = x1+10
        #3ra hilera
        hilera3 = 31
        for i in range(num_buttons):
            x1 = x1 + padding
            x2 = x1 + width
            y2 = y1 + height
            indice = self.buscar_valor(hilera3)
            self.texto3 = self.canvas.create_text(x1+ width/2, y2+15, text= hilera3, fill= "black", font= ('Helvetica 10 bold'))
            tag_diente = 'D' + str(hilera3)
            if(indice is not None):
                #print(indice)
                if self.dientes[indice][7] == 'red' or self.dientes[indice][7] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, width= 2, outline= self.dientes[indice][7])
                elif self.dientes[indice][8] == 'red' or self.dientes[indice][8] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_line(x1+5, y1+5, x2-5, y2-5, fill= self.dientes[indice][8], width= 5)
                    self.canvas.create_line(x1+5, y2-5, x2-5, y1+5, fill= self.dientes[indice][8], width= 5)
                else:
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= self.dientes[indice][5], outline = "black")#MEDIAL
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= self.dientes[indice][4], outline = "black")#INTERIOR
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][3], outline = "black")#DISTAL
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][2], outline = "black")#VESTIBULAR
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= self.dientes[indice][6], tags= tag_diente)#OCLUSAL
            else:
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
            x1 = x2
            self.canvas.tag_bind(tag_diente, '<Enter>', self.change_cursor_enter)
            self.canvas.tag_bind(tag_diente, '<Leave>', self.change_cursor_leave)
            self.canvas.tag_bind(tag_diente, '<Button-1>', lambda event, numero= hilera3: self.editar_diente(numero))
            hilera3+=1
        x1 = 120
        y1 = y2 + 60
        hilera5 = 55
        for i in range(num_buttons-3):
            x1 = x1 + padding
            x2 = x1 + width
            y2 = y1 + height
            indice = self.buscar_valor(hilera5)
            self.texto5 = self.canvas.create_text(x1+ width/2, y1-15, text= hilera5, fill= "black", font= ('Helvetica 10 bold'))
            tag_diente = 'D' + str(hilera5)
            if(indice is not None):
                #print(indice)
                if self.dientes[indice][7] == 'red' or self.dientes[indice][7] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, width= 2, outline= self.dientes[indice][7])
                elif self.dientes[indice][8] == 'red' or self.dientes[indice][8] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_line(x1+5, y1+5, x2-5, y2-5, fill= self.dientes[indice][8], width= 2)
                    self.canvas.create_line(x1+5, y2-5, x2-5, y1+5, fill= self.dientes[indice][8], width= 2)
                else:
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= self.dientes[indice][2], outline = "black")#DISTAL
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= self.dientes[indice][3], outline = "black")#VESTIBULAR
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][4], outline = "black")#MEDIAL
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][5], outline = "black")#INTERIOR
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= self.dientes[indice][6], tags= tag_diente)#OCLUSAL
            else:
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
            x1 = x2
            self.canvas.tag_bind(tag_diente, '<Enter>', self.change_cursor_enter)
            self.canvas.tag_bind(tag_diente, '<Leave>', self.change_cursor_leave)
            self.canvas.tag_bind(tag_diente, '<Button-1>', lambda event, numero= hilera5: self.editar_diente(numero))
            hilera5-=1

        x1 = x2+11
        #y1= 195
        hilera6 = 61
        for i in range(num_buttons-3):
            x1 = x1 + padding
            x2 = x1 + width
            y2 = y1 + height
            indice = self.buscar_valor(hilera6)
            self.texto6 = self.canvas.create_text(x1+ width/2, y1-15, text= hilera6, fill= "black", font= ('Helvetica 10 bold'))
            tag_diente = 'D' + str(hilera6)
            if(indice is not None):
                #print(indice)
                if self.dientes[indice][7] == 'red' or self.dientes[indice][7] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, width= 2, outline= self.dientes[indice][7])
                elif self.dientes[indice][8] == 'red' or self.dientes[indice][8] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_line(x1+5, y1+5, x2-5, y2-5, fill= self.dientes[indice][8], width= 2)
                    self.canvas.create_line(x1+5, y2-5, x2-5, y1+5, fill= self.dientes[indice][8], width= 2)
                else:
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= self.dientes[indice][4], outline = "black")# MEDIAL
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= self.dientes[indice][3], outline = "black")#VESTIBULAR
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][2], outline = "black")#DISTAL
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][5], outline = "black")#INTERIOR
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= self.dientes[indice][6], tags= tag_diente)#OCLUSAL
            else:
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
            x1 = x2
            self.canvas.tag_bind(tag_diente, '<Enter>', self.change_cursor_enter)
            self.canvas.tag_bind(tag_diente, '<Leave>', self.change_cursor_leave)
            self.canvas.tag_bind(tag_diente, '<Button-1>', lambda event, numero= hilera6: self.editar_diente(numero))
            hilera6+=1
        x1 = 120
        y1 = y2 + 10
        self.canvas.create_text(50, y2, text= 'DERECHA', fill= "black", font= ('Helvetica 10 bold'))
        self.canvas.create_text(x2+75, y2, text= 'IZQUIERDA', fill= "black", font= ('Helvetica 10 bold'))

        hilera8 = 85
        for i in range(num_buttons-3):
            x1 = x1 + padding
            x2 = x1 + width
            y2 = y1 + height
            indice = self.buscar_valor(hilera8)
            tag_diente = 'D' + str(hilera8)
            self.texto8 = self.canvas.create_text(x1+ width/2, y2+15, text= hilera8, fill= "black", font= ('Helvetica 10 bold'))
                
            if(indice is not None):
                #print(indice)
                if self.dientes[indice][7] == 'red' or self.dientes[indice][7] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, width= 2, outline= self.dientes[indice][7])
                elif self.dientes[indice][8] == 'red' or self.dientes[indice][8] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_line(x1+5, y1+5, x2-5, y2-5, fill= self.dientes[indice][8], width= 2)
                    self.canvas.create_line(x1+5, y2-5, x2-5, y1+5, fill= self.dientes[indice][8], width= 2)
                else:
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= self.dientes[indice][2], outline = "black")#DISTAL
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= self.dientes[indice][5], outline = "black")#INTERIOR
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][4], outline = "black")#MEDIAL
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][3], outline = "black")#VESTIBULAR
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= self.dientes[indice][6], tags= tag_diente)#OCLUSAL
            else:
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
            x1 = x2
            self.canvas.tag_bind(tag_diente, '<Enter>', self.change_cursor_enter)
            self.canvas.tag_bind(tag_diente, '<Leave>', self.change_cursor_leave)
            self.canvas.tag_bind(tag_diente, '<Button-1>', lambda event, numero= hilera8: self.editar_diente(numero))
            hilera8-=1
        x1 = x2+11
        y1 = y2-height
        hilera7 = 71
        for i in range(num_buttons-3):
            x1 = x1 + padding
            x2 = x1 + width
            y2 = y1 + height
            indice = self.buscar_valor(hilera7)
            self.texto3 = self.canvas.create_text(x1+ width/2, y2+15, text= hilera7, fill= "black", font= ('Helvetica 10 bold'))
            tag_diente = 'D' + str(hilera7)
            if(indice is not None):
                #print(indice)
                if self.dientes[indice][7] == 'red' or self.dientes[indice][7] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, width= 5, outline= self.dientes[indice][7])
                elif self.dientes[indice][8] == 'red' or self.dientes[indice][8] == 'blue':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_line(x1+5, y1+5, x2-5, y2-5, fill= self.dientes[indice][8], width= 5)
                    self.canvas.create_line(x1+5, y2-5, x2-5, y1+5, fill= self.dientes[indice][8], width= 5)
                else:
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= self.dientes[indice][5], outline = "black")#MEDIAL
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= self.dientes[indice][4], outline = "black")#INTERIOR
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][3], outline = "black")#DISTAL
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][2], outline = "black")#VESTIBULAR
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= self.dientes[indice][6], tags= tag_diente)#OCLUSAL
            else:
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
            x1 = x2
            self.canvas.tag_bind(tag_diente, '<Enter>', self.change_cursor_enter)
            self.canvas.tag_bind(tag_diente, '<Leave>', self.change_cursor_leave)
            self.canvas.tag_bind(tag_diente, '<Button-1>', lambda event, numero= hilera7: self.editar_diente(numero))
            hilera7+=1
        x1 = padding
        y1 = 30

'''        
#def button_click(event, index):
    #canvas.itemconfig(buttons[index], fill="red")
#def cargar_dientes():

def editar_diente( numero):
    print('prueba', numero)
    diente= Diente()
'''
if __name__ == "__main__":
    Odontograma()    