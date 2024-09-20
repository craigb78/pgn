
# single char tokens
LEFT_BRACKET = 1
RIGHT_BRACKET = 2

LEFT_BRACE_COMMENT = 3
RIGHT_BRACE_COMMENT = 4

INTEGER = 5 # ie the number prefixing a pair of moves
PERIOD = 6 # after the move number indication

SYMBOL = 7 # [a-zA-Z0-9] [a-zA-Z0-9_+#=:-]*
STRING = 8  # ('\\\\' | '\\"' | ~[\\"])*

# keywords
RESULT_DRAW = 9 #  "1/2-1/2"
RESULT_WHITE_WIN =  10 # 1-0 (digit 1 dash digit zero)
RESULT_BLACK_WIN =  11 # 0-1 (digit zero dash digit 1)
RESULT_GAME_UNFINISHED = 22 # "*" indicates game abandoned unfinished or still in progress (etc)

EOF = 99

# non-terminal tokens (for parser)
TAG_PAIR = 1000


KEYWORDS = {
    # "O-O": token_type.CASTLE_KINGS_SIDE,
    # "O-O-O": token_type.CASTLE_QUEENS_SIDE,
    # "x": token_type.TAKES,
    # "Event": token_type.TAG_EVENT,
    # "Site" : token_type.TAG_SITE,
    # "Date": token_type.TAG_DATE,
    # "Round": token_type.TAG_ROUND,
    # "White": token_type.TAG_WHITE,
    # "Black": token_type.TAG_BLACK,
    # "Result": token_type.TAG_RESULT,
    "1-0": RESULT_WHITE_WIN,
     "0-1": RESULT_BLACK_WIN,
     "1/2-1/2": RESULT_DRAW,
     "*": RESULT_GAME_UNFINISHED
    # "+": token_type.CHECK,
    # "#": token_type.CHECKMATE
}


def get_pgn_keyword(identifier):
    return KEYWORDS.get(identifier)
