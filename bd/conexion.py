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
    
    def cerrar_bd(self):
        self.cur.close()
                   
    def inserta_producto(self, codigo, nombre, modelo, precio, cantidad):        
        #sql='''INSERT INTO productos (CODIGO, NOMBRE, MODELO, PRECIO, CANTIDAD) VALUES('{}', '{}','{}', '{}','{}')'''.format(codigo, nombre, modelo, precio, cantidad)
        self.cur.close()

    '''def mostrar_productos(self):
        cursor = self.conexion.cursor()
        sql = "SELECT * FROM productos " 
        cursor.execute(sql)
        registro = cursor.fetchall()
        return registro

    def busca_producto(self, nombre_producto):
        cur = self.conexion.cursor()
        sql = "SELECT * FROM productos WHERE NOMBRE = {}".format(nombre_producto)
        cur.execute(sql)
        nombreX = cur.fetchall()
        cur.close()     
        return nombreX 
    
    def elimina_productos(self, nombre):
        cur = self.conexion.cursor()
        #sql='DELETE FROM productos WHERE NOMBRE = {}'.format(nombre)
        cur.execute(sql)
        self.conexion.commit()    
        cur.close()
    
    def actualiza_productos(self,Id, codigo, nombre, modelo, precio, cantidad):
        cur = self.conexion.cursor()
        sql ='UPDATE productos SET  CODIGO ='{}', NOMBRE = '{}' , MODELO = '{}', PRECIO = '{}', CANTIDAD = '{}'
        WHERE ID = '{}' .format(codigo, nombre, modelo, precio, cantidad, Id)
        cur.execute(sql)
        a = cur.rowcount
        self.conexion.commit()    
        cur.close()
        return a  
    '''
    