import copy

from pgn.pgn_squares import *
from pgn.piece_type import *
from pgn.piece_colours import *
import pgn.pretty_print as pretty_print
from pgn.pgn_logging import logger
import pgn.bit_utils as bit_utils
from pgn.pgn_move import PGNPly


class PGNBoard:

    def __init__(self):
        """ starting positions for a standard game """
        self.__black_king = E8
        self.__black_queen = D8
        self.__black_bishop = C8 | F8
        self.__black_knight = B8 | G8
        self.__black_rook = A8 | H8
        self.__black_pawn = ROW_7

        self.__white_king = E1
        self.__white_queen = D1
        self.__white_bishop = C1 | F1
        self.__white_knight = B1 | G1
        self.__white_rook = A1 | H1
        self.__white_pawn = ROW_2

    def clear_board(self):
        self.__black_king = 0
        self.__black_queen = 0
        self.__black_bishop = 0
        self.__black_knight = 0
        self.__black_rook = 0
        self.__black_pawn = 0

        self.__white_king = 0
        self.__white_queen = 0
        self.__white_bishop = 0
        self.__white_knight = 0
        self.__white_rook = 0
        self.__white_pawn = 0

    def black_pieces(self):
        return (self.__black_pawn
                | self.__black_rook
                | self.__black_knight
                | self.__black_bishop
                | self.__black_queen
                | self.__black_king)

    def white_pieces(self):
        return (self.__white_pawn
                | self.__white_rook
                | self.__white_knight
                | self.__white_bishop
                | self.__white_queen
                | self.__white_king)

    def all_pieces(self):
        return self.black_pieces() | self.white_pieces()

    def occupied(self, origin_sq):
        return origin_sq & self.all_pieces()

    def get_piece(self, sq) -> (int, int):
        if bit_utils.is_mask_set(self.__white_pawn, sq):
            return (WHITE, PAWN)
        if bit_utils.is_mask_set(self.__white_rook, sq):
            return (WHITE, ROOK)
        if bit_utils.is_mask_set(self.__white_knight, sq):
            return (WHITE, KNIGHT)
        if bit_utils.is_mask_set(self.__white_bishop, sq):
            return (WHITE, BISHOP)
        if bit_utils.is_mask_set(self.__white_queen, sq):
            return (WHITE, QUEEN)
        if bit_utils.is_mask_set(self.__white_king, sq):
            return (WHITE, KING)
        if bit_utils.is_mask_set(self.__black_pawn, sq):
            return (BLACK, PAWN)
        if bit_utils.is_mask_set(self.__black_rook, sq):
            return (BLACK, ROOK)
        if bit_utils.is_mask_set(self.__black_knight, sq):
            return (BLACK, KNIGHT)
        if bit_utils.is_mask_set(self.__black_bishop, sq):
            return (BLACK, BISHOP)
        if bit_utils.is_mask_set(self.__black_queen, sq):
            return (BLACK, QUEEN)
        if bit_utils.is_mask_set(self.__black_king, sq):
            return (BLACK, KING)

        return (0,0) # there is nothing on the square

    def make_move(self, piece_type, colour, origin_sq, destination_sq):
        # when taking, clear any other piece on dest square
        dest_piece_colour, dest_piece_type = self.get_piece(destination_sq)
        if dest_piece_colour == colour:
            raise ValueError("expected piece of opposite colour")
        if (dest_piece_colour, dest_piece_type) != (0,0):
            # remove the piece that has been taken
            logger.debug(
                f"taking {piece_colour_to_str(dest_piece_colour)} {piece_type_to_str(dest_piece_type)} on {square_to_str(destination_sq)}")
            bitmap = self.__get_bitmap(piece_type=dest_piece_type,colour=dest_piece_colour)
            bitmap = bit_utils.clear_mask(bitmap, destination_sq)
            self.__set_bitmap(piece_type=dest_piece_type,colour=dest_piece_colour, bitmap=bitmap)

        if piece_type == PAWN and (dest_piece_colour, dest_piece_type) == (0,0):
            # check if this is an enpassant move, in which case, take the opposite colour's pawn.
            en_passant_square = self.is_en_passant(colour, origin_sq, destination_sq)
            if en_passant_square:
                # take the opponent's pawn
                logger.debug(
                    f"{piece_colour_to_str(colour)} taking enpassant {square_to_str(en_passant_square)}")
                bitmap = self.__get_bitmap(piece_type=PAWN, colour=opposite_colour(colour))
                bitmap = bit_utils.clear_mask(bitmap, en_passant_square)
                self.__set_bitmap(piece_type=PAWN, colour=opposite_colour(colour), bitmap=bitmap)

        # move the piece from the origin sq to the new dest dsq
        bitmap = self.__get_bitmap(piece_type=piece_type, colour=colour)
        bitmap = self.__replace(bitmap, origin_sq, destination_sq)
        self.__set_bitmap(piece_type=piece_type, colour=colour, bitmap=bitmap)

    def __get_bitmap(self, piece_type, colour) -> int:
        b = 0
        if bit_utils.is_mask_set(colour, WHITE):
            if bit_utils.is_mask_set(piece_type, PAWN):
                b = bit_utils.set_mask(b, self.__white_pawn)
            if bit_utils.is_mask_set(piece_type, ROOK):
                b = bit_utils.set_mask(b, self.__white_rook)
            if bit_utils.is_mask_set(piece_type, KNIGHT):
                b = bit_utils.set_mask(b, self.__white_knight)
            if bit_utils.is_mask_set(piece_type, BISHOP):
                b = bit_utils.set_mask(b, self.__white_bishop)
            if bit_utils.is_mask_set(piece_type, QUEEN):
                b = bit_utils.set_mask(b, self.__white_queen)
            if bit_utils.is_mask_set(piece_type, KING):
                b = bit_utils.set_mask(b, self.__white_king)

        if bit_utils.is_mask_set(colour, BLACK):
            if bit_utils.is_mask_set(piece_type, PAWN):
                b = bit_utils.set_mask(b, self.__black_pawn)
            if bit_utils.is_mask_set(piece_type, ROOK):
                b = bit_utils.set_mask(b, self.__black_rook)
            if bit_utils.is_mask_set(piece_type, KNIGHT):
                b = bit_utils.set_mask(b, self.__black_knight)
            if bit_utils.is_mask_set(piece_type, BISHOP):
                b = bit_utils.set_mask(b, self.__black_bishop)
            if bit_utils.is_mask_set(piece_type, QUEEN):
                b = bit_utils.set_mask(b, self.__black_queen)
            if bit_utils.is_mask_set(piece_type, KING):
                b = bit_utils.set_mask(b, self.__black_king)

        return b

    def __set_bitmap(self, piece_type, colour, bitmap: int) -> None:
        if colour == WHITE:
            if piece_type == PAWN:
                self.__white_pawn = bitmap
            elif piece_type == ROOK:
                self.__white_rook = bitmap
            elif piece_type == KNIGHT:
                self.__white_knight = bitmap
            elif piece_type == BISHOP:
                self.__white_bishop = bitmap
            elif piece_type == QUEEN:
                self.__white_queen = bitmap
            elif piece_type == KING:
                self.__white_king = bitmap
            else:
                raise ValueError(f"unknown white piece_type: {piece_type}")
        elif colour == BLACK:
            if piece_type == PAWN:
                self.__black_pawn = bitmap
            elif piece_type == ROOK:
                self.__black_rook = bitmap
            elif piece_type == KNIGHT:
                self.__black_knight = bitmap
            elif piece_type == BISHOP:
                self.__black_bishop = bitmap
            elif piece_type == QUEEN:
                self.__black_queen = bitmap
            elif piece_type == KING:
                self.__black_king = bitmap
            else:
                raise ValueError(f"unknown black piece_type: {piece_type}")
        else:
            raise ValueError(f"unknown colour: {colour}")

    def __replace(self, bitmap, origin_sq, dest_sq):
        """ move the piece from the origin sq to the dest sq"""

        if not bit_utils.is_mask_set(bitmap, origin_sq):
            raise ValueError("piece is not on origin sq")

        bitmap = bit_utils.clear_mask(bitmap, origin_sq)
        bitmap = bit_utils.set_mask(bitmap, dest_sq)

        return bitmap

    def __str__(self):
        VBAR = "\u254D"
        HBAR = "\u2015"  # horizontal bar
        board_str = '\t\u2015\t' * 8 + '\n'
        file_str = ""
        file_num = 8
        sq = A8
        while sq > 0:
            (colour, piece_type) = self.get_piece(sq)
            file_str += '|\t' + pretty_print.get_icon(colour, piece_type) + '\t'
            sq = (sq >> 1)
            if len(file_str) == 32:
                board_str += str(file_num) + file_str + '|\n'
                board_str += '\t\u2015\t' * 8 + '\n'
                file_str = ""
                file_num = file_num - 1

        board_str += " |\tA\t|\tB\t|\tC\t|\tD\t|\tE\t|\tF\t|\tG\t|\tH\t|\n"
        return board_str.rstrip()  # rstrip to remove trailing \n

    def do_castle(self, castle_kings_side=False, castle_queens_side=False, colour=WHITE):
        rook_origin_sq = 0
        rook_dest_sq = 0

        king_origin_sq = 0
        king_dest_sq = 0

        if colour == WHITE:
            king_origin_sq = E1
            if castle_kings_side:
                king_dest_sq = G1
                rook_origin_sq = H1
                rook_dest_sq = F1
            elif castle_queens_side:
                king_dest_sq = C1
                rook_origin_sq = A1
                rook_dest_sq = D1
        elif colour == BLACK:
            king_origin_sq = E8
            if castle_kings_side:
                king_dest_sq = G8
                rook_origin_sq = H8
                rook_dest_sq = F8
            elif castle_queens_side:
                king_dest_sq = C8
                rook_origin_sq = A8
                rook_dest_sq = D8
        else:
            raise ValueError("castling expected")

        # could do some validation here eg (does the king exist on the expected sq? does the rook exist on the expected sq?)
        # but we can assume the PGN file is correct

        # swap the king and the rook
        self.make_move(KING, colour, king_origin_sq, king_dest_sq)
        self.make_move(ROOK, colour, rook_origin_sq, rook_dest_sq)

    def generate_knight_moves(self, origin_square):
        """
        generate moves that can be made with a knight
        The constants are determined by the relative bitmasks of the squares
        """
        possible_dest_squares: int = 0

        #   up to right
        possible_dest_squares |= up_two(right(origin_square & ~COL_H))
        # up to left
        possible_dest_squares |= up_two(left(origin_square & ~COL_A))
        # down to right
        possible_dest_squares |= down_two(right(origin_square & ~COL_H))
        # down to left
        possible_dest_squares |= down_two(left(origin_square & ~COL_A))
        # left and up
        possible_dest_squares |= left_two(up_one(origin_square & ~COL_A & ~COL_B))
        # left and down
        possible_dest_squares |= left_two(down_one(origin_square & ~COL_A & ~COL_B))
        # right and up
        possible_dest_squares |= right_two(up_one(origin_square & ~COL_G & ~COL_H))
        # right and down
        possible_dest_squares |= right_two(down_one(origin_square & ~COL_G & ~COL_H))

        logger.debug(
            f"generate_knight_moves col for {square_to_str(origin_square)} are {square_to_str(possible_dest_squares)}")

        return possible_dest_squares

    def is_clear_run(self, piece_type: int, origin_sq: int, dest_sq: int, possible_dest_sqs: int) -> bool:
        if piece_type not in (BISHOP, ROOK, QUEEN):
            # Knights jump over pieces in the way
            # kings only move 1 place, so there is nothing between their origin and dest
            # pawns are treated differently as they can move 2 squares forward but this does not result in capture (=> dest end point cannot be excluded)
            raise ValueError()

        # the sqs from origin to dest excluding the end points (since we capture what is on the end point)
        path_mask = bit_utils.create_mask_exclusive(origin_sq, dest_sq)
        clear_run = (path_mask & possible_dest_sqs & self.all_pieces()) == 0
        #logger.info(
        #  f"is_clear_run({square_to_str(origin_sq)} to {square_to_str(dest_sq)})/possible_dest_sqs={square_to_str(possible_dest_sqs)},clear_run={clear_run}")
        return clear_run

    def generate_rook_moves(self, origin_sq, dest_sq):
        # the rook can move along the row it's on and the along the column it's on
        row = find_row(origin_sq)
        col = find_col(origin_sq)

        # logger.debug(f"generate_rook_moves col for {square_to_str(origin_sq)} are {square_to_str(col)}")
        # logger.debug(f"generate_rook_moves row for {square_to_str(origin_sq)} are {square_to_str(row)}")

        moves = 0
        if self.is_clear_run(ROOK, origin_sq, dest_sq, row):
            # restrict diagonals to start and end points
            moves |= bit_utils.create_mask_inclusive(origin_sq, dest_sq) & row

        if self.is_clear_run(ROOK, origin_sq, dest_sq, col):
            # restrict diagonals to start and end points
            moves |= bit_utils.create_mask_inclusive(origin_sq, dest_sq) & col

        # logger.debug(f"generate_rook_moves for {square_to_str(origin_sq)} to {square_to_str(dest_sq)} are {square_to_str(moves)}")

        return moves

    def generate_bishop_moves(self, origin_sq, dest_sq):
        diagonals = 0
        for next_diagonal in find_diagonal(origin_sq):
            if self.is_clear_run(BISHOP, origin_sq, dest_sq, next_diagonal):
                # restrict the diagonal to the start and end points
                diagonals |= bit_utils.create_mask_inclusive(origin_sq, dest_sq) & next_diagonal
            #  logger.debug(
            #    f"generate_bishop_moves diagonals for {square_to_str(origin_sq)} are {square_to_str(diagonals)}")
        return diagonals

    def generate_king_moves(self, origin_square) -> int:
        possible_dest_squares: int = 0

        #   UP
        possible_dest_squares |= up_one(origin_square & ~ROW_8)
        # DIAGONAL UP LEFT
        possible_dest_squares |= up_left(origin_square & ~ROW_8)
        # DIAGONAL UP RIGHT
        possible_dest_squares |= up_right(origin_square & ~ROW_8)
        # DOWN
        possible_dest_squares |= down_one(origin_square & ~ROW_1)
        # DIAGONAL DOWN LEFT
        possible_dest_squares |= down_left(origin_square & ~ROW_1)
        # DIAGONAL DOWN RIGHT
        possible_dest_squares |= down_right(origin_square & ~ROW_1)
        # LEFT
        possible_dest_squares |= left(origin_square & ~COL_A)
        # RIGHT
        possible_dest_squares |= right(origin_square & ~COL_H)

        return possible_dest_squares

    def generate_queen_moves(self, origin_sq, dest_sq):
        return self.generate_bishop_moves(origin_sq, dest_sq) | self.generate_rook_moves(origin_sq, dest_sq)

    def generate_pawn_moves(self, colour, origin_square, capture) -> int:
        possible_dest_squares: int = 0

        logger.debug(f"generate_pawn_moves()/origin_sq: {square_to_str(origin_square)}, up_one: {square_to_str(up_one(origin_square))}")

        if colour == WHITE:
            # UP one place. This places must be unoccupied
            if not row_8(origin_square) and not self.occupied(up_one(origin_square)):
                possible_dest_squares |= up_one(origin_square)
                # UP two places
                # if attempting to move 2 squares on first move, both of the squares must be unoccupied
                if row_2(origin_square) and not self.occupied(up_two(origin_square)):
                    # restrict diagonals to start and end points
                    possible_dest_squares |= up_two(origin_square)

            # white en passant
            if row_5(origin_square):
                # UP TO LEFT IS VACANT, PIECE TO LEFT IS BLACK PAWN
                if (not self.occupied(up_left(origin_square))
                        and self.get_piece(left(origin_square)) == (BLACK, PAWN)):
                    possible_dest_squares |= up_left(origin_square)
                # UP TO RIGHT IS VACANT, PIECE TO RIGHT IS BLACK PAWN
                if (not self.occupied(up_right(origin_square))
                        and self.get_piece(right(origin_square)) == (BLACK, PAWN)):
                    possible_dest_squares |= up_right(origin_square)

            if capture or possible_dest_squares == 0:  # some pgn games don't indicate pawn captures with the x
                # DIAGONAL UP LEFT (if is occupied)
                if self.occupied(up_left(origin_square)):
                    possible_dest_squares |= up_left(origin_square)
                # DIAGONAL UP RIGHT (if is occupied)
                if self.occupied(up_right(origin_square)):
                    possible_dest_squares |= up_right(origin_square)
        elif colour == BLACK:
            # DOWN one place
            if not row_1(origin_square) and not self.occupied(down_one(origin_square)):
                possible_dest_squares |= down_one(origin_square)
                # DOWN TWO PLACES
                if row_7(origin_square) and not self.occupied(down_two(origin_square)):
                    possible_dest_squares |= down_two(origin_square)
            # black is taking en passant
            if row_4(origin_square):
                # DOWN TO RIGHT IS VACANT, PIECE TO RIGHT IS WHITE PAWN
                if (not self.occupied(down_right(origin_square))
                        and self.get_piece(right(origin_square)) == (WHITE, PAWN)):
                    possible_dest_squares |= down_right(origin_square)
                # DOWN TO LEFT IS VACANT, PIECE TO LEFT IS WHITE PAWN
                if (not self.occupied(down_left(origin_square))
                        and self.get_piece(left(origin_square)) == (WHITE, PAWN)):
                    possible_dest_squares |= down_left(origin_square)

            if capture or possible_dest_squares == 0:  # some pgn games don't indicate pawn captures with the x
                # DIAGONAL DOWN LEFT (if is occupied)
                if self.occupied(down_left(origin_square)):
                    possible_dest_squares |= down_left(origin_square)
                # DIAGONAL DOWN RIGHT (if is occupied)
                if self.occupied(down_right(origin_square)):
                    possible_dest_squares |= down_right(origin_square)
        else:
            raise ValueError(f"unknown colour: {colour}")

        logger.debug(
            f"generate_pawn_moves()/origin_sq: {square_to_str(origin_square)} possible dest squares: {square_to_str(possible_dest_squares)}")
        return possible_dest_squares

    def is_en_passant(self, colour, origin_square, dest_square) -> (int, int):
        """
        If this is an enpassant move, return the colour and square of the piece that has been taken (not the dest sq)
        """
        # white is taking en passant
        if colour == WHITE and row_5(origin_square):
            # UP TO LEFT IS VACANT, PIECE TO LEFT IS BLACK PAWN
            if (dest_square == up_left(origin_square)
                    and not self.occupied(up_left(origin_square))
                    and self.get_piece(left(origin_square)) == (BLACK, PAWN)):
                return left(origin_square)
            # UP TO RIGHT IS VACANT, PIECE TO RIGHT IS BLACK PAWN
            if (dest_square == up_right(origin_square)
                    and not self.occupied(up_right(origin_square))
                    and self.get_piece(right(origin_square)) == (BLACK, PAWN)):
                return right(origin_square)

        if colour == BLACK and row_4(origin_square):
            # DOWN TO RIGHT IS VACANT, PIECE TO RIGHT IS WHITE PAWN
            if (dest_square == down_right(origin_square)
                    and not self.occupied(down_right(origin_square))
                    and self.get_piece(right(origin_square)) == (WHITE, PAWN)):
                return (origin_square)
            # DOWN TO LEFT IS VACANT, PIECE TO LEFT IS WHITE PAWN
            if (dest_square == down_left(origin_square)
                    and not self.occupied(down_left(origin_square))
                    and self.get_piece(left(origin_square)) == (WHITE, PAWN)):
                return left(origin_square)

        return 0 # we are not taking en passsant

    def generate_moves(self, piece_type, colour, origin_sq, dest_sq, capture: bool = False) -> int:
        """
        Given an origin square, list the dest sqs that the piece can move to.
        e.g., for a bishop this is all the squares the lie on the same diagonals as the bishop
        For a knight, this is all the squares the knight can move to.
        """
        moves = 0
        if bit_utils.is_mask_set(piece_type, KNIGHT):
            moves |= self.generate_knight_moves(origin_sq)
        if bit_utils.is_mask_set(piece_type, ROOK):
            moves |= self.generate_rook_moves(origin_sq, dest_sq)
        if bit_utils.is_mask_set(piece_type, BISHOP):
            moves |= self.generate_bishop_moves(origin_sq, dest_sq)
        if bit_utils.is_mask_set(piece_type, QUEEN):
            moves |= self.generate_queen_moves(origin_sq, dest_sq)
        if bit_utils.is_mask_set(piece_type, KING):
            moves |= self.generate_king_moves(origin_sq)
        if bit_utils.is_mask_set(piece_type, PAWN):
            moves |= self.generate_pawn_moves(colour, origin_sq, capture)

        return moves

    def determine_origin_sq(self, piece_type,
                            colour,
                            dest_square,
                            origin_square=0,
                            origin_row=0,
                            origin_col=0,
                            capture=False) -> [int]:
        """
            given a dest square (bitmask E5 etc)
            determine the starting square (bitmask A1 etc)
        """
        moveable_pieces_of_type_and_colour = self.moveable_to_dest_sq(piece_type, colour, dest_square, capture)
        if moveable_pieces_of_type_and_colour == 0:
            # the pgn file indicates a move that we cannot make,
            # so there is either a code error or an error in pgn
            raise ValueError("did not find any pieces to move to " + square_to_str(dest_square))
        else:
            # if we have any indication of the origin square then
            # use it to narrow down the possible origin sq of the move
            if origin_square != 0:
                # if we have an origin square to disambiguate...
                moveable_pieces_of_type_and_colour &= origin_square
            if origin_row != 0:
                # if we have an origin rank to disambiguate...
                moveable_pieces_of_type_and_colour &= origin_row
            if origin_col != 0:
                # if we have an origin file to disambiguate...
                moveable_pieces_of_type_and_colour &= origin_col

            if bit_utils.number_of_bits_set(moveable_pieces_of_type_and_colour, highest_bit=A8) > 1:
                # discount any move if it puts this colours king in check
                # (or if still in check after the move)
                logger.debug(f"about to try_move() for piece_type {piece_type_to_str(piece_type)}"
                             f",colour={piece_colour_to_str(colour)}"
                             f",moveable_pieces_of_type_and_colour={square_to_str(moveable_pieces_of_type_and_colour)}"
                             f",dest_square={square_to_str(dest_square)}")
                moveable_pieces_of_type_and_colour = PGNBoard.try_move(self, piece_type, colour,
                                                                       moveable_pieces_of_type_and_colour, dest_square)

            if bit_utils.number_of_bits_set(moveable_pieces_of_type_and_colour, highest_bit=A8) != 1:
                raise ValueError(f"expected one piece that can move to "
                                 f"destination square {square_to_str(dest_square)} "
                                 f"but got the following possible origins "
                                 f"{square_to_str(moveable_pieces_of_type_and_colour)}")
            else:
                # we've found a single piece of the correct type and colour that can move to the destination square.
                # We assume the PGN files are valid, and that the move is legal
                # This sq is therefore the starting square for the move
                logger.info("%s %s MOVING from %s to %s",
                            piece_type_to_str(piece_type),
                            piece_colour_to_str(colour),
                            square_to_str(moveable_pieces_of_type_and_colour),
                            square_to_str(dest_square))
                return moveable_pieces_of_type_and_colour

    def moveable_to_dest_sq(self, piece_type, colour, dest_square, capture: bool):
        """ 
        get all pieces of the type and colour that can move to the dest square
        """
        def test(origin_sq) -> int:
            # get all squares the piece can move to
            logger.debug(f"moveable_to_dest_sq()/test({square_to_str(origin_sq)})")
            origin_sq_colour, origin_sq_piece_type = self.get_piece(origin_sq)
            possible_dest_sqs = self.generate_moves(origin_sq_piece_type,
                                                    origin_sq_colour,
                                                    origin_sq,
                                                    dest_square,
                                                    capture)
            logger.debug(f"moveable_to_dest_sq()/"
                         f"piece_type={piece_type_to_str(origin_sq_piece_type)},"
                         f"colour={piece_colour_to_str(origin_sq_colour)},"
                         f"origin={square_to_str(origin_sq)},"
                         f"dest_sq={square_to_str(dest_square)},"
                         f"possible_dest_sqs={square_to_str(possible_dest_sqs)}")

            # if one of the squares is the dest square,
            # and (if applicable to piece type) the squares between origin_sq and dest_sq are empty
            # then we've found the piece we are looking for
            if bit_utils.is_mask_set(possible_dest_sqs, dest_square):
                return origin_sq
            return 0

        # 1. do we have a piece of the given colour and type?
        all_pieces_of_type_and_colour = self.__get_bitmap(piece_type=piece_type, colour=colour)
        # 2. list all the pieces of this colour and type that can move to the destination square
        moveable_pieces_of_type_and_colour: int = bit_utils.for_each_bit_set(all_pieces_of_type_and_colour,
                                                                             highest_bit=A8, func=test)
        logger.info("%s %s can move from %s to %s all_pieces: %s",
                    piece_type_to_str(piece_type),
                    piece_colour_to_str(colour),
                    square_to_str(moveable_pieces_of_type_and_colour),
                    square_to_str(dest_square),
                    square_to_str(all_pieces_of_type_and_colour)
                    )
        return moveable_pieces_of_type_and_colour

    def play(self, ply: PGNPly) -> None:
        logger.info(f"---------board playing ply: {ply}--------------")

        # castling is a special case
        if ply.castle_kings_side or ply.castle_queens_side:
            self.do_castle(ply.castle_kings_side, ply.castle_queens_side, ply.colour)
        else:
            # get the origin square
            origin_sq = self.determine_origin_sq(ply.piece_type,
                                                 ply.colour,
                                                 ply.dest_sq,
                                                 ply.origin_sq,
                                                 ply.origin_row,
                                                 ply.origin_col,
                                                 ply.capture)

            # update the move object with the origin
            ply.origin_sq = origin_sq

            # then make the move
            self.make_move(ply.piece_type,
                           ply.colour,
                           origin_sq,
                           ply.dest_sq)

    def is_in_check(self, colour) -> bool:
        """
        can pieces of the opposite colour "move_to" i.e., check the king?
        :param colour:
        :return:
        """
        if colour == BLACK:
            king = self.__black_king
            checking_piece = self.moveable_to_dest_sq(piece_type=ALL_PIECES_TYPES, colour=WHITE, dest_square=king,
                                                      capture=True)
        else:
            king = self.__white_king
            checking_piece = self.moveable_to_dest_sq(piece_type=ALL_PIECES_TYPES,
                                                      colour=BLACK,
                                                      dest_square=king,
                                                      capture=True)

        logger.debug(
            f"is_in_check()/{piece_colour_to_str(colour)},king sq={square_to_str(king)}, checking_piece: {square_to_str(checking_piece)}")
        return checking_piece != 0

    @staticmethod
    def try_move(board, piece_type: int, colour: int, moves_to_try: int, dest_sq: int) -> int:
        """
        Try each of the supplied moves on the board, and return all that are legal
        :param moves_to_try:
        :return:
        """

        def in_check(next_move_to_try: int) -> int:
            # make the move, then determine if colour is in check
            copied_board = copy.copy(board)
            copied_board.make_move(piece_type, colour, next_move_to_try, dest_sq)
            if not copied_board.is_in_check(colour):
                logger.info(
                    f"try_move()/next_move_to_try {piece_type_to_str(piece_type)} {piece_colour_to_str(colour)} {square_to_str(next_move_to_try)} to {square_to_str(dest_sq)}")
                return next_move_to_try  # then this is a valid move since making it does not put our king in check
            return 0

        moveable = bit_utils.for_each_bit_set(bitmap=moves_to_try, highest_bit=A8, func=in_check)
        return moveable
