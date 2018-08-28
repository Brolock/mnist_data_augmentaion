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

    import matplotlib.pyplot as plt
    plt.imshow(merged_digits_image, cmap="gray")
    plt.show()

    return merged_digits_image
