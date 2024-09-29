from dataclasses import dataclass
from pgn.token_type import tt_to_str

@dataclass
class Token:
    tt: int  # token_type
    lexeme: str
    line: int

    def __repr__(self):
        return f"Token(tt={tt_to_str(self.tt)}, lexeme: {self.lexeme}, line {self.line})"
