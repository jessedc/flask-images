# coding=utf8

from PIL import Image

IMAGE_RESIZE_RULE_CROP_NONE = "resize"
IMAGE_RESIZE_RULE_CROP_MIDDLE = "resize-crop"


def best_image_size(in_size, out_size):
    in_ratio = in_size[0] / float(in_size[1])
    out_ratio = out_size[0] / float(out_size[1])

    if out_ratio > in_ratio:
        return out_size[0], int(round(out_size[0] * in_size[1] / in_size[0]))
    elif out_ratio < in_ratio:
        return int(round(out_size[1] * in_size[0] / in_size[1])), out_size[1]
    else:
        return out_size


def best_image_crop(in_size, crop_size):

    if crop_size[0] >= in_size[0] and crop_size[1] >= in_size[1]:
        return None

    in_ratio = in_size[0] / float(in_size[1])
    crop_ratio = crop_size[0] / float(crop_size[1])

    if crop_ratio > in_ratio:
        return 0, int(round((in_size[1] - crop_size[1]) / 2)), in_size[0], int(round((in_size[1] + crop_size[1]) / 2))
    elif crop_ratio < in_ratio:
        return int(round((in_size[0] - crop_size[0]) / 2)), 0, int(round((in_size[0] + crop_size[0]) / 2)), in_size[1]
    else:
        return int(round((in_size[0] - crop_size[0]) / 4)), \
            int(round((in_size[1] - crop_size[1]) / 4)), \
            int(round(in_size[1] - (in_size[1] - crop_size[1]) / 4)), \
            int(round(in_size[0] - (in_size[0] - crop_size[0]) / 4))


def resize_and_crop(img, size, crop_type):
    """
    Resize and crop an image to fit the specified size.

    :rtype : Image
    :argument img: image to resize.
    :argument @size `(width, height)` tuple.
    :argument crop_type:
    """

    image_size = best_image_size(img.size, size)
    img = img.resize(image_size, Image.ANTIALIAS)

    if crop_type == IMAGE_RESIZE_RULE_CROP_MIDDLE:
        image_crop = best_image_crop(image_size, size)

        if image_crop is not None:
            img = img.crop(image_crop)

    return img
