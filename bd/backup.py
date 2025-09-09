import sqlite3
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import util.config as utl

class Backup:
    def __init__(self):
        super().__init__()
        self.bd_seleccionada = ''  # Variable para almacenar la base de datos seleccionada
        self.fuenteb = utl.definir_fuente_bold()
        self.fuenten = utl.definir_fuente()
        self.color_fondo1, self.color_fondo2 = utl.definir_color_fondo()

    def configurar_interfaz(self, frame):
        # Estilo de la tabla
        self.estilo_tablab = ttk.Style(frame)
        self.estilo_tablab.theme_use('alt')
        self.estilo_tablab.configure('TablaBackup.Treeview', font=self.fuenten, foreground='black', rowheight=20)
        self.estilo_tablab.configure('TablaBackup.Treeview.Heading', background=self.color_fondo1, foreground='white', padding=3, font=self.fuenteb)

        # Crear la tabla para mostrar las bases de datos
        self.tabla = ttk.Treeview(frame, columns=("Nombre", "Fecha"), show="headings", height=8, style="TablaBackup.Treeview")
        self.tabla.heading("Nombre", text="Nombre BD")
        self.tabla.heading("Fecha", text="Fecha de creación")
        self.tabla.column('Nombre', width=350, anchor='w')
        self.tabla.column('Fecha', width=200, anchor='w')
        
        # Configurar grid
        self.tabla.grid(column=0, row=2, columnspan=3, padx=(10, 0), sticky='nsew')
        ladoy = ttk.Scrollbar(frame, orient='vertical', command=self.tabla.yview)
        ladoy.grid(column=3, row=2, sticky='ns')
        self.tabla.configure(yscrollcommand=ladoy.set)

        # Bind para seleccionar la base de datos desde la tabla
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_desde_tabla)

        # Listar las bases de datos en la tabla
        self.listar_bases_datos()

        self.frame_botones = tk.Frame(frame, bg=self.color_fondo2)
        self.frame_botones.grid(column=0, row=3, columnspan=4, sticky='ew', pady=10)
        
        btn_cargar_copia = tk.Button(self.frame_botones, text="Cargar copia de seguridad", fg='white', 
                                   font=self.fuenteb, bg=self.color_fondo1, bd=2, borderwidth=2, 
                                   command=self.cargar_backup)
        btn_cargar_copia.grid(column=0, row=0, padx=(10, 5), pady=(10, 10))

        btn_guardar_copia = tk.Button(self.frame_botones, text="Crear copia de seguridad", fg='white', 
                                    font=self.fuenteb, bg=self.color_fondo1, bd=2, borderwidth=2, 
                                    command=self.crear_backup)
        btn_guardar_copia.grid(column=1, row=0, padx=5, pady=(10, 10))

        # Botón para eliminar la base de datos seleccionada
        btn_eliminar_copia = tk.Button(self.frame_botones, text="Eliminar copia de seguridad", fg='white', 
                                     font=self.fuenteb, bg='#d9534f', bd=2, borderwidth=2,  # Color rojo para peligro
                                     command=self.eliminar_backup)
        btn_eliminar_copia.grid(column=2, row=0, padx=5, pady=(10, 10))

    def obtener_carpeta_script(self):
        """Obtiene la ruta del directorio donde se encuentra el script Backup"""
        return os.path.dirname(os.path.abspath(__file__))

    def eliminar_backup(self):
        """Elimina la copia de seguridad seleccionada"""
        if not self.bd_seleccionada:
            messagebox.showwarning("Advertencia", "Debe seleccionar una copia de seguridad primero")
            return

        # Prevenir eliminación de la base de datos principal
        if self.bd_seleccionada == "consultorioMyM.sqlite3":
            messagebox.showerror("Error", "No se puede eliminar la base de datos principal")
            return

        # Confirmar la eliminación
        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de que desea eliminar permanentemente la copia de seguridad:\n\n"
            f"'{self.bd_seleccionada}'?\n\n"
            "¡Esta acción no se puede deshacer!"
        )

        if not respuesta:
            return

        carpeta_script = self.obtener_carpeta_script()
        ruta_backup = os.path.join(carpeta_script, self.bd_seleccionada)

        # Verificar que el archivo existe
        if not os.path.exists(ruta_backup):
            messagebox.showerror("Error", f"No se encuentra el archivo: {self.bd_seleccionada}")
            return

        try:
            # Eliminar el archivo
            os.remove(ruta_backup)
            messagebox.showinfo("Éxito", f"Copia de seguridad eliminada: {self.bd_seleccionada}")

            # Limpiar selección y actualizar lista
            self.bd_seleccionada = ''
            self.listar_bases_datos()

        except PermissionError:
            messagebox.showerror("Error", "Permiso denegado. El archivo puede estar en uso.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el archivo: {e}")

    def cargar_backup(self):
        """Carga/restaura una copia de seguridad seleccionada"""
        if not self.bd_seleccionada:
            messagebox.showwarning("Advertencia", "Debe seleccionar una copia de seguridad primero")
            return

        # Prevenir restauración de la base de datos principal sobre sí misma
        if self.bd_seleccionada == "consultorioMyM.sqlite3":
            messagebox.showwarning("Advertencia", "No puede restaurar la base de datos principal sobre sí misma")
            return

        # Confirmar la acción con el usuario
        respuesta = messagebox.askyesno(
            "Confirmar restauración",
            f"¿Está seguro de que desea restaurar la base de datos principal usando:\n\n"
            f"'{self.bd_seleccionada}'?\n\n"
            "ADVERTENCIA: Esta acción sobrescribirá la base de datos actual y no se puede deshacer."
        )

        if not respuesta:
            return

        carpeta_script = self.obtener_carpeta_script()
        
        # Definir nombres de archivos
        bd_principal = "consultorioMyM.sqlite3"  # Nombre de la BD principal
        bd_backup = self.bd_seleccionada  # BD de backup seleccionada
        
        ruta_backup = os.path.join(carpeta_script, bd_backup)
        ruta_principal = os.path.join(carpeta_script, bd_principal)
        
        # Verificar que el backup existe
        if not os.path.exists(ruta_backup):
            messagebox.showerror("Error", f"No se encuentra el backup: {bd_backup}")
            return

        try:            
            # Verificar integridad del backup antes de restaurar
            if not self.verificar_integridad_bd(ruta_backup):
                messagebox.showerror("Error", "El archivo de backup está corrupto o no es una base de datos válida")
                return
            
            # Realizar la restauración
            shutil.copy(ruta_backup, ruta_principal)
            
            # Verificar que la restauración fue exitosa
            if self.verificar_integridad_bd(ruta_principal):
                messagebox.showinfo(
                    "Éxito", 
                    f"Backup restaurado exitosamente!\n\n"
                    f"Base de datos principal: {bd_principal}\n"
                    f"Backup utilizado: {bd_backup}\n"
                )
                self.listar_bases_datos()  # Actualizar la tabla
            else:                
                messagebox.showerror("Error", "La restauración falló")
                
        except PermissionError:
            messagebox.showerror("Error", "Permiso denegado. Asegúrese de que la base de datos no esté en uso.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el backup: {e}")

    def verificar_integridad_bd(self, ruta_bd):
        """Verifica que un archivo SQLite3 sea válido y no esté corrupto"""
        try:
            if not os.path.exists(ruta_bd):
                return False
            
            # Intentar conectar y ejecutar una consulta simple
            conn = sqlite3.connect(ruta_bd)
            cursor = conn.cursor()
            
            # Verificar integridad con PRAGMA integrity_check
            cursor.execute("PRAGMA integrity_check")
            resultado = cursor.fetchone()
            
            # Verificar que existen tablas esenciales (opcional)
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tablas = cursor.fetchall()
            
            conn.close()
            
            # Si integrity_check retorna 'ok', la BD está intacta
            return resultado and resultado[0] == 'ok' and len(tablas) > 0
            
        except sqlite3.Error:
            return False
        except Exception:
            return False

    def crear_backup(self):
        carpeta_script = self.obtener_carpeta_script()
        print(carpeta_script)
        fecha_actual = datetime.now().strftime("%Y%m%d_%H%M")
        nombre = 'consultorioMyM'

        ruta_original = os.path.join(carpeta_script, nombre+".sqlite3")
        base_nombre = f"{nombre}_{fecha_actual}.sqlite3"
        ruta_copia = os.path.join(carpeta_script, base_nombre)
        try:
            shutil.copy(ruta_original, ruta_copia)
            messagebox.showinfo("Éxito", f"Backup creado: {base_nombre}")
            self.listar_bases_datos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el backup: {e}")

    def listar_bases_datos(self):
        """Lista todas las bases de datos .sqlite3 excepto la principal consultorioMyM.sqlite3"""
        carpeta_origen = self.obtener_carpeta_script()
        
        # Obtener todos los archivos .sqlite3 excluyendo la BD principal
        bases_datos = [
            f for f in os.listdir(carpeta_origen) 
            if f.endswith(".sqlite3") and f != "consultorioMyM.sqlite3"
        ]

        # Limpiar la tabla
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        # Insertar las bases de datos en la tabla
        for base_datos in bases_datos:
            ruta_archivo = os.path.join(carpeta_origen, base_datos)
            try:
                fecha_creacion = datetime.fromtimestamp(os.path.getctime(ruta_archivo)).strftime('%Y-%m-%d %H:%M:%S')
                nombre_sin_extension = os.path.splitext(base_datos)[0]
                self.tabla.insert("", "end", values=(nombre_sin_extension, fecha_creacion))
            except OSError:
                self.tabla.insert("", "end", values=(os.path.splitext(base_datos)[0], "Fecha no disponible"))

        if not bases_datos:
            messagebox.showinfo("Información", "No se encontraron copias de seguridad en la carpeta.")

    def seleccionar_desde_tabla(self, event):
        selected_item = self.tabla.selection()
        if selected_item:
            item = self.tabla.item(selected_item[0])
            seleccion = item['values'][0]
            self.bd_seleccionada = seleccion + '.sqlite3'