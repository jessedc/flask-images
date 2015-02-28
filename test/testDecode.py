__author__ = 'jesse'

import unittest
import urllib


class DecodeTests(unittest.TestCase):
    def test_decoding_plus_symbols(self):

        url = 'photos/Screen+shot+2001-27+at+7.30.19+PM'
        un_quoted_url = urllib.unquote_plus(urllib.unquote(url)).decode('utf8')

        self.assertEqual(un_quoted_url, 'photos/Screen shot 2001-27 at 7.30.19 PM')

    def test_percent_escapes(self):

        url = 'photos/ABC%27s+Brisbane+%2844+of+42%29'
        un_quoted_url = urllib.unquote_plus(urllib.unquote(url)).decode('utf8')

        self.assertEqual(un_quoted_url, 'photos/ABC\'s Brisbane (44 of 42)')


if __name__ == '__main__':
    unittest.main()
