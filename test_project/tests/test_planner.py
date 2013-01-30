from django.utils import unittest

from planner.utils import double


class UtilsTests(unittest.TestCase):
    def test_multiply_numbers(self):
        self.assertEqual(double(4), 8)
