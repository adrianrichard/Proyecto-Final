import tkinter as tk
from tkinter import ttk, messagebox
class Frame(tk.Frame):
   def __init__(self, root = None):
        super().__init__(root, width=480, height=320)
        self.root = tk.Tk()
        self.root.title('DENTALMATIC')
        self.root.geometry('500x500')
        self.root.resizable(width= 0, height= 0)

        title = tk.Label(root, text= "Inicio de sesion", font= ('Comic Sans MS', 30), fg= "#666a88", bg='#fcfcfc', pady= 50)
        title.pack(expand= tk.YES,fill= tk.BOTH)

        etiqueta_usuario = tk.Label(root, text= "Usuario", font= ('Comic Sans MS', 14), fg="#666a88", bg='#fcfcfc', anchor= "w")
        etiqueta_usuario.pack(fill= tk.X, padx= 20, pady= 5)
        self.usuario = ttk.Entry(root, font= ('Comic Sans MS', 14))
        self.usuario.pack(fill= tk.X, padx= 20, pady= 10)

        etiqueta_password = tk.Label(root, text= "Contraseña", font= ('Comic Sans MS', 14), fg="#666a88", bg='#fcfcfc', anchor= "w")
        etiqueta_password.pack(fill= tk.X, padx= 20, pady= 5)
        self.password = ttk.Entry(root, font= ('Comic Sans MS', 14))
        self.password.pack(fill= tk.X, padx= 20, pady= 10)
        self.password.config(show= "*")

        inicio = tk.Button(root, text= "Ingresar", font= ('Comic Sans MS', 15), bg='#1F704B', bd=0, fg="#fff")
        inicio.pack(fill= tk.X, padx= 20, pady= 20)
        inicio.bind("<Return>", (lambda event: self.verificar()))