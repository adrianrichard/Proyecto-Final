import sqlite3  # O el conector de tu base de datos
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
#from PIL import Image
from io import BytesIO
import datetime
import shutil
from datetime import datetime
from tkinter import ttk, messagebox
import os
import util.config as utl
canvas = None

class Informes:
    def __init__(self):
        super().__init__()
        self.informe_seleccionado = ''  # Variable para almacenar la base de datos seleccionada
        self.fuenteb = utl.definir_fuente_bold()
        self.fuenten = utl.definir_fuente()

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

        btn_crear_grafico = tk.Button(frame, text="Crear gráfica", fg= 'white', font = self.fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, command= self.graficar_ventana)
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
        self.selector_mes.set(meses[0])
        if self.informe_seleccionado == 'Cantidad de turnos' or self.informe_seleccionado == 'Horario de turnos por año' or self.informe_seleccionado == 'Día de turnos':
            self.selector_mes.config(state="disabled")
        self.selector_anio= ttk.Combobox(self.nueva_ventana, state= "readonly", values= anios, width= 20, background= "white")
        self.selector_anio.grid(column= 1, row= 1, padx= (10, 10), pady= (0, 5))
        self.selector_anio.set(anios[0])
        # Frame para el gráfico en la nueva ventana
        self.frame_grafico = tk.Frame(self.nueva_ventana, background='white', relief="raised", width=450, height=350)
        self.frame_grafico.grid(column= 0, row= 3, columnspan=3, pady=(10, 10), padx=(10, 10))

        boton_graficar = tk.Button(self.nueva_ventana, text="Graficar", fg= 'white', font = self.fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, command= self.crear_grafica)
        boton_graficar.grid(column= 0, row= 2)
        boton_pdf = tk.Button(self.nueva_ventana, text="Guardar PDF", fg= 'white', font = self.fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, command= self.create_pdf)
        boton_pdf.grid(column= 1, row= 2)
        boton_salir = tk.Button(self.nueva_ventana, text="Salir", command= self.salir, bg= "orange", width= 8, font = self.fuenteb,  bd= 2, borderwidth= 2)
        boton_salir.grid(column= 2, row= 2)

    def salir(self):
        plt.close('all')
        self.nueva_ventana.destroy()

    def listar_informes(self):
        # Limpiar la tabla si ya tiene datos
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        self.tabla.insert("", "end", values=('Cantidad de turnos', 'Turnos dados por mes cada año'))
        self.tabla.insert("", "end", values=('Horario de turnos por mes', 'Horarios con más demanda por mes y año'))
        self.tabla.insert("", "end", values=('Horario de turnos por año', 'Horarios con más demanda por año'))
        self.tabla.insert("", "end", values=('Día de turnos', 'Días con más demanda por mes y año'))
        self.tabla.insert("", "end", values=('Prestaciones', 'Prestaciones más frecuentes por año'))
        self.tabla.insert("", "end", values=('Pacientes', 'Distribución por edad'))

    def seleccionar_desde_tabla(self, event):#
        selected_item = self.tabla.selection()
        if selected_item:
            item = self.tabla.item(selected_item)
            self.informe_seleccionado=item['values'][0]
            #print(self.informe_seleccionado)

    def turnosxmes(self):
        global canvas
        # Obtener los datos de la base de datos
        datos = self.obtener_datos_por_mes_anio()
        # # Procesar los datos para graficar
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        conteos = [fila[1] for fila in datos]
        # Crear la figura
        self.fig, ax = plt.subplots(figsize=(4.5, 3.8))
        ax.bar(meses, conteos, color='skyblue')  # Gráfico de barras
        ax.set_xlabel('Meses')
        ax.set_ylabel('Cantidad de turnos')
        ax.set_title('Turnos por Mes')
 
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
    
    def create_bar_chart(self):
        datos=[]
        valoresx=[]
        valoresy=[]
        self.fig, ax = plt.subplots(figsize=(4.5, 3.8))
        if self.informe_seleccionado == 'Cantidad de turnos':
            titulo='Cantidad de turnos por mes en '+self.selector_anio.get()
            datos = self.obtener_datos_por_mes_anio()
            valoresx = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            valoresy = [fila[1] for fila in datos]
            ax.bar(valoresx, valoresy, color='skyblue')  # Gráfico de barras
            ax.set_xlabel('Meses')
            ax.set_ylabel('Cantidad de turnos')
            ax.set_title(titulo)
            plt.xticks(rotation=60, ha='right')

        if self.informe_seleccionado == 'Horario de turnos por mes':
            titulo='Turnos por horario en el mes de '+self.selector_mes.get()+'-'+self.selector_anio.get()
            datos = self.obtener_horario_mes()
            valoresy = [fila[1] for fila in datos]
            valoresx = [fila[0] for fila in datos]
            ax.bar(valoresx, valoresy, color='skyblue')  # Gráfico de barras
            ax.set_xlabel('Horario')
            ax.set_ylabel('Cantidad de turnos')
            ax.set_title(titulo)
            plt.xticks(rotation=90, ha='right')

        if self.informe_seleccionado == 'Horario de turnos por año':
            titulo='Turnos por horario en el año '+self.selector_anio.get()
            datos = self.obtener_horario_anio()
            print(datos)
            valoresy = [fila[1] for fila in datos]
            valoresx = [fila[0] for fila in datos]
            ax.bar(valoresx, valoresy, color='skyblue')  # Gráfico de barras
            ax.set_xlabel('Horario')
            ax.set_ylabel('Cantidad de turnos')
            ax.set_title(titulo)
            plt.xticks(rotation=90, ha='right')
        if self.informe_seleccionado == 'Día de turnos':
            self.contar_dias_semana()
        plt.tight_layout()

        # Crear el canvas de matplotlib en Tkinter y asignarlo al frame de la nueva ventana
        canvas = FigureCanvasTkAgg(self.fig, self.frame_grafico)
        #self.canvas.get_tk_widget().destroy()
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)

        # Cerrar los recursos de la figura
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        plt.close(self.fig)
        buffer.seek(0)
        return buffer

    def crear_grafica(self):
        plt.clf()
        plt.close('all')        
        self.create_bar_chart()
        
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
    def mes_a_numero(self, nombre_mes):
        meses = {
            "enero": '01',
            "febrero": '02',
            "marzo": '03',
            "abril": '04',
            "mayo": '05',
            "junio": '06',
            "julio": '07',
            "agosto": '08',
            "septiembre": '09',
            "octubre": '10',
            "noviembre": '11',
            "diciembre": '12'
        }
        return meses.get(nombre_mes.lower(), "Mes no válido")
   
    def obtener_horario_mes(self):
    # Conexión a la base de datos (ajusta la ruta si usas sqlite)
        datos=['Vacio']
        mes=self.mes_a_numero(self.selector_mes.get())
        #print(mes)
        try:
            conn = sqlite3.connect('./bd/consultorio2.sqlite3')
            cursor = conn.cursor()
            # mes=self.selector_mes.get()
            # anio=self.selector_anio.get()
            # print('obtener datos')
            # Consulta SQL para agrupar por mes y año (en formato YYYY-MM)
            cursor.execute(""" SELECT Hora, COUNT(*) AS Cantidad_Turnos FROM Turnos WHERE strftime('%Y', Fecha) = ? AND strftime('%m', Fecha) = ? GROUP BY Hora ORDER BY Hora ASC""", (self.selector_anio.get(),mes,))
            datos = cursor.fetchall()
            conn.close()
        except:
            print('no carga')
            
        return datos
    
    def obtener_horario_anio(self):
    # Conexión a la base de datos (ajusta la ruta si usas sqlite)
        datos=['Vacio']
        
        try:
            conn = sqlite3.connect('./bd/consultorio2.sqlite3')
            cursor = conn.cursor()
            # mes=self.selector_mes.get()
            # anio=self.selector_anio.get()
            # print('obtener datos')
            # Consulta SQL para agrupar por mes y año (en formato YYYY-MM)
            cursor.execute(""" SELECT Hora, COUNT(*) AS Cantidad_Turnos FROM Turnos WHERE strftime('%Y', Fecha) = ? GROUP BY Hora ORDER BY Hora ASC""", (self.selector_anio.get(),))
            datos = cursor.fetchall()
            conn.close()
        except:
            print('no carga')
        return datos
    
    def get_image_size(self, image_path, max_width, max_height):
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

    def contar_dias_semana(self):
        
        conn = sqlite3.connect('./bd/consultorio2.sqlite3')
        cursor = conn.cursor()
        # Consulta SQL para agrupar por mes y año (en formato YYYY-MM)
        cursor.execute("SELECT CASE strftime('%w', Fecha)  WHEN '0' THEN 'Domingo'\
            WHEN '1' THEN 'Lunes'\
            WHEN '2' THEN 'Martes'\
            WHEN '3' THEN 'Miércoles'\
            WHEN '4' THEN 'Jueves'\
            WHEN '5' THEN 'Viernes'\
            WHEN '6' THEN 'Sábado'\
            END,\
            COUNT(*) AS Cantidad_Turnos FROM Turnos WHERE strftime('%Y', Fecha) = ? GROUP BY strftime('%w', Fecha) ORDER BY strftime('%w', Fecha)""", (self.selector_anio.get(),))
        datos = cursor.fetchall()
        # Convertir los resultados a una lista de años
        dias = [day[0] for day in datos]
        cantidad=[cant[1] for cant in datos]
        conn.close()
        #return años_unicos
        print(dias, cantidad)
        # dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
        # conteo = {dia: 0 for dia in dias_semana}
        # for fecha in fechas:
        #     dia_semana = dias_semana[fecha.weekday()]
        #     conteo[dia_semana] += 1
        # print(conteo)
        # return conteo
# Función para guardar el gráfico como un PDF
    def guardar_grafico_pdf(self):
        print('guardarPDF')
    # Pedir al usuario que elija dónde guardar el archivo
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        if file_path:
            # Guardar la figura de matplotlib como una imagen temporal
            imagen_temporal = "grafico_temporal.png"
            self.fig.savefig(imagen_temporal)

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

    def create_pdf(self):
        #name=''
        if self.informe_seleccionado == 'Cantidad de turnos':
            pdf_filename='CantidadTurnos'+self.selector_anio.get()+'.pdf'
        #pdf_filename = "documento_con_graficas.pdf"
        document = SimpleDocTemplate(pdf_filename, pagesize=A4)

        # Obtener los estilos de muestra
        styles = getSampleStyleSheet()

        # Contenido del PDF
        content = []
        
        # Añadir una imagen externa y mantener la relación de aspecto
        image_path = "./Extras/LOGO.png"  # Cambia "logo.png" al nombre de tu imagen
        max_width = 20 * cm
        max_height = 10 * cm
        if os.path.exists(image_path):
            img_width, img_height =self.get_image_size(image_path, max_width, max_height)
            logo_image = Image(image_path, width=img_width, height=img_height)
            content.append(logo_image)
        else:
            title = Paragraph("MyM Odontología", styles['Title'])
            content.append(title)
        
        # Título
        title = Paragraph("Informe", styles['Title'])
        content.append(title)
        
        # Crear gráficos y añadirlos al PDF
        bar_chart_buffer = self.create_bar_chart()
        bar_chart_image = Image(bar_chart_buffer, width=12 * cm, height=10* cm)
        content.append(bar_chart_image)

        # line_chart_buffer = create_line_chart()
        # line_chart_image = Image(line_chart_buffer, width=4*inch, height=3*inch)
        # # content.append(line_chart_image)

        # pie_chart_buffer = create_pie_chart()
        # pie_chart_image = Image(pie_chart_buffer, width=4*inch, height=3*inch)
        # content.append(pie_chart_image)

        # Construir el documento PDF
        document.build(content)

        # Abrir el PDF con el visor predeterminado del sistema
        os.startfile(pdf_filename)  # Para Windows
