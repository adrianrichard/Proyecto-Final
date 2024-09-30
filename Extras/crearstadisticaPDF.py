import datetime
import random
import matplotlib.pyplot as plt
from fpdf import FPDF

# Función para generar una lista de 100 fechas aleatorias en el año 2024
def generar_fechas_aleatorias(n=100, start_year=2024):
    fechas = []
    start_date = datetime.date(start_year, 1, 1)
    end_date = datetime.date(start_year, 12, 31)
    delta = (end_date - start_date).days
    for _ in range(n):
        random_days = random.randint(0, delta)
        fecha = start_date + datetime.timedelta(days=random_days)
        fechas.append(fecha)
    return fechas

# Función para contar cuántas veces aparece cada día de la semana
def contar_dias_semana(fechas):
    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    conteo = {dia: 0 for dia in dias_semana}
    for fecha in fechas:
        dia_semana = dias_semana[fecha.weekday()]
        conteo[dia_semana] += 1
    return conteo

# Generar las 100 fechas aleatorias
fechas_aleatorias = generar_fechas_aleatorias()

# Contar cuántas veces aparece cada día de la semana
conteo_dias = contar_dias_semana(fechas_aleatorias)

# Crear gráfica
plt.bar(conteo_dias.keys(), conteo_dias.values(), color='skyblue')
plt.xlabel('Día de la semana')
plt.ylabel('Frecuencia')
plt.title('Distribución de días de la semana en fechas aleatorias')

# Guardar gráfica temporalmente
graph_file_path = 'grafico_dias_semana.png'
plt.savefig(graph_file_path)
plt.close()

# Crear PDF con encabezado y la imagen
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Encabezado
pdf.cell(200, 10, txt="Odontologia MyM", ln=True, align='C')
pdf.cell(200, 10, txt="Domicilio: M David 1987", ln=True, align='C')
pdf.cell(200, 10, txt=f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d')}", ln=True, align='C')
pdf.cell(200, 10, txt="Telefono: 34345678978", ln=True, align='C')

# Insertar la imagen de la gráfica
pdf.image(graph_file_path, x=50, y=60, w=110)

# Guardar el PDF
pdf_output_path = "Reporte_Odontologia.pdf"
pdf.output(pdf_output_path)

pdf_output_path
