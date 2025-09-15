from modulos.modulo_login import Login
import os
import sys
import tkinter as tk
from tkinter import messagebox

class DentalApp:
    def __init__(self):
        self.setup_directories()
        # El resto de tu inicialización...
    
    def setup_directories(self):
        """Crear carpetas necesarias si no existen"""
        if getattr(sys, 'frozen', False):
            self.base_dir = os.path.dirname(sys.executable)
        else:
            self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        directories = {
            'bd': 'Base de datos',
            'imagenes': 'Archivos de imágenes',
            'informes': 'Reportes PDF',
            'galeria': 'Galería de imágenes'
        }
        
        for dir_name, description in directories.items():
            dir_path = os.path.join(self.base_dir, dir_name)
            if not os.path.exists(dir_path):
                try:
                    os.makedirs(dir_path)
                    print(f"Creado: {dir_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo crear {description}: {e}")
                    sys.exit(1)

# Al inicio de tu ejecución
if __name__ == "__main__":
    app = DentalApp()
    # Resto de tu código...
"""Abre la ventana de Login"""
Login()