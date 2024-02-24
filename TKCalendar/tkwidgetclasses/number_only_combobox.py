from tkinter.ttk import Combobox, Style
from tkinter import Tk, Toplevel

class NumberOnlyCombobox(Combobox):
    
    def __init__(self, master: Tk or Toplevel, base_value: str or int, max_length: int = None, **kw):
        """ Constructs a Tkinter Entry """
        super().__init__(master=master, **kw)
        #self.style = Style()
        #self.style.theme_use("clam")
        self.max_length = max_length
        self.base_value = base_value

        self.bind("<FocusOut>", self._check_value)

    def set_style(self, fbg: str = "white", bg: str = "white"):
        self.style.configure("TCombobox", fieldbackground=fbg, background=bg)

    def _check_value(self, e):
        try:
            int(self.get())
        except ValueError:
            self.set(self.base_value)

        if self.max_length:
            if len(self.get()) > self.max_length:
                self.set(self.base_value)


