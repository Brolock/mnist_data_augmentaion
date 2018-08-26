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

