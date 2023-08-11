import tkinter as tk
from PIL import ImageTk, Image
import tkinter.filedialog as tk_file
import os
root = tk.Tk()

root.geometry('580x550')

root.title('Tkinter Hub')

def display_image(index):
    image_display_lb.config(image=images_list[index][1])
    
def popup_menu(e):
    menu_bar.tk_popup( x=e.x_root, y=e.y_root)

images_list=[]
images_vars=[]

def load_images():
    dir_path = tk_file.askdirectory()
    images_files = os.listdir(dir_path)
    for r in range(0, len(images_files)):
        images_list.append([
            ImageTk.PhotoImage(Image.open(dir_path + '/' + images_files[r]).resize((50, 50), Image.Resampling.LANCZOS)),
            ImageTk.PhotoImage(Image.open(dir_path + '/'+ images_files[r]).resize((480,360), Image.Resampling.LANCZOS))
        
        ])
        images_vars.append(f'imag_{r}')
    
    for n in range(len(images_vars)):
        globals()[images_vars[n]] = tk.Button(slider, image=images_list[n][0], bd=0, command= lambda n=n: display_image(n))
        globals()[images_vars[n]].pack(side=tk.LEFT)
    
menu_btn = tk.Button(root, text= '≡', bd=0, font=('Bold', 15))
menu_btn.pack( side=tk.TOP, anchor=tk.W, padx=20, pady=20)
menu_btn.bind('<Button>', popup_menu)

menu_bar = tk.Menu(root, tearoff=False)

menu_bar.add_command(label='Open Folder', command=load_images)

image_display_lb = tk.Label(root)
image_display_lb.pack(anchor=tk.CENTER)
canvas = tk.Canvas(root, height=60, width=500)
canvas.pack(side=tk.BOTTOM, fill=tk.X)
x_scroll_bar = tk.Scrollbar(root, orient=tk.HORIZONTAL)
x_scroll_bar.pack(side=tk.BOTTOM, fill=tk.X)
x_scroll_bar.config(command=canvas.xview)
canvas.config(xscrollcommand=x_scroll_bar.set)
canvas.bind('<Configure>', lambda e: canvas.bbox('all'))
slider = tk.Frame(canvas)
canvas.create_window((0, 0), window=slider, anchor=tk.NW)

root.mainloop()