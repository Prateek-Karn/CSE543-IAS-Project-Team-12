import sys
import os
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk,ImageEnhance
import numpy as np
import ndjson
import cv2
import noise_generator5 as ng5
from ndjsontopng import process_ndjson
from challenges import erase_line_segment
from trial import add_noise_to_drawing
from similarity_score import calculate_similarity

# # #Converting ndjson file into png file 
ndjson_file_path = "full_raw_axe.ndjson"

process_ndjson(ndjson_file_path)


# #Creating Challenges from the png images

image_path = "ndjsontopng/reconstructed_image_4520796586246144.png"  # Your image path
modified_image_border, modified_image_no_border, blocked_region, corners = erase_line_segment(image_path)

print(f"Square corners coordinates:")
print(f"Top-left corner: ({corners[0]}, {corners[1]})")
print(f"Bottom-right corner: ({corners[2]}, {corners[3]})")


#Adding Filter and Drawing the CAPTCHA

add_noise_to_drawing()


#Doing Similarity Check 

result = calculate_similarity("plain_user_drawing.png", "plain_user_drawing.png")
print(f"Total Pixels: {result['total_pixels']}")
print(f"Matching Pixels: {result['matching_pixels']}")
print(f"Pixel Similarity Percentage: {result['pixel_similarity_percentage']:.2f}%")
print(f"Path Similarity Percentage: {result['path_similarity_percentage']:.2f}%")
print(f"Overall Similarity Score: {result['overall_similarity_score']:.2f}%")

