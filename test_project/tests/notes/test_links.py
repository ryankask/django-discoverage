from django.utils import unittest

from links.utils import incr


class UtilsTests(unittest.TestCase):
    def test_incr_number(self):
        self.assertEqual(incr(2), 3)
