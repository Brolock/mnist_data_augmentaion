import numpy as np
from collections import namedtuple

def first_row(digit_image, condition):
    ''' Returns the first row in a matrix that respects the condition fucntion'''
    for idx, column in enumerate(digit_image):
        if condition(column):
            return idx

BoundingBox = namedtuple('BoundingBox', ['left', 'right', 'top', 'bot'])

def get_bounding_boxes(digit_images, background_color):
    ''' Returns the indices position of the digits '''
    has_white = lambda column: np.any(column != background_color)
    for image in digit_images:
        left = first_row(image.T, has_white)
        # The last column containing atleast one white
        right = image.shape[1] - first_row(np.flip(image.T, axis=0), has_white)
        top = first_row(image, has_white)
        # The last row containing atleast one white
        bot = image.shape[0] - first_row(np.flip(image, axis=0), has_white)

        yield BoundingBox(left, right, top, bot)
