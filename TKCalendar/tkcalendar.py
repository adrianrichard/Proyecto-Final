from datetime import datetime
from functools import partial
from tkinter import *

from events.eventdbcontroller import EventController
from datehandler.datehandler import DateHandler as dH
from tkconfiguration.eventcolor import EventColor
from tkwidgetclasses.hover_button import HoverButton
from toplevels.daytoplevel import DayTopWindow
from tkwindowextensions.tk_legend import TKLegend

from pathlib import Path

script_location = Path(__file__).absolute().parent
#file_location = script_location / 'file.yaml'
#file = file_location.open()

class TKCalendar():

    def __init__(self):
        super().__init__()

        self.date_buttons = []
        self.toplevel = None
        self.legend = None
        self.header = None

        self.year = datetime.now().year  # Devuelve entero de 4-digit (year)
        self.month = datetime.now().month  # Devuelve entero(month)
        self.dates = []

        """ Clases soporte """
        self.dh = dH()

        #self.up_chevron_path=script_location / 'chevron_up.png'
        file_location = script_location / 'chevron_up.png'
        #file = file_location.open()
        self.up_chevron = PhotoImage(file_location.open())
        file_location = script_location / 'chevron_down.png'
        self.down_chevron = PhotoImage(file_location.open())
        
    def _make_header(self, frame):
        """ Crea el encabezado """        
        header_text = f"{self.dh.month_num_to_string(self.month)} {self.year}"
        self.header = Label(frame, text=header_text, font="Arvo 15", justify=CENTER)
        self.header.grid(row=0, column=0, columnspan=7, sticky=EW, ipady=10)

        day_list = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sabado", "Domingo"]
        for i, j in enumerate(day_list):
            Label(frame, text=day_list[i], bd=1, relief=SOLID).grid(row=1, column=i, sticky=NSEW, ipady=10)

    def _make_month_adjust_buttons(self, frame):
        """ Crea los botones para cambiar el mes """
        Button(frame, text="<", command=self.month_down, bg="#808080", height=2, width=8).grid(row=0, column=1)
        Button(frame, text=">", command=self.month_up, bg="#808080", height=2, width=8).grid(row=0, column=5)        

    def _make_day_buttons(self, frame):
        """ Crea botones de fechas """
        coords = [(i, j) for i in range(2, 8) for j in range(0, 7)]
        for coord in coords:
            btn = HoverButton(frame, bg="gray", relief=SUNKEN, bd=2, height=4, width=10)
            btn.grid(row=coord[0], column=coord[1], sticky=NSEW)
            self.date_buttons.append(btn)
    
    def _configure_header(self):
        """ Actualiza el encabezado del mes """
        self.header.configure(text=f"{self.dh.month_num_to_string(self.month)} {self.year}")

    def _configure_day_buttons(self):
        """ Set button text to date numbers """
        self.dates = self.dh.date_list(self.year, self.month)  # Devuelve 35 dias (5 semanas)
        self.dates.extend([0 for _ in range(42 - len(self.dates))])  # agrega ceros en las fechas porque son 42 botones de fecha

        for i, j in enumerate(self.dates):  # Configure el texto del boton para mostrar la fecha
            if j == 0:
                self.date_buttons[i].configure(text="", state=DISABLED, bg="#808080")
            else:
                self.date_buttons[i].configure(text=j, command=partial(self.day_info, j), bg="white", state=NORMAL)
            #Marca la fecha actual
            if j == datetime.today().day \
                    and self.month == datetime.today().month \
                    and self.year == datetime.today().year:
                self.date_buttons[i].configure(bg="#D9FFE3")

    def _event_color_buttons(self):
        for button in self.date_buttons:
            if button["text"] != 0:
                query = {"year": self.year, "month": self.month, "day": button["text"]}
                date_events = EventController.find_by_elements(query)
                if date_events:
                    categories = [event.category for event in date_events]
                    EventColor().colorize(button, categories)

    def _configure_rows_columns(self, frame):
        """ Configura filas y columnas para expandandirlas al tamaño de la ventana """
        [frame.rowconfigure(i, weight=1) for i in range(frame.grid_size()[1])]
        [frame.columnconfigure(i, weight=1) for i in range(frame.grid_size()[0])]

    def month_up(self):
        """ Aumenta el mes y reconfigura la interface del calendario """
        self.month += 1
        if self.month == 13:
            self.month = 1
            self.year += 1
        self._configure_day_buttons()
        self._event_color_buttons()
        self._configure_header()

    def month_down(self):
        """ Disminuye el mes y reconfigura la interface del calendario """
        self.month -= 1
        if self.month == 0:
            self.month = 12
            self.year -= 1
        self._configure_day_buttons()
        self._event_color_buttons()
        self._configure_header()

    def day_info(self, day_num):
        """ Abre una ventana para guardar la cita """
        try:
            self.toplevel.destroy()
            self.toplevel = DayTopWindow(day_num, self.month, self.year)
        except AttributeError:
            self.toplevel = DayTopWindow(day_num, self.month, self.year)