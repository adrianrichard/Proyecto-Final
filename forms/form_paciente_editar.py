import tkinter as tk
from tkinter.font import BOLD
import util.generic as utl
from tkinter import messagebox, Button, Entry, Label #, PhotoImage
from tkinter import  StringVar, Frame
#from bd.conexion import Conexion
import sqlite3

class Paciente_update:    
    
    def conexionBBDD(self):
        
        try:
            self.miConexion=sqlite3.connect("./bd/DBpaciente.sqlite3")
            self.miCursor=self.miConexion.cursor()
            
        except:
            self.miCursor.execute('''
                CREATE TABLE Paciente (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NOMBRE VARCHAR(50) NOT NULL,
                APELLIDO VARCHAR(50) NOT NULL)
                ''')
            self.miConexion.commit()
            self.miConexion.close()

            messagebox.showinfo("CONEXION","Base de Datos Creada exitosamente")    
    
    def cargar_datos(self, dni):
        try:
            self.miCursor.execute("SELECT * FROM paciente WHERE dni=?", (dni,))
            campos=self.miCursor.fetchall()
        
            self.nombre_paciente.set(campos[0][1])
            self.apellido_paciente.set(campos[0][2])
            self.dni_paciente.set(dni)
            self.domicilio_paciente.set(campos[0][4])
            self.telefono_paciente.set(campos[0][5])
            self.email_paciente.set(campos[0][6])
            self.obrasocial_paciente.set(campos[0][7])
            self.nrosocio_paciente.set(campos[0][8])
        except:
            messagebox.showinfo("Buscar paciente", "No se ha podido encontrar el paciente")
            self.frame_paciente.destroy()

    def actualizar(self):
        datos=self.nombre_paciente.get(), self.apellido_paciente.get(), self.dni_paciente.get(), self.domicilio_paciente.get(),self.telefono_paciente.get(),self.email_paciente.get(),self.obrasocial_paciente.get(),self.nrosocio_paciente.get(),self.dni_actual
        
        try:
            sql="UPDATE Paciente SET nombre =?, apellido=?, dni=?, domicilio=?, telefono=?, email=?, obrasocial=?, nrosocio=? where dni=?"
            self.miCursor.execute(sql, datos)
            self.miConexion.commit()
            messagebox.showinfo("GUARDAR","Paciente actualizado exitosamente")
            self.frame_paciente.destroy()
        except:
            messagebox.showinfo("GUARDAR", "No se ha podido guardar el paciente")
        
    def Salir(self): 
        answer = messagebox.askokcancel(title='Salir', message='¿Desea salir sin guardar?', icon='warning')
        if answer:
            self.frame_paciente.destroy()
                                                 
    def __init__(self, dni, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self.frame_paciente= tk.Toplevel()
        self.frame_paciente.grab_set_global() # Obliga a las ventanas estar deshabilitadas y deshabilitar todos los eventos e interacciones con la ventana
        self.frame_paciente.focus_set() # Mantiene el foco cuando se abre la ventana.        

        self.frame_paciente.title('DentalMatic')
        self.frame_paciente.geometry('800x300')
        self.frame_paciente.config(bg='gray90')
        self.frame_paciente.resizable(width= 0, height= 0)
        utl.centrar_ventana(self.frame_paciente, 600, 450)
        self.menu = True
        self.color = True
        self.frame_top = Frame(self.frame_paciente, bg= '#1F704B', height= 50)
        self.dni_actual =dni

        self.frame_top.grid(column= 1, row= 0, sticky= 'nsew')
        self.frame_principal = Frame(self.frame_paciente)
        self.frame_principal.config(bg='gray90')
        self.frame_principal.grid(column= 1, row= 1, sticky= 'nsew')
        self.nombre_paciente = StringVar()
        self.apellido_paciente = StringVar()
        self.dni_paciente =  StringVar()
        self.domicilio_paciente =  StringVar()
        self.telefono_paciente =  StringVar()
        self.email_paciente =  StringVar()
        self.obrasocial_paciente =  StringVar()
        self.nrosocio_paciente =  StringVar()
        self.conexionBBDD()
        self.widgets()
        
    def widgets(self):       
        
        self.titulo = Label(self.frame_top, text= 'Datos del paciente', bg= '#1F704B', fg= 'white', font= ('Comic Sans MS', 15, 'bold')).grid(column= 0, row=0, pady= 20, padx= 10)
        Button(self.frame_principal, text= 'Cerrar',  font= ('Comic Sans MS', 12, BOLD), fg= 'white', bg= '#1F704B', activebackground= 'gray', bd= 2, command= self.Salir).grid(column= 2, row=3, pady= 5, padx= 100)
        
        self.cargar_datos(self.dni_actual)
        #Entradas Y ETIQUETAS DATOS DEL PACIENTE
        Entry(self.frame_principal, textvariable=self.nombre_paciente, font= ('Comic Sans MS', 14)).grid(column=1, row=1, pady=5, padx=10)
        Entry(self.frame_principal, textvariable=self.apellido_paciente, font= ('Comic Sans MS', 14)).grid(column=1, row=2, pady=5, padx=10)
        Entry(self.frame_principal, textvariable=self.dni_paciente, font= ('Comic Sans MS', 14)).grid(column=1, row=3, pady=5, padx=10)
        Entry(self.frame_principal, textvariable=self.domicilio_paciente, font= ('Comic Sans MS', 14)).grid(column=1, row=4, pady=5, padx=10)
        Entry(self.frame_principal, textvariable=self.telefono_paciente, font= ('Comic Sans MS', 14)).grid(column=1, row=5, pady=5, padx=10)
        Entry(self.frame_principal, textvariable=self.email_paciente, font= ('Comic Sans MS', 14)).grid(column=1, row=6, pady=5, padx=10)
        Entry(self.frame_principal, textvariable=self.obrasocial_paciente, font= ('Comic Sans MS', 14)).grid(column=1, row=7, pady=5, padx=10)
        Entry(self.frame_principal, textvariable=self.nrosocio_paciente, font= ('Comic Sans MS', 14)).grid(column=1, row=8, pady=5, padx=10)

        Label(self.frame_principal, text= 'Nombre/s', bg='gray90', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=1, pady=5, padx=2)
        Label(self.frame_principal, text= 'Apellido/s', bg='gray90', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=2, pady=5, padx=2)
        Label(self.frame_principal, text= 'D.N.I.', bg='gray90', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=3, pady=5, padx=2)
        Label(self.frame_principal, text= 'Domicilio', bg='gray90', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=4, pady=5, padx=2)
        Label(self.frame_principal, text= 'Telefono', bg='gray90', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=5, pady=5, padx=2)
        Label(self.frame_principal, text= 'Email', bg='gray90', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=6, pady=5, padx=2)
        Label(self.frame_principal, text= 'Obra Social', bg='gray90', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=7, pady=5, padx=2)
        Label(self.frame_principal, text= 'Nro de socio', bg='gray90', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=8, pady=5, padx=2)
        Button(self.frame_principal, text= 'Actualizar',  font= ('Comic Sans MS', 12, BOLD), fg= 'white', bg= '#1F704B', activebackground= 'gray', bd= 2, command=self.actualizar).grid(column= 2, row=1, pady= 5, padx= 100)

        self.frame_paciente.mainloop()
        
if __name__ == "__main__":
    Paciente_update()