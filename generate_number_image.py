#! /usr/bin/env python3

import numpy as np

import argparse
import utility

from mnist_loader import get_mnist_dict, get_digits_from_dataset

#Transformations HAVE to modify the given np.array(s) in place
def generate_number_image(number, merge_digits_function,
                          final_image_transformations=[],
                          digit_wise_transformations=[]):

    data, label_to_indices = get_mnist_dict()

    number = utility.convert_to_list(number)

    digit_images = get_digits_from_dataset(number, label_to_indices, data)

    for transformation in digit_wise_transformations:
        transformation(digit_images)

    merged_digits_image = merge_digits_function(digit_images)

    for transformation in final_image_transformations:
        transformation(merged_digits_image)

    import matplotlib.pyplot as plt
    plt.imshow(merged_digits_image, cmap="gray")
    plt.show()

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

    ## TODO extract that from here
    from digits_merge import horizontal_merge, optimal_horizontal_merge
    merge_digits_function = lambda image: optimal_horizontal_merge(image,
            int(args.min_max[0]), int(args.min_max[1]), background_color=0)

    from image_transformation import center_to_shape
    center_function = lambda image: center_to_shape(image,
            (28, int(args.image_width)), background_color=0)

    generate_number_image(args.number, merge_digits_function,
            final_image_transformations=[center_function])
