#! /usr/bin/env python3

import argparse

from generate_number_image import generate_number_image
from digits_merge import optimal_horizontal_merge
from image_transformation import center_to_shape


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

    # Function used to merge digit images together
    merge_digits_function = lambda image: optimal_horizontal_merge(image,
            int(args.min_max[0]), int(args.min_max[1]), background_color=0)

    # Function used to center the image to the desired shape
    center_function = lambda image: center_to_shape(image,
            (28, int(args.image_width)), background_color=0)

    from digit_transformations import rotate
    rotato = lambda images: rotate(images, angle=90, reshape=True)

    from image_transformation import grayscale_to_color
    import numpy as np
    violet = np.array([72, 61, 139])
    coral = np.array([255, 127, 80])
    to_color = lambda image: grayscale_to_color(image, violet, coral)

    image = generate_number_image(args.number,
            merge_digits_function,
            final_image_transformations=[center_function, to_color],
            digit_wise_transformations=[rotato])

    image = image / 255
    import matplotlib.pyplot as plt
    plt.imshow(image)
    plt.show()
