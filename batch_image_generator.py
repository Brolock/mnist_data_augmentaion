#! /usr/bin/env python3

import argparse

from generate_number_image import generate_image_batch

from digits_merge import optimal_horizontal_merge
from image_transformation import center_to_shape
from digit_transformations import rotate

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch_size",
                        help="number of images to be generated")
    parser.add_argument("--min_max", nargs=2, default=(5, 5),
                        help="The minimum and maximum number of "
                             "pixels between two digits, default (5, 5)")
    parser.add_argument("--image_width",
                        help="The width of the resulting image in pixels")

    args = parser.parse_args()
    # Function used to merge digit images together
    min_dist, max_dist = (2, 10)
    merge_digits_function = lambda image: optimal_horizontal_merge(image,
            min_dist, max_dist, background_color=0)

    # Function used to center the image to the desired shape
    image_width = 150
    center_function = lambda image: center_to_shape(image,
            (28, image_width), background_color=0)

    angle = -30
    rotato = lambda images: rotate(images, angle=angle, reshape=True)

    images = generate_image_batch(10, number_length=5,
            merge_digits_function=merge_digits_function,
            final_image_transformations=[center_function],
            digit_wise_transformations=[rotato])

    import matplotlib.pyplot as plt
    for image in images:
        plt.imshow(image, cmap="gray")
        plt.show()
