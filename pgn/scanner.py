"""

http://www.saremba.de/chessgml/standards/pgn/pgn-complete.htm#:~:text=PGN%20is%20%22Portable%20Game%20Notation,and%20generation%20by%20computer%20programs.

"""
from pgn.token_type import TokenType
from pgn.token_type import get_keyword
from pgn.pgn_token import Token

class Scanner:
    """ scanner for PGN files """
    def __init__(self, source):
        self._source: str = source
        self._tokens = []
        self._start: int = 0
        self._current: int = 0 # index of current char
        self._line: int = 1
        self._errors = []

    def tokens(self) -> []:
        return self._tokens

    def has_errors(self):
        return len(self._errors)

    def print_errors(self):
        for next_error in self._errors:
            print(next_error)

    def print_tokens(self):
        for next_token in self._tokens:
            print(next_token)

    def __at_end(self):
        """ have we consumed all the chars in self.source??"""
        return self._current >= len(self._source)

    def scan_tokens(self):
        """ populate the list of tokens """
        while not self.__at_end():
            self._start = self._current
            self.__scan_token()

        self._tokens.append(Token(TokenType.EOF, lexeme=None, literal=None, line=-1))
        return self._tokens

    def __scan_token(self):
        ch = self.__advance()
        match ch:
            case "[":
                self.__add_token(TokenType.LEFT_TAG)
            case "]":
                self.__add_token(TokenType.RIGHT_TAG)

            case "{":
                self.__add_token(TokenType.LEFT_BRACE_COMMENT)
            case "}":
                self.__add_token(TokenType.RIGHT_BRACE_COMMENT)

            case '\n':
                self._line = self._line + 1

            case ' ':
                pass # ignore whitespace
            case '\r':
                pass # ignore whitespace
            case '\t':
                pass # ignore whitespace
            #case ch if ch.isdigit():
                #self.__number()
            case _ if self.__is_identifier_char(ch): # handle unexpected chars in the input
               self.__identifier()
            case _:
                self._errors += (self._line, f"unexpected char: {ch}")

    def __match(self, expected):
        """
        Conditional advance()
        Only consume the char if it's what we are looking for
        """

        if not self.__at_end():
            return False

        if self._source[self._current] != expected:
            return False

        self._current = self._current + 1
        return True

    def __advance(self):
        """ consume and return the next char in the source file """
        current_char = self._source[self._current]
        self._current = self._current + 1
        return current_char

    def __peek(self):
        """
            look ahead without consuming
            for multi char tokens eg castle indicators we need to look ahead at the next token as well
        """
        if self.__at_end():
            return '\0'

        return self._source[self._current]

    def __add_token(self, token_type: TokenType, literal=None):
        text = self._source[self._start : self._current]
        self._tokens.append(Token(token_type, text, literal, self._line))

    def __number(self):
        while self.__peek().isdigit():
            self.__advance()

        self.__add_token(TokenType.NUMBER, int(self._source[self._start : self._current]))

        if self.__peek() == '.':  # Consume the "." on the move numbering
            self.__advance()


    def __identifier(self):
        """ create an identifier token """
        while self.__is_identifier_char(self.__peek()):
            self.__advance()

        # add the keyword type if we have one
        text = self._source[self._start : self._current]
        keyword_token_type = get_keyword(text)
        if keyword_token_type:
            self.__add_token(keyword_token_type)
        else:
            # TODO this might be an error if we only have keywords....
            self.__add_token(TokenType.IDENTIFIER)

    def __is_identifier_char(self, ch):
        """ what is the total set of characters that make up an identifier in PGN? """
        # alpha
        # numeric
        # - (for castling) or draw indicator
        return ch.isalnum() or ch in ['-', '/']


