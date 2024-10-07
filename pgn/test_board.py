import unittest
from pgn.pgn_board import *

class TestBoard(unittest.TestCase):


    def test_en_passant_black_down_right(self):
        b = PGNBoard()  # board with default starting positions

        b.make_move(PAWN, BLACK, B7, B4)
        b.make_move(PAWN, WHITE, C2, C4)
        print(b)
        moves = b.determine_origin_sq(PAWN, BLACK, dest_square=C3, origin_col=COL_B, capture=True)
        self.assertEqual(moves, B4, "black can take en passant up left")

    def test_en_passant_black_down_leftt(self):
        b = PGNBoard()  # board with default starting positions

        b.make_move(PAWN, BLACK, B7, B4)
        b.make_move(PAWN, WHITE, A2, A4)
        print(b)
        moves = b.determine_origin_sq(PAWN, BLACK, dest_square=A3, origin_col=COL_B, capture=True)
        self.assertEqual(moves, B4, "black can take en passant up right")

    def test_en_passant_white_up_left(self):
        b = PGNBoard()  # board with default starting positions

        b.make_move(PAWN, WHITE, C2, C5)
        b.make_move(PAWN, BLACK, B7, B5)

        moves = b.determine_origin_sq(PAWN, WHITE, dest_square=B6, origin_col=COL_C, capture=True)
        self.assertEqual(moves, C5, "white can take en passant up left")

    def test_en_passant_white_up_right(self):
        b = PGNBoard()  # board with default starting positions

        b.make_move(PAWN, WHITE, A2, A5)
        b.make_move(PAWN, BLACK, B7, B5)

        moves = b.determine_origin_sq(PAWN, WHITE, dest_square=B6, origin_col=COL_A, capture=True)
        self.assertEqual(moves, A5, "white can take en passant up left")

    def test_can_move_white_pawn(self):
        b = PGNBoard()  # board with default starting positions

        # up one
        pawn_moves = b.determine_origin_sq(PAWN, WHITE, A3)
        self.assertEqual(pawn_moves, A2)

        # up two
        pawn_moves = b.determine_origin_sq(PAWN, WHITE, C4)
        self.assertEqual(pawn_moves, C2)

        # taking to left
        b.make_move(PAWN, WHITE, A2, A4)
        b.make_move(PAWN, BLACK, B7, B5)
        b.make_move(PAWN, WHITE, C2, C4)

        pawn_moves = b.determine_origin_sq(PAWN, WHITE, dest_square=B5, origin_col=COL_C, capture=True)
        self.assertEqual(pawn_moves, C4)

        # taking to right
        b.make_move(PAWN, BLACK, D7, D3)
        print(b)
        pawn_moves = b.determine_origin_sq(PAWN, WHITE, dest_square=D3, origin_col=COL_E, capture=True)
        self.assertEqual(pawn_moves, E2)

    def test_can_move_knight(self):
        b = PGNBoard() # board with default starting positions
        knight_moves = b.determine_origin_sq(KNIGHT, WHITE, C3)
        self.assertEqual(knight_moves, B1)

    def test_can_move_rook(self):
        b = PGNBoard()  # board with default starting positions

        try:
            # ROOK A1 and Rook H8 cannot move to E5.
            b.determine_origin_sq(ROOK, WHITE, E5)
        except:
            pass  # expected exception

        b.make_move(PAWN, WHITE, A2, A4)
        a1_rook_moves = b.determine_origin_sq(ROOK, WHITE, A3)
        self.assertEqual(a1_rook_moves, A1, "rook can move A1 to A3")

        # Both white rooks D3, so need to supply rank or file of source
        b.make_move(ROOK, WHITE, A1, A3)
        b.make_move(PAWN, WHITE, H2, H4)
        b.make_move(ROOK, WHITE, H1, H3)

        try:
            b.determine_origin_sq(ROOK, WHITE, D3, origin_row=ROW_3)
        except:
            pass  # multiple moves because ROW_3 doesn't disambiguate

        a1_rook_moves = b.determine_origin_sq(ROOK, WHITE, D3, origin_square=COL_A)
        self.assertEqual(a1_rook_moves, A3)


    def test_can_move_bishop(self):
        b = PGNBoard()  # board with default starting positions

        b.make_move(PAWN, WHITE, B2, B3)
        bishop_moves = b.determine_origin_sq(BISHOP, WHITE, A3)
        self.assertEqual(bishop_moves, C1, "bishop can move diagonal left")
        b.make_move(BISHOP, WHITE, C1, A3)


        bishop_moves = b.determine_origin_sq(BISHOP, WHITE, C5)
        self.assertEqual(bishop_moves, A3, "bishop can move diagonal right")
        b.make_move(BISHOP, WHITE, A3, C5)

        # put the pawn in the way of the bishops intended dest square
        b.make_move(PAWN, WHITE, B3, B4)
        try:
            b.determine_origin_sq(BISHOP, WHITE, A3)
        except:
            pass # there are no bishops that can move to the dest square.



    def test_can_move_queen(self):
        b = PGNBoard()  # board with default starting positions
        b.make_move(PAWN, WHITE, E2, E3)
        a1_queen_moves = b.determine_origin_sq(QUEEN, WHITE, H5)
        self.assertEqual(a1_queen_moves, D1, "queen can make a diagonal move")
        b.make_move(QUEEN, WHITE, D1, H5)

        a1_queen_moves = b.determine_origin_sq(QUEEN, WHITE, A5)
        self.assertEqual(square_to_str(a1_queen_moves), square_to_str(H5), "queen can make a horizontal move")
        b.make_move(QUEEN, WHITE, H5, A5)

        a1_queen_moves = b.determine_origin_sq(QUEEN, WHITE, A6)
        self.assertEqual(a1_queen_moves, A5, "queen can make a vertical move")
        b.make_move(QUEEN, WHITE, A5, A6)

    def test_can_move_king(self):
        b = PGNBoard()  # board with default starting positions
        print(b)
        possible_dest_sq = [D1, D2, E2, F2, F1]
        for dest_sq in possible_dest_sq:
            a1_king_moves = b.determine_origin_sq(KING, WHITE, dest_sq)
            self.assertEqual(a1_king_moves, E1, f"King should be able to move from E1 to {square_to_str(dest_sq)}")

    def test_pawn_moves_white(self):
        # forward one place
        print('{:064b}'.format(C2), "C2")
        print('{:064b}'.format(C3), "C3")
        print('{:064b}'.format(C2 << 8), "C2<<8", "EQUALS C3: ", (C2 << 8) == C3)
        self.assertTrue((C2 << 8) == C3, f'C2<<8 EQUALS C3 {C2 << 8:064b}')

        # forward two places but only from 2nd file
        print('{:064b}'.format(C2), "C2")
        print('{:064b}'.format(C4), "C4")
        print('{:064b}'.format(C2 << 16), "C2<<16", "EQUALS C4: ", (C2 << 16) == C4)
        self.assertTrue((C2 << 16) == C4, f'C2<<16 EQUALS C4 {C2 << 16:064b}')

        # can take diaognal up left
        print('{:064b}'.format(C2), "C2")
        print('{:064b}'.format(B3), "B3")
        print('{:064b}'.format(C2 << 9), "C2<<9", "EQUALS B3: ", (C2 << 9) == B3)
        self.assertTrue((C2 << 9) == B3, f'C2<<9 EQUALS B3 {C2 << 9:064b}')

        # can take another piece diagonal up right
        print('{:064b}'.format(C2), "E5")
        print('{:064b}'.format(D3), "D3")
        print('{:064b}'.format(C2 << 7), "C2<<7", "EQUALS D3: ", (C2 << 7) == D3)
        self.assertTrue((C2 << 7) == D3, f'C2<<7 EQUALS D3 {C2 << 7:064b}')

        # en passant???

    def test_king_moves(self):
        """
        UP from E5 to E6 
          #
          K
        """
        print('{:064b}'.format(E5), "E5")
        print('{:064b}'.format(E6), "E6")
        print('{:064b}'.format( E5<<8 ), "E5<<8", "EQUALS E6: ", (E5 << 8) == E6)
        self.assertTrue((E5<<8) == E6, f'E5<<8 EQUALS E6 {E5 << 8:064b}')

        """
        DIAGONAL UP LEFT from E5 to D6
        #
          K
        """
        print('{:064b}'.format(E5), "E5")
        print('{:064b}'.format(D6), "D6")
        print('{:064b}'.format(E5 << 9), "E5<<9", "EQUALS D6: ", (E5 << 9) == D6)
        self.assertTrue((E5 << 9) ==  D6, f'E5<<9 EQUALS D6 {E5 << 9:064b}')

        """
        DIAGONAL UP RIGHT from E5 to F6
          #
        K
        """
        print('{:064b}'.format(E5), "E5")
        print('{:064b}'.format(F6), "F6")
        print('{:064b}'.format(E5 << 7), "E5<<7", "EQUALS F6: ", (E5 << 7) == F6)
        self.assertTrue((E5 << 7) ==  F6, f'E5<<7 EQUALS F6 {E5 << 7:064b}')

        """
        DOWN from E5 to E4 
        K
        #
        """
        print('{:064b}'.format(E5), "E5")
        print('{:064b}'.format(E4), "E4")
        print('{:064b}'.format(E5 >> 8), "E5>>8", "EQUALS E4: ", (E5 >> 8) == E4)
        self.assertTrue((E5 >> 8) == E4, f'E5>>8 EQUALS E4 {E5 >> 8:064b}')

        """
        DIAGONAL DOWN LEFT from E5 to D4
          K
        # 
        """
        print('{:064b}'.format(E5), "E5")
        print('{:064b}'.format(D4), "D4")
        print('{:064b}'.format(E5 >> 7), "E5>>7", "EQUALS D4: ", (E5 >> 7) == D4)
        self.assertTrue((E5 >> 7) ==  D4, f'E5>>7 EQUALS D4 {E5 >> 7:064b}')

        """
        DIAGONAL DOWN RIGHT from E5 to F4
        K
          #
        """
        print('{:064b}'.format(E5), "E5")
        print('{:064b}'.format(F4), "F4")
        print('{:064b}'.format(E5 >> 9), "E5>>9", "EQUALS F4: ", (E5 >> 9) == F4)
        self.assertTrue((E5 >> 9) == F4, f'E5>>9 EQUALS F4 {E5 >> 9:064b}')

        """
        LEFT from E5 to D5
        #K
        """
        print('{:064b}'.format(E5), "E5")
        print('{:064b}'.format(D5), "D5")
        print('{:064b}'.format(E5 << 1), "E5<<8", "EQUALS D5: ", (E5 << 1) == D5)
        self.assertTrue((E5 << 1) == D5, f'E5<<1 EQUALS D5 {E5 << 1:064b}')


        """
        RIGHT from E5 to F5
        K#
        """
        print('{:064b}'.format(E5), "E5")
        print('{:064b}'.format(E4), "F5")
        print('{:064b}'.format(E5 >> 1), "E5>>1", "EQUALS F5: ", (F5 >> 1) == F5)
        self.assertTrue((E5 >> 1) ==  F5, f'E5>>1 EQUALS F5 {E5 >> 1:064b}')


    def test_knight_moves(self):
        b = PGNBoard()
        #b.make_move(KNIGHT, WHITE, B1, C3)
        print(str(b))

        """
        ## UP TO RIGHT
        #
        K
        """
        print('{:064b}'.format(E5), "E5")
        print('{:064b}'.format(F7), "F7")
        print('{:064b}'.format( E5<<15 ), "E5<<15", "EQUALS F7: ", (E5 << 15) == F7)
        self.assertTrue((E5<<15) == F7, f'E5<<15 EQUALS F7 {E5 << 15:064b}')


        """
        ## UP TO LEFT
         #
         K
        """
        print('{:064b}'.format(B2), "E5")
        print('{:064b}'.format(D7), "D7")
        print('{:064b}'.format(E5 << 17), "E5<<17", "EQUALS D7: ", (E5 << 17) == D7)
        self.assertTrue((E5 << 17) == D7, f'E5<<17 EQUALS D7: {E5 << 17:064b}')

        """
        K
        #
        ## DOWN TO RIGHT
        """
        print('{:064b}'.format(E5), "E5")
        print('{:064b}'.format(F3), "F3")
        print('{:064b}'.format( E5>>17 ), "E5>>17", "EQUALS F3: ", (E5>>17) == F3)
        self.assertTrue((E5 >> 17) == F3, f'E5>>17 EQUALS F3: {E5 >> 17:064b}')
        """
         K
         #
        ## DOWN TO LEFT
        """
        print('{:064b}'.format(E5), "E5")
        print('{:064b}'.format(D3), "D3")
        print('{:064b}'.format( E5>>15 ), "E5>>15", "EQUALS D3: ", (E5>>15) == D3)
        self.assertTrue((E5 >> 15) == D3, f'E5>>15 EQUALS D3: {E5 >> 15:064b}')

        """
        #
        ##K LEFT and UP
        """
        print('{:064b}'.format(E5), "E5")
        print('{:064b}'.format(D3), "C6")
        print('{:064b}'.format(E5 << 10), "E5<<10", "EQUALS C6: ", (E5 << 10) == C6)
        self.assertTrue((E5 << 10) == C6, f'E5<<10 EQUALS C6: {E5 << 10:064b}')


        """
        ##K LEFT and DOWN
        #
        """
        print('{:064b}'.format(E5), "E5")
        print('{:064b}'.format(C4), "C4")
        print('{:064b}'.format(E5 >> 6), "E5>>6", "EQUALS C4: ", (E5 >> 6) == C4)
        self.assertTrue((E5 >> 6) == C4, f'E5>>6 EQUALS C4 {E5 >> 6:064b}')

        """
          #
        K## RIGHT and UP
        """
        print('{:064b}'.format(E5), "E5")
        print('{:064b}'.format(G6), "G6")
        print('{:064b}'.format(E5 << 6), "E5<<6", "EQUALS G6: ", (E5 << 6) == G6)
        self.assertTrue((E5 << 6) == G6, f'E5<<6 EQUALS G6: {E5 << 6:064b}')


        """
        K## RIGHT and DOWN
          #
        """
        print('{:064b}'.format(E5), "E5")
        print('{:064b}'.format(G4), "G4")
        print('{:064b}'.format(E5 >> 10), "E5>>10", "EQUALS G4: ", (E5>>10) == G4)
        self.assertTrue((E5 >> 10) == G4, f' E5>>10 EQUALS G4: {E5 >> 10:064b}')


    def test_to_str(self):
        # given
        b = PGNBoard()
        expected_b_str = """	―		―		―		―		―		―		―		―	
8|	♜	|	♞	|	♝	|	♛	|	♚	|	♝	|	♞	|	♜	|
	―		―		―		―		―		―		―		―	
7|	♟	|	♟	|	♟	|	♟	|	♟	|	♟	|	♟	|	♟	|
	―		―		―		―		―		―		―		―	
6|	 	|	 	|	 	|	 	|	 	|	 	|	 	|	 	|
	―		―		―		―		―		―		―		―	
5|	 	|	 	|	 	|	 	|	 	|	 	|	 	|	 	|
	―		―		―		―		―		―		―		―	
4|	 	|	 	|	 	|	 	|	 	|	 	|	 	|	 	|
	―		―		―		―		―		―		―		―	
3|	 	|	 	|	 	|	 	|	 	|	 	|	 	|	 	|
	―		―		―		―		―		―		―		―	
2|	♙	|	♙	|	♙	|	♙	|	♙	|	♙	|	♙	|	♙	|
	―		―		―		―		―		―		―		―	
1|	♖	|	♘	|	♗	|	♕	|	♔	|	♗	|	♘	|	♖	|
	―		―		―		―		―		―		―		―	
 |	A	|	B	|	C	|	D	|	E	|	F	|	G	|	H	|"""

        # when
        b_str = str(b)

        # then
        print(b_str)
        self.assertEqual(expected_b_str, b_str)