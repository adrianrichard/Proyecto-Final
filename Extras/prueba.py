import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.font import BOLD
from tkinter import  messagebox, Button, Label, Frame
import sqlite3

class Paciente():

    def conexionBBDD():
	    miConexion=sqlite3.connect("./bd/DBpaciente2.sqlite3")
	    miCursor=miConexion.cursor()

	    try:
		    miCursor.execute('''
			    CREATE TABLE Paciente (
			    ID INTEGER PRIMARY KEY AUTOINCREMENT,
			    NOMBRE VARCHAR(50) NOT NULL,
   			    APELLIDO VARCHAR(50) NOT NULL,
                DNI INT NOT NULL,
			    DOMICILIO VARCHAR(50) NOT NULL,
                TELEFONO INT NOT NULL,
			    EMAIL VARCHAR(50) NOT NULL,
                OBRASOCIAL VARCHAR(50) NOT NULL,
                NROSOCIO INT NOT NULL)
			    ''')

		    messagebox.showinfo("CONEXION","Base de Datos Creada exitosamente")

	    except:
		    messagebox.showinfo("CONEXION", "Conexión exitosa con la base de datos")


    def crear(self):
	    miConexion=sqlite3.connect("./bd/DBpaciente.sqlite3")
	    miCursor=miConexion.cursor()

        #np=

	    #datos=self.nombre_paciente.get(), self.apellido_paciente.get(),self.dni_paciente.get(), self.domicilio_paciente.get(),self.telefono_paciente.get(),self.email_paciente.get(),self.obrasocial_paciente.get(),self.nrosocio_paciente.get()
        #print(datos)
	    miCursor.execute("INSERT INTO Paciente VALUES(NULL,?,?)", (self.nombre_paciente.get(), self.apellido_paciente.get()))
	    miConexion.commit()

    def __init__(self):

        self.frame_paciente= tk.Tk()
        self.frame_paciente.title('DentalMatic')
        self.frame_paciente.geometry('1000x500')
        self.frame_paciente.config(bg='#fcfcfc')
        self.frame_paciente.resizable(width= 0, height= 0)
        #utl.centrar_ventana(self.frame_paciente, 900, 600)
        self.menu = True
        self.color = True
        self.frame_top = Frame(self.frame_paciente, bg= '#1F704B', height= 50)

        self.frame_top.grid(column= 1, row= 0, sticky= 'nsew')
        self.frame_principal = Frame(self.frame_paciente)
        self.frame_principal.grid(column= 1, row= 1, sticky= 'nsew')
        self.nombre_paciente = StringVar()
        self.apellido_paciente = StringVar()
        self.dni_paciente =  StringVar()
        self.domicilio_paciente =  StringVar()
        self.telefono_paciente =  StringVar()
        self.email_paciente =  StringVar()
        self.obrasocial_paciente =  StringVar()
        self.nrosocio_paciente =  StringVar()
        self.titulo = Label(self.frame_top, text= 'Paciente', bg= '#1F704B', fg= 'white', font= ('Comic Sans MS', 15, 'bold')).grid(column= 1, row=0, pady= 20, padx= 10)
        Button(self.frame_top, text= 'Cerrar',  font= ('Comic Sans MS', 15, BOLD), fg= 'white', bg= '#1F704B', activebackground= 'gray', bd= 0, command= self.frame_paciente.destroy).grid(column= 2, row=0, pady= 20, padx= 500)


        #conexionBBDD()

        #Entradas Y ETIQUETAS DATOS DEL PACIENTE
        self.nombre_paciente = ttk.Entry(self.frame_principal, font= ('Comic Sans MS', 14)).grid(column=1, row=1, pady=5, padx=10)
        self.apellido_paciente = ttk.Entry(self.frame_principal, font= ('Comic Sans MS', 14)).grid(column=1, row=2, pady=5, padx=10)
        self.dni_paciente = ttk.Entry(self.frame_principal, font= ('Comic Sans MS', 14)).grid(column=1, row=3, pady=5, padx=10)
        self.domicilio_paciente = ttk.Entry(self.frame_principal, font= ('Comic Sans MS', 14)).grid(column=1, row=4, pady=5, padx=10)
        self.telefono_pacient = ttk.Entry(self.frame_principal, font= ('Comic Sans MS', 14)).grid(column=1, row=5, pady=5, padx=10)
        self.email_paciente = ttk.Entry(self.frame_principal, font= ('Comic Sans MS', 14)).grid(column=1, row=6, pady=5, padx=10)
        self.obrasocial_paciente = ttk.Entry(self.frame_principal, font= ('Comic Sans MS', 14)).grid(column=1, row=7, pady=5, padx=10)
        self.nrosocio_paciente = ttk.Entry(self.frame_principal, font= ('Comic Sans MS', 14)).grid(column=1, row=8, pady=5, padx=10)

        Label(self.frame_principal, text= 'Nombre/s',  fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=1, pady=5, padx=2)
        Label(self.frame_principal, text= 'Apellido/s',  fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=2, pady=5, padx=2)
        Label(self.frame_principal, text= 'D.N.I.',  fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=3, pady=5, padx=2)
        Label(self.frame_principal, text= 'Domicilio',  fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=4, pady=5, padx=2)
        Label(self.frame_principal, text= 'Telefono', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=5, pady=5, padx=2)
        Label(self.frame_principal, text= 'Email', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=6, pady=5, padx=2)
        Label(self.frame_principal, text= 'Obra Social', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=7, pady=5, padx=2)
        Label(self.frame_principal, text= 'Nro de socio', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=8, pady=5, padx=2)
        Button(self.frame_principal, text= 'Crear',  font= ('Comic Sans MS', 12, BOLD), fg= 'white', bg= '#1F704B', activebackground= 'gray', bd= 0, command= self.crear).grid(column= 3, row=1, pady= 5, padx= 200)
        Button(self.frame_principal, text= 'Cancelar',  font= ('Comic Sans MS', 12, BOLD), fg= 'white', bg= '#1F704B', activebackground= 'gray', bd= 0, command= self.frame_paciente.destroy).grid(column= 3, row=2, pady= 5, padx= 200)
        Button(self.frame_principal, text= 'Limpiar datos',  font= ('Comic Sans MS', 12, BOLD), fg= 'white', bg= '#1F704B', activebackground= 'gray', bd= 0, command= self.frame_paciente.destroy).grid(column= 3, row=3, pady= 5, padx= 200)

        self.frame_paciente.mainloop()



#def only_numbers(char):
    #return char.isdigit()

if __name__ == "__main__":
    Paciente()

