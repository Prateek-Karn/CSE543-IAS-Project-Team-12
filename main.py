import sys
import os
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk, ImageEnhance
import numpy as np
import ndjson
import cv2
import noise_generator5 as ng5

# Converting of Ndjson to png file format
def process_ndjson(file_path, target_size=(1024, 1024), max_samples=40, sharpness_factor=2.0):
    with open(file_path, 'r') as f:
        data = ndjson.load(f)

    count = 0
    for record in data:
        if count >= max_samples:
            break
        # Extract the key ID and drawing data from the record, key ID used when saving the PNG.    
        key_id = record.get("key_id")
        drawing = record.get("drawing", [])

        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = float('-inf'), float('-inf')
        #Create the bounding box of the image drawing
        for stroke in drawing:
            if isinstance(stroke, list) and len(stroke) == 3:
                x_coords = stroke[0]
                y_coords = stroke[1]
                if x_coords:
                    min_x = min(min_x, min(x_coords))
                    max_x = max(max_x, max(x_coords))
                if y_coords:
                    min_y = min(min_y, min(y_coords))
                    max_y = max(max_y, max(y_coords))

        img_width = int(max_x - min_x + 10)
        img_height = int(max_y - min_y + 10)
        img = Image.new('L', (img_width, img_height), color=255) #create a white canvas
        draw = ImageDraw.Draw(img)
        #Draw the stroke on the image
        for stroke in drawing:
            if isinstance(stroke, list) and len(stroke) == 3:
                x_coords = stroke[0]
                y_coords = stroke[1]
                scaled_x = [(x - min_x) for x in x_coords]
                scaled_y = [(y - min_y) for y in y_coords]
                points = list(zip(scaled_x, scaled_y))
                if points:
                    draw.line(points, fill=0, width=2)

        img = img.resize(target_size, Image.LANCZOS)

        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(sharpness_factor)

        if np.array(img).sum() < (img_width * img_height * 255):
            img.save(f'ndjsontopng/reconstructed_image_{key_id}.png')
            count += 1

    print("Reconstructed images saved.")

ndjson_file_path = "full_raw_axe.ndjson"

# Creating Challenges for the image and storing the cropped part into a folder
def ensure_directories_exist():
    """Create the required directories if they don't exist."""
    directories = ['blockedregion_images', 'challenge_created']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

def erase_line_segment(image_path, square_size=50):
    ensure_directories_exist()

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not load image")
    
    original_image = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50,
                           minLineLength=30, maxLineGap=10)
    
    if lines is None:
        raise ValueError("No lines detected in the image")
    
    best_point = None
    max_line_strength = 0
    
    for line in lines:
        x1, y1, x2, y2 = line[0]
        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2
        
        if (mid_x < square_size or mid_x > image.shape[1] - square_size or 
            mid_y < square_size or mid_y > image.shape[0] - square_size):
            continue
        
        line_strength = np.sum(edges[mid_y-5:mid_y+5, mid_x-5:mid_x+5])
        
        if line_strength > max_line_strength:
            max_line_strength = line_strength
            best_point = (mid_x, mid_y)
    
    if best_point is None:
        raise ValueError("Could not find suitable line to erase")
    
    half_size = square_size // 2
    x = best_point[0] - half_size
    y = best_point[1] - half_size
    
    blocked_region = original_image[y:y+square_size, x:x+square_size].copy()
    
    image_no_border = image.copy()
    image_no_border[y:y+square_size, x:x+square_size] = [255, 255, 255]
    
    image_with_border = image_no_border.copy()
    red_color = (0, 0, 255)
    border_thickness = 2
    cv2.rectangle(image_with_border, (x, y), (x + square_size, y + square_size), 
                 red_color, border_thickness)
    
    top_left = (x, y)
    bottom_right = (x + square_size, y + square_size)
    
    base_filename = os.path.splitext(os.path.basename(image_path))[0]
    
    cv2.imwrite(os.path.join('challenge_created', f'{base_filename}_no_border.png'), image_no_border)
    cv2.imwrite(os.path.join('blockedregion_images', f'{base_filename}_blocked.png'), blocked_region)
    
    return image_with_border, image_no_border, blocked_region, (top_left[0], top_left[1], bottom_right[0], bottom_right[1])

# Adding Noise into the PNG image using Noise Generator
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

def add_noise_to_drawing(input_image_path="challenge_created/reconstructed_image_4883602938527744_no_border.png"):
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

# Using Similarity Score we determine the accuracy of the image drawn vs the actual image
def calculate_similarity(image_path1, image_path2):
    # Load the images and convert them to black and white (1-bit pixels)
    image1 = Image.open(image_path1).convert("1")
    image2 = Image.open(image_path2).convert("1")

    # Resize image1 to match the size of image2 if they differ
    image1 = image1.resize(image2.size)

    # Convert the images to numpy arrays for easier processing
    image1_np = np.array(image1)
    image2_np = np.array(image2)

    # Calculate total number of pixels and count matching pixels
    total_pixels = image1_np.size
    matching_pixels = np.sum(image1_np == image2_np)

    # Helper function to find paths of connected pixels in an image
    def find_paths(image_np):
        visited = np.zeros(image_np.shape, dtype=bool)  # Track visited pixels
        paths = []  # Store all discovered paths

        # Depth-first search function to explore connected pixels
        def dfs(x, y, path):
            stack = [(x, y)]
            while stack:
                cx, cy = stack.pop()
                if visited[cx, cy]:
                    continue
                visited[cx, cy] = True  # Mark current pixel as visited
                path.append((cx, cy))  # Add pixel to the current path

                # Check neighbors in four directions
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < image_np.shape[0] and 0 <= ny < image_np.shape[1]:
                        if image_np[nx, ny] == 1 and not visited[nx, ny]:
                            stack.append((nx, ny))

        # Iterate over each pixel in the image
        for i in range(image_np.shape[0]):
            for j in range(image_np.shape[1]):
                if image_np[i, j] == 1 and not visited[i, j]:
                    path = []  # Initialize a new path
                    dfs(i, j, path)  # Perform DFS to find connected pixels
                    paths.append(path)  # Add the path to the list

        return paths

    # Find connected paths in both images
    paths_image1 = find_paths(image1_np)
    paths_image2 = find_paths(image2_np)

    # Calculate the difference in the number of paths
    differing_paths = abs(len(paths_image1) - len(paths_image2))

    # Calculate path similarity score based on path count
    path_similarity_score = 1 - (
        differing_paths / max(len(paths_image1), len(paths_image2), 1)
    )

    # Convert pixel similarity score to a percentage
    pixel_similarity_percentage = (matching_pixels / total_pixels) * 100
    # Convert path similarity score to a percentage
    path_similarity_percentage = path_similarity_score * 100
    # Calculate overall similarity by averaging pixel and path similarity percentages
    overall_similarity_score = (pixel_similarity_percentage * 0.5) + (
        path_similarity_percentage * 0.5
    )

    # Return all calculated metrics
    return {
        "total_pixels": total_pixels,
        "matching_pixels": matching_pixels,
        "pixel_similarity_percentage": pixel_similarity_percentage,
        "path_similarity_percentage": path_similarity_percentage,
        "overall_similarity_score": overall_similarity_score,
    }

if __name__ == "__main__":
    process_ndjson(ndjson_file_path)
    
    image_path = "ndjsontopng/reconstructed_image_4883602938527744.png"
    modified_image_border, modified_image_no_border, blocked_region, corners = erase_line_segment(image_path)
    
    print(f"Square corners coordinates:")
    print(f"Top-left corner: ({corners[0]}, {corners[1]})")
    print(f"Bottom-right corner: ({corners[2]}, {corners[3]})")
    
    add_noise_to_drawing()
    
    result = calculate_similarity("blockedregion_images/reconstructed_image_4883602938527744_blocked.png", "plain_user_drawing.png")
    print(f"Total Pixels: {result['total_pixels']}")
    print(f"Matching Pixels: {result['matching_pixels']}")
    print(f"Pixel Similarity Percentage: {result['pixel_similarity_percentage']:.2f}%")
    print(f"Path Similarity Percentage: {result['path_similarity_percentage']:.2f}%")
    print(f"Overall Similarity Score: {result['overall_similarity_score']:.2f}%")