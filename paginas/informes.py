import sqlite3  # O el conector de tu base de datos
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as pdf_canvas
from PIL import Image
import shutil
from datetime import datetime
from tkinter import ttk, messagebox
import os
import util.config as utl
canvas = None
class Informes:
    def __init__(self):
        super().__init__()
        #frame = ventana
        self.informe_seleccionado = ''  # Variable para almacenar la base de datos seleccionada
        self.fuenteb = utl.definir_fuente_bold()
        self.fuenten = utl.definir_fuente()
        #self.configurar_interfaz()
        

    def configurar_interfaz(self, frame):
        self.frame=frame
        # Estilo de la tabla
        estilo_tabla = ttk.Style(self.frame)
        estilo_tabla.configure('Treeview.Heading', background='green', fg='black', padding=3, font=('Arial', 11, 'bold'))

        # Crear la tabla para mostrar las bases de datos
        self.tabla = ttk.Treeview(self.frame, columns=("Informe", "Descripcion"), show="headings", height=4)
        self.tabla.heading("Informe", text="Informe")
        self.tabla.heading("Descripcion", text="Descripción")
        self.tabla.column('Informe', width= 200 , anchor= 'w')
        self.tabla.column('Descripcion',  width= 350 , anchor= 'w')
        [frame.columnconfigure(i, weight= 1) for i in range(frame.grid_size()[0]-1)]
        self.tabla.grid(column= 0, row= 5, columnspan= 2, padx= (10,0), sticky= 'nsew')
        ladoy = ttk.Scrollbar(frame, orient ='vertical', command = self.tabla.yview)
        ladoy.grid(column= 3, row= 5, sticky='ns')
        self.listar_informes()
        # Bind para seleccionar la base de datos desde la tabla
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_desde_tabla)

        btn_crear_grafico = tk.Button(frame, text="Crear gráfica", fg= 'white', font = self.fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, command=self.graficar_ventana)
        btn_crear_grafico.grid(column= 0, row= 6, padx=(10, 10), pady=(10, 10))
        # # Botón para crear una copia de seguridad

        # btn_guardar_copia = tk.Button(frame, text="Crear copia de seguridad", fg= 'white', font = self.fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, command=self.crear_backup)
        # btn_guardar_copia.grid(column= 1, row=6, padx=(10, 10), pady=(10, 10))

    def graficar_ventana(self):
        # Crear una nueva ventana
        self.nueva_ventana = tk.Toplevel(self.frame)
        self.nueva_ventana.title('Informes')
        self.nueva_ventana.resizable(width= 0, height= 0)
        utl.centrar_ventana(self.nueva_ventana, 500, 500)
        self.nueva_ventana.grab_set_global() # Obliga a las ventanas estar deshabilitadas y deshabilitar todos los eventos e interacciones con la ventana
        self.nueva_ventana.focus_set() # Mantiene el foco cuando se abre la ventana.
        titulo = tk.Label(self.nueva_ventana, text= "Informes", font= ("Arial", 16))
        titulo.grid(column= 0, row= 0)
        anios=self.obtener_anios()                   
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        self.selector_mes= ttk.Combobox(self.nueva_ventana, state= "readonly", values= meses, width= 20, background= "white")
        self.selector_mes.grid(column= 0, row= 1, padx= (10, 10), pady= (0, 5))
        self.selector_mes.set('Elija mes')
        if self.informe_seleccionado == 'Cantidad de pacientes':
            self.selector_mes.config(state="disabled")
        self.selector_anio= ttk.Combobox(self.nueva_ventana, state= "readonly", values= anios, width= 20, background= "white")
        self.selector_anio.grid(column= 1, row= 1, padx= (10, 10), pady= (0, 5))
        self.selector_anio.set('Elija año')
        # Frame para el gráfico en la nueva ventana
        self.frame_grafico = tk.Frame(self.nueva_ventana, background='white', relief="raised")
        self.frame_grafico.grid(column= 0, row= 3, columnspan=3, pady=(10, 10), padx=(10, 10))

        boton_graficar = tk.Button(self.nueva_ventana, text="Graficar", command= self.crear_grafica)
        boton_graficar.grid(column= 0, row= 2)
        boton_pdf = tk.Button(self.nueva_ventana, text="Guardar PDF", command=lambda: self.guardar_grafico_pdf)
        boton_pdf.grid(column= 1, row= 2)
        boton_salir = tk.Button(self.nueva_ventana, text="Salir", command=self.nueva_ventana.destroy)
        boton_salir.grid(column= 2, row= 2)

    def listar_informes(self):
        # Limpiar la tabla si ya tiene datos
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        self.tabla.insert("", "end", values=('Cantidad de pacientes', 'Pacientes atendidos por mes cada año'))
        self.tabla.insert("", "end", values=('Horario de turnos', 'Horarios con más demanda por mes y año'))
        self.tabla.insert("", "end", values=('Día de turnos', 'Días con más demanda por mes y año'))
        self.tabla.insert("", "end", values=('Prestaciones', 'Prestaciones más frecuentes por año'))
        self.tabla.insert("", "end", values=('Pacientes', 'Distribución por edad'))
        #Cantidad de pacientes atendidos:
        #Tipo de prestaciones realizadas:
        #horas y días de mayor demanda
        #Tipos de tratamientos más frecuentes:
        #Distribución por edad y sexo:

    def seleccionar_desde_tabla(self, event):#
        selected_item = self.tabla.selection()
        if selected_item:
            item = self.tabla.item(selected_item)
            self.informe_seleccionado=item['values'][0]
            #print(self.informe_seleccionado)
            #self.bd_seleccionada =  seleccion+'.sqlite3'
    
    def turnosxmes(self):
        global canvas
        # Obtener los datos de la base de datos
        datos = self.obtener_datos_por_mes_anio()
        #print(datos)
        #self.borrar_grafica()
        # # Procesar los datos para graficar
        #meses_anios = [fila[0] for fila in datos]
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        conteos = [fila[1] for fila in datos]
        # Crear la figura
        self.fig, ax = plt.subplots(figsize=(4, 3))
        ax.bar(meses, conteos, color='skyblue')  # Gráfico de barras
        ax.set_xlabel('Meses')
        ax.set_ylabel('Cantidad de turnos')
        ax.set_title('Turnos por Mes')
        # Ajustar la escala del eje Y (ejemplo)
        # ax.set_ylim(0, max(conteos) + 5)  # Limitar entre 0 y un poco más del máximo valor
    
        # # Ajustar la escala del eje X (ejemplo)
        # ax.set_xlim(-0.5, len(meses_anios) - 0.5) 
        # Ajustar los ticks del eje X para que no se solapen
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # Crear el canvas de matplotlib en Tkinter y asignarlo al frame de la nueva ventana
        canvas = FigureCanvasTkAgg(self.fig, self.frame_grafico)
        #self.canvas.get_tk_widget().destroy()
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)
        

        # Cerrar los recursos de la figura
        plt.close(self.fig)
  
    def crear_grafica(self):
        #print('Graficar')
        plt.clf()
        plt.close('all')
        
        self.turnosxmes()
    def borrar_grafica(self):
        global canvas  # Usar la variable global
        if canvas is not None:
            # Limpiar el canvas
            canvas.figure.clf()  # Limpia la figura
            canvas.draw()  # Redibuja el canvas
            canvas = None   
# Función para obtener los datos agrupados por mes y año
    def obtener_anios(self):
        conn = sqlite3.connect('./bd/consultorio2.sqlite3')
        cursor = conn.cursor()
        # Consulta SQL para agrupar por mes y año (en formato YYYY-MM)
        cursor.execute("SELECT DISTINCT strftime('%Y', Fecha) AS Año FROM Turnos ORDER BY Año DESC")
        años_unicos = cursor.fetchall()
        # Convertir los resultados a una lista de años
        años_unicos = [año[0] for año in años_unicos]
        conn.close()
        return años_unicos

    def obtener_datos_por_mes_anio(self):
    # Conexión a la base de datos (ajusta la ruta si usas sqlite)
        datos=['Vacio']
        try:
            conn = sqlite3.connect('./bd/consultorio2.sqlite3')
            cursor = conn.cursor()
            # mes=self.selector_mes.get()
            # anio=self.selector_anio.get()
            # print('obtener datos')
            # Consulta SQL para agrupar por mes y año (en formato YYYY-MM)
            cursor.execute(""" SELECT strftime('%m', Fecha) AS Mes, COUNT(*) AS CantidadTurnos FROM Turnos WHERE strftime('%Y', Fecha) = ? GROUP BY Mes ORDER BY Mes""", (self.selector_anio.get(),))
            datos = cursor.fetchall()
            conn.close()
        except:
            print('no carga')
            
        return datos

# Función para guardar el gráfico como un PDF
    def guardar_grafico_pdf(self, fig):
    # Pedir al usuario que elija dónde guardar el archivo
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        if file_path:
            # Guardar la figura de matplotlib como una imagen temporal
            imagen_temporal = "grafico_temporal.png"
            fig.savefig(imagen_temporal)

            # Crear el PDF con reportlab
            c = pdf_canvas.Canvas(file_path, pagesize=letter)
            c.drawString(100, 750, "Gráfico de Turnos por Mes")

            # Cargar la imagen temporal
            img = Image.open(imagen_temporal)
            img_width, img_height = img.size

            # Ajustar la imagen en el tamaño de la página del PDF
            max_width = 500
            max_height = 400
            scale = min(max_width / img_width, max_height / img_height)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)

            # Insertar la imagen en el PDF
            c.drawImage(imagen_temporal, 50, 300, new_width, new_height)

            # Guardar y cerrar el PDF
            c.save()

            # Eliminar la imagen temporal
            img.close()

# # Función para manejar el cierre de la ventana principal
# def cerrar_ventana():
#     ventana.quit()
#     ventana.destroy()
# # Crear la ventana de Tkinter
# ventana = tk.Tk()
# ventana.title('Gráfico de Turnos por Mes y Año')
# ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana)

# # Frame superior para el título
# frame_titulo = tk.Frame(ventana)
# frame_titulo.pack(side=tk.TOP, fill=tk.X)

# # Etiqueta de título
# titulo = tk.Label(frame_titulo, text="Gráfico de Turnos por Mes y Año", font=("Arial", 16))
# titulo.pack(pady=10)

# # Frame para el gráfico
# frame_grafico = tk.Frame(ventana)
# frame_grafico.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# # Frame para los botones
# frame_botones = tk.Frame(ventana)
# frame_botones.pack(side=tk.BOTTOM, pady=20)

# # Botón para graficar
# boton_graficar = tk.Button(ventana, text="Graficar por Mes y Año", command=graficar_en_nueva_ventana)
# boton_graficar.pack()
# ##boton_salir = tk.Button(frame_botones, text="Salir", command=ventana.destroy)
# ##boton_salir.grid(column=1, row=0)
# # Ejecutar la aplicación
# ventana.mainloop()
