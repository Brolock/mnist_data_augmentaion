import numpy as np

def center_to_shape(image, shape, background_color=0):

    center_image = np.full(shape, background_color)

    extra_rows = shape[0] - image.shape[0]
    extra_cols = shape[1] - image.shape[1]

    # if *_extra_space is negative, we need to crop the original image to fit
    rows_to_crop_start = abs(min(0, extra_rows // 2))
    rows_to_crop_end = abs(extra_rows) - rows_to_crop_start if rows_to_crop_start else 0
    rows_to_crop_end = image.shape[1] - rows_to_crop_end

    cols_to_crop_start = abs(min(0, extra_cols // 2))
    cols_to_crop_end = abs(extra_cols) - cols_to_crop_start if cols_to_crop_start else 0
    cols_to_crop_end = image.shape[1] - cols_to_crop_end

    # if *_extra_space is positive we need the indices where to insert
    rows_in_center_start = max(0, extra_rows // 2)
    rows_in_center_end = shape[0] - (extra_rows - rows_in_center_start)

    cols_in_center_start = max(0, extra_cols // 2)
    cols_in_center_end  = shape[1] - (extra_cols - cols_in_center_start)

    center_image[rows_in_center_start:rows_in_center_end,
            cols_in_center_start:cols_in_center_end] = (
                    image[rows_to_crop_start:rows_to_crop_end,
                          cols_to_crop_start:cols_to_crop_end]
                    )

    image = center_image
