import tkinter as tk
from PIL import Image, ImageGrab
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as pdf_canvas

def crear_pdf():
    # Captura la ventana y guarda el área del Canvas
    x0 = root.winfo_rootx() + canvas.winfo_x()
    y0 = root.winfo_rooty() + canvas.winfo_y()
    x1 = x0 + canvas.winfo_width()
    y1 = y0 + canvas.winfo_height()
    imagen_canvas = ImageGrab.grab((x0, y0, x1, y1))
    imagen_canvas.save("canvas_image.png")

    # Crear el PDF con ReportLab e insertar la imagen
    pdf = pdf_canvas.Canvas("output.pdf", pagesize=letter)
    pdf.drawImage("canvas_image.png", 0, 0, width=400, height=300)  # Ajustar según el tamaño del canvas
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
