from PIL import Image
import numpy as np
import random
import os

os.chdir("C:\\Users\\soumy\\OneDrive\\Desktop\\Python")

def add_noise(image_path, output_path, noise_type="gaussian", mean=0, var=100):
    image = Image.open(image_path)
    image = np.array(image)
    
    if noise_type == "gaussian": #because we used probability density function
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
        
        #white noise
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
        noisy_image[coords[0], coords[1], :] = 255
        
        #bloack noise
        num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
        noisy_image[coords[0], coords[1], :] = 0
    else:
        raise ValueError("noise type is not there.")
    
    #need this conversion because WHEN WE CREATE THE NOISE, THE VALUES GOES OUTSIDE THIS RANGE (0,255)
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
    
    noisy_image_pil = Image.fromarray(noisy_image)
    noisy_image_pil.save(output_path)
    
    print(f"Noise added and saved to {output_path}")

input_image = "input_image2.png"  #image path
output_image = "airplane_noise2.png" #path where noisy image gonna save and the name of the file.
add_noise(input_image, output_image, noise_type="gaussian", mean=0, var=2000)
