#! /usr/bin/env python3

import argparse

from generate_number_image import generate_number_image
from digits_merge import optimal_horizontal_merge
from image_transformation import center_to_shape

import utility

def generate_numbers_sequence(digits, spacing_range, image_width):
    # Function used to merge digit images together
    merge_digits_function = lambda image: optimal_horizontal_merge(image,
            spacing_range[0], spacing_range[1], background_color=0)

    # Function used to center the image to the desired shape
    center_function = lambda image: center_to_shape(image,
            (28, image_width), background_color=0)

    image = generate_number_image(digits,
            merge_digits_function,
            final_image_transformations=[center_function],
            digit_wise_transformations=[])

    image = image / 255
    return image

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--number",
                        help="The number image to be generated")
    parser.add_argument("--min_max", nargs=2,
                        help="The minimum and maximum number of "
                             "pixels between two digits")
    parser.add_argument("--image_width",
                        help="The width of the resulting image in pixels")

    args = parser.parse_args()

    image = generate_numbers_sequence(args.number,
                              (int(args.min_max[0]), int(args.min_max[1])),
                              int(args.image_width))

    utility.save_to_dir(image, args.number)

    import matplotlib.pyplot as plt
    plt.imshow(image)
    plt.show()
