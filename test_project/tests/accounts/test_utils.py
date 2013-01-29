from django.utils import unittest

from accounts.utils import multiply_numbers


class UtilsTests(unittest.TestCase):
    def test_multiply_numbers(self):
        self.assertEqual(multiply_numbers(2, 3), 6)
