import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ExifTags
from datetime import datetime

class ImageViewer:
    def __init__(self, root, folder_path):
        self.root = root
        self.root.title("Visualizador de Imágenes con Zoom")

        # Configurar la carpeta de imágenes
        self.folder_path = folder_path
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

        # Variables
        self.image_list = []
        self.current_index = 0
        self.thumbnail_buttons = []
        self.thumbnail_images = []
        self.zoom_level = 1.0  # 1.0 = 100%
        self.zoom_factors = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0, 4.0]
        self.image_position = [0, 0]  # Para el desplazamiento de imagen con zoom

        # Crear widgets
        self.create_widgets()

        # Cargar imágenes
        self.load_images()

        # Mostrar la primera imagen si existe
        if self.image_list:
            self.show_image(0)
            self.update_thumbnails()

    def create_widgets(self):
        # Frame principal
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame superior para la imagen principal
        self.image_frame = tk.Frame(self.main_frame)
        self.image_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas para mostrar la imagen principal con scrollbars
        self.canvas = tk.Canvas(self.image_frame, bg='white', width=600, height=400)
        self.h_scroll = tk.Scrollbar(self.image_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.v_scroll = tk.Scrollbar(self.image_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)

        # Grid layout para canvas y scrollbars
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.h_scroll.grid(row=1, column=0, sticky="ew")
        self.image_frame.grid_rowconfigure(0, weight=1)
        self.image_frame.grid_columnconfigure(0, weight=1)

        # Configurar eventos para zoom con rueda del mouse
        self.canvas.bind("<MouseWheel>", self.zoom_with_wheel)
        self.canvas.bind("<ButtonPress-1>", self.start_pan)
        self.canvas.bind("<B1-Motion>", self.pan_image)
        self.canvas.bind("<Configure>", self.reset_image_position)

        # Frame para controles
        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.pack(fill=tk.X, pady=5)

        # Botones de navegación
        self.prev_btn = tk.Button(self.control_frame, text="Anterior", command=self.prev_image)
        self.prev_btn.pack(side=tk.LEFT, padx=5)

        self.next_btn = tk.Button(self.control_frame, text="Siguiente", command=self.next_image)
        self.next_btn.pack(side=tk.LEFT, padx=5)

        # Controles de zoom
        self.zoom_out_btn = tk.Button(self.control_frame, text="Zoom -", command=lambda: self.adjust_zoom(-0.25))
        self.zoom_out_btn.pack(side=tk.LEFT, padx=5)

        self.zoom_in_btn = tk.Button(self.control_frame, text="Zoom +", command=lambda: self.adjust_zoom(0.25))
        self.zoom_in_btn.pack(side=tk.LEFT, padx=5)

        self.zoom_reset_btn = tk.Button(self.control_frame, text="Zoom 100%", command=self.reset_zoom)
        self.zoom_reset_btn.pack(side=tk.LEFT, padx=5)

        # Botón para agregar imagen
        self.add_btn = tk.Button(self.control_frame, text="Agregar Imagen", command=self.add_image)
        self.add_btn.pack(side=tk.LEFT, padx=5)

        # Botón para eliminar imagen
        self.del_btn = tk.Button(self.control_frame, text="Eliminar Imagen", command=self.delete_image)
        self.del_btn.pack(side=tk.LEFT, padx=5)

        # Botón para ver metadatos
        self.meta_btn = tk.Button(self.control_frame, text="Ver Metadatos", command=self.show_metadata)
        self.meta_btn.pack(side=tk.LEFT, padx=5)

        # Etiqueta para información de la imagen y zoom
        self.info_label = tk.Label(self.main_frame, text="", anchor=tk.W)
        self.info_label.pack(fill=tk.X)

        # Frame para miniaturas con scrollbar
        self.thumbnail_frame = tk.Frame(self.main_frame)
        self.thumbnail_frame.pack(fill=tk.X, pady=5)

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
        self.thumbnails_inner_frame.bind("<Configure>", self.on_thumbnail_frame_configure)

    def on_thumbnail_frame_configure(self, event):
        """Actualizar scrollregion cuando cambia el tamaño del frame de miniaturas"""
        self.thumbnail_canvas.configure(scrollregion=self.thumbnail_canvas.bbox("all"))

    def load_images(self):
        self.image_list = []
        valid_extensions = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')

        for filename in os.listdir(self.folder_path):
            if filename.lower().endswith(valid_extensions):
                self.image_list.append(os.path.join(self.folder_path, filename))

        self.image_list.sort()

    def show_image(self, index):
        if 0 <= index < len(self.image_list):
            self.current_index = index
            image_path = self.image_list[index]

            try:
                # Cargar la imagen original
                self.original_image = Image.open(image_path)
                self.current_image = self.original_image.copy()

                # Aplicar el zoom actual
                self.apply_zoom()

                # Actualizar información
                self.info_label.config(
                    text=f"Imagen {index + 1} de {len(self.image_list)}: {os.path.basename(image_path)} | Zoom: {int(self.zoom_level*100)}%"
                )

                # Resaltar miniatura seleccionada
                self.highlight_selected_thumbnail()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir la imagen: {e}")

    def apply_zoom(self):
        if hasattr(self, 'original_image'):
            # Calcular nuevo tamaño
            width = int(self.original_image.width * self.zoom_level)
            height = int(self.original_image.height * self.zoom_level)

            # Redimensionar la imagen
            self.current_image = self.original_image.resize((width, height), Image.LANCZOS)

            # Mostrar en canvas
            self.tk_img = ImageTk.PhotoImage(self.current_image)
            self.canvas.delete("all")
            self.image_on_canvas = self.canvas.create_image(
                self.image_position[0],
                self.image_position[1],
                anchor=tk.NW,
                image=self.tk_img
            )

            # Actualizar scrollregion
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def adjust_zoom(self, factor_change):
        new_zoom = self.zoom_level + factor_change
        # Limitar el zoom entre 10% y 400%
        new_zoom = max(0.1, min(4.0, new_zoom))

        if new_zoom != self.zoom_level:
            self.zoom_level = new_zoom
            self.apply_zoom()
            self.update_info_label()

    def zoom_with_wheel(self, event):
        # Zoom in/out con la rueda del mouse
        if event.delta > 0:
            self.adjust_zoom(0.25)
        else:
            self.adjust_zoom(-0.25)

    def reset_zoom(self):
        self.zoom_level = 1.0
        self.image_position = [0, 0]
        self.apply_zoom()
        self.update_info_label()

    def reset_image_position(self, event=None):
        """Centrar la imagen cuando se redimensiona el canvas"""
        if hasattr(self, 'original_image'):
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            img_width = self.current_image.width
            img_height = self.current_image.height

            # Centrar la imagen si es más pequeña que el canvas
            if img_width < canvas_width and img_height < canvas_height:
                self.image_position = [
                    (canvas_width - img_width) // 2,
                    (canvas_height - img_height) // 2
                ]
                self.apply_zoom()

    def start_pan(self, event):
        """Iniciar el desplazamiento de la imagen"""
        self.pan_start_x = event.x
        self.pan_start_y = event.y

    def pan_image(self, event):
        """Mover la imagen con el mouse"""
        if hasattr(self, 'pan_start_x'):
            dx = event.x - self.pan_start_x
            dy = event.y - self.pan_start_y

            self.image_position[0] += dx
            self.image_position[1] += dy

            self.canvas.move(self.image_on_canvas, dx, dy)
            self.pan_start_x = event.x
            self.pan_start_y = event.y

    def update_info_label(self):
        if 0 <= self.current_index < len(self.image_list):
            image_path = self.image_list[self.current_index]
            self.info_label.config(
                text=f"Imagen {self.current_index + 1} de {len(self.image_list)}: {os.path.basename(image_path)} | Zoom: {int(self.zoom_level*100)}%"
            )

    def update_thumbnails(self):
        # Limpiar miniaturas anteriores
        for widget in self.thumbnails_inner_frame.winfo_children():
            widget.destroy()

        self.thumbnail_buttons = []
        self.thumbnail_images = []

        # Crear miniaturas para cada imagen
        for idx, image_path in enumerate(self.image_list):
            try:
                # Crear miniatura
                img = Image.open(image_path)
                img.thumbnail((80, 80))

                # Convertir a PhotoImage
                thumb_img = ImageTk.PhotoImage(img)
                self.thumbnail_images.append(thumb_img)

                # Crear botón con la miniatura
                btn = tk.Button(
                    self.thumbnails_inner_frame,
                    image=thumb_img,
                    command=lambda i=idx: self.show_image(i)
                )
                btn.config(width=90, height=90)
                btn.pack(side=tk.LEFT, padx=2, pady=2)
                self.thumbnail_buttons.append(btn)


            except Exception as e:
                print(f"Error al crear miniatura para {image_path}: {e}")

        # Resaltar miniatura seleccionada
        self.highlight_selected_thumbnail()

    def highlight_selected_thumbnail(self):
        for i, btn in enumerate(self.thumbnail_buttons):
            if i == self.current_index:
                btn.config(relief=tk.SUNKEN, bg='light blue')
            else:
                btn.config(relief=tk.RAISED, bg='SystemButtonFace')

    def prev_image(self):
        if len(self.image_list) > 0:
            new_index = (self.current_index - 1) % len(self.image_list)
            self.show_image(new_index)

    def next_image(self):
        if len(self.image_list) > 0:
            new_index = (self.current_index + 1) % len(self.image_list)
            self.show_image(new_index)

    def add_image(self):
        filetypes = (
            ("Imágenes", "*.jpg *.jpeg *.png"),
            ("Todos los archivos", "*.*")
        )

        file_path = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=filetypes
        )

        if file_path:
            try:
                # Verificar que sea una imagen válida
                with Image.open(file_path) as img:
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
                self.load_images()
                self.show_image(len(self.image_list) - 1)
                self.update_thumbnails()

                messagebox.showinfo("Éxito", "Imagen agregada correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar la imagen: {e}")

    def delete_image(self):
        if len(self.image_list) == 0:
            return

        current_image = self.image_list[self.current_index]
        confirm = messagebox.askyesno(
            "Confirmar",
            f"¿Estás seguro de eliminar {os.path.basename(current_image)}?"
        )

        if confirm:
            try:
                os.remove(current_image)
                self.load_images()

                if len(self.image_list) > 0:
                    new_index = min(self.current_index, len(self.image_list) - 1)
                    self.show_image(new_index)
                else:
                    self.canvas.delete("all")
                    self.info_label.config(text="No hay imágenes en la carpeta")
                    self.current_index = 0

                self.update_thumbnails()
                messagebox.showinfo("Éxito", "Imagen eliminada correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la imagen: {e}")

    def show_metadata(self):
        if len(self.image_list) == 0:
            return

        current_image = self.image_list[self.current_index]

        try:
            with Image.open(current_image) as img:
                # Obtener metadatos EXIF
                exif_data = img._getexif()
                metadata = {}

                if exif_data:
                    for tag, value in exif_data.items():
                        tag_name = ExifTags.TAGS.get(tag, tag)
                        metadata[tag_name] = value

                # Obtener fecha de creación del archivo
                file_time = os.path.getmtime(current_image)
                file_date = datetime.fromtimestamp(file_time).strftime("%Y-%m-%d %H:%M:%S")

                # Crear ventana de metadatos
                meta_window = tk.Toplevel(self.root)
                meta_window.title("Metadatos de la imagen")

                # Mostrar información básica
                tk.Label(meta_window, text=f"Archivo: {os.path.basename(current_image)}",
                         font=('Arial', 10, 'bold')).pack(anchor=tk.W, padx=10, pady=5)

                tk.Label(meta_window, text=f"Fecha del sistema: {file_date}").pack(anchor=tk.W, padx=10)

                # Mostrar fecha EXIF si existe
                if 'DateTime' in metadata:
                    exif_date = metadata['DateTime']
                    tk.Label(meta_window, text=f"Fecha EXIF: {exif_date}").pack(anchor=tk.W, padx=10)
                elif 'DateTimeOriginal' in metadata:
                    exif_date = metadata['DateTimeOriginal']
                    tk.Label(meta_window, text=f"Fecha EXIF (Original): {exif_date}").pack(anchor=tk.W, padx=10)
                else:
                    tk.Label(meta_window, text="No se encontró fecha en los metadatos EXIF").pack(anchor=tk.W, padx=10)

                # Mostrar más metadatos si existen
                if metadata:
                    tk.Label(meta_window, text="\nOtros metadatos:", font=('Arial', 9, 'bold')).pack(anchor=tk.W, padx=10, pady=(10,0))

                    meta_text = tk.Text(meta_window, height=10, width=50)
                    scroll = tk.Scrollbar(meta_window, command=meta_text.yview)
                    meta_text.configure(yscrollcommand=scroll.set)

                    scroll.pack(side=tk.RIGHT, fill=tk.Y)
                    meta_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

                    for key, value in metadata.items():
                        meta_text.insert(tk.END, f"{key}: {value}\n")
                    meta_text.config(state=tk.DISABLED)

                # Botón para cerrar
                tk.Button(meta_window, text="Cerrar", command=meta_window.destroy).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron leer los metadatos: {e}")

if __name__ == "__main__":
    # Obtener la carpeta de imágenes desde un string
    # (Reemplaza esto con tu string específico)
    folder_path = "C:/Mis_Imagenes"  # Ejemplo - cambia esto por tu ruta

    root = tk.Tk()
    root.geometry("700x600")  # Aumenté la altura para las miniaturas
    app = ImageViewer(root, folder_path)
    root.mainloop()