import tkinter as tk
from tkinter.font import BOLD
import util.generic as utl
from tkinter import  Button, Entry, Label, ttk, PhotoImage
from tkinter import  StringVar, Scrollbar, Frame
from forms.form_paciente import Paciente

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

    def pantalla_datos(self):
        self.paginas.select([self.frame_pacientes])
        self.frame_pacientes.columnconfigure(0, weight= 1)
        self.frame_pacientes.columnconfigure(1, weight= 1)
        self.frame_pacientes.rowconfigure(2, weight= 1)
        self.frame_tabla_uno.columnconfigure(0, weight= 1)
        self.frame_tabla_uno.rowconfigure(0, weight= 1)

    def pantalla_escribir(self):
        self.paginas.select([self.frame_tres])
        self.frame_tres.columnconfigure(0, weight= 1)
        self.frame_tres.columnconfigure(1, weight= 1)

    def pantalla_actualizar(self):
        self.paginas.select([self.frame_cuatro])
        self.frame_cuatro.columnconfigure(0, weight= 1)
        self.frame_cuatro.columnconfigure(1, weight= 1)
    
    def pantalla_buscar(self):
        self.paginas.select([self.frame_cinco])
        self.frame_cinco.columnconfigure(0, weight= 1)
        self.frame_cinco.columnconfigure(1, weight =1)
        self.frame_cinco.columnconfigure(2, weight= 1)
        self.frame_cinco.rowconfigure(2, weight= 1)
        self.frame_tabla_dos.columnconfigure(0, weight= 1)
        self.frame_tabla_dos.rowconfigure(0, weight= 1)

    def pantalla_ajustes(self):
        self.paginas.select([self.frame_seis])
    
    def agregar_paciente(self):
        Paciente()
        #paciente.agregar_paciente

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

    def widgets(self):
        self.imagen_inicio = PhotoImage(file ='./GUILogin/imagenes/inicio2.png')
        self.imagen_menu = PhotoImage(file ='./GUILogin/imagenes/menu3.png')
        self.imagen_paciente = PhotoImage(file ='./GUILogin/imagenes/agregar3.png')
        self.imagen_calendario = PhotoImage(file ='./GUILogin/imagenes/calendario.png')
        self.imagen_historia_clinica = PhotoImage(file ='./GUILogin/imagenes/historial3.png')
        self.imagen_buscar = PhotoImage(file ='./GUILogin/imagenes/buscar.png')
        self.imagen_ajustes = PhotoImage(file ='./GUILogin/imagenes/configuracion.png')
        self.imagen_agregar_paciente = PhotoImage(file ='./GUILogin/imagenes/agregar_paciente.png')
        self.imagen_editar_paciente = PhotoImage(file ='./GUILogin/imagenes/editar_paciente.png')

        self.logo = PhotoImage(file ='./GUILogin/imagenes/logo1.png')

        self.bt_inicio = Button(self.frame_inicio, image= self.imagen_inicio, bg= '#1F704B', activebackground='black', bd= 0, command= self.menu_lateral)
        self.bt_inicio.grid(column= 0, row= 0, padx= 5, pady= 10)
        self.bt_cerrar = Button(self.frame_inicio, image= self.imagen_menu, bg= '#1F704B', activebackground='black', bd= 0, command= self.menu_lateral)
        self.bt_cerrar.grid(column= 0, row= 0, padx= 5, pady= 10)

		#BOTONES Y ETIQUETAS DEL MENU LATERAL
        Button(self.frame_menu, image= self.imagen_paciente, bg= '#1F704B', activebackground= 'white', bd= 0, command= self.pantalla_datos).grid(column= 0, row= 1, pady= 20, padx= 10)
        Button(self.frame_menu, image= self.imagen_calendario, bg= '#1F704B', activebackground= 'white', bd= 0, command= self.pantalla_escribir ).grid(column= 0, row= 2, pady= 20, padx= 10)
        Button(self.frame_menu, image= self.imagen_historia_clinica, bg= '#1F704B',activebackground= 'white', bd= 0, command= self.pantalla_actualizar).grid(column= 0, row= 3, pady= 20, padx= 10)
        Button(self.frame_menu, image= self.imagen_buscar, bg= '#1F704B', activebackground= 'white', bd= 0, command= self.pantalla_buscar).grid(column=0, row=4, pady=20, padx=10)
        Button(self.frame_menu, image= self.imagen_ajustes, bg= '#1F704B', activebackground= 'white', bd= 0, command= self.pantalla_ajustes).grid(column=0, row=5, pady=20,padx=10)

        Label(self.frame_menu, text= 'Pacientes', bg= '#1F704B', fg= 'white', font= ('Comic Sans MS', 12, 'bold')).grid(column=1, row=1, pady= 20, padx= 2)
        Label(self.frame_menu, text= 'Calendario', bg= '#1F704B', fg= 'white', font= ('Comic Sans MS', 12, 'bold')).grid(column=1, row=2, pady= 20, padx= 2)
        Label(self.frame_menu, text= 'Historia \nClinica', bg= '#1F704B', fg= 'white', font= ('Comic Sans MS', 12, 'bold')).grid(column=1, row= 3, pady= 20, padx= 2)
        Label(self.frame_menu, text= 'Eliminar', bg= '#1F704B', fg= 'white', font= ('Comic Sans MS', 12, 'bold')).grid(column=1, row=4, pady= 20, padx= 2)
        Label(self.frame_menu, text= 'Versión', bg= '#1F704B', fg= 'white', font= ('Comic Sans MS', 12, 'bold')).grid(column=1, row=5, pady= 20, padx= 2)

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
        self.frame_principal = Frame(self.paginas, bg='#fcfcfc') #color de fondo
        self.frame_pacientes = Frame(self.paginas, bg='#fcfcfc') #color de fondo
        self.frame_tres = Frame(self.paginas, bg='#fcfcfc')
        self.frame_cuatro = Frame(self.paginas, bg='#fcfcfc')
        self.frame_cinco = Frame(self.paginas, bg='#fcfcfc')
        self.frame_seis = Frame(self.paginas, bg='#fcfcfc')
        self.paginas.add(self.frame_principal)
        self.paginas.add(self.frame_pacientes)
        self.paginas.add(self.frame_tres)
        self.paginas.add(self.frame_cuatro)
        self.paginas.add(self.frame_cinco)
        self.paginas.add(self.frame_seis)

		##############################         PAGINAS       #############################################
		######################## FRAME TITULO #################
        self.titulo = Label(self.frame_top, text= 'Consultorio Odóntologico MyM', bg= '#1F704B', fg= 'white', font= ('Comic Sans MS', 15, 'bold'))
        self.titulo.pack(expand=1)

		######################## VENTANA PRINCIPAL #################
        Label(self.frame_principal, image= self.logo, bg= 'white').pack(expand= 1)

		######################## MOSTRAR TODOS LOS PACIENTES #################
        #Label(self.frame_pacientes, text= 'Listado de pacientes', bg= 'white', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column= 0, row= 0)
        Button(self.frame_pacientes, image= self.imagen_editar_paciente, text= 'ACTUALIZAR', fg= 'black', font = ('Arial', 11,'bold'), bg= '#1F704B', bd= 2, borderwidth= 2).grid(column= 1, row= 0, pady= 5)
        Label(self.frame_pacientes, text= 'Editar', bg= 'white', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column= 1, row= 1)
        Button(self.frame_pacientes, image= self.imagen_agregar_paciente, text= 'NUEVO', fg= 'black', font= ('Arial', 11,'bold'), bg= '#1F704B', bd= 2, borderwidth= 2, command= self.agregar_paciente).grid(column= 2, row= 0, pady= 5)
        Label(self.frame_pacientes, text= 'Agregar', bg= 'white', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column= 2, row= 1)
        self.busqueda = ttk.Entry(self.frame_pacientes, width= 10 ,font= ('Comic Sans MS', 14)).grid(column= 0, row= 0, pady= 5)
        Button(self.frame_pacientes, text= 'Buscar', bg= 'white', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column= 0, row= 1)
        #command= self.datos_totales, 
  

		#ESTILO DE LAS TABLAS DE DATOS TREEVIEW
        estilo_tabla = ttk.Style()
        estilo_tabla.configure("Treeview", font= ('Comic Sans MS', 10, 'bold'), foreground='black', background='white')  #, fieldbackground='yellow'
        estilo_tabla.map('Treeview', background=[('selected', 'white')], foreground=[('selected','black')] )
        estilo_tabla.configure('Heading', background = 'white', foreground='navy', padding= 3, font= ('Comic Sans MS', 10, 'bold'))
        estilo_tabla.configure('Item', foreground = 'white', focuscolor ='white')
        estilo_tabla.configure('TScrollbar', arrowcolor = 'white', bordercolor  ='black', troughcolor= 'white', background ='white')

		#TABLA UNO
        self.frame_tabla_uno = Frame(self.frame_pacientes, bg='gray90')
        self.frame_tabla_uno.grid(columnspan=3, row=2, sticky='nsew')
        self.tabla_uno = ttk.Treeview(self.frame_tabla_uno)
        self.tabla_uno.grid(column=0, row=0, sticky='nsew')
        ladox = ttk.Scrollbar(self.frame_tabla_uno, orient = 'horizontal', command= self.tabla_uno.xview)
        ladox.grid(column=0, row = 1, sticky='ew')
        ladoy = ttk.Scrollbar(self.frame_tabla_uno, orient ='vertical', command = self.tabla_uno.yview)
        ladoy.grid(column = 1, row = 0, sticky='ns')

        self.tabla_uno.configure(xscrollcommand = ladox.set, yscrollcommand = ladoy.set)
        self.tabla_uno['columns'] = ('Nombre', 'Modelo', 'Precio', 'Cantidad')
        self.tabla_uno.column('#0', minwidth=100, width=120, anchor='center')
        self.tabla_uno.column('Nombre', minwidth=100, width=130 , anchor='center')
        self.tabla_uno.column('Modelo', minwidth=100, width=120, anchor='center' )
        self.tabla_uno.column('Precio', minwidth=100, width=120 , anchor='center')
        self.tabla_uno.column('Cantidad', minwidth=100, width=105, anchor='center')

        self.tabla_uno.heading('#0', text='Codigo', anchor ='center')
        self.tabla_uno.heading('Nombre', text='Nombre', anchor ='center')
        self.tabla_uno.heading('Modelo', text='Modelo', anchor ='center')
        self.tabla_uno.heading('Precio', text='Precio', anchor ='center')
        self.tabla_uno.heading('Cantidad', text='Cantidad', anchor ='center')
#		self.tabla_uno.bind("<<TreeviewSelect>>", self.obtener_fila)

		######################## REGISTRAR  NUEVOS PRODUCTOS #################
        Label(self.frame_tres, text = 'Agregar Nuevos Datos', fg='blue', bg ='white', font=('Comic Sans MS',24,'bold')).grid(columnspan=2, column=0, row=0, pady=5)
        Label(self.frame_tres, text = 'Codigo', fg='navy', bg ='white', font=('Comic Sans MS',13,'bold')).grid(column=0,row=1, pady=15, padx=5)
        Label(self.frame_tres, text = 'Nombre', fg='navy', bg ='white', font=('Comic Sans MS',13,'bold')).grid(column=0,row=2, pady=15)
        Label(self.frame_tres, text = 'Modelo', fg='navy', bg ='white', font=('Comic Sans MS',13,'bold')).grid(column=0,row=3, pady=15)
        Label(self.frame_tres, text = 'Precio', fg='navy', bg ='white', font=('Comic Sans MS',13,'bold')).grid(column=0,row=4, pady=15)
        Label(self.frame_tres, text = 'Cantidad', fg='navy', bg ='white', font=('Comic Sans MS',13,'bold')).grid(column=0,row=5, pady=15)  ##E65561

        #Entry(self.frame_tres, textvariable=self.codigo , font=('Comic Sans MS', 12), highlightbackground = "DarkOrchid1", highlightcolor= "green2", highlightthickness=5).grid(column=1, row=1)
       # Entry(self.frame_tres, textvariable=self.nombre , font=('Comic Sans MS', 12), highlightbackground = "DarkOrchid1", highlightcolor= "green2", highlightthickness=5).grid(column=1, row=2)
        #Entry(self.frame_tres, textvariable=self.modelo , font=('Comic Sans MS', 12), highlightbackground = "DarkOrchid1", highlightcolor= "green2", highlightthickness=5).grid(column=1, row=3)
        #Entry(self.frame_tres, textvariable=self.precio , font=('Comic Sans MS', 12), highlightbackground = "DarkOrchid1", highlightcolor= "green2", highlightthickness=5).grid(column=1, row=4)
       # Entry(self.frame_tres, textvariable=self.cantidad , font=('Comic Sans MS', 12), highlightbackground = "DarkOrchid1", highlightcolor= "green2", highlightthickness=5).grid(column=1, row=5)

		#Button(self.frame_tres,command= self.agregar_datos, text='REGISTRAR', font=('Arial',10,'bold'), bg='magenta2').grid(column=3,row=6, pady=10, padx=4)
        self.aviso_guardado = Label(self.frame_tres, bg= 'white', font=('Comic Sans MS', 12), fg= 'black')
        self.aviso_guardado.grid(columnspan= 2, column= 0, row= 6, padx= 5)

		########################   ACTUALIZAR LOS PRODUCTOS REGISTRADOS     #################
        Label(self.frame_cuatro, text = 'Actualizar Datos', fg= 'blue', bg='white', font=('Comic Sans MS', 24, 'bold')).grid(columnspan= 4, row= 0)
        Label(self.frame_cuatro, text = 'Ingrese el nombre del producto a actualizar', fg= 'black', bg= 'white', font=('Comic Sans MS', 12)).grid(columnspan=2, row=1)
        #Entry(self.frame_cuatro, textvariable= self.buscar_actualiza, font=('Comic Sans MS', 12), highlightbackground = "magenta2", width=12, highlightthickness=5).grid(column=2, row=1, padx=5)
		#Button(self.frame_cuatro, command= self.actualizar_datos, text='BUSCAR', font=('Arial',12,'bold'), bg='deep sky blue').grid(column=3,row=1, pady=5, padx=15)
        self.aviso_actualizado = Label(self.frame_cuatro, fg= 'black', bg= 'white', font=('Comic Sans MS', 12,'bold'))
        self.aviso_actualizado.grid(columnspan= 2, row= 7, pady= 10, padx= 5)
        
        Label(self.frame_cuatro, text= 'Codigo', fg='navy', bg='white', font=('Comic Sans MS',13,'bold')).grid(column= 0, row= 2, pady= 15, padx= 10)
        Label(self.frame_cuatro, text= 'Nombre', fg='navy', bg='white', font=('Comic Sans MSl',13,'bold')).grid(column= 0, row= 3, pady= 15)
        Label(self.frame_cuatro, text= 'Modelo', fg='navy', bg='white', font=('Comic Sans MS',13,'bold')).grid(column= 0, row= 4, pady= 15)
        Label(self.frame_cuatro, text= 'Precio', fg='navy',bg='white', font=('Comic Sans MS',13,'bold')).grid(column= 0, row= 5, pady= 15)
        Label(self.frame_cuatro, text= 'Cantidad', fg='navy', bg='white', font=('Comic Sans MS',13,'bold')).grid(column= 0, row= 6, pady= 15)  ##E65561

        #Entry(self.frame_cuatro, textvariable=self.codigo, font=('Comic Sans MS', 12), highlightbackground = "deep sky blue", highlightcolor= "green", highlightthickness=5).grid(column=1,row=2)
        #Entry(self.frame_cuatro, textvariable=self.nombre, font=('Comic Sans MS', 12), highlightbackground = "deep sky blue", highlightcolor= "green", highlightthickness=5).grid(column=1,row=3)
        #Entry(self.frame_cuatro, textvariable=self.modelo, font=('Comic Sans MS', 12), highlightbackground = "deep sky blue", highlightcolor= "green", highlightthickness=5).grid(column=1,row=4)
        #Entry(self.frame_cuatro, textvariable=self.precio, font=('Comic Sans MS', 12), highlightbackground = "deep sky blue", highlightcolor= "green", highlightthickness=5).grid(column=1,row=5)
        #Entry(self.frame_cuatro, textvariable=self.cantidad, font=('Comic Sans MS', 12), highlightbackground = "deep sky blue", highlightcolor= "green", highlightthickness=5).grid(column=1,row=6)
		
		######################## BUSCAR y ELIMINAR DATOS #################
        Label(self.frame_cinco, text = 'Buscar y Eliminar Datos', fg='blue', bg='white', font=('Comic Sans MS', 24,'bold')).grid(columnspan= 4,  row= 0, sticky= 'nsew', padx= 2)
        #Entry(self.frame_cinco, textvariable= self.buscar, font=('Comic Sans MS', 12), highlightbackground = "DarkOrchid1", highlightcolor= "deep sky blue", highlightthickness=5).grid(column=0, row=1, sticky='nsew', padx=2)
		#Button(self.frame_cinco,command = self.buscar_nombre, text='BUSCAR POR NOMBRE', font=('Arial',8,'bold'), bg='deep sky blue').grid(column = 1, row=1, sticky='nsew', padx=2)
		#Button(self.frame_cinco,command = self.eliminar_fila, text='ELIMINAR', font=('Arial',8,'bold'), bg='red').grid(column = 2, row=1, sticky='nsew',padx=2)
        self.indica_busqueda= Label(self.frame_cinco, width= 15, text= '', fg= 'blue', bg= 'white', font=('Comic Sans MS', 12,'bold'))
        self.indica_busqueda.grid(column= 3, row= 1, padx= 2)

		#TABLA DOS
        self.frame_tabla_dos = Frame(self.frame_cinco, bg= 'gray90')
        self.frame_tabla_dos.grid(columnspan= 4, row= 2, sticky='nsew')
        self.tabla_dos = ttk.Treeview(self.frame_tabla_dos)
        self.tabla_dos.grid(column= 0, row= 0, sticky='nsew')
        ladox = ttk.Scrollbar(self.frame_tabla_dos, orient= 'horizontal', command= self.tabla_dos.xview)
        ladox.grid(column= 0, row= 1, sticky='ew')
        ladoy = ttk.Scrollbar(self.frame_tabla_dos, orient='vertical', command= self.tabla_dos.yview)
        ladoy.grid(column= 1, row= 0, sticky='ns')

        self.tabla_dos.configure(xscrollcommand= ladox.set, yscrollcommand= ladoy.set)
        self.tabla_dos['columns'] = ('Nombre', 'Modelo', 'Precio', 'Cantidad')
        self.tabla_dos.column('#0', minwidth= 100, width= 120, anchor= 'center')
        self.tabla_dos.column('Nombre', minwidth= 100, width= 130 , anchor= 'center')
        self.tabla_dos.column('Modelo', minwidth= 100, width= 120, anchor= 'center' )
        self.tabla_dos.column('Precio', minwidth= 100, width= 120 , anchor= 'center')
        self.tabla_dos.column('Cantidad', minwidth= 100, width= 105, anchor= 'center')

        self.tabla_dos.heading('#0', text= 'Codigo', anchor= 'center')
        self.tabla_dos.heading('Nombre', text= 'Nombre', anchor= 'center')
        self.tabla_dos.heading('Modelo', text= 'Modelo', anchor= 'center')
        self.tabla_dos.heading('Precio', text= 'Precio', anchor= 'center')
        self.tabla_dos.heading('Cantidad', text= 'Cantidad', anchor= 'center')
#		self.tabla_dos.bind("<<TreeviewSelect>>", self.obtener_fila)

		######################## AJUSTES #################
        self.text_ajustes = Label(self.frame_seis, text= 'Configuracion', fg='blue', bg='white', font=('Comic Sans MS', 28,'bold'))
        self.text_ajustes.pack(expand= 1)
        self.texto= Label(self.frame_seis, text= '@autor:AdriaTech \n Desarrollado en Python', fg='red', bg='white', font=('Comic Sans MS', 18))
        self.texto.pack(expand= 1)
                
        self.ventana.mainloop()