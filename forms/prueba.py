import tkinter as tk
from tkinter import *
from tkinter.font import BOLD
from tkinter import  ttk, Button, Label, Frame

class Paciente:    
        
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

        self.titulo = Label(self.frame_top, text= 'Paciente', bg= '#1F704B', fg= 'white', font= ('Comic Sans MS', 15, 'bold')).grid(column= 1, row=0, pady= 20, padx= 10)
        Button(self.frame_top, text= 'Cerrar',  font= ('Comic Sans MS', 15, BOLD), fg= 'white', bg= '#1F704B', activebackground= 'gray', bd= 0, command= self.frame_paciente.destroy).grid(column= 2, row=0, pady= 20, padx= 500)
        nombre_paciente = StringVar()
        apellido_paciente = StringVar()
        dni_paciente =  StringVar()
        domicilio_paciente =  StringVar()
        telefono_paciente =  StringVar()
        email_paciente =  StringVar()
        obrasocial_paciente =  StringVar()
        nrosocio_paciente =  StringVar()
        #Entradas Y ETIQUETAS DATOS DEL PACIENTE
        Entry(self.frame_principal,  textvariable=nombre_paciente, font= ('Comic Sans MS', 14)).grid(column=1, row=1, pady=5, padx=10)
        Entry(self.frame_principal, textvariable=apellido_paciente, font= ('Comic Sans MS', 14)).grid(column=1, row=2, pady=5, padx=10)
        Entry(self.frame_principal, textvariable=dni_paciente, font= ('Comic Sans MS', 14)).grid(column=1, row=3, pady=5, padx=10)
        Entry(self.frame_principal, textvariable=domicilio_paciente, font= ('Comic Sans MS', 14)).grid(column=1, row=4, pady=5, padx=10)
        Entry(self.frame_principal, textvariable=telefono_paciente, font= ('Comic Sans MS', 14)).grid(column=1, row=5, pady=5, padx=10)
        Entry(self.frame_principal, textvariable=email_paciente, font= ('Comic Sans MS', 14)).grid(column=1, row=6, pady=5, padx=10)
        Entry(self.frame_principal, textvariable=obrasocial_paciente, font= ('Comic Sans MS', 14)).grid(column=1, row=7, pady=5, padx=10)
        Entry(self.frame_principal, textvariable=nrosocio_paciente, font= ('Comic Sans MS', 14)).grid(column=1, row=8, pady=5, padx=10)
        
        Label(self.frame_principal, text= 'Nombre/s',  fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=1, pady=5, padx=2)
        Label(self.frame_principal, text= 'Apellido/s',  fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=2, pady=5, padx=2)
        Label(self.frame_principal, text= 'D.N.I.',  fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=3, pady=5, padx=2)
        Label(self.frame_principal, text= 'Domicilio',  fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=4, pady=5, padx=2)
        Label(self.frame_principal, text= 'Telefono', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=5, pady=5, padx=2)
        Label(self.frame_principal, text= 'Email', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=6, pady=5, padx=2)
        Label(self.frame_principal, text= 'Obra Social', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=7, pady=5, padx=2)
        Label(self.frame_principal, text= 'Nro de socio', fg= 'black', font= ('Comic Sans MS', 12, 'bold')).grid(column=0, row=8, pady=5, padx=2)
        Button(self.frame_principal, text= 'Cerrar',  font= ('Comic Sans MS', 12, BOLD), fg= 'white', bg= '#1F704B', activebackground= 'gray', bd= 0, command= self.frame_paciente.destroy).grid(column= 3, row=1, pady= 5, padx= 200)
        Button(self.frame_principal, text= 'Cancelar',  font= ('Comic Sans MS', 12, BOLD), fg= 'white', bg= '#1F704B', activebackground= 'gray', bd= 0, command= self.frame_paciente.destroy).grid(column= 3, row=2, pady= 5, padx= 200)
        Button(self.frame_principal, text= 'Limpiar datos',  font= ('Comic Sans MS', 12, BOLD), fg= 'white', bg= '#1F704B', activebackground= 'gray', bd= 0, command= self.frame_paciente.destroy).grid(column= 3, row=2, pady= 5, padx= 200)

        self.frame_paciente.mainloop()
    def only_numbers(char):
        return char.isdigit()    
		
if __name__ == "__main__":
    Paciente()

