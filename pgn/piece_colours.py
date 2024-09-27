WHITE=2**50
BLACK=2**51


def piece_colour_to_str(piece_colour):
    if piece_colour == WHITE:
        return "WHITE"
    if piece_colour == BLACK:
        return "BLACK"
    return None
