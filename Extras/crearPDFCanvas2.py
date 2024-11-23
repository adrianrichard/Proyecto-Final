import tkinter as tk
from PIL import Image, ImageGrab
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas as pdf_canvas
import os

def crear_pdf():
    # Captura la ventana y guarda el área del Canvas
    x0 = root.winfo_rootx() + canvas.winfo_x()
    y0 = root.winfo_rooty() + canvas.winfo_y()
    x1 = x0 + canvas.winfo_width()
    y1 = y0 + canvas.winfo_height()
    imagen_canvas = ImageGrab.grab((x0, y0, x1, y1))
    imagen_canvas.save("canvas_image.png")

    # Crear el PDF con ReportLab e insertar la imagen
    pdf = pdf_canvas.Canvas("output.pdf", pagesize=A4)
    ancho_pagina, alto_pagina = A4
    logo_path = "LOGO.png"
    alto_imagen=400
    if os.path.exists(logo_path):
        with Image.open(logo_path) as img:
            logo_width, logo_height = img.size
            escala_logo = min(alto_imagen / logo_width, alto_imagen / logo_height)  # Escalar a máximo 80x80
            logo_width = int(logo_width * escala_logo)
            logo_height = int(logo_height * escala_logo)
            logo_x = (ancho_pagina - logo_width) / 2  # Centrar en X
            logo_y = alto_pagina - 120  # Posición en Y desde la parte superior

        pdf.drawImage(logo_path, logo_x, logo_y, width=logo_width, height=logo_height)

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, alto_pagina - 150, f"Apellido/s y Nombre/s:")
    pdf.drawString(50, alto_pagina - 170, f"DNI: ")
    pdf.drawString(50, alto_pagina - 190, f"Obra Social:")
    pdf.drawString(ancho_pagina - 300, alto_pagina - 190, f"N° de Socio: ")
    captura_path = "canvas_image.png"
    if os.path.exists(captura_path):
        with Image.open(captura_path) as img:
            img_width, img_height = img.size
            max_width = ancho_pagina - 200
            max_height = alto_pagina - 300
            escala_canvas = min(max_width / img_width, max_height / img_height)
            img_width = int(img_width * escala_canvas)
            img_height = int(img_height * escala_canvas)
            captura_x = (ancho_pagina - img_width) / 2  # Centrar en X
            captura_y = alto_pagina - 500  # Margen inferior de 50

        pdf.drawImage(
            captura_path,
            captura_x,
            captura_y,
            width=img_width,
            height=img_height
        )
    pdf.save()
    print("PDF creado exitosamente")

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Gráfica en Canvas de Tkinter")

# Crear el Canvas
canvas = tk.Canvas(root, width=400, height=300, bg="white")
canvas.pack()

# Actualizar la ventana para obtener el tamaño correcto del canvas
root.update()

# Dibujar en el Canvas (ejemplo de gráfico de barras)
datos = [50, 120, 80, 150, 200]
ancho_barra = 40
espacio = 10
for i, valor in enumerate(datos):
    x0 = i * (ancho_barra + espacio) + espacio
    y0 = canvas.winfo_height() - valor
    x1 = x0 + ancho_barra
    y1 = canvas.winfo_height()
    canvas.create_rectangle(x0, y0, x1, y1, fill="blue")

# Botón para crear el PDF
boton_pdf = tk.Button(root, text="Crear PDF", command=crear_pdf)
boton_pdf.pack()

# Iniciar el bucle principal de Tkinter
root.mainloop()
