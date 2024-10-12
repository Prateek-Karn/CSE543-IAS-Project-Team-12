from PIL import Image, ImageFilter
import numpy as np
import random
import os

os.chdir("C:\\Users\\soumy\\OneDrive\\Desktop\\Python")

def add_noise(image_path, output_path, noise_type="gaussian", mean=0, var=2000, blur_section=False):
    
    image = Image.open(image_path)
    image = np.array(image)
    
    if noise_type == "gaussian":
        #because we used probability density function
        row, col, ch = image.shape
        sigma = var**0.5
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        noisy_image = image + gauss
    elif noise_type == "salt_pepper":
        #salt n pepper noise
        row, col, ch = image.shape
        s_vs_p = 150 #make it really big for more dense noise
        amount = 50
        noisy_image = np.copy(image)
        
        # white noise
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
        noisy_image[coords[0], coords[1], :] = 255
        
        #black nosie
        num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
        noisy_image[coords[0], coords[1], :] = 0
    else:
        raise ValueError("noise type is not there.")
    
    #need this conversion because WHEN WE CREATE THE NOISE, THE VALUES GOES OUTSIDE THIS RANGE (0,255)
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
    
    #ADDED THIS NEW SECTION. GIVING BLUR A TRY.
    noisy_image_pil = Image.fromarray(noisy_image)
    
    if blur_section:
        #USING THE RANDOM LIBRARY TO GET THE RANDOM COORDINATES TO BLUR. (PARTICULARILY A SECTION)
        width, height = noisy_image_pil.size
        x1 = random.randint(0, width // 2)
        y1 = random.randint(0, height // 2)
        x2 = random.randint(x1 + width // 4, width)
        y2 = random.randint(y1 + height // 4, height)
        
        #Cropping the section, applying the blur and pasting it back to the coordinate.
        section = noisy_image_pil.crop((x1, y1, x2, y2))
        blurred_section = section.filter(ImageFilter.BLUR)
        noisy_image_pil.paste(blurred_section, (x1, y1, x2, y2))
    
    noisy_image_pil.save(output_path)
    
    print(f"Noise added and blurred section saved to {output_path}")


input_image = "input_image2.png" 
output_image = "airplane_noise_blur.png"
add_noise(input_image, output_image, noise_type="gaussian", mean=0, var=2000, blur_section=True)
