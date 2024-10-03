from pgn.pgn_squares import *
from pgn.piece_colours import piece_colour_to_str
from pgn.piece_type import *


class PGNPly:
    def __init__(self):
        self.colour: int = 0
        self.piece_type: int = 0
        self.capture: bool = False
        self.castle_kings_side: bool = False
        self.castle_queens_side: bool = False
        self.origin_sq: int = 0
        self.origin_row: int = 0
        self.origin_col: int = 0
        self.dest_sq: int = 0

    def __str__(self):
        return (f"PGNPly(color:{piece_colour_to_str(self.colour)},"
                f"piece_type:{piece_type_to_str(self.piece_type)},"
                f"capture:{self.capture},"
                f"castle king:{self.castle_kings_side},"
                f"castle queen:{self.castle_queens_side})"
                f"dest_sq:{square_to_str(self.dest_sq)}")


"""
A full move is a turn by both players, White and Black. A turn by either White or Black is a half-move, or (in computer context) one ply.
"""
class PGNMove:
    def __init__(self, white_ply, black_ply):
        self.white_ply: PGNPly = white_ply
        self.black_ply: PGNPly = black_ply

    def __str__(self):
        return f"PGNMove(white_ply:{self.white_ply},black_ply:{self.black_ply})"
