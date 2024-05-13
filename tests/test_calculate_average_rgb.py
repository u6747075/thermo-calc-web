import unittest
import numpy as np
import cv2
from src.edge_detect.contours_manipulator import calculate_average_rgb

def color_to_temperature(color, min_temp, max_temp):
    # Mock function to convert color to temperature
    return (color[0] + color[1] + color[2]) % (max_temp - min_temp) + min_temp

class TestCalculateAverageRgb(unittest.TestCase):
    def setUp(self):
        # Create a mock image (100x100 pixels, 3 channels for RGB)
        self.image = np.full((100, 100, 3), 255, np.uint8)  # White image

        # Define a simple square outer contour
        self.outer_contour = np.array([[[10, 10]], [[10, 30]], [[30, 30]], [[30, 10]]], dtype=np.int32)

        # Define a smaller inner contour
        self.child_contours = [np.array([[[15, 15]], [[15, 25]], [[25, 25]], [[25, 15]]], dtype=np.int32)]

    def test_calculate_average_rgb_with_valid_input(self):
        average_temperature, count, average_color = calculate_average_rgb(
            self.image, self.outer_contour, self.child_contours, 0, 100)
        
        # Check the count of pixels within the outer contour minus child contours
        expected_count = (21 * 21) - (11 * 11)  # area of the outer contour minus area of the child contour
        self.assertEqual(count, expected_count)

        # Since the image is white and the mask will exclude the child contour,
        # the average color should still be white (255, 255, 255)
        self.assertEqual(average_color, (255, 255, 255))

    def test_calculate_average_rgb_with_no_inner_contour(self):
        average_temperature, count, average_color = calculate_average_rgb(
            self.image, self.outer_contour, [], 0, 100)
        
        # Check the count of pixels, which should be the area of the outer contour
        expected_count = 21 * 21  # area of the outer contour
        self.assertEqual(count, expected_count)

        # Average color should be white because the image is fully white
        self.assertEqual(average_color, (255, 255, 255))

if __name__ == '__main__':
    unittest.main()
