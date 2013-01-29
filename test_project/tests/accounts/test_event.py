from django.utils import unittest

from event.utils import decr


class UtilsTests(unittest.TestCase):
    def test_decr(self):
        self.assertEqual(decr(2), 1)
