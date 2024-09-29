# single char tokens
LEFT_BRACKET = 1
RIGHT_BRACKET = 2

LEFT_BRACE_COMMENT = 3
RIGHT_BRACE_COMMENT = 4

INTEGER = 5  # ie the number prefixing a pair of moves
PERIOD = 6  # after the move number indication

SYMBOL = 7  # [a-zA-Z0-9] [a-zA-Z0-9_+#=:-]*
STRING = 8  # ('\\\\' | '\\"' | ~[\\"])*

# keywords
RESULT_DRAW = 9  # "1/2-1/2"
RESULT_WHITE_WIN = 10  # 1-0 (digit 1 dash digit zero)
RESULT_BLACK_WIN = 11  # 0-1 (digit zero dash digit 1)
RESULT_GAME_UNFINISHED = 22  # "*" indicates game abandoned unfinished or still in progress (etc)

EOF = 99

# SAN move tokens
CASTLE_KINGS_SIDE = 100
CASTLE_QUEENS_SIDE = 101
CAPTURE = 102
CHECKMATE = 103
CHECK = 105
EN_PASSANT = 106
DRAW_OFFERED = 107

# KING = 200
# QUEEN = 201
# KNIGHT = 202
# BISHOP = 203
# ROOK = 204
# PAWN = 205
PIECE_TYPE = 220
ROW = 500 # numbers
COL = 510 # letters

#
# A = 400
# B = 401
# C = 402
# D = 403
# E = 404
# F = 405
# G = 406
# H = 407
#
# _1 = 410
# _2 = 411
# _3 = 412
# _4 = 413
# _5 = 414
# _6 = 415
# _7 = 416
# _8 = 417

PGN_KEYWORDS = {
    "1-0": RESULT_WHITE_WIN,
    "0-1": RESULT_BLACK_WIN,
    "1/2-1/2": RESULT_DRAW,
    "*": RESULT_GAME_UNFINISHED
}

SAN_KEYWORDS = {
    "0-0": CASTLE_KINGS_SIDE,  # with zeros
    "0-0-0": CASTLE_QUEENS_SIDE,
    "O-O": CASTLE_KINGS_SIDE,  # with letter O
    "O-O-O": CASTLE_QUEENS_SIDE,

    "x": CAPTURE,
    "++": CHECKMATE,
    "#": CHECKMATE,
    "+": CHECK,
    "e.p.": EN_PASSANT,
    "(=)": DRAW_OFFERED
}


def get_pgn_keyword(identifier):
    return PGN_KEYWORDS.get(identifier)

def get_san_keyword(identifier):
    return SAN_KEYWORDS.get(identifier)


def tt_to_str(tt):
    if tt == LEFT_BRACKET:
        return "LEFT_BRACKET"
    elif tt == RIGHT_BRACKET:
        return "RIGHT_BRACKET"
    elif tt == LEFT_BRACE_COMMENT:
        return "LEFT_BRACE_COMMENT"
    elif tt == RIGHT_BRACE_COMMENT:
        return "RIGHT_BRACE_COMMENT"
    elif tt == INTEGER:
        return "INTEGER"
    elif tt == PERIOD:
        return "PERIOD"
    elif tt == SYMBOL:
        return "SYMBOL"
    elif tt == STRING:
        return "STRING"
    elif tt == RESULT_DRAW:
        return "RESULT_DRAW"
    elif tt == RESULT_WHITE_WIN:
        return "RESULT_WHITE_WIN"
    elif tt == RESULT_BLACK_WIN:
        return "RESULT_BLACK_WIN"
    elif tt == RESULT_GAME_UNFINISHED:
        return "RESULT_GAME_UNFINISHED"
    elif tt == CASTLE_KINGS_SIDE:
        return "CASTLE_KINGS_SIDE"
    elif tt == CASTLE_QUEENS_SIDE:
        return "CASTLE_QUEENS_SIDE"
    elif tt == CAPTURE:
        return "CAPTURE"
    elif tt  == CHECKMATE:
        return "CHECKMATE"
    elif tt == CHECK:
        return "CHECK"
    elif tt == EN_PASSANT:
        return "EN_PASSANT"
    elif tt == DRAW_OFFERED:
        return "DRAW_OFFERED"
    elif tt == PIECE_TYPE:
        return "PIECE_TYPE"
    elif tt == ROW:
        return "ROW"
    elif tt == COL:
        return "COL"
    elif tt == EOF:
        return "EOF"
    else:
        return str(tt)