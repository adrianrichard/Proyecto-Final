from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import util.config as utl

class Galeria:
    def __init__(self):
        super().__init__()
        self.bd_seleccionada = ''  # Variable para almacenar la base de datos seleccionada
        self.fuenteb = utl.definir_fuente_bold()
        self.fuenten = utl.definir_fuente()
        print("Galeria")

    def configurar_interfaz(self, frame):
        # Estilo de la tabla
        self.estilo_tablab = ttk.Style(frame)
        self.estilo_tablab.theme_use('alt')
        self.estilo_tablab.configure('TablaBackup.Treeview', font= self.fuenten, foreground= 'black', rowheight= 20)
        self.estilo_tablab.configure('TablaBackup.Treeview.Heading', background= '#1F704B', foreground= 'white', padding= 3, font= self.fuenteb)

        # Crear la tabla para mostrar las bases de datos
        self.tabla = ttk.Treeview(frame, columns=("Nombre", "Fecha"), show="headings", height=8, style="TablaBackup.Treeview")
        self.tabla.heading("Nombre", text="Nombre BD")
        self.tabla.heading("Fecha", text="Fecha de creación")
        self.tabla.column('Nombre', width= 350 , anchor= 'w')
        self.tabla.column('Fecha',  width= 200 , anchor= 'w')
        [frame.columnconfigure(i, weight= 1) for i in range(frame.grid_size()[0]-1)]
        self.tabla.grid(column= 0, row= 2, columnspan= 2, padx= (10, 0), sticky= 'nsew')
        ladoy = ttk.Scrollbar(frame, orient ='vertical', command = self.tabla.yview)
        ladoy.grid(column = 3, row = 2, sticky='ns')

        # Bind para seleccionar la base de datos desde la tabla
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_desde_tabla)

        # Listar las bases de datos en la tabla
        self.frame_botones = tk.Frame(frame, bg='gray90')
        self.frame_botones.grid(column= 0, row= 3)
        btn_cargar_copia = tk.Button(self.frame_botones, text="Cargar copia de seguridad", fg= 'white', font = self.fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, command=self.crear_backup)
        btn_cargar_copia.grid(column= 0, row=0, padx=(10, 10), pady=(10, 10))

        # Botón para crear una copia de seguridad
        btn_guardar_copia = tk.Button(self.frame_botones, text="Crear copia de seguridad", fg= 'white', font = self.fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, command=self.crear_backup)
        btn_guardar_copia.grid(column= 2, row=0, padx=(10, 10), pady=(10, 10))
