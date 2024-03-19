import sqlite3
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import io

conn = sqlite3.connect('imagenes.db')
cursor = conn.cursor()

cursor.execute("SELECT imagen FROM imagenes")
imagen_blob = cursor.fetchone()[0]

ventana = Tk()
ventana.title("Mostrar imagen BLOB")
label_imagen = Label(ventana)
label_imagen.pack()

imagen = Image.open(io.BytesIO(imagen_blob))

imagen_tk = ImageTk.PhotoImage(imagen)

label_imagen.config(image=imagen_tk)

ventana.mainloop()
