import os
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import noise_generator5 as ng5

def ensure_directories_exist():
    """Create the required directory if it doesn't exist."""
    directory = 'noisegenerated_image'
    if not os.path.exists(directory):
        os.makedirs(directory)

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

        # basically this is going to update everytime the user draws. i.e. the user is going to draw on noise and it's going to come out without noise.
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

        print(f"Drawing saved as {file_path_no_noise}")

def add_noise_to_drawing(input_image_path):
    # Create the noisegenerated_image directory if it doesn't exist
    ensure_directories_exist()
    
    if input_image_path is None:
        # Original behavior: Generate a blank image
        blank_image = Image.new("RGB", (500, 500), "white")
        input_image_path = "blank_image.png"
        blank_image.save(input_image_path)
    
    # Generate noise and save in the noisegenerated_image folder
    base_filename = os.path.splitext(os.path.basename(input_image_path))[0]
    noisy_image = os.path.join('noisegenerated_image', f'{base_filename}_noisy.png')
    ng5.add_noise(input_image_path, noisy_image)

    root = tk.Tk()
    app = DrawingApp(root, noisy_image)
    root.mainloop()

