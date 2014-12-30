import json


def sizes_from_file(sizes_file):
    json_data = open(sizes_file)
    image_sizes = json.load(json_data)["sizes"]
    json_data.close()

    size_objects = []

    for size in image_sizes:
        size_objects.append(Size(size['width'], size['height'], size['mode']))

    return size_objects


class Size:

    def __init__(self, width, height, mode):
        self.width = width
        self.height = height
        self.mode = mode

    def key_name_for_size(self, filename):
        return "{0}/{1}/{2}/{3}".format(self.width, self.height, self.mode, filename)
