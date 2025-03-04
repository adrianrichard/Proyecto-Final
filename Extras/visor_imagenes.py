from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import tkinter.filedialog as tk_file
import os
root = tk.Tk()

root.geometry('800x550')

root.title('Tkinter Hub')

def display_image(index):
    image_display_lb.config(image=images_list[index][1])

images_list=[]
images_vars=[]

def load_images(canvas):
    
    dir_path = tk_file.askdirectory()
    images_files = os.listdir(dir_path)
    for r in range(0, len(images_files)):
        image = Image.open(dir_path + '/' + images_files[r])
        ancho, alto = image.size
        ratio = ancho / alto
        if ratio > 1:
            new_altura = 300
            new_ancho = int(ratio * new_altura)
        elif ratio <= 1:
            new_ancho = 400
            new_altura = int(ratio * new_ancho)
                            
        image_resize = image.resize((new_ancho, new_altura))

        images_list.append([
            ImageTk.PhotoImage(Image.open(dir_path + '/' + images_files[r]).resize((50, 50), Image.Resampling.LANCZOS)),
            ImageTk.PhotoImage(image_resize, Image.Resampling.LANCZOS)
            ])
        images_vars.append(f'imag_{r}')

    for n in range(len(images_vars)):
        globals()[images_vars[n]] = tk.Button(slider, image=images_list[n][0], bd=0, command= lambda n=n: display_image(n))
        globals()[images_vars[n]].pack(side=tk.LEFT)
    n =len(images_list)+1
    canvas.config(scrollregion=(0,0,n*50,500))



image_display_lb = tk.Label(root)
image_display_lb.pack(anchor=tk.CENTER)
canvas = tk.Canvas(root, height=60, width=500, scrollregion=(0,0,500,500))
canvas.pack(side=tk.BOTTOM, fill=tk.X)
x_scroll_bar = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=canvas.xview)
x_scroll_bar.pack(side=tk.BOTTOM, fill=tk.X)
print(len(images_list))
canvas.config(xscrollcommand=x_scroll_bar.set)
canvas.bind('<Configure>', lambda e: canvas.bbox('all'))
slider = tk.Frame(canvas)
canvas.create_window((0, 0), window=slider, anchor=tk.NW)
#print(len(images_vars))

menu_btn = tk.Button(root, text= 'Open Folder', bd=0, font=('Bold', 15), command=load_images(canvas))
menu_btn.pack( side=tk.TOP, anchor=tk.W, padx=20, pady=20)

root.mainloop()