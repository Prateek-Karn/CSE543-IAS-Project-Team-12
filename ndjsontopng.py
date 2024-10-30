import ndjson
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance

def process_ndjson(file_path, target_size=(512, 512), max_samples=1000, sharpness_factor=2.0):
    with open(file_path, 'r') as f:
        data = ndjson.load(f)

    count = 0
    for record in data:
        if count >= max_samples:
            break
            
        key_id = record.get("key_id")
        drawing = record.get("drawing", [])

        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = float('-inf'), float('-inf')

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
        img = Image.new('L', (img_width, img_height), color=255)
        draw = ImageDraw.Draw(img)

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
