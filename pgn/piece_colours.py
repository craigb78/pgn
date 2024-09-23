WHITE=2**0
BLACK=2**1


def piece_colour_to_str(piece_colour):
    if piece_colour == WHITE:
        return "WHITE"
    if piece_colour == BLACK:
        return "BLACK"
    return None