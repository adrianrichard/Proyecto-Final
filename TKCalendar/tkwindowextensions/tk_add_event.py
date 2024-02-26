from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Style
from events.events import Event
from events.eventdbcontroller import EventController

class TurnoNuevo:

    def __init__(self, ventana: Tk or Toplevel, dia: int, mes: int, anio: int, callback: callable = None):

        self.root = ventana
        
        self.dia = dia
        self.mes = mes
        self.anio = anio
        self.grid_row_start = ventana.grid_size()[1]
        self.column_count = ventana.grid_size()[0]
        self.callback = callback

        self.crear_main_frame()
        self.crear_header()
        self.crear_nombre_entry()
        self.crear_tiempo_widgets()
        self.crear_prestacion_combobox()
        self.crear_botones()

    def crear_main_frame(self):
        self.border_frame = Frame(self.root, bg=self.root["bg"])
        self.border_frame.grid(row=self.grid_row_start, column=0, columnspan=self.column_count, sticky=NSEW)
        self.main_frame = Frame(self.root, bg="#BDC1BE")
        self.main_frame.grid(row=self.grid_row_start, column=0, columnspan=self.column_count, sticky=NSEW, padx=10, pady=10)

    def crear_header(self):
        Label(self.main_frame, text="AGREGAR TURNO", font="Courier 12 underline", bg="#BDC1BE").pack(pady=8)

    def crear_nombre_entry(self):
        self.nombre_entry = Entry(self.main_frame, justify=CENTER)
        self.nombre_entry.pack(pady=8)
        self.nombre_entry.insert(0, "Paciente")
        self.nombre_entry.focus_set()  # Not so sure about this yet

    def crear_tiempo_widgets(self):
        tiempo_frame = Frame(self.main_frame)
        tiempo_frame.pack(pady=8)

        horas = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
        self.selector_hora = Combobox(tiempo_frame, values=horas, state="readonly", justify=CENTER, background="white")
        self.selector_hora.set("Hora")
        self.selector_hora.grid(row=0, column=0)

        minutos = ["00"]
        minutos.extend([str(num * 10) for num in range(1, 6)])
        self.selector_minuto = Combobox(tiempo_frame, state="readonly", values=minutos, justify=CENTER, background="white")
        self.selector_minuto.set("00")
        self.selector_minuto.grid(row=0, column=1, sticky=E)
        self.selector_hora.bind("<<ComboboxSelected>>", lambda e: self.main_frame.focus())
        self.selector_minuto.bind("<<ComboboxSelected>>", lambda e: self.main_frame.focus())

    def crear_prestacion_combobox(self):
        prestaciones = ["Consulta", "Extracción", "Tratamiento de conducto", "Reparación"]
        self.selector_prestacion = Combobox(self.main_frame, state="readonly", values=prestaciones, width=25, justify=CENTER, background="white")
        self.selector_prestacion.pack(pady=8)
        self.selector_prestacion.set("Prestación")
        self.selector_prestacion.bind("<<ComboboxSelected>>", lambda e: self.main_frame.focus())

    def crear_botones(self):
        button_frame = Frame(self.main_frame, bg="#BDC1BE")
        button_frame.pack(pady=10)

        self.confirm_img = PhotoImage(file="img/confirm.png")
        Button(button_frame, image=self.confirm_img, command=self.agregar_turno, relief=FLAT, bg="#BDC1BE").grid(row=0, column=0)

        self.cancelar_img = PhotoImage(file="img/deny.png")
        Button(button_frame, image=self.cancelar_img, command=self.cancelar, relief=FLAT, bg="#BDC1BE").grid(row=0, column=1)

    def agregar_turno(self):
        
        ev_dict = {
            "day": self.dia,
            "year": self.anio,
            "month": self.mes,
            "title": self.nombre_entry.get(),
            "time_hours": self.selector_hora.get(),
            "time_minutes": self.selector_minuto.get(),
            "category": self.selector_prestacion.get()
        }

        style = Style()
        if ev_dict["time_hours"] == "Hora" or ev_dict["title"] == "Paciente":
            style.configure("TCombobox", fieldbackground="red", background="white")
            self.nombre_entry.configure(bg="red")
            messagebox.showinfo(message="Completar campos", title="Advertencia")
            return

        """ Reconfigure red zones if triggered """
        self.nombre_entry.configure(bg="white")
        style.configure("TCombobox", fieldbackground="white", background="white")

        e = Event.create(ev_dict)

        self.main_frame.destroy()

        if self.root.confirmation:
            self.root.confirmation.destroy()

        if EventController.insert(e):
            self.root.confirmation = Label(self.root, text="¡Turno guardado!", font="Courier 15")
        else:
            self.root.confirmation = Label(self.root, text="Ocurrió un error", font="Courier 15")

        self.root.confirmation.grid(row=self.grid_row_start+1, column=0, columnspan=4, pady=10)
        self.root.extension = None
        self.callback()

    def cancelar(self):
        self.main_frame.destroy()
        self.root.extension = None
        self.callback()