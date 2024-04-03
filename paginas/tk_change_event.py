from tkinter import *
from tkinter.ttk import Combobox, Style
import util.generic as utl
from paginas.events.events import Event
from paginas.events.eventdbcontroller import EventController
#from tkwidgetclasses.textfilled_entry import TextFilledEntry

class TurnoModificar:
   
    def __init__(self, root_window: Tk or Toplevel, id: int, callback: callable = None):
        self.root = root_window
        self.id = id
        self.event = None
        self.grid_row_start = root_window.grid_size()[1]
        self.column_count = root_window.grid_size()[0]
        self.callback = callback

        self.confirm = None
        self.deny = None

        self.crear_main_frame()
        self.crear_encabezado()
        self.crear_nombre_entry()
        self.crear_tiempo_widgets()
        self.crear_prestacion_combobox()
        self.crear_botones()
        self.obtener_info_turno()
        self.configurar_tiempo()
        self.configurar_nombre()
        self.configurar_prestacion()
        self.configurar_filas_columnas()

    def crear_main_frame(self):
        self.border_frame = Frame(self.root, bg=self.root["bg"])
        self.border_frame.grid(row=self.grid_row_start, column=0, columnspan=self.column_count, sticky=NSEW)
        self.main_frame = Frame(self.root, bg="#BDC1BE")
        self.main_frame.grid(row=self.grid_row_start, column=0, columnspan=self.column_count, sticky=NSEW, padx=10, pady=10)

    def crear_encabezado(self):
        Label(self.main_frame, text="MODIFICAR TURNO", font="Courier 12 underline", bg="#BDC1BE").grid(pady=5)

    def crear_nombre_entry(self):
        self.nombre_entry = Entry(self.main_frame, justify=CENTER)
        self.nombre_entry.grid(pady=8)

    def crear_tiempo_widgets(self):
        tiempo_frame = Frame(self.main_frame)
        tiempo_frame.grid(pady=8)

        horas = [ 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]

        self.selector_hora = Combobox(tiempo_frame, values=horas, state="readonly", justify=CENTER, background="white")
        self.selector_hora.set("Hora")
        self.selector_hora.grid(row=0, column=0)

        minutos = ["00"]
        minutos.extend([str(num * 10) for num in range(1, 6)])
        self.selector_minuto =Combobox(tiempo_frame, values=minutos, state="readonly", justify=CENTER, background="white")
        self.selector_minuto.set("00")
        self.selector_minuto.grid(row=0, column=1, sticky=E)

        self.selector_hora.bind("<<ComboboxSelected>>", lambda e: self.main_frame.focus())
        self.selector_minuto.bind("<<ComboboxSelected>>", lambda e: self.main_frame.focus())

    def crear_prestacion_combobox(self):
        prestaciones = ["Consulta", "Extracción", "Tratamiento de conducto", "Reparación"]
        self.selector_prestacion = Combobox(self.main_frame, state="readonly", values=prestaciones, width=25, justify=CENTER, background="white")
        self.selector_prestacion.grid(pady=8)
        self.selector_prestacion.set("Prestación")
        self.selector_prestacion.bind("<<ComboboxSelected>>", lambda e: self.main_frame.focus())

    def crear_botones(self):
        button_frame = Frame(self.main_frame, bg="#BDC1BE")
        button_frame.grid(pady=8)
        self.confirm_img = utl.leer_imagen("confirm.png", (70,50))
        Button(button_frame, image=self.confirm_img, command=self.cambiar_turno, relief=FLAT, bg="#BDC1BE").grid(row=0, column=0)

        self.cancelar_img = utl.leer_imagen("deny.png", (70,50))
        Button(button_frame, image=self.cancelar_img, command=self.cancelar, relief=FLAT, bg="#BDC1BE").grid(row=0, column=1)

    def obtener_info_turno(self):
        self.event = EventController.find_by_id(self.id)

    def configurar_nombre(self):
        self.nombre_entry.delete(0, END)
        self.nombre_entry.insert(0, self.event.title)

    def configurar_tiempo(self):
        self.selector_hora.set(self.event.time_hours)
        self.selector_minuto.set(self.event.time_minutes)

    def configurar_prestacion(self):
        if self.event.category:
            self.selector_prestacion.set(self.event.category)

    def configurar_filas_columnas(self):
        """ Configure rows to 1:1 weight """
        [self.main_frame.rowconfigure(i, weight=1) for i in range(self.main_frame.grid_size()[1])]
        [self.main_frame.columnconfigure(i, weight=1) for i in range(self.main_frame.grid_size()[0])]

    def cambiar_turno(self):
        ev_dict = {
            "title": self.nombre_entry.get(),
            "time_hours": self.selector_hora.get(),
            "time_minutes": self.selector_minuto.get(),
            "category": self.selector_prestacion.get()
        }

        style = Style()
        if ev_dict["time_hours"] == "Hour" or ev_dict["time_minutes"] == "Minutes" or ev_dict["title"] == "Title":
            style.configure("TCombobox", fieldbackground="red", background="white")
            self.nombre_entry.configure(bg="red")
            Label(self.main_frame, text="Complete la información", bg="#BDC1BE", fg="red", font="Helvetica 13").grid(row=6, column=0, pady=10)
            return

        """ Reconfigure red zones if triggered """
        self.nombre_entry.configure(bg="white")
        style.configure("TCombobox", fieldbackground="white", background="white")

        event = Event.create(ev_dict)

        self.main_frame.destroy()
        if EventController.update_event(event, self.id):
            self.root.confirmation = Label(self.root, text="¡Turno modificado!", font="Courier 15")
        else:
            self.root.confirmation = Label(self.root, text="Ocurrio un error", font="Courier 15")

        self.root.confirmation.grid(row=self.grid_row_start+1, column=0, columnspan=4, pady=10)
        self.root.extension = None
        self.callback()

    def cancelar(self):
        self.main_frame.destroy()
        self.root.extension = None
        self.callback()