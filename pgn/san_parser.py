from pgn.piece_type import *
from typing import Optional
from pgn.pgn_logging import logger
from pgn.pgn_token import Token
from pgn.pgn_move import PGNMove
from pgn.token_type import *
from pgn.pgn_move import PGNPly
from pgn.piece_colours import *
from pgn.pgn_squares import *

class SANParser:

    def __init__(self):
        self.__moves: [PGNMove] = []

    def parse_san_move(self, white_san_tokens: [Token], black_san_tokens: [Token]):
        """
            parse the san tokens and return a list of move
        """
        white_ply: Optional[PGNPly] = None
        black_ply: Optional[PGNPly] = None

        if white_san_tokens:
            white_ply = self.parse_san_ply(white_san_tokens)
            white_ply.colour = WHITE
        if black_san_tokens:
            black_ply = self.parse_san_ply(black_san_tokens)
            black_ply.colour = BLACK

        self.__moves.append(PGNMove(white_ply, black_ply))

    def parse_san_ply(self, ply_tokens) -> PGNPly:
        """
        parse the tokens for a single ply
        :param ply_tokens:
        :return:
        """
        ply = PGNPly()
        rows_cols: [int] = []
        for t in ply_tokens:
            if t.tt == PIECE_TYPE:
                ply.piece_type = str_to_piece_type(t.lexeme)
            elif t.tt == ROW:
                rows_cols.append(str_to_row(t.lexeme))
            elif t.tt == COL:
                rows_cols.append(str_to_col(t.lexeme))
            elif t.tt == CAPTURE:
                ply.capture = True
            elif t.tt == CASTLE_QUEENS_SIDE:
                ply.castle_queens_side = True
            elif t.tt == CASTLE_KINGS_SIDE:
                ply.castle_kings_side = True
            elif t.tt == EOF:
                pass
            else:
                logger.debug(f"san_parser, unmatched token: {t}")

        # should be 2 entries
        # or 3 with diambiguating row or col
        # or 4 with disambiguating row and col
        if len(rows_cols) >= 2:
            # the intersection of the row and col is the dest sq
            ply.dest_sq = rows_cols[-2] & rows_cols[-1]

        if len(rows_cols) == 3:
            # is it an origin square or an origin row
            if find_row(rows_cols[-3]):
                ply.origin_row  = rows_cols[-3]
            if find_col(rows_cols[-3]):
                ply.origin_col = rows_cols[-3]

        if len(rows_cols) == 4:
            ply.origin_sq = rows_cols[-4] & rows_cols[-3]
            # since we have the origin square,
            # we shouldn't need the row and col
            # but are adding it here for completeness
            ply.origin_row = rows_cols[-3]
            ply.origin_col = rows_cols[-4]

        if not ply.piece_type:
            ply.piece_type = PAWN

        return ply

    def collect(self) -> [PGNMove]:
        """
        :return: the list of parsed moves
        """
        return self.__moves

