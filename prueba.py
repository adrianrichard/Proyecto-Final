import Tkinter

def funcion():
    otra_ventana = Tkinter.Toplevel(root)
    root.iconify()

root = Tkinter.Tk()
boton = Tkinter.Button(root, text="Abrir otra ventana", command=funcion)
boton.pack()
root.mainloop()