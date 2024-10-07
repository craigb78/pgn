from typing import Sequence
import pgn.token_type as tt
import re
from pgn.pgn_token import *


# as an alternative to san_scanner

class RegexSANScanner:

    def __init__(self, san_str):
        self.__san_str = san_str

    def scan_tokens(self):
        return self.san_dict_to_tokens(self.san_regex(self.__san_str))

    def san_regex(self, source: str):
        san_pattern = re.compile(r'(?P<piece_type>[KQBNR])?'
                                 r'(?P<castle_queens_side>O-O-O|0-0-0)?'
                                 r'(?P<castle_kings_side>O-O|0-0)?'
                                 r'(?P<enpassant>e\.p\.)?'
                                 r'(?P<origin_col>[a-h])?'
                                 r'(?P<origin_row>[1-8])?'
                                 r'(?P<capture>x)?'
                                 r'(?P<dest_col>[a-h])?'
                                 r'(?P<dest_row>[1-8])?'
                                 r'(?P<check>\+[^+]?)?'
                                 r'(?P<checkmate>\+\+|#)?'
                                 )
        match = san_pattern.search(source)
        if match:
            return match.groupdict()
        return {}


    def san_dict_to_tokens(self, san_dict) -> []:
        san_tokens = []

        if lexeme := san_dict.get("castle_kings_side"):
            san_tokens.append(Token(tt.CASTLE_KINGS_SIDE, lexeme, 0))
        elif lexeme := san_dict.get("castle_queens_side"):
            san_tokens.append(Token(tt.CASTLE_QUEENS_SIDE, lexeme, 0))
        elif lexeme := san_dict.get("piece_type"):
            san_tokens.append(Token(tt.PIECE_TYPE, lexeme, 0))
        else:
            san_tokens.append(Token(tt.PIECE_TYPE, "P", 0))

        if lexeme := san_dict.get("origin_col"):
            san_tokens.append(Token(tt.COL, lexeme, 0))

        if lexeme := san_dict.get("origin_row"):
            san_tokens.append(Token(tt.ROW, lexeme, 0))

        if lexeme := san_dict.get("capture"):
            san_tokens.append(Token(tt.CAPTURE, lexeme, 0))

        if lexeme := san_dict.get("dest_col"):
            san_tokens.append(Token(tt.COL, lexeme, 0))

        if lexeme := san_dict.get("dest_row"):
            san_tokens.append(Token(tt.ROW, lexeme, 0))

        if lexeme := san_dict.get("check"):
            san_tokens.append(Token(tt.CHECK, lexeme, 0))

        if lexeme := san_dict.get("checkmate"):
            san_tokens.append(Token(tt.CHECKMATE, lexeme, 0))

        if lexeme := san_dict.get("enpassant"):
            san_tokens.append(Token(tt.EN_PASSANT, lexeme, 0))

        return san_tokens

