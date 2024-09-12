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

from pgn.pgn_token import Token
from pgn.token_type import TokenType
from pgn.expr import *

class Parser:
    def __init__(self, tokens):
        self._tokens = tokens
        self._current: int = 0

    def pgn_database(self) -> PGNDatabase:
        pgn_database = PGNDatabase()
        while not self.is_at_end():
            pgn_database.append(self.pgn_game())
        return pgn_database

    def pgn_game(self) -> PGNGame:
        game = PGNGame()
        game.set_tag_section(self.tag_section())
        game.set_move_section(self.move_section())
        return game

    def tag_section(self) -> TagSection:
        tag_section = TagSection()
        while self.match(TokenType.TAG_PAIR):
            tag_section.append_tag_pair(self.tag_pair())
        return tag_section

    def tag_name(self) -> Token:
        return self.advance()

    def tag_value(self) -> Token:
        return self.advance()

    def tag_pair(self) -> TagPair:
        tag_pair = TagPair(self.tag_name(), self.tag_value())
        return tag_pair

    def result(self)-> PGNGameResult:
        return PGNGameResult(self.advance())

    def move_section(self) -> MoveSection:
        move_section = MoveSection()
        # TODO movetext needs added
        move_section.set_result(self.result())

    def move(self):
        return PGNMove(self.advance())

    def parse(self) -> Expr:
        return self.pgn_database()

    def is_at_end(self) -> bool:
        return self.peek().token_type == TokenType.EOF

    def peek(self) -> Token:
        try:
            return self._tokens[self._current]
        except IndexError as ie:
            raise ie

    def previous(self) -> Token:
        return self._tokens[self._current - 1]

    def check(self, type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().token_type == type

    def advance(self) -> Token:
        if not self.is_at_end():
            self._current = self._current + 1
        return self.previous()

    def match(self, *types) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False
