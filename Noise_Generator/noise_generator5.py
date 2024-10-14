from PIL import Image, ImageFilter, ImageDraw
import numpy as np
import random
#removed the import os module here cause i no longer need to change the directory. I have everything here.

#os.chdir("C:\\Users\\soumy\\OneDrive\\Desktop\\CSE543-IAS-Project-Team-12\\Noise_Generator")

def add_noise(image_path, output_path, noise_type="gaussian", mean=0, var=2000, blur_section=False, num_lines=7): 
    '''The third try for the noise_generator function. This time we needed to add random lines with blur and salt and pepper.
    The coordinates are random and so is the lines. their lengths but i have fixed the number of lines till 5. haven't tested it against
    A.I. right now.
    The function used to generate salt n pepper noise is the gaussian. probability density function.'''

    image = Image.open(image_path)
    image = np.array(image)
    
    if noise_type == "gaussian":
        row, col, ch = image.shape
        sigma = var**0.5
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        noisy_image = image + gauss
    # REMOVED SALT N PEPPER NOISE FROM THIS SECTION
    
    else:
        raise ValueError("noise type is not there.")
    
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8) 

    noisy_image_pil = Image.fromarray(noisy_image)
    
    # THIS IS THE NEW SECTION. I HAVE ADDED THIS AS THIS WILL DRAW RANDOM LINES.
    draw = ImageDraw.Draw(noisy_image_pil)
    width, height = noisy_image_pil.size
    for _ in range(num_lines):
        #FOR NOW THE START AND END POINTS FOR THE LINES ARE RANDOM.
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=(0,0,0), width=random.randint(1, 3))

    # NEW SECTION: ADDED CIRCLES AND TRIANGLES INSTEAD OF SALT N PEPPER NOISE
    for _ in range(5):  # Drawing 5 random circles
        radius = random.randint(10, 30)
        x, y = random.randint(0, width - radius), random.randint(0, height - radius)
        draw.ellipse((x, y, x + radius, y + radius), outline=(0, 0, 0), width=2)
    
    for _ in range(5):  # Draw 5 random triangles
        points = [(random.randint(0, width), random.randint(0, height)) for _ in range(3)]
        draw.polygon(points, outline=(0, 0, 0), width=2)
    
    # BLURRING THE WHOLE IMAGE INSTEAD OF JUST A SECTION
    if blur_section:
        noisy_image_pil = noisy_image_pil.filter(ImageFilter.BLUR)  # Applied blur to the entire image
    
    noisy_image_pil.save(output_path)
    
    print(f"Noise, random lines, circles, triangles, and blur applied. Saved to {output_path}")

#input_image = "user_drawn_pencil.png" 
#output_image = "noisy_pencil_experiment1.png"  
#add_noise(input_image, output_image, noise_type="gaussian", mean=0, var=2000, blur_section=True, num_lines=7)
#UNCOMMENT THE ABOVE LINES TO SEE THE THE BASIC FUNCTIONALITY