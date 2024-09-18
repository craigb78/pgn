"""

Grammar notation	Code representation
Terminal	Code to match and consume a token
Nonterminal	Call to that rule’s function
|	if or switch statement
* or +	while or for loop
?	if statement

pgn_database: pgn_game*;
pgn_game: tag_section movetext_section;
tag_section: tag_pair*;
tag_pair: LEFT_BRACKET tag_name tag_value RIGHT_BRACKET;
tag_name: SYMBOL;
tag_value: STRING;

movetext_section: element_sequence game_termination;

element_sequence: (element | recursive_variation)*;

element: move_number_indication| san_move;
move_number_indication: INTEGER PERIOD?;
san_move: SYMBOL;
recursive_variation: LEFT_PARENTHESIS element_sequence RIGHT_PARENTHESIS;

game_termination: WHITE_WINS| BLACK_WINS| DRAWN_GAME| ASTERISK;

WHITE_WINS: '1-0';
BLACK_WINS: '0-1';
DRAWN_GAME: '1/2-1/2';
"""

from pgn.expr import *
from pgn.token_type import TokenType


class Parser:
    def __init__(self, tokens):
        self._tokens = tokens
        self._current: int = 0
        self._errors = []

    def has_errors(self):
        return len(self._errors)

    def add_error(self, msg):
        self._errors.append(msg)
        print(msg)


    #    raise ParserError(msg)

    def print_errors(self):
        for next_error in self._errors:
            print(next_error)

    def pgn_database(self) -> PGNDatabase:
        games: List[PGNGame] = []
        while not self.is_at_end():
            games.append(self.pgn_game())
        pgn_database = PGNDatabase(games)
        return pgn_database

    def pgn_game(self) -> PGNGame:
        return PGNGame(self.tag_section(), self.move_text())

    def tag_section(self) -> TagSection:
        tag_section = TagSection()
        while self.match(TokenType.LEFT_BRACKET):
            tag_section.append_tag_pair(self.tag_pair())
            if not self.match(TokenType.RIGHT_BRACKET):
                self.add_error(f"expected a RIGHT_BRACKET but got {self.peek().token_type}")

        return tag_section

    def tag_name(self) -> Token:
        if not self.match(TokenType.SYMBOL):
            self.add_error(f"expected a SYMBOL but got {self.previous().token_type}")
        return self.previous()

    def tag_value(self) -> Token:
        if not self.match(TokenType.STRING):
            self.add_error(f"expected a STRING but got {self.previous().token_type}")
        return self.previous()

    def tag_pair(self) -> TagPair:
        tag_pair = TagPair(self.tag_name(), self.tag_value())
        return tag_pair

    def result(self) -> PGNGameResult:
        if self.previous().token_type in [ TokenType.RESULT_GAME_UNFINISHED,
                        TokenType.RESULT_DRAW,
                        TokenType.RESULT_WHITE_WIN,
                        TokenType.RESULT_BLACK_WIN]:
           return PGNGameResult(self.previous())
        return None

    def move_text(self) -> MoveText:
        elems = []
        while not self.match(  TokenType.RESULT_GAME_UNFINISHED,
                        TokenType.RESULT_DRAW,
                        TokenType.RESULT_WHITE_WIN,
                        TokenType.RESULT_BLACK_WIN):
            elems.append(self.move())

        return MoveText(ElementSequence(elems), self.result())


    def brace_comment(self):
        comment = ""
        if self.match(TokenType.LEFT_BRACE_COMMENT):
            while self.match(TokenType.SYMBOL, TokenType.PERIOD):
                comment = comment + " " + self.previous().lexeme
            self.match(TokenType.RIGHT_BRACE_COMMENT)
        return comment

    def move(self) -> Element:
        if not self.match(TokenType.INTEGER):
            self.add_error(f"move() expected type INTEGER but got: {self.peek()}")
        move_number = self.previous()

        elem = Element(move_number)

        self.match(TokenType.PERIOD) # optional, zero or more periods

        if self.match(TokenType.SYMBOL):
            # if there is no comment between the moves then there will be a single symbol
            # containing move moves.
            # There is also a single symbol if the game ends with a single move.
            elem.add_move(self.previous())
            elem.add_comment(self.brace_comment())

        # if there is a comment, then the move number may be shown again followed by 3 periods
        self.match(TokenType.INTEGER)
        while self.match(TokenType.PERIOD):
            pass

        # second symbol (if it exists)
        if self.match(TokenType.SYMBOL):
            elem.add_move(self.previous())
            elem.add_comment(self.brace_comment())

        return elem

    def parse(self) -> Expr:
        return self.pgn_database()

    def is_at_end(self) -> bool:
        return self.peek().token_type == TokenType.EOF

    def peek(self) -> Token:
        return self._tokens[self._current]

    def previous(self) -> Token:
        return self._tokens[self._current - 1]

    def check(self, token_type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().token_type == token_type

    def advance(self) -> Token:
        if not self.is_at_end():
            self._current = self._current + 1
        return self.previous()

    def match(self, *types) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
          #  else:
              #  self.add_error(f"not expected type {type} got: {self.peek()}")
        return False
