import sys
import os
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import numpy as np

sys.path.append(os.path.join(os.getcwd(), 'Noise_Generator'))

import noise_generator5 as ng5


class DrawingApp:
    def __init__(self, root, noisy_image):
        self.root = root
        self.noisy_image = noisy_image
        self.image_with_noise = Image.open(noisy_image)  # Load the noisy background image

        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()

        #converting the PIL image to kinter image format to display in the kinter app
        self.tk_noise_image = ImageTk.PhotoImage(self.image_with_noise)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_noise_image)

        self.drawing_tool = "pencil"
        self.canvas.bind("<B1-Motion>", self.paint)

        # bascially this is going to update everytime the user draws. i.e. the user is going to draw on noise and it's going to come out without noise.
        self.image_no_noise = Image.new("RGB", (500, 500), "white")
        self.draw_no_noise = ImageDraw.Draw(self.image_no_noise)

        # Add a button to save the drawing
        save_button = tk.Button(self.root, text="Save Drawing", command=self.save_image)
        save_button.pack()

    def paint(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)

        # Draw on the canvas
        self.canvas.create_oval(x1, y1, x2, y2, fill="black", width=5)

        # Save the stroke to the image without noise
        self.draw_no_noise.ellipse([x1, y1, x2, y2], fill="black")

    def save_image(self):
        # Save the user's drawing without noise
        file_path_no_noise = "plain_user_drawing.png"
        self.image_no_noise.save(file_path_no_noise)

        print(f"Drawings saved as {file_path_no_noise} and {file_path_with_noise}")


# Function to add noise and then let the user draw on it
def add_noise_to_drawing():
    # Step 1: Generate a blank image (500x500) and apply noise
    blank_image = Image.new("RGB", (500, 500), "white")
    blank_image_path = "blank_image.png"
    blank_image.save(blank_image_path)

    noisy_image = "noisy_background.png"
    ng5.add_noise(blank_image_path, noisy_image)  # Generate the noisy background

    # Step 2: Start the drawing app with the noisy background
    root = tk.Tk()
    app = DrawingApp(root, noisy_image)
    root.mainloop()


add_noise_to_drawing()
