import util.generic as utl
from tkinter import *
from datehandler.datehandler import DateHandler
from tkwindowextensions.tk_add_event import TurnoNuevo
from tkwindowextensions.tk_remove_event import TurnoEliminar
from tkwindowextensions.tk_change_event import TurnoModificar
from events.eventdbcontroller import EventController
from tkinter import Button

class DayTopWindow(Toplevel):
    
    def __init__(self, dia: int, mes: int, anio: int):
        super().__init__()        

        self.attributes = ("-topmost", True)
        utl.centrar_ventana(self, 480, 550)
        self.title("Agenda de turnos")
        self.resizable(width=False, height=False)
        self.turnos_box = None
        self.configure(bg="#D1D6D3")
        self.grab_set_global()
        self.extension = None
        self.confirmation = None

        self.dia = dia
        self.mes = mes
        self.anio = anio

        self.crear_encabezado()
        self.crear_botones_cambio_fecha()
        self.crear_listbox_citas()
        self.crear_event_buttons()
        self.configurar_event_box()

    def crear_encabezado(self):
        """ Crea encabezado """
        encabezado_texto = f"{self.dia}/{self.mes}/{self.anio}"
        self.encabezado = Label(self, text=encabezado_texto, font="Courier 15", justify=CENTER, borderwidth=3, bd=3, bg="#D1D6D3")
        self.encabezado.grid(row=0, column=1, columnspan=2, ipady=3)

    def crear_botones_cambio_fecha(self):
        """ Crea botones para cambiar fecha """
        Button(self, text=">", command=self.avanzar_dia, bg="#BDC1BE", height=1, width=4).grid(row=0, column=3)
        Button(self, text="<", command=self.retroceder_dia, bg="#BDC1BE", height=1, width=4).grid(row=0, column=0)

    def crear_listbox_citas(self):
        self.turnos_box = Listbox(self, bg="#BDC1BE", height=10, width=50, selectmode=SINGLE, font="Arvo 12", justify=CENTER, activestyle='none')
        self.turnos_box.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky=EW)

    def crear_event_buttons(self):
        """ Crea botones de interaccion  """
        self.agregar_img =utl.leer_imagen("./imagenes/add.png", (50, 50))
        self.eliminar_img = utl.leer_imagen('./imagenes/eliminar2.png', (50, 50))
        self.cambiar_img = utl.leer_imagen('./imagenes/next.png', (50, 50))

        Button(self, text="Agregar turno", bg="#D1D6D3", bd= 2, borderwidth= 2, width=10, command=self.agregar_turno).grid(row=2, column=0)
        Button(self, text="Eliminar turno", bg="#D1D6D3", bd= 2, borderwidth= 2, width=10, command=self.eliminar_turno).grid(row=2, column=1)
        Button(self, text="Editar turno", bg="#D1D6D3", bd= 2, borderwidth= 2, width=10, command=self.cambiar_turno).grid(row=2, column=2)
        Button(self, text="Salir", bg="orange", bd= 2, borderwidth= 2, width=10, command=self.destroy).grid(row=2, column=3)


    def configurar_encabezado(self):
        """ Actualiza el header de la fecha """
        encabezado_texto = f"{self.dia}/{self.mes}/{self.anio}"
        self.encabezado.configure(text=encabezado_texto)

    def configurar_event_box(self):
        """ Carga la lista con citas del dia """
        self.turnos_box.delete(0, END)
        query = {"year": self.anio, "month": self.mes, "day": self.dia}
        event_data = EventController.find_by_elements(query)
        list_data = [
            f"{ev.time_hours}:{ev.time_minutes} - {ev.title} - {ev.category} [{ev.id}]" for ev in event_data]

        if not list_data:
            list_data = ["No hay turnos"]
        else:
            list_data.insert(0, "Elegir turno")
        [self.turnos_box.insert(END, ev_data) for ev_data in list_data]

    def avanzar_dia(self):
        """ AVANZAR 1 DIA """
        cant_dias = DateHandler().days_in_month(self.mes, self.anio)
        self.dia += 1
        if self.dia > cant_dias:
            self.dia = 1
            self.mes += 1
            if self.mes > 12:
                self.mes = 1
                self.anio += 1
        self.configurar_encabezado()
        self.turnos_box.destroy()
        self.crear_listbox_citas()
        self.configurar_event_box()

        if self.extension:
            self.extension.main_frame.destroy()
            self.extension = None

    def retroceder_dia(self):
        """ RETROCEDER 1 DIA """
        self.dia -= 1
        if self.dia < 1:
            self.mes -= 1
            if self.mes < 1:
                self.anio -= 1
            self.dia = DateHandler().days_in_month(self.mes, self.anio)
        self.configurar_encabezado()
        self.turnos_box.destroy()
        self.crear_listbox_citas()
        self.configurar_event_box()

        if self.extension:
            self.extension.main_frame.destroy()
            self.extension = None

    def agregar_turno(self):
        """ AGREGAR TURNO """
        if not self.extension:
            self.confirmation.destroy() if self.confirmation else None
            self.extension = True
            self.extension = TurnoNuevo(self, self.dia, self.mes, self.anio, self.configurar_event_box)

    def eliminar_turno(self):
         if not self.extension:
            if not self.turnos_box.curselection():
                if self.confirmation:
                    self.confirmation.destroy()
                self.confirmation = Label(self, text="Elija un turno", font="Courier 15")
                self.confirmation.grid(row=self.grid_size()[1], column=0, columnspan=4, pady=10)
                return

            self.confirmation.destroy() if self.confirmation else None

            selection = self.turnos_box.get(self.turnos_box.curselection()).strip()
            if selection not in ["No hay turnos", "Elija un turno"]:
                self.extension = True
                str_id = selection.split(" ")[-1]
                int_id = int(str_id[1:-1])
                self.extension = TurnoEliminar(self, int_id, self.configurar_event_box)

    def cambiar_turno(self):
        if not self.extension:
            if not self.turnos_box.curselection():
                if self.confirmation:
                    self.confirmation.destroy()
                self.confirmation = Label(self, text="Elija un turno", font="Courier 15")
                self.confirmation.grid(row=self.grid_size()[1], column=0, columnspan=4, pady=10)
                return

            self.confirmation.destroy() if self.confirmation else None

            selection = self.turnos_box.get(self.turnos_box.curselection()).strip()
            if selection not in ["No hay turnos", "Elija un turno"]:
                self.extension = True
                str_id = selection.split(" ")[-1]
                int_id = int(str_id[1:-1])
                self.extension = TurnoModificar(self, int_id, self.configurar_event_box)