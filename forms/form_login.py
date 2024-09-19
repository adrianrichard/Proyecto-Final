import tkinter as tk
from tkinter import ttk
from tkinter import  *
import util.generic as utl
from forms.form_administrador import MasterPanel
from forms.form_secretario import SecretarioPanel
from forms.form_odontologo import OdontologoPanel
from tkinter  import messagebox
from bd.conexion import Conexion
import re

class Login:

    def verificar(self, event=None):
        """Ingreso de usuario y contraseña"""
        username = self.nombre_usuario.get()
        password = self.pass_usuario.get()
        """Instancia de Conexion"""
        db = Conexion()
        """comprobar si existe la base de datos"""
        if(db.comprobar_bd()):
            """Conectar BD y crear cursor"""
            db.conectar()
            """Busca el usuario y contraseña"""
            if db.buscar_usuario(username, password):
                """Determina que tipo de usuario ingreso"""
                tipo_user = db.determinar_usuario(username, password)
                """Si es administrador"""
                if tipo_user[0][0] == 'administrador':
                    messagebox.showinfo(title = "Ingreso", message = "Ingreso autorizado")
                    db.cerrar_bd()
                    self.nombre_usuario.set('')
                    self.pass_usuario.set('')
                    self.frame_login.destroy()
                    MasterPanel()
                """Si es odontologo"""
                if tipo_user[0][0] == 'odontologo':
                    messagebox.showinfo(title = "Ingreso", message = "Ingreso autorizado")
                    db.cerrar_bd()
                    self.nombre_usuario.set('')
                    self.pass_usuario.set('')
                    self.frame_login.destroy()
                    OdontologoPanel()
                """Si es secretario"""
                if tipo_user[0][0] == 'secretario':
                    messagebox.showinfo(title = "Ingreso", message = "Ingreso autorizado")
                    db.cerrar_bd()
                    self.nombre_usuario.set('')
                    self.pass_usuario.set('')
                    self.frame_login.destroy()
                    SecretarioPanel()

            else:
                """Si usuario y/o contraseña son incorrectos"""
                messagebox.showerror(title = "Advertencia", message = "Usuario o contraseña incorrectos")
            db.cerrar_bd()

        else:
            messagebox.showerror(title = "Advertencia", message = "Error de conexión a base de datos")


    def validar_nombre(self, value):
        pattern = r'\b[A-Za-z_]\b'
        if re.fullmatch(pattern, value) is None:
            return False 
        return True

    def validar_pass(self, value):
        pattern = r'\b[A-Za-z0-9_]\b'
        if re.fullmatch(pattern, value) is None:
            return False
        return True

    def __init__(self):

        self.frame_login = tk.Tk()
        self.frame_login.title('DENTALMATIC')
        self.frame_login.geometry('500x500')
        self.frame_login.resizable(width = 0, height = 0)
        self.imagen_ventana = utl.leer_imagen('tooth.jpg', (38, 38))
        self.frame_login.iconphoto(False, self.imagen_ventana)

        utl.centrar_ventana(self.frame_login, 600, 500)
        fuente2=('Comic Sans MS', 15)
        fuente='Comic Sans MS'
        color_fuente = 'black'
        color_fondo1 = utl.definir_color_fondo()
        color_fondo2 = 'gray90'
        self.nombre_usuario = StringVar()
        self.pass_usuario = StringVar()

        # frame_logo
        try:
            logo = utl.leer_imagen("logo1.png", (250, 200))
            frame_logo = tk.Frame(self.frame_login, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10, bg=color_fondo1)
            frame_logo.pack(side="left", expand=tk.YES, fill=tk.BOTH)
            tk.Label(frame_logo, image=logo, bg=color_fondo1).place(x=0, y=0, relwidth=1, relheight=1)
        except:
            frame_logo = tk.Frame(self.frame_login, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10, bg=color_fondo1)
            frame_logo.pack(side="left", expand=tk.YES, fill= tk.BOTH)
            tk.Label(frame_logo, text="DENTALMATIC", font=(fuente, 25), fg="white", bg=color_fondo1, anchor="w").place(x=0, y=0, relwidth=1, relheight=1)

        #frame_form
        frame_form = tk.Frame(self.frame_login, bd=0, relief=tk.SOLID, bg=color_fondo2)
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)

        #frame_form_top
        frame_form_top = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg=color_fondo2)
        frame_form_top.pack(side="top", fill=tk.X)
        tk.Label(frame_form_top, text="Inicio de sesión", font=(fuente, 20), fg=color_fuente, bg=color_fondo2, pady=50).pack(expand=tk.YES, fill=tk.BOTH)
        #end frame_form_top

        #frame_form_fill
        frame_form_fill = tk.Frame(frame_form, height=50,  bd=0, relief=tk.SOLID, bg=color_fondo2)
        frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        tk.Label(frame_form_fill, text="Usuario", font=fuente2, fg=color_fuente, bg=color_fondo2, anchor="w").pack(fill=tk.X, padx=20, pady=5)
        self.usuario = ttk.Entry(frame_form_fill, textvariable=self.nombre_usuario, font=(fuente, 14), validate="key", validatecommand=(frame_form_fill.register(self.validar_nombre), "%S"))
        self.usuario.pack(fill=tk.X, padx=20, pady=10)
        self.usuario.focus()

        etiqueta_password = tk.Label(frame_form_fill, text="Contraseña", font=fuente2, fg=color_fuente, bg=color_fondo2, anchor="w")
        etiqueta_password.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(frame_form_fill, textvariable=self.pass_usuario, font=(fuente, 14), validate="key", validatecommand=(frame_form_fill.register(self.validar_pass), "%S"))
        self.password.pack(fill=tk.X, padx=20, pady=10)
        self.password.bind('<Return>', (lambda event: self.verificar()))

        self.password.config(show="*")

        inicio = tk.Button(frame_form_fill, text="Ingresar", font=fuente2, bg=color_fondo1, bd=0, fg="white", command=self.verificar)
        inicio.pack(fill=tk.X, padx=20, pady=20)
        inicio.bind("<Return>", (lambda event: self.verificar()))

        self.frame_login.mainloop()

if __name__ == "__main__":
   Login()