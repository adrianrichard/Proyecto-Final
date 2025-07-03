import os
import platform
import subprocess
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generar_pdf_y_seleccionar(output_path):
    """Genera un PDF y abre la carpeta seleccionando el archivo"""
    # 1. Generar el PDF (ejemplo mínimo)
    c = canvas.Canvas(output_path, pagesize=A4)
    c.drawString(100, 750, "Documento generado automáticamente")
    c.save()

    # 2. Abrir carpeta y seleccionar archivo
    seleccionar_archivo_en_explorador(output_path)

def seleccionar_archivo_en_explorador(filepath):
    """Abre el explorador de archivos y selecciona el archivo especificado"""
    try:
        sistema = platform.system()
        path_absoluto = os.path.abspath(filepath)

        if sistema == "Windows":
            # La mejor manera en Windows
            subprocess.run(f'explorer /select,"{path_absoluto}"', shell=True)
        elif sistema == "Darwin":  # macOS
            # Comando para macOS
            subprocess.run(['open', '-R', path_absoluto])
        else:  # Linux
            # Intentamos con los gestores de archivos más comunes
            try:
                subprocess.run(['nautilus', '--select', path_absoluto])
            except FileNotFoundError:
                try:
                    subprocess.run(['dolphin', '--select', path_absoluto])
                except FileNotFoundError:
                    # Fallback: abrir solo la carpeta
                    subprocess.run(['xdg-open', os.path.dirname(path_absoluto)])

        print(f"Archivo seleccionado: {path_absoluto}")
    except Exception as e:
        print(f"Error al abrir el explorador: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    # Ruta relativa o absoluta donde se guardará el PDF
    directorio_salida = "informes_odontologicos"
    nombre_archivo = "paciente_juan_perez2.pdf"

    # Crear directorio si no existe
    os.makedirs(directorio_salida, exist_ok=True)

    # Ruta completa del archivo
    ruta_completa = os.path.join(directorio_salida, nombre_archivo)

    # Generar y mostrar el PDF
    generar_pdf_y_seleccionar(ruta_completa)