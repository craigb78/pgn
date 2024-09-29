import unittest
from pgn.san_parser import SANParser
from pgn.pgn_move import *
from pgn.pgn_token import Token
from pgn.piece_type import *
from pgn.piece_colours import *
from pgn.pgn_squares import *
class TestSANParser(unittest.TestCase):

    def test_(self):
        # given
        san_parser = SANParser()
        white_san_tokens: [Token] = [
            Token(tt=510, lexeme='e', line=1),
            Token(tt=500, lexeme='4', line=1)
        ]
        black_san_tokens: [Token] = [
            Token(tt=510, lexeme='e', line=1),
            Token(tt=500, lexeme='5', line=1)
        ]
        # when
        san_parser.parse_san_move(white_san_tokens, black_san_tokens)
        pgn_moves: [PGNMove] = san_parser.collect()

        # then
        print(dir(PGNPly))

        self.assertTrue(len(pgn_moves), "Expected 1 move")
        self.assertTrue(pgn_moves[0].white_ply is not None, "Expected white ply")
        self.assertTrue(pgn_moves[0].black_ply is not None, "Expected black ply")

        self.assertEqual(pgn_moves[0].white_ply.colour, WHITE, "")
        self.assertEqual(pgn_moves[0].white_ply.piece_type, PAWN, "")
        self.assertEqual(pgn_moves[0].white_ply.capture, False, "")
        self.assertEqual(pgn_moves[0].white_ply.castle_kings_side, False, "")
        self.assertEqual(pgn_moves[0].white_ply.castle_queens_side, False, "")
        #self.assertEqual(pgn_moves[0].white_ply.origin_sq, E2, "")
        #self.assertEqual(pgn_moves[0].white_ply.origin_row, ROW_2, "")
        #self.assertEqual(pgn_moves[0].white_ply.origin_col, COL_E, "")
        self.assertEqual(pgn_moves[0].white_ply.dest_sq,  E4, "")
