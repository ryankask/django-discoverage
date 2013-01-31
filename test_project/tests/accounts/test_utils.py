from django.utils import unittest

from accounts.utils import multiply_numbers, concat


class UtilsTests(unittest.TestCase):
    def test_multiply_numbers(self):
        self.assertEqual(multiply_numbers(2, 3), 6)

    def test_concat(self):
        self.assertEqual(concat('re', 'lease'), 'release')
