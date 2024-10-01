import sqlite3
import os

class Conexion():

    def comprobar_bd(self):
        return os.path.isfile('./bd/consultorio_odontologico.sqlite3')

    def conectar(self):
        self.db = sqlite3.connect('./bd/consultorio_odontologico.sqlite3')
        return self.db
    
    def obtener_cursor(self):
        self.cur = self.db.cursor()
        return self.db.cursor()

    def buscar_usuario(self, username, password):
        self.cur.execute('SELECT nombre_usuario, pass_usuario FROM usuarios WHERE nombre_usuario = ? AND pass_usuario = ?', (username, password))
        registro = self.cur.fetchall()
        return registro
    
    def determinar_usuario(self, username, password):
        self.cur.execute('SELECT tipo_usuario FROM usuarios WHERE nombre_usuario = ? AND pass_usuario = ?', (username, password))
        tipo_usuario = self.cur.fetchall()
        return tipo_usuario
    
    def cerrar_bd(self):
        self.cur.close()
    
    def crear_bd_login(self):
        self.miCursor.execute('''
                CREATE TABLE uUsuarios (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NOMBRE_USUARIO VARCHAR(50) NOT NULL,
                CLAVE VARCHAR(50) NOT NULL
                TIPO_USUARIO VARCHAR(50) NOT NULL)
                ''')
        self.miConexion.commit()
        self.miConexion.close()