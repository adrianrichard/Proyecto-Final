from tkinter import *
import tkinter as tk
from tkinter.font import BOLD
import util.config as utl
from tkinter import messagebox, Button, Entry, Label
from tkinter import  StringVar, Frame
import re
from bd.conexion import Conexion
#from bd.conexion import Conexion
import sqlite3
fuenteb= utl.definir_fuente_bold()
fuenten= utl.definir_fuente()
ancho=15

class Paciente:
   
    def validar_email(self, email):
        email = self.entry_correo.get()
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            self.entry_correo.config(bg= "pale green")
            self.email_valido_label.config(text= "Formato válido", fg='green')
            self.correovalido = True
        else:
            self.entry_correo.config( bg="orange red")
            self.email_valido_label.config(text= "Formato inválido", fg='red')
            self.correovalido = False

    def validar_DNI(self, text, new_text):
        if len(new_text) > 8:
            return False
        return text.isdecimal()
    
    def validar_alfa(self, value):
        return value.isalpha()
    
    def validar_alfanum(sel, value):
        return value.isalnum() or value.isspace()
    
    def validar_telefono(self, text, new_text):
        if len(new_text) > 11:
            return False
        return text.isdecimal()
    
    def validar_numero(self, event):
        texto = self.entry_nombre.get()
        if not re.match(r'^[a-zA-Z]$', texto):  # Si es un número
            messagebox.showerror("Error", "Solo se permiten letras.")
            self.entry_nombre.delete(len(texto) - 1)
        
    def cargar_datos(self, dni):
        self.dni_paciente_anterior=dni
        try:
            self.miCursor.execute("SELECT * FROM Pacientes WHERE ID=?", (dni,))
            campos=self.miCursor.fetchall()
            
            self.nombre_paciente.set(campos[0][1])
            self.apellido_paciente.set(campos[0][2])
            self.dni_paciente.set(dni)
            self.domicilio_paciente.set(campos[0][3])
            self.telefono_paciente.set(campos[0][4])
            self.email_paciente.set(campos[0][5])
            self.obrasocial_paciente.set(campos[0][6])
            self.nrosocio_paciente.set(campos[0][7])
        except:
            messagebox.showinfo("Buscar paciente", "No se ha podido encontrar el paciente")

    def actualizar(self):        
        datos=self.nombre_paciente.get().upper(), self.apellido_paciente.get().upper(), self.dni_paciente.get(), self.domicilio_paciente.get().upper(),self.telefono_paciente.get(),self.email_paciente.get(),self.obrasocial_paciente.get().upper(),self.nrosocio_paciente.get(), self.dni_paciente_anterior
        try:
            sql="UPDATE Pacientes SET nombre =?, apellido=?, ID=?, domicilio=?, telefono=?, email=?, obrasocial=?, nrosocio=? where ID=?"
            self.miCursor.execute(sql, datos)
            self.miConexion.commit()
            messagebox.showinfo("GUARDAR","Paciente actualizado exitosamente")
            self.frame_paciente.destroy()
        except:
            messagebox.showinfo("GUARDAR", "No se ha podido actualizar el paciente")
            
    def guardar(self):
        guardar=False
        if(self.nombre_paciente.get()==''):
            messagebox.showinfo("GUARDAR", "Complete el campo Nombre")
        elif(self.apellido_paciente.get()==''):
            messagebox.showinfo("GUARDAR", "Complete el campo Apellido")
        elif(self.dni_paciente.get()==''):
            messagebox.showinfo("GUARDAR", "Complete el campo DNI")
        elif(self.domicilio_paciente.get()==''):
            messagebox.showinfo("GUARDAR", "Complete el campo Domicilio")
        elif(self.telefono_paciente.get()==''):
            messagebox.showinfo("GUARDAR", "Complete el campo Teléfono")
        elif(not self.correovalido):
            messagebox.showinfo("GUARDAR", "Formato de email incorrecto")
        else:
            guardar=True
        if(guardar):    
            datos=self.nombre_paciente.get().upper(), self.apellido_paciente.get().upper(), self.dni_paciente.get(), self.domicilio_paciente.get().upper(),self.telefono_paciente.get(),self.email_paciente.get(),self.obrasocial_paciente.get().upper(),self.nrosocio_paciente.get()
            try:
                self.miCursor.execute("INSERT INTO Pacientes VALUES(NULL,?,?,?,?,?,?,?,?)", (datos))
                self.miConexion.commit()
                messagebox.showinfo("GUARDAR","Paciente guardado exitosamente")
                self.frame_paciente.destroy()
            except:
                messagebox.showinfo("GUARDAR", "No se ha podido guardar el paciente")

    def Salir(self):
        answer = messagebox.askokcancel(title='Salir', message='¿Desea salir sin guardar?', icon='warning')
        if answer:
            self.frame_paciente.destroy()
    
    def ventana_paciente(self):
        self.frame_paciente= tk.Toplevel()
        self.frame_paciente.grab_set_global() # Obliga a las ventanas estar deshabilitadas y deshabilitar todos los eventos e interacciones con la ventana
        self.frame_paciente.focus_set() # Mantiene el foco cuando se abre la ventana.
        self.imagen_ventana = utl.leer_imagen('tooth.jpg', (38, 38))
        self.frame_paciente.iconphoto(False, self.imagen_ventana)  
        self.frame_paciente.title('DentalMatic')
        self.frame_paciente.geometry('800x300')
        self.frame_paciente.config(bg='gray90')
        self.frame_paciente.resizable(width= 0, height= 0)
        utl.centrar_ventana(self.frame_paciente, 625, 500)
        self.menu = True
        self.color = True
        self.frame_top = Frame(self.frame_paciente, bg= '#1F704B', height= 50)

        self.frame_top.grid(column= 1, row= 0, sticky= 'nsew')
        self.frame_principal = Frame(self.frame_paciente)
        self.frame_principal.config(bg='gray90')
        self.frame_principal.grid(column= 1, row= 1, sticky= 'nsew')
        self.titulo = Label(self.frame_top, text= 'Datos del paciente', bg= '#1F704B', fg= 'white', font= fuenteb).grid(column= 0, row=0, pady= 20, padx= 10)
        Button(self.frame_principal, text= 'Cerrar',  font= fuenteb, fg= 'white', bg= '#1F704B', activebackground= 'gray', width=15, bd= 2, command= self.Salir).grid(column= 2, row=10, pady= 5)

        #Entradas Y ETIQUETAS DATOS DEL PACIENTE
        self.entry_nombre = Entry(self.frame_principal, textvariable=self.nombre_paciente, width=25, font= fuenten, validate="key", validatecommand=(self.frame_principal.register(self.validar_numero), "%S"))
        self.entry_nombre.grid(column=1, row=1, pady=5)
        self.entry_nombre.bind("<KeyRelease>", self.validar_numero)
        Entry(self.frame_principal, textvariable=self.apellido_paciente, width=25, font= fuenten, validate="key", validatecommand=(self.frame_principal.register(self.validar_alfa), "%S")).grid(column=1, row=2, pady=5)
        Entry(self.frame_principal, textvariable=self.dni_paciente, width=25, font= fuenten, validate="key", validatecommand=(self.frame_principal.register(self.validar_DNI), "%S", "%P")).grid(column=1, row=3, pady=5)
        Entry(self.frame_principal, textvariable=self.domicilio_paciente, width=25, font= fuenten, validate="key", validatecommand=(self.frame_principal.register(self.validar_alfanum), "%S")).grid(column=1, row=4, pady=5)
        Entry(self.frame_principal, textvariable=self.telefono_paciente, width=25, font= fuenten, validate="key", validatecommand=(self.frame_principal.register(self.validar_telefono), "%S", "%P")).grid(column=1, row=5, pady=5)
        self.entry_correo =Entry(self.frame_principal, textvariable=self.email_paciente, width=25, font= fuenten)
        self.entry_correo.grid(column=1, row=6, pady=5)
        validate_email = self.frame_principal.register(lambda email: self.validar_email(self.entry_correo))
        self.entry_correo.config(validate="key", validatecommand=(validate_email, '%P'))
        def actualizar_label(event):
            self.validar_email(self.entry_correo)
        self.entry_correo.bind('<Key>', actualizar_label)
        Entry(self.frame_principal, textvariable=self.obrasocial_paciente, width=25, font= fuenten, validate="key", validatecommand=(self.frame_principal.register(self.validar_alfa), "%S")).grid(column=1, row=7, pady=5)
        Entry(self.frame_principal, textvariable=self.nrosocio_paciente, width=25, font= fuenten, validate="key", validatecommand=(self.frame_principal.register(self.validar_telefono), "%S", "%P")).grid(column=1, row=8, pady=5)

        Label(self.frame_principal, text= 'Nombre/s', bg='gray90', fg= 'black', anchor="e", width=ancho, font= fuenteb).grid(column=0, row=1, pady=5, padx=2)
        Label(self.frame_principal, text= 'Apellido/s', bg='gray90', fg= 'black', anchor="e", width=ancho, font= fuenteb).grid(column=0, row=2, pady=5, padx=2)
        Label(self.frame_principal, text= 'D.N.I.', bg='gray90', fg= 'black', anchor="e", width=ancho, font= fuenteb).grid(column=0, row=3, pady=5, padx=2)
        Label(self.frame_principal, text= 'Domicilio', bg='gray90', fg= 'black', anchor="e", width=ancho, font= fuenteb).grid(column=0, row=4, pady=5, padx=2)
        Label(self.frame_principal, text= 'Telefono', bg='gray90', fg= 'black', anchor="e", width=ancho, font= fuenteb).grid(column=0, row=5, pady=5, padx=2)
        Label(self.frame_principal, text= 'Email', bg='gray90', fg= 'black', anchor="e", width=ancho, font= fuenteb).grid(column=0, row=6, pady=5, padx=2)
        Label(self.frame_principal, text= 'Obra Social', bg='gray90', fg= 'black', anchor="e", width=ancho, font= fuenteb).grid(column=0, row=7, pady=5, padx=2)
        Label(self.frame_principal, text= 'Nro de socio', bg='gray90', fg= 'black', anchor="e", width=ancho, font= fuenteb).grid(column=0, row=8, pady=5, padx=2)
        if(self.dni_paciente.get()==''):
            Button(self.frame_principal, text= 'Guardar',  font= fuenteb, fg= 'white', bg= '#1F704B', activebackground= 'gray', width=15, bd= 2, command= self.guardar).grid(column= 0, row=10, pady= 5, padx= 20)
        else:
            self.titulo = Label(self.frame_top, text= 'Actualizar paciente', bg= '#1F704B', fg= 'white', font= fuenteb).grid(column= 0, row=0, pady= 20, padx= 10)
            Button(self.frame_principal, text= 'Actualizar',  font= fuenteb, fg= 'white', bg= '#1F704B', width=15, activebackground= 'gray', bd= 2, command= self.actualizar).grid(column= 0, row=10, pady= 5, padx= 20)
        Label(self.frame_principal, text= '*', anchor="w", width=20, bg='gray90', fg= 'red', font= fuenten).grid(column=2, row=1, pady=5)
        Label(self.frame_principal, text= '*', anchor="w", width=20, bg='gray90', fg= 'red', font= fuenten).grid(column=2, row=2, pady=5)
        Label(self.frame_principal, text= '*', anchor="w", width=20, bg='gray90', fg= 'red', font= fuenten).grid(column=2, row=3, pady=5)
        Label(self.frame_principal, text= '*', anchor="w", width=20, bg='gray90', fg= 'red', font= fuenten).grid(column=2, row=4, pady=5)
        Label(self.frame_principal, text= '*', anchor="w", width=20, bg='gray90', fg= 'red', font= fuenten).grid(column=2, row=5, pady=5)
        self.email_valido_label=Label(self.frame_principal, text= '', anchor="w", width=20, bg='gray90', fg= 'red', font= fuenten)
        self.email_valido_label.grid(column=2, row=6, pady=5)
        Label(self.frame_principal, text= '* Campos obligatorios', anchor="e", width=20, bg='gray90', fg= 'red', font= fuenten).grid(column=2, row=9, pady=5, padx=2)

        self.frame_paciente.mainloop()
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.nombre_paciente = StringVar()
        self.apellido_paciente = StringVar()
        self.dni_paciente_anterior =  StringVar()
        self.dni_paciente =  StringVar()
        self.domicilio_paciente =  StringVar()
        self.telefono_paciente =  StringVar()
        self.email_paciente =  StringVar()
        self.obrasocial_paciente =  StringVar()
        self.nrosocio_paciente =  StringVar()
        self.correovalido=False
        self.db = Conexion()
        self.miConexion=self.db.conectar()
        self.miCursor=self.miConexion.cursor()
        #self.conexionBBDD()

if __name__ == "__main__":
    Paciente()