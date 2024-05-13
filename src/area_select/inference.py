import numpy as np
import cv2
from src.utils.inference import calculate_average_rgb

def area_tempreture(roi_cropped,min_temp,max_temp):
    temperatures = []

    for row in roi_cropped:
        for pixel in row:
            tem= color_to_temperature(pixel,min_temp=min_temp,max_temp=max_temp)
            if tem is None:
                continue
            temperatures.append(tem)

    average_temperature = np.mean(temperatures)
    return average_temperature

def extract_polygon_roi(image, polygon_points):
    if len(polygon_points)<=2:
        raise ValueError("number of points should be more than 2")
    # Ensure points are in the correct shape (n, 1, 2) where n is the number of points
    contour = np.array(polygon_points, dtype=np.int32).reshape((-1, 1, 2))
    
    # Create a mask that is black
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    
    # Fill the polygon defined by the contour in the mask with white color
    cv2.fillPoly(mask, [contour], 255)
    
    # Apply the mask to the image using bitwise operation
    roi = cv2.bitwise_and(image, image, mask=mask)
    
    return roi

def get_temp_from_poly(image,polygon_points,min_temp,max_temp):
    return calculate_average_rgb(image,np.array(polygon_points, dtype=np.int32).reshape((-1, 1, 2)),[],min_temp,max_temp)[0]
    roi = extract_polygon_roi(image,polygon_points)
    return area_tempreture(roi,min_temp,max_temp)
    
