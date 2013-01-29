from django.utils import unittest

from bookmarks.utils import square_num

TESTS_APPS = ['bookmarks']

class UtilsTests(unittest.TestCase):
    def test_square_num(self):
        self.assertEqual(square_num(3), 9)
