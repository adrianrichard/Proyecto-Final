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

        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)

        # label
        ttk.Label(text='Email:').grid(row=0, column=0, padx=5, pady=5)

        # email entry
        vcmd = (self.register(self.validate), '%P')
        ivcmd = (self.register(self.on_invalid),)

        self.email_entry = Entry(self, width=50, bg="sky blue")
        self.email_entry.config(validate='focusout', validatecommand=vcmd, invalidcommand=ivcmd)
        self.email_entry.grid(row=0, column=1, columnspan=2, padx=5)

        self.label_error = ttk.Label(self, foreground='red')
        self.label_error.grid(row=1, column=1, sticky=tk.W, padx=5)

        # button
        self.send_button = tk.Button(text='Send', state="disable", disabledforeground="red").grid(row=0, column=4, padx=5)
    
    #def cargar_turnos(self, frame):    
        self.frame_tabla_turnos = Frame(self, bg= 'gray90')
        self.frame_tabla_turnos.grid(column=0, row=1, columnspan=4, sticky='nsew')
        self.frame_tabla_turnos = ttk.Treeview(self.frame_tabla_turnos, selectmode ='browse')
        self.frame_tabla_turnos.grid(column=0, row=1, columnspan=4, sticky='nsew')
        # ladoy = ttk.Scrollbar(self.frame_tabla_turnos, orient ='vertical', command = self.frame_tabla_turnos.yview)
        # ladoy.grid(column = 4, row = 1, sticky='ns')
        # self.frame_tabla_turnos.configure(yscrollcommand = ladoy.set)
        self.frame_tabla_turnos['columns'] = ( 'Paciente', 'Prestacion','Odontologo')
        self.frame_tabla_turnos.column('#0', minwidth=100, width=120, anchor='center')
        self.frame_tabla_turnos.column('Paciente', minwidth=100, width=120, anchor='center' )
        self.frame_tabla_turnos.column('Prestacion', minwidth=100, width=120, anchor='center' )        
        self.frame_tabla_turnos.column('Odontologo', minwidth=100, width=120, anchor='center' )
        self.frame_tabla_turnos.delete(*self.frame_tabla_turnos.get_children())
        self.frame_tabla_turnos.heading('#0', text='Horario', anchor ='center')
        self.frame_tabla_turnos.heading('Paciente', text='Paciente', anchor ='center')
        self.frame_tabla_turnos.heading('Prestacion', text='Prestacion', anchor ='center')
        self.frame_tabla_turnos.heading('Odontologo', text='Odontologo', anchor ='center')
        # Hora de inicio
        start_time = datetime.strptime("08:00", "%H:%M")
        # Intervalo de 30 minutos
        time_interval = timedelta(minutes=30)
        # Generar horarios en un día
        for i in range(11 * 2):  # 24 horas en un día, cada hora tiene dos intervalos de 30 minutos
            current_time = start_time + i * time_interval
            #print(current_time.strftime("%H:%M"))     
            self.frame_tabla_turnos.insert('',i, text = current_time.strftime("%H:%M"), values=(i,i))     

    def show_message(self, error='', color='black'):
        self.label_error['text'] = error
        self.email_entry['foreground'] = color

    def validate(self, value):
        """
        Validat the email entry
        :param value:
        :return:
        """
        pattern = r'\b[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(pattern, value) is None:
            
            return False
        self.email_entry.configure(bg="white")
        self.show_message()
        return True

    def on_invalid(self):
        """
        Show the error message if the data is not valid
        :return:
        """
        #self.show_message('Please enter a valid email', 'red')
        #self.email_entry['background'] = 'red'
        self.email_entry.focus()
        #messagebox.showwarning("Invalid", "Invalid email format.")


if __name__ == '__main__':
    app = App()
    app.mainloop()