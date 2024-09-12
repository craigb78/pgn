from abc import abstractmethod, ABC
from pgn.token_type import TokenType
from pgn.pgn_token import Token

class Expr(ABC):
    def accept(self, visitor):
        visitor.visit_expr(self)

class TagPair(Expr):
    def __init__(self, tag_name: Token, tag_value: Token):
        self._tag_name = tag_name
        self._tag_value = tag_value

    def accept(self, visitor):
        visitor.visit_event_tag(self)

class PGNMove(Expr):
    def __init__(self, move: Token):
        self._move = move

class PGNGameResult(Expr):
    def __init__(self, result: Token):
        self._result = result

class TagPair(Expr):
    def __init(self, tag_name, tag_value):
        self._tag_name = tag_name
        self._tag_value = tag_value

class TagSection(Expr):
    def __init__(self):
        self._tag_pairs = []
    def append_tag_pair(self, event_tag: TagPair):
        self._tag_pairs.append(event_tag)

class MoveSection(Expr):
    def __init__(self):
        self._moves = []

    def append_move(self, move: PGNMove):
        self._moves.append(move)

class PGNGame(Expr):
    def __init__(self):
        self._tag_section = None
        self._move_section = None

    def set_tag_section(self, tag_section: TagSection):
        self._tag_section = tag_section

    def set_move_section(self, move_section: MoveSection):
        self._move_section = move_section

class ElementSequence(Expr):
    def __init__(self):
        self._result: PGNGameResult


class MoveSection(Expr):
    def __init__(self):
        self._result: PGNGameResult

    def set_element_sequence(self, seq: ElementSequence):
        self._element_sequence = seq

    def set_result(self, result: PGNGameResult):
        self._result = result


class PGNDatabase(Expr):
    def __init__(self):
        self._games = []

    def append(self, pgn_game: PGNGame):
        self._games.append(pgn_game)


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
        print(f"visiting event tag {event_tag}")
