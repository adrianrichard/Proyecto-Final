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
root = tk.Tk()
#root.configure(padx = 10, pady = 10)
buttons = []
fecha_actual = datetime.now().date()
fecha_actual = fecha_actual.strftime("%d-%m-%Y")
#print(fecha_actual)
try:
    miConexion=sqlite3.connect("../bd/DBpaciente.sqlite3")
    miCursor=miConexion.cursor()
    sql = "SELECT Apellido, Nombre, DNI, Telefono, ObraSocial FROM Paciente ORDER BY Apellido"
    miCursor.execute(sql)
    pacientes = miCursor.fetchall()
    miConexion.commit()
    #print(pacientes)
except:
    print("error")
print(pacientes[0][2])
datos= pacientes[0][2], fecha_actual, 'Militello'
print(datos)
# try:
#     miConexion=sqlite3.connect("../bd/DBpaciente.sqlite3")
#     miCursor=miConexion.cursor()
#     datos= pacientes[0][2], fecha_actual, 'Militello'
#     sql = "INSERT INTO Odontograma (DNI_paciente, Fecha, Doctor) VALUES ( ?, ?, ?)"
#     miCursor.execute(sql, datos)
#     miConexion.commit()
#     #print(pacientes)
# except:
#     print("error")

colores=["red", "yellow", "blue","white"]

ancho = 850
Label(root, text='Odontograma', font='Arial 20 bold').grid(column=0, row=0)
nombre=pacientes[0][1]
apellido=pacientes[0][0]
obra_social=pacientes[0][4]
dni=pacientes[0][2]
frame_datos_paciente=Frame(root, border=1, borderwidth=2)
frame_datos_paciente.grid(column=0, row=1)
Label(frame_datos_paciente, text='Nombre Completo: '+apellido+', '+nombre, font='Arial 15').grid(column=0, row=0, sticky='e', padx=(5,15))
Label(frame_datos_paciente, text='Obra Social: '+obra_social,  font='Arial 15').grid(column=1, row=0, sticky='e', padx=(5,15))
Label(frame_datos_paciente, text='D.N.I.: '+str(dni),  font='Arial 15').grid(column=2, row=0, sticky='e', padx=(5,15))
frame_dientes = Frame(root)
frame_dientes.grid(column=0, row=2, pady=(10,10))
canvas = tk.Canvas(frame_dientes, width=ancho, height=600)
canvas.pack()

#def button_click(event, index):
    #canvas.itemconfig(buttons[index], fill="red")
def cargar_dientes():
    try:
        miConexion=sqlite3.connect("../bd/DBpaciente.sqlite3")
        miCursor=miConexion.cursor()
        sql = "SELECT ID_odontograma from Odontograma ORDER BY ID_odontograma DESC LIMIT 1"
        miCursor.execute(sql)
        miConexion.commit()
        ID_odonto_actual= miCursor.fetchone()
        print(ID_odonto_actual[0])
    except:
        print("error diente")

def crear_dientes():
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

        canvas.create_text(x1+ width/2, 15, text=hilera1, fill="black", font=('Helvetica 10 bold'))
        canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
        canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
        canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
        canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
        canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
        hilera1-=1
        if corona:
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
            canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
            canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
            canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
            canvas.create_oval(x1+5,y1+5,x2-5,y2-5, width=5, outline="blue")
        if extraido:
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
            canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
            canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
            canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
            canvas.create_line(x1+5,y1+5,x2-5,y2-5, fill="red", width=5)
            canvas.create_line(x1+5,y2-5,x2-5,y1+5, fill="red", width=5)

        x1=x2
    #linea horizontal
    canvas.create_line(0, y2+padding, ancho, y2+padding, width=3)
    x1=x1+10
    #linea vertical
    canvas.create_line(x1, 5, x1, 320, width=3)
    
    #2da hilera
    hilera2=21
    for i in range(num_buttons):
        x1 = x1 + padding
        y1 = 30
        x2 = x1 + width
        y2 = y1 + height
        canvas.create_text(x1+ width/2, 15, text=hilera2, fill="black", font=('Helvetica 10 bold'))
        hilera2+=1
        #corona=True
        if corona:
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
            canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
            canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
            canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
            canvas.create_oval(x1+5, y1+5, x2-5, y2-5, width=5, outline="blue")
        if extraido:
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
            canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
            canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
            canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
            canvas.create_line(x1+5, y1+5, x2-5, y2-5, fill="red", width=5)
            canvas.create_line(x1+5, y2-5, x2-5, y1+5, fill="red", width=5)
        else:
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill=colores[i%3], outline = "black")
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill=colores[i%2], outline = "black")
            canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill=colores[2], outline = "black")
            canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill=colores[i%1], outline = "black")
            canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
        x1=x2
    y1=y2+20
    x1=0
    #4ta hilera
    hilera4=48
    for i in range(num_buttons):
        x1 = x1 + padding       
        x2 = x1 + width
        y2 = y1 + height
        canvas.create_text(x1+ width/2, y2+15, text=hilera4, fill="black", font=('Helvetica 10 bold'))
        hilera4-=1                
        if corona:
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
            canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
            canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
            canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
            canvas.create_oval(x1+5, y1+5, x2-5, y2-5, width=5, outline="blue")

        elif extraido:                    
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2,fill="white", outline = "black")
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1,fill="white", outline = "black")
            canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2,fill="white", outline = "black")
            canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2,fill="white", outline = "black")
            canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
            canvas.create_line(x1+5,y1+5,x2-5,y2-5, fill="red", width=5)
            canvas.create_line(x1+5,y2-5,x2-5,y1+5, fill="red", width=5)
        else:
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2,fill=colores[0], outline = "black")
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1,fill=colores[1], outline = "black")
            canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2,fill=colores[2], outline = "black")
            canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2,fill=colores[3], outline = "black")
            canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
        x1=x2
    x1=x1+10
    #3ra hilera
    hilera3=31
    for i in range(num_buttons):
        x1 = x1 + padding
        x2 = x1 + width
        y2 = y1 + height
        canvas.create_text(x1+ width/2, y2+15, text=hilera3, fill="black", font=('Helvetica 10 bold'))
        hilera3+=1
        if corona:            
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2,fill="white", outline = "black")
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1,fill="white", outline = "black")
            canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2,fill="white", outline = "black")
            canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2,fill="white", outline = "black")
            canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
            canvas.create_oval(x1+5,y1+5,x2-5,y2-5, width=5, outline="blue")
        elif extraido:                    
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2,fill="white", outline = "black")
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1,fill="white", outline = "black")
            canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2,fill="white", outline = "black")
            canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2,fill="white", outline = "black")
            canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
            canvas.create_line(x1+5,y1+5,x2-5,y2-5, fill="red", width=5)
            canvas.create_line(x1+5,y2-5,x2-5,y1+5, fill="red", width=5)
        else:
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2,fill=colores[0], outline = "black")
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1,fill=colores[1], outline = "black")
            canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2,fill=colores[2], outline = "black")
            canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2,fill=colores[3], outline = "black")
            canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
        x1=x2
    x1=138
    y1=y2 + 60
    hilera5=55
    for i in range(num_buttons-3):
        x1 = x1 + padding
        x2 = x1 + width
        y2 = y1 + height
        canvas.create_text(x1+ width/2, y1-15, text=hilera5, fill="black", font=('Helvetica 10 bold'))
        hilera5-=1
        if corona:
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
            canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
            canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
            canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
            canvas.create_oval(x1+5, y1+5, x2-5, y2-5, width=5, outline="blue")
        elif extraido:                    
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2,fill="white", outline = "black")
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1,fill="white", outline = "black")
            canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2,fill="white", outline = "black")
            canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2,fill="white", outline = "black")
            canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
            canvas.create_line(x1+5,y1+5,x2-5,y2-5, fill="red", width=5)
            canvas.create_line(x1+5,y2-5,x2-5,y1+5, fill="red", width=5)
        else:
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2,fill=colores[0], outline = "black")
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1,fill=colores[1], outline = "black")
            canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2,fill=colores[2], outline = "black")
            canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2,fill=colores[3], outline = "black")
            canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
        x1=x2
    x1=x2+11
    #y1= 195
    hilera6=61
    for i in range(num_buttons-3):
        x1 = x1 + padding
        x2 = x1 + width
        y2 = y1 + height
        canvas.create_text(x1+ width/2, y1-15, text=hilera6, fill="black", font=('Helvetica 10 bold'))
        hilera6+=1
        if corona:
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
            canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
            canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
            canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
            canvas.create_oval(x1+5, y1+5, x2-5, y2-5, width=5, outline="blue")
        elif extraido:                    
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2,fill="white", outline = "black")
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1,fill="white", outline = "black")
            canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2,fill="white", outline = "black")
            canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2,fill="white", outline = "black")
            canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
            canvas.create_line(x1+5,y1+5,x2-5,y2-5, fill="red", width=5)
            canvas.create_line(x1+5,y2-5,x2-5,y1+5, fill="red", width=5)
        else:
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2,fill=colores[0], outline = "black")
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1,fill=colores[1], outline = "black")
            canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2,fill=colores[2], outline = "black")
            canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2,fill=colores[3], outline = "black")
            canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
        x1=x2
    x1=138
    y1=y2 + 10
    hilera8=85
    for i in range(num_buttons-3):
        x1 = x1 + padding
        x2 = x1 + width
        y2 = y1 + height
        canvas.create_text(x1+ width/2, y2+15, text=hilera8, fill="black", font=('Helvetica 10 bold'))
        hilera8-=1
        if corona:            
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
            canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
            canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
            canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
            canvas.create_oval(x1+5, y1+5, x2-5, y2-5, width=5, outline="blue")
        elif extraido:                    
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2,fill="white", outline = "black")
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1,fill="white", outline = "black")
            canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2,fill="white", outline = "black")
            canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2,fill="white", outline = "black")
            canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
            canvas.create_line(x1+5,y1+5,x2-5,y2-5, fill="red", width=5)
            canvas.create_line(x1+5,y2-5,x2-5,y1+5, fill="red", width=5)
        else:
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2,fill=colores[3], outline = "black")
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1,fill=colores[1], outline = "black")
            canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2,fill=colores[2], outline = "black")
            canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2,fill=colores[3], outline = "black")
            canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
        x1=x2
    x1=x2+11
    y1= y2-height
    hilera7=71
    for i in range(num_buttons-3):
        x1 = x1 + padding
        x2 = x1 + width
        y2 = y1 + height
        canvas.create_text(x1+ width/2, y2+15, text=hilera7, fill="black", font=('Helvetica 10 bold'))
        
        tag=str(hilera7)
        if corona:
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill="white", outline = "black")
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill="white", outline = "black")
            canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
            canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill="white", outline = "black")
            canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
            canvas.create_oval(x1+5, y1+5, x2-5, y2-5, width=5, outline="blue")
        elif extraido:
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2,fill="white", outline = "black")
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1,fill="white", outline = "black")
            canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2,fill="white", outline = "black")
            canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2,fill="white", outline = "black")
            canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
            canvas.create_line(x1+5,y1+5,x2-5,y2-5, fill="red", width=5)
            canvas.create_line(x1+5,y2-5,x2-5,y1+5, fill="red", width=5)
        else:
            
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2,fill=colores[0], outline = "black")
            canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1,fill=colores[1], outline = "black")
            canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2,fill=colores[2], outline = "black")
            canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2,fill=colores[3], outline = "black")
            canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
            
            
        hilera7+=1
        x1=x2
    x1=padding
    y1=30
    
    D18=canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x1 + width - width/3.0, y1 + height - height/3.0, fill="green", tags="D18")
    canvas.tag_bind('D18', '<Enter>', change_cursor_enter)
    canvas.tag_bind('D18', '<Leave>', change_cursor_leave)
    canvas.tag_bind('D18', '<Button-1>', editar_diente)
    canvas.tag_bind('D18', '<Button-1>', lambda event, numero=18: editar_diente(numero))
    D17=canvas.create_rectangle(x1 + width +padding+ width/3.0, y1 + height/3.0, x1 +padding+ 2*width - width/3.0, y1 + height - height/3.0, fill="green", tags="D17")
    canvas.tag_bind('D17', '<Enter>', change_cursor_enter)
    canvas.tag_bind('D17', '<Leave>', change_cursor_leave)
    canvas.tag_bind('D17', '<Button-1>', lambda event, numero=17: editar_diente(numero))

color_index = 0
colores2 = ['white', 'blue', 'red']

def editar_diente( numero):
    print('prueba', numero)
    diente= Diente()
    

#     ventana_secundaria = tk.Toplevel(root, background='gray')
#     ventana_secundaria.title("Editar diente")
#     ventana_secundaria.geometry('400x300')
#     ventana_secundaria.grab_set_global() # Obliga a las ventanas estar deshabilitadas y deshabilitar todos los eventos e interacciones con la ventana
#     ventana_secundaria.focus_set() # Mantiene el foco cuando se abre la ventana.
    
#         #item = self.tabla_turnos.focus()
#         #print(self.turno_seleccionado)
#         # self.horario = self.data['values'][0]
#         # self.paciente = self.data['values'][1]
#         # self.prestacion = self.data['values'][2]
#         # self.odontologo = self.data['values'][3]
#     Label(ventana_secundaria, text="EDITAR DIENTE", font=("Arial", 15, 'bold'), bg="gray90", width=60).pack(pady=10)
#     Label(ventana_secundaria, text="FECHA: DD/MM/AAAA ", font=("Arial", 10, 'bold'), bg="gray90", width=60).pack()
#     diente_frame = Frame(ventana_secundaria)
#     diente_frame.pack(pady=(10,10))
#     c = tk.Canvas(diente_frame, width=400, height=150)
#     c.pack()
#     width = 100
#     height = 100
#     x1=100
#     y1=25
#     x2 = x1 + width
#     y2 = y1 + height    
#     # cara_d=c.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2,fill="white", outline = "black")
#     # c.tag_bind(cara_d, '<Button-1>', lambda event: cambiar_color())
#     # cara_v=c.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1,fill="white", outline = "black")
#     # c.tag_bind(cara_v, '<Button-1>', lambda event: cambiar_color())
#     # cara_i=c.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2,fill="white", outline = "black")
#     # c.tag_bind(cara_i, '<Button-1>', lambda event: cambiar_color())
#     cara_m=c.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2,fill="white", outline = "black")
#     #c.tag_bind(cara_m, '<Button-1>', lambda event: cambiar_color())
#     c.itemconfig(cara_m, fill='gray')
#     cara_o=c.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
#     c.tag_bind(cara_o, '<Button-1>', lambda event: cambiar_color(cara_o, c))
#     button_frame = Frame(ventana_secundaria, bg="gray")
#     button_frame.pack(pady=10)

#     #Button(button_frame, text= 'Guardar', command= guardar_turno, bg= "#BDC1BE", width= 10).grid(row= 0, column= 0, padx= 10)
#     #Button(button_frame, text= 'Eliminar', command= self.eliminar_turno, bg= "#BDC1BE", width= 10).grid(row= 0, column= 1, padx= 10)
#     Button(button_frame, text= 'Salir', command= ventana_secundaria.destroy, bg= "orange red", width= 10).grid(row= 0, column= 2, padx= 10)

# def cambiar_color(cara, c):
#     global color_index, canvas
#     color_index = (color_index + 1) % len(colores2)
#     color_actual = colores2[color_index]
#     print('hola')
#     c.canvas.itemconfig(cara, fill="red")
#     #label_color_actual.config(text=f"Color actual: {color_actual.capitalize()}")
        
def change_cursor_enter(event):
    # Cambiar el cursor al pasar sobre un cuadrado
    canvas.config(cursor="hand2")
    
def change_cursor_leave(event):
    # Restaurar el cursor al salir del cuadrado
    canvas.config(cursor="")
crear_dientes()
cargar_dientes()
#capture_screenshot()
root.mainloop()
