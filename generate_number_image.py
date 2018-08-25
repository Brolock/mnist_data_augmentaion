#! /usr/bin/env python3

import numpy as np

import argparse
import utility

from mnist import MNIST
from collections import namedtuple

#TODO Make my own Mnist loader
def load_mnist(path_to_mnist):
    ''' Load training and testing sets, merge them and return the tuple (data, labels)'''
    mnist_loader = MNIST(path_to_mnist, return_type='numpy')
    data_train, labels_train = mnist_loader.load_training()
    data_test, labels_test = mnist_loader.load_testing()

    data_full = np.append(data_train, data_test, axis=0)
    labels_full = np.append(labels_train, labels_test, axis=0)

    return (data_full, labels_full)

BoundingBox = namedtuple('BoundingBox', ['left', 'right', 'top', 'bot'])

#TODO URGENT: rewrite with a function :first_row(matrix, func)
#such that I can write left = first_row(image.T, lambda:...)
def get_bounding_box(digit_images, background_color):
    bounding_boxes = []
    for image in digit_images:
        left, right, top, bot = (None, None, None, None)
        for idx, column in enumerate(image.T):
            print(column)
            if np.any(column != background_color) and not left:
                left = idx
            if left and np.all(column == background_color) and not right:
                right = idx - 1
        for idx, row in enumerate(image):
            if np.any(row != background_color)and not top:
                top = idx
            if top and np.all(row == background_color) and not bot:
                bot = idx - 1

        bounding_boxes.append(BoundingBox(left, right, top, bot))

    return bounding_boxes


#TODO integrate background_color better
def generate_number_image(number, min_max, image_width, background_color=0):
    data, labels = load_mnist("python-mnist/data")

    label_to_indices = [[] for x in range(10)]
    for idx, label in enumerate(labels):
        label_to_indices[label].append(idx)
    # Convert python list[list] to np.array[np.array]
    label_to_indices = np.array([np.array(l) for l in label_to_indices])

    number = utility.convert_to_list(number)

    digit_indices = np.array([np.random.choice(label_to_indices[digit]) for digit in number])
    digit_images = np.array(data[digit_indices].reshape(len(digit_indices), 28, 28))

    import matplotlib.pyplot as plt
    for image in digit_images:
        plt.imshow(image, cmap="gray")
        plt.show()

    digit_bounding_boxes = get_bounding_box(digit_images, background_color)

    print([elem for elem in digit_bounding_boxes])

    min_dist, max_dist = min_max
    #TODO Should max_dist be included?
    digit_distances = np.random.randint(min_dist, max_dist + 1, len(number) - 1)


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

    generate_number_image(args.number,
                          tuple(map(int, args.min_max)),
                          int(args.image_width))
