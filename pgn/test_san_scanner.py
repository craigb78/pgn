import unittest
import pgn.token_type as token_type
from pgn.san_scanner import SANScanner

class SANScannerTest(unittest.TestCase):

    # Fide Laws of chess appendix C,
    # Sample game:
    # 1. e4 e5 2. Nf3 Nf6 3. d4 exd4 4. e5 Ne4 5. Qxd4 d5 6. exd6e.p. Nxd6
    # 7. Bg5 Nc6 8. Qe3+ Be7 9. Nbd2 0-0 10. 0-0-0 Re8 11. Kb1 (=)
    """

    Or: 1. e4 e5 2. Nf3 Nf6 3. d4 ed4 4. e5 Ne4 5. Qd4 d5 6. ed6 Nd6 7. Bg5 Nc6 8. Qe3 Be7 9 Nbd2 0-0 10. 0-0-0 Re8 11. Kb1 (=)

    Or: 1. e2e4 e7e5 2.Ng1f3 Ng8f6 3. d2d4 e5xd4 4. e4e5 Nf6e4 5. Qd1xd4 d7d5 6. e5xd6 e.p. Ne4xd6 7. Bc1g5 Nb8c6 8. Qd4d3 Bf8e7 9. Nb1d2 0-0 10. 0-0-0 Rf8e8 11. Kb1 (=)
    """

    def scan(self, san_move):
        scanner = SANScanner(san_move)
        scanner.scan_tokens()
        scanner.print_tokens()
        if scanner.has_errors():
            scanner.print_errors()
            self.fail(f"Errors found when scanning san_move {san_move}")
        return scanner.tokens()

    def test_san_scan_1(self):
        tokens = self.scan("e4 e5")

        self.assertEqual(tokens[0].tt, token_type.COL)
        self.assertEqual(tokens[0].lexeme, 'e')
        self.assertEqual(tokens[1].tt, token_type.ROW)
        self.assertEqual(tokens[1].lexeme, '4')

        self.assertEqual(tokens[2].tt, token_type.COL)
        self.assertEqual(tokens[2].lexeme, 'e')
        self.assertEqual(tokens[3].tt, token_type.ROW)
        self.assertEqual(tokens[3].lexeme, '5')

        self.assertEqual(tokens[4].tt, token_type.EOF)

    def test_san_scan_2(self):
        tokens = self.scan("Nf3 Nf6")

        self.assertEqual(tokens[0].tt, token_type.PIECE_TYPE)
        self.assertEqual(tokens[0].lexeme, 'N')
        self.assertEqual(tokens[1].tt, token_type.COL)
        self.assertEqual(tokens[1].lexeme, 'f')
        self.assertEqual(tokens[2].tt, token_type.ROW)
        self.assertEqual(tokens[2].lexeme, '3')
        self.assertEqual(tokens[3].tt, token_type.PIECE_TYPE)
        self.assertEqual(tokens[3].lexeme, 'N')
        self.assertEqual(tokens[4].tt, token_type.COL)
        self.assertEqual(tokens[4].lexeme, 'f')
        self.assertEqual(tokens[5].tt, token_type.ROW)
        self.assertEqual(tokens[5].lexeme, '6')
        self.assertEqual(tokens[6].tt, token_type.EOF)

        # parser = SANParser(scanner.tokens())
        # ast = parser.parse()
        # if parser.has_errors():
        #     parser.print_errors()
        #     self.fail("Parser found errors")

    def test_san_scan_6(self):
        tokens = self.scan("exd6e.p. Nxd6")

        self.assertEqual(tokens[0].tt, token_type.COL)
        self.assertEqual(tokens[0].lexeme, 'e')
        self.assertEqual(tokens[1].tt, token_type.CAPTURE)
        self.assertEqual(tokens[2].lexeme, 'd')
        self.assertEqual(tokens[3].tt, token_type.ROW)
        self.assertEqual(tokens[3].lexeme, '6')
        self.assertEqual(tokens[4].tt, token_type.EN_PASSANT)



    def test_san_scan_10(self):
        tokens = self.scan("0-0-0 Re8")

        self.assertEqual(tokens[0].tt, token_type.CASTLE_QUEENS_SIDE)
        self.assertEqual(tokens[1].tt, token_type.PIECE_TYPE)
        self.assertEqual(tokens[1].lexeme, 'R')
        self.assertEqual(tokens[2].tt, token_type.COL)
        self.assertEqual(tokens[2].lexeme, 'e')
        self.assertEqual(tokens[3].tt, token_type.ROW)
        self.assertEqual(tokens[3].lexeme, '8')
        self.assertEqual(tokens[4].tt, token_type.EOF)


if __name__ == '__main__':
    unittest.main()
