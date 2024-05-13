import unittest
import numpy as np
from src.edge_detect.contours_manipulator import find_closest_outer_contour

class TestFindClosestOuterContour(unittest.TestCase):
    def setUp(self):
        # Define some simple contours: rectangles or triangles for simplicity
        self.contours = [
            np.array([[0, 0], [0, 10], [10, 10], [10, 0]], dtype=np.int32).reshape(-1, 1, 2),  # Square contour
            np.array([[20, 20], [20, 40], [40, 40], [40, 20]], dtype=np.int32).reshape(-1, 1, 2),  # Another square
            np.array([[50, 50], [50, 70], [70, 60]], dtype=np.int32).reshape(-1, 1, 2)  # Triangle
        ]

    def test_find_contour_with_point_inside(self):
        # Test point inside the first contour
        result_index = find_closest_outer_contour(self.contours, 5, 5)
        self.assertEqual(result_index, 0, "Should return the index of the first contour")

    def test_find_contour_with_point_inside_second_contour(self):
        # Test point inside the second contour
        result_index = find_closest_outer_contour(self.contours, 30, 30)
        self.assertEqual(result_index, 1, "Should return the index of the second contour")

    def test_find_contour_with_point_outside_all_contours(self):
        # Test point outside all contours
        # print("ss")
        result_index = find_closest_outer_contour(self.contours, 100, 100)
        self.assertEqual(result_index, -1, "Should return -1 as no contour contains the point")

    def test_find_contour_with_point_on_the_edge(self):
        # Test point on the edge of a contour (should return the contour if strictly inside checking is not required)
        result_index = find_closest_outer_contour(self.contours, 0, 0)
        self.assertEqual(result_index, 0, "Should return the index of the first contour")

if __name__ == '__main__':
    unittest.main()
