from tkinter import Label, Tk, Toplevel, S, E, Frame, NSEW, PhotoImage, Button, CENTER, FLAT, SUNKEN
from tkinter.ttk import Combobox, Style
from events.events import Event
from events.eventdbcontroller import EventController
from tkwidgetclasses.number_only_combobox import NumberOnlyCombobox
from tkwidgetclasses.textfilled_entry import TextFilledEntry

class TKAddEventExtension:

    def __init__(self, root_window: Tk or Toplevel, day: int, month: int, year: int, callback: callable = None):

        self.root = root_window
        self.day = day
        self.month = month
        self.year = year
        self.grid_row_start = root_window.grid_size()[1]
        self.column_count = root_window.grid_size()[0]
        self.callback = callback

        self._create_main_frame()
        self._make_header()
        self._make_title_entry()
        self._make_time_widgets()
        self._make_category_combobox()
        self._make_add_cancel_buttons()

    def _create_main_frame(self):
        """ Create a frame for add event widgets """
        self.border_frame = Frame(self.root, bg=self.root["bg"])
        self.border_frame.grid(row=self.grid_row_start, column=0, columnspan=self.column_count, sticky=NSEW)
        self.main_frame = Frame(self.root, bg="#BDC1BE")
        self.main_frame.grid(row=self.grid_row_start, column=0, columnspan=self.column_count, sticky=NSEW, padx=10,
                             pady=10)

    def _make_header(self):
        Label(self.main_frame, text="AGREGAR CITA", font="Courier 12 underline", bg="#BDC1BE").pack(pady=8)

    def _make_title_entry(self):
        """ Creates title text filled entry """
        self.title_entry = TextFilledEntry(self.main_frame, "Paciente", justify=CENTER)
        self.title_entry.pack(pady=8)
        self.title_entry.focus_set()  # Not so sure about this yet

    def _make_time_widgets(self):
        """ Create time selection boxes """
        time_frame = Frame(self.main_frame)
        time_frame.pack(pady=8)

        hour_nums = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]

        self.hour_selector = NumberOnlyCombobox(time_frame, "Hora", 2, values=hour_nums, justify=CENTER, background="white")
        self.hour_selector.set("Hora")
        self.hour_selector.grid(row=0, column=0)

        minute_nums = ["00"]
        minute_nums.extend([str(num * 10) for num in range(1, 6)])
        self.minute_selector = NumberOnlyCombobox(time_frame, "Minutos", 2, values=minute_nums, justify=CENTER, background="white")
        self.minute_selector.set("00")
        self.minute_selector.grid(row=0, column=1, sticky=E)
        self.hour_selector.bind("<<ComboboxSelected>>", lambda e: self.main_frame.focus())
        self.minute_selector.bind("<<ComboboxSelected>>", lambda e: self.main_frame.focus())

    def _make_category_combobox(self):
        categories = ["Consulta", "Extracción", "Tratamiento de conducto", "Reparación"]
        self.category_selector = Combobox(self.main_frame, values=categories, justify=CENTER, background="white")
        self.category_selector.pack(pady=8)
        self.category_selector.set("Categoria")
        self.category_selector.bind("<<ComboboxSelected>>", lambda e: self.main_frame.focus())

    def _make_add_cancel_buttons(self):
        button_frame = Frame(self.main_frame, bg="#BDC1BE")
        button_frame.pack(pady=10)

        self.add_img = PhotoImage(file="img/add_call.png")
        self.add = Button(button_frame, image=self.add_img, command=self._add_event, relief=FLAT, bg="#BDC1BE")
        self.add.grid(row=0, column=0)

        self.cancel_img = PhotoImage(file="img/cancel_call.png")
        self.cancel = Button(button_frame, image=self.cancel_img, command=self._cancel_event, relief=FLAT, bg="#BDC1BE")
        self.cancel.grid(row=0, column=1)

    def _add_event(self):
        
        ev_dict = {
            "day": self.day,
            "year": self.year,
            "month": self.month,
            "title": self.title_entry.get(),
            "time_hours": self.hour_selector.get(),
            "time_minutes": self.minute_selector.get(),
            "category": self.category_selector.get()
        }

        style = Style()
        if ev_dict["time_hours"] == "Hour" or ev_dict["time_minutes"] == "Minutes" or ev_dict["title"] == "Title":
            style.configure("TCombobox", fieldbackground="red", background="white")
            self.title_entry.configure(bg="red")
            self.warning = Label(self.main_frame, text="Completar campos", bg="#BDC1BE", fg="red", font="Helvetica 13")
            self.warning.grid(row=6, column=0, pady=10)
            return

        """ Reconfigure red zones if triggered """
        self.title_entry.configure(bg="white")
        style.configure("TCombobox", fieldbackground="white", background="white")

        e = Event.create(ev_dict)

        self.main_frame.destroy()

        if self.root.confirmation:
            self.root.confirmation.destroy()

        if EventController.insert(e):
            self.root.confirmation = Label(self.root, text="¡Cita guardada!", font="Courier 10")
        else:
            self.root.confirmation = Label(self.root, text="Ocurrió un error", font="Courier 10")

        self.root.confirmation.grid(row=self.grid_row_start+1, column=1, pady=10)
        self.root.extension = None
        self.callback()

    def _cancel_event(self):
        self.main_frame.destroy()
        self.root.extension = None
        self.callback()