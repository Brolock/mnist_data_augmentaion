import numpy as np

def center_to_shape(image, shape, background_color=0):
    ''' Center the image inside of an image of shape shape, crops if necessary '''
    min_row = min(image.shape[0], shape[0]) // 2
    min_cols = min(image.shape[1], shape[1]) // 2

    # Get center of both original image and desired shape and get the indices
    # to draw to and from by taking the minimum dimension of the two
    center_result = (shape[0] // 2, shape[1] // 2)
    res_box = (center_result[0] - min_row, center_result[0] + min_row,
               center_result[1] - min_cols, center_result[1] + min_cols)

    center_image = (image.shape[0] // 2, image.shape[1] // 2)
    img_box = (center_image[0] - min_row, center_image[0] + min_row,
               center_image[1] - min_cols, center_image[1] + min_cols)

    res = np.full(shape, background_color)
    res[res_box[0]:res_box[1], res_box[2]:res_box[3]] = (
            image[img_box[0]: img_box[1], img_box[2]: img_box[3]])

    return res

def grayscale_to_color(image, black_color, white_color):
    ''' Linearly interpolate from grayscale to black_color and white_color '''
    slope = (white_color - black_color) / 255
    colored_image = np.full((image.shape[0], image.shape[1], 3), slope)

    return colored_image * image[:, :, None] + black_color

def random_noise(image, min_color=[0, 0, 0], max_color=[255, 255, 255],
                 amount=0.01):
    ''' Add random colored pixels to the image, color picked between min_color and max_color '''
    row, col = image.shape[:2]
    num_pixels = int(np.ceil(amount * row * col))
    coords = [np.random.randint(0, i, num_pixels)
              for i in image.shape[:2]]

    colors = np.array([[np.random.randint(lo, hi)
                        for (lo, hi) in zip(min_color, max_color)]
                        for _ in range(num_pixels)])

    image[tuple(coords)] = colors.reshape(image[tuple(coords)].shape)
    return image

# Could make a better version for colored image so the noise isnt pure green red and blue
def salt_and_pepper(image, min_color=0, max_color=255,
                    amount=0.01, salt_percent=0.5):
    ''' Applies Salt and pepper noise to the image '''
    # Salt
    num_salt = int(np.ceil(amount * image.size * salt_percent))
    coords = [np.random.randint(0, i, num_salt)
              for i in image.shape]
    image[tuple(coords)] = max_color

    # Pepper
    num_pepper = int(np.ceil(amount* image.size * (1. - salt_percent)))
    coords = [np.random.randint(0, i, num_pepper)
              for i in image.shape]
    image[tuple(coords)] = min_color
    return image
