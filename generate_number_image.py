import numpy as np
import utility

from mnist_loader import get_mnist_dict, get_digits_from_dataset

def generate_number_image(number, merge_digits_function,
                          final_image_transformations=[],
                          digit_wise_transformations=[]):
    data, label_to_indices = get_mnist_dict()

    number = utility.convert_to_list(number)

    digit_images = get_digits_from_dataset(number, label_to_indices, data)

    for transformation in digit_wise_transformations:
        digit_images = transformation(digit_images)

    merged_digits_image = merge_digits_function(digit_images)

    for transformation in final_image_transformations:
        merged_digits_image = transformation(merged_digits_image)

    return merged_digits_image

def generate_numbers(batch_size, number_length):
    min_val, max_val = (10**(number_length - 1),
                        10**number_length - 1)

    numbers = np.random.random_integers(min_val, max_val, batch_size)
    return np.array([utility.convert_to_list(number) for number in numbers])

def generate_image_batch(batch_size, number_length,
                     merge_digits_function,
                     final_image_transformations=[],
                     digit_wise_transformations=[]):
    '''
    Generate batch_size random numbers images with number_length digits
    Returns a tuple of the images and the digits generated
    '''
    data, label_to_indices = get_mnist_dict()

    numbers = generate_numbers(batch_size, number_length)

    digit_images = np.array([get_digits_from_dataset(image, label_to_indices, data)
                             for image in numbers])

    for transformation in digit_wise_transformations:
        digit_images = np.array([transformation(single_number)
                                 for single_number in digit_images])

    # Cannot use np array here as the merged_image size is variable
    # Could rewrite a merge function that also does centering / reshaping
    merged_digits_images = [merge_digits_function(single_number)
                            for single_number in digit_images]

    # As of right now this only works if rescaling is the first transformation
    for transformation in final_image_transformations:
        merged_digits_images = np.array([transformation(single_image) for
                               single_image in merged_digits_images])


    return merged_digits_images, numbers
