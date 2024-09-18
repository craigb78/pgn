"""

http://www.saremba.de/chessgml/standards/pgn/pgn-complete.htm#:~:text=PGN%20is%20%22Portable%20Game%20Notation,and%20generation%20by%20computer%20programs.

"""
import re

from pgn.pgn_token import Token
from pgn.token_type import TokenType
from pgn.token_type import get_keyword


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

        self._tokens.append(Token(TokenType.EOF, lexeme="", literal=None, line=-1))
        return self._tokens

    def __scan_token(self):
        ch = self.__advance()
        match ch:
            case "[":
                self.__add_token(TokenType.LEFT_BRACKET)
            case "]":
                self.__add_token(TokenType.RIGHT_BRACKET)

            case "{":
                self.__add_token(TokenType.LEFT_BRACE_COMMENT)
            case "}":
                self.__add_token(TokenType.RIGHT_BRACE_COMMENT)

            case '\n':
                self._line = self._line + 1
            case _ if self.__is_integer(ch):  # INTEGER
                self.__integer()
            case '.': # PERIOD
                self.__add_token(TokenType.PERIOD)
            case _ if self.__is_symbol(ch): # SYMBOL
               self.__symbol()
            case _ if self.__is_string_prefix(ch): # STRING
                self.__string()
            case _ if self.__is_whitespace(ch):  # SPACES
                pass
            case _:
                self._errors += (self._line, f"unexpected char: {ch}")

    def __match(self, callback_function):
        """
        Conditional advance()
        Only consume the char if it's what we are looking for
        """
        matched = False
        while not self.__at_end() and callback_function(self._source[self._current]):
            self._current = self._current + 1
            matched = True

      #  if matched:
         #   print(f"matched: {self._source[self._start : self._current]}")
        return matched

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


    def __is_integer(self, ch):
        # a digit should be followed by another digit, a period or whitespace
        return ch.isdigit() and (self.__peek().isdigit() or self.__peek() in [' ', '\n', '\t'] or self.__peek() == '.')

    def __integer(self):
        self.__match(lambda c : c.isdigit())
        self.__add_token(TokenType.INTEGER, int(self._source[self._start : self._current]))

    def __symbol(self):
        """ create a symbol token """
        # [a-zA-Z0-9_+#=:-]*
        self.__match(lambda c: Scanner.__is_symbol(c))

        # add the keyword type if we have one
        text = self._source[self._start : self._current]
        keyword_token_type = get_keyword(text)
        if keyword_token_type:
            self.__add_token(keyword_token_type)
        else:
            # otherwise, it's a symbol
            self.__add_token(TokenType.SYMBOL)

    @staticmethod
    def __is_symbol(ch):
        is_suffix = re.match(r'[a-zA-Z0-9_+#=:/-]+', ch)
        return is_suffix

    @staticmethod
    def __is_string_prefix(ch):
        return ch == r'"'

    def __string(self):
        """
/// A string token is a sequence of zero or more printing characters delimited by a
/// pair of quote characters (ASCII decimal value 34, hexadecimal value 0x22).  An
/// empty string is represented by two adjacent quotes.  (Note: an apostrophe is
/// not a quote.)  A quote inside a string is represented by the backslash
/// immediately followed by a quote.  A backslash inside a string is represented by
/// two adjacent backslashes.  Strings are commonly used as tag pair values (see
/// below).  Non-printing characters like newline and tab are not permitted inside
/// of strings.  A string token is terminated by its closing quote.  Currently, a
/// string is limited to a maximum of 255 characters of data.
        :return:
        """

        self.__match(lambda c : c.isalpha() or c.isdigit() or c in ['"', ".", "\\", "/", ' ', ',', '-'] )
        self.__match(lambda c : c == '"')
        self.__add_token(TokenType.STRING)

    @staticmethod
    def __is_whitespace(ch):
        return re.match("[ \r\t]", ch)
