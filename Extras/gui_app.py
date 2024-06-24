import tkinter as tk
from tkinter import ttk, messagebox
class App(tk.Frame):
   def __init__(self, root = None):
        super().__init__(root, width=480, height=320)
        self.root = tk.Tk()
        self.root.title('DENTALMATIC')
        self.root.geometry('500x500')
        self.root.resizable(width= 0, height= 0)
        self.root.mainloop()