from termcolor import cprint
import sys
import numpy as np

import os
import matplotlib.pyplot as plt
import re

def convert_to_list(number):
    """ Convert input to a list of digits (works with int and string) """
    type_number = type(number)
    if type_number is np.ndarray:
        return number
    if type_number is list:
        return np.array(number)
    elif type_number is str:
        return [int(digit) for digit in number]
    elif type_number is int or type_number is np.int64:
        return [int(digit) for digit in str(number)]
    else:
        cprint("Type: {} unsupported for number, please use an integer, "
                "a string a list or a numpy.array".format(type_number), "red")
        sys.exit(1)

def mkdir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def save_to_dir(image, number, path="data/generated_numbers"):
    ''' Saves the image to path/[0-9]+_digits_numbers/actual_number_idx.png '''
    size = len(number)
    destination_dir = os.path.join(path, "{}_digits_numbers".format(size))
    mkdir(destination_dir)

    number = ''.join(str(digit) for digit in number)
    filename_pattern = re.compile(r"{}_(\d+).png".format(number))
    matches = [filename_pattern.match(f) for f in os.listdir(destination_dir)]
    matches = [int(match.group(1)) for match in matches if match is not None]

    matches.append(0)

    filename_id = max(matches) + 1

    plt.imsave("{}_{}.png".format(os.path.join(destination_dir, number),
                                  filename_id), image)
