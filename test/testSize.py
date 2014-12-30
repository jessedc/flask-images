# coding=utf8

from unittest import TestCase
from ImageResizer import Resize
from ImageResizer.Size import Size


class ImageSizeTests(TestCase):

    def test_size_key_name_happy_path(self):
        size = Size(100, 200, Resize.IMAGE_RESIZE_RULE_CROP_NONE)
        key_name = size.key_name_for_size('test.jpg')

        self.assertEqual(key_name, '100/200/resize/test.jpg')