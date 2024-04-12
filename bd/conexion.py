import sqlite3
import os

class Conexion():

    def comprobar_bd(self):
        return os.path.isfile('./bd/consultorio.sqlite3')

    def conectar(self):
        self.db = sqlite3.connect('./bd/consultorio.sqlite3')
        self.cur = self.db.cursor()

    def buscar_usuario(self, username, password):
        self.cur.execute('SELECT Nombre_usuario, Clave FROM Usuarios WHERE Nombre_usuario = ? AND Clave = ?', (username, password))
        registro = self.cur.fetchall()
        return registro
    
    def determinar_usuario(self, username, password):
        self.cur.execute('SELECT Tipo_usuario FROM Usuarios WHERE Nombre_usuario = ? AND Clave = ?', (username, password))
        tipo_usuario = self.cur.fetchall()
        return tipo_usuario
    
    def cerrar_bd(self):
        self.cur.close()
 