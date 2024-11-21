import tkinter as tk
from PIL import ImageGrab
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as pdf_canvas

def crear_pdf():
    # Captura la ventana completa de Tkinter
    x0 = root.winfo_rootx()
    y0 = root.winfo_rooty()
    x1 = x0 + root.winfo_width()
    y1 = y0 + root.winfo_height()
    captura = ImageGrab.grab((x0, y0, x1, y1))
    captura.save("captura_tkinter.png")  # Guardar como imagen temporal

    # Crear PDF e insertar la imagen capturada
    pdf = pdf_canvas.Canvas("output.pdf", pagesize=letter)
    pdf.drawImage("captura_tkinter.png", 0, 0, width=letter[0], height=letter[1])  # Ajustar tamaño
    pdf.save()
    print("PDF creado exitosamente con la captura de pantalla")

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Ventana de Tkinter para Captura")

# Ejemplo de contenido en la ventana de Tkinter
canvas = tk.Canvas(root, width=400, height=300, bg="white")
canvas.pack()

# Dibujar algo en el Canvas (por ejemplo, un gráfico de barras)
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
boton_pdf = tk.Button(root, text="Crear PDF de la Ventana", command=crear_pdf)
boton_pdf.pack()

# Iniciar el bucle principal de Tkinter
root.mainloop()
