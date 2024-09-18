from dataclasses import dataclass

from pgn.token_type import TokenType


@dataclass
class Token:
    token_type: TokenType
    lexeme: str
    literal: str
    line: int
