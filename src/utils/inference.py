import cv2
import numpy as np
from .color_to_thermo import color_to_temperature

def calculate_average_rgb(image, outer_contour, child_contours,min_temp,max_temp):

    # Create a mask the same size as the image, initialized to black
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    
    # Draw the outer contour in white on the mask
    cv2.drawContours(mask, [outer_contour], -1, 255, -1)
    
    # Subtract the child contours by drawing them in black
    cv2.drawContours(mask, child_contours, -1, 0, -1)
    
    # Apply the mask to the image
    masked_image = cv2.bitwise_and(image, image, mask=mask)
    
    # Calculate the average color of the masked area
    where = np.where(mask == 255)
    count = len(where[0])

    if count > 0:  # Ensure there is at least some area to calculate
        average_color = np.mean(masked_image[where], axis=0)
        average_color = tuple(int(c) for c in average_color)
        average_temperature = color_to_temperature(average_color,min_temp,max_temp)  # Assuming BGR format
    else:
        average_color=None
        average_temperature = 0  # Default to some neutral temperature if no area to calculate
    
    return average_temperature, count, average_color
