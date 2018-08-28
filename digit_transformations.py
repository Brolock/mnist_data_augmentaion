import scipy.ndimage.interpolation as inter
import numpy as np

def rotate(images, angle, reshape):
    ''' Forwards to scipy's rotation to every image in a list of images '''
    return np.array([inter.rotate(image, angle=angle, reshape=reshape)
                    for image in images])
