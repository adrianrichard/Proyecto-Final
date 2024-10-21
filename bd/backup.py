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
        #frame = ventana
        self.bd_seleccionada = ''  # Variable para almacenar la base de datos seleccionada
        self.fuenteb = utl.definir_fuente_bold()
        self.fuenten = utl.definir_fuente()
        #self.configurar_interfaz()

    def configurar_interfaz(self, frame):
        # frame.title("Gestión de Base de Datos")
        # frame.geometry("500x400")

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
        self.tabla.grid(column= 0, row= 2, columnspan= 2, padx= (10,0), sticky= 'nsew')
        ladoy = ttk.Scrollbar(frame, orient ='vertical', command = self.tabla.yview)
        ladoy.grid(column = 3, row = 2, sticky='ns')

        # Bind para seleccionar la base de datos desde la tabla
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_desde_tabla)

        # Listar las bases de datos en la tabla
        #self.listar_bases_datos()
        btn_cargar_copia = tk.Button(frame, text="Cargar copia de seguridad", fg= 'white', font = self.fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, command=self.crear_backup)
        btn_cargar_copia.grid(column= 0, row=3, padx=(10, 10), pady=(10, 10))

        # Botón para crear una copia de seguridad
        btn_guardar_copia = tk.Button(frame, text="Crear copia de seguridad", fg= 'white', font = self.fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, command=self.crear_backup)
        btn_guardar_copia.grid(column= 1, row=3, padx=(10, 10), pady=(10, 10))

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
            #print(f"Base de datos seleccionada: {self.bd_seleccionada}")

# # Crear la ventana principal
# ventana = tk.Tk()

# # Crear instancia de la clase Backup
# backup = Backup(ventana)

# # Iniciar el loop principal de la interfaz
# ventana.mainloop()