import tkinter as tk
from tkinter.font import BOLD
import util.generic as utl
from tkinter import  Tk, Button, Entry, Label, ttk, PhotoImage
from tkinter import  StringVar,Scrollbar,Frame
from bd.conexion import Conexion

class Paciente:    
                                      
    def __init__(self):        
        self.frame_paciente= tk.Toplevel()
        self.frame_paciente.grab_set_global() # Obliga a las ventanas estar deshabilitadas y deshabilitar todos los eventos e interacciones con la ventana
        self.frame_paciente.focus_set() # Mantiene el foco cuando se abre la ventana.
        self.frame_paciente.title('DentalMatic')
        self.frame_paciente.geometry('1000x500')
        self.frame_paciente.config(bg='#fcfcfc')
        self.frame_paciente.resizable(width= 0, height= 0)
        utl.centrar_ventana(self.frame_paciente, 900, 600)
        self.menu = True
        self.color = True
        self.frame_top = Frame(self.frame_paciente, bg= 'black', height= 50)

        self.frame_top.grid(column= 1, row= 0, sticky= 'nsew')        
        self.frame_principal = Frame(self.frame_paciente, bg= 'white')
        self.frame_principal.grid(column= 1, row= 1, sticky= 'nsew')		
        self.frame_paciente.columnconfigure(1, weight= 1)
        self.frame_paciente.rowconfigure(1, weight= 1)
        self.frame_principal.columnconfigure(1, weight= 1)
        self.frame_principal.rowconfigure(1, weight= 1)
        self.titulo = Label(self.frame_top, text= 'Consultorio Odóntologico MyM', bg= 'black', fg= 'white', font= ('Comic Sans MS', 15, 'bold')).grid(column= 1, row=0, pady= 20, padx= 10)
        Button(self.frame_top, text= 'Cerrar', fg= 'white', bg= 'black', activebackground= 'black', bd= 0, command= self.frame_paciente.destroy).grid(column= 2, row=0, pady= 20, padx= 10)


    #def pantalla_inicial(self):
    

    #def pantalla_datos(self):
             
    #def pantalla_escribir(self):
     
    #def pantalla_actualizar(self):
        
    
    #def pantalla_buscar(self):

   # def pantalla_ajustes(self):
    
    #def agregar_paciente():
        
		#BOTONES Y ETIQUETAS DEL MENU LATERAL
        Button(self.frame_principal, text= 'Pacientes', fg= 'white', bg='black', activebackground='black', bd=0).grid(column=0, row=1, pady=20,padx=10)
        Button(self.frame_principal, text= 'Pacientes', fg= 'white', bg='black',activebackground='black', bd=0 ).grid(column=0, row=2, pady=20,padx=10)
        Button(self.frame_principal, text= 'Pacientes', fg= 'white', bg= 'black',activebackground='black', bd=0 ).grid(column=0, row=3, pady=20,padx=10)
        Button(self.frame_principal, text= 'Pacientes', fg= 'white', bg= 'black',activebackground='black', bd=0).grid(column=0, row=4, pady=20,padx=10)
        Button(self.frame_principal, text= 'Pacientes', fg= 'white', bg= 'black',activebackground='black', bd=0).grid(column=0, row=5, pady=20,padx=10)

        Label(self.frame_principal, text= 'Pacientes', bg= 'black', fg= 'white', font= ('Comic Sans MS', 12, 'bold')).grid(column=1, row=1, pady=20, padx=2)
        Label(self.frame_principal, text= 'Calendario', bg= 'black', fg= 'white', font= ('Comic Sans MS', 12, 'bold')).grid(column=1, row=2, pady=20, padx=2)
        Label(self.frame_principal, text= 'Historia \nClinica', bg= 'black', fg= 'white', font= ('Comic Sans MS', 12, 'bold')).grid(column=1, row=3, pady=20, padx=2)
        Label(self.frame_principal, text= 'Eliminar', bg= 'black', fg= 'white', font= ('Comic Sans MS', 12, 'bold')).grid(column=1, row=4, pady=20, padx=2)
        Label(self.frame_principal, text= 'Versión', bg= 'black', fg= 'white', font= ('Comic Sans MS', 12, 'bold')).grid(column=1, row=5, pady=20, padx=2)
        self.frame_paciente.mainloop()

if __name__ == "__main__":
    Paciente()
    #def agregar_paciente():
        

    '''    estilo_paginas = ttk.Style()
        estilo_paginas.configure("TNotebook", background='black', foreground='gray', padding=0, borderwidth=0)
        estilo_paginas.theme_use('default')
        estilo_paginas.configure("TNotebook", background='black', borderwidth=0)
        estilo_paginas.configure("TNotebook.Tab", background="black", borderwidth=0)
        estilo_paginas.map("TNotebook", background=[("selected", 'black')])
        estilo_paginas.map("TNotebook.Tab", background=[("selected", 'black')], foreground=[("selected", 'gray')]);

		#CREACCION DE LAS PAGINAS
        self.paginas = ttk.Notebook(self.frame_principal , style= 'TNotebook') #, style = 'TNotebook'
        self.paginas.grid(column=0,row=0, sticky='nsew')
        self.frame_uno = Frame(self.paginas, bg='white') #color de fondo
        self.frame_dos = Frame(self.paginas, bg='white') #color de fondo
        self.frame_tres = Frame(self.paginas, bg='white')
        self.frame_cuatro = Frame(self.paginas, bg='white')
        self.frame_cinco = Frame(self.paginas, bg='white')
        self.frame_seis = Frame(self.paginas, bg='white')
        self.paginas.add(self.frame_uno)
        self.paginas.add(self.frame_dos)
        self.paginas.add(self.frame_tres)
        self.paginas.add(self.frame_cuatro)
        self.paginas.add(self.frame_cinco)
        self.paginas.add(self.frame_seis)
	'''	
  ##############################         PAGINAS       #############################################
		######################## FRAME TITULO #################
        

		######################## VENTANA PRINCIPAL #################
        #Label(self.frame_principal, image= self.logo, bg='white').pack(expand= 1)

