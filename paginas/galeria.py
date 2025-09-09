from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, Frame
import util.config as utl
from bd.conexion import Conexion
from tkinter import *
from PIL import Image, ImageTk
import os

class Galeria:
    def __init__(self):
        super().__init__()
        self.fuenteb = utl.definir_fuente_bold()
        self.fuenten = utl.definir_fuente()
        self.imagen_zoom_mas = utl.leer_imagen('zoom-in.png', (38, 38))
        self.imagen_zoom_menos = utl.leer_imagen('zoom-out.png', (38, 38))
        self.imagen_zoom_100 = utl.leer_imagen('zoom-real.png', (38, 38))
        self.imagen_anterior_icono = utl.leer_imagen('imagen-anterior.png', (38, 38))
        self.imagen_siguiente_icono = utl.leer_imagen('imagen-siguiente.png', (38, 38))
        self.agregar_imagen_icono = utl.leer_imagen('agregar-imagen.png', (38, 38))
        self.eliminar_imagen_icono = utl.leer_imagen('eliminar-imagen.png', (38, 38))
        self.dni_paciente = StringVar()
        self.paciente = None
        self.ventana_galeria = None
        self.folder_name = ""
        self.folder_path = ""
        self.ancho= 900
        self.db = Conexion()
        self.miConexion = self.db.conectar()
        self.lista_imagenes = []
        self.indice_actual = 0
        self.miniaturas_botones = []
        self.miniaturas_imagenes = []
        self.color_fondo1, self.color_fondo2= utl.definir_color_fondo()
        self.nivel_zoom = 1.0  # 1.0 = 100%
        #self.zoom_factors = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0, 4.0]
        self.posicion_imagen = [0, 0]  # Para el desplazamiento de imagen con zoom

    def crear_carpeta(self, dni):
        self.folder_name = "galeria/"+str(dni)
        self.folder_path = os.path.abspath(self.folder_name)
        try:
            if not os.path.exists(self.folder_name):
                answer = messagebox.askokcancel('Crear carpeta', '¿Desea crear la galeria?', icon= 'warning')                
                if answer:
                    os.makedirs(self.folder_name)
                    messagebox.showinfo("Galeria", "Carpeta creada exitosamente")
                    return True
                else:
                    return False
            else:
                return True
        except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir la imagen: {e}")

    def ventana_gal(self):
        self.ventana_galeria= tk.Toplevel()
        self.ventana_galeria.grab_set() # Obliga a las ventanas estar deshabilitadas y deshabilitar todos los eventos e interacciones con la ventana
        self.ventana_galeria.focus_set() # Mantiene el foco cuando se abre la ventana.
        self.ventana_galeria.geometry('750x500')
        self.ventana_galeria.grid_columnconfigure(0, weight= 1)
        self.ventana_galeria.configure(bg= "gray")        
        utl.centrar_ventana(self.ventana_galeria, self.ancho, 600)
        self.ventana_galeria.resizable(False, False)
        self.fecha_actual = datetime.now().date()
        self.fecha_actual = self.fecha_actual.strftime("%d-%m-%Y")
        Label(self.ventana_galeria, text= 'GALERIA', font= 'Arial 20 bold', bg= "gray", fg= 'white').grid(column= 0, row= 0)

        apellido= self.paciente[0]
        nombre= self.paciente[1]
        dni= self.paciente[2]

        self.frame_datos_paciente= Frame(self.ventana_galeria, border= 1, borderwidth= 2, bg= "gray90")
        self.frame_datos_paciente.grid(column= 0, row= 1, sticky= "nsew", columnspan= 5)
        Label(self.frame_datos_paciente, text= 'Nombre Completo: ', font= self.fuenteb, bg= "gray90").grid(column= 0, row= 0, sticky= 'e', padx= (15, 0))
        Label(self.frame_datos_paciente, text= apellido+', '+ nombre, font= self.fuenten, bg= "gray90").grid(column= 1, row= 0, sticky= 'w', padx= (0, 20))
        Label(self.frame_datos_paciente, text= 'D.N.I.: ', font= self.fuenteb, bg= "gray90").grid(column= 2, row= 0, sticky= 'e', padx= (5, 0))
        Label(self.frame_datos_paciente, text= dni, font= self.fuenten, bg= "gray90").grid(column= 3, row= 0, sticky= 'w', padx= (0, 20))

        self.frame_visor= Frame(self.ventana_galeria, border= 1, borderwidth= 2, bg= "gray")
        self.frame_visor.grid(column= 0, row= 2)
        self.boton_salir_odonto= Button(self.frame_datos_paciente, text= 'Salir', command= self.salir, font= self.fuenteb, bg= "orange", width= 8)
        self.boton_salir_odonto.grid(row= 0, column= 4, padx= (300, 10), sticky= "e")

        self.create_widgets()
        self.cargar_imagenes()
        # Mostrar la primera imagen si existe
        def cargar_primera_imagen():
            if self.lista_imagenes:
                self.mostrar_imagen(0)
                self.cargar_miniaturas()
    
    # Programar la carga después de que la ventana esté visible
        self.ventana_galeria.after(100, cargar_primera_imagen)
        self.ventana_galeria.mainloop()

    def cargar_paciente(self, dni):
        self.dni_paciente = dni
        try:
            self.miCursor=self.miConexion.cursor()
            self.miCursor.execute("SELECT apellido, nombre, ID, fechanacimiento, obrasocial, nrosocio FROM Pacientes WHERE ID=?", (self.dni_paciente,))
            self.paciente = self.miCursor.fetchone()
            self.miConexion.commit()
        except:
            self.ventana_galeria.grab_release()
            messagebox.showinfo("Galeria", "No se cargo el paciente")
            self.ventana_galeria.focus_set()
            self.ventana_galeria.grab_set()

    def convertir_fecha(self, fecha):
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
        fecha_date = fecha_obj.date()
        return fecha_date.strftime("%d-%m-%Y")

    def salir(self):
        self.ventana_galeria.grab_release()
        answer = messagebox.askokcancel('Salir', '¿Desea salir sin guardar?', icon= 'warning', parent= self.ventana_galeria)        
        if answer:
            self.ventana_galeria.destroy()
        else: 
            self.ventana_galeria.focus_set()
            self.ventana_galeria.grab_set()

    def create_widgets(self):
        # Frame superior para la imagen principal
        self.frame_imagen = tk.Frame(self.frame_visor, bg= "gray90")
        self.frame_imagen.grid(column= 0, row= 0)
        self.frame_imagen.grid_columnconfigure(0, weight= 1)
        self.frame_imagen.grid_rowconfigure(0, weight= 1)
        
        # Canvas para mostrar la imagen principal con scrollbars
        self.canvas = tk.Canvas(self.frame_imagen, bg= 'black', width= self.ancho*0.97, height= 350)
        self.h_scroll = tk.Scrollbar(self.frame_imagen, orient= tk.HORIZONTAL, command= self.canvas.xview)
        self.v_scroll = tk.Scrollbar(self.frame_imagen, orient= tk.VERTICAL, command= self.canvas.yview)
        self.canvas.configure(xscrollcommand= self.h_scroll.set, yscrollcommand= self.v_scroll.set)

        # Grid layout para canvas y scrollbars
        self.canvas.grid(row= 0, column= 0, sticky= "nsew")
        self.v_scroll.grid(row= 0, column= 1, sticky= "ns")
        self.h_scroll.grid(row= 1, column= 0, sticky= "ew")

        # INICIALIZAR TEXTO INFORMATIVO (SOLO UNA VEZ)
        self.inicializar_texto_info()

        # Configurar eventos
        self.canvas.bind("<MouseWheel>", self.zoom_rueda_mouse)
        self.canvas.bind("<ButtonPress-1>", self.start_pan)
        self.canvas.bind("<B1-Motion>", self.mover_imagen)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Frame para controles
        self.control_frame = Frame(self.frame_imagen, bg= "gray")
        self.control_frame.grid(column= 0, row= 2, pady = (5, 5), sticky= "nsew", columnspan= 8)

        # Botones de navegación
        self.prev_btn = tk.Button(self.control_frame, image= self.imagen_anterior_icono, text= "Anterior", command= self.imagen_anterior, bg= self.color_fondo1)
        self.prev_btn.grid(column= 0, row= 0, padx= (150, 50), pady = (5, 5))

        self.next_btn = tk.Button(self.control_frame, image= self.imagen_siguiente_icono, text= "Siguiente", command= self.imagen_siguiente, bg= self.color_fondo1)
        self.next_btn.grid(column= 4, row= 0,  padx= (0, 100))

        # Controles de zoom
        self.zoom_out_btn = tk.Button(self.control_frame, image= self.imagen_zoom_menos, text= "Zoom -", command= lambda: self.ajustar_zoom(-0.25), bg= self.color_fondo1)
        self.zoom_out_btn.grid(column= 1, row= 0, padx= (0, 25))

        self.zoom_in_btn = tk.Button(self.control_frame, image= self.imagen_zoom_mas, text= "Zoom +", command= lambda: self.ajustar_zoom(0.25), bg= self.color_fondo1)
        self.zoom_in_btn.grid(column= 2, row= 0, padx= (0, 25))

        self.zoom_reset_btn = tk.Button(self.control_frame, image= self.imagen_zoom_100, text= "Zoom 100%", command= self.resetear_zoom, bg= self.color_fondo1)
        self.zoom_reset_btn.grid(column= 3, row= 0, padx= (0, 50))

        # Botón para agregar imagen
        self.add_btn = tk.Button(self.control_frame, image= self.agregar_imagen_icono, text= "Agregar Imagen", command= self.add_image, bg= self.color_fondo1)
        self.add_btn.grid(column= 5, row= 0,  padx= (0, 25))

        # Botón para eliminar imagen
        self.del_btn = tk.Button(self.control_frame, image= self.eliminar_imagen_icono, text= "Eliminar Imagen", command= self.delete_image, bg= self.color_fondo1)
        self.del_btn.grid(column= 6, row= 0)

        # Frame para miniaturas con scrollbar
        self.thumbnail_frame = tk.Frame(self.frame_imagen)
        self.thumbnail_frame.grid(column= 0, row= 3, sticky= "nsew")

        # Canvas para miniaturas con scrollbar horizontal
        self.thumbnail_canvas = tk.Canvas(self.thumbnail_frame, height= 50)
        self.thumbnail_scroll = tk.Scrollbar(self.thumbnail_frame, orient= tk.HORIZONTAL, command= self.thumbnail_canvas.xview)
        self.thumbnail_canvas.configure(xscrollcommand= self.thumbnail_scroll.set)
        self.thumbnail_scroll.pack(side= tk.BOTTOM, fill= tk.X)
        self.thumbnail_canvas.pack(side= tk.TOP, fill= tk.X)

        # Frame interno para las miniaturas
        self.thumbnails_inner_frame = tk.Frame(self.thumbnail_canvas)
        self.thumbnail_canvas.create_window((0, 0), window= self.thumbnails_inner_frame, anchor= 'nw')

        # Configurar el evento de redimensionamiento
        self.thumbnails_inner_frame.bind("<Configure>", self.on_thumbnail_frame_configure)
            
    def on_thumbnail_frame_configure(self, event):
        """Actualizar scrollregion cuando cambia el tamaño del frame de miniaturas"""
        self.thumbnail_canvas.configure(scrollregion= self.thumbnail_canvas.bbox("all"))

    def cargar_imagenes(self):
        self.lista_imagenes = []
        valid_extensions = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')

        for filename in os.listdir(self.folder_path):
            if filename.lower().endswith(valid_extensions):
                self.lista_imagenes.append(os.path.join(self.folder_path, filename))
        self.lista_imagenes.sort()

    def mostrar_imagen(self, index):
        if 0 <= index < len(self.lista_imagenes):
            self.indice_actual = index
            image_path = self.lista_imagenes[index]
            try:
                # Cargar la imagen original
                self.original_image = Image.open(image_path)
                # ESPERAR A QUE EL CANVAS ESTÉ DISPONIBLE
                self.canvas.update_idletasks()
                # OBTENER DIMENSIONES REALES DEL CANVAS
                canvas_width = max(1, self.canvas.winfo_width())
                canvas_height = max(1, self.canvas.winfo_height())
                if canvas_width <= 1 or canvas_height <= 1:
                    # SI EL CANVAS NO TIENE TAMAÑO, USAR ZOOM POR DEFECTO
                    self.nivel_zoom = 1.0
                else:
                    # CALCULAR ZOOM PARA AJUSTAR AL CANVAS (usar el 90% del espacio disponible)
                    img_width, img_height = self.original_image.size
                    # Calcular ratios manteniendo relación de aspecto
                    width_ratio = (canvas_width * 0.9) / img_width
                    height_ratio = (canvas_height * 0.9) / img_height
                    # Usar el ratio más pequeño para mantener la relación de aspecto
                    self.nivel_zoom = min(width_ratio, height_ratio, 1.0)
                self.posicion_imagen = [0, 0]
                # Aplicar zoom y actualizar
                self.apply_zoom()
                # ACTUALIZAR TEXTO INFORMATIVO
                self.actualizar_info_imagen()
                self.highlight_selected_thumbnail()            
            except Exception as e:
                self.ventana_galeria.grab_release()
                messagebox.showerror("Error", f"No se pudo abrir la imagen: {e}", parent=self.ventana_galeria)
                self.ventana_galeria.grab_set()               
            
    def apply_zoom(self):
        if hasattr(self, 'original_image'):
            try:
                width = max(1, int(self.original_image.width * self.nivel_zoom * 0.98))
                height = max(1, int(self.original_image.height * self.nivel_zoom * 0.98))

                self.imagen_actual = self.original_image.resize((width, height), Image.LANCZOS)
                self.tk_img = ImageTk.PhotoImage(self.imagen_actual)

                self.canvas.delete("all")

                # PRIMERO DIBUJAR LA IMAGEN
                x_pos = max(0, self.posicion_imagen[0])
                y_pos = max(0, self.posicion_imagen[1])
                self.image_on_canvas = self.canvas.create_image(x_pos, y_pos, anchor= tk.NW, image= self.tk_img)

                # LUEGO DIBUJAR EL TEXTO Y FONDO (SOBRE LA IMAGEN)
                self.inicializar_texto_info()

                self.canvas.configure(scrollregion=self.canvas.bbox("all"))

                # FORZAR QUE EL TEXTO ESTÉ SIEMPRE EN PRIMER PLANO
                self.canvas.tag_raise(self.info_text)
                self.canvas.tag_raise(self.info_bg)

                # ACTUALIZAR INFORMACIÓN
                self.actualizar_info_imagen()
                self.actualizar_posicion_texto()

            except Exception as e:
                self.ventana_galeria.grab_release()
                messagebox.showerror("Error", f"Error en apply_zoom: {e}", parent= self.ventana_galeria)
                self.ventana_galeria.focus_set()
                self.ventana_galeria.grab_set()

    def ajustar_zoom(self, factor_change):
        new_zoom = self.nivel_zoom + factor_change
        # Limitar el zoom entre 10% y 400%
        new_zoom = max(0.1, min(4.0, new_zoom))

        if new_zoom != self.nivel_zoom:
            self.nivel_zoom = new_zoom
            self.apply_zoom()

    def zoom_rueda_mouse(self, event):
        # Zoom in/out con la rueda del mouse
        if event.delta > 0:
            self.ajustar_zoom(0.25)
        else:
            self.ajustar_zoom(-0.25)

    def resetear_zoom(self):
        self.nivel_zoom = 1.0
        self.posicion_imagen = [0, 0]
        self.apply_zoom()

    def reset_image_position(self, event=None):
        """Centrar la imagen cuando se redimensiona el canvas"""
        if hasattr(self, 'original_image'):
            try:
                # ESPERAR A QUE EL CANVAS ESTÉ LISTO
                self.canvas.update_idletasks()
                
                canvas_width = max(1, self.canvas.winfo_width())
                canvas_height = max(1, self.canvas.winfo_height())
                
                if canvas_width <= 1 or canvas_height <= 1:
                    return  # Canvas no está listo aún
                    
                img_width = max(1, int(self.original_image.width * self.nivel_zoom))
                img_height = max(1, int(self.original_image.height * self.nivel_zoom))

                # Centrar la imagen si es más pequeña que el canvas
                if img_width < canvas_width and img_height < canvas_height:
                    self.posicion_imagen = [
                        max(0, (canvas_width - img_width) // 2),
                        max(0, (canvas_height - img_height) // 2)
                    ]
                else:
                    self.posicion_imagen = [0, 0]

                # VOLVER A APLICAR EL ZOOM CON LA NUEVA POSICIÓN
                self.apply_zoom()
            except Exception as e:
                self.ventana_galeria.grab_release()
                messagebox.showerror("Error", f"Error en reset_image_position: {e}", parent= self.ventana_galeria)
                self.ventana_galeria.focus_set()
                self.ventana_galeria.grab_set()

    def start_pan(self, event):
        """Iniciar el desplazamiento de la imagen"""
        self.pan_start_x = event.x
        self.pan_start_y = event.y

    def mover_imagen(self, event):
        """Mover la imagen con el mouse"""
        if hasattr(self, 'pan_start_x'):
            dx = event.x - self.pan_start_x
            dy = event.y - self.pan_start_y

            self.posicion_imagen[0] += dx
            self.posicion_imagen[1] += dy

            self.canvas.move(self.image_on_canvas, dx, dy)
            self.pan_start_x = event.x
            self.pan_start_y = event.y

    def cargar_miniaturas(self):
        # Limpiar miniaturas anteriores
        for widget in self.thumbnails_inner_frame.winfo_children():
            widget.destroy()

        self.miniaturas_botones = []
        self.miniaturas_imagenes = []

        # Crear miniaturas para cada imagen
        for idx, image_path in enumerate(self.lista_imagenes):
            try:
                # Crear miniatura
                imagen = Image.open(image_path)
                imagen.thumbnail((50, 50))

                # Convertir a PhotoImage
                thumb_img = ImageTk.PhotoImage(imagen)
                self.miniaturas_imagenes.append(thumb_img)

                # Crear botón con la miniatura
                btn = tk.Button(self.thumbnails_inner_frame, image= thumb_img, command= lambda i=idx: self.mostrar_imagen(i))
                btn.config(width= 50, height= 50)
                btn.pack(side=tk.LEFT, padx= 2, pady= 5)
                self.miniaturas_botones.append(btn)

            except Exception as e:
                self.ventana_galeria.grab_release()
                messagebox.showerror("Error", f"No se cargaron las miniaturas: {e}", parent= self.ventana_galeria)
                self.ventana_galeria.focus_set()
                self.ventana_galeria.grab_set()

        # Resaltar miniatura seleccionada
        self.highlight_selected_thumbnail()

    def highlight_selected_thumbnail(self):
        for i, btn in enumerate(self.miniaturas_botones):
            if i == self.indice_actual:
                btn.config(relief= tk.FLAT, bg= 'light blue')
            else:
                btn.config(relief= tk.FLAT, bg= 'SystemButtonFace')

    def imagen_anterior(self):
        if len(self.lista_imagenes) > 0:
            new_index = (self.indice_actual - 1) % len(self.lista_imagenes)
            self.mostrar_imagen(new_index)

    def imagen_siguiente(self):
        if len(self.lista_imagenes) > 0:
            new_index = (self.indice_actual + 1) % len(self.lista_imagenes)
            self.mostrar_imagen(new_index)

    def add_image(self):
        filetypes = (("Imágenes", "*.jpg *.jpeg *.png"), ("Todos los archivos", "*.*"))
        self.ventana_galeria.grab_release()

        file_path = filedialog.askopenfilename(title="Seleccionar imagen", filetypes= filetypes, parent= self.ventana_galeria)

        if file_path:
            try:
                # Verificar que sea una imagen válida
                with Image.open(file_path) as imagen:
                    pass

                # Copiar a la carpeta de imágenes
                filename = os.path.basename(file_path)
                dest_path = os.path.join(self.folder_path, filename)

                # Si el archivo ya existe, agregar timestamp
                if os.path.exists(dest_path):
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    name, ext = os.path.splitext(filename)
                    filename = f"{name}_{timestamp}{ext}"
                    dest_path = os.path.join(self.folder_path, filename)

                # Copiar el archivo
                with open(file_path, 'rb') as src, open(dest_path, 'wb') as dst:
                    dst.write(src.read())

                # Recargar imágenes y mostrar la nueva
                self.cargar_imagenes()
                self.mostrar_imagen(len(self.lista_imagenes) - 1)
                self.cargar_miniaturas()

                messagebox.showinfo("Éxito", "Imagen agregada correctamente", parent= self.ventana_galeria)
                self.ventana_galeria.focus_set()
                self.ventana_galeria.grab_set()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar la imagen: {e}", parent= self.ventana_galeria)
                self.ventana_galeria.focus_set()
                self.ventana_galeria.grab_set()
        self.ventana_galeria.focus_set()
        self.ventana_galeria.grab_set()

    def delete_image(self):
        if len(self.lista_imagenes) == 0:
            return

        imagen_actual = self.lista_imagenes[self.indice_actual]
        self.ventana_galeria.grab_release()
        confirm = messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar {os.path.basename(imagen_actual)}?", parent= self.ventana_galeria)

        if confirm:
            try:
                os.remove(imagen_actual)
                self.cargar_imagenes()

                if len(self.lista_imagenes) > 0:
                    new_index = min(self.indice_actual, len(self.lista_imagenes) - 1)
                    self.mostrar_imagen(new_index)
                else:
                    self.canvas.delete("all")
                    # self.info_label.config(text="No hay imágenes en la carpeta")
                    self.indice_actual = 0

                self.cargar_miniaturas()
                messagebox.showinfo("Éxito", "Imagen eliminada correctamente", parent= self.ventana_galeria)
                self.ventana_galeria.focus_set()
                self.ventana_galeria.grab_set()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la imagen: {e}", parent= self.ventana_galeria)
                self.ventana_galeria.focus_set()
                self.ventana_galeria.grab_set()
        self.ventana_galeria.focus_set()
        self.ventana_galeria.grab_set()

    def inicializar_texto_info(self):
        """Inicializar el texto informativo en el canvas"""
        # Crear texto inicial con posición temporal
        self.info_text = self.canvas.create_text(
            50, 50,  # Posición temporal
            text="Cargando...",
            fill="white",
            font=("Arial", 10, "bold"),
            anchor=tk.NW,
            tags="image_info"
        )
        
        # Crear fondo semitransparente
        self.info_bg = self.canvas.create_rectangle(
            45, 45, 55, 55,  # Posición temporal
            fill="#000000",    # Negro sólido
            outline="",        # Sin borde
            stipple="gray50",  # Patrón de transparencia (50% opacidad)
            tags="info_bg"
        )
        # PONER EL FONDO DETRÁS DEL TEXTO
        self.canvas.tag_lower(self.info_bg, self.info_text)
        # Programar posicionamiento correcto después de que el canvas esté listo
        self.ventana_galeria.after(500, self.actualizar_posicion_texto)

    def on_canvas_configure(self, event=None):
        """Manejar redimensionamiento del canvas"""
        try:
            self.actualizar_posicion_texto()
            if hasattr(self, 'original_image'):
                # ESPERAR UN MOMENTO ANTES DE REAJUSTAR (evita flickering)
                self.ventana_galeria.after(100, self.reset_image_position)
        except Exception as e:
            self.ventana_galeria.grab_release()
            messagebox.showerror("Error", f"Error en on_canvas_configure: {e}", parent= self.ventana_galeria)
            self.ventana_galeria.focus_set()
            self.ventana_galeria.grab_set()

    def actualizar_posicion_texto(self, event=None):
        """Posicionar texto en esquina INFERIOR DERECHA"""
        try:
            self.canvas.update_idletasks()
            canvas_width = max(1, self.canvas.winfo_width())
            canvas_height = max(1, self.canvas.winfo_height())

            if canvas_width > 50 and canvas_height > 50:
                # ESQUINA INFERIOR DERECHA
                text_x = canvas_width - 15
                text_y = canvas_height - 15

                # Actualizar posición del texto
                self.canvas.coords(self.info_text, text_x, text_y)
                self.canvas.itemconfig(self.info_text, anchor=tk.SE)

                # AJUSTAR FONDO SEMITRANSPARENTE AL TEXTO
                bbox = self.canvas.bbox(self.info_text)
                if bbox:
                    # Agregar márgenes más generosos
                    padding_x = 12
                    padding_y = 8

                    self.canvas.coords(
                        self.info_bg,
                        bbox[0] - padding_x, 
                        bbox[1] - padding_y,
                        bbox[2] + padding_x, 
                        bbox[3] + padding_y
                    )

                    # ASEGURAR QUE EL FONDO ESTÉ DETRÁS DEL TEXTO
                    self.canvas.tag_lower(self.info_bg, self.info_text)

            # Reintentar si el canvas es muy pequeño
            elif canvas_width <= 50 or canvas_height <= 50:
                self.ventana_galeria.after(100, self.actualizar_posicion_texto)
        except Exception as e:
            self.ventana_galeria.grab_release()
            messagebox.showerror("Error", f"Error en  posicionando texto: {e}", parent= self.ventana_galeria)
            self.ventana_galeria.focus_set()
            self.ventana_galeria.grab_set()

    def actualizar_info_imagen(self):
        """Actualizar el contenido del texto informativo"""
        try:
            if (hasattr(self, 'lista_imagenes') and 
                self.lista_imagenes and 
                0 <= self.indice_actual < len(self.lista_imagenes)):

                image_path = self.lista_imagenes[self.indice_actual]
                filename = os.path.basename(image_path)

                # Obtener fecha de modificación
                try:
                    mod_time = os.path.getmtime(image_path)
                    file_date = datetime.fromtimestamp(mod_time).strftime("%d/%m/%Y %H:%M")
                except:
                    file_date = "Fecha desconocida"

                # FORMATEAR ZOOM CON 0 DECIMALES
                zoom_percent = int(round(self.nivel_zoom * 100))
                info_text = f"{filename}\n{file_date}\nZoom: {zoom_percent}%"

                # Actualizar texto en canvas
                self.canvas.itemconfig(self.info_text, text=info_text)

                # Forzar actualización de posición
                self.actualizar_posicion_texto()

        except Exception as e:
            self.ventana_galeria.grab_release()
            messagebox.showerror("Error", f"Error actualizando info imagen: {e}", parent= self.ventana_galeria)
            self.ventana_galeria.focus_set()
            self.ventana_galeria.grab_set()