#import sqlite3
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import os
import util.config as utl

class Backup:
    def __init__(self):
        super().__init__()
        self.bd_seleccionada = ''  # Variable para almacenar la base de datos seleccionada
        self.fuenteb = utl.definir_fuente_bold()
        self.fuenten = utl.definir_fuente()

    def configurar_interfaz(self, frame):
        # Estilo de la tabla
        self.estilo_tablab = ttk.Style(frame)
        self.estilo_tablab.theme_use('alt')
        self.estilo_tablab.configure('TablaBackup.Treeview', font= self.fuenten, foreground= 'black', rowheight= 20)
        self.estilo_tablab.configure('TablaBackup.Treeview.Heading', background= '#1F704B', foreground= 'white', padding= 3, font= self.fuenteb)

        # Crear la tabla para mostrar las bases de datos
        self.tabla = ttk.Treeview(frame, columns=("Nombre", "Fecha"), show="headings", height=4, style="TablaBackup.Treeview")
        self.tabla.heading("Nombre", text="Nombre BD")
        self.tabla.heading("Fecha", text="Fecha de creación")
        self.tabla.column('Nombre', width= 350 , anchor= 'w')
        self.tabla.column('Fecha',  width= 200 , anchor= 'w')
        [frame.columnconfigure(i, weight= 1) for i in range(frame.grid_size()[0]-1)]
        self.tabla.grid(column= 0, row= 2, columnspan= 2, padx= (10,0), sticky= 'nsew')
        ladoy = ttk.Scrollbar(frame, orient ='vertical', command = self.tabla.yview)
        ladoy.grid(column = 3, row = 2, sticky='ns')

        # Bind para seleccionar la base de datos desde la tabla
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_desde_tabla)

        # Listar las bases de datos en la tabla
        self.frame_botones = tk.Frame(frame)
        self.frame_botones.grid(column= 0, row= 3)
        btn_cargar_copia = tk.Button(self.frame_botones, text="Cargar copia de seguridad", fg= 'white', font = self.fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, command=self.crear_backup)
        btn_cargar_copia.grid(column= 0, row=0, padx=(10, 10), pady=(10, 10))

        # Botón para crear una copia de seguridad
        btn_guardar_copia = tk.Button(self.frame_botones, text="Crear copia de seguridad", fg= 'white', font = self.fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, command=self.crear_backup)
        btn_guardar_copia.grid(column= 2, row=0, padx=(10, 10), pady=(10, 10))

    def crear_backup(self):
        if not self.bd_seleccionada:
            messagebox.showwarning("Advertencia", "Debe seleccionar una base de datos primero")
            return

        carpeta_script = os.path.dirname(__file__)  # Obtener la ruta del script
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
            messagebox.showinfo("Éxito", f"Backup creado: {ruta_copia}")
            self.listar_bases_datos()  # Actualizar la tabla con las nuevas bases de datos
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el backup: {e}")

    def listar_bases_datos(self):
        carpeta_origen = os.path.dirname(__file__)  # Obtener la carpeta donde está el script
        bases_datos = [f for f in os.listdir(carpeta_origen) if f.endswith(".sqlite3")]

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