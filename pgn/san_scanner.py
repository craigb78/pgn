import re
import token_type
from scanner import Scanner
from error_log import ErrorLog


class SANScanner:
    def __init__(self, source: str):
        self.__scanner = Scanner(source)
        self.__errors = ErrorLog()

    def scan_tokens(self):
        self.__scanner.scan_tokens(self.scan_token)

    def scan_token(self):
        ch = self.__scanner.advance()
        match ch:
            case _ if self.is_en_passant(ch):
                self.__scanner.add_token(token_type.EN_PASSANT)
            case 'K':
                self.__scanner.add_token(token_type.KING)
            case 'Q':
                self.__scanner.add_token(token_type.QUEEN)
            case 'N':
                self.__scanner.add_token(token_type.KNIGHT)
            case 'B':
                self.__scanner.add_token(token_type.BISHOP)
            case 'R':
                self.__scanner.add_token(token_type.ROOK)
            case 'P':
                self.__scanner.add_token(token_type.PAWN)
            case 'a':
                self.__scanner.add_token(token_type.A)
            case 'b':
                self.__scanner.add_token(token_type.B)
            case 'c':
                self.__scanner.add_token(token_type.C)
            case 'd':
                self.__scanner.add_token(token_type.D)
            case 'e':
                self.__scanner.add_token(token_type.E)
            case 'f':
                self.__scanner.add_token(token_type.F)
            case 'g':
                self.__scanner.add_token(token_type.G)
            case 'h':
                self.__scanner.add_token(token_type.H)
            case '1':
                self.__scanner.add_token(token_type._1)
            case '2':
                self.__scanner.add_token(token_type._2)
            case '3':
                self.__scanner.add_token(token_type._3)
            case '4':
                self.__scanner.add_token(token_type._4)
            case '5':
                self.__scanner.add_token(token_type._5)
            case '6':
                self.__scanner.add_token(token_type._6)
            case '7':
                self.__scanner.add_token(token_type._7)
            case '8':
                self.__scanner.add_token(token_type._8)
            case 'x':
                self.__scanner.add_token(token_type.CAPTURE)
            case _ if self.__is_whitespace(ch):  # SPACES
                pass
            case _ if self.__is_symbol(ch):
                self.__symbol()
            case _:
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
        keyword_token_type = token_type.get_pgn_keyword(text)
        if keyword_token_type:
            self.__scanner.add_token(keyword_token_type)
        else:
            # otherwise, it's a symbol
            self.__scanner.add_token(token_type.SYMBOL)

    def __is_symbol(self, ch):
        return ch in r'[a-zA-Z0-9+#=()-]'

    def is_en_passant(self, ch):
        if ch == 'e' and self.__scanner.peek() == '.':
            res = self.__scanner.match_once('.') and self.__scanner.match_once('p') and self.__scanner.match_once('.')
            if not res:
                self.__errors.add_error(error_msg="Expected e.p.")
            return True
        return False

    def __is_whitespace(self, ch):
        return re.match("[ \r\t]", ch)
