import tkinter as tk
import util.config as utl
from bd.conexion import Conexion
import re
from tkinter import messagebox, Button, Entry, Label, StringVar, Frame
#import sqlite3

class Odontologo:

    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwargs)
        self.master_panel_ref = kwargs.get('master_panel_ref', None)
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

    def ventana(self, master_panel_ref=None):
        if master_panel_ref:
            self.master_panel_ref = master_panel_ref
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
        utl.centrar_ventana(self.frame_odontologo, 550, 300)
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
        self.apellido_odontologo_valido = Label(self.frame_principal, text= '*', anchor= 'w', width= 15, bg= 'gray90', fg= 'red', font= self.fuenten)
        self.apellido_odontologo_valido.grid(column= 2, row= 1, pady= 5, padx= 2)

        Label(self.frame_principal, text= 'Nombre', anchor= "e", width= 15, bg= self.color_fondo2, fg= 'black', font= self.fuenteb).grid(column= 0, row= 2, pady= 5)
        self.entry_nombre = Entry(self.frame_principal, textvariable= self.nombre_odontologo, width= 25, font= self.fuenten)
        self.entry_nombre.grid(column= 1, row= 2, pady= 5, padx= 5)
        self.nombre_odontologo_valido = Label(self.frame_principal, text= '*', anchor= 'w', width= 15, bg= 'gray90', fg= 'red', font= self.fuenten)
        self.nombre_odontologo_valido.grid(column= 2, row= 2, pady= 5, padx= 2)

        Label(self.frame_principal, text= 'Matricula', anchor= "e", width= 15, bg= self.color_fondo2, fg= 'black', font= self.fuenteb).grid(column= 0, row= 3, pady= 5)
        self.entry_matricula = Entry(self.frame_principal, textvariable= self.matricula, width= 25, font= self.fuenten)
        self.entry_matricula.grid(column= 1, row= 3, pady= 5, padx= 5)
        self.matricula_valida = Label(self.frame_principal, text= '*', anchor= 'w', width= 15, bg= 'gray90', fg= 'red', font= self.fuenten)
        self.matricula_valida.grid(column= 2, row= 3, pady= 5, padx= 2)

        if(self.matricula.get()==''):
            self.titulo = Label(self.frame_top, text= 'Crear odontólogo', bg= self.color_fondo1, fg= 'white', font= self.fuenteb)
            self.titulo.grid(column= 0, row= 0, pady= 20, padx= 10)
            Button(self.frame_principal, text= 'Guardar', font= self.fuenteb, fg= 'white', bg= '#1F704B', activebackground= 'gray', bd= 2, width= 10, command= self.guardar).grid(column= 0, row= 5, pady= 5)
        else:
            self.titulo = Label(self.frame_top, text= 'Actualizar odontólogo', bg= self.color_fondo1, fg= 'white', font= self.fuenteb)
            self.titulo.grid(column= 0, row= 0, pady= 20, padx= 10)
            Button(self.frame_principal, text= 'Actualizar',  font= self.fuenteb, fg= 'white', bg= self.color_fondo1, activebackground= 'gray', bd= 2, width= 10, command= self.actualizar).grid(column= 0, row= 5, pady= 5)

        Label(self.frame_principal, text= '* Campos obligatorios', anchor= "w", width= 25, bg= 'gray90', fg= 'red', font= self.fuenten).grid(column= 1, row= 4, pady= 5, padx= 2)

        #Label(self.frame_principal, text= 'Contraseña: debe poseer un mínimo de 8 caracteres\n al menos una minuscula\n al menos una mayuscula\n al menos un digito', width= 50, borderwidth= 2, relief= "solid", bg= 'gray90', fg= 'black', font= self.fuenten).grid( column= 0, columnspan= 3, row= 5, pady= 5)
        Button(self.frame_principal, text= 'Cerrar',  font= self.fuenteb, bg= "orange", width= 10, command= self.Salir).grid(column= 2, row= 5, pady= 5, padx= (0, 10))
        self.frame_odontologo.protocol("WM_DELETE_WINDOW", self.Salir)

        self.frame_odontologo.mainloop()

    def guardar(self):
        apellido = False
        nombre = False
        matricula = False
        if not self.validar_alfa(self.apellido_odontologo.get()):
            self.apellido_odontologo_valido.config(fg= "red", text= "Sólo letras")
            self.entry_apellido.config(bg= "red")
            apellido = False
        else:
            self.apellido_odontologo_valido.config(fg= "green",text= "Válido")
            self.entry_apellido.config(bg= "green")
            apellido = True

        if not self.validar_alfa(self.nombre_odontologo.get()):
            self.nombre_odontologo_valido.config(fg= "red", text= "Sólo letras")
            self.entry_nombre.config(bg= "red")
            nombre = False
        else:
            self.nombre_odontologo_valido.config(fg= "green",text= "Válido")
            self.entry_nombre.config(bg= "green")
            nombre = True

        if not self.validar_matricula(self.matricula.get()):
            self.matricula_valida.config(fg= "red", text= "Sólo números")
            self.entry_matricula.config(bg= "red")
            matricula = False
        else:
            self.matricula_valida.config(fg= "green", text= "Válido")
            self.entry_matricula.config(bg= "green")
            matricula = True

        if apellido and nombre and matricula:            
            datos = self.matricula.get(), self.apellido_odontologo.get(), self.nombre_odontologo.get()
            #print(datos)
            try:
                self.miCursor.execute("INSERT INTO Odontologos VALUES(?,?,?)", (datos))
                self.miConexion.commit()
                if self.master_panel_ref:  # Si tenemos referencia al panel principal
                    self.master_panel_ref.mostrar_odontologos()
                self.frame_odontologo.destroy()                
                messagebox.showinfo("GUARDAR", "Guardado exitosamente")
            except:
                messagebox.showinfo("GUARDAR", "No se ha podido guardar el odontólogo")        

    def cargar_datos(self, matricula):
        try:
            datos= self.obtener_datos_odontologo(matricula)
        except:
            messagebox.showinfo("AVISO", "No se ha podido encontrar el odontólogo")
        try:
            self.miCursor.execute("SELECT * FROM Odontologos WHERE matricula=?", (matricula,))
            campos=self.miCursor.fetchone()        
            self.apellido_odontologo.set(campos[1])
            self.nombre_odontologo.set(campos[2])
        except:
            messagebox.showinfo("Odontólogo", "No se ha podido cargar el odontólogo")

    def obtener_datos_odontologo(self, matricula):
        try:
            self.miCursor.execute('SELECT Apellido_odontologo, Nombre_odontologo FROM Odontologos WHERE Matricula=?', (matricula,))
            datos_odontologo = self.miCursor.fetchone()            
        except:
            messagebox.showinfo("Aviso", "No se encontró el odontólogo")
        return datos_odontologo

    def actualizar(self):
        apellido_valido = False
        nombre_valido = False

        if not self.validar_alfa(self.apellido_odontologo.get()):
            self.apellido_odontologo_valido.config(fg="red", text="Sólo letras")
            self.entry_apellido.config(bg="red")
            apellido_valido = False
        else:
            self.apellido_odontologo_valido.config(fg="green", text="Válido")
            self.entry_apellido.config(bg="green")
            apellido_valido = True

        if not self.validar_alfa(self.nombre_odontologo.get()):
            self.nombre_odontologo_valido.config(fg="red", text="Sólo letras")
            self.entry_nombre.config(bg="red")
            nombre_valido = False
        else:
            self.nombre_odontologo_valido.config(fg="green", text="Válido")
            self.entry_nombre.config(bg="green")
            nombre_valido = True

        if apellido_valido and nombre_valido:
            try:
                sql = "UPDATE Odontologos SET Apellido_odontologo = ?, Nombre_odontologo = ? WHERE Matricula = ?"
                datos = (self.apellido_odontologo.get(), self.nombre_odontologo.get(), self.matricula.get())
                self.miCursor.execute(sql, datos)
                self.miConexion.commit()
                if self.master_panel_ref:
                    self.master_panel_ref.mostrar_odontologos()
                messagebox.showinfo("ACTUALIZAR", "Odontólogo actualizado exitosamente")
                self.frame_odontologo.destroy()
            except:
                messagebox.showinfo("ERROR", "No se pudo actualizar el odontólogo")

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

    def validar_alfa(self, cadena):
        patron = r'^[a-zA-ZáéíóúÁÉÍÓÚ\s]+$'  # Permite caracteres
        return bool(re.match(patron, cadena))

    # def validar_apellido(self, cadena):
    #     patron = r'^[a-zA-Z]*$'  # Permite caracteres
    #     return bool(re.match(patron, cadena))

    def validar_matricula(self, cadena):
        return bool(re.fullmatch(r'\d+', cadena))

if __name__ == "__main__":
    Odontologo()