from enum import Enum
from enum import unique, auto

@unique
class TokenType(Enum):
    # single char tokens
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()

    LEFT_BRACE_COMMENT = auto()
    RIGHT_BRACE_COMMENT = auto()

    INTEGER = auto() # ie the number prefixing a pair of moves
    PERIOD = auto() # after the move number indication

    SYMBOL = auto() # [a-zA-Z0-9] [a-zA-Z0-9_+#=:-]*
    STRING = auto()  # ('\\\\' | '\\"' | ~[\\"])*

    # keywords
    RESULT_DRAW = auto() #  "1/2-1/2"
    RESULT_WHITE_WIN =  auto() # 1-0 (digit 1 dash digit zero)
    RESULT_BLACK_WIN =  auto() # 0-1 (digit zero dash digit 1)
    RESULT_GAME_UNFINISHED = auto() # "*" indicates game abandoned unfinished or still in progress (etc)

    EOF = auto()

    # non-terminal tokens (for parser)
    TAG_PAIR = auto()





KEYWORDS = {
    # "O-O": TokenType.CASTLE_KINGS_SIDE,
    # "O-O-O": TokenType.CASTLE_QUEENS_SIDE,
    # "x": TokenType.TAKES,
    # "Event": TokenType.TAG_EVENT,
    # "Site" : TokenType.TAG_SITE,
    # "Date": TokenType.TAG_DATE,
    # "Round": TokenType.TAG_ROUND,
    # "White": TokenType.TAG_WHITE,
    # "Black": TokenType.TAG_BLACK,
    # "Result": TokenType.TAG_RESULT,
    "1-0": TokenType.RESULT_WHITE_WIN,
     "0-1": TokenType.RESULT_BLACK_WIN,
     "1/2-1/2": TokenType.RESULT_DRAW,
     "*": TokenType.RESULT_GAME_UNFINISHED
    # "+": TokenType.CHECK,
    # "#": TokenType.CHECKMATE
}


def get_keyword(identifier):
    return KEYWORDS.get(identifier)
