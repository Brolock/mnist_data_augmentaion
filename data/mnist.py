import urllib.request
import gzip
import os.path
from termcolor import cprint

import struct
import numpy as np

MNIST_URL = "http://yann.lecun.com/exdb/mnist/"
TRAIN_IMAGES = "train-images-idx3-ubyte.gz"
TRAIN_LABELS = "train-labels-idx1-ubyte.gz"
TEST_IMAGES = "t10k-images-idx3-ubyte.gz"
TEST_LABELS = "t10k-labels-idx1-ubyte.gz"

CUR_DIR = os.path.dirname(os.path.realpath(__file__))

def download_mnist(destination_dir=CUR_DIR):
    ''' Downloads mnist training and testing files if not already present '''
    dataset_files = [TRAIN_IMAGES, TRAIN_LABELS, TEST_IMAGES, TEST_LABELS]
    for filename in dataset_files:
        dest_file = os.path.join(destination_dir, filename)
        if not os.path.isfile(dest_file):
            cprint("Downloading {}".format(filename), "yellow")

            dest_file = urllib.request.urlretrieve(os.path.join(MNIST_URL, filename),
                                                   dest_file)
            cprint("Successfully dowloaded {}".format(dest_file), "green")

def load_training(dir_path=CUR_DIR):
    ''' Returns a tuple of the image set and the labels for training '''
    download_mnist(dir_path)

    return load(os.path.join(dir_path, TRAIN_IMAGES),
                os.path.join(dir_path, TRAIN_LABELS))

def load_testing(dir_path=CUR_DIR):
    ''' Returns a tuple of the image set and the labels for testing '''
    download_mnist(dir_path)

    return load(os.path.join(dir_path, TEST_IMAGES),
                os.path.join(dir_path, TEST_LABELS))

from array import array
def load(path_images, path_labels):
    ''' Load and return mnist images and labels from the ubyte.gz files '''
    with gzip.open(path_labels, 'rb') as f:
        _, _= struct.unpack(">II", f.read(8))

        labels = array("B", f.read())

    with gzip.open(path_images, 'rb') as f:
        _, size, rows, cols = struct.unpack(">IIII", f.read(16))

        image_data = array("B", f.read())

    images = np.full((size, rows * cols), 0)
    for i in range(size):
        images[i][:] = image_data[i * rows * cols:(i + 1) * rows * cols]

    return images, labels
