#import PIL
from PIL import ImageTk, Image
import re

path_relativo=""

def obtener_path(path):
        path_relativo=path
        return path_relativo

def leer_imagen(nombre_imagen, size):
        path_absoluto="./imagenes/"+nombre_imagen
        #print(path_absoluto)
        return ImageTk.PhotoImage(Image.open(path_absoluto).resize(size, Image.Resampling.LANCZOS))

def centrar_ventana(ventana,aplicacion_ancho,aplicacion_largo):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_largo = ventana.winfo_screenheight()
    x = int((pantalla_ancho/2) - (aplicacion_ancho/2))
    y = int((pantalla_largo/2) - (aplicacion_largo/2))
    return ventana.geometry(f"{aplicacion_ancho}x{aplicacion_largo}+{x}+{y}")

def definir_fuente():
    return ('Arial', 12)

def definir_fuente_bold():
    return ('Arial', 12, 'bold')

def definir_color_fuente():
    return 'black','white'

def definir_color_fondo():
    return '#1F704B', 'gray90'

def validar_password(password):
    valido=False
    minuscula=False
    mayuscula=False
    numero=False
    espacio=True
    caracter=True
    if len(password) < 8:
        valido = False
    else:
        for i in password:
            if i.islower():
                minuscula=True
            elif i.isdigit():
                numero=True
            elif i.isupper():
                mayuscula=True
            elif i.count(" ")== 1:
                espacio=False
            else:
                caracter=False
        if minuscula and mayuscula and numero and espacio and caracter:
            valido = True
    return valido

def validar_correo(self, value):
    pattern = r'\b[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(pattern, value) is None:
        return False
    return True