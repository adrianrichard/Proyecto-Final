import sqlite3
import os
from tkinter import messagebox

class Conexion():
    # Variable de clase para rastrear todas las instancias
    _instancias = []
    
    def __init__(self, ruta_bd='./bd/consultorioMyM.sqlite3'):
        self.ruta_bd = ruta_bd
        self.db = None  # Inicializar explícitamente como None
        self.cur = None  # Inicializar explícitamente como None
        Conexion._instancias.append(self)

    def comprobar_bd(self):
        return os.path.isfile(self.ruta_bd)

    def conectar(self):
        try:
            self.db = sqlite3.connect(self.ruta_bd)
            return self.db
        except sqlite3.Error as e:
            messagebox.showerror("Advertencia", f"Error al conectar a la base de datos \n {e}")
            return None

    def obtener_cursor(self):
        if self.db:
            self.cur = self.db.cursor()
            return self.cur
        return None

    def buscar_usuario(self, username, password):
        try:
            if not self.cur:
                self.conectar()
                self.obtener_cursor()
            
            self.cur.execute('SELECT nombre_usuario, pass_usuario, tipo_usuario FROM usuarios WHERE nombre_usuario = ? AND pass_usuario = ?', (username, password))
            registro = self.cur.fetchone()
            return registro
        except sqlite3.Error as e:
            messagebox.showerror("Advertencia", f"Error al conectar a la base de datos \n {e}")
            return None

    def cerrar_bd(self):
        """Cierra la conexión de manera segura, evitando errores con None"""
        # Verificar que cur existe y no es None antes de cerrarlo
        if hasattr(self, 'cur') and self.cur is not None:
            try:
                self.cur.close()
            except:
                pass  # Ignorar errores al cerrar
        
        # Verificar que db existe y no es None antes de cerrarlo
        if hasattr(self, 'db') and self.db is not None:
            try:
                self.db.close()
            except:
                pass  # Ignorar errores al cerrar

        # Limpiar las referencias
        self.cur = None
        self.db = None

    @classmethod
    def cerrar_todas_conexiones(cls):
        """Cierra todas las conexiones a la base de datos de manera segura"""
        for instancia in cls._instancias:
            try:
                instancia.cerrar_bd()
            except Exception as e:
                messagebox.showerror(f"Advertencia: Error al cerrar conexión: {e}")
                # Continuar con las demás instancias

    @classmethod
    def reconectar_todas(cls):
        """Reconecta todas las instancias después de un cambio de BD"""
        for instancia in cls._instancias:
            try:
                if hasattr(instancia, 'ruta_bd'):
                    # Cerrar primero si hay conexiones existentes
                    instancia.cerrar_bd()
                    # Reconectar
                    instancia.db = sqlite3.connect(instancia.ruta_bd)
                    instancia.cur = instancia.db.cursor()
            except Exception as e:
                messagebox.showerror(f"Error al reconectar: {e}")

    def crear_bd_login(self):
        try:
            self.conectar()
            self.obtener_cursor()
            
            self.cur.execute('''
                    CREATE TABLE IF NOT EXISTS Usuarios (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    NOMBRE_USUARIO VARCHAR(50) NOT NULL,
                    CLAVE VARCHAR(50) NOT NULL,
                    TIPO_USUARIO VARCHAR(50) NOT NULL)
                    ''')
            self.db.commit()
            self.cerrar_bd()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al crear tabla de usuarios: {e}")