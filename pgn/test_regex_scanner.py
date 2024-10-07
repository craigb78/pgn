from unittest import TestCase

from pgn.token_type import *
from regex_scanner import *

class TestRegexSANScanner(TestCase):
    def test_san_dict_to_tokens_1(self):
        scanner = RegexSANScanner('Qxd8+')
        tokens = scanner.scan_tokens()

        self.assertEqual(tokens[0], Token(PIECE_TYPE, "Q", 0))
        self.assertEqual(tokens[1], Token(CAPTURE, "x", 0))
        self.assertEqual(tokens[2], Token(COL, "d", 0))
        self.assertEqual(tokens[3], Token(ROW, "8", 0))
        self.assertEqual(tokens[4], Token(CHECK, "+", 0))

    def test_san_dict_to_tokens_2(self):
        scanner = RegexSANScanner('e4')
        tokens = scanner.scan_tokens()

        self.assertEqual(tokens[0], Token(PIECE_TYPE, "P", 0))
        self.assertEqual(tokens[1], Token(COL, "e", 0))
        self.assertEqual(tokens[2], Token(ROW, "4", 0))

    def test_san_dict_to_tokens_3(self):
        scanner = RegexSANScanner('0-0-0+') # zeros
        tokens = scanner.scan_tokens()

        self.assertEqual(tokens[0], Token(CASTLE_QUEENS_SIDE, "0-0-0", 0))
        self.assertEqual(tokens[1], Token(CHECK, "+", 0))

    def test_san_dict_to_tokens_4(self):
        scanner = RegexSANScanner('O-O') # letter O
        tokens = scanner.scan_tokens()

        self.assertEqual(tokens[0], Token(CASTLE_KINGS_SIDE, "O-O", 0))


