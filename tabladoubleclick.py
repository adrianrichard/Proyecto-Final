import tkinter as tk
from tkinter import ttk

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.tree = ttk.Treeview()
        self.tree.pack()
        self.tree['columns'] = ('Nombre', 'D.N.I.', 'Teléfono', 'Obra Social')
        for i in range(10):
            self.tree.insert("", "end", text="Item %s" % i, values=(i, (i+1)*103046,(i+1)*100))
        self.tree.bind("<Double-1>", self.OnDoubleClick)
        self.root.mainloop()

    def OnDoubleClick(self, event):
        item = self.tree.focus()
        self.data = self.tree.item(item)
        self.dni_paciente=self.data['values'][1]
        print("you clicked on", self.dni_paciente)

if __name__ == "__main__":
    app = App()