import sqlite3  # O el conector de tu base de datos
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
# from tkinter import filedialog
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas as pdf_canvas
from PIL import Image
import shutil
from datetime import datetime
from tkinter import ttk, messagebox
import os
import util.config as utl

class Informes:
    def __init__(self):
        super().__init__()
        #frame = ventana
        self.bd_seleccionada = ''  # Variable para almacenar la base de datos seleccionada
        self.fuenteb = utl.definir_fuente_bold()
        self.fuenten = utl.definir_fuente()
        #self.configurar_interfaz()

    def configurar_interfaz(self, frame):

        # Estilo de la tabla
        estilo_tabla = ttk.Style(frame)
        estilo_tabla.configure('Treeview.Heading', background='green', fg='black', padding=3, font=('Arial', 11, 'bold'))

        # Crear la tabla para mostrar las bases de datos
        self.tabla = ttk.Treeview(frame, columns=("Nombre", "Fecha"), show="headings", height=5)
        self.tabla.heading("Nombre", text="Nombre BD")
        self.tabla.heading("Fecha", text="Fecha de creación")
        self.tabla.column('Nombre', width= 300 , anchor= 'w')
        self.tabla.column('Fecha',  width= 200 , anchor= 'w')
        [frame.columnconfigure(i, weight= 1) for i in range(frame.grid_size()[0]-1)]
        self.tabla.grid(column= 0, row= 5, columnspan= 2, padx= (10,0), sticky= 'nsew')
        ladoy = ttk.Scrollbar(frame, orient ='vertical', command = self.tabla.yview)
        ladoy.grid(column = 3, row = 5, sticky='ns')

        # Bind para seleccionar la base de datos desde la tabla
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_desde_tabla)

        # Listar las bases de datos en la tabla
        #self.listar_bases_datos()
        btn_cargar_copia = tk.Button(frame, text="Cargar copia de seguridad", fg= 'white', font = self.fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, command=self.crear_backup)
        btn_cargar_copia.grid(column= 0, row=6, padx=(10, 10), pady=(10, 10))

        # Botón para crear una copia de seguridad
        btn_guardar_copia = tk.Button(frame, text="Crear copia de seguridad", fg= 'white', font = self.fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, command=self.crear_backup)
        btn_guardar_copia.grid(column= 1, row=6, padx=(10, 10), pady=(10, 10))

    def crear_backup(self):
        if not self.bd_seleccionada:
            messagebox.showwarning("Advertencia", "Debe seleccionar una base de datos primero.")
            return

        #print('Crear backup de:', self.bd_seleccionada)

        carpeta_script = os.path.dirname(__file__)  # Obtener la ruta del script
        #print('carpeta',carpeta_script)
        fecha_actual = datetime.now().strftime("%Y%m%d%H%M")
        nombre = 'consultorioMyM'
        
        # Ruta del archivo original
        ruta_original = os.path.join(carpeta_script, self.bd_seleccionada)
        
        base_nombre = f"{nombre}_{fecha_actual}.sqlite3"

        # Crear la ruta para la copia en la misma carpeta con otro nombre
        ruta_copia = os.path.join(carpeta_script, base_nombre)
        
        # Copiar el archivo
        try:
            shutil.copy(ruta_original, ruta_copia)
            #print(f"Archivo copiado de {ruta_original} a {ruta_copia}")
            messagebox.showinfo("Éxito", f"Backup creado: {ruta_copia}")
            self.listar_bases_datos()  # Actualizar la tabla con las nuevas bases de datos
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el backup: {e}")

    def listar_bases_datos(self):
        carpeta_origen = os.path.dirname(__file__)  # Obtener la carpeta donde está el script
        #print('carpeta origen', carpeta_origen)
        bases_datos = [f for f in os.listdir(carpeta_origen) if f.endswith(".sqlite3")]
        #print(bases_datos)

        # Limpiar la tabla si ya tiene datos
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        
        # Insertar las bases de datos en la tabla
        for _, base_datos in enumerate(bases_datos):
            ruta_copia = os.path.join(carpeta_origen, base_datos)
            fecha_creacion = datetime.fromtimestamp(os.path.getctime(ruta_copia)).strftime('%Y-%m-%d %H:%M:%S')
            self.tabla.insert("", "end", values=(base_datos.split('.')[0], fecha_creacion))

        if not bases_datos:
            messagebox.showinfo("Información", "No se encontraron bases de datos en la carpeta seleccionada.")

    def seleccionar_desde_tabla(self, event):
        selected_item = self.tabla.selection()
        if selected_item:
            item = self.tabla.item(selected_item)
            seleccion=item['values'][0]
            self.bd_seleccionada =  seleccion+'.sqlite3' # Guardar el nombre de la base de datos seleccionada
# # Función para obtener los datos agrupados por mes y año
# def obtener_datos_por_mes_anio():
#     # Conexión a la base de datos (ajusta la ruta si usas sqlite)
#     conn = sqlite3.connect('consultorio2.sqlite3')
#     cursor = conn.cursor()

#     # Consulta SQL para agrupar por mes y año (en formato YYYY-MM)
#     cursor.execute("""
#         SELECT strftime('%m', fecha) AS mes_anio, COUNT(*)
#         FROM turnos
#         GROUP BY mes_anio
#     """)
#     datos = cursor.fetchall()

#     conn.close()
#     return datos

# def graficar_en_nueva_ventana():
#     # Crear una nueva ventana
#     nueva_ventana = tk.Toplevel(ventana)
#     nueva_ventana.title('Gráfico de Turnos')

#     # Frame para el gráfico en la nueva ventana
#     frame_grafico = tk.Frame(nueva_ventana)
#     frame_grafico.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

#     # Obtener los datos de la base de datos
#     datos = obtener_datos_por_mes_anio()

#     # Procesar los datos para graficar
#     meses_anios = [fila[0] for fila in datos]
#     conteos = [fila[1] for fila in datos]

#     # Crear la figura
#     fig, ax = plt.subplots()
#     ax.bar(meses_anios, conteos, color='skyblue')  # Gráfico de barras
#     ax.set_xlabel('Meses y Años')
#     ax.set_ylabel('Cantidad de turnos')
#     ax.set_title('Turnos por Mes y Año')

#     # Ajustar los ticks del eje X para que no se solapen
#     plt.xticks(rotation=45, ha='right')

#     # Crear el canvas de matplotlib en Tkinter y asignarlo al frame de la nueva ventana
#     canvas = FigureCanvasTkAgg(fig, frame_grafico)
#     canvas.draw()
#     canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

#     # Cerrar los recursos de la figura
#     plt.close(fig)
#     boton_pdf = tk.Button(nueva_ventana, text="Guardar Gráfico como PDF", command=lambda: guardar_grafico_pdf(fig))
#     boton_pdf.pack(side=tk.BOTTOM, pady=10)

# # Función para guardar el gráfico como un PDF
# def guardar_grafico_pdf(fig):
#     # Pedir al usuario que elija dónde guardar el archivo
#     file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

#     if file_path:
#         # Guardar la figura de matplotlib como una imagen temporal
#         imagen_temporal = "grafico_temporal.png"
#         fig.savefig(imagen_temporal)

#         # Crear el PDF con reportlab
#         c = pdf_canvas.Canvas(file_path, pagesize=letter)
#         c.drawString(100, 750, "Gráfico de Turnos por Mes y Año")

#         # Cargar la imagen temporal
#         img = Image.open(imagen_temporal)
#         img_width, img_height = img.size

#         # Ajustar la imagen en el tamaño de la página del PDF
#         max_width = 500
#         max_height = 400
#         scale = min(max_width / img_width, max_height / img_height)
#         new_width = int(img_width * scale)
#         new_height = int(img_height * scale)

#         # Insertar la imagen en el PDF
#         c.drawImage(imagen_temporal, 50, 300, new_width, new_height)

#         # Guardar y cerrar el PDF
#         c.save()

#         # Eliminar la imagen temporal
#         img.close()

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
