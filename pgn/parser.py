"""

Grammar notation	Code representation
Terminal	Code to match and consume a token
Non-terminal	Call to that rule’s function
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
import pgn.token_type as token_type

class Parser:

    def __init__(self, tokens):
        self.__tokens = tokens
        self.__current: int = 0

    def is_at_end(self) -> bool:
        return self.peek().tt == token_type.EOF

    def peek(self) -> Token:
        return self.__tokens[self.__current]

    def previous(self) -> Token:
        return self.__tokens[self.__current - 1]

    def check(self, tt) -> bool:
        if self.is_at_end():
            return False
        return self.peek().tt == tt

    def advance(self) -> Token:
        if not self.is_at_end():
            self.__current = self.__current + 1
        return self.previous()

    def match(self, *types) -> bool:
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False
