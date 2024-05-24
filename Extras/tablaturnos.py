from tkinter import *
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
import re
from tkinter import messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Tkinter Validation Demo')
        self.geometry("500x500")

        self.create_widgets()

    def create_widgets(self):

        Button(self, text="Agregar turno", bg="#D1D6D3", bd= 2, borderwidth= 2, width=10).grid(row=0, column=0, pady=(5,5))
        Button(self, text="Eliminar turno", bg="#D1D6D3", bd= 2, borderwidth= 2, width=10).grid(row=0, column=1, pady=(5,5))
        Button(self, text="Editar turno", bg="#D1D6D3", bd= 2, borderwidth= 2, width=10).grid(row=0, column=2, pady=(5,5))
        Button(self, text="Salir", bg="orange", bd= 2, borderwidth= 2, width=10, command=self.destroy).grid(row=0, column=3, pady=(5,5))
    #def cargar_turnos(self, frame):    
        self.frame_tabla_turnos = Frame(self, bg= 'gray90')
        #self.frame_tabla_turnos.grid(column=0, row=1, columnspan=4, sticky='nsew')
        self.frame_tabla_turnos = ttk.Treeview(self.frame_tabla_turnos, columns=("Horario", "Paciente", "Prestacion", "Odontologo"), show='headings')
        #self.frame_tabla_turnos.grid(column=0, row=1, columnspan=4, sticky='nsew')
        
        self.frame_tabla_turnos.heading("Horario", text="Horario")
        self.frame_tabla_turnos.heading("Paciente", text="Paciente")
        self.frame_tabla_turnos.heading("Prestacion", text="Prestacion")
        self.frame_tabla_turnos.heading("Odontologo", text="Odontologo")
        
        self.frame_tabla_turnos.column("Horario", width=100)
        self.frame_tabla_turnos.column("Paciente", width=100)
        self.frame_tabla_turnos.column("Prestacion", width=100)
        self.frame_tabla_turnos.column("Odontologo", width=100)
        # [self.frame_tabla_turnos.columnconfigure(i, weight=1) for i in range(self.grid_size()[0])]
        # [self.columnconfigure(i, weight=1) for i in range(self.grid_size()[0])]
        # [self.frame_tabla_turnos.rowconfigure(i, weight=1) for i in range(self.grid_size()[1])] 
        # Hora de inicio
        start_time = datetime.strptime("08:00", "%H:%M")
        # Intervalo de 30 minutos
        time_interval = timedelta(minutes=30)
        self.frame_tabla_turnos.delete(*self.frame_tabla_turnos.get_children())
        # Generar horarios en un día
        for i in range(11 * 2):  # 24 horas en un día, cada hora tiene dos intervalos de 30 minutos
            current_time = start_time + i * time_interval
            #print(current_time.strftime("%H:%M"))     
            self.frame_tabla_turnos.insert('',i, text = current_time.strftime("%H:%M"), values=(i,i))
        scrollbar = ttk.Scrollbar(self.frame_tabla_turnos, orient=tk.VERTICAL, command=self.frame_tabla_turnos.yview)
        self.frame_tabla_turnos.configure(yscroll=scrollbar.set)
        # Ubicar el Treeview y la barra de desplazamiento en el Frame
        self.frame_tabla_turnos.grid(row=1, column=0, sticky='nsew', columnspan=4)
        scrollbar.grid(row=1, column=5, sticky='ns')
        # ladoy = ttk.Scrollbar(self.frame_tabla_turnos, orient ='vertical', command = self.frame_tabla_turnos.yview)
        # ladoy.grid(column = 0, row = 1, sticky='ns')
        # #ladoy.pack(side ='right')
        # self.frame_tabla_turnos.configure(yscrollcommand = ladoy.set) 

if __name__ == '__main__':
    app = App()
    app.mainloop()