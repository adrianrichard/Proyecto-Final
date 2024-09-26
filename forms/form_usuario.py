import tkinter as tk
from tkinter import ttk
from tkinter.font import BOLD
import util.generic as utl
from bd.conexion import Conexion

from tkinter import messagebox, Button, Entry, Label, StringVar, Frame
#from bd.conexion import Conexion
import sqlite3

import re
class Usuario:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombre_usuario = StringVar()
        self.nombre_usuario_anterior = StringVar()
        self.clave = StringVar()
        self.tipo_usuario =  StringVar()
        self.id_usuario =  StringVar()
        self.usuario_existente = False
        self.fuenteb= utl.definir_fuente_bold()
        self.fuenten= utl.definir_fuente()
        self.db = Conexion()
        self.miConexion=self.db.conectar()
        self.miCursor=self.miConexion.cursor()

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

        Button(self.frame_principal, text= 'Cerrar',  font= self.fuenteb, fg= 'white', bg= '#1F704B', activebackground= 'gray', bd= 2, width=20, command= self.Salir).grid(column= 2, row=6, pady= 5, padx= 5)

        #Entradas Y ETIQUETAS DATOS DEL USUARIO
        #Entry(self.frame_principal, textvariable=self.nombre_usuario, width=25, font= fuenten).grid(column=1, row=1, pady=5, padx=10)
        Entry(self.frame_principal, textvariable=self.nombre_usuario, width=25, font= self.fuenten, validate="key", validatecommand=(self.frame_principal.register(self.validar_nombre), "%S"), invalidcommand=(self.frame_principal.register(self.on_invalid), )).grid(column=1, row=1, pady=5, padx=10)
        Entry(self.frame_principal, textvariable=self.clave, width=25, font= self.fuenten).grid(column=1, row=2, pady=5, padx=10)        
        
        Label(self.frame_principal, text= 'Nombre del usuario', anchor="e", width=20, bg='gray90', fg= 'black', font= self.fuenteb).grid(column=0, row=1, pady=5)
        Label(self.frame_principal, text= 'Clave', anchor="e", width=20, bg='gray90', fg= 'black', font= self.fuenteb).grid(column=0, row=2, pady=5, padx=2)

        Label(self.frame_principal, text= 'Tipo de usuario', anchor="e", width=20, bg='gray90', fg= 'black', font= self.fuenteb).grid(column=0, row=3, pady=5, padx=2)
        if(self.nombre_usuario.get()==''):
            self.titulo = Label(self.frame_top, text= 'Crear usuario', bg= '#1F704B', fg= 'white', font= self.fuenteb).grid(column= 0, row=0, pady= 20, padx= 10)
            Button(self.frame_principal, text= 'Guardar',  font= self.fuenteb, fg= 'white', bg= '#1F704B', activebackground= 'gray', bd= 2, width=20, command= self.guardar).grid(column= 0, row=6, pady= 5, padx= 5)
            combo=ttk.Combobox(self.frame_principal, textvariable=self.tipo_usuario, width=23, font= self.fuenten, state="readonly", values=["administrador", "odontologo", "secretario"])
            combo.grid(column=1, row=3, pady=5, padx=10)
            combo.current(2)
            Label(self.frame_principal, text= '*', anchor="w", width=20, bg='gray90', fg= 'red', font= self.fuenten).grid(column=2, row=3, pady=5, padx=2)
        else:
            self.titulo = Label(self.frame_top, text= 'Actualizar usuario', bg= '#1F704B', fg= 'white', font= self.fuenteb).grid(column= 0, row=0, pady= 20, padx= 10)
            Button(self.frame_principal, text= 'Actualizar',  font=self.fuenteb, fg= 'white', bg= '#1F704B', activebackground= 'gray', bd= 2, width=20, command= self.actualizar).grid(column= 0, row=6, pady= 5, padx= 5)
            combo=ttk.Combobox(self.frame_principal, textvariable=self.tipo_usuario, width=23, font= self.fuenten, state="disabled", values=["administrador", "odontologo", "secretario"])
            combo.grid(column=1, row=3, pady=5, padx=10)
        Label(self.frame_principal, text= '* Campos obligatorios', anchor="w", width=20, bg='gray90', fg= 'red', font= self.fuenten).grid(column=2, row=4, pady=5, padx=2)
        Label(self.frame_principal, text= '*', anchor="w", width=20, bg='gray90', fg= 'red', font= self.fuenten).grid(column=2, row=1, pady=5, padx=2)
        Label(self.frame_principal, text= '*', anchor="w", width=20, bg='gray90', fg= 'red', font= self.fuenten).grid(column=2, row=2, pady=5, padx=2)
        Label(self.frame_principal, text= 'Contraseña: debe poseer un mínimo de 8 caracteres\n al menos una minuscula\n al menos una mayuscula\n al menos un digito', width=50, borderwidth=2, relief="solid", bg='gray90', fg= 'black', font= self.fuenten).grid( column=0, columnspan=3, row=5, pady=5)
        self.frame_usuario.protocol("WM_DELETE_WINDOW", self.Salir)

        self.frame_usuario.mainloop()
    
    def guardar(self):
        if(self.validar_usuario(self.nombre_usuario.get())):
            messagebox.showinfo("Usuario existente", "Ya existe este usuario")
        else:
            if(self.validar_contrasenia(self.clave.get()) and self.nombre_usuario.get()!=''):
                datos=self.nombre_usuario.get(), self.clave.get(), self.tipo_usuario.get()
                try:
                    self.miCursor.execute("INSERT INTO Usuarios VALUES(NULL,?,?,?)", (datos))
                    self.miConexion.commit()
                    self.frame_usuario.destroy()
                except:
                    messagebox.showinfo("GUARDAR", "No se ha podido guardar el usuario")
            else:
                messagebox.showwarning("Nombre usuario", "Completar campos")                

    def cargar_datos(self, usuario):
        self.nombre_usuario.set(usuario)
        self.nombre_usuario_anterior=usuario
        try:
            self.miCursor.execute("SELECT * FROM Usuarios WHERE Nombre_usuario=?", (usuario,))
            campos=self.miCursor.fetchall()        
            self.clave.set(campos[0][2])
            self.tipo_usuario.set(campos[0][3])
        except:
            messagebox.showinfo("Buscar usuario", "No se ha podido cargar el usuario")            

    def validar_usuario(self, nombre_usuario):
       
        try:
            self.miCursor.execute('SELECT COUNT(Nombre_usuario) FROM Usuarios WHERE Nombre_usuario=?', (nombre_usuario,))
            existe = self.miCursor.fetchone()[0]
            self.usuario_existente = bool(existe)
            
        except:
            messagebox.showinfo("Usuario existente", "USUARIO EXISTENTE")

        return self.usuario_existente

    def actualizar(self):
        datos=self.nombre_usuario.get(), self.clave.get(), self.nombre_usuario_anterior
        if self.validar_contrasenia(self.clave.get()):
            
            if self.validar_usuario(self.nombre_usuario.get()):
                messagebox.showinfo("Usuario existente", "USUARIO EXISTENTE")
                pass
            else:                
                try:
                    sql="UPDATE Usuarios SET Nombre_usuario =?, Clave=? where Nombre_usuario=?"
                    self.miCursor.execute(sql, datos)
                    self.miConexion.commit()
                    messagebox.showinfo("GUARDAR","Usuario actualizado exitosamente")
                    self.frame_usuario.destroy()
                except:
                    messagebox.showinfo("GUARDAR", "No se ha podido guardar el usuario")
        else:
            pass

    def eliminar_usuario(self, nombre):

        msg_box = messagebox.askquestion('Eliminar usuario', '¿Desea elminar al usuario?', icon='warning')
        if msg_box == 'yes':
            try:
                self.miCursor.execute("DELETE FROM Usuarios WHERE Nombre_usuario = ?", (nombre,))
                self.miConexion.commit()
                messagebox.showinfo("ELIMINAR","Usuario eliminado exitosamente")
            except:
                messagebox.showinfo("ELIMINAR", "No se ha podido eliminar el usuario")

    def Salir(self):
        answer = messagebox.askokcancel(title='Salir', message='¿Desea salir sin guardar?', icon='warning')
        if answer:
            self.miConexion.close()
            self.frame_usuario.destroy()
    
    def on_invalid(self):
        messagebox.showinfo("NOMBRE USUARIO","Sólo letras o _ (Guión bajo)\nNo puede comenzar con _ (Guión bajo)")

    def validar_nombre(self, value):
        pattern = r'\b[A-Za-z_]\b'
        if re.fullmatch(pattern, value) is None:
            return False 
        return True

    def validar_contrasenia(self, password):
        largo = re.compile(r'.{8,}')
        digito = re.compile(r'\d+')
        letra_may = re.compile(r'[A-Z]+')
        letra_min = re.compile(r'[a-z]+')
        self.longitud=False
        self.numero=False
        self.mayuscula=False
        self.minuscula=False
        self.valido=False
        a="Debe contener al menos 8 caracteres"
        if(largo.search(password)):
            a=""
            self.longitud=True
        b="\nAgregar un digito"
        if(digito.search(password)):
            b=""
            self.numero=True
        c="\nAgregar una mayúscula"
        if(letra_may.search(password)):
            c=""
            self.mayuscula=True
        d="\nAgregar una minúscula"
        if(letra_min.search(password)):
            d=""
            self.minuscula=True
        if(self.longitud and self.numero and self.mayuscula and self.minuscula):
            self.valido = True

        cadena=a+b+c+d
        if(cadena != ""):
            messagebox.showwarning("CONTRASEÑA INVÁLIDA", cadena)

        return self.valido

if __name__ == "__main__":
    Usuario()