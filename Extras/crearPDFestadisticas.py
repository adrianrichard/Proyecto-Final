import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
import os

# Función para calcular el tamaño de la imagen manteniendo la relación de aspecto
def get_image_size(image_path, max_width, max_height):
    image_reader = ImageReader(image_path)
    img_width, img_height = image_reader.getSize()
    aspect_ratio = img_width / img_height

    if img_width > max_width:
        img_width = max_width
        img_height = img_width / aspect_ratio

    if img_height > max_height:
        img_height = max_height
        img_width = img_height * aspect_ratio

    return img_width, img_height

# Función para crear un gráfico de barras
def create_bar_chart():
    fig, ax = plt.subplots()
    categories = ['Ventas', 'Clientes', 'Proyectos']
    values = [100, 150, 25]
    ax.bar(categories, values, color=['blue', 'green', 'red'])
    ax.set_title('Estadísticas de Ventas', fontsize=14, fontweight='bold', family='serif')
    ax.set_xlabel('Categorías', fontsize=12, fontweight='bold', family='serif')
    ax.set_ylabel('Valores', fontsize=12, fontweight='bold', family='serif')

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)
    return buffer

# Función para crear un gráfico de líneas
def create_line_chart():
    fig, ax = plt.subplots()
    months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
    sales = [2000, 2500, 1500, 3500, 2500, 4500]
    ax.plot(months, sales, marker='o', color='b', linestyle='-')
    ax.set_title('Ventas Mensuales', fontsize=14, fontweight='bold', family='serif')
    ax.set_xlabel('Meses', fontsize=12, fontweight='bold', family='serif')
    ax.set_ylabel('Ventas ($)', fontsize=12, fontweight='bold', family='serif')

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)
    return buffer

# Función para crear un gráfico de pastel
def create_pie_chart():
    fig, ax = plt.subplots()
    labels = ['Producto A', 'Producto B', 'Producto C']
    sizes = [300, 500, 200]
    colors = ['gold', 'lightcoral', 'lightskyblue']
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)
    return buffer

# Crear el documento PDF
def create_pdf_with_charts():
    pdf_filename = "documento_con_graficas.pdf"
    document = SimpleDocTemplate(pdf_filename, pagesize=A4)

    # Obtener los estilos de muestra
    styles = getSampleStyleSheet()

    # Contenido del PDF
    content = []
    
    # Añadir una imagen externa y mantener la relación de aspecto
    image_path = "LOGO.png"  # Cambia "logo.png" al nombre de tu imagen
    max_width = 4 * inch
    max_height = 2 * inch
    if os.path.exists(image_path):
        img_width, img_height = get_image_size(image_path, max_width, max_height)
        logo_image = Image(image_path, width=img_width, height=img_height)
        content.append(logo_image)
    else:
        title = Paragraph("MyM Odontología", styles['Title'])
        content.append(title)
    
    # Título
    title = Paragraph("Informe", styles['Title'])
    content.append(title)
    
    # Crear gráficos y añadirlos al PDF
    bar_chart_buffer = create_bar_chart()
    bar_chart_image = Image(bar_chart_buffer, width=4*inch, height=3*inch)
    content.append(bar_chart_image)

    # line_chart_buffer = create_line_chart()
    # line_chart_image = Image(line_chart_buffer, width=4*inch, height=3*inch)
    # content.append(line_chart_image)

    pie_chart_buffer = create_pie_chart()
    pie_chart_image = Image(pie_chart_buffer, width=4*inch, height=3*inch)
    content.append(pie_chart_image)

    # Construir el documento PDF
    document.build(content)

    # Abrir el PDF con el visor predeterminado del sistema
    os.startfile(pdf_filename)  # Para Windows

    # Para macOS o Linux, puedes usar `open` o `xdg-open`
    # os.system(f"open {pdf_filename}")  # Para macOS
    # os.system(f"xdg-open {pdf_filename}")  # Para Linux

    print(f"PDF generado: {pdf_filename}")

# Ejecutar la función para crear el PDF
create_pdf_with_charts()
