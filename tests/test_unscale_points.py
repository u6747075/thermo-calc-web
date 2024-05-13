import unittest
from src.utils.unscale_points import unscale_points  # Ensure to import the function correctly from its module
import logging

# Disable logging while testing
logging.disable(logging.CRITICAL)

class TestUnscalePoints(unittest.TestCase):
    def test_basic_unscale(self):
        # Test a basic unscale scenario
        point = (300, 150)
        width = 200
        original_dimension = (400, 300)
        height_ratio = 1.5
        expected_output = (600, 150)
        result = unscale_points(point, width, original_dimension, height_ratio)
        self.assertEqual(result, expected_output)

    def test_zero_width(self):
        # Test the behavior with zero width
        point = (300, 150)
        width = 0
        original_dimension = (400, 300)
        height_ratio = 1.5
        with self.assertRaises(ValueError):
            unscale_points(point, width, original_dimension, height_ratio)

    def test_negative_dimensions(self):
        # Test negative dimensions to see if the function handles it
        point = (300, 150)
        width = -200
        original_dimension = (400, -300)
        height_ratio = 1.5
        with self.assertRaises(ValueError):

            result = unscale_points(point, width, original_dimension, height_ratio)


    def test_height_ratio_zero(self):
        # Test zero height ratio
        point = (300, 150)
        width = 200
        original_dimension = (400, 300)
        height_ratio = 0

        with self.assertRaises(ValueError):

            result = unscale_points(point, width, original_dimension, height_ratio)


    def test_identity_scale(self):
        # Test with scaling factor of 1 (i.e., no scaling)
        point = (400, 300)
        width = 400
        original_dimension = (400, 300)
        height_ratio = 300/400
        expected_output = (400, 300)
        
        result = unscale_points(point, width, original_dimension, height_ratio)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()
