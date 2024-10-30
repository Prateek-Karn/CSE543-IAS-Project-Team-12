# drawing_app.py
import tkinter as tk
from PIL import Image, ImageDraw
import numpy as np

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=280, height=280, bg='white')
        self.canvas.pack()

        # PIL Image and Draw object
        self.image = Image.new("L", (280, 280), 'white')
        self.draw = ImageDraw.Draw(self.image)

        # Bind the mouse motion to the paint function
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    def paint(self, event):
        x1, y1 = (event.x - 4), (event.y - 4)
        x2, y2 = (event.x + 4), (event.y + 4)
        self.canvas.create_oval(x1, y1, x2, y2, fill='black')
        self.draw.ellipse([x1, y1, x2, y2], fill='black')

    def reset(self, event):
        pass

    def get_image_data(self):
        img = self.image.resize((28, 28))
        img_array = np.array(img) / 255.0
        return img_array.reshape(28, 28)
