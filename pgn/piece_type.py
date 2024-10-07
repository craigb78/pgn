import pgn.bit_utils as bit_utils

QUEEN = 2**1
BISHOP = 2**2
KNIGHT = 2**3
ROOK = 2**4
PAWN = 2**5
KING = 2**6

ALL_PIECES_TYPES = KING | QUEEN | BISHOP | KNIGHT | ROOK | PAWN


def piece_type_to_str(piece_type):
    piece_type_strs = []

    if bit_utils.is_mask_set(piece_type, KING):
        piece_type_strs.append('K')
    if bit_utils.is_mask_set(piece_type, QUEEN):
        piece_type_strs.append('Q')
    if bit_utils.is_mask_set(piece_type, BISHOP):
        piece_type_strs.append('B')
    if bit_utils.is_mask_set(piece_type, KNIGHT):
        piece_type_strs.append('N')
    if bit_utils.is_mask_set(piece_type, ROOK):
        piece_type_strs.append('R')
    if bit_utils.is_mask_set(piece_type, PAWN):
        piece_type_strs.append('P')

    return ",".join(piece_type_strs)


def str_to_piece_type(ch):
    if ch == 'K':
        return KING
    if ch == 'Q':
        return QUEEN
    if ch == 'B':
        return BISHOP
    if ch == 'N':
        return KNIGHT
    if ch == 'R':
        return ROOK
    if ch == 'P':
        return PAWN
