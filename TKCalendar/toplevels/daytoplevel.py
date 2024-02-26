import util.generic as utl
from tkinter import *
from datehandler.datehandler import DateHandler
from tkwindowextensions.tk_add_event import NuevaCita
from tkwindowextensions.tk_remove_event import TKRemoveEvent
from tkwindowextensions.tk_change_event import TKChangeEvent
from events.eventdbcontroller import EventController
from tkinter import Button

class DayTopWindow(Toplevel):
    """ Toplevel class for event operations on the TKCalendar """
    
    def __init__(self, dia: int, month: int, year: int):
        super().__init__()        

        self.attributes = ("-topmost", True)
        utl.centrar_ventana(self, 480, 550)
        self.title(f"{month}/{dia}/{year} Events")
        self.resizable(width=False, height=False)
        self.event_box = None
        self.configure(bg="#D1D6D3")
        self.grab_set_global()
        self.extension = None
        self.confirmation = None

        self.dia = dia
        self.month = month
        self.year = year

        self.crear_header()
        self.crear_botones_cambio_fecha()
        self._make_event_listbox()
        self._make_event_buttons()
        self._configure_event_box()

    def crear_header(self):
        """ Crea encabezado """
        header_text = f"{self.month}/{self.dia}/{self.year}"
        self.header = Label(self, text=header_text, font="Courier 15", justify=CENTER, borderwidth=3, bd=3, bg="#D1D6D3")
        self.header.grid(row=0, column=1, columnspan=2, ipady=3)

    def crear_botones_cambio_fecha(self):
        """ Crea botones para cambiar fecha """
        Button(self, text=">", command=self.day_up, bg="#BDC1BE", height=1, width=4).grid(row=0, column=3)
        Button(self, text="<", command=self.day_down, bg="#BDC1BE", height=1, width=4).grid(row=0, column=0)

    def _make_event_listbox(self):
        self.event_box = Listbox(self, bg="#BDC1BE", height=10, width=50, selectmode=SINGLE, font="Arvo 12", justify=CENTER, activestyle='none')
        self.event_box.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky=EW)

    def _make_event_buttons(self):
        """ Crea botones de interaccion  """
        self.add_img =utl.leer_imagen("./imagenes/add.png", (50, 50))
        self.remove_img = utl.leer_imagen('./imagenes/eliminar2.png', (50, 50))
        self.change_img = utl.leer_imagen('./imagenes/next.png', (50, 50))

        Button(self, text="Agregar cita", bg="#D1D6D3", bd= 2, borderwidth= 2, width=10, command=self.agregar_cita).grid(row=2, column=0)
        Button(self, text="Eliminar Cita", bg="#D1D6D3", bd= 2, borderwidth= 2, width=10, command=self.remove_event).grid(row=2, column=1)
        Button(self, text="Editar Cita", bg="#D1D6D3", bd= 2, borderwidth= 2, width=10, command=self.change_event).grid(row=2, column=2)
        Button(self, text="Salir", bg="orange", bd= 2, borderwidth= 2, width=10, command=self.destroy).grid(row=2, column=3)


    def _configure_header(self):
        """ Actualiza el header de la fecha """
        header_text = f"{self.month}/{self.dia}/{self.year}"
        self.header.configure(text=header_text)

    def _configure_event_box(self):
        """ Carga la lista con citas del dia """
        self.event_box.delete(0, END)
        query = {"year": self.year, "month": self.month, "day": self.dia}
        event_data = EventController.find_by_elements(query)
        list_data = [
            f"{ev.time_hours}:{ev.time_minutes} - {ev.title} - {ev.category} [{ev.id}]" for ev in event_data]

        if not list_data:
            list_data = ["No hay citas"]
        else:
            list_data.insert(0, "Elegir cita")
        [self.event_box.insert(END, ev_data) for ev_data in list_data]

    def day_up(self):
        """ AVANZAR 1 DIA """
        num_of_days = DateHandler().days_in_month(self.month, self.year)
        self.dia += 1
        if self.dia > num_of_days:
            self.dia = 1
            self.month += 1
            if self.month > 12:
                self.month = 1
                self.year += 1
        self._configure_header()
        self.event_box.destroy()
        self._make_event_listbox()
        self._configure_event_box()

        if self.extension:
            self.extension.main_frame.destroy()
            self.extension = None

    def day_down(self):
        """ RETROCEDER 1 DIA """
        self.dia -= 1
        if self.dia < 1:
            self.month -= 1
            if self.month < 1:
                self.year -= 1
            self.dia = DateHandler().days_in_month(self.month, self.year)
        self._configure_header()
        self.event_box.destroy()
        self._make_event_listbox()
        self._configure_event_box()

        if self.extension:
            self.extension.main_frame.destroy()
            self.extension = None

    def agregar_cita(self):
        """ AGREGAR CITA """
        if not self.extension:
            self.confirmation.destroy() if self.confirmation else None
            self.extension = True
            self.extension = NuevaCita(self, self.dia, self.month, self.year, self._configure_event_box)

    def remove_event(self):
        if not self.extension:
            if not self.event_box.curselection():
                if self.confirmation:
                    self.confirmation.destroy()
                self.confirmation = Label(self, text="Elegir cita", font="Courier 10")
                self.confirmation.grid(row=self.grid_size()[1], column=1, pady=10)
                return

            self.confirmation.destroy() if self.confirmation else None

            selection = self.event_box.get(self.event_box.curselection()).strip()
            if selection not in ["No hay citas", "Elija una cita"]:
                self.extension = True
                str_id = selection.split(" ")[-1]
                int_id = int(str_id[1:-1])
                self.extension = TKRemoveEvent(self, int_id, self._configure_event_box)

    def change_event(self):
        if not self.extension:
            if not self.event_box.curselection():
                if self.confirmation:
                    self.confirmation.destroy()
                self.confirmation = Label(self, text="Elija una cita", font="Courier 10")
                self.confirmation.grid(row=self.grid_size()[1], column=1, pady=10)
                return

            self.confirmation.destroy() if self.confirmation else None

            selection = self.event_box.get(self.event_box.curselection()).strip()
            if selection not in ["No hay citas", "Elija una cita"]:
                self.extension = True
                str_id = selection.split(" ")[-1]
                int_id = int(str_id[1:-1])
                self.extension = TKChangeEvent(self, int_id, self._configure_event_box)
