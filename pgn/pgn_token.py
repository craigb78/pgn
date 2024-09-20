from dataclasses import dataclass


@dataclass
class Token:
    tt: int  # token_type
    lexeme: str
    line: int
