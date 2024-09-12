from enum import Enum
from enum import unique

@unique
class TokenType(Enum):
    # single char tokens
    LEFT_TAG = 1
    RIGHT_TAG = 2

    LEFT_BRACE_COMMENT = 3
    RIGHT_BRACE_COMMENT = 4

    LEFT_BRACKET_COMMENT = 5
    RIGHT_BRACKET_COMMENT = 6

    TAKES = 7  # ie x

    NUMBER = 8 # ie the number prefixing a pair of moves

    # multi char tokens
    CASTLE_KINGS_SIDE = 30
    CASTLE_QUEENS_SIDE = 31

    CHECK = 32 # '+'
    CHECKMATE = 33 # '#'

    RESULT_DRAW = 35 #  "1/2-1/2"
    RESULT_WHITE_WIN =  36 # 1-0 (digit 1 dash digit zero)
    RESULT_BLACK_WIN =  37 # 0-1 (digit zero dash digit 1)
    RESULT_GAME_UNFINISHED = 38 # "*" indicates game abandoned unfinished or still in progress (etc)

    # literals

    TAG_NAME = 40
    TAG_VALUE = 41
    TAG_PAIR = 42


    IDENTIFIER = 100

    EOF = 200


    TAG_EVENT = 300
    TAG_SITE = 301
    TAG_DATE = 302
    TAG_ROUND = 303
    TAG_WHITE = 304
    TAG_BLACK = 305
    TAG_RESULT = 306

    START_TAGS = 310
    END_TAGS = 311

    START_MOVE_TEXT = 320
    END_MOVE_TEXT = 321

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
    # "1-0": TokenType.RESULT_WHITE_WIN,
    # "0-1": TokenType.RESULT_BLACK_WIN,
    # "1/2-1/2": TokenType.RESULT_DRAW,
    # "*": TokenType.RESULT_GAME_UNFINISHED,
    # "+": TokenType.CHECK,
    # "#": TokenType.CHECKMATE
}


def get_keyword(identifier):
    return KEYWORDS.get(identifier)
