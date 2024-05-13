import unittest
from src.edge_detect.contours_manipulator import find_closest_inner_contour
import numpy as np
class TestFindClosestInnerContour(unittest.TestCase):
    def setUp(self):
        # Sample hierarchy setup: [[next, previous, first_child, parent], ...]
        # Hierarchy with multiple children and nested children
        self.hierarchy = [
            [[1, -1, 2, -1],   # 0: parent of 2
             [4, 0, 3, -1],    # 1: parent of 3
             [-1, -1, -1, 0],  # 2: child of 0
             [-1, -1, -1, 1],  # 3: child of 1
             [-1, 1, -1, -1]]  # 4: no children
        ]
        self.hierarchy = np.array(self.hierarchy, dtype=int)

    def test_with_single_child(self):
        result = find_closest_inner_contour(self.hierarchy, 0)
        self.assertEqual(result, [2], "Should return the correct list of child contour indices.")

    def test_with_multiple_children(self):
        # Adjusting setup for multiple children to the same parent
        hierarchy = [
            [[1, -1, 2, -1],  # 0: parent of 2 and 4
             [-1, 0, 4, -1],  # 1: parent of none, child of none
             [-1, -1, -1, 0], # 2: child of 0
             [-1, -1, -1, -1],# 3: no children and no parent
             [-1, -1, -1, 0]] # 4: child of 0
        ]
        hierarchy = np.array(hierarchy, dtype=int)
        result = find_closest_inner_contour(hierarchy, 0)
        self.assertEqual(sorted(result), [2, 4], "Should return correct child indices.")

    def test_no_children(self):
        result = find_closest_inner_contour(self.hierarchy, 4)
        self.assertEqual(result, [], "Should return an empty list when there are no children.")

    def test_invalid_parent_index(self):
        result = find_closest_inner_contour(self.hierarchy, -1)
        self.assertEqual(result, [], "Should return an empty list when the parent index is invalid.")

    def test_non_existent_parent_index(self):
        with self.assertRaises(ValueError):

            result = find_closest_inner_contour(self.hierarchy, 10)


if __name__ == '__main__':
    unittest.main()
