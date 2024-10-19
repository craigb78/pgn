import unittest

from pgn.pgn_board import PGNBoard
import pgn.fen_generator

class TestFenGenerator(unittest.TestCase):
    def test_to_fen(self):
        board = PGNBoard()
        self.assertEqual("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0", pgn.fen_generator.to_fen(board))

    def test_expand_empty(self):
        self.assertEqual("rnbqkbnr/pppppppp/11111111/11111111/11111111/11111111/111PPPPP/RNBQKBNR",
                         pgn.fen_generator.expand_empty("rnbqkbnr/pppppppp/8/8/8/8/3PPPPP/RNBQKBNR"))

    def test_replace_empty(self):
        self.assertEqual("ppp3pp", pgn.fen_generator.replace_empty("ppp111pp"))
        self.assertEqual("1pp3p1", pgn.fen_generator.replace_empty("1pp111p1"))
        self.assertEqual("pppppppp", pgn.fen_generator.replace_empty("pppppppp"))
        self.assertEqual("8", pgn.fen_generator.replace_empty("11111111"))
        self.assertEqual("R2Q2K1", pgn.fen_generator.replace_empty("R11Q11K1"))
        self.assertEqual("3N5", pgn.fen_generator.replace_empty("111N11111"))
        self.assertEqual("7P", pgn.fen_generator.replace_empty("1111111P"))


if __name__ == '__main__':
    unittest.main()
