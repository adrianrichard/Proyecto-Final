import tkinter as tk
from tkinter import ttk
from tkinter.font import BOLD
import util.generic as utl
from tkinter import messagebox, Button, Entry, Label, StringVar, Frame
#from bd.conexion import Conexion
import sqlite3
fuenteb= utl.definir_fuente('MS Sans Serif', 12, 'BOLD')
fuenten= utl.definir_fuente('MS Sans Serif', 12, 'normal')
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
        if (self.usuario_existente(self.nombre_usuario.get())):
            print("existe")
        if(utl.validar_password(self.clave.get())):
            datos=self.nombre_usuario.get(), self.clave.get(), self.tipo_usuario.get()
            Label(self.frame_principal, text= 'Contraseña valida', anchor="w", width=20, bg='gray90', fg= 'red', font= fuenten).grid(column=2, row=2, pady=5, padx=2)
            try:
                self.miCursor.execute("INSERT INTO Usuarios VALUES(NULL,?,?,?)", (datos))
                self.miConexion.commit()
                #messagebox.showinfo("GUARDAR","Usuario guardado exitosamente")
                self.frame_usuario.destroy()
            except:
                messagebox.showinfo("GUARDAR", "No se ha podido guardar el usuario")
        else:
            Label(self.frame_principal, text= 'Contraseña invalida', anchor="w", width=20, bg='gray90', fg= 'red', font= fuenten).grid(column=2, row=2, pady=5, padx=2)
    
    def cargar_datos(self, usuario):
        self.nombre_usuario.set(usuario)        
        try:
            self.miCursor.execute("SELECT * FROM Usuarios WHERE Nombre_usuario=?", (usuario,))
            campos=self.miCursor.fetchall()        
            #self.nombre_usuario.set(usuario)
            self.clave.set(campos[0][2])
            self.tipo_usuario.set(campos[0][3])
            #self.id_usuario.set(campos[0][2])
        except:
            messagebox.showinfo("Buscar usuario", "No se ha podido encontrar el usuario")            
            self.frame_usuario.destroy()
    
    def usuario_existente(self, nombre_usuario):
        usuario_existente = False
        cant = 0
        try:
            cant = self.miCursor('SELECT COUNT(Nombre_usuario) FROM Usuarios WHERE Nombre_usuario = ?', (nombre_usuario))
            if cant == 1:
                usuario_existente = True
            return usuario_existente
        except:
            return usuario_existente
        
    def actualizar(self):
        self.miConexion=sqlite3.connect("./bd/consultorio.sqlite3")
        self.miCursor=self.miConexion.cursor()
        if(utl.validar_password(self.clave.get())):
            user = self.nombre_usuario.get()
            datos=self.nombre_usuario.get(), self.clave.get(), self.tipo_usuario.get(), user
        #print(datos)
            try:
                sql="UPDATE Usuarios SET Nombre_usuario =?, Clave=?, Tipo_usuario=? where Nombre_usuario=?"
                self.miCursor.execute(sql, datos)
                self.miConexion.commit()
                messagebox.showinfo("GUARDAR","Usuario actualizado exitosamente")
                self.frame_usuario.destroy()
            except:
                messagebox.showinfo("GUARDAR", "No se ha podido guardar el Usuario")
        else:
            messagebox.showwarning("CONTRASEÑA", "Contraseña inválida")
    
    def eliminar_usuario(self, nombre):
        msg_box = messagebox.askquestion('Eliminar usuario', '¿Desea elminar al usuario?', icon='warning')
        if msg_box == 'yes':
            self.miCursor.execute("DELETE FROM Usuarios WHERE Nombre_usuario = ?", (nombre,))
            self.miConexion.commit()
            messagebox.showinfo("ELIMINAR","Usuario eliminado exitosamente")
        
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

    def ventana(self):
        self.frame_usuario= tk.Toplevel()
        self.frame_usuario.grab_set_global() # Obliga a las ventanas estar deshabilitadas y deshabilitar todos los eventos e interacciones con la ventana
        self.frame_usuario.focus_set() # Mantiene el foco cuando se abre la ventana.
        self.imagen_ventana = utl.leer_imagen('tooth.jpg', (38, 38))
        self.frame_usuario.iconphoto(False, self.imagen_ventana)        
        self.frame_usuario.title('DentalMatic')
        self.frame_usuario.geometry('800x500')
        self.frame_usuario.config(bg='gray90')
        self.frame_usuario.resizable(width= 0, height= 0)
        utl.centrar_ventana(self.frame_usuario, 700, 400)
        self.menu = True
        self.color = True
        self.frame_top = Frame(self.frame_usuario, bg= '#1F704B', height= 50)

        self.frame_top.grid(column= 1, row= 0, sticky= 'nsew')
        self.frame_principal = Frame(self.frame_usuario)
        self.frame_principal.config(bg='gray90')
        self.frame_principal.grid(column= 1, row= 1, sticky= 'nsew')

        self.conexionBBDD()
        
        Button(self.frame_principal, text= 'Cerrar',  font= fuenteb, fg= 'white', bg= '#1F704B', activebackground= 'gray', bd= 2, width=20, command= self.Salir).grid(column= 2, row=6, pady= 5, padx= 5)

        #Entradas Y ETIQUETAS DATOS DEL USUARIO
        Entry(self.frame_principal, textvariable=self.nombre_usuario, width=25, font= fuenten).grid(column=1, row=1, pady=5, padx=10)
        Entry(self.frame_principal, textvariable=self.clave, width=25, font= fuenten).grid(column=1, row=2, pady=5, padx=10)        
        
        Label(self.frame_principal, text= 'Nombre del usuario', anchor="e", width=20, bg='gray90', fg= 'black', font= fuenteb).grid(column=0, row=1, pady=5)
        Label(self.frame_principal, text= 'Clave', anchor="e", width=20, bg='gray90', fg= 'black', font= fuenteb).grid(column=0, row=2, pady=5, padx=2)
        combo=ttk.Combobox(self.frame_principal, textvariable=self.tipo_usuario, width=23, font= fuenten, state="readonly", values=["administrador", "odontologo", "secretario"])
        combo.grid(column=1, row=3, pady=5, padx=10)

        Label(self.frame_principal, text= 'Tipo de usuario', anchor="e", width=20, bg='gray90', fg= 'black', font= fuenteb).grid(column=0, row=3, pady=5, padx=2)
        if(self.nombre_usuario.get()==''):
            self.titulo = Label(self.frame_top, text= 'Crear usuario', bg= '#1F704B', fg= 'white', font= fuenteb).grid(column= 0, row=0, pady= 20, padx= 10)
            Button(self.frame_principal, text= 'Guardar',  font= fuenteb, fg= 'white', bg= '#1F704B', activebackground= 'gray', bd= 2, width=20, command= self.guardar).grid(column= 0, row=6, pady= 5, padx= 5)
        else:
            self.titulo = Label(self.frame_top, text= 'Actualizar usuario', bg= '#1F704B', fg= 'white', font= fuenteb).grid(column= 0, row=0, pady= 20, padx= 10)
            Button(self.frame_principal, text= 'Actualizar',  font=fuenteb, fg= 'white', bg= '#1F704B', activebackground= 'gray', bd= 2, width=20, command= self.actualizar).grid(column= 0, row=6, pady= 5, padx= 5)
        Label(self.frame_principal, text= '* Campos obligatorios', anchor="w", width=20, bg='gray90', fg= 'red', font= fuenten).grid(column=2, row=4, pady=5, padx=2)
        Label(self.frame_principal, text= '*', anchor="w", width=20, bg='gray90', fg= 'red', font= fuenten).grid(column=2, row=1, pady=5, padx=2)
        Label(self.frame_principal, text= '*', anchor="w", width=20, bg='gray90', fg= 'red', font= fuenten).grid(column=2, row=2, pady=5, padx=2)
        Label(self.frame_principal, text= '*', anchor="w", width=20, bg='gray90', fg= 'red', font= fuenten).grid(column=2, row=3, pady=5, padx=2)
        Label(self.frame_principal, text= 'Contraseña: debe poseer un mínimo de 8 caracteres\n al menos una minuscula\n al menos una mayuscula\n al menos un digito', width=50, borderwidth=2, relief="solid", bg='gray90', fg= 'black', font= fuenten).grid( column=0, columnspan=3, row=5, pady=5)

        self.frame_usuario.mainloop()

if __name__ == "__main__":
    Usuario()