import tkinter as tk
import re

def validar_correo(entry):
    correo = entry.get()
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', correo):
        entry_correo.config(text="Correo válido", bg="green")
    else:
        entry_correo.config(text="Correo inválido", bg="red")

# Crear la ventana
ventana = tk.Tk()
ventana.title("Validar Correo Electrónico")

# Crear la entrada
entry_correo = tk.Entry(ventana)
entry_correo.pack(pady=10)

# Vincular la función de validación al evento de cambio en la entrada
validate_email = ventana.register(lambda email: validar_correo(entry_correo))
entry_correo.config(validate="key", validatecommand=(validate_email, '%P'))

# Etiqueta para mostrar el resultado
resultado = tk.Label(ventana, text="", fg="black")
resultado.pack(pady=5)

# Función para actualizar el contenido del label mientras se escribe
def actualizar_label(event):
    validar_correo(entry_correo)

# Vincular la función actualizar_label al evento de pulsación de tecla en la entrada
entry_correo.bind('<Key>', actualizar_label)

ventana.mainloop()
