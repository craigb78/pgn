from pgn.piece_colours import opposite_colour, WHITE, BLACK
from pgn.pgn_squares import *
from pgn.piece_type import *

class TurnCounter:
    def __init__(self):
        # number of half moves
        self.halfmoves = 0

        # number of full moves
        self.fullmoves = 0

        # next colour to move
        self.active_colour = WHITE

        # if the pawn could be captured en passant
        self.en_passant_sq = None

        # castling availability
        self.black_kings_castle_avail = True
        self.black_queens_castle_avail = True
        self.white_kings_castle_avail = True
        self.white_queens_castle_avail = True

    def moved(self, colour, piece_type, origin_sq, dest_sq):
        if (piece_type == PAWN
                and bit_utils.is_mask_set(origin_sq, ROW_2)
                and bit_utils.is_mask_set(origin_sq, ROW_4)
                and colour == WHITE):
            self.en_passant_sq = dest_sq
        elif (piece_type == PAWN
              and bit_utils.is_mask_set(origin_sq, ROW_7)
              and bit_utils.is_mask_set(origin_sq, ROW_5)
              and colour == BLACK):
            self.en_passant_sq = dest_sq
        else:
            self.en_passant_sq = None

        if piece_type == ROOK and origin_sq == A1 and colour == WHITE:
            self.white_queens_castle_avail = False

        if piece_type == ROOK and origin_sq == H1 and colour == WHITE:
            self.white_kings_castle_avail = False

        if piece_type == ROOK and origin_sq == A8 and colour == BLACK:
            self.black_queens_castle_avail = False

        if piece_type == ROOK and origin_sq == H8 and colour == BLACK:
            self.black_kings_castle_avail = False

        if piece_type == KING and colour == WHITE:
            self.white_kings_castle_avail = False
            self.white_queens_castle_avail = False

        if piece_type == KING and colour == BLACK:
            self.black_kings_castle_avail = False
            self.black_queens_castle_avail = False

        self.active_colour = opposite_colour(colour)

        self.halfmoves += 1

        if colour == BLACK:
            self.fullmoves += 1


