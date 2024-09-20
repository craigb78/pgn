import re
from token_type import (token_type, get_pgn_keyword)
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
            case 'x':
                self.__scanner.add_token(token_type.TAKES)
            case '_':
                pass

    def print_tokens(self):
        self.__scanner.print_tokens()

    def tokens(self):
        return self.__scanner.tokens()

    def has_errors(self):
        return self.__errors.has_errors()

    def print_errors(self):
        self.__errors.print_errors()
