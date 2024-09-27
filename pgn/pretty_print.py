from piece_colours import *
from piece_type import *
"""
    unicode chess piece characters
"""
WHITE_KING = "\u2654"
WHITE_QUEEN = "\u2655"
WHITE_ROOK = "\u2656"
WHITE_BISHOP = "\u2657"
WHITE_KNIGHT = "\u2658"
WHITE_PAWN = "\u2659"

BLACK_KING = "\u265A"
BLACK_QUEEN = "\u265B"
BLACK_ROOK = "\u265C"
BLACK_BISHOP = "\u265D"
BLACK_KNIGHT = "\u265E"
BLACK_PAWN = "\u265F"


def get_icon(colour, piece_type) -> str:
    if colour == WHITE:
        if piece_type == PAWN:
            return WHITE_PAWN
        elif piece_type == ROOK:
            return WHITE_ROOK
        elif piece_type == KNIGHT:
            return WHITE_KNIGHT
        elif piece_type == BISHOP:
            return WHITE_BISHOP
        elif piece_type == QUEEN:
            return WHITE_QUEEN
        elif piece_type == KING:
            return WHITE_KING
    else:
        if piece_type == PAWN:
            return BLACK_PAWN
        elif piece_type == ROOK:
            return BLACK_ROOK
        elif piece_type == KNIGHT:
            return BLACK_KNIGHT
        elif piece_type == BISHOP:
            return BLACK_BISHOP
        elif piece_type == QUEEN:
            return BLACK_QUEEN
        elif piece_type == KING:
            return BLACK_KING

    return ' ' # blank square
