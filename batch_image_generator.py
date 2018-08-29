#! /usr/bin/env python3

import argparse
import utility

from generate_number_image import generate_image_batch

from digits_merge import optimal_horizontal_merge
from image_transformation import center_to_shape
from digit_transformations import rotate

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch_size",
                        help="number of images to be generated")
    parser.add_argument("--number_of_digits",
                        help="The number of digits in the generated number")
    parser.add_argument("--min_max", nargs=2, default=(5, 5),
                        help="The minimum and maximum number of "
                             "pixels between two digits, default (5, 5)")
    parser.add_argument("--image_width",
                        help="The width of the resulting image in pixels")

    parser.add_argument("--rotation_angle", default=0,
                        help="Digit wise rotation angle (in degrees)")

    args = parser.parse_args()
    # Function used to merge digit images together
    min_dist, max_dist = (int(args.min_max[0]), int(args.min_max[1]))
    merge_digits_function = lambda image: optimal_horizontal_merge(image,
            min_dist, max_dist, background_color=0)

    # Function used to center the image to the desired shape
    image_width = int(args.image_width)
    center_function = lambda image: center_to_shape(image,
            (28, image_width), background_color=0)

    angle = int(args.rotation_angle)
    rotato = lambda images: rotate(images, angle=angle, reshape=True)

    batch_size = int(args.batch_size)
    nb_digits = int(args.number_of_digits)
    images, numbers = generate_image_batch(batch_size, nb_digits,
            merge_digits_function,
            final_image_transformations=[center_function],
            digit_wise_transformations=[rotato])

    images = images / 255
    for image, number in zip(images, numbers):
        utility.save_to_dir(image, number)
