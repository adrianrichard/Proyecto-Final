from datetime import datetime
from functools import partial
from tkinter import *

from events.eventdbcontroller import EventController
from datehandler.datehandler import DateHandler as dH
from tkconfiguration.eventcolor import EventColor
from toplevels.daytoplevel import DayTopWindow

from pathlib import Path

script_location = Path(__file__).absolute().parent
#file_location = script_location / 'file.yaml'
#file = file_location.open()

class TKCalendar():

    def __init__(self):
        super().__init__()

        self.botones_fecha = []
        self.toplevel = None
        self.encabezado = None

        self.anio = datetime.now().year  # Devuelve entero de 4-digit (anio)
        self.mes = datetime.now().month  # Devuelve entero(mes)
        self.fechas = []

        """ Clases soporte """
        self.dh = dH()

        #self.up_chevron_path=script_location / 'chevron_up.png'
        file_location = script_location / 'chevron_up.png'
        #file = file_location.open()
        self.up_chevron = PhotoImage(file_location.open())
        file_location = script_location / 'chevron_down.png'
        self.down_chevron = PhotoImage(file_location.open())
        
    def crear_encabezado(self, frame):
        """ Crea el encabezado """        
        encabezado_texto = f"{self.dh.month_num_to_string(self.mes)} {self.anio}"
        self.encabezado = Label(frame, text=encabezado_texto, font="Arvo 20", justify=CENTER)
        self.encabezado.grid(row=0, column=0, columnspan=7, sticky=EW, ipady=10)

        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sabado", "Domingo"]
        for i, j in enumerate(dias):
            Label(frame, text=dias[i], bd=1, font="Arvo 15", relief=SOLID).grid(row=1, column=i, sticky=NSEW, ipady=10)

        Button(frame, text="<", command=self.mes_anterior, bg="#808080", height=2, width=8).grid(row=0, column=1)
        Button(frame, text=">", command=self.mes_siguiente, bg="#808080", height=2, width=8).grid(row=0, column=5)        

    def crear_botones_fechas(self, frame):
        """ Crea botones de fechas mes actual """
        coords = [(i, j) for i in range(2, 8) for j in range(0, 7)]
        for coord in coords:
            btn = Button(frame, bg="gray", relief=SUNKEN, bd=2, height=4, width=10)
            btn.grid(row=coord[0], column=coord[1], sticky=NSEW)
            self.botones_fecha.append(btn)
    
    def actualizar_encabezado(self):
        """ Actualiza el encabezado del mes """
        self.encabezado.configure(text=f"{self.dh.month_num_to_string(self.mes)} {self.anio}")

    def actualizar_botones_fechas(self):
        """ Set button text to date numbers """
        self.fechas = self.dh.date_list(self.anio, self.mes)  # Devuelve 35 dias (5 semanas)
        self.fechas.extend([0 for _ in range(42 - len(self.fechas))])  # agrega ceros en las fechas porque son 42 botones de fecha

        for i, j in enumerate(self.fechas):  # Configure el texto del boton para mostrar la fecha
            if j == 0:
                self.botones_fecha[i].configure(text="", state=DISABLED, bg="#808080")
            else:
                self.botones_fecha[i].configure(text=j, command=partial(self.info_dia, j), bg="white", state=NORMAL)
            #Marca la fecha actual
            if j == datetime.today().day \
                    and self.mes == datetime.today().month \
                    and self.anio == datetime.today().year:
                self.botones_fecha[i].configure(bg="orange")

    def event_color_buttons(self):
        for button in self.botones_fecha:
            if button["text"] != 0:
                query = {"year": self.anio, "month": self.mes, "day": button["text"]}
                date_events = EventController.find_by_elements(query)
                if date_events:
                    prestaciones = [event.category for event in date_events]
                    EventColor().colorize(button, prestaciones)

    def configurar_filas_columnas(self, frame):
        """ Configura filas y columnas para expandandirlas al tamaño de la ventana """
        [frame.rowconfigure(i, weight=1) for i in range(frame.grid_size()[1])]
        [frame.columnconfigure(i, weight=1) for i in range(frame.grid_size()[0])]

    def mes_siguiente(self):
        """ Aumenta el mes y reconfigura la interface del calendario """
        self.mes += 1
        if self.mes == 13:
            self.mes = 1
            self.anio += 1
        self.actualizar_botones_fechas()
        self.event_color_buttons()
        self.actualizar_encabezado()

    def mes_anterior(self):
        """ Disminuye el mes y reconfigura la interface del calendario """
        self.mes -= 1
        if self.mes == 0:
            self.mes = 12
            self.anio -= 1
        self.actualizar_botones_fechas()
        self.event_color_buttons()
        self.actualizar_encabezado()

    def info_dia(self, dia):
        """ Abre una ventana para guardar la cita """
        try:
            self.toplevel.destroy()
            self.toplevel = DayTopWindow(dia, self.mes, self.anio)
        except AttributeError:
            self.toplevel = DayTopWindow(dia, self.mes, self.anio)