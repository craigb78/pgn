KING = 2**0
QUEEN = 2**1
BISHOP= 2**2
KNIGHT= 2**3
ROOK= 2**4
PAWN= 2**5

def piece_type_to_str(piece_type):
    if piece_type == KING:
        return 'K'
    if piece_type == QUEEN:
        return 'Q'
    if piece_type == BISHOP:
        return 'B'
    if piece_type == KNIGHT:
        return 'N'
    if piece_type == ROOK:
        return 'R'
    if piece_type == PAWN:
        return 'P'
    return None


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

