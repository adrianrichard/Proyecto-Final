from PIL import ImageTk, Image
path_relativo=""

def obtener_path(path):
        path_relativo=path
        return path_relativo
        
def leer_imagen(path, size):
        path_absoluto=path_relativo+path
        return ImageTk.PhotoImage(Image.open(path_absoluto).resize(size, Image.Resampling.LANCZOS))

def centrar_ventana(ventana,aplicacion_ancho,aplicacion_largo):    
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_largo = ventana.winfo_screenheight()
    x = int((pantalla_ancho/2) - (aplicacion_ancho/2))
    y = int((pantalla_largo/2) - (aplicacion_largo/2))
    return ventana.geometry(f"{aplicacion_ancho}x{aplicacion_largo}+{x}+{y}")
