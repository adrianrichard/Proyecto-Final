import tkinter as tk
import util.config as utl
from bd.conexion import Conexion
import re
from tkinter import messagebox, Button, Entry, Label, StringVar, Frame
#import sqlite3

class Odontologo:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombre_odontologo = StringVar()
        self.apellido_odontologo =  StringVar() 
        self.matricula = StringVar()
        #self.nombre_odontologo_anterior = StringVar()
        self.fuenteb= utl.definir_fuente_bold()
        self.fuenten= utl.definir_fuente()
        self.color_fuente1, self.color_fuente2 = utl.definir_color_fuente()
        self.color_fondo1, self.color_fondo2 = utl.definir_color_fondo()
        self.db = Conexion()
        self.miConexion=self.db.conectar()
        self.miCursor=self.miConexion.cursor()

    def ventana(self):
        self.frame_odontologo= tk.Toplevel()
        self.frame_odontologo.grab_set_global() # Obliga a las ventanas estar deshabilitadas y deshabilitar todos los eventos e interacciones con la ventana
        self.frame_odontologo.focus_set() # Mantiene el foco cuando se abre la ventana.
        self.imagen_ventana = utl.leer_imagen('tooth.jpg', (38, 38))
        self.frame_odontologo.iconphoto(False, self.imagen_ventana)        
        self.frame_odontologo.title('DentalMatic')
        self.frame_odontologo.geometry('700x500')
        self.frame_odontologo.config(bg= self.color_fondo2)
        self.frame_odontologo.resizable(width= 0, height= 0)
        self.frame_odontologo.columnconfigure(0, weight= 1)
        utl.centrar_ventana(self.frame_odontologo, 510, 400)
        self.menu = True
        self.color = True
        self.frame_top = Frame(self.frame_odontologo, bg= self.color_fondo1)
        self.frame_top.grid(column= 1, row= 0, sticky= "nsew")
        self.frame_principal = Frame(self.frame_odontologo)
        self.frame_principal.config(bg= self.color_fondo2)
        self.frame_principal.grid(column= 1, row= 1, sticky= 'nsew')

        #Entradas Y ETIQUETAS DATOS DEL ODONTOLOGO
        Label(self.frame_principal, text= 'Apellido', anchor= "e", width= 15, bg= 'gray90', fg= 'black', font= self.fuenteb).grid(column= 0, row= 1, pady= 5)
        self.entry_apellido = Entry(self.frame_principal, textvariable= self.apellido_odontologo, width= 25, font= self.fuenten)
        self.entry_apellido.grid(column= 1, row= 1, pady= 5, padx= 5)
        #self.nombre_usuario_valido = Label(self.frame_principal, text= '*', anchor= 'w', width= 25, bg= 'gray90', fg= 'red', font= self.fuenten)
        #self.nombre_usuario_valido.grid(column= 2, row= 1, pady= 5, padx= 2)

        Label(self.frame_principal, text= 'Nombre', anchor= "e", width= 15, bg= self.color_fondo2, fg= 'black', font= self.fuenteb).grid(column= 0, row= 2, pady= 5)
        self.entry_nombre = Entry(self.frame_principal, textvariable= self.nombre_odontologo, width= 25, font= self.fuenten)
        self.entry_nombre.grid(column= 1, row= 2, pady= 5, padx= 5)
        #Label(self.frame_principal, text= '*', anchor= "w", width= 25, bg= 'gray90', fg= 'red', font= self.fuenten).grid(column= 2, row= 2, pady= 5, padx= 2)

        Label(self.frame_principal, text= 'Matricula', anchor= "e", width= 15, bg= self.color_fondo2, fg= 'black', font= self.fuenteb).grid(column= 0, row= 3, pady= 5)
        self.entry_matricula = Entry(self.frame_principal, textvariable= self.nombre_odontologo, width= 25, font= self.fuenten)
        self.entry_matricula.grid(column= 1, row= 3, pady= 5, padx= 5)
        if(self.matricula.get()==''):
            self.titulo = Label(self.frame_top, text= 'Crear odontólogo', bg= self.color_fondo1, fg= 'white', font= self.fuenteb)
            self.titulo.grid(column= 0, row= 0, pady= 20, padx= 10)
            Button(self.frame_principal, text= 'Guardar', font= self.fuenteb, fg= 'white', bg= '#1F704B', activebackground= 'gray', bd= 2, width= 10, command= self.guardar).grid(column= 0, row= 5, pady= 5)
            #Label(self.frame_principal, text= '*', anchor= "w", width= 25, bg= 'gray90', fg= 'red', font= self.fuenten).grid(column= 2, row= 3, pady= 5, padx= 2)
        else:
            self.titulo = Label(self.frame_top, text= 'Actualizar odontólogo', bg= self.color_fondo1, fg= 'white', font= self.fuenteb)
            self.titulo.grid(column= 0, row= 0, pady= 20, padx= 10)
            Button(self.frame_principal, text= 'Actualizar',  font= self.fuenteb, fg= 'white', bg= self.color_fondo1, activebackground= 'gray', bd= 2, width= 10, command= self.actualizar).grid(column= 0, row= 5, pady= 5)
            
        #Label(self.frame_principal, text= '* Campos obligatorios', anchor= "w", width= 20, bg= 'gray90', fg= 'red', font= self.fuenten).grid(column= 1, row= 4, pady= 5, padx= 2)

        #Label(self.frame_principal, text= 'Contraseña: debe poseer un mínimo de 8 caracteres\n al menos una minuscula\n al menos una mayuscula\n al menos un digito', width= 50, borderwidth= 2, relief= "solid", bg= 'gray90', fg= 'black', font= self.fuenten).grid( column= 0, columnspan= 3, row= 5, pady= 5)
        Button(self.frame_principal, text= 'Cerrar',  font= self.fuenteb, bg= "orange", width= 10, command= self.Salir).grid(column= 2, row= 5, pady= 5, padx= (0, 10))
        self.frame_odontologo.protocol("WM_DELETE_WINDOW", self.Salir)

        self.frame_odontologo.mainloop()

    def guardar(self):
        if not self.validar_nombre(self.nombre_odontologo.get()):
            messagebox.showinfo("Usuario inválido", "Sólo letras o _ (Guión bajo)\nNo puede comenzar con _ (Guión bajo)")            
            self.entry_nombre.config(bg= "orange red")
        elif self.validar_usuario(self.nombre_odontologo.get()):
            self.nombre_usuario_valido.config(text= "* Ya existe este usuario", fg= 'red')
            self.entry_nombre.config(bg= "orange red")
        else:
            if(self.validar_contrasenia(self.clave.get()) and self.nombre_usuario.get()!=''):
                datos=self.nombre_usuario.get(), self.clave.get(), self.tipo_usuario.get()
                try:
                    self.miCursor.execute("INSERT INTO Usuarios VALUES(NULL,?,?,?)", (datos))
                    self.miConexion.commit()
                    self.frame_odontologo.destroy()
                except:
                    messagebox.showinfo("GUARDAR", "No se ha podido guardar el usuario")
            else:
                messagebox.showwarning("Nombre usuario", "Completar campos")

    def cargar_datos(self, usuario):
        self.nombre_usuario.set(usuario)
        self.nombre_usuario_anterior=usuario
        try:
            self.miCursor.execute("SELECT * FROM usuarios WHERE nombre_usuario=?", (usuario,))
            campos=self.miCursor.fetchall()        
            self.clave.set(campos[0][2])
            self.tipo_usuario.set(campos[0][3])
        except:
            messagebox.showinfo("Buscar usuario", "No se ha podido cargar el usuario")

    def obtener_datos_odontologo(self, matricula):
        try:
            self.miCursor.execute('SELECT Apellido_odontologo, Nombre_odontologo FROM Odontologos WHERE Matricula=?', (matricula,))
            datos_odontologo = self.miCursor.fetchone()            
        except:
            messagebox.showinfo("Aviso", "No se encontró el odontólogo")
        return datos_odontologo

    def actualizar(self):
        datos= self.clave.get(), self.nombre_usuario_anterior
        usuario_valido=False

        if not self.validar_nombre(self.nombre_usuario.get()):
            messagebox.showinfo("Usuario inválido", "Sólo letras o _ (Guión bajo)\nNo puede comenzar con _ (Guión bajo)")
            self.entry_nombre.config(bg= "orange red")
        elif self.validar_nombre(self.nombre_usuario.get()):
            self.entry_nombre.config(bg= "pale green")
            usuario_valido = True
        if self.validar_contrasenia(self.clave.get()) and usuario_valido:

            if self.nombre_usuario.get() == self.nombre_usuario_anterior:
                try:
                    sql="UPDATE usuarios SET pass_usuario=? where nombre_usuario=?"
                    self.miCursor.execute(sql, datos)
                    self.miConexion.commit()
                    messagebox.showinfo("GUARDAR","Usuario actualizado exitosamente")
                    self.frame_odontologo.destroy()
                except:
                    messagebox.showinfo("GUARDAR", "No se ha podido guardar el usuario")
            elif self.validar_usuario(self.nombre_usuario.get()):
                self.nombre_usuario_valido.config(text= "* Ya existe este usuario", fg= 'red')
                self.entry_nombre.config(bg= "orange red")
                pass
            else:
                datos=self.nombre_usuario.get(), self.clave.get(), self.nombre_usuario_anterior
                try:
                    sql="UPDATE usuarios SET nombre_usuario =?, pass_usuario=? where nombre_usuario=?"
                    self.miCursor.execute(sql, datos)
                    self.miConexion.commit()
                    messagebox.showinfo("GUARDAR","Usuario actualizado exitosamente")
                    self.frame_odontologo.destroy()
                except:
                    messagebox.showinfo("GUARDAR", "No se ha podido guardar el usuario")
        else:
            pass

    def eliminar_odontologo(self, matricula):
        try:
            datos= self.obtener_datos_odontologo(matricula)
        except:
            messagebox.showinfo("AVISO", "No se ha podido encontrar el odontólogo")

        msg_box = messagebox.askquestion('Eliminar odontólogo', f'¿Desea eliminar a {datos[0]}, {datos[1]}?', icon='warning')
        if msg_box == 'yes'and matricula != 'admin':
            try:
                self.miCursor.execute("DELETE FROM odontologos WHERE matricula = ?", (matricula,))
                self.miConexion.commit()
                messagebox.showinfo("ELIMINAR","Odontólogo eliminado exitosamente")
            except:
                messagebox.showinfo("ELIMINAR", "No se ha podido eliminar el odontólogo")

    def Salir(self):
        answer = messagebox.askokcancel(title='Salir', message='¿Desea salir sin guardar?', icon='warning')
        if answer:
            self.miConexion.close()
            self.frame_odontologo.destroy()

    def on_invalid(self):
        messagebox.showinfo("NOMBRE USUARIO","Sólo letras o _ (Guión bajo)\nNo puede comenzar con _ (Guión bajo)")

    def validar_nombre(self, cadena):
        patron = r'^[a-zA-Z]*$'  # Permite 1+ caracteres, números y _
        return bool(re.match(patron, cadena))

        """
        def validar_con_feedback():
            if not entry.get().isdigit():
                tk.messagebox.showerror("Error", "Solo se permiten números")
                entry.delete(0, tk.END)

        entry = ttk.Entry(root)
        entry.bind('<FocusOut>', lambda e: validar_con_feedback())
        """



if __name__ == "__main__":
    Odontologo()