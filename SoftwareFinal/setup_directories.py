import os
import sys

def create_required_directories():
    """Crea las carpetas necesarias para la aplicación"""
    directories = ['bd', 'imagenes', 'informes', 'galeria']
    
    # Determinar la ruta base dependiendo de si está empaquetado o no
    if getattr(sys, 'frozen', False):
        # Ejecutando como empaquetado
        base_path = os.path.dirname(sys.executable)
    else:
        # Ejecutando desde el código fuente
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    for directory in directories:
        dir_path = os.path.join(base_path, directory)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Directorio creado: {dir_path}")
        else:
            print(f"Directorio ya existe: {dir_path}")
    
    return base_path

# Ejecutar al importar
create_required_directories()