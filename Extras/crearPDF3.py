import tkinter as tk
from tkinter import ttk
from PIL import ImageGrab
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table, TableStyle
from reportlab.lib import colors

# Crear un gráfico con matplotlib
def create_chart():
    fig, ax = plt.subplots()
    categories = ['Ventas', 'Clientes', 'Proyectos']
    values = [100000, 150, 25]
    ax.bar(categories, values, color=['blue', 'green', 'red'])
    ax.set_title('Estadísticas del Negocio')
    ax.set_xlabel('Categorías')
    ax.set_ylabel('Valores')

    # Guardar el gráfico en un buffer de bytes
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)
    buffer.seek(0)
    return buffer

# Crear la interfaz gráfica con tkinter
def create_tkinter_window():
    window = tk.Tk()
    window.title("Reporte de Estadísticas")

    # Crear un gráfico y agregarlo a la ventana
    chart_buffer = create_chart()
    chart_image = tk.PhotoImage(data=chart_buffer.getvalue())

    label_chart = tk.Label(window, image=chart_image)
    label_chart.image = chart_image  # Mantener una referencia para evitar que se recoja
    label_chart.pack()

    # Estadísticas
    stats = tk.Label(window, text="Ventas Totales: $100,000\nClientes Nuevos: 150\nProyectos Completados: 25")
    stats.pack()

    window.update_idletasks()

    # Capturar la ventana de tkinter como una imagen
    x = window.winfo_rootx()
    y = window.winfo_rooty()
    x1 = x + window.winfo_width()
    y1 = y + window.winfo_height()
    img = ImageGrab.grab().crop((x, y, x1, y1))

    img_buffer = BytesIO()
    img.save(img_buffer, format='png')
    img_buffer.seek(0)

    window.destroy()
    return img_buffer

# Crear el documento PDF
def create_pdf_with_tkinter_content():
    pdf_filename = "documento_con_tkinter.pdf"
    document = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # Obtener los estilos de muestra
    styles = getSampleStyleSheet()

    # Contenido del PDF
    content = []

    # Capturar y añadir el contenido de la ventana tkinter
    tkinter_image_buffer = create_tkinter_window()
    tkinter_image = Image(tkinter_image_buffer, width=6*inch, height=4*inch)
    content.append(tkinter_image)

    # Construir el documento PDF
    document.build(content)

    print(f"PDF generado: {pdf_filename}")

create_pdf_with_tkinter_content()
