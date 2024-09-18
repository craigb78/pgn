from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from typing import List

from pgn.pgn_token import Token


@dataclass
class Expr(ABC):
    def accept(self, visitor):
        visitor.visit_expr(self)


@dataclass
class TagPair(Expr):
    tag_name: Token
    tag_value: Token

    def accept(self, visitor):
        visitor.visit_event_tag(self)


@dataclass
class Element(Expr):  # a move
    move: Token


@dataclass
class PGNGameResult(Expr):
    result: Token


@dataclass
class TagPair(Expr):
    tag_name: Token
    tag_value: Token


@dataclass
class TagSection(Expr):
    tag_pairs: List[TagPair] = field(init=False, default_factory=list)

    def append_tag_pair(self, event_tag: TagPair):
        self.tag_pairs.append(event_tag)


@dataclass
class MoveNumber(Expr):
    move_number: int


@dataclass
class Element(Expr):
    move_number_indication: MoveNumber = field(init=True)
    san_moves: List[Token] = field(init=False, default_factory=list)
    comments: List[str] = field(init=False, default_factory=list)

    def add_move(self, san_move: Token):
        self.san_moves.append(san_move)

    def add_comment(self, comment: str):
        self.comments.append(comment)


@dataclass
class ElementSequence(Expr):
    elements: List[Element] = field(default_factory=list)


@dataclass
class MoveText(Expr):
    element_sequence: ElementSequence
    result: PGNGameResult


@dataclass
class PGNGame(Expr):
    tag_section: TagSection
    move_text: MoveText


@dataclass
class PGNDatabase(Expr):
    games: List[PGNGame] = field(default_factory=list)


class Visitor(ABC):
    @abstractmethod
    def visit_expr(self, expr):
        pass

    @abstractmethod
    def visit_event_tag(self, event_tag: TagPair):
        pass


class PrintASTVisitor(Visitor):

    def visit_expr(self, expr):
        print(f"visiting {expr}")

    def visit_event_tag(self, event_tag: TagPair):
        print(f"visiting event tag {event_tag.tag_name}")
