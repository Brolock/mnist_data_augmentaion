import numpy as np

import sys
sys.path.insert(0, '/home/brolock/Work/mnist_augmentation/data')
import mnist

def load_mnist(path_to_mnist):
    ''' Load training and testing sets, merge them and return the tuple (data, labels)'''
    data_train, labels_train = mnist.load_training()
    data_test, labels_test = mnist.load_testing()

    data_full = np.concatenate((data_train, data_test))
    labels_full = np.concatenate((labels_train, labels_test))

    return (data_full, labels_full)

def get_digits_from_dataset(digits, label_to_indices, mnist_data):
    ''' Randomly pick digits from image set '''
    digit_indices = np.array([np.random.choice(label_to_indices[digit])
                        for digit in digits])
    return np.array(mnist_data[digit_indices])

def get_mnist_dict():
    ''' Returns mnist images and a dict containing the indices of each digit '''
    data, labels = load_mnist("python-mnist/data")

    label_to_indices = [[] for x in range(10)]
    for idx, label in enumerate(labels):
        label_to_indices[label].append(idx)
    # Convert python list[list] to np.array[np.array]
    return data, np.array([np.array(l) for l in label_to_indices])
