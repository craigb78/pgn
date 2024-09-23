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