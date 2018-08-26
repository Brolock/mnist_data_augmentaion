from mnist import MNIST
import numpy as np

#TODO Make my own Mnist loader
def load_mnist(path_to_mnist):
    ''' Load training and testing sets, merge them and return the tuple (data, labels)'''
    mnist_loader = MNIST(path_to_mnist, return_type='numpy')
    data_train, labels_train = mnist_loader.load_training()
    data_test, labels_test = mnist_loader.load_testing()

    data_full = np.concatenate((data_train, data_test))
    labels_full = np.concatenate((labels_train, labels_test))

    return (data_full, labels_full)

def get_digits_from_dataset(digits, label_to_indices, mnist_data):
    ''' Randomly pick digits from image set and reshape image to 28x28 '''
    digit_indices = np.array([np.random.choice(label_to_indices[digit])
                        for digit in digits])
    return np.array(mnist_data[digit_indices].reshape(len(digit_indices), 28, 28))

def get_mnist_dict():
    ''' Returns mnist images and a dict containing the indices of each digit '''
    data, labels = load_mnist("python-mnist/data")

    label_to_indices = [[] for x in range(10)]
    for idx, label in enumerate(labels):
        label_to_indices[label].append(idx)
    # Convert python list[list] to np.array[np.array]
    return data, np.array([np.array(l) for l in label_to_indices])
