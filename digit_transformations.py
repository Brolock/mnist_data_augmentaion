import scipy.ndimage.interpolation as inter
import numpy as np

def rotate(images, angle, max_angle=None):
    ''' Forwards to scipy's rotation to every image in a list of images '''
    if not max_angle: max_angle = angle + 1
    return np.array([inter.rotate(image,
                                  angle=np.random.randint(angle, max_angle),
                                  reshape=False)
                                for image in images])
