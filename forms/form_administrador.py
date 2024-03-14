import tkinter as tk
from tkinter.font import BOLD
from tkinter import ttk
import util.generic as utl
from tkinter import  Button, messagebox, Label, ttk, PhotoImage
from tkinter import  StringVar, Frame
from forms.form_paciente import Paciente
from forms.form_paciente_editar import Paciente_update
from tkcalendar import TKCalendar
from visorimagenes import ImageGalleryApp

import sqlite3

class MasterPanel:    
                                      
    def __init__(self):        
        self.ventana = tk.Tk()                             
        self.ventana.title('DentalMatic')
       # w, h = self.ventana.winfo_screenwidth(), self.ventana.winfo_screenheight()                                    
        self.ventana.geometry('1000x500+180+80')
        self.ventana.config(bg= '#fcfcfc')
        self.ventana.resizable(width= 0, height= 0)
        utl.centrar_ventana(self.ventana, 900, 600)            
        self.menu = True
        self.color = True
        self.dni_paciente =  StringVar()
        self.dato_paciente =  StringVar()

        self.frame_inicio = Frame(self.ventana, bg= '#1F704B', width= 50, height= 45)
        self.frame_inicio.grid_propagate(0)
        self.frame_inicio.grid(column= 0, row= 0, sticky='nsew')
        self.frame_menu = Frame(self.ventana, bg= '#1F704B', width= 50)
        self.frame_menu.grid_propagate(0)
        self.frame_menu.grid(column= 0, row= 1, sticky= 'nsew')
        self.frame_top = Frame(self.ventana, bg= '#1F704B', height= 50)
        self.frame_top.grid(column= 1, row= 0, sticky= 'nsew')
        self.frame_raiz = Frame(self.ventana, bg= '#1F704B')
        self.frame_raiz.grid(column= 1, row= 1, sticky= 'nsew')		
        self.ventana.columnconfigure(1, weight= 1)
        self.ventana.rowconfigure(1, weight= 1)
        self.frame_raiz.columnconfigure(0, weight= 1)
        self.frame_raiz.rowconfigure(0, weight= 1)
        
        self.widgets()

    def pantalla_inicial(self):
        self.paginas.select([self.frame_principal])

    def pantalla_pacientes(self):
        self.paginas.select([self.frame_pacientes])
        [self.frame_pacientes.columnconfigure(i, weight=1) for i in range(self.frame_pacientes.grid_size()[0])]
        [self.frame_tabla_paciente.columnconfigure(i, weight=1) for i in range(self.frame_pacientes.grid_size()[0])]
        [self.frame_tabla_paciente.rowconfigure(i, weight=1) for i in range(self.frame_pacientes.grid_size()[1])]

    def pantalla_calendario(self):        
        self.paginas.select([self.frame_calendario])
        
        Tcal = TKCalendar()
        Tcal.crear_encabezado(self.frame_calendario)
        Tcal.crear_botones_fechas(self.frame_calendario)
        Tcal.actualizar_botones_fechas()
        Tcal.event_color_buttons()
        Tcal.configurar_filas_columnas(self.frame_calendario)

    def pantalla_historia(self):
        self.paginas.select([self.historia])
        self.historia.columnconfigure(0, weight= 1)
        self.historia.columnconfigure(1, weight= 1)
    
    def pantalla_galeria(self):
        self.paginas.select([self.frame_galeria])
        Gallery=ImageGalleryApp(self.frame_galeria)
        Gallery.configurar_filas_columnas(self.frame_galeria)
        

    def pantalla_info(self):
        self.paginas.select([self.frame_info])
    
    def salir(self):
        answer = messagebox.askokcancel(title='Salir', message='¿Desea salir?', icon='warning')
        if answer:
            self.ventana.destroy()
    
    def agregar_paciente(self):
        Paciente()
        
    def editar_paciente(self):
        Paciente_update(self.dni_paciente)        
    
    def eliminar_paciente(self):
        try:
            self.miConexion=sqlite3.connect("./bd/DBpaciente.sqlite3")
            self.miCursor=self.miConexion.cursor()
            msg_box = messagebox.askquestion('Eliminar paciente', '¿Desea elminar al paciente?', icon='warning')
            if msg_box == 'yes':
                self.miCursor.execute("DELETE FROM Paciente WHERE dni = ?", (self.dni_paciente,))
                self.miConexion.commit()
                messagebox.showinfo("ELIMINAR","Paciente eliminado exitosamente")
        except:
            messagebox.showinfo("ELIMINAR", "No se ha podido elimnar el paciente")
        self.mostrar_datos()         
    
    def menu_lateral(self):
        if self.menu is True:
            for i in range(50, 170, 10):
                self.frame_menu.config(width= i)
                self.frame_inicio.config(width= i)
                self.frame_menu.update()
                clik_inicio = self.bt_cerrar.grid_forget()
                if clik_inicio is None:
                    self.bt_inicio.grid(column= 0, row= 0, padx= 10, pady= 10)
                    self.bt_inicio.grid_propagate(0)
                    self.bt_inicio.config(width= i)
                    self.pantalla_inicial()
            self.menu = False
        else:
            for i in range(170, 50, -10):
                self.frame_menu.config(width=  i)
                self.frame_inicio.config(width= i)
                self.frame_menu.update()
                clik_inicio = self.bt_inicio.grid_forget()
                if clik_inicio is None:
                    self.frame_menu.grid_propagate(0)
                    self.bt_cerrar.grid(column= 0, row= 0, padx= 10, pady= 10)
                    self.bt_cerrar.grid_propagate(0)
                    self.bt_cerrar.config(width= i)
                    self.pantalla_inicial()
                self.menu = True
    
    def mostrar_datos(self):
        self.miConexion=sqlite3.connect("./bd/DBpaciente.sqlite3")
        self.miCursor=self.miConexion.cursor()
        bd = "SELECT Apellido, Nombre, DNI, Telefono, ObraSocial FROM Paciente"
        self.miCursor.execute(bd)
        datos = self.miCursor.fetchall()
        self.tabla_paciente.delete(*self.tabla_paciente.get_children())
        i = -1
        for dato in datos:
            i= i+1
            self.tabla_paciente.insert('',i, text = datos[i][0], values=(datos[i][1],datos[i][2],datos[i][3],datos[i][4]))
    
    def buscar_paciente(self):
        self.miConexion=sqlite3.connect("./bd/DBpaciente.sqlite3")
        self.miCursor=self.miConexion.cursor()
        self.buscar =self.dato_paciente.get()
        
        bd =f"SELECT Apellido, Nombre, DNI, Telefono, ObraSocial FROM Paciente WHERE Apellido LIKE '%{self.buscar}%' OR Nombre LIKE '%{self.buscar}%' ORDER BY Nombre DESC"
        self.miCursor.execute(bd)
        datos = self.miCursor.fetchall()
        self.tabla_paciente.delete(*self.tabla_paciente.get_children())
        i = -1
        for dato in datos:
            i= i+1
            self.tabla_paciente.insert('',i, text = datos[i][0], values=(datos[i][1],datos[i][2],datos[i][3],datos[i][4]))
    
    def obtener_fila(self, event):
        item = self.tabla_paciente.focus()
        self.data = self.tabla_paciente.item(item)
        self.dni_paciente=self.data['values'][1]
        
    def widgets(self):
        #self.imagen_inicio = PhotoImage(file ='./imagenes/home-removebg-preview.png')
        #tself.imagen_menu = PhotoImage(file ='./imagenes/menu4-removebg-preview.png')
        self.imagen_paciente = PhotoImage(file ='./imagenes/agregar3.png')
        self.imagen_calendario = PhotoImage(file ='./imagenes/calendario-removebg-preview.png')
        self.imagen_historia_clinica = PhotoImage(file ='./imagenes/historial3.png')
        self.imagen_buscar = PhotoImage(file ='./imagenes/foto-removebg-preview.png')
        self.imagen_ajustes = PhotoImage(file ='./imagenes/info_icon_white.png')
        self.imagen_agregar_paciente = PhotoImage(file ='./imagenes/agregar_paciente.png')
        self.imagen_editar_paciente = PhotoImage(file ='./imagenes/editar_paciente.png')
        self.imagen_refrescar = PhotoImage(file ='./imagenes/refrescar.png')
        self.imagen_eliminar_paciente = PhotoImage(file ='./imagenes/eliminar22.png')
        self.imagen_salir = PhotoImage(file ='./imagenes/salir.png')
        self.logo = PhotoImage(file ='./imagenes/logo1.png')

        try:
            self.imagen_inicio = PhotoImage(file ='./imagenes/home-removebg-preview.png')
            self.imagen_menu = PhotoImage(file ='./imagenes/menu4-removebg-preview.png')
            self.bt_inicio = Button(self.frame_inicio, image= self.imagen_inicio, bg= '#1F704B', activebackground='white', bd= 0, command= self.menu_lateral)
            self.bt_cerrar = Button(self.frame_inicio, image= self.imagen_menu, bg= '#1F704B', activebackground='white', bd= 0, command= self.menu_lateral)
        except:
            self.bt_inicio = Button(self.frame_inicio, text= 'INICIO', font= ('Comic Sans MS', 12, 'bold'), bg= '#1F704B', activebackground='white', bd= 0, command= self.menu_lateral)
            self.bt_cerrar = Button(self.frame_inicio, text= 'INICIO', font= ('Comic Sans MS', 12, 'bold'), bg= '#1F704B', activebackground='white', bd= 0, command= self.menu_lateral)
        
        self.bt_inicio.grid(column= 0, row= 0, padx= 5, pady= 10)        
        self.bt_cerrar.grid(column= 0, row= 0, padx= 5, pady= 10)

		#BOTONES Y ETIQUETAS DEL MENU LATERAL
        Button(self.frame_menu, image= self.imagen_paciente, bg= '#1F704B', activebackground= 'white', bd= 0, command= self.pantalla_pacientes).grid(column= 0, row= 1, pady= 20, padx= 10)
        Button(self.frame_menu, image= self.imagen_calendario, bg= '#1F704B', activebackground= 'white', bd= 0, command= self.pantalla_calendario ).grid(column= 0, row= 2, pady= 20, padx= 10)
        Button(self.frame_menu, image= self.imagen_historia_clinica, bg= '#1F704B',activebackground= 'white', bd= 0, command= self.pantalla_historia).grid(column= 0, row= 3, pady= 20, padx= 10)
        Button(self.frame_menu, image= self.imagen_buscar, bg= '#1F704B', activebackground= 'white', bd= 0, command= self.pantalla_galeria).grid(column=0, row=4, pady=20, padx=10)
        Button(self.frame_menu, image= self.imagen_ajustes, bg= '#1F704B', activebackground= 'white', bd= 0, command= self.pantalla_info).grid(column=0, row=5, pady=20,padx=10)
        Button(self.frame_menu, image= self.imagen_salir, bg= '#1F704B', activebackground= 'white', bd= 0, command= self.salir).grid(column=0, row=6, pady=20,padx=10)


        Label(self.frame_menu, text= 'Pacientes', bg= '#1F704B', fg= 'white', font= ('Comic Sans MS', 12, 'bold')).grid(column=1, row=1, pady= 20, padx= 2)
        Label(self.frame_menu, text= 'Calendario', bg= '#1F704B', fg= 'white', font= ('Comic Sans MS', 12, 'bold')).grid(column=1, row=2, pady= 20, padx= 2)
        Label(self.frame_menu, text= 'Historia \nClinica', bg= '#1F704B', fg= 'white', font= ('Comic Sans MS', 12, 'bold')).grid(column=1, row= 3, pady= 20, padx= 2)
        Label(self.frame_menu, text= 'Galeria', bg= '#1F704B', fg= 'white', font= ('Comic Sans MS', 12, 'bold')).grid(column=1, row=4, pady= 20, padx= 2)
        Label(self.frame_menu, text= 'Versión', bg= '#1F704B', fg= 'white', font= ('Comic Sans MS', 12, 'bold')).grid(column=1, row=5, pady= 20, padx= 2)
        Label(self.frame_menu, text= 'Salir', bg= '#1F704B', fg= 'white', font= ('Comic Sans MS', 12, 'bold')).grid(column=1, row=6, pady= 20, padx= 2)

		#############################  CREAR  PAGINAS  ##############################
        estilo_paginas = ttk.Style()
        estilo_paginas.configure("TNotebook", background='#1F704B', foreground='#1F704B', padding= 0, borderwidth= 0)
        estilo_paginas.theme_use('default')
        estilo_paginas.configure("TNotebook", background='#1F704B', borderwidth= 0)
        estilo_paginas.configure("TNotebook.Tab", background="#1F704B", borderwidth= 0)
        estilo_paginas.map("TNotebook", background=[("selected", '#1F704B')])
        estilo_paginas.map("TNotebook.Tab", background=[("selected", '#1F704B')], foreground=[("selected", '#1F704B')]);
        
		#CREACCION DE LAS PAGINAS
        self.paginas = ttk.Notebook(self.frame_raiz, style= 'TNotebook')
        self.paginas.grid(column= 0, row= 0, sticky='nsew')
        self.frame_principal = Frame(self.paginas, bg='gray90') #color de fondo
        self.frame_pacientes = Frame(self.paginas, bg='gray90') #color de fondo
        self.frame_calendario = Frame(self.paginas, bg='gray90')
        self.historia = Frame(self.paginas, bg='gray90')
        self.frame_galeria = Frame(self.paginas, bg='gray90')
        self.frame_info = Frame(self.paginas, bg='gray90')
        self.paginas.add(self.frame_principal)
        self.paginas.add(self.frame_pacientes)
        self.paginas.add(self.frame_calendario)
        self.paginas.add(self.historia)
        self.paginas.add(self.frame_galeria)
        self.paginas.add(self.frame_info)

		##############################         PAGINAS       #############################################
		######################## FRAME TITULO #################
        self.titulo = Label(self.frame_top, text= 'Consultorio Odontológico MyM', bg= '#1F704B', fg= 'white', font= ('Comic Sans MS', 15, 'bold'))
        self.titulo.pack(expand=1)

		######################## VENTANA PRINCIPAL #################
        Label(self.frame_principal, image= self.logo, bg= 'gray90').pack(expand= 1)

		######################## PACIENTES #################
        Button(self.frame_pacientes, image= self.imagen_agregar_paciente, text= 'AGREGAR', fg= 'black', font= ('Arial', 11,'bold'), bg= '#1F704B', bd= 2, borderwidth= 2, command= self.agregar_paciente).grid(column= 4, row= 0, pady= 5)
        Label(self.frame_pacientes, text= 'Agregar', bg= 'gray90', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column= 4, row= 1)
        Button(self.frame_pacientes, image= self.imagen_editar_paciente, text= 'EDITAR', fg= 'black', font = ('Arial', 11,'bold'), bg= '#1F704B', bd= 2, borderwidth= 2, command= self.editar_paciente).grid(column= 1, row= 0, pady= 5)
        Label(self.frame_pacientes, text= 'Editar', bg= 'gray90', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column= 1, row= 1)
        Button(self.frame_pacientes, image= self.imagen_eliminar_paciente, text= 'ELIMINAR', fg= 'black', font= ('Arial', 11,'bold'), bg= '#1F704B', bd= 2, borderwidth= 2, command= self.eliminar_paciente).grid(column= 2, row= 0, pady= 5)
        Label(self.frame_pacientes, text= 'Eliminar', bg= 'gray90', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column= 2, row= 1)
        Button(self.frame_pacientes, image= self.imagen_refrescar, text= 'REFRESCAR', fg= 'black', font = ('Arial', 11,'bold'), bg= '#1F704B', bd= 2, borderwidth= 2, command= self.mostrar_datos).grid(column= 3, row= 0, pady= 5)
        Label(self.frame_pacientes, text= 'Refrescar', bg= 'gray90', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column= 3, row= 1)
        self.busqueda = ttk.Entry(self.frame_pacientes, textvariable=self.dato_paciente, width= 10 ,font= ('Comic Sans MS', 14)).grid(column= 0, row= 0, pady= 5)
        Button(self.frame_pacientes, text= 'Buscar', bg= '#1F704B', fg= 'black', font= ('Comic Sans MS', 12, 'bold'), command= self.buscar_paciente).grid(column= 0, row= 1)
        #self.Buscar.bind("<Return>", (lambda event: self.buscar_paciente()))

		#ESTILO DE LAS TABLAS DE DATOS TREEVIEW
        estilo_tabla = ttk.Style()
        estilo_tabla.configure("Treeview", font= ('Comic Sans MS', 10, 'bold'), foreground='black', background='white', rowheight=40)
        estilo_tabla.map('Treeview', background=[('selected', '#1F704B')], foreground=[('selected','white')] )
        estilo_tabla.configure('Heading', background = 'white', foreground='navy', padding= 3, font= ('Comic Sans MS', 10, 'bold'))
        estilo_tabla.configure('Item', foreground = 'white', focuscolor ='white')
        estilo_tabla.configure('TScrollbar', arrowcolor = 'white', bordercolor  ='black', troughcolor= 'white', background ='white')

		#TABLA PACIENTE
        self.frame_tabla_paciente = Frame(self.frame_pacientes, bg='gray90')
        self.frame_tabla_paciente.grid(columnspan=5, row=2, sticky='nsew')
        self.tabla_paciente = ttk.Treeview(self.frame_tabla_paciente)
        self.tabla_paciente.grid(column=0, row=2, columnspan=5, sticky='nsew')
        ladoy = ttk.Scrollbar(self.frame_tabla_paciente, orient ='vertical', command = self.tabla_paciente.yview)
        ladoy.grid(column = 5, row = 2, sticky='ns')
        self.tabla_paciente.configure(yscrollcommand = ladoy.set)
        self.tabla_paciente['columns'] = ('Nombre', 'D.N.I.', 'Teléfono', 'Obra Social')
        self.tabla_paciente.column('#0', minwidth=100, width=120, anchor='center')
        self.tabla_paciente.column('Nombre', minwidth=100, width=130 , anchor='center')
        self.tabla_paciente.column('D.N.I.', minwidth=100, width=120, anchor='center' )
        self.tabla_paciente.column('Teléfono', minwidth=100, width=120 , anchor='center')
        self.tabla_paciente.column('Obra Social', minwidth=100, width=105, anchor='center')

        self.tabla_paciente.heading('#0', text='Apellido', anchor ='center')
        self.tabla_paciente.heading('Nombre', text='Nombre', anchor ='center')
        self.tabla_paciente.heading('D.N.I.', text='D.N.I.', anchor ='center')
        self.tabla_paciente.heading('Teléfono', text='Teléfono', anchor ='center')
        self.tabla_paciente.heading('Obra Social', text='Obra Social', anchor ='center')
        self.mostrar_datos()
        self.tabla_paciente.bind("<<TreeviewSelect>>", self.obtener_fila)

		######################## HISTORIA CLINICA #################
        Label(self.historia, text = 'HISTORIA CLINICA', fg= '#1F704B', bg='gray90', font=('Comic Sans MS', 24, 'bold')).grid(columnspan= 4, row= 0)
        
		######################## GALERIA #################
        Label(self.frame_galeria, text = 'GALERIA', fg='#1F704B', bg='gray90', font=('Comic Sans MS', 24,'bold')).grid(column= 0,  row= 0)
        
        		
		######################## INFO #################
        self.name = Label(self.frame_info, text= 'DENTALMATIC', fg='#1F704B', bg='gray90', font=('Comic Sans MS', 30,'bold')).pack(expand= 1)
        self.version = Label(self.frame_info, text= 'Versión 1.0 - 2024', fg='#1F704B', bg='gray90', font=('Comic Sans MS', 15,'bold')).pack(expand= 1)
        self.autor= Label(self.frame_info, text= 'Autor:Rodrigo Adrian Richard\nDesarrollado en Python', fg='black', bg='gray90', font=('Comic Sans MS', 10)).pack(expand= 1)
                
        self.ventana.mainloop()