import re
import pgn.token_type as token_type

from pgn.scanner import Scanner
from pgn.error_log import ErrorLog

class SANScanner:
    def __init__(self, source: str):
        self.__scanner = Scanner(source)
        self.__errors = ErrorLog()

    def scan_tokens(self):
        return self.__scanner.scan_tokens(self.scan_token)

    def scan_token(self):
        ch = self.__scanner.advance()

        if self.is_en_passant(ch):
            self.__scanner.add_token(token_type.EN_PASSANT)

        elif self.is_piece_type(ch):
            self.__scanner.add_token(token_type.PIECE_TYPE)

        elif self.is_row(ch):
            self.__scanner.add_token(token_type.ROW)

        elif self.is_col(ch):
            self.__scanner.add_token(token_type.COL)

        elif self.is_capture(ch):
            self.__scanner.add_token(token_type.CAPTURE)

        elif self.__is_whitespace(ch):  # SPACES
            pass

        elif self.__is_symbol(ch):
            self.__symbol()

        else:
             self.__errors.add_error(line_number=self.__scanner.line(), error_msg=f"unexpected char: {ch}")

    def print_tokens(self):
        self.__scanner.print_tokens()

    def tokens(self):
        return self.__scanner.tokens()

    def has_errors(self):
        return self.__errors.has_errors()

    def print_errors(self):
        self.__errors.print_errors()

    def __symbol(self):
        """ create a symbol token """
        # [a-zA-Z0-9_+#=:-]*
        self.__scanner.match(lambda c: self.__is_symbol(c))

        # add the keyword type if we have one
        text = self.__scanner.token_text()
        keyword_token_type = token_type.get_san_keyword(text)
        if keyword_token_type:
            self.__scanner.add_token(keyword_token_type)
        else:
            # otherwise, it's a symbol
            self.__scanner.add_token(token_type.SYMBOL)

    def __is_symbol(self, ch) -> bool:
        m = re.match(r'[a-zA-Z0-9+#=()-]', ch)
        return m is not None

    def is_en_passant(self, ch):
        if ch == 'e' and self.__scanner.peek() == '.':
            res = self.__scanner.match_once('.') and self.__scanner.match_once('p') and self.__scanner.match_once('.')
            if not res:
                self.__errors.add_error(error_msg="Expected e.p.")
            return True
        return False

    def __is_whitespace(self, ch) -> bool:
        m = re.match("[ \r\t]", ch)
        return m is not None

    def is_capture(self, ch):
        return ch == 'x'

    def is_piece_type(self, ch):
        return ch in ('K', 'Q', 'B', 'N', 'R', 'P')

    def is_row(self, ch) -> bool:
        m = re.match('[1-8]', ch)
        return m is not None

    def is_col(self, ch) -> bool:
        m = re.match('[a-hA-H]', ch)
        return m is not None