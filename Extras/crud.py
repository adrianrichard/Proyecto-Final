import tkinter as tk
from client.gui_app import Frame
def main():
    root=tk.Tk()
    root.title('CRUD paciente')
    root.resizable(0,0)
    app = Frame(root=root)
    frame=tk.Frame(root)
    frame.pack()
    frame.config(width=480, height=320, bg='green')
    app.mainloop()

if __name__ == '__main__':
    main()
