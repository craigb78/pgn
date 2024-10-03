from unittest import TestCase
import bit_utils
from pgn_squares import *

class Test(TestCase):
    def test_is_clear_run(self):
        bitmap = A8 | A1
        self.assertTrue(bit_utils.is_clear_run(bitmap=bitmap, highest_bit=A8, lowest_bit=A1),
                        "A1 and A8 are set, with nothing set in between")

        bitmap = A8 | A3 | A1
        self.assertFalse(bit_utils.is_clear_run(bitmap=bitmap, highest_bit=A8, lowest_bit=A1),
                        "A1 and A8 are set, with A3 in between")




