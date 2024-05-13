import cv2
import numpy as np
from assets.color_pallet import iron_palette
# def calculate_average_rgb(image, outer_contour, child_contours):
#     """
#     Calculates the average RGB values between an outer contour and its child contours.
    
#     Parameters:
#     - image: Source image
#     - outer_contour: The outer contour (numpy array of points)
#     - child_contours: List of child contour arrays
    
#     Returns:
#     - average_rgb: The average RGB values as a tuple
#     """
#     # Create a mask the same size as the image, initialized to black
#     mask = np.zeros(image.shape[:2], dtype=np.uint8)
    
#     # Draw the outer contour in white on the mask
#     cv2.drawContours(mask, [outer_contour], -1, 255, -1)
    
#     # Subtract the child contours by drawing them in black
#     cv2.drawContours(mask, child_contours, -1, 0, -1)
    
#     # Apply the mask to the image
#     masked_image = cv2.bitwise_and(image, image, mask=mask)
    
#     # Calculate the average color of the masked area
#     where = np.where(mask == 255)
#     count = len(where[0])

#     if count > 0:  # Ensure there is at least some area to calculate
#         average_color = np.mean(masked_image[where], axis=0)
#         average_temperature = color_to_temperature(tuple(int(c) for c in average_color))  # Assuming BGR format
#     else:
#         average_temperature = 0  # Default to some neutral temperature if no area to calculate
    
#     return average_temperature, count


# def find_closest_outer_contour(contours, hierarchy, x, y):
#     min_dist = float('inf')
#     closest_contour_index = -1

#     for i, contour in enumerate(contours):
#         # Check if the contour is an outer contour (no parent)
        
#             dist = cv2.pointPolygonTest(contour, (x, y), True)
#             if dist > 0 and dist < min_dist:  # Point inside contour and closer than any previous
#                 min_dist = dist
#                 closest_contour_index = i
    
#     return closest_contour_index

# def find_closest_inner_contour(contours, hierarchy, parent_index):
#     """
#     Retrieve all direct child contours for a given parent contour index.
#     Args:
#     - contours: List of all contours found by cv2.findContours
#     - hierarchy: Hierarchy information returned by cv2.findContours
#     - parent_index: Index of the parent contour

#     Returns:
#     - List of child contours
#     """
#     children = []
#     if parent_index == -1 or hierarchy[0][parent_index][2] == -1:
#         return children  # No children

#     return [i for i,c in enumerate(hierarchy[0]) if c[3]==parent_index]
# def aggregate_rgb_values(image, contours, indices):
#     total_pixels = 0
#     sum_rgb = 0

#     for index in indices:
#         outer_contour = contours[index]
#         child_indices = find_closest_inner_contour(contours, hierarchy, index)
#         child_contours = [contours[i] for i in child_indices]
#         rgb, count = calculate_average_rgb(image.copy(), outer_contour, child_contours)
#         sum_rgb += (rgb) * count
#         total_pixels += count

#     if total_pixels > 0:
#         overall_average_rgb = (sum_rgb / total_pixels)
#         return overall_average_rgb
#     else:
#         return (0, 0, 0)

def mouse_callback(event, x, y, flags, param):
    global highlighted_image, contours,outer_hist
    if event == cv2.EVENT_LBUTTONDOWN:
 
        closest_outer=find_closest_outer_contour(contours,hierarchy,x,y)
        inners =find_closest_inner_contour(contours,hierarchy,closest_outer)

        if closest_outer in outer_hist:
            outer_hist.remove(closest_outer)
            cv2.drawContours(highlighted_image,[contours[i] for i in inners], -1, (0, 255, 0), 1) 
            cv2.drawContours(highlighted_image, [contours[closest_outer]], -1, (0, 255, 0), 1) 
            print("no average")
        else:
            outer_hist.add(closest_outer)
            cv2.drawContours(highlighted_image,[contours[i] for i in inners], -1, (255, 0, 0), 1) 
            cv2.drawContours(highlighted_image, [contours[closest_outer]], -1, (255, 0, 0), 1) 
        
        print(avg_rgb_text:=aggregate_rgb_values(image.copy(),contours,outer_hist),len(outer_hist))
        # cv2.putText(highlighted_image, str(avg_rgb_text), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


        cv2.imshow('Highlighted Image', highlighted_image)
        
def crop_and_save_contour(contour, index):
    # Create a mask for the contour
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, [contour], -1, (255), thickness=cv2.FILLED)
    
    # Create a bounding rectangle to crop the image and the mask
    x, y, w, h = cv2.boundingRect(contour)
    cropped_mask = mask[y:y+h, x:x+w]
    cropped_image = image[y:y+h, x:x+w]

    # Apply the mask to the cropped image
    cropped_image = cv2.bitwise_and(cropped_image, cropped_image, mask=cropped_mask)
    
    # Save the cropped image
    save_path = f'cropped_contour_{index}.png'
    cv2.imwrite(save_path, cropped_image)
    print(f"Cropped area saved as {save_path}")


# Function to find nearest color in palette and calculate temperature
# def color_distance(hex1, hex2):
#     # Simple RGB distance
#     rgb1 = [int(hex1[i:i+2], 16) for i in range(1, len(hex1), 2)]
#     rgb2 = [int(hex2[i:i+2], 16) for i in range(1, len(hex2), 2)]
#     return sum((c1 - c2) ** 2 for c1, c2 in zip(rgb1, rgb2)) ** 0.5
# def color_to_temperature(color):
#     # Convert color from BGR to hex
#     hex_color = '#{0:02x}{1:02x}{2:02x}'.format(color[2], color[1], color[0])

#     # Find the nearest color in the palette
#     closest_color = min(iron_palette, key=lambda x: color_distance(x, hex_color))
#     index = iron_palette.index(closest_color)

#     # Interpolate temperature
#     return min_temp + (max_temp - min_temp) * (index / len(iron_palette))

# def detect_edges(image):
#     image = cv2.imread(image_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     blurred = cv2.GaussianBlur(gray, (7, 7), 0)
#     # cv2.rectangle(blurred, (0, 0), (blurred.shape[1]-1, blurred.shape[0]-1), (255, 255, 255), 1)

#     edges = cv2.Canny(blurred, 55, 100)
#     kernel = np.ones((3, 3), np.uint8)
#     dilated_edges = cv2.dilate(edges, kernel, iterations=1)
#     return dilated_edges



if __name__=="__main__":
    min_temp = 22.1
    max_temp = 41.6
        
    outer_hist=set()
    # Load the image
    image_path = '/Users/Mahir/ChoY/thermo_note/assets/TTT2.jpeg'
    image = cv2.imread(image_path)
    dilated_edges = detect_edges(image)

    # # Create a mask and apply itz
    # mask = cv2.bitwise_not(dilated_edges)
    # image_without_cursor = cv2.bitwise_and(image, image, mask=mask)

    # Find and draw contours
    contours, hierarchy = cv2.findContours(dilated_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(hierarchy)


    highlighted_image = image.copy()

    cv2.drawContours(highlighted_image, contours, -1, (0, 255, 0), 1) 

    # Set up windows and callback functions
    cv2.namedWindow('Highlighted Image')
    cv2.setMouseCallback('Highlighted Image', mouse_callback)

    # Display images
    cv2.imshow('Original Image', image)
    cv2.imshow('Edges', dilated_edges)
    # cv2.imshow('Image without Cursor', image_without_cursor)
    cv2.imshow('Highlighted Image', highlighted_image)

    # Wait for a key press to save or close all windows
    while True:
        key = cv2.waitKey(0)
        if key == 13:  # Check if Enter key is pressed
            cv2.imwrite('highlighted_image.png', highlighted_image)  # Save the image
            print("Image saved as highlighted_image.png")
        elif key == 27:  # Check if ESC key is pressed
            break
    cv2.destroyAllWindows()



