import tkinter as tk
from tkinter import ttk
from tkinter.font import BOLD
import util.generic as utl
from tkinter import messagebox, Button, Entry, Label, StringVar, Frame
#from bd.conexion import Conexion
import sqlite3

class Usuario:

    def conexionBBDD(self):

        try:
            self.miConexion=sqlite3.connect("./bd/consultorio.sqlite3")
            self.miCursor=self.miConexion.cursor()

        except:
            self.miCursor.execute('''
                CREATE TABLE Usuarios (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NOMBRE_USUARIO VARCHAR(50) NOT NULL,
                CLAVE VARCHAR(50) NOT NULL
                TIPO_USUARIO VARCHAR(50) NOT NULL)
                ''')
            self.miConexion.commit()
            self.miConexion.close()

            messagebox.showinfo("CONEXION","Base de Datos Creada exitosamente")

    def guardar(self):
        self.miConexion=sqlite3.connect("./bd/consultorio.sqlite3")
        self.miCursor=self.miConexion.cursor()
        datos=self.nombre_usuario.get(), self.clave.get(), self.tipo_usuario.get(), 1
        try:
            self.miCursor.execute("INSERT INTO Usuarios VALUES(?,?,?,?)", (datos))
            self.miConexion.commit()
            messagebox.showinfo("GUARDAR","Paciente guardado exitosamente")
            self.frame_usuario.destroy()
        except:
            messagebox.showinfo("GUARDAR", "No se ha podido guardar el paciente")
    
    def ventana(self):
        self.frame_usuario= tk.Toplevel()
        self.frame_usuario.grab_set_global() # Obliga a las ventanas estar deshabilitadas y deshabilitar todos los eventos e interacciones con la ventana
        self.frame_usuario.focus_set() # Mantiene el foco cuando se abre la ventana.

        self.frame_usuario.title('DentalMatic')
        self.frame_usuario.geometry('800x300')
        self.frame_usuario.config(bg='gray90')
        self.frame_usuario.resizable(width= 0, height= 0)
        utl.centrar_ventana(self.frame_usuario, 600, 450)
        self.menu = True
        self.color = True
        self.frame_top = Frame(self.frame_usuario, bg= '#1F704B', height= 50)

        self.frame_top.grid(column= 1, row= 0, sticky= 'nsew')
        self.frame_principal = Frame(self.frame_usuario)
        self.frame_principal.config(bg='gray90')
        self.frame_principal.grid(column= 1, row= 1, sticky= 'nsew')

        self.conexionBBDD()
        
        Button(self.frame_principal, text= 'Cerrar',  font= ('Comic Sans MS', 12, BOLD), fg= 'white', bg= '#1F704B', activebackground= 'gray', bd= 2, command= self.Salir).grid(column= 2, row=3, pady= 5, padx= 50)

        #Entradas Y ETIQUETAS DATOS DEL USUARIO
        Entry(self.frame_principal, textvariable=self.nombre_usuario, font= ('Comic Sans MS', 14)).grid(column=1, row=1, pady=5, padx=10)
        Entry(self.frame_principal, textvariable=self.clave, font= ('Comic Sans MS', 14)).grid(column=1, row=2, pady=5, padx=10)        
        
        Label(self.frame_principal, text= 'Nombre del usuario', bg='gray90', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=1, pady=5, padx=2)
        Label(self.frame_principal, text= 'Clave', bg='gray90', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=2, pady=5, padx=2)
        combo=ttk.Combobox(self.frame_principal, textvariable=self.tipo_usuario, font= ('Comic Sans MS', 14), state="readonly", values=["administrador", "odontologo", "secretario"])
        combo.grid(column=1, row=3, pady=5, padx=10)

        Label(self.frame_principal, text= 'Tipo de usuario', bg='gray90', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=3, pady=5, padx=2)
        if(self.nombre_usuario.get()==''):
            self.titulo = Label(self.frame_top, text= 'Crear usuario', bg= '#1F704B', fg= 'white', font= ('Comic Sans MS', 15, 'bold')).grid(column= 0, row=0, pady= 20, padx= 10)
            Button(self.frame_principal, text= 'Guardar',  font= ('Comic Sans MS', 12, BOLD), fg= 'white', bg= '#1F704B', activebackground= 'gray', bd= 2, command= self.guardar).grid(column= 2, row=1, pady= 5, padx= 50)
        else:
            self.titulo = Label(self.frame_top, text= 'Actualizar usuario', bg= '#1F704B', fg= 'white', font= ('Comic Sans MS', 15, 'bold')).grid(column= 0, row=0, pady= 20, padx= 10)
            Button(self.frame_principal, text= 'Actualizar',  font= ('Comic Sans MS', 12, BOLD), fg= 'white', bg= '#1F704B', activebackground= 'gray', bd= 2, command= self.actualizar).grid(column= 2, row=1, pady= 5, padx= 50)
        self.frame_usuario.mainloop()
    
    def cargar_datos(self, usuario):
        self.nombre_usuario.set(usuario)
        
        try:
            self.miCursor.execute("SELECT * FROM Usuarios WHERE Nombre_usuario=?", (usuario,))
            campos=self.miCursor.fetchall()        
            #self.nombre_usuario.set(usuario)
            self.clave.set(campos[0][1])
            self.tipo_usuario.set(campos[0][2])
            self.id_usuario.set(campos[0][3])
        except:
            messagebox.showinfo("Buscar paciente", "No se ha podido encontrar el paciente")            
            self.frame_usuario.destroy()

    def actualizar(self):
        self.miConexion=sqlite3.connect("./bd/consultorio.sqlite3")
        self.miCursor=self.miConexion.cursor()
        user = self.nombre_usuario.get()
        datos=self.nombre_usuario.get(), self.clave.get(), self.tipo_usuario.get(), self.id_usuario.get(), user
        #print(datos)
        try:
            sql="UPDATE Usuarios SET Nombre_usuario =?, Clave=?, Tipo_usuario=?, ID=? where Nombre_usuario=?"
            self.miCursor.execute(sql, datos)
            self.miConexion.commit()
            messagebox.showinfo("GUARDAR","Paciente actualizado exitosamente")
            self.frame_usuario.destroy()
        except:
            messagebox.showinfo("GUARDAR", "No se ha podido guardar el paciente")
                
    def Salir(self):
        answer = messagebox.askokcancel(title='Salir', message='¿Desea salir sin guardar?', icon='warning')
        if answer:
            self.frame_usuario.destroy()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombre_usuario = StringVar()
        self.clave = StringVar()
        self.tipo_usuario =  StringVar()
        self.id_usuario =  StringVar()
        #self.nombre_usuario.set('')        

if __name__ == "__main__":
    Usuario()