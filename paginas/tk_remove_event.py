from tkinter import *
import util.generic as utl
from paginas.events.eventdbcontroller import EventController

class TurnoEliminar:
   
    def __init__(self, ventana: Tk or Toplevel, id: int, callback: callable = None):
        
        self.root = ventana
        self.id = id
        self.event = None
        self.grid_row_start = ventana.grid_size()[1]
        self.column_count = ventana.grid_size()[0]
        self.callback = callback

        self.confirm = None
        self.deny = None

        self.crear_main_frame()
        self.crear_header()
        self.obtener_info_evento()
        self.crear_data_display()
        self.crear_botones()
        self.configurar_filas_columnas()

    def crear_main_frame(self):
        self.border_frame = Frame(self.root, bg=self.root["bg"])
        self.border_frame.grid(row=self.grid_row_start, column=0, columnspan=self.column_count, sticky=NSEW)
        self.main_frame = Frame(self.root, bg="#BDC1BE")
        self.main_frame.grid(row=self.grid_row_start, column=0, columnspan=self.column_count, sticky=NSEW, padx=10, pady=10)

    def crear_header(self):
        Label(self.main_frame, text="ELIMINAR TURNO", font="Courier 12 underline", bg="#BDC1BE").grid(row=0, column=1, pady=5, sticky=S)

    def obtener_info_evento(self):
        self.event = EventController.find_by_id(self.id)

    def crear_data_display(self):
        event_data_frame = Frame(self.main_frame, bg="#D1D6D3", relief=GROOVE)
        event_data_frame.grid(row=1, column=0, columnspan=3)
        
        e = self.event
        event_data = f"Paciente: {e.title}\n" \
                     f"Fecha: {e.day}/{e.month}/{e.year}\n" \
                     f"Horario: {e.time_hours}:{e.time_minutes}\n" \
                     f"Prestación: {e.category}" \

        Label(event_data_frame, bg="#D1D6D3", text=event_data, font="Helvetica 12").grid(row=0, column=0, columnspan=3, ipady=20, ipadx=20)

    def crear_botones(self):
        self.confirm_img = utl.leer_imagen("confirm.png", (70,50))
        Button(self.main_frame, image=self.confirm_img, command=self.eliminar_turno, relief=FLAT, bg="#BDC1BE").grid(row=2, column=0)

        self.cancelar_img = utl.leer_imagen("deny.png", (70,50))
        Button(self.main_frame, image=self.cancelar_img, command=self.cancelar, relief=FLAT, bg="#BDC1BE").grid(row=2, column=2)

    def configurar_filas_columnas(self):
        """ Configure rows to 1:1 weight """
        [self.main_frame.rowconfigure(i, weight=1) for i in range(self.main_frame.grid_size()[1])]
        [self.main_frame.columnconfigure(i, weight=1) for i in range(self.main_frame.grid_size()[0])]

    def cancelar(self):
        self.main_frame.destroy()
        self.root.extension = None
        self.callback()

    def eliminar_turno(self):
        if self.root.confirmation:
            self.root.confirmation.destroy()
        self.main_frame.destroy()

        if EventController.remove_doc(self.id):
            self.root.confirmation = Label(self.root, text="¡Turno eliminado!", font="Courier 15")
        else:
            self.root.confirmation = Label(self.root, text="Ocurrió un error", font="Courier 15")

        self.root.confirmation.grid(row=6, column=0, columnspan=4, pady=10)
        self.root.extension = None
        self.callback()