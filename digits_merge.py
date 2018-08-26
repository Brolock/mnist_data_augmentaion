from bounding_box import get_bounding_boxes
from itertools import zip_longest
import numpy as np

def horizontal_merge(digit_images, min_dist, max_dist, background_color=0):
    '''
    Merges list of digit images horizontally, each digit is separated by
    a distance picked randomly between min_dist and max_dist
    background_color indicates the color of every pixel not being part of digit
    '''
    bounding_boxes = get_bounding_boxes(digit_images, background_color)
    digit_distances = np.random.randint(min_dist, max_dist + 1,
                                        digit_images.shape[0] - 1)

    height = digit_images.shape[1]
    output = np.empty((28, 0))

    for digit, bb, space in zip_longest(digit_images, bounding_boxes,
                                        digit_distances, fillvalue=0):
        digit_only= digit[:, bb.left:bb.right]
        output = np.hstack((output, digit_only))

        blank_space = np.full((height, space), background_color)
        output = np.hstack((output, blank_space))

    return output


# Is faster than the other implementation as it doesnt concatenate
# (reallocate memory) for every digit and space
# Looks messier and would be harder to modify though
def optimal_horizontal_merge(digit_images, min_dist, max_dist, background_color=0):
    '''
    Merges list of digit images horizontally, each digit is separated by
    a distance picked randomly between min_dist and max_dist
    background_color indicates the color of every pixel not being part of digit
    '''
    bounding_boxes = get_bounding_boxes(digit_images, background_color)
    digit_distances = np.random.randint(min_dist, max_dist + 1,
                                        digit_images.shape[0] - 1)

    height = digit_images.shape[1]
    digits_only = [digit[:, bb.left:bb.right] for
                    digit, bb in zip(digit_images, bounding_boxes)]

    # Compute the final shape of the image
    digits_total_width = sum(img.shape[1] for img in digits_only)
    result_shape = (height, digits_total_width + sum(digit_distances))

    output = np.full(result_shape, background_color)
    # Fill output with the digits extracted out of their bounding boxes
    write_idx = 0
    for digit, blank_space in zip_longest(digits_only, digit_distances,
                                          fillvalue=0):
        digit_width = digit.shape[1]
        output[:, write_idx:write_idx + digit_width] = digit
        write_idx += digit_width + blank_space

    return output
