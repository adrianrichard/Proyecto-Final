import tkinter as tk
from tkinter import ttk
from tkinter.font import BOLD
import util.generic as utl
from forms.form_master import MasterPanel
from tkinter.messagebox import showinfo,showerror
from bd.conexion import Conexion

class Login:

    def verificar(self):
        username = self.usuario.get()
        password = self.password.get()
        db = Conexion()

        if(db.comprobar_bd()):
            db.conectar()
            if db.buscar_usuario(username, password):
                showinfo(title= "Ingreso", message= "Ingreso autorizado")
                db.cerrar_bd()
                self.frame_login.destroy()
                MasterPanel()
            else:
                showerror(title= "Advertencia", message= "Usuario o contraseña incorrectos")
            db.cerrar_bd()

        else:
            showerror(title= "Advertencia", message= "Error de conexión a base de datos")
    


    def __init__(self):
        self.frame_login = tk.Tk()
        self.frame_login.title('DENTALMATIC')
        self.frame_login.geometry('500x500')
        self.frame_login.resizable(width= 0, height= 0)
        utl.centrar_ventana(self.frame_login, 600, 500)

        try:
            logo =utl.leer_imagen("./imagenes/logo1.png", (250, 200))
            frame_logo = tk.Frame(self.frame_login, bd= 0, width= 300, relief= tk.SOLID, padx= 10, pady= 10, bg= '#1F704B')
            frame_logo.pack(side= "left", expand= tk.YES, fill= tk.BOTH)
            label = tk.Label(frame_logo, image= logo, bg= '#1F704B')
            label.place(x= 0, y= 0, relwidth= 1, relheight= 1)            
        except:
        # frame_logo
            frame_logo = tk.Frame(self.frame_login, bd= 0, width= 300, relief= tk.SOLID, padx= 10, pady= 10, bg= '#1F704B')
            frame_logo.pack(side= "left", expand= tk.YES, fill= tk.BOTH)
            label = tk.Label(frame_logo, text= "DENTALMATIC", font= ('Comic Sans MS', 25), fg="white", bg='#1F704B', anchor= "w")
            label.place(x= 0, y= 0, relwidth= 1, relheight= 1)
        

        #frame_form
        frame_form = tk.Frame(self.frame_login, bd= 0, relief= tk.SOLID, bg= '#fcfcfc')
        frame_form.pack(side= "right", expand= tk.YES, fill= tk.BOTH)
        #frame_form

        #frame_form_top
        frame_form_top = tk.Frame(frame_form, height= 50, bd= 0, relief= tk.SOLID, bg= '#fcfcfc')
        frame_form_top.pack(side= "top", fill= tk.X)
        title = tk.Label(frame_form_top, text= "Inicio de sesión", font= ('Comic Sans MS', 30), fg= "#666a88", bg='#fcfcfc', pady= 50)
        title.pack(expand= tk.YES,fill= tk.BOTH)
        #end frame_form_top

        #frame_form_fill
        frame_form_fill = tk.Frame(frame_form, height= 50,  bd= 0, relief= tk.SOLID, bg='#fcfcfc')
        frame_form_fill.pack(side= "bottom", expand= tk.YES, fill= tk.BOTH)

        etiqueta_usuario = tk.Label(frame_form_fill, text= "Usuario", font= ('Comic Sans MS', 14), fg="#666a88", bg='#fcfcfc', anchor= "w")
        etiqueta_usuario.pack(fill= tk.X, padx= 20, pady= 5)
        self.usuario = ttk.Entry(frame_form_fill, font= ('Comic Sans MS', 14))
        self.usuario.pack(fill= tk.X, padx= 20, pady= 10)

        etiqueta_password = tk.Label(frame_form_fill, text= "Contraseña", font= ('Comic Sans MS', 14), fg="#666a88", bg='#fcfcfc', anchor= "w")
        etiqueta_password.pack(fill= tk.X, padx= 20, pady= 5)
        self.password = ttk.Entry(frame_form_fill, font= ('Comic Sans MS', 14))
        self.password.pack(fill= tk.X, padx= 20, pady= 10)
        self.password.config(show= "*")

        inicio = tk.Button(frame_form_fill, text= "Ingresar", font= ('Comic Sans MS', 15, BOLD), bg='#1F704B', bd=0, fg="#fff", command= self.verificar)
        inicio.pack(fill= tk.X, padx= 20, pady= 20)
        inicio.bind("<Return>", (lambda event: self.verificar()))
        #end frame_form_fill
        self.frame_login.mainloop()

if __name__ == "__main__":
   Login()