import tkinter as tk
from tkinter import Frame, Label, Button, Toplevel
import sqlite3
from tkinter import *

from PIL import ImageGrab
from datetime import datetime
color_index = 0
colores2 = ['white', 'blue', 'red']

class Diente:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ventana_secundaria = tk.Tk()
        ventana_secundaria.title("Editar diente")
        ventana_secundaria.geometry('400x300')
        ventana_secundaria.grab_set_global() # Obliga a las ventanas estar deshabilitadas y deshabilitar todos los eventos e interacciones con la ventana
        ventana_secundaria.focus_set() # Mantiene el foco cuando se abre la ventana.
        ventana_secundaria.config(bg= 'gray')
        #item = self.tabla_turnos.focus()
        #print(self.turno_seleccionado)
        # self.horario = self.data['values'][0]
        # self.paciente = self.data['values'][1]
        # self.prestacion = self.data['values'][2]
        # self.odontologo = self.data['values'][3]
        Label(ventana_secundaria, text="EDITAR DIENTE", font=("Arial", 15, 'bold'), bg="gray90", width=60).pack(pady=10)
        Label(ventana_secundaria, text="FECHA: DD/MM/AAAA ", font=("Arial", 10, 'bold'), bg="gray90", width=60).pack()
        diente_frame = Frame(ventana_secundaria)
        diente_frame.pack(pady=(10,10))
        self.canvas = tk.Canvas(diente_frame, width=400, height=150)
        self.canvas.pack()
        width = 100
        height = 100
        x1=100
        y1=25
        x2 = x1 + width
        y2 = y1 + height    
        cara_d=self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2,fill="white", outline = "black")
        self.canvas.tag_bind(cara_d, '<Button-1>', lambda event: self.cambiar_color(cara_d))
    # cara_v=c.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1,fill="white", outline = "black")
    # c.tag_bind(cara_v, '<Button-1>', lambda event: cambiar_color())
    # cara_i=c.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2,fill="white", outline = "black")
    # c.tag_bind(cara_i, '<Button-1>', lambda event: cambiar_color())
        cara_m=self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2,fill="white", outline = "black")
        self.canvas.tag_bind(cara_m, '<Button-1>', lambda event: self.cambiar_color(cara_m))
        #self.canvas.itemconfig(cara_m, fill='gray')
        cara_o=self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill="white")
        self.canvas.tag_bind(cara_o, '<Button-1>', lambda event: self.cambiar_color(cara_o))
        button_frame = Frame(ventana_secundaria, bg="gray")
        button_frame.pack(pady=10)

    #Button(button_frame, text= 'Guardar', command= guardar_turno, bg= "#BDC1BE", width= 10).grid(row= 0, column= 0, padx= 10)
    #Button(button_frame, text= 'Eliminar', command= self.eliminar_turno, bg= "#BDC1BE", width= 10).grid(row= 0, column= 1, padx= 10)
        Button(button_frame, text= 'Salir', command= ventana_secundaria.destroy, bg= "orange red", width= 10).grid(row= 0, column= 2, padx= 10)
# try:
#     miConexion=sqlite3.connect("../bd/DBpaciente.sqlite3")
#     miCursor=miConexion.cursor()
#     sql = "SELECT Apellido, Nombre, DNI, Telefono, ObraSocial FROM Paciente ORDER BY Apellido"
#     miCursor.execute(sql)
#     pacientes = miCursor.fetchall()
#     miConexion.commit()
#     #print(pacientes)
# except:
#     print("error")



# def editar_diente( numero):
#     print('prueba', numero)

        ventana_secundaria.mainloop()

    def cambiar_color(self, cara):
        global color_index
        color_index = (color_index + 1) % len(colores2)
        color_actual = colores2[color_index]
        #print('hola')
        self.canvas.itemconfig(cara, fill=color_actual)
    #label_color_actual.config(text=f"Color actual: {color_actual.capitalize()}")
        
# def change_cursor_enter(event):
#     # Cambiar el cursor al pasar sobre un cuadrado
#     canvas.config(cursor="hand2")
    
# def change_cursor_leave(event):
#     # Restaurar el cursor al salir del cuadrado
#     canvas.config(cursor="")
# crear_dientes()
#capture_screenshot()
if __name__ == "__main__":
    Diente()    