#import PIL
from PIL import ImageTk, Image
from tkinter  import messagebox
import re
from .paths import resource_path

path_relativo=""

def obtener_path(path):
    path_relativo=path
    return path_relativo

def leer_imagen(path, tamaño, mantener_proporciones=True):
    try:
        # Usar resource_path para obtener la ruta correcta
        full_path = resource_path(path)
        #messagebox.showerror(f"Intentando cargar imagen: {full_path}")  # Debug
        
        img = Image.open(full_path)
        
        if mantener_proporciones:
            # Calcular nuevo tamaño manteniendo proporciones
            ancho_original, alto_original = img.size
            ancho_deseado, alto_deseado = tamaño
            
            # Calcular ratios
            ratio_ancho = ancho_deseado / ancho_original
            ratio_alto = alto_deseado / alto_original
            
            # Usar el ratio más pequeño para mantener proporciones
            ratio = min(ratio_ancho, ratio_alto)
            
            nuevo_ancho = int(ancho_original * ratio)
            nuevo_alto = int(alto_original * ratio)
            
            # Redimensionar manteniendo proporciones
            img = img.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
        else:
            # Redimensionar forzando el tamaño exacto
            img = img.resize(tamaño, Image.Resampling.LANCZOS)
        
        return ImageTk.PhotoImage(img)
        
    except Exception as e:
        messagebox.showerror("Error", "No se logro cargar la imagen")
        return None

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