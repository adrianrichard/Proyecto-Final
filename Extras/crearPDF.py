import sys
import os
import subprocess
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Datos de ejemplo (reemplaza con tus propios datos)
datos_personales = ['Juan Pérez', '10/01/1994', 30, 'Av. Principal 123, Ciudad', '123-456789', 'juan@example.com']

datos_tabla = [
    {'fecha': '2024-06-15', 'prestacion': 'Limpieza dental', 'obra_social': 'OSDE', 'odontologo': 'Dr. Martínez'},
    {'fecha': '2024-06-20', 'prestacion': 'Extracción muela', 'obra_social': 'Swiss Medical', 'odontologo': 'Dra. Gómez'}
    # Agrega más filas según necesites
]

def create_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)

    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(25, 750, "Datos Personales")
    # Datos personales
    c.setFont("Helvetica", 12)
    y = 730
    x=25
    c.drawString(x, y, f"Nombre completo: {datos_personales[0]}")
    c.drawString(x+300, y, f"Dirección: {datos_personales[3]}")
    y -= 20
    c.drawString(x, y, f"Fecha de nacimiento: {datos_personales[1]}")
    c.drawString(x+300, y, f"Edad: {datos_personales[2]}")
    # for key, value in datos_personales.items():
    #     c.drawString(25, y, f"{key}: {value}")
    #     y -= 20

    # Espacio para la tabla
    y -= 20
    c.line(25, y, 600, y)

    # Encabezados de la tabla
    header = ["Fecha", "prestacion", "obra_social", "odontologo"]
    c.setFont("Helvetica-Bold", 12)
    y -= 30
    x = 25
    for item in header:
        c.drawString(x, y, item)
        x += 150

    # Contenido de la tabla
    c.setFont("Helvetica", 12)
    y -= 20
    for data in datos_tabla:
        x = 25
        for key in header:
            c.drawString(x, y, data[key.lower()])
            x += 150
        y -= 20

    c.save()

    # Abrir el archivo PDF con el visor predeterminado
    open_pdf(filename)

def open_pdf(filename):
    # Utilizar subprocess para abrir el visor de PDF predeterminado
    if sys.platform.startswith('darwin'):  # MacOS
        subprocess.call(['open', filename])
    elif os.name == 'nt':  # Windows
        os.startfile(filename)
    elif os.name == 'posix':  # Linux, BSD, etc.
        subprocess.call(['xdg-open', filename])

if __name__ == "__main__":
    nombrePDF=datos_personales[0]+'.pdf'
    print(nombrePDF)
    create_pdf(nombrePDF)
