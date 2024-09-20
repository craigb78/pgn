from pgn.expr import *
from parser import Parser
from error_log import ErrorLog
import token_type

class PGNParser:

    def __init__(self, tokens):
        self.__parser = Parser(tokens)
        self.__errors = ErrorLog()

    def parse(self) -> Expr:
        return self.pgn_database()

    def pgn_database(self) -> PGNDatabase:
        games: List[PGNGame] = []
        while not self.__parser.is_at_end():
            print(f"is parser at end of games: {self.__parser.peek()}")
            games.append(self.pgn_game())
            print(f"added game {len(games)}")
        pgn_database = PGNDatabase(games)
        return pgn_database

    def pgn_game(self) -> PGNGame:
        return PGNGame(self.tag_section(), self.move_text())

    def tag_section(self) -> TagSection:
        tag_section = TagSection()
        while self.__parser.match(token_type.LEFT_BRACKET):
            tag_section.append_tag_pair(self.tag_pair())
            if not self.__parser.match(token_type.RIGHT_BRACKET):
                self.__errors.add_error(f"expected a RIGHT_BRACKET but got {self.__parser.peek().tt}")

        return tag_section

    def tag_name(self) -> Token:
        if not self.__parser.match(token_type.SYMBOL):
            self.__errors.add_error(f"expected a SYMBOL but got {self.__parser.previous().tt}")
        return self.__parser.previous()

    def tag_value(self) -> Token:
        if not self.__parser.match(token_type.STRING):
            self.__errors.add_error(f"expected a STRING but got {self.__parser.previous().tt}")
        return self.__parser.previous()

    def tag_pair(self) -> TagPair:
        tag_pair = TagPair(self.tag_name(), self.tag_value())
        return tag_pair

    def result(self) -> PGNGameResult:
        if self.__parser.match(token_type.RESULT_GAME_UNFINISHED,
                                           token_type.RESULT_DRAW,
                                           token_type.RESULT_WHITE_WIN,
                                           token_type.RESULT_BLACK_WIN):
            return PGNGameResult(self.__parser.previous())
        return None

    def move_text(self) -> MoveText:
        elems: [Token] = []

        while True:
            next_move = self.move()
            if next_move:
                print(f"added elem {len(elems)} {next_move}")
                elems.append(next_move)

            else:
                break

        return MoveText(ElementSequence(elems), self.result())

    def brace_comment(self):
        comment: str = ""
        if self.__parser.match(token_type.LEFT_BRACE_COMMENT):
            while self.__parser.match(token_type.SYMBOL, token_type.PERIOD):
                comment = comment + " " + self.__parser.previous().lexeme
            self.__parser.match(token_type.RIGHT_BRACE_COMMENT)
        return comment

    def move(self) -> Element:
        if not self.__parser.match(token_type.INTEGER):
            self.__errors.add_error(f"move() expected type INTEGER but got: {self.__parser.peek()}")
            return None

        move_number = self.__parser.previous()

        elem = Element(move_number)

        self.__parser.match(token_type.PERIOD)  # optional, zero or more periods

        if self.__parser.match(token_type.SYMBOL):
            # if there is no comment between the moves then there will be a single symbol
            # containing move moves.
            # There is also a single symbol if the game ends with a single move.
            elem.add_move(self.__parser.previous())
            elem.add_comment(self.brace_comment())

        # if there is a comment, then the move number may be shown again followed by 3 periods
        self.__parser.match(token_type.INTEGER)
        while self.__parser.match(token_type.PERIOD):
            pass

        # second symbol (if it exists)
        if self.__parser.match(token_type.SYMBOL):
            elem.add_move(self.__parser.previous())
            elem.add_comment(self.brace_comment())

        return elem

    def has_errors(self):
        return self.__errors.has_errors()

    def print_errors(self):
        return self.__errors.print_errors()
