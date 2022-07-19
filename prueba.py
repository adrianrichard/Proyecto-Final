import tkinter

def funcion():
    otra_ventana = tkinter.Toplevel(root) #delante de la otra ventana
    #root.iconify() #minimiza a la barra de tareas

root = tkinter.Tk()
boton = tkinter.Button(root, text="Abrir otra ventana", command=funcion)
boton.pack()
root.mainloop()