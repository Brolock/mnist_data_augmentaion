#! /usr/bin/env python3

import unittest
import time

class TimedTest(unittest.TestCase):
    def setUp(self):
        self.start_time = time.time()

    def tearDown(self):
        t = time.time() - self.start_time
        print("{:0.2f}s  ".format(t), end='', flush=True)

import numpy as np
TEST_ARRAY = np.array([[0, 10, 160, 18, 0],
                       [0, 64, 20,  89, 2],
                       [6, 207, 1, 101, 9],
                       [3, 257, 0, 172, 4],
                       [0, 134, 55, 98, 0],
                       [0, 24, 183, 22, 0]])

from digit_transformations import rotate
from image_transformation import center_to_shape, grayscale_to_color
from digits_merge import horizontal_merge, optimal_horizontal_merge

class TestTransformations(TimedTest):
    def test_rotate_shape(self):
        # Test that rotate results in constant shape
        for [a, b, c, d] in np.random.randint(-180, 180, size=4000).reshape(1000, 4):
            self.assertEqual(rotate([TEST_ARRAY], min(a, b), max(a, b) + 1).shape,
                             rotate([TEST_ARRAY], min(c, d), max(c, d) + 1).shape)

    def test_rotate_values(self):
        # Test that rotation have expected results for both clockwise and anticlockwise
        rotated_30 = np.array([[[ 0,  0, 13,  0,  0],
                                [14, 65, 81, 39,  0],
                                [37, 99,  3,144,  4],
                                [ 6,238, 52,102, 52],
                                [ 0, 77,152,100, 29],
                                [ 0,  0, 17,  0,  0]]])
        np.testing.assert_array_equal(
                rotate([TEST_ARRAY], 30),
                rotated_30)

        rotated_minus_90 =  np.array([[[  0,  0,  0,  0,  0],
                                       [ 16,103,127, 69,  2],
                                       [112,119,143, 68, 71],
                                       [102, 74, 55, 38, 89],
                                       [ 10, 77, 77, 53, 13],
                                       [  0,  0,  0,  0,  0]]])
        np.testing.assert_array_equal(
                rotate([TEST_ARRAY], -90),
                rotated_minus_90)


    def test_center_to_shape(self):
        # Test padding
        shape1 = (10, 10)
        self.assertEqual(center_to_shape(TEST_ARRAY, shape1).shape, shape1)
        reshaped1 = np.array([[0, 0, 0, 0,   0,   0,   0, 0, 0, 0],
                              [0, 0, 0, 0,   0,   0,   0, 0, 0, 0],
                              [0, 0, 0, 0,  10, 160,  18, 0, 0, 0],
                              [0, 0, 0, 0,  64,  20,  89, 2, 0, 0],
                              [0, 0, 0, 6, 207,   1, 101, 9, 0, 0],
                              [0, 0, 0, 3, 257,   0, 172, 4, 0, 0],
                              [0, 0, 0, 0, 134,  55,  98, 0, 0, 0],
                              [0, 0, 0, 0,  24, 183,  22, 0, 0, 0],
                              [0, 0, 0, 0,   0,   0,   0, 0, 0, 0],
                              [0, 0, 0, 0,   0,   0,   0, 0, 0, 0]])
        np.testing.assert_array_equal(
                center_to_shape(TEST_ARRAY, shape1),
                reshaped1)

        # Test cropping
        shape2 = (3, 4)
        self.assertEqual(center_to_shape(TEST_ARRAY, shape2).shape, shape2)
        reshaped2 = np.array([[6, 207,  1, 101],
                              [3, 257,  0, 172],
                              [0, 134, 55,  98]])
        np.testing.assert_array_equal(
                center_to_shape(TEST_ARRAY, shape2),
                reshaped2)

    def test_grayscale_to_color(self):
        black_color = np.array([4, 22, 12])
        white_color = np.array([152, 23, 209])

        self.assertEqual(grayscale_to_color(
                            TEST_ARRAY, black_color, white_color).shape,
                            (TEST_ARRAY.shape[0], TEST_ARRAY.shape[1], 3))

        np.testing.assert_array_almost_equal(
                grayscale_to_color(np.array([[0, 0], [0, 0]]), black_color, white_color),
                np.array([[[4., 22., 12.], [4., 22., 12.]], [[4., 22., 12.], [4., 22., 12.]]]),
                decimal=0)

        np.testing.assert_array_almost_equal(
                grayscale_to_color(np.array([[255, 255], [255, 255]]), black_color, white_color),
                np.array([[[152., 23., 209.], [152., 23., 209.]], [[152., 23., 209.], [152., 23., 209.]]]),
                decimal=0)

        color = np.array([[[  4. ,  22. ,  12. ],
                           [  9.8,  22.0,  19.7],
                           [ 96.8,  22.6, 135.6],
                           [ 14.4,  22.0,  25.9],
                           [  4. ,  22. ,  12. ]],

                          [[  4. ,  22. ,  12. ],
                           [ 41.1,  22.2,  61.4],
                           [ 15.6,  22.0,  27.4],
                           [ 55.6,  22.3,  80.7],
                           [  5.1,  22.0,  13.5]],

                          [[7.482,  22.0,  16.6],
                           [124.1,  22.8, 171.9],
                           [  4.5,  22.0,  12.7],
                           [ 62.6,  22.3,  90.0],
                           [  9.2,  22.0,  18.9]],

                          [[5.741,  22.0,  14.3],
                           [153.1,  23.0, 210.5],
                           [  4. ,  22. ,  12. ],
                           [103.8,  22.6, 144.8],
                           [  6.3,  22.0,  15.0]],

                          [[ 4.  ,  22. ,  12. ],
                           [ 81.7,  22.5, 115.5],
                           [ 35.9,  22.2,  54.4],
                           [ 60.8,  22.3,  87.7],
                           [  4. ,  22. ,  12. ]],

                          [[ 4.  ,  22. ,  12. ],
                           [ 17.9,  22.0,  30.5],
                           [110.2,  22.7, 153.3],
                           [ 16.7,  22.0,  28.9],
                           [  4. ,  22. ,  12. ]]])
        np.testing.assert_array_almost_equal(
                grayscale_to_color(TEST_ARRAY, black_color, white_color),
                color,
                decimal=1)

    def test_horizontal_merge(self):
        multiple_test_array = np.array([TEST_ARRAY, TEST_ARRAY, TEST_ARRAY])
        # Test that both horizontal and optimal_horizontal have the same output
        for dist in np.random.randint(0, 100, size=1000):
            np.testing.assert_array_equal(
                    horizontal_merge(multiple_test_array, dist, dist),
                    optimal_horizontal_merge(multiple_test_array, dist, dist))

        # Test that the random padding added is correct
        number_images = multiple_test_array.shape[0]
        image_width = multiple_test_array.shape[2]
        for [a, b] in np.random.randint(0, 100, size=2000).reshape(1000, 2):
            low, high = min(a, b), max(a, b)
            result = optimal_horizontal_merge(multiple_test_array, low, high)
            self.assertTrue(
                    result.shape[1] <= number_images * image_width + (number_images - 1) * high)
            self.assertTrue(
                    result.shape[1] >= number_images * image_width + (number_images - 1) * low)

        # Check for equality
        merged_array = [[0,  10, 160,  18, 0, 0, 0, 0,  10, 160,  18, 0, 0, 0, 0,  10, 160,  18, 0],
                        [0,  64,  20,  89, 2, 0, 0, 0,  64,  20,  89, 2, 0, 0, 0,  64,  20,  89, 2],
                        [6, 207,   1, 101, 9, 0, 0, 6, 207,   1, 101, 9, 0, 0, 6, 207,   1, 101, 9],
                        [3, 257,   0, 172, 4, 0, 0, 3, 257,   0, 172, 4, 0, 0, 3, 257,   0, 172, 4],
                        [0, 134,  55,  98, 0, 0, 0, 0, 134,  55,  98, 0, 0, 0, 0, 134,  55,  98, 0],
                        [0,  24, 183,  22, 0, 0, 0, 0,  24, 183,  22, 0, 0, 0, 0,  24, 183,  22, 0]]
        np.testing.assert_array_equal(
                optimal_horizontal_merge(multiple_test_array, 2, 2),
                merged_array)

from single_image_generator import generate_numbers_sequence
from batch_image_generator import generate_batch_numbers

class TestGeneration(TimedTest):
    def test_generate_numbers_sequence(self):
        self.assertEqual(
                generate_numbers_sequence([1, 3, 3, 7], (3, 10), 140).shape,
                (28, 140))

    def test_generate_batch_numbers(self):
        images, numbers = generate_batch_numbers(7000, 10, (3, 10), 500, -30, 30)

        self.assertEqual(images.shape, (7000, 28, 500))
        self.assertEqual(len(numbers), 7000)

if __name__ == '__main__':
    suite_transfo = unittest.TestLoader().loadTestsFromTestCase(TestTransformations)
    unittest.TextTestRunner(verbosity=2).run(suite_transfo)

    suite_gen = unittest.TestLoader().loadTestsFromTestCase(TestGeneration)
    unittest.TextTestRunner(verbosity=2).run(suite_gen)
