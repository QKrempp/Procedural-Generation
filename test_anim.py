from tkinter import *
from PIL import Image, ImageTk
import time

root = Tk()

images = []  # to hold the newly created image

def create_circle(x1, y1, x2, y2, **kwargs):
    if 'alpha' in kwargs:
        alpha = int(kwargs.pop('alpha') * 255)
        fill = kwargs.pop('fill')
        fill = root.winfo_rgb(fill) + (alpha,)
        image = Image.new('RGBA', (x2-x1, y2-y1), fill)
        images.append(ImageTk.PhotoImage(image))
        canvas.create_image(x1, y1, image=images[-1], anchor='nw')
    canvas.create_oval(x1, y1, x2, y2, **kwargs)

canvas = Canvas(width=500, height=400)
canvas.pack()

create_circle(10, 10, 200, 100, fill='blue')
create_circle(50, 50, 250, 150, fill='green', alpha=.5)
i = 0


while True:
    create_circle(80+i, 80+i, 150+i, 120+i, fill='#800000', alpha=.8)
    i += 10
    root.update()
    time.sleep(1)


root.mainloop()
