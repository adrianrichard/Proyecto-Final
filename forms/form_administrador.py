import tkinter as tk
from tkinter.font import BOLD
from tkinter import ttk
import util.generic as utl
from tkinter import  Button, messagebox, Label, ttk, PhotoImage
from tkinter import  StringVar, Frame
from forms.form_paciente import Paciente
from forms.form_usuario import Usuario
from paginas.tkcalendar import TKCalendar
from util.visorimagenes import ImageGalleryApp
import sqlite3
fuenteb = utl.definir_fuente_bold()
fuenten = utl.definir_fuente()
pacientes = []
incremento = 10
fuente2= 'Comic Sans MS'
color_fuente = 'black'
color_fondo1 = utl.definir_color_fondo()
color_fondo2 = 'gray90'
global indice_paciente

class MasterPanel:

    def __init__(self):

        self.ventana= tk.Tk()
        #self.ventana= tk.Toplevel()
        #self.ventana.grab_set_global() # Obliga a las ventanas estar deshabilitadas y deshabilitar todos los eventos e interacciones con la ventana
        #self.ventana.focus_set() # Mantiene el foco cuando se abre la ventana.
        self.ventana.title('DentalMatic')
        self.ventana.geometry('1000x500+180+80')
        self.ventana.config(bg= '#fcfcfc')
        self.ventana.resizable(width= 0, height= 0)
        utl.centrar_ventana(self.ventana, 900, 600)
        self.menu = True
        self.imagen_ventana = utl.leer_imagen('tooth.jpg', (38, 38))
        self.ventana.iconphoto(False, self.imagen_ventana)
        self.dni_paciente =  StringVar()
        self.dato_paciente =  StringVar()
        self.nombre_usuario =  StringVar()

        self.frame_inicio = Frame(self.ventana, bg= color_fondo1, width= 50, height= 45)
        self.frame_inicio.grid_propagate(0)
        self.frame_inicio.grid(column= 0, row= 0, sticky= 'nsew')
        self.frame_menu = Frame(self.ventana, bg= color_fondo1, width= 60)
        self.frame_menu.grid_propagate(0)
        self.frame_menu.grid(column= 0, row= 1, sticky= 'nsew')
        self.frame_top = Frame(self.ventana, bg= color_fondo1, height= 50)
        self.frame_top.grid(column= 1, row= 0, sticky= 'nsew')
        self.frame_raiz = Frame(self.ventana, bg= color_fondo1)
        self.frame_raiz.grid(column= 1, row= 1, sticky= 'nsew')
        self.ventana.columnconfigure(1, weight= 1)
        self.ventana.rowconfigure(1, weight= 1)
        self.frame_raiz.columnconfigure(0, weight= 1)
        self.frame_raiz.rowconfigure(0, weight= 1)

        self.widgets()

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

    def pantalla_inicial(self):
        self.paginas.select([self.frame_principal])

    def pantalla_usuarios(self):
        self.paginas.select([self.frame_usuarios])
        [self.frame_tabla_usuario.columnconfigure(i, weight= 1) for i in range(self.frame_usuarios.grid_size()[0])]
        [self.frame_usuarios.columnconfigure(i, weight= 1) for i in range(self.frame_usuarios.grid_size()[0])]
        [self.frame_tabla_usuario.rowconfigure(i, weight= 1) for i in range(self.frame_usuarios.grid_size()[1])]

    def pantalla_pacientes(self):
        self.paginas.select([self.frame_pacientes])
        [self.frame_pacientes.columnconfigure(i, weight= 1) for i in range(self.frame_pacientes.grid_size()[0])]
        [self.frame_tabla_paciente.columnconfigure(i, weight= 1) for i in range(self.frame_pacientes.grid_size()[0])]
        [self.frame_tabla_paciente.rowconfigure(i, weight= 1) for i in range(self.frame_pacientes.grid_size()[1])]
        self.estilo_tabla.configure('Treeview.Heading', background= 'green', fg= 'black', padding= 3, font= fuenteb)        
        self.estilo_tabla.configure("Treeview", font= fuenten, foreground= 'black', rowheight= 35)

    def pantalla_calendario(self):
        self.paginas.select([self.frame_calendario])
        Tcal = TKCalendar()
        Tcal.crear_encabezado(self.frame_calendario)
        Tcal.crear_botones_fechas(self.frame_calendario)
        Tcal.actualizar_botones_fechas()
        #Tcal.cargar_turnos(self.frame_calendario)
        #Tcal.event_color_buttons()
        Tcal.configurar_filas_columnas(self.frame_calendario)

    def pantalla_historia(self):
        self.paginas.select([self.historia])
        self.historia.columnconfigure(0, weight= 1)
        self.historia.columnconfigure(1, weight= 1)
        self.estilo_tabla.configure('Treeview.Heading', background= 'green', fg= 'black', padding= 3, font= fuenteb)        
        self.estilo_tabla.configure("Treeview", font= fuenten, foreground= 'black', rowheight= 35)

    def pantalla_galeria(self):
        self.paginas.select([self.frame_galeria])
        Gallery=ImageGalleryApp(self.frame_galeria)
        Gallery.configurar_filas_columnas(self.frame_galeria)

    def salir(self):
        answer = messagebox.askokcancel(title= 'Salir', message= '¿Desea salir?', icon= 'warning')
        if answer:            
            self.ventana.destroy()

    def agregar_paciente(self):
        paciente= Paciente()
        paciente.ventana_paciente()

    def editar_paciente(self, event):
        paciente= Paciente()
        item = self.tabla_paciente.focus()
        self.data = self.tabla_paciente.item(item)
        try:
            self.dni_paciente = self.data['values'][1]
            paciente.cargar_datos(self.dni_paciente)
            paciente.ventana_paciente()
        except:
            pass

    def eliminar_paciente(self):
        try:
            self.miConexion = sqlite3.connect("./bd/DBpaciente.sqlite3")
            self.miCursor = self.miConexion.cursor()
            msg_box = messagebox.askquestion('Eliminar paciente', '¿Desea elminar al paciente?', icon='warning')
            if msg_box == 'yes':
                self.miCursor.execute("DELETE FROM Paciente WHERE dni = ?", (self.dni_paciente,))
                self.miConexion.commit()
                messagebox.showinfo("ELIMINAR","Paciente eliminado exitosamente")
                self.mostrar_pacientes()
        except:
            messagebox.showinfo("ELIMINAR", "No se ha podido elimnar el paciente")

    def cargar_tabla_pacientes(self):
        self.miConexion = sqlite3.connect("./bd/DBpaciente.sqlite3")
        self.miCursor = self.miConexion.cursor()
        bd = "SELECT Apellido, Nombre, DNI, Telefono, ObraSocial FROM Paciente ORDER BY Apellido"
        self.miCursor.execute(bd)
        pacientes = self.miCursor.fetchall()
        return pacientes

    def cargar_pacientes_previos(self):
        global indice_paciente
        self.boton_pos.config(state= 'normal', bg= '#1F704B')
        if indice_paciente == 0:
            self.boton_previo.config(state= 'disabled', bg= '#1F704B')

        paciente_lista = self.cargar_tabla_pacientes()
        offset = len(paciente_lista)%incremento
        if indice_paciente ==  len(paciente_lista):
            indice_paciente = indice_paciente - offset
            if offset == 0:
                indice_paciente = indice_paciente - incremento
        indice_paciente = indice_paciente - incremento
        if(indice_paciente >= 0):
            self.tabla_paciente.delete(*self.tabla_paciente.get_children())
            for i in range(indice_paciente, indice_paciente + incremento):
                self.tabla_paciente.insert('', i, text = paciente_lista[i][0], values= (paciente_lista[i][1], paciente_lista[i][2], paciente_lista[i][3], paciente_lista[i][4]))            
        if indice_paciente < 0 :
            indice_paciente = 0

    def cargar_pacientes_posteriores(self):
        global indice_paciente
        self.boton_previo.config(state= 'normal', bg= '#1F704B')
        paciente_lista = self.cargar_tabla_pacientes()
        if indice_paciente != len(paciente_lista):
            indice_paciente = indice_paciente + incremento
            if indice_paciente+incremento <= len(paciente_lista):
                self.tabla_paciente.delete(*self.tabla_paciente.get_children())
                for i in range(indice_paciente, indice_paciente + incremento):
                    self.tabla_paciente.insert('', i, text = paciente_lista[i][0], values=(paciente_lista[i][1], paciente_lista[i][2], paciente_lista[i][3], paciente_lista[i][4]))
                if(indice_paciente+incremento == len(paciente_lista)):
                    indice_paciente = len(paciente_lista)
                    self.boton_pos.config(state= 'disabled', bg= '#1F704B')
            elif indice_paciente+incremento > len(paciente_lista):
                offset = len(paciente_lista)%incremento
                self.tabla_paciente.delete(*self.tabla_paciente.get_children())
                for i in range(indice_paciente, indice_paciente + offset):
                    self.tabla_paciente.insert('', i, text = paciente_lista[i][0], values=(paciente_lista[i][1], paciente_lista[i][2], paciente_lista[i][3], paciente_lista[i][4]))        
                indice_paciente = len(paciente_lista)
                self.boton_pos.config(state= 'disabled', bg= '#1F704B')

    def mostrar_pacientes(self):
        global indice_paciente
        self.boton_pos.config(state= 'normal', bg= '#1F704B')
        self.boton_previo.config(state= 'disabled', bg= '#1F704B')
        indice_paciente= 0
        self.miConexion = sqlite3.connect("./bd/DBpaciente.sqlite3")
        self.miCursor = self.miConexion.cursor()
        bd = "SELECT Apellido, Nombre, DNI, Telefono, ObraSocial FROM Paciente ORDER BY Apellido"
        self.miCursor.execute(bd)
        datos = self.miCursor.fetchall()
        self.tabla_paciente.delete(*self.tabla_paciente.get_children())
        for i in range(0, incremento):
                self.tabla_paciente.insert('', i, text= datos[i][0], values=(datos[i][1], datos[i][2], datos[i][3], datos[i][4]))

    def buscar_paciente(self):
        self.miConexion = sqlite3.connect("./bd/DBpaciente.sqlite3")
        self.miCursor = self.miConexion.cursor()
        self.buscar = self.dato_paciente.get()

        bd = f"SELECT Apellido, Nombre, DNI, Telefono, ObraSocial FROM Paciente WHERE Apellido LIKE '%{self.buscar}%' OR Nombre LIKE '%{self.buscar}%' ORDER BY Nombre DESC"
        self.miCursor.execute(bd)
        datos = self.miCursor.fetchall()
        self.tabla_paciente.delete(*self.tabla_paciente.get_children())
        i = -1
        for dato in datos:
            i= i+1
            self.tabla_paciente.insert('', i, text = datos[i][0], values=(datos[i][1], datos[i][2], datos[i][3], datos[i][4]))
    def buscar_historia(self):
        self.miConexion = sqlite3.connect("./bd/DBpaciente.sqlite3")
        self.miCursor = self.miConexion.cursor()
        self.buscar = self.dato_paciente.get()

        bd = f"SELECT Apellido, Nombre, DNI, ObraSocial FROM Paciente WHERE Apellido LIKE '%{self.buscar}%' OR Nombre LIKE '%{self.buscar}%' ORDER BY Apellido DESC"
        self.miCursor.execute(bd)
        datos = self.miCursor.fetchall()
        self.tabla_historia.delete(*self.tabla_historia.get_children())
        i = -1
        for dato in datos:
            i= i+1
            self.tabla_historia.insert('', i, text = datos[i][0], values=(datos[i][0], datos[i][1], datos[i][2], datos[i][3]))

    def seleccionar_paciente(self, event):
        item = self.tabla_paciente.focus()
        self.data = self.tabla_paciente.item(item)
        self.dni_paciente = self.data['values'][1]

    def mostrar_usuarios(self):
        self.miConexion = sqlite3.connect("./bd/consultorio.sqlite3")
        self.miCursor = self.miConexion.cursor()
        bd = "SELECT Nombre_usuario, Clave, Tipo_usuario FROM Usuarios"
        self.miCursor.execute(bd)
        datos = self.miCursor.fetchall()
        self.tabla_usuario.delete(*self.tabla_usuario.get_children())
        i = -1
        for dato in datos:
            i= i+1
            self.tabla_usuario.insert('', i, text = datos[i][0], values=("*********", datos[i][2]))

    def seleccionar_usuario(self, event):
        (sel,) = self.tabla_usuario.selection()
        self.nombre_usuario = self.tabla_usuario.item(sel, "text")

    def agregar_usuario(self):
        user = Usuario()
        user.conexionBBDD()
        user.ventana()

    def editar_usuario(self, event):
        try:
            (sel,) = self.tabla_usuario.selection()
            self.usuario = self.tabla_usuario.item(sel, "text")
            user = Usuario()
            user.conexionBBDD()
            user.cargar_datos(self.usuario)
            user.ventana()
        except:
            pass

    def eliminar_usuario(self):
        #print(self.nombre_usuario)
        user = Usuario()
        user.conexionBBDD()
        user.eliminar_usuario(self.nombre_usuario)
        self.mostrar_usuarios()

    def nada(self):
        pass    

    def widgets(self):
        self.imagen_usuario = utl.leer_imagen('dentist-icon2-removebg-preview.png', (38, 38))
        #tself.imagen_menu = PhotoImage(file ='./imagenes/menu4-removebg-preview.png')
        self.imagen_paciente = PhotoImage(file= './imagenes/agregar3.png')
        self.imagen_calendario = PhotoImage(file= './imagenes/calendario-removebg-preview.png')
        self.imagen_historia_clinica = PhotoImage(file= './imagenes/historial3.png')
        self.imagen_galeria = PhotoImage(file= './imagenes/foto-removebg-preview.png')
        self.imagen_agregar_paciente = PhotoImage(file= './imagenes/agregar_paciente.png')
        self.imagen_editar_paciente = PhotoImage(file= './imagenes/editar_paciente.png')
        self.imagen_refrescar = PhotoImage(file= './imagenes/refrescar.png')
        self.imagen_eliminar_paciente = PhotoImage(file= './imagenes/eliminar22.png')
        self.imagen_salir = PhotoImage(file= './imagenes/salir.png')
        self.logo = PhotoImage(file= './imagenes/logo1.png')

        try:
            self.imagen_inicio = PhotoImage(file ='./imagenes/home-removebg-preview.png')
            self.imagen_menu = PhotoImage(file ='./imagenes/menu4-removebg-preview.png')
            self.bt_inicio = Button(self.frame_inicio, image= self.imagen_inicio, bg= '#1F704B', activebackground= 'white', bd= 0, command= self.menu_lateral)
            self.bt_cerrar = Button(self.frame_inicio, image= self.imagen_menu, bg= '#1F704B', activebackground= 'white', bd= 0, command= self.menu_lateral)
        except:
            self.bt_inicio = Button(self.frame_inicio, text= 'INICIO', font= (fuente2, 12, 'bold'), bg= '#1F704B', activebackground= 'white', bd= 0, command= self.menu_lateral)
            self.bt_cerrar = Button(self.frame_inicio, text= '☰', font= ('Comic Sans MS', 12, 'bold'), bg= '#1F704B', activebackground= 'white', bd= 0, command= self.menu_lateral)

        self.bt_inicio.grid(column= 0, row= 0, padx= 5, pady= 10)
        self.bt_cerrar.grid(column= 0, row= 0, padx= 5, pady= 10)

		#BOTONES Y ETIQUETAS DEL MENU LATERAL
        Button(self.frame_menu, image= self.imagen_usuario, bg= '#1F704B', activebackground= 'white', bd= 0, command= self.pantalla_usuarios).grid(column= 0, row= 1, pady= 20, padx= 10)
        Button(self.frame_menu, image= self.imagen_paciente, bg= '#1F704B', activebackground= 'white', bd= 0, command= self.pantalla_pacientes).grid(column= 0, row= 2, pady= 20, padx= 10)
        Button(self.frame_menu, image= self.imagen_calendario, bg= '#1F704B', activebackground= 'white', bd= 0, command= self.pantalla_calendario ).grid(column= 0, row= 3, pady= 20, padx= 10)
        Button(self.frame_menu, image= self.imagen_historia_clinica, bg= '#1F704B',activebackground= 'white', bd= 0, command= self.pantalla_historia).grid(column= 0, row= 4, pady= 20, padx= 10)
        Button(self.frame_menu, image= self.imagen_galeria, bg= '#1F704B', activebackground= 'white', bd= 0, command= self.pantalla_galeria).grid(column=0, row=5, pady=20, padx=10)
        Button(self.frame_menu, image= self.imagen_salir, bg= '#1F704B', activebackground= 'white', bd= 0, command= self.salir).grid(column= 0, row= 7, pady= 20, padx= 10)

        Label(self.frame_menu, text= 'Usuarios', bg= '#1F704B', fg= 'white', font= (fuente2, 12, 'bold')).grid(column= 1, row= 1, pady= 20, padx= 2)
        Label(self.frame_menu, text= 'Pacientes', bg= '#1F704B', fg= 'white', font= (fuente2, 12, 'bold')).grid(column= 1, row= 2, pady= 20, padx= 2)
        Label(self.frame_menu, text= 'Calendario', bg= '#1F704B', fg= 'white', font= (fuente2, 12, 'bold')).grid(column= 1, row= 3, pady= 20, padx= 2)
        Label(self.frame_menu, text= 'Historia \nClinica', bg= '#1F704B', fg= 'white', font= (fuente2, 12, 'bold')).grid(column= 1, row= 4, pady= 20, padx= 2)
        Label(self.frame_menu, text= 'Galeria', bg= '#1F704B', fg= 'white', font= (fuente2, 12, 'bold')).grid(column= 1, row= 5, pady= 20, padx= 2)
        Label(self.frame_menu, text= 'Salir', bg= '#1F704B', fg= 'white', font= (fuente2, 12, 'bold')).grid(column= 1, row= 7, pady= 20, padx= 2)

		#############################  CREAR  PAGINAS  ##############################
        estilo_paginas = ttk.Style()
        estilo_paginas.layout('TNotebook.Tab', []) #desactiva las pestañas
##        estilo_paginas.configure("TNotebook", background='#1F704B', foreground='#1F704B', padding= 0, borderwidth= 0)
##        estilo_paginas.theme_use('default')
##        estilo_paginas.configure("TNotebook", background='#1F704B', borderwidth= 0)
##        estilo_paginas.configure("TNotebook.Tab", background="#1F704B", borderwidth= 0)
##        estilo_paginas.map("TNotebook", background=[("selected", '#1F704B')])
##        estilo_paginas.map("TNotebook.Tab", background=[("selected", '#1F704B')], foreground=[("selected", '#1F704B')]);

        self.paginas = ttk.Notebook(self.frame_raiz, style= 'TNotebook')
        self.paginas.grid(column= 0, row= 0, sticky= 'nsew')
        self.frame_principal = Frame(self.paginas, bg= 'gray90') #color de fondo
        self.frame_usuarios = Frame(self.paginas, bg= 'gray90') #color de fondo
        self.frame_pacientes = Frame(self.paginas, bg= 'gray90') #color de fondo
        self.frame_calendario = Frame(self.paginas, bg= 'gray90')
        self.historia = Frame(self.paginas, bg= 'gray90')
        self.frame_galeria = Frame(self.paginas, bg= 'gray90')
        self.paginas.add(self.frame_principal)
        self.paginas.add(self.frame_usuarios)
        self.paginas.add(self.frame_pacientes)
        self.paginas.add(self.frame_calendario)
        self.paginas.add(self.historia)
        self.paginas.add(self.frame_galeria)

		##############################         PAGINAS       #############################################
		######################## FRAME TITULO #################
        self.titulo = Label(self.frame_top, text= 'Consultorio Odontológico MyM', bg= '#1F704B', fg= 'white', font= ('Comic Sans MS', 15, 'bold'))
        self.titulo.pack(expand= 1)

		######################## VENTANA PRINCIPAL #################
        Label(self.frame_principal, image= self.logo, bg= 'gray90').pack(expand= 1)

        #ESTILO DE LAS TABLAS DE DATOS TREEVIEW
        self.estilo_tabla = ttk.Style()
        #estilo_tabla.theme_use('classic')
        self.estilo_tabla.configure("Treeview", font= fuenten, foreground= 'black', rowheight= 30)
        #estilo_tabla.map('Treeview.Heading', background=[('selected', '#1F704B')], foreground=[('selected','white')] )
        self.estilo_tabla.configure('Treeview.Heading', background= 'green', fg= 'black', padding= 3, font= fuenteb)
##        estilo_tabla.configure('Item', foreground = 'red', focuscolor ='green')
##        estilo_tabla.configure('TScrollbar', arrowcolor = 'white', bordercolor  ='black', troughcolor= 'white', background ='white')

        ######################## USUARIOS #################
        Label(self.frame_usuarios, text= 'USUARIOS', bg= 'gray90', fg= '#1F704B', font= ('Comic Sans MS', 15, 'bold')).grid(column= 0, row= 0, columnspan= 3, padx=5, sticky="W")       
        Button(self.frame_usuarios, image= self.imagen_agregar_paciente, text= 'AGREGAR', fg= 'black', font= fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, command= self.agregar_usuario).grid(column= 0, row= 1, pady= 5)
        Label(self.frame_usuarios, text= 'Agregar', bg= 'gray90', fg= 'black', font= fuenteb).grid(column= 0, row= 2)
        Button(self.frame_usuarios, image= self.imagen_eliminar_paciente, text= 'ELIMINAR', fg= 'black', font= fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, command= self.eliminar_usuario).grid(column= 1, row= 1, pady= 5)
        Label(self.frame_usuarios, text= 'Eliminar', bg= 'gray90', fg= 'black', font= fuenteb).grid(column= 1, row= 2)
        Button(self.frame_usuarios, image= self.imagen_refrescar, text= 'REFRESCAR', fg= 'black', font = fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, command= self.mostrar_usuarios).grid(column= 2, row= 1, pady= 5)
        Label(self.frame_usuarios, text= 'Refrescar', bg= 'gray90', fg= 'black', font= fuenteb).grid(column= 2, row= 2)

        #TABLA USUARIO
        self.frame_tabla_usuario = Frame(self.frame_usuarios, bg= 'gray90')
        self.frame_tabla_usuario.grid(columnspan= 3, row= 3, sticky= 'nsew')
        self.tabla_usuario = ttk.Treeview(self.frame_tabla_usuario, selectmode ='browse')
        self.tabla_usuario.grid(column= 0, row= 3, columnspan= 3, sticky='nsew')
        ladoy = ttk.Scrollbar(self.frame_tabla_usuario, orient ='vertical', command = self.tabla_usuario.yview)
        ladoy.grid(column = 4, row = 3, sticky='ns')
        self.tabla_usuario.configure(yscrollcommand = ladoy.set)
        self.tabla_usuario['columns'] = ( 'Clave', 'Tipo_usuario')
        self.tabla_usuario.column('#0', minwidth= 100, width= 120, anchor= 'w')
        self.tabla_usuario.column('Clave', minwidth= 100, width= 120, anchor= 'center')
        self.tabla_usuario.column('Tipo_usuario', minwidth= 100, width= 120, anchor= 'e')

        self.tabla_usuario.heading('#0', text= 'Usuario', anchor= 'center')
        self.tabla_usuario.heading('Clave', text= 'Clave', anchor= 'center')
        self.tabla_usuario.heading('Tipo_usuario', text= 'Tipo de usuario', anchor= 'center')
        self.mostrar_usuarios()
        self.tabla_usuario.bind("<Double-1>", self.editar_usuario)
        self.tabla_usuario.bind("<<TreeviewSelect>>", self.seleccionar_usuario)

		######################## PACIENTES #################
        Label(self.frame_pacientes, text= 'PACIENTES', bg= 'gray90', fg= '#1F704B', font= ('Comic Sans MS', 15, 'bold')).grid(column= 0, row= 0, columnspan= 4, padx=5, sticky="W")       
        Button(self.frame_pacientes, image= self.imagen_agregar_paciente, text= 'AGREGAR', fg= 'black', font= fuenten, bg= '#1F704B', bd= 2, borderwidth= 2, command= self.agregar_paciente).grid(column= 0, row= 1, pady= 5)
        Label(self.frame_pacientes, text= 'Agregar', bg= 'gray90', fg= 'black', font= fuenteb).grid(column= 0, row= 2)
        Button(self.frame_pacientes, image= self.imagen_eliminar_paciente, text= 'ELIMINAR', fg= 'black', font= fuenten, bg= '#1F704B', bd= 2, borderwidth= 2, command= self.eliminar_paciente).grid(column= 1, row= 1, pady= 5)
        Label(self.frame_pacientes, text= 'Eliminar', bg= 'gray90', fg= 'black', font= fuenteb).grid(column= 1, row= 2)
        Button(self.frame_pacientes, image= self.imagen_refrescar, text= 'REFRESCAR', fg= 'black', font = fuenten, bg= '#1F704B', bd= 2, borderwidth= 2, command= self.mostrar_pacientes).grid(column= 2, row= 1, pady= 5)
        Label(self.frame_pacientes, text= 'Refrescar', bg= 'gray90', fg= 'black', font= fuenteb).grid(column= 2, row= 2)
        self.busqueda = ttk.Entry(self.frame_pacientes, textvariable= self.dato_paciente, width= 20 ,font= fuenten).grid(column= 3, row= 1, pady= 5)
        Button(self.frame_pacientes, text= 'Buscar', bg= '#1F704B', fg= 'black', font= fuenteb, command= self.buscar_paciente).grid(column= 3, row= 2, pady=(0,5))

        self.boton_previo = tk.Button(self.frame_pacientes, text= '<', fg= 'black', font = fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, width= 5, command= self.cargar_pacientes_previos)
        self.boton_previo.grid(column= 0, row= 3, padx= 10, pady=(0,5), sticky= "W")
        self.boton_pos = tk.Button(self.frame_pacientes, text= '>', fg= 'black', font = fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, width= 5, command= self.cargar_pacientes_posteriores)
        self.boton_pos.grid(column= 3, row= 3, padx=(0,10), pady=(0,5), sticky= "E")

		#TABLA PACIENTE
        self.frame_tabla_paciente = Frame(self.frame_pacientes, bg= 'gray90')
        self.frame_tabla_paciente.grid(columnspan= 4, row= 4, sticky= 'nsew')
        self.tabla_paciente = ttk.Treeview(self.frame_tabla_paciente, selectmode= 'browse')
        self.tabla_paciente.grid(column= 0, row= 4, columnspan= 4, sticky= 'nsew')
        ladoy = ttk.Scrollbar(self.frame_tabla_paciente, orient= 'vertical', command= self.tabla_paciente.yview)
        ladoy.grid(column = 5, row = 4, sticky= 'ns')
        self.tabla_paciente.configure(yscrollcommand = ladoy.set)
        self.tabla_paciente['columns'] = ('Nombre', 'D.N.I.', 'Teléfono', 'Obra Social')
        self.tabla_paciente.column('#0', minwidth= 100, width= 120, anchor= 'w')
        self.tabla_paciente.column('Nombre', minwidth= 100, width= 130 , anchor= 'w')
        self.tabla_paciente.column('D.N.I.', minwidth= 100, width= 120, anchor= 'center' )
        self.tabla_paciente.column('Teléfono', minwidth= 100, width= 120 , anchor= 'center')
        self.tabla_paciente.column('Obra Social', minwidth= 100, width= 105, anchor= 'center')

        self.tabla_paciente.heading('#0', text= 'Apellido', anchor= 'center', command= self.nada)
        self.tabla_paciente.heading('Nombre', text= 'Nombre', anchor= 'center')
        self.tabla_paciente.heading('D.N.I.', text= 'D.N.I.', anchor = 'center')
        self.tabla_paciente.heading('Teléfono', text= 'Teléfono', anchor= 'center')
        self.tabla_paciente.heading('Obra Social', text= 'Obra Social', anchor= 'center')
        self.mostrar_pacientes()
        self.tabla_paciente.bind("<<TreeviewSelect>>", self.seleccionar_paciente)
        self.tabla_paciente.bind("<Double-1>", self.editar_paciente)

		######################## HISTORIA CLINICA #################
        Label(self.historia, text= 'HISTORIA CLINICA', fg= '#1F704B', bg='gray90', font=('Comic Sans MS', 24, 'bold')).grid(columnspan= 4, row= 0)
        self.busqueda = ttk.Entry(self.historia, textvariable= self.dato_paciente, width= 20 ,font= fuenten).grid(column= 1, row= 1, pady= 5, sticky="W")
        Button(self.historia, text= 'Buscar', bg= '#1F704B', fg= 'black', font= fuenteb, command= self.buscar_historia).grid(column= 0, row= 1, padx=(10,5))
        
        self.frame_tabla_historia= Frame(self.historia, bg= 'gray90')
        self.frame_tabla_historia.grid(columnspan= 4, row= 4, sticky= 'nsew')
        self.tabla_historia = ttk.Treeview(self.historia, columns= ("Apellido", "Nombre", "D.N.I.", "Obra social"), show= 'headings', height= 25, selectmode ='browse')
        self.tabla_historia.grid(column= 0, row= 4, columnspan= 4, sticky= 'nsew')
        ladoy = ttk.Scrollbar(self.frame_tabla_historia, orient= 'vertical', command= self.tabla_historia.yview)
        ladoy.grid(column = 5, row = 4, sticky= 'ns')
        self.tabla_historia.configure(yscrollcommand = ladoy.set)
        self.tabla_historia.heading("Apellido", text= "Apellido")
        self.tabla_historia.heading("Nombre", text= "Nombre")
        self.tabla_historia.heading("D.N.I.", text= "D.N.I.")
        self.tabla_historia.heading("Obra social", text= "Obra social")

        # # Ajustar el ancho de las columnas
        # self.tabla_historia.column("Apellido", width= 70, anchor= 'center')
        # self.tabla_historia.column("Nombre", width= 200)
        # self.tabla_historia.column("D.N.I.", width= 250)
        # self.tabla_historia.column("Obra social", width= 200)
        
        #self.tabla_historia.bind("<Double-1>", self.editar_turno)

		######################## GALERIA #################
        Label(self.frame_galeria, text= 'GALERIA', fg= '#1F704B', bg= 'gray90', font=('Comic Sans MS', 24,'bold')).grid(column= 0,  row= 0)

        self.ventana.mainloop()