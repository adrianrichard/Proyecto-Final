import sqlite3
import os
from tkinter import messagebox

class Conexion():
    #maneja la ruta de la base de datos como una variable de clase o un parámetro para hacerla más flexible
    def __init__(self, ruta_bd='./bd/consultorio_odontologico.sqlite3'):
        self.ruta_bd = ruta_bd

    def comprobar_bd(self):
        return os.path.isfile(self.ruta_bd)

    def conectar(self):
        self.db = sqlite3.connect(self.ruta_bd)
        return self.db

    def obtener_cursor(self):
        self.cur = self.db.cursor()
        return self.cur

    def buscar_usuario(self, username, password):
        try:
            self.cur.execute('SELECT nombre_usuario, pass_usuario, tipo_usuario FROM usuarios WHERE nombre_usuario = ? AND pass_usuario = ?', (username, password))
            registro = self.cur.fetchone()
            return registro
        except sqlite3.Error as e:
            messagebox.showerror(title = "Advertencia", message =f"Error al conectar a la base de datos \n {e}")            

    # def determinar_usuario(self, username, password):
    #     self.cur.execute('SELECT tipo_usuario FROM usuarios WHERE nombre_usuario = ? AND pass_usuario = ?', (username, password))
    #     tipo_usuario = self.cur.fetchall()
    #     return tipo_usuario
    
    def cerrar_bd(self):
        if hasattr(self, 'cur'):
            self.cur.close()
        if hasattr(self, 'db'):
            self.db.close()
    
    def crear_bd_login(self):
        self.cur.execute('''
                CREATE TABLE IF NOT EXISTS Usuarios (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NOMBRE_USUARIO VARCHAR(50) NOT NULL,
                CLAVE VARCHAR(50) NOT NULL,
                TIPO_USUARIO VARCHAR(50) NOT NULL)
                ''')
        self.db.commit()
        self.cerrar_bd()  # Cierra la conexión correctamente