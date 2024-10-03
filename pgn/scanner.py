"""

http://www.saremba.de/chessgml/standards/pgn/pgn-complete.htm#:~:text=PGN%20is%20%22Portable%20Game%20Notation,and%20generation%20by%20computer%20programs.

"""
from typing import Sequence
from pgn_logging import logger
import pgn.token_type as token_type
from pgn.pgn_token import Token
class Scanner:
    """ scanner for PGN files """
    def __init__(self, source):
        self.__source: Sequence = source
        self.__tokens = []
        self.__start: int = 0
        self.__current: int = 0 # index of current char
        self.__line: int = 1

    def tokens(self) -> []:
        return self.__tokens

    def print_tokens(self):
        for next_token in self.__tokens:
            logger.debug(next_token)

    def at_end(self):
        """ have we consumed all the chars in self.source??"""
        return self.__current >= len(self.__source)

    def scan_tokens(self, scan_token_callback):
        """ populate the list of tokens """
        while not self.at_end():
            self.__start = self.__current
            scan_token_callback()

        self.__tokens.append(Token(token_type.EOF, lexeme="", line=-1))
        return self.__tokens

    def match(self, callback_function):
        """
        Match a char
        Conditional advance()
        Only consume the char if it's what we are looking for
        """
        matched = False
        while not self.at_end() and callback_function(self.__source[self.__current]):
            self.__current = self.__current + 1
            matched = True

        return matched

    def match_once(self, ch):
        """
        Match a char
        Conditional advance()
        Only consume the char if it's what we are looking for
        """
        matched = False
        if not self.at_end() and ch == self.__source[self.__current]:
            self.__current = self.__current + 1
            matched = True

        return matched

    def advance(self):
        """ consume and return the next char in the source file """
        current_char = self.__source[self.__current]
        self.__current = self.__current + 1
        return current_char

    def token_text(self) -> str:
        return self.__source[self.__start: self.__current]

    def peek(self):
        """
            peek at next char
            look ahead without consuming
            for multi char tokens eg castle indicators we need to look ahead at the next token as well
        """
        if self.at_end():
            return '\0'

        return self.__source[self.__current]

    def add_token(self, a_token):
        text = self.__source[self.__start: self.__current]
        self.__tokens.append(Token(a_token, text, self.__line))

    def increment_line(self):
        self.__line = self.__line + 1

    def line(self):
        return self.__line
