from django.utils import unittest

from todo.notes.utils import add_numbers


class UtilsTests(unittest.TestCase):
    def test_add_numbers(self):
        self.assertEqual(add_numbers(2, 3), 5)
