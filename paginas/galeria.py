from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import util.config as utl
from bd.conexion import Conexion
from tkinter import *
import os

class Galeria:
    def __init__(self, dni):
        super().__init__()
        self.bd_seleccionada = ''  # Variable para almacenar la base de datos seleccionada
        self.fuenteb = utl.definir_fuente_bold()
        self.fuenten = utl.definir_fuente()
        #print("Galeria")
        self.dni_paciente = StringVar()
        self.db = Conexion()
        self.miConexion = self.db.conectar()
        self.folder_path = "imagenes/"+str(dni)
        print(self.folder_path)
        try:
            if not os.path.exists(self.folder_path):
                answer = messagebox.askokcancel(title= 'Crear carpeta', message= '¿Desea crear la galeria?', icon= 'warning')
                if answer:
                    os.makedirs(self.folder_path)
                else:
                    return
            else:
                print("carpeta abierta")
        except:
            print("error")
        self.lista_imagenes = []
        self.indice_actual = 0
        self.miniaturas_botones = []
        self.miniaturas_imagenes = []
        self.nivel_zoom = 1.0  # 1.0 = 100%
        #self.zoom_factors = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0, 4.0]
        self.posicion_imagen = [0, 0]  # Para el desplazamiento de imagen con zoom

    def ventana_gal(self):
        self.ventana_galeria= tk.Toplevel()
        self.ventana_galeria.grab_set_global() # Obliga a las ventanas estar deshabilitadas y deshabilitar todos los eventos e interacciones con la ventana
        self.ventana_galeria.focus_set() # Mantiene el foco cuando se abre la ventana.
        self.ventana_galeria.geometry('750x500')
        self.ventana_galeria.grid_columnconfigure(0, weight= 1)
        self.ventana_galeria.configure(bg= "gray")
        utl.centrar_ventana(self.ventana_galeria, 900, 500)
        self.fecha_actual = datetime.now().date()
        self.fecha_actual = self.fecha_actual.strftime("%d-%m-%Y")
        Label(self.ventana_galeria, text= 'GALERIA', font= 'Arial 20 bold', bg= "gray", fg= 'white').grid(column= 0, row= 0)

        apellido= self.paciente[0]
        nombre= self.paciente[1]
        dni= self.paciente[2]
        fechanac= self.convertir_fecha(self.paciente[3])
        obra_social= self.paciente[4]
        nrosocio= self.paciente[5]
        #print(nombre, apellido, obra_social, dni)
        self.frame_datos_paciente=Frame(self.ventana_galeria, border= 1, borderwidth= 2, bg= "gray90")
        self.frame_datos_paciente.grid(column= 0, row= 1, sticky= "nsew")
        Label(self.frame_datos_paciente, text= 'Nombre Completo:', font= self.fuenteb, bg= "gray90").grid(column= 0, row= 0, sticky= 'e', padx= (5, 0))
        Label(self.frame_datos_paciente, text= apellido+', '+nombre, font= self.fuenten, bg= "gray90").grid(column= 1, row= 0, sticky= 'w', padx= (0, 10))
        Label(self.frame_datos_paciente, text= 'D.N.I.:', font= self.fuenteb, bg= "gray90").grid(column= 2, row= 0, sticky= 'e', padx= (5, 0))
        Label(self.frame_datos_paciente, text= dni, font= self.fuenten, bg= "gray90").grid(column= 3, row= 0, sticky= 'w', padx= (0, 10))
        Label(self.frame_datos_paciente, text= 'Fecha de nacimiento:', font= self.fuenteb, bg= "gray90").grid(column= 4, row= 0, sticky= 'e', padx= (5, 0))
        Label(self.frame_datos_paciente, text= fechanac, font= self.fuenten, bg= "gray90").grid(column= 5, row= 0, sticky= 'w', padx= (0, 10))
        Label(self.frame_datos_paciente, text= 'Obra Social: ',  font= self.fuenteb, bg= "gray90").grid(column= 0, row= 1, sticky= 'e', padx= (5, 0))
        Label(self.frame_datos_paciente, text= obra_social, font= self.fuenten, bg= "gray90").grid(column= 1, row= 1, sticky= 'w', padx= (0, 10))
        Label(self.frame_datos_paciente, text= 'Nº socio: ',  font= self.fuenteb, bg= "gray90").grid(column= 2, row= 1, sticky= 'e', padx= (5, 0))
        Label(self.frame_datos_paciente, text= nrosocio, font= self.fuenten, bg= "gray90").grid(column= 3, row= 1, sticky= 'w', padx= (0, 10))
        self.ancho = 700
        self.create_widgets()
        self.frame_dientes = Frame(self.ventana_galeria)
        self.frame_dientes.grid(column= 0, row= 3, pady= (10, 10))
        self.canvas = tk.Canvas(self.frame_dientes, width= self.ancho-20, height= 300)
        self.canvas.grid(row= 0, column= 0,columnspan=3, padx= 10)
       
        # self.boton_guardar_odonto=Button(self.frame_dientes, text= 'Guardar', command= self.guardar_odontograma, font= self.fuenteb, bg= '#1F704B', fg= 'white', width= 8)
        # self.boton_guardar_odonto.grid(row= 1, column= 0, padx= 10, pady= 10)
        # self.boton_PDF=Button(self.frame_dientes, text= 'Crear PDF', command= self.crear_pdf, font= self.fuenteb, bg= "gray", width= 8)
        # self.boton_PDF.grid(row= 1, column= 1, padx= 0)
        self.boton_salir_odonto=Button(self.frame_dientes, text= 'Salir', command= self.salir, font= self.fuenteb, bg= "orange", width= 8)
        self.boton_salir_odonto.grid(row= 1, column= 2, padx= (0, 10))
        self.ventana_galeria.mainloop()
        
    def cargar_paciente(self, dni):
        self.dni_paciente = dni
        try:
            #self.miConexion=sqlite3.connect("./bd/DBpaciente.sqlite3")
            self.miCursor=self.miConexion.cursor()
            self.miCursor.execute("SELECT apellido, nombre, ID, fechanacimiento, obrasocial, nrosocio FROM Pacientes WHERE ID=?", (dni,))
            self.paciente = self.miCursor.fetchone()
            self.miConexion.commit()
            #print(self.paciente)
        except:
            messagebox.showinfo("Paciente", "No se cargo el paciente")

    def convertir_fecha(self, fecha):
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
        fecha_date = fecha_obj.date()
        return fecha_date.strftime("%d-%m-%Y")
    
    def salir(self):
        answer = messagebox.askokcancel(title= 'Salir', message= '¿Desea salir sin guardar?', icon= 'warning')
        if answer:            
            self.ventana_galeria.destroy()
    
    def create_widgets(self):
        # Frame principal
        self.frame_visor = tk.Frame(self.ventana_galeria)
        self.frame_visor.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame superior para la imagen principal
        self.frame_imagen = tk.Frame(self.frame_visor)
        self.frame_imagen.pack(fill=tk.BOTH, expand=True)

        # Canvas para mostrar la imagen principal con scrollbars
        self.canvas = tk.Canvas(self.frame_imagen, bg='gray', width=600, height=400)
        self.h_scroll = tk.Scrollbar(self.frame_imagen, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.v_scroll = tk.Scrollbar(self.frame_imagen, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)

        # Grid layout para canvas y scrollbars
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.h_scroll.grid(row=1, column=0, sticky="ew")
        self.frame_imagen.grid_rowconfigure(0, weight=1)
        self.frame_imagen.grid_columnconfigure(0, weight=1)

        # # Configurar eventos para zoom con rueda del mouse
        # self.canvas.bind("<MouseWheel>", self.zoom_rueda_mouse)
        # self.canvas.bind("<ButtonPress-1>", self.start_pan)
        # self.canvas.bind("<B1-Motion>", self.mover_imagen)
        # self.canvas.bind("<Configure>", self.reset_image_position)
        
        # Etiqueta para información de la imagen y zoom
        self.info_label = tk.Label(self.frame_visor, text="", anchor=tk.W)
        self.info_label.pack(fill=tk.X)
        
        # Frame para controles
        self.control_frame = tk.Frame(self.frame_visor)
        self.control_frame.pack(fill=tk.X, pady=5)

        # # Botones de navegación
        # self.prev_btn = tk.Button(self.control_frame, text="Anterior", command=self.imagen_anterior)
        # self.prev_btn.pack(side=tk.LEFT, padx=5)

        # self.next_btn = tk.Button(self.control_frame, text="Siguiente", command=self.next_image)
        # self.next_btn.pack(side=tk.LEFT, padx=5)

        # # Controles de zoom
        # self.zoom_out_btn = tk.Button(self.control_frame, text="Zoom -", command=lambda: self.ajustar_zoom(-0.25))
        # self.zoom_out_btn.pack(side=tk.LEFT, padx=5)

        # self.zoom_in_btn = tk.Button(self.control_frame, text="Zoom +", command=lambda: self.ajustar_zoom(0.25))
        # self.zoom_in_btn.pack(side=tk.LEFT, padx=5)

        # self.zoom_reset_btn = tk.Button(self.control_frame, text="Zoom 100%", command=self.resetear_zoom)
        # self.zoom_reset_btn.pack(side=tk.LEFT, padx=5)

        # # Botón para agregar imagen
        # self.add_btn = tk.Button(self.control_frame, text="Agregar Imagen", command=self.add_image)
        # self.add_btn.pack(side=tk.LEFT, padx=5)

        # # Botón para eliminar imagen
        # self.del_btn = tk.Button(self.control_frame, text="Eliminar Imagen", command=self.delete_image)
        # self.del_btn.pack(side=tk.LEFT, padx=5)

        # # Botón para ver metadatos
        # self.meta_btn = tk.Button(self.control_frame, text="Ver Metadatos", command=self.show_metadata)
        # self.meta_btn.pack(side=tk.LEFT, padx=5)

        # Frame para miniaturas con scrollbar
        self.thumbnail_frame = tk.Frame(self.frame_visor)
        self.thumbnail_frame.pack(fill=tk.X, pady=(5, 15))

        # Canvas para miniaturas con scrollbar horizontal
        self.thumbnail_canvas = tk.Canvas(self.thumbnail_frame, height=90)
        self.thumbnail_scroll = tk.Scrollbar(self.thumbnail_frame, orient=tk.HORIZONTAL,
                                           command=self.thumbnail_canvas.xview)
        self.thumbnail_canvas.configure(xscrollcommand=self.thumbnail_scroll.set)

        self.thumbnail_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.thumbnail_canvas.pack(side=tk.TOP, fill=tk.X)

        # Frame interno para las miniaturas
        self.thumbnails_inner_frame = tk.Frame(self.thumbnail_canvas)
        self.thumbnail_canvas.create_window((0, 0), window=self.thumbnails_inner_frame, anchor='nw')

        # Configurar el evento de redimensionamiento
        #self.thumbnails_inner_frame.bind("<Configure>", self.on_thumbnail_frame_configure)    
    