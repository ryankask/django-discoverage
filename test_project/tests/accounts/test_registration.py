from django.utils import unittest

from registration.utils import subtract_numbers


class UtilsTests(unittest.TestCase):
    TESTS_APPS = ['registration']

    def test_subtract_numbers(self):
        self.assertEqual(subtract_numbers(2, 3), -1)
