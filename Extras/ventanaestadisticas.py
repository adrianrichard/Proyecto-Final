import sqlite3  # O el conector de tu base de datos
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# Función para obtener los datos agrupados por mes y año
def obtener_datos_por_mes_anio():
    # Conexión a la base de datos (ajusta la ruta si usas sqlite)
    conn = sqlite3.connect('consultorio2.sqlite3')
    cursor = conn.cursor()

    # Consulta SQL para agrupar por mes y año (en formato YYYY-MM)
    cursor.execute("""
        SELECT strftime('%m', fecha) AS mes_anio, COUNT(*)
        FROM turnos
        GROUP BY mes_anio
    """)
    datos = cursor.fetchall()

    conn.close()
    return datos

# Función para graficar los datos por mes y año
def graficar_datos_por_mes_anio():
    # Obtener los datos de la base de datos
    datos = obtener_datos_por_mes_anio()

    # Procesar los datos para graficar
    meses_anios = [fila[0] for fila in datos]
    conteos = [fila[1] for fila in datos]

    # Crear la figura
    fig, ax = plt.subplots()
    ax.bar(meses_anios, conteos, color='skyblue')  # Gráfico de barras
    ax.set_xlabel('Meses y Años')
    ax.set_ylabel('Cantidad de turnos')
    ax.set_title('Turnos por Mes y Año')

    # Ajustar los ticks del eje X para que no se solapen
    plt.xticks(rotation=45, ha='right')

    # Crear el canvas de matplotlib en Tkinter
    canvas = FigureCanvasTkAgg(fig, ventana)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    # Cerrar los recursos de la figura una vez que se haya dibujado
    plt.close(fig)

# Crear la ventana de Tkinter
ventana = tk.Tk()
ventana.title('Gráfico de Turnos por Mes y Año')
# Frame superior para el título
frame_titulo = tk.Frame(ventana)
frame_titulo.pack(side=tk.TOP, fill=tk.X)

# Etiqueta de título
titulo = tk.Label(frame_titulo, text="Gráfico de Turnos por Mes y Año", font=("Arial", 16))
titulo.pack(pady=10)

# Frame para el gráfico
frame_grafico = tk.Frame(ventana)
frame_grafico.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Frame para los botones
frame_botones = tk.Frame(ventana)
frame_botones.pack(side=tk.BOTTOM, pady=20)

# Botón para graficar
boton_graficar = tk.Button(ventana, text="Graficar por Mes y Año", command=graficar_datos_por_mes_anio)
boton_graficar.pack()
##boton_salir = tk.Button(frame_botones, text="Salir", command=ventana.destroy)
##boton_salir.grid(column=1, row=0)
# Ejecutar la aplicación
ventana.mainloop()
