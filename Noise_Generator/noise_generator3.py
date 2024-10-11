from PIL import Image, ImageFilter, ImageDraw
import numpy as np
import random
import os

os.chdir("C:\\Users\\soumy\\OneDrive\\Desktop\\Python")

def add_noise(image_path, output_path, noise_type="gaussian", mean=0, var=2000, blur_section=False, num_lines=5): #ADDED THIS NUMBER OF LINES BECUASE WE NEEDED A NEW TYPE OF NOSIE. WHICH WE CHOSE AS LINES.
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
    elif noise_type == "salt_pepper":
       
        row, col, ch = image.shape
        s_vs_p = 150
        amount = 50
        noisy_image = np.copy(image)
        
       #white noise
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
        noisy_image[coords[0], coords[1], :] = 255
        
        #black noise
        num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
        noisy_image[coords[0], coords[1], :] = 0
    else:
        raise ValueError("noise type is not there.")
    
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8) #to understand this read the previous function. I am reducing the comments from this

    noisy_image_pil = Image.fromarray(noisy_image)
    
    # THIS IS THE NEW SECTION. I HAVE ADDED THIS AS THIS WILL DRAW RANDOM LINES.
    draw = ImageDraw.Draw(noisy_image_pil)
    width, height = noisy_image_pil.size
    for _ in range(num_lines):
        # FOR NOW THE START AND END POINTS FOR THE LINES ARE RANDOM.
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        #line_color = tuple(np.random.randint(0, 256, size=3))  # UNCOMMENT THIS TO GET COLOR LINES
        draw.line((x1, y1, x2, y2), fill=(0,0,0), width=random.randint(1, 3))
                                    #this is where the line_color will come. in fill
    if blur_section:

        x1 = random.randint(0, width // 2)
        y1 = random.randint(0, height // 2)
        x2 = random.randint(x1 + width // 4, width)
        y2 = random.randint(y1 + height // 4, height)
        

        section = noisy_image_pil.crop((x1, y1, x2, y2))
        blurred_section = section.filter(ImageFilter.BLUR)
        noisy_image_pil.paste(blurred_section, (x1, y1, x2, y2))
    
    noisy_image_pil.save(output_path)
    
    print(f"Noise, random lines, and blurred section saved to {output_path}")

input_image = "input_image3.png" 
output_image = "airplane_noise_blur_lines2.png"  
add_noise(input_image, output_image, noise_type="gaussian", mean=0, var=2000, blur_section=True, num_lines=7)
