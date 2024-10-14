"""
PGN to FEN
"""
import re

from pgn.pgn_board import PGNBoard
from pgn.pgn_squares import *
from pgn.piece_type import *
from pgn.piece_colours import *


def get_fen_icon(colour, piece_type):
    icon = '1'  # blank square
    if piece_type == PAWN:
        icon = 'P'
    elif piece_type == ROOK:
        icon = 'R'
    elif piece_type == KNIGHT:
        icon = 'N'
    elif piece_type == BISHOP:
        icon = 'B'
    elif piece_type == QUEEN:
        icon = 'Q'
    elif piece_type == KING:
        icon = 'K'

    # WHITE IS UPPER CASE
    # black is lower case
    if colour == BLACK:
        icon = icon.lower()

    return icon


def is_number(ch):
    return re.match(r"(\d)", ch) is not None

def pieces(board: PGNBoard):
    fen_str = ""
    sq = A8
    while sq >= H1:
        fen_str += get_fen_icon(*board.get_piece(sq))
        if (sq & (COL_H & ~H1)) != 0:
            fen_str += "/"  # row separator
        sq = sq >> 1
    return replace_empty(fen_str)


def replace_empty(in_str):
    """
    replace any sequences of  1s (empties) in the input with the length of the seq
    eg
    ppp111p1 becomes ppp3p1
    :param in_str:
    :return:
    """
    fen_str = ""
    for icon in in_str:
        if icon == '1' and len(fen_str) > 0 and is_number(fen_str[-1]):
            fen_str = fen_str[:-1] + str(int(fen_str[-1]) + 1)  # if the last char is a number, increment by 1
        else:
            fen_str += icon
    return fen_str

def active_colour(board: PGNBoard):
    if board.turn_counter.active_colour == WHITE:
        return "w"
    return "b"


def castling_availability(board: PGNBoard):
    ca = ""

    if board.turn_counter.white_kings_castle_avail:
        ca += "K"

    if board.turn_counter.white_queens_castle_avail:
        ca += "Q"

    if board.turn_counter.black_kings_castle_avail:
        ca += "k"

    if board.turn_counter.black_queens_castle_avail:
        ca += "q"

    return ca or '-'


def en_passant_target_sq(board: PGNBoard):
    return f"{board.turn_counter.en_passant_sq or '-'}"


def full_moves(board: PGNBoard):
    return f"{board.turn_counter.fullmoves}"


def half_moves(board: PGNBoard):
    return f"{board.turn_counter.halfmoves}"


def to_fen(board: PGNBoard):
    """
    generate a fen str for this board's positions
    :param board:
    :return:
    """
    return (f"{pieces(board)} "
            f"{active_colour(board)} "
            f"{castling_availability(board)} "
            f"{en_passant_target_sq(board)} "
            f"{half_moves(board)} "
            f"{full_moves(board)}")
