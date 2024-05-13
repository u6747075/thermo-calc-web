import cv2 
from src.utils.inference import calculate_average_rgb
def find_closest_outer_contour(contours, x, y):
    min_dist = float('inf')
    closest_contour_index = -1

    for i, contour in enumerate(contours):
        # Check if the contour is an outer contour (no parent)
        
            dist = cv2.pointPolygonTest(contour, (x, y), True)
            if dist > 0 and dist < min_dist:  # Point inside contour and closer than any previous
                min_dist = dist
                closest_contour_index = i
    
    return closest_contour_index

def find_closest_inner_contour( hierarchy, parent_index):
    """
    Retrieve all direct child contours for a given parent contour index.
    Args:

    - hierarchy: Hierarchy information returned by cv2.findContours
    - parent_index: Index of the parent contour

    Returns:
    - List of child contours
    """
    if parent_index>=len(hierarchy[0]):
        raise ValueError("parent_index should exist")
    children = []
    if parent_index == -1 or hierarchy[0][parent_index][2] == -1:
        return children  # No children

    return [i for i,c in enumerate(hierarchy[0]) if c[3]==parent_index]

def aggregate_rgb_values(image, contours, hierarchy, indices,min_temp,max_temp):
    total_pixels = 0
    sum_rgb = 0

    for index in indices:
        outer_contour = contours[index]
        child_indices = find_closest_inner_contour( hierarchy, index)
        child_contours = [contours[i] for i in child_indices]
        rgb, count,_ = calculate_average_rgb(image.copy(), outer_contour, child_contours,min_temp,max_temp)
        sum_rgb += (rgb) * count
        total_pixels += count

    if total_pixels > 0:
        overall_average_rgb = (sum_rgb / total_pixels)
        return overall_average_rgb
    else:
        return 0