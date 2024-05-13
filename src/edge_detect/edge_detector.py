import cv2
import numpy as np

def detect_edges(image):
    # image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    # cv2.rectangle(blurred, (0, 0), (blurred.shape[1]-1, blurred.shape[0]-1), (255, 255, 255), 1)

    edges = cv2.Canny(blurred, 55, 100)
    kernel = np.ones((3, 3), np.uint8)
    dilated_edges = cv2.dilate(edges, kernel, iterations=1)
    return dilated_edges

