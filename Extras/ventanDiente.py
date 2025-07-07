from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageDraw, ImageTk
##self.numero_actual = numero
ventana_secundaria = tk.Tk()
ventana_secundaria.title("Editar diente")
ventana_secundaria.geometry('300x350')
##        utl.centrar_ventana(self.ventana_secundaria, 300, 350)
##        self.ventana_secundaria.grab_set_global() # Obliga a las ventanas estar deshabilitadas y deshabilitar todos los eventos e interacciones con la ventana
##        self.ventana_secundaria.focus_set() # Mantiene el foco cuando se abre la ventana.
def create_circle_image(color, radius=15, outline_width=3):
    size = radius * 2 + outline_width
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))  # Fondo transparente
    draw = ImageDraw.Draw(img)
    draw.ellipse(
        (outline_width, outline_width, size-outline_width, size-outline_width),
        outline=color,
        width=outline_width
    )
    return ImageTk.PhotoImage(img)
def crear_imagen_x(color):
    img = Image.new("RGBA", (30, 30), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.line((5, 5, 25, 25), fill=color, width=3)
    draw.line((25, 5, 5, 25), fill=color, width=3)
    return ImageTk.PhotoImage(img)

img = create_circle_image("red")

Label(ventana_secundaria, text= "EDITAR DIENTE", font= ("Arial", 15, 'bold'), fg= 'white', bg= "gray", width= 60).pack(pady= 10)
Label(ventana_secundaria, text= "DIENTE "+str(10000), font= ("Arial", 12, 'bold'), fg= 'white', bg= "gray", width= 60).pack()
diente_frame = Frame(ventana_secundaria)
diente_frame.pack(pady= (10, 10))
botones_frame = Frame(ventana_secundaria)
botones_frame.pack(pady= (10, 10))
boton_extraccion=Button(botones_frame, image=img, text= 'Extracción', bg= "gray90")
boton_extraccion.grid(row= 0, column= 0, padx= 10)
corona_azul = create_circle_image("blue")
boton_extraccion=Button(botones_frame, image=corona_azul, text= 'Extracción', bg= "gray90")
boton_extraccion.grid(row= 0, column= 1, padx= 10)
corona_verde = create_circle_image("green")
boton_extraccion=Button(botones_frame, image=corona_verde, text= 'Extracción', bg= "gray90")
boton_extraccion.grid(row= 0, column= 2, padx= 10)
extraccion_azul = crear_imagen_x("blue")
boton_extraccion=Button(botones_frame, image=extraccion_azul, text= 'Extracción', bg= "gray90")
boton_extraccion.grid(row= 1, column= 0, padx= 10)
##corona_azul = create_circle_image("blue")
##boton_extraccion=Button(botones_frame, image=corona_azul, text= 'Extracción', bg= "gray90")
##boton_extraccion.grid(row= 1, column= 1, padx= 10)
##corona_verde = create_circle_image("green")
##boton_extraccion=Button(botones_frame, image=corona_verde, text= 'Extracción', bg= "gray90")
##boton_extraccion.grid(row= 1, column= 2, padx= 10)
##        #Button(botones_frame, text= 'X Azul', command= partial(self.extraccion, numero), bg= "blue", width= 5).grid(row= 0, column= 1, padx= 10)
##        self.boton_corona=Button(botones_frame, text= 'Corona', command= self.corona, bg= "white", width= 8)
##        self.boton_corona.grid(row= 0, column= 1, padx= 10)
##        #Button(botones_frame, text= 'O Azul', command= partial(self.corona, numero), bg= "blue", width= 5).grid(row= 0, column= 3, padx= 10)
##        Button(botones_frame, text= 'CANCELAR', command= self.cancelar, width= 8).grid(row= 1, column= 1, padx= 10, pady=(10, 0))
##        Button(botones_frame, text= 'GUARDAR', command= self.guardar_diente, font= self.fuenteb, bg= '#1F704B', fg= 'white', width= 8).grid(row= 1, column= 0, padx= 10, pady=(10, 0))
##
##        self.canvas2 = tk.Canvas(diente_frame, width= 400, height= 150)
##        self.canvas2.pack()
##        if self.dientes == []:
##            self.diente_actual=[0, numero, self.ID_odonto, 'white','white','white','white','white','white','white']
##        for diente in self.dientes:
##            if diente[1] == numero:
##                #print("numero", diente)
##                self.diente_actual=list(diente)
##                break
##            else:
##                self.diente_actual=[0, numero, self.ID_odonto, 'white','white','white','white','white','white','white']
##
##        #print("diente cargado", self.diente_actual)
##        width = 100
##        height = 100
##        x1 = 100
##        y1 = 25
##        x2 = x1 + width
##        y2 = y1 + height
##        #LETRAS
##        if numero == 11 or numero == 12 or numero == 13 or numero == 14 or numero == 15 or numero == 16 or numero == 17 or numero == 18 \
##            or numero == 51 or numero == 52 or numero == 53 or numero == 54 or numero == 55:
##            self.canvas2.create_text(x1+ width/2, 15, text= 'V', fill= "black", font= ('Helvetica 10 bold'))
##            self.canvas2.create_text(x1-10, 25+ width/2, text= 'D', fill= "black", font= ('Helvetica 10 bold'))
##            self.canvas2.create_text(x1+ width/2, 35+ height, text= 'P', fill= "black", font= ('Helvetica 10 bold'))
##            self.canvas2.create_text(x1+ width+10, 25+ width/2, text= 'M', fill= "black", font= ('Helvetica 10 bold'))
##            if self.diente_actual[9] == 'red' or self.diente_actual[9] == 'blue'  or self.diente_actual[9] == 'green':
##                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= 'white', outline = "black", tags= 'C1')
##                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= 'white', outline = "black", tags= 'C2')
##                self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C3')
##                self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C4')
##                self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= 'white', tags= 'CO')
##                self.canvas2.create_oval(x1+5, y1+5, x2-5, y2-5, width= 5, outline= self.diente_actual[9])
##                self.boton_corona.config(bg=self.determinar_color(self.diente_actual[9]))
##            elif self.diente_actual[8] == 'red' or self.diente_actual[8] == 'blue' or self.diente_actual[8] == 'green':
##                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= 'white', outline = "black", tags= 'C1')
##                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= 'white', outline = "black", tags= 'C2')
##                self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C3')
##                self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C4')
##                self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= 'white', tags= 'CO')
##                self.canvas2.create_line(x1+5, y1+5, x2-5, y2-5, fill= self.diente_actual[8], width= 5)
##                self.canvas2.create_line(x1+5, y2-5, x2-5, y1+5, fill= self.diente_actual[8], width= 5)
##                self.boton_extraccion.config(bg=self.determinar_color(self.diente_actual[8]))
##            else:
##                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= self.diente_actual[3], outline = "black", tags= 'C1')
##                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= self.diente_actual[4], outline = "black", tags= 'C2')
##                self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= self.diente_actual[5], outline = "black", tags= 'C3')
##                self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= self.diente_actual[6], outline = "black", tags= 'C4')
##                self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= self.diente_actual[7], tags= 'CO')
##            self.canvas2.tag_bind('C1', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C1'))
##            self.canvas2.tag_bind('C2', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C2'))
##            self.canvas2.tag_bind('C3', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C3'))
##            self.canvas2.tag_bind('C4', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C4'))
##            self.canvas2.tag_bind('CO', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'CO'))
##        elif numero == 21 or numero == 22 or numero == 23 or numero == 24 or numero == 25 or numero == 26 or numero == 27 or numero == 28 \
##            or numero == 61 or numero == 62 or numero == 63 or numero == 64 or numero == 65:
##            self.canvas2.create_text(x1+ width/2, 15, text= 'V', fill= "black", font= ('Helvetica 10 bold'))
##            self.canvas2.create_text(x1-10, 25+ width/2, text= 'M', fill= "black", font= ('Helvetica 10 bold'))
##            self.canvas2.create_text(x1+ width/2, 35+ height, text= 'P', fill= "black", font= ('Helvetica 10 bold'))
##            self.canvas2.create_text(x1+ width+10, 25+ width/2, text= 'D', fill= "black", font= ('Helvetica 10 bold'))
##            if self.diente_actual[9] == 'red' or self.diente_actual[9] == 'blue' or self.diente_actual[9] == 'green':
##                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= 'white', outline = "black", tags= 'C1')
##                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= 'white', outline = "black", tags= 'C2')
##                self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C3')
##                self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C4')
##                self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= 'white', tags= 'CO')
##                self.canvas2.create_oval(x1+5, y1+5, x2-5, y2-5, width= 5, outline= self.diente_actual[9])
##                self.boton_corona.config(bg=self.determinar_color(self.diente_actual[9]))
##            elif self.diente_actual[8] == 'red' or self.diente_actual[8] == 'blue' or self.diente_actual[8] == 'green':
##                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= 'white', outline = "black", tags= 'C1')
##                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= 'white', outline = "black", tags= 'C2')
##                self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C3')
##                self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C4')
##                self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= 'white', tags= 'CO')
##                self.canvas2.create_line(x1+5, y1+5, x2-5, y2-5, fill= self.diente_actual[8], width= 5)
##                self.canvas2.create_line(x1+5, y2-5, x2-5, y1+5, fill= self.diente_actual[8], width= 5)
##                self.boton_extraccion.config(bg= self.determinar_color(self.diente_actual[8]))
##            else:
##                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= self.diente_actual[5], outline = "black", tags= 'C1')
##                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= self.diente_actual[4], outline = "black", tags= 'C2')
##                self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= self.diente_actual[3], outline = "black", tags= 'C3')
##                self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= self.diente_actual[6], outline = "black", tags= 'C4')
##                self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= self.diente_actual[7], tags= 'CO')
##
##            self.canvas2.tag_bind('C1', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C1'))
##            self.canvas2.tag_bind('C2', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C2'))
##            self.canvas2.tag_bind('C3', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C3'))
##            self.canvas2.tag_bind('C4', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C4'))
##            self.canvas2.tag_bind('CO', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'CO'))
##        elif numero == 31 or numero == 32 or numero == 33 or numero == 34 or numero == 35 or numero == 36 or numero == 37 or numero == 38 \
##            or numero == 71 or numero == 72 or numero == 73 or numero == 74 or numero == 75:
##            self.canvas2.create_text(x1+ width/2, 15, text= 'L', fill= "black", font= ('Helvetica 10 bold'))
##            self.canvas2.create_text(x1-10, 25+ width/2, text= 'M', fill= "black", font= ('Helvetica 10 bold'))
##            self.canvas2.create_text(x1+ width/2, 35+ height, text= 'V', fill= "black", font= ('Helvetica 10 bold'))
##            self.canvas2.create_text(x1+ width+10, 25+ width/2, text= 'D', fill= "black", font= ('Helvetica 10 bold'))
##            if self.diente_actual[9] == 'red' or self.diente_actual[9] == 'blue' or self.diente_actual[9] == 'green':
##                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= 'white', outline = "black", tags= 'C1')
##                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= 'white', outline = "black", tags= 'C2')
##                self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C3')
##                self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C4')
##                self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= 'white', tags= 'CO')
##                self.canvas2.create_oval(x1+5, y1+5, x2-5, y2-5, width= 5, outline= self.diente_actual[9])
##                self.boton_corona.config(bg=self.determinar_color(self.diente_actual[9]))
##            elif self.diente_actual[8] == 'red' or self.diente_actual[8] == 'blue' or self.diente_actual[8] == 'green':
##                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= 'white', outline = "black", tags= 'C1')
##                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= 'white', outline = "black", tags= 'C2')
##                self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C3')
##                self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C4')
##                self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= 'white', tags= 'CO')
##                self.canvas2.create_line(x1+5, y1+5, x2-5, y2-5, fill= self.diente_actual[8], width= 5)
##                self.canvas2.create_line(x1+5, y2-5, x2-5, y1+5, fill= self.diente_actual[8], width= 5)
##                self.boton_extraccion.config(bg= self.determinar_color(self.diente_actual[8]))
##            else:
##                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= self.diente_actual[5], outline = "black", tags= 'C1')
##                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= self.diente_actual[4], outline = "black", tags= 'C2')
##                self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= self.diente_actual[3], outline = "black", tags= 'C3')
##                self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= self.diente_actual[4], outline = "black", tags= 'C4')
##                self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= self.diente_actual[7], tags= 'CO')
##
##            self.canvas2.tag_bind('C1', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C1'))
##            self.canvas2.tag_bind('C2', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C2'))
##            self.canvas2.tag_bind('C3', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C3'))
##            self.canvas2.tag_bind('C4', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C4'))
##            self.canvas2.tag_bind('CO', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'CO'))
##        elif numero == 41 or numero == 42 or numero == 43 or numero == 44 or numero == 45 or numero == 46 or numero == 47 or numero == 48 \
##            or numero == 81 or numero == 82 or numero == 83 or numero == 84 or numero == 85:
##            self.canvas2.create_text(x1+ width/2, 15, text= 'L', fill= "black", font= ('Helvetica 10 bold'))
##            self.canvas2.create_text(x1-10, 25+ width/2, text= 'D', fill= "black", font= ('Helvetica 10 bold'))
##            self.canvas2.create_text(x1+ width/2, 35+ height, text= 'V', fill= "black", font= ('Helvetica 10 bold'))
##            self.canvas2.create_text(x1+ width+10, 25+ width/2, text= 'M', fill= "black", font= ('Helvetica 10 bold'))
##            if self.diente_actual[9] == 'red' or self.diente_actual[9] == 'blue'or self.diente_actual[9] == 'green':
##                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= 'white', outline = "black", tags= 'C1')
##                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= 'white', outline = "black", tags= 'C2')
##                self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C3')
##                self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C4')
##                self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= 'white', tags= 'CO')
##                self.canvas2.create_oval(x1+5, y1+5, x2-5, y2-5, width= 5, outline= self.diente_actual[9])
##                self.boton_corona.config(bg=self.determinar_color(self.diente_actual[9]))
##            elif self.diente_actual[8] == 'red' or self.diente_actual[8] == 'blue' or self.diente_actual[8] == 'green':
##                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= 'white', outline = "black", tags= 'C1')
##                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= 'white', outline = "black", tags= 'C2')
##                self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C3')
##                self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C4')
##                self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= 'white', tags= 'CO')
##                self.canvas2.create_line(x1+5, y1+5, x2-5, y2-5, fill= self.diente_actual[8], width= 5)
##                self.canvas2.create_line(x1+5, y2-5, x2-5, y1+5, fill= self.diente_actual[8], width= 5)
##                self.boton_extraccion.config(bg= self.determinar_color(self.diente_actual[8]))
##            else:
##                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= self.diente_actual[3], outline = "black", tags= 'C1')
##                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= self.diente_actual[6], outline = "black", tags= 'C2')
##                self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= self.diente_actual[5], outline = "black", tags= 'C3')
##                self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= self.diente_actual[4], outline = "black", tags= 'C4')
##                self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= self.diente_actual[7], tags= 'CO')
##
##            self.canvas2.tag_bind('C1', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C1'))
##            self.canvas2.tag_bind('C2', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C2'))
##            self.canvas2.tag_bind('C3', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C3'))
##            self.canvas2.tag_bind('C4', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C4'))
##            self.canvas2.tag_bind('CO', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'CO'))
##
##        else:
##            self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= 'white', outline = "black", tags= 'C1')
##            self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= 'white', outline = "black", tags= 'C2')
##            self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C3')
##            self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C4')
##            self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= 'white', tags= 'CO')
##
##            self.canvas2.tag_bind('C1', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C1'))
##            self.canvas2.tag_bind('C2', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C2'))
##            self.canvas2.tag_bind('C3', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C3'))
##            self.canvas2.tag_bind('C4', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C4'))
##            self.canvas2.tag_bind('CO', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'CO'))
ventana_secundaria.mainloop()