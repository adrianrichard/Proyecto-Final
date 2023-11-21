import tkinter as tk
def main():
    root=tk.Tk()
    root.title('CRUD paciente')
    root.resizable(0,0)
    frame=tk.Frame(root)
    frame.pack()
    frame.config(width=480, height=320, bg='green')
    root.mainloop()

if __name__ == '__main__':
    main()
