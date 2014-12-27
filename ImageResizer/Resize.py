# coding=utf8

from PIL import Image

IMAGE_RESIZE_RULE_FIT = "fit"
IMAGE_RESIZE_RULE_FILL = "fill"
IMAGE_RESIZE_RULE_CROP_TOP = "top"
IMAGE_RESIZE_RULE_CROP_BOTTOM = "bottom"
IMAGE_RESIZE_RULE_CROP_MIDDLE = "middle"


# source https://gist.github.com/sigilioso/2957026#comment-1241684
def resize_and_crop(img, size, crop_type):
    """
    Resize and crop an image to fit the specified size.

    :rtype : Image
    :argument img: image to resize.
    :argument @size `(width, height)` tuple.
    :argument crop_type: can be 'top', 'middle' or 'bottom', depending on this value, the image will be cropped getting the 'top/left', 'middle' or 'bottom/right' of the image to fit the size.
    :raises ValueError: if an invalid `crop_type` is provided.
    """
    # If height is higher we resize vertically, if not we resize horizontally

    # Get current and desired ratio for the images
    img_ratio = img.size[0] / float(img.size[1])
    ratio = size[0] / float(size[1])
    # The image is scaled/cropped vertically or horizontally depending on the ratio
    if ratio > img_ratio:
        img = img.resize((size[0], int(round(size[0] * img.size[1] / img.size[0]))), Image.ANTIALIAS)
        # Crop in the top, middle or bottom
        if crop_type == IMAGE_RESIZE_RULE_CROP_TOP:
            box = (0, 0, img.size[0], size[1])
        elif crop_type == IMAGE_RESIZE_RULE_CROP_MIDDLE:
            box = (0, int(round((img.size[1] - size[1]) / 2)), img.size[0], int(round((img.size[1] + size[1]) / 2)))
        elif crop_type == IMAGE_RESIZE_RULE_CROP_BOTTOM:
            box = (0, img.size[1] - size[1], img.size[0], img.size[1])
        else:
            raise ValueError('ERROR: invalid value for crop_type')
        img = img.crop(box)
    elif ratio < img_ratio:
        img = img.resize((int(round(size[1] * img.size[0] / img.size[1])), size[1]), Image.ANTIALIAS)
        # Crop in the top, middle or bottom
        if crop_type == IMAGE_RESIZE_RULE_CROP_TOP:
            box = (0, 0, size[0], img.size[1])
        elif crop_type == IMAGE_RESIZE_RULE_CROP_MIDDLE:
            box = (int(round((img.size[0] - size[0]) / 2)), 0, int(round((img.size[0] + size[0]) / 2)), img.size[1])
        elif crop_type == IMAGE_RESIZE_RULE_CROP_BOTTOM:
            box = (img.size[0] - size[0], 0, img.size[0], img.size[1])
        else:
            raise ValueError('ERROR: invalid value for crop_type')
        img = img.crop(box)
    else:
        img = img.resize((size[0], size[1]), Image.ANTIALIAS)

    return img
