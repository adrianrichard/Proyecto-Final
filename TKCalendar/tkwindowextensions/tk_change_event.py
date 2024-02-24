from tkinter import Label, Tk, Toplevel, E, S, Frame, NSEW, PhotoImage, Button, CENTER, FLAT, END
from tkinter.ttk import Combobox, Style
from events.events import Event
from events.eventdbcontroller import EventController
from tkwidgetclasses.number_only_combobox import NumberOnlyCombobox
from tkwidgetclasses.textfilled_entry import TextFilledEntry

class TKChangeEvent:
   
    def __init__(self, root_window: Tk or Toplevel, id: int, callback: callable = None):
        self.root = root_window
        self.id = id
        self.event = None
        self.grid_row_start = root_window.grid_size()[1]
        self.column_count = root_window.grid_size()[0]
        self.callback = callback

        self.confirm = None
        self.deny = None

        self._create_main_frame()
        self._make_header()
        self._make_title_entry()
        self._make_time_widgets()
        self._make_category_combobox()
        self._make_confirm_deny_buttons()
        self._get_event_data()
        self._configure_time()
        self._configure_title()
        self._configure_category()

    def _create_main_frame(self):
        self.border_frame = Frame(self.root, bg=self.root["bg"])
        self.border_frame.grid(row=self.grid_row_start, column=0, columnspan=3, sticky=NSEW)
        self.main_frame = Frame(self.root, bg="#BDC1BE")
        self.main_frame.grid(row=self.grid_row_start, column=0, columnspan=3, sticky=NSEW, padx=10, pady=10)

    def _make_header(self):
        Label(self.main_frame, text="MODIFICAR CITA", font="Courier 18 underline", bg="#BDC1BE").grid(row=0, column=0, columnspan=2, pady=5, sticky=S)

    def _make_title_entry(self):
        self.title_entry = TextFilledEntry(self.main_frame, "Title", justify=CENTER)
        self.title_entry.grid(pady=8)

    def _make_time_widgets(self):
        time_frame = Frame(self.main_frame)
        time_frame.grid(pady=8)

        hour_nums = [ 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]

        self.hour_selector = Combobox(time_frame, values=hour_nums, justify=CENTER, background="white")
        self.hour_selector.set("Hora")
        self.hour_selector.grid(row=0, column=0)

        minute_nums = ["00"]
        minute_nums.extend([str(num * 10) for num in range(1, 6)])
        self.minute_selector =Combobox(time_frame, values=minute_nums, justify=CENTER, background="white")
        self.minute_selector.set("00")
        self.minute_selector.grid(row=0, column=1, sticky=E)

        self.hour_selector.bind("<<ComboboxSelected>>", lambda e: self.main_frame.focus())
        self.minute_selector.bind("<<ComboboxSelected>>", lambda e: self.main_frame.focus())

    def _make_category_combobox(self):
        categories = ["Consulta", "Extracción", "Tratamiento de conducto", "Reparación"]
        self.category_selector = Combobox(self.main_frame, values=categories, justify=CENTER, background="white")
        self.category_selector.grid(pady=8)
        self.category_selector.set("Categoria")
        self.category_selector.bind("<<ComboboxSelected>>", lambda e: self.main_frame.focus())

    def _make_confirm_deny_buttons(self):
        button_frame = Frame(self.main_frame, bg="#BDC1BE")
        button_frame.grid(pady=8)

        self.confirm_img = PhotoImage(file="img/confirm.png")
        self.confirm = Button(button_frame, image=self.confirm_img, command=self._change_event, relief=FLAT, bg="#BDC1BE")
        self.confirm.grid(row=0, column=0)

        self.cancel_img = PhotoImage(file="img/deny.png")
        self.cancel = Button(button_frame, image=self.cancel_img, command=self._cancel_event, relief=FLAT, bg="#BDC1BE")
        self.cancel.grid(row=0, column=1)

    def _get_event_data(self):
        self.event = EventController.find_by_id(self.id)

    def _configure_title(self):
        self.title_entry.delete(0, END)
        self.title_entry.insert(0, self.event.title)

    def _configure_time(self):
        self.hour_selector.set(self.event.time_hours)
        self.minute_selector.set(self.event.time_minutes)

    def _configure_category(self):
        if self.event.category:
            self.category_selector.set(self.event.category)

    def _configure_rows_cols(self):
        """ Configure rows to 1:1 weight """
        [self.main_frame.rowconfigure(i, weight=1) for i in range(self.main_frame.grid_size()[1])]
        [self.main_frame.columnconfigure(i, weight=1) for i in range(self.main_frame.grid_size()[0])]

    def _change_event(self):
        ev_dict = {
            "title": self.title_entry.get(),
            "time_hours": self.hour_selector.get(),
            "time_minutes": self.minute_selector.get(),
            "category": self.category_selector.get()
        }

        style = Style()
        if ev_dict["time_hours"] == "Hour" or ev_dict["time_minutes"] == "Minutes" or ev_dict["title"] == "Title":
            style.configure("TCombobox", fieldbackground="red", background="white")
            self.title_entry.configure(bg="red")
            self.warning = Label(self.main_frame, text="Complete la información", bg="#BDC1BE", fg="red", font="Helvetica 13")
            self.warning.grid(row=6, column=0, pady=10)
            return

        """ Reconfigure red zones if triggered """
        self.title_entry.configure(bg="white")
        style.configure("TCombobox", fieldbackground="white", background="white")

        event = Event.create(ev_dict)

        self.main_frame.destroy()
        if EventController.update_event(event, self.id):
            self.root.confirmation = Label(self.root, text="¡Cita modificada!", font="Courier 15")
        else:
            self.root.confirmation = Label(self.root, text="Ocurrio un error", font="Courier 15")

        self.root.confirmation.grid(row=self.grid_row_start+1, column=1, pady=10)
        self.root.extension = None
        self.callback()

    def _cancel_event(self):
        self.main_frame.destroy()
        self.root.extension = None
        self.callback()