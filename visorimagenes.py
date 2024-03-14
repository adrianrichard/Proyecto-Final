from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import tkinter.filedialog as tk_file
import os
images_list=[]
images_vars=[]  
class ImageGalleryApp:
    def __init__(self, root):
        
        def display_image(index):
            image_display_lb.config(image=images_list[index][1], height=360)

        def load_images():
            images_list.clear()
            images_vars.clear()

            dir_path = tk_file.askdirectory()
            images_files = os.listdir(dir_path)
          
            for r in range(0, len(images_files)):
                image = Image.open(dir_path + '/' + images_files[r])
                ancho, alto = image.size
                ratio = ancho / alto
                #print(ancho, alto, ratio)
                if ratio >=1:
                    if (alto*ratio) >= 300:
                        new_ancho = 400
                        new_altura = int(new_ancho/ratio)                    
                    else:
                        new_altura = 300
                        new_ancho = int(ratio * new_altura)
                elif ratio <1:        
                    if (ancho*ratio) >= 400:
                        new_altura = 300
                        new_ancho = int(ratio * new_altura)
                    else:
                        new_ancho = 400
                        new_altura = int(ratio*new_ancho)                
                #print(new_ancho, new_altura)
                image_resize = image.resize((new_ancho, new_altura))

                images_list.append([
                    ImageTk.PhotoImage(Image.open(dir_path + '/' + images_files[r]).resize((50, 50), Image.Resampling.LANCZOS)),
                    ImageTk.PhotoImage(image_resize, Image.Resampling.LANCZOS)
                    ])
                images_vars.append(f'imag_{r}')

            for n in range(len(images_vars)):
                globals()[images_vars[n]] = tk.Button(slider, image=images_list[n][0], bd=0, command= lambda n=n: display_image(n))
                globals()[images_vars[n]].grid(row=2, column=n)

        menu_btn = tk.Button(root, text= 'Abrir carpeta', font=('Arial', 11,'bold'), bg= '#1F704B', bd= 2, borderwidth= 2, command=load_images)
        menu_btn.grid( row=0, column=1)        
        image_display_lb = tk.Label(root, height=20, bg='gray90')
        image_display_lb.grid(row=1, column=0, columnspan=2, pady=0)
        canvas = tk.Canvas(root, height=50, width=500)
        canvas.grid(row=3, column=0, columnspan=2, pady=0)
        #x_scroll_bar = tk.Scrollbar(root, orient=tk.HORIZONTAL)
        #x_scroll_bar.grid(column = 0, row = 3, columnspan=2, sticky='ns')
        #x_scroll_bar.config(borderwidth=2, command=canvas.xview)
        #canvas.config(xscrollcommand=x_scroll_bar.set)
        canvas.bind('<Configure>', lambda e: canvas.bbox('all'))
        slider = tk.Frame(canvas)
        canvas.create_window((0, 0), window=slider, anchor=tk.NW)
    
    def configurar_filas_columnas(self, root):
        """ Configura filas y columnas para expandandirlas al tamaño de la ventana """
        [root.rowconfigure(i, weight=1) for i in range(root.grid_size()[1])]
        [root.columnconfigure(i, weight=1) for i in range(root.grid_size()[0])]

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageGalleryApp(root)
    root.mainloop()
