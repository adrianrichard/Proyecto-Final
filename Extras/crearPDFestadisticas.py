import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table, TableStyle
from reportlab.lib import colors

# Función para crear un gráfico de barras
def create_bar_chart():
    fig, ax = plt.subplots()
    categories = ['Ventas', 'Clientes', 'Proyectos']
    values = [100, 150, 25]
    ax.bar(categories, values, color=['blue', 'green', 'red'])
    ax.set_title('Estadísticas de Ventas', fontsize=14, fontweight='bold', family='serif')
    ax.set_xlabel('Categorías', fontsize=12, fontweight='bold', family='serif')
    ax.set_ylabel('Valores', fontsize=12, fontweight='bold', family='serif')

    # Personalizar la fuente de los ticks
    ax.tick_params(axis='both', which='major', labelsize=10, labelcolor='black', direction='in')
    ax.xaxis.set_tick_params(labelsize=10, labelcolor='black')
    ax.yaxis.set_tick_params(labelsize=10, labelcolor='black')

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

    # Personalizar la fuente de los ticks
    ax.tick_params(axis='both', which='major', labelsize=10, labelcolor='black', direction='in')
    ax.xaxis.set_tick_params(labelsize=10, labelcolor='black')
    ax.yaxis.set_tick_params(labelsize=10, labelcolor='black')

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
    document = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # Obtener los estilos de muestra
    styles = getSampleStyleSheet()

    # Contenido del PDF
    content = []

    # Título
    title = Paragraph("Reporte de Estadísticas con Gráficos", styles['Title'])
    content.append(title)

    # Crear gráficos y añadirlos al PDF
    bar_chart_buffer = create_bar_chart()
    bar_chart_image = Image(bar_chart_buffer, width=4*inch, height=3*inch)
    content.append(bar_chart_image)

    line_chart_buffer = create_line_chart()
    line_chart_image = Image(line_chart_buffer, width=4*inch, height=3*inch)
    content.append(line_chart_image)

    pie_chart_buffer = create_pie_chart()
    pie_chart_image = Image(pie_chart_buffer, width=4*inch, height=3*inch)
    content.append(pie_chart_image)

    # Estadísticas en forma de tabla
    data = [
        ['Categoría', 'Valor'],
        ['Ventas Totales', '$100,000'],
        ['Clientes Nuevos', '150'],
        ['Proyectos Completados', '25'],
    ]

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    content.append(table)

    # Construir el documento PDF
    document.build(content)

    print(f"PDF generado: {pdf_filename}")

create_pdf_with_charts()
