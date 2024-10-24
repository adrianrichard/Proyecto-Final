import datetime
import random
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

# Generar 100 fechas aleatorias
def generar_fechas_aleatorias(n):
    fechas = []
    for _ in range(n):
        año = random.randint(2000, 2024)
        mes = random.randint(1, 12)
        # Ajustar el día según el mes
        if mes == 2:
            # Febrero, considerar años bisiestos
            día = random.randint(1, 29 if (año % 4 == 0 and (año % 100 != 0 or año % 400 == 0)) else 28)
        elif mes in [4, 6, 9, 11]:
            # Abril, junio, septiembre, noviembre tienen 30 días
            día = random.randint(1, 30)
        else:
            # Otros meses tienen 31 días
            día = random.randint(1, 31)
        fecha = datetime.date(año, mes, día)
        fechas.append(fecha)
    return fechas

# Contar días de la semana excluyendo domingos
def contar_dias_semana(fechas):
    conteo = [0] * 6  # Solo 6 días (lunes a sábado)
    for fecha in fechas:
        if fecha.weekday() != 6:  # Excluir domingos
            conteo[fecha.weekday()] += 1
    return conteo

# Normalizar los valores de conteo
def normalizar_conteo(conteo):
    total = sum(conteo)
    return [x / total for x in conteo]

# Crear gráfica de torta y guardarla como archivo
def crear_grafica(conteo):
    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
    plt.pie(conteo, labels=dias_semana, autopct='%1.1f%%', startangle=140)
    plt.title('Frecuencia de días de la semana en 100 fechas aleatorias')
    plt.savefig('grafica.png')
    plt.close()

# Crear PDF
def crear_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Agregar logo, si existe
    try:
        pdf.image('LOGO.png', x=10, y=10, w=180)
    except FileNotFoundError:
        pdf.cell(200, 10, txt="LOGO no encontrado", ln=True, align='C')
    
    pdf.cell(200, 10, txt="Odontologia MyM", ln=True, align='C')
    pdf.cell(200, 10, txt="Domicilio: M David 1987  Teléfono: 34345678978", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Fecha: {datetime.date.today()}", ln=True, align='C')
    pdf.ln(40)  # Espacio antes de la imagen de la gráfica
    
    # Agregar gráfica
    try:
        pdf.image('grafica.png', x=10, y=60, w=180)
    except FileNotFoundError:
        pdf.cell(200, 10, txt="Gráfica no encontrada", ln=True, align='C')
    
    pdf.output("reporte.pdf")

    # Borrar la imagen después de crear el PDF, si existe
    if os.path.exists('grafica.png'):
        os.remove('grafica.png')

# Ejecutar funciones
fechas = generar_fechas_aleatorias(100)
conteo = contar_dias_semana(fechas)
conteo_normalizado = normalizar_conteo(conteo)
crear_grafica(conteo_normalizado)
crear_pdf()
