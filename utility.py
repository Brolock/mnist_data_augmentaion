from termcolor import cprint
import sys
import numpy as np

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
