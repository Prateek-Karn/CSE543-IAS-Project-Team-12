import sys
import os
import tkinter as tk
from PIL import Image, ImageDraw
import numpy as np

sys.path.append(os.path.join(os.getcwd(), 'Noise_Generator')) #this was needed since noise generator was in the sub directory and this function is in the main directory

import noise_generator5 as ng5


#making a simple drawing interface.
class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(self.root, bg="white", width=500, height=500)
        self.canvas.pack()
        self.drawing_tool = "pencil"
        self.canvas.bind("<B1-Motion>", self.paint)
        self.image = Image.new("RGB", (500, 500), "white")
        self.draw = ImageDraw.Draw(self.image)

        #this will add a button and save the  drawing.
        save_button = tk.Button(self.root, text="Save Drawing", command=self.save_image)
        save_button.pack()

    def paint(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, fill="black", width=5)
        self.draw.ellipse([x1, y1, x2, y2], fill="black")
    def save_image(self):
        file_path = "user_drawn_image"
        self.image.save(file_path + ".png")
        print(f"Drawing saved as {file_path}.png")

# merging with noise generator
def add_noise_to_drawing():
    root = tk.Tk() #this use to create the main window. every kinter needs it.
    app = DrawingApp(root)
    root.mainloop()

    #naming the input and output images.
    input_image = "user_drawn_image.png"
    output_image = "noisy_user_image.png"
    
    #calling our function
    ng5.add_noise(input_image, output_image)


add_noise_to_drawing() #this will start the tkinter as in this function we have tk.Tk()