import cv2
import numpy as np

def erase_line_segment(image_path, square_size=50):

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
    red_color = (0, 0, 255)  # BGR format
    border_thickness = 2
    cv2.rectangle(image_with_border, (x, y), (x + square_size, y + square_size), 
                 red_color, border_thickness)
    
    top_left = (x, y)
    bottom_right = (x + square_size, y + square_size)
    
    cv2.imwrite('challenge_created_no_border.png', image_no_border)
    cv2.imwrite('blocked_region.png', blocked_region)
    
    return image_with_border, image_no_border, blocked_region, (top_left[0], top_left[1], bottom_right[0], bottom_right[1])

'''image_path = "Untitled2.png"  # Your image path
modified_image_border, modified_image_no_border, blocked_region, corners = erase_line_segment(image_path)

print(f"Square corners coordinates:")
print(f"Top-left corner: ({corners[0]}, {corners[1]})")
print(f"Bottom-right corner: ({corners[2]}, {corners[3]})")

# Display the results (optional)
cv2.imshow('Modified Image without Border', modified_image_no_border)
cv2.imshow('Blocked Region', blocked_region)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
#NO NEED TO UNDOC THIS BECAUSE THIS IS WORKING FINE. WE ONLY NEED THE FUNCTION.

