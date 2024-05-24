import tkinter as tk
from tkinter import ttk
from tkinter import *
from datetime import datetime, timedelta

# Crear la ventana principal
root = tk.Tk()
root.title("Turnos")

# Crear un Frame para contener el Treeview y la barra de desplazamiento
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=False)

# Crear el Treeview
tree = ttk.Treeview(frame, columns=("Horario", "Paciente", "Prestacion", "Odontologo"), show='headings')

# Definir los encabezados de las columnas
tree.heading("Horario", text="Horario")
tree.heading("Paciente", text="Paciente")
tree.heading("Prestacion", text="Prestacion")
tree.heading("Odontologo", text="Odontologo")

# Ajustar el ancho de las columnas
tree.column("Horario", width=100)
tree.column("Paciente", width=100)
tree.column("Prestacion", width=100)
tree.column("Odontologo", width=100)

# Agregar filas al Treeview
for i in range(1, 21):
    tree.insert("", "end", values=(f"Fila {i} Col1", f"Fila {i} Col2", f"Fila {i} Col3", f"Fila {i} Col4"))

# Crear la barra de desplazamiento vertical
scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)

# Ubicar el Treeview y la barra de desplazamiento en el Frame
tree.grid(row=1, column=0, sticky='nsew', columnspan=4)
scrollbar.grid(row=1, column=5, sticky='ns')

# Configurar el Frame para expandir el Treeview y la barra de desplazamiento
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
Button(frame, text="Agregar turno", bg="#D1D6D3", bd= 2, borderwidth= 2, width=10).grid(row=0, column=0, padx=(10,10), pady=(5,5))
Button(frame, text="Eliminar turno", bg="#D1D6D3", bd= 2, borderwidth= 2, width=10).grid(row=0, column=1, padx=(10,10), pady=(5,5))
Button(frame, text="Editar turno", bg="#D1D6D3", bd= 2, borderwidth= 2, width=10).grid(row=0, column=2, padx=(10,10), pady=(5,5))
Button(frame, text="Salir", bg="orange", bd= 2, borderwidth= 2, width=10).grid(row=0, column=3, padx=(10,10), pady=(5,5))

# Ejecutar la aplicación
root.mainloop()
