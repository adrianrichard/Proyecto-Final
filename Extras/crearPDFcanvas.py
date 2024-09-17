import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageDraw
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Image as PDFImage

# Función para crear una imagen en blanco
def create_blank_image(width, height):
    return Image.new('RGB', (width, height), 'white')

# Función para dibujar en el canvas de tkinter y en una imagen de Pillow
def draw_on_canvas(canvas, pillow_image):
    draw = ImageDraw.Draw(pillow_image)
##
##    # Crear dibujos en el canvas
##    canvas.create_rectangle(50, 50, 200, 200, fill="blue", outline="black")
##    canvas.create_oval(100, 100, 250, 250, fill="red", outline="black")
##    canvas.create_line(50, 50, 250, 250, fill="green", width=3)
##    canvas.create_text(150, 300, text="Dibujo en Canvas", font=("Helvetica", 16))

    # Dibujar en la imagen de Pillow
    draw.rectangle([50, 50, 200, 200], fill="blue", outline="black")
    draw.ellipse([100, 100, 250, 250], fill="red", outline="black")
    for i in range(0,3):
        x = 50*i
        print(i, x)

        draw.line([50*i, 50*i, 250*i, 250], fill="green", width=3)
    draw.text((150, 300), "Dibujo en Canvas", fill="black")
    width = 100
    height = 100
    x1=100
    y1=25
    x2 = x1 + width
    y2 = y1 + height
    canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2,fill="white", outline = "black")
# Función para crear un PDF con el contenido del canvas
def create_pdf_with_canvas_content():
    pdf_filename = "documento_con_canvas.pdf"
    document = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # Crear una ventana de tkinter
    root = tk.Tk()
    root.title("Canvas de tkinter")

    # Crear un canvas
    canvas_width = 400
    canvas_height = 400
    canvas = Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()

    # Crear una imagen en blanco con Pillow
    pillow_image = create_blank_image(canvas_width, canvas_height)

    # Dibujar en el canvas y en la imagen de Pillow
    draw_on_canvas(canvas, pillow_image)

    # Guardar la imagen en un archivo temporal
    temp_filename = tempfile.mktemp(suffix='.png')
    pillow_image.save(temp_filename, format='png')

    # Crear el PDF
    content = []
    pdf_image = PDFImage(temp_filename, width=6*inch, height=6*inch)
    content.append(pdf_image)

    # Construir el documento PDF
    document.build(content)

    root.destroy()
    print(f"PDF generado: {pdf_filename}")

create_pdf_with_canvas_content()
