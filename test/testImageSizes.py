# coding=utf8

from unittest import TestCase
from ImageResizer.Resize import best_image_size, best_image_crop


class ImageSizeTests(TestCase):

    # landscape (1.33) to landscape (1.26)
    def test_best_fit_case_1(self):
        # constrained to height, width scaled (in ratio > out ratio)
        self.assertEqual(best_image_size((816, 612), (180, 143)), (190, 143))

    # landscape (1.33) to landscape (1.45)
    def test_best_fit_case_2(self):
        # constrained to width, height scaled (in ratio < out ratio)
        self.assertEqual(best_image_size((816, 612), (180, 124)), (180, 135))

    # landscape (1.33) to portrait (0.79)
    def test_best_fit_case_3(self):
        # constrained to height, width scaled (in ratio > out ratio)
        self.assertEqual(best_image_size((816, 612), (143, 180)), (240, 180))

    # portrait (0.75) to landscape (1.45)
    def test_best_fit_case_4(self):
        # constrained to width, height scaled (in ratio < out ratio)
        self.assertEqual(best_image_size((612, 816), (180, 124)), (180, 240))

    # square to square
    def test_best_fit_case_5(self):
        # size equals out size
        self.assertEqual(best_image_size((250, 250), (100, 100)), (100, 100))

    # crop the same size
    def test_best_crop_case_1(self):
        self.assertEqual(best_image_crop((100, 100), (100, 100)), None)

    # crop the same ratio
    def test_best_crop_case_2(self):
        self.assertEqual(best_image_crop((200, 200), (100, 100)), (25, 25, 175, 175))

    # crop bigger width than input
    def test_best_crop_case_3(self):
        self.assertEqual(best_image_crop((100, 100), (110, 100)), None)

    # crop bigger height than input
    def test_best_crop_case_4(self):
        self.assertEqual(best_image_crop((100, 100), (100, 110)), None)

    # crop bigger than input
    def test_best_crop_case_5(self):
        self.assertEqual(best_image_crop((100, 100), (200, 200)), None)