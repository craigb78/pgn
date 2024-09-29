import re
from pgn.scanner import Scanner
from pgn.error_log import ErrorLog
import pgn.token_type as token_type


class PGNScanner:
    def __init__(self, source: str):
        self.__scanner = Scanner(source)
        self.__errors = ErrorLog()

    def scan_tokens(self):
        self.__scanner.scan_tokens(self.scan_token)

    def scan_token(self):
        ch = self.__scanner.advance()
        match ch:
            case "[":
                self.__scanner.add_token(token_type.LEFT_BRACKET)
            case "]":
                self.__scanner.add_token(token_type.RIGHT_BRACKET)
            case "{":
                self.__scanner.add_token(token_type.LEFT_BRACE_COMMENT)
            case "}":
                self.__scanner.add_token(token_type.RIGHT_BRACE_COMMENT)
            case '\n':
                self.__scanner.increment_line()
            case _ if self.__is_integer(ch):  # INTEGER
                self.__integer()
            case '.':  # PERIOD
                self.__scanner.add_token(token_type.PERIOD)
            case _ if self.__is_symbol(ch):  # SYMBOL
                self.__symbol()
            case _ if self.__is_string_prefix(ch):  # STRING
                self.__string()
            case _ if self.__is_whitespace(ch):  # SPACES
                pass
            case _:
                self.__errors.add_error(self.__scanner.line(), f"unexpected char: {ch}")

    def __is_integer(self, ch):
        # a digit should be followed by another digit, a period or whitespace
        return ch.isdigit() and (self.__scanner.peek().isdigit() or self.__scanner.peek() in [' ', '\n', '\t', '.'])

    def __integer(self):
        self.__scanner.match(lambda c: c.isdigit())
        self.__scanner.add_token(token_type.INTEGER)

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

    def __is_symbol(self, ch) -> bool:
        m = re.match(r'[a-zA-Z0-9_+#=:/-]', ch)
        return m is not None

    def __is_string_prefix(self, ch):
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

        self.__scanner.match(lambda c: c == '"')
        self.__scanner.match(lambda c: c.isalpha() or
                                       c.isdigit() or
                                       c in [".", "\\", "/", ' ', ',', '-', '?', '&', '(', ')', "'", '`', ':', '+'])
        self.__scanner.match(lambda c: c == '"')
        self.__scanner.add_token(token_type.STRING)

    @staticmethod
    def __is_whitespace(ch) -> bool:
        match = re.match("[ \r\t]", ch)
        return match is not None

    def print_tokens(self):
        self.__scanner.print_tokens()

    def tokens(self):
        return self.__scanner.tokens()

    def has_errors(self):
        return self.__errors.has_errors()

    def print_errors(self):
        self.__errors.print_errors()

