#author:@Soham

import cv2
import numpy as np
import ndjson
import cv2
import noise_generator5 as ng5


def ensure_directories_exist():
    """Create the required directories if they don't exist."""
    directories = ['blockedregion_images', 'challenge_created']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

def erase_line_segment(image_path, square_size=6):  # Reduced square size
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not load image")
    

    # Print image shape to verify dimensions
    print(f"Image shape: {image.shape}")
    

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Reduce or remove blur for small images

    blurred = cv2.GaussianBlur(gray, (3, 3), 0)  # Reduced kernel size
    edges = cv2.Canny(blurred, 30, 100)  # Adjusted thresholds
    
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=10,  # Reduced threshold
                           minLineLength=5,  # Reduced minimum line length
                           maxLineGap=2)     # Reduced max gap
    if lines is None:
        raise ValueError("No lines detected in the image")
    

    best_point = None
    max_line_strength = 0
    
    for line in lines:
        x1, y1, x2, y2 = line[0]
        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2
        
        # Adjusted edge avoidance for smaller images
        if (mid_x < square_size or mid_x > image.shape[1] - square_size or 
            mid_y < square_size or mid_y > image.shape[0] - square_size):
            continue
        
        # Reduced window size for line strength calculation
        line_strength = np.sum(edges[mid_y-2:mid_y+2, mid_x-2:mid_x+2])
        
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
    
    red_color = (0, 0, 255)
    border_thickness = 1  # Reduced thickness for small images
    cv2.rectangle(image, (x, y), (x + square_size, y + square_size), 
                 red_color, border_thickness)
    
    top_left = (x, y)
    bottom_right = (x + square_size, y + square_size)
    
    cv2.imwrite('challenge_created.png', image)
    
    return image, (top_left[0], top_left[1], bottom_right[0], bottom_right[1])

image_path = "image_000272.png"
modified_image, corners = erase_line_segment(image_path)
print(f"Square corners coordinates:")
print(f"Top-left corner: ({corners[0]}, {corners[1]})")
print(f"Bottom-right corner: ({corners[2]}, {corners[3]})")



display_image = cv2.resize(modified_image, (280, 280), 
                            interpolation=cv2.INTER_NEAREST)
cv2.imshow('Modified Image', display_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
