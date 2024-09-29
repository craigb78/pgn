import logging

from pgn.pgn_squares import *
from pgn.piece_type import *
from pgn.piece_colours import *
import pgn.pretty_print as pretty_print
from pgn.pgn_logging import logger
import pgn.bit_utils as bit_utils
from pgn_move import PGNPly

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

    def get_piece(self, sq) -> (int, int,):
        if bit_utils.is_mask_set(self.__white_pawn, sq):
            return (WHITE, PAWN,)
        elif bit_utils.is_mask_set(self.__white_rook, sq):
            return (WHITE, ROOK, )
        elif bit_utils.is_mask_set(self.__white_knight, sq):
            return WHITE, KNIGHT,
        elif bit_utils.is_mask_set(self.__white_bishop, sq):
            return (WHITE, BISHOP,)
        elif bit_utils.is_mask_set(self.__white_queen, sq):
            return (WHITE, QUEEN,)
        elif bit_utils.is_mask_set(self.__white_king, sq):
            return (WHITE, KING,)
        elif bit_utils.is_mask_set(self.__black_pawn, sq):
            return (BLACK, PAWN,)
        elif bit_utils.is_mask_set(self.__black_rook, sq):
            return (BLACK, ROOK,)
        elif bit_utils.is_mask_set(self.__black_knight, sq):
            return (BLACK, KNIGHT, )
        elif bit_utils.is_mask_set(self.__black_bishop, sq):
            return (BLACK, BISHOP,)
        elif bit_utils.is_mask_set(self.__black_queen, sq):
            return (BLACK, QUEEN,)
        elif bit_utils.is_mask_set(self.__black_king, sq):
            return (BLACK, KING,)

        return (-1, -1)

    def make_move(self, piece_type, colour, origin_sq, destination_sq):
        actual_colour, actual_piece_type = self.get_piece(origin_sq)

        if actual_colour != colour:
            raise ValueError("piece on origin sq does not have expected colour")
        if actual_piece_type != piece_type:
            raise ValueError("piece on origin sq does not have expected piece type")
        
        bitmap = self.__get_bitmap(piece_type, colour)
        updated_bitmap = self.__replace(bitmap, origin_sq, destination_sq)
        self.__set_bitmap(piece_type, colour, updated_bitmap)
        
    def __get_bitmap(self, piece_type, colour):
        if colour == WHITE:
            if piece_type == PAWN:
                return self.__white_pawn
            elif piece_type == ROOK:
                return self.__white_rook
            elif piece_type == KNIGHT:
                return self.__white_knight
            elif piece_type == BISHOP:
                return self.__white_bishop
            elif piece_type == QUEEN:
                return self.__white_queen
            elif piece_type == KING:
                return self.__white_king
            else:
                raise ValueError(f"unknown white piece_type: {piece_type}")
        elif colour == BLACK:
            if piece_type == PAWN:
                return self.__black_pawn
            elif piece_type == ROOK:
                return self.__black_rook
            elif piece_type == KNIGHT:
                return self.__black_knight
            elif piece_type == BISHOP:
                return self.__black_bishop
            elif piece_type == QUEEN:
                return self.__black_queen
            elif piece_type == KING:
                return self.__black_king
            else:
                raise ValueError(f"unknown black piece_type: {piece_type}")
        else:
            raise ValueError(f"unknown colour: {colour}")

        return None

    def __set_bitmap(self, piece_type, colour, bitmask):
        if colour == WHITE:
            if piece_type == PAWN:
                self.__white_pawn = bitmask
            elif piece_type == ROOK:
                self.__white_rook = bitmask
            elif piece_type == KNIGHT:
                self.__white_knight = bitmask
            elif piece_type == BISHOP:
                self.__white_bishop = bitmask
            elif piece_type == QUEEN:
                self.__white_queen = bitmask
            elif piece_type == KING:
                self.__white_king = bitmask
            else:
                raise ValueError(f"unknown white piece_type: {piece_type}")
        elif colour == BLACK:
            if piece_type == PAWN:
                self.__black_pawn = bitmask
            elif piece_type == ROOK:
                self.__black_rook = bitmask
            elif piece_type == KNIGHT:
                self.__black_knight = bitmask
            elif piece_type == BISHOP:
                self.__black_bishop = bitmask
            elif piece_type == QUEEN:
                self.__black_queen = bitmask
            elif piece_type == KING:
                self.__black_king = bitmask
            else:
                raise ValueError(f"unknown black piece_type: {piece_type}")
        else:
            raise ValueError(f"unknown colour: {colour}")

    def __replace(self, bitmap, origin_sq, dest_sq):
        """ move the piece from the origin sq to the dest sq"""
        #bit_utils.print_bitmap("bitmap", bitmap)
        #bit_utils.print_bitmap("origin_sq", origin_sq)
        #bit_utils.print_bitmap("dest_sq", dest_sq)

        if not bit_utils.is_mask_set(bitmap, origin_sq):
            raise ValueError("piece is not on origin sq")

        bitmap = bit_utils.clear_mask(bitmap, origin_sq)
        #bit_utils.print_bitmap("bitmap after clearing", bitmap)

        bitmap = bit_utils.set_mask(bitmap, dest_sq)
        #bit_utils.print_bitmap("bitmap after set mask", bitmap)

        return bitmap

    def __str__(self):
        VBAR = "\u254D"
        HBAR = "\u2015"  # horizontal bar
        board_str  = '\t\u2015\t' * 8 + '\n'
        file_str = ""
        file_num = 8
        sq = A8
        while sq > 0:
            (colour, piece_type) = self.get_piece(sq)
            file_str += '|\t'+pretty_print.get_icon(colour, piece_type)+'\t'
            sq = (sq >> 1)
            if len(file_str) == 32:
                board_str += str(file_num) + file_str + '|\n'
                board_str += '\t\u2015\t' * 8 + '\n'
                file_str = ""
                file_num = file_num - 1

        board_str += " |\tA\t|\tB\t|\tC\t|\tD\t|\tE\t|\tF\t|\tG\t|\tH\t|\n"
        return board_str.rstrip() # rstrip to remove trailing \n

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
                king_dest_sq = D8
                rook_origin_sq = A8
                rook_dest_sq = C8
        else:
            raise ValueError("castling expected")

        # could do some validation here eg (does the king exist on the expected sq? does the rook exist on the expected sq?)
        # but we can assume the PGN file is correct

        # swap the king and the rook
        self.make_move(KING, colour, king_origin_sq, king_dest_sq)
        self.make_move(ROOK, colour, rook_origin_sq, rook_dest_sq)

    def inbounds(self, dest_sq): # make sure we are not going off the board
        if H1 <= dest_sq <= A8:
            return dest_sq
        else:
            return 0

    def generate_knight_moves(self, origin_square):
        """
        generate moves that can be made with a knight
        The constants are determined by the relative bitmasks of the squares
        """
        possible_dest_squares = 0

        #   up to right
        possible_dest_squares |= self.inbounds(origin_square << 15)
        # up to left
        possible_dest_squares |= self.inbounds(origin_square << 17)
        # down to right
        possible_dest_squares |= self.inbounds(origin_square >> 17)
        # down to left
        possible_dest_squares |= self.inbounds(origin_square >> 15)
        # left and up
        possible_dest_squares |= self.inbounds(origin_square << 10)
        # left and down
        possible_dest_squares |= self.inbounds(origin_square >> 6)
        # right and up
        possible_dest_squares |= self.inbounds(origin_square << 6)
        # right and down
        possible_dest_squares |= self.inbounds(origin_square >> 10)

        return possible_dest_squares

    def generate_rook_moves(self, origin_sq):
        row = find_row(origin_sq)
        col = find_col(origin_sq)

        logger.debug(f"generate_rook_moves col for {square_to_str(origin_sq)} are {square_to_str(col)}")
        logger.debug(f"generate_rook_moves row for {square_to_str(origin_sq)} are {square_to_str(row)}")

        # clear the origin sq the piece is on since we cannot "move" to the current sq.
        return bit_utils.clear_mask(row | col, origin_sq)

    def generate_bishop_moves(self, origin_sq):
        diag = find_diagonal(origin_sq) # there should be 1 or 2 diagonals
        diag = bit_utils.clear_mask(diag, origin_sq)
        logger.debug(f"generate_bishop_moves diagonals for {square_to_str(origin_sq)} are {square_to_str(diag)}")
        return diag

    def generate_king_moves(self, origin_square) -> int:
        possible_dest_squares: int = 0

        #   UP
        possible_dest_squares |= self.inbounds(origin_square << 8)
        # DIAGONAL UP LEFT
        possible_dest_squares |= self.inbounds(origin_square << 9)
        # DIAGONAL UP RIGHT
        possible_dest_squares |= self.inbounds(origin_square << 7)
        # DOWN
        possible_dest_squares |= self.inbounds(origin_square >> 8)
        # DIAGONAL DOWN LEFT
        possible_dest_squares |= self.inbounds(origin_square >> 7)
        # DIAGONAL DOWN RIGHT
        possible_dest_squares |= self.inbounds(origin_square >> 9)
        # LEFT
        logger.debug(f"generate_king_moves({square_to_str(origin_square)})/LEFT/before={square_to_str(possible_dest_squares)}")
        possible_dest_squares |= self.inbounds(origin_square << 1)
        logger.debug(f"generate_king_moves({square_to_str(origin_square)})/LEFT/after={square_to_str(possible_dest_squares)}")
        logger.debug(f"generate_king_moves({square_to_str(origin_square)})/LEFT/origin_square<<1={square_to_str(origin_square << 1)}")
        # RIGHT
        possible_dest_squares |= self.inbounds(origin_square >> 1)

        logger.debug(f'generate_king_moves({square_to_str(origin_square)})/possible_dest_squares={square_to_str(possible_dest_squares)}')

        return possible_dest_squares

    def generate_queen_moves(self, origin_sq):
        return self.generate_bishop_moves(origin_sq) | self.generate_rook_moves(origin_sq)

    def generate_pawn_moves(self, colour, origin_square, capture) -> int:
        possible_dest_squares: int = 0

        if colour == WHITE:
            if capture:
                # DIAGONAL UP LEFT
                possible_dest_squares |= self.inbounds(origin_square << 9)
                # DIAGONAL UP RIGHT
                possible_dest_squares |= self.inbounds(origin_square << 7)
            else:
                # UP one place
                possible_dest_squares |= self.inbounds(origin_square << 8)
                if find_row(origin_square) == ROW_2:
                    # UP two places
                    possible_dest_squares |= self.inbounds(origin_square << 16)

            # TODO white en passant???
        else:
            if capture:
                # DIAGONAL DOWN LEFT
                possible_dest_squares |= self.inbounds(origin_square >> 7)
                # DIAGONAL DOWN RIGHT
                possible_dest_squares |= self.inbounds(origin_square >> 9)
            else:
                # DOWN one place
                possible_dest_squares |= self.inbounds(origin_square >> 8)
                if find_row(origin_square) == ROW_7:
                    # DOWN TWO PLACES
                    possible_dest_squares |= self.inbounds(origin_square >> 16)
                # TODO black en passant???
        return possible_dest_squares

    def generate_moves(self, piece_type, colour, origin_sq, capture:bool=False) -> int:
        if piece_type == KNIGHT:
            return self.generate_knight_moves(origin_sq)
        elif piece_type == ROOK:
            return self.generate_rook_moves(origin_sq)
        elif piece_type == BISHOP:
            return self.generate_bishop_moves(origin_sq)
        elif piece_type == QUEEN:
            return self.generate_queen_moves(origin_sq)
        elif piece_type == KING:
            return self.generate_king_moves(origin_sq)
        elif piece_type == PAWN:
            return self.generate_pawn_moves(colour, origin_sq, capture)
        else:
            raise ValueError(f"unknown piece type: {piece_type}")

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

        def test(origin_sq):
            logger.debug(f"can_move_to()/origin({square_to_str(origin_sq)})")
            # get all squares the piece can move to
            possible_dest_sqs = self.generate_moves(piece_type, colour, origin_sq, capture)
            # if one of the squares is the dest square, then we've found the piece we are looking for
            if bit_utils.is_mask_set(possible_dest_sqs, dest_square):
                return origin_sq
            else:
                return 0

        #1. do we have a piece of the given colour and type?
        all_pieces_of_type_and_colour = self.__get_bitmap(piece_type, colour)

        #2. list all the pieces of this colour and type that can move to the destination square
        moveable_pieces_of_type_and_colour: int = bit_utils.for_each_bit_set(all_pieces_of_type_and_colour, highest_bit=A8, func=test)
        logger.info("%s %s can move from %s to %s",
                    piece_type_to_str(piece_type),
                    piece_colour_to_str(colour),
                    square_to_str(moveable_pieces_of_type_and_colour),
                    square_to_str(dest_square))

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

            if bit_utils.number_of_bits_set(moveable_pieces_of_type_and_colour, highest_bit=A8) != 1:
                raise ValueError(f"expected one piece that can move to "
                                 f"destination square {square_to_str(dest_square)} "
                                 f"but got the following possible origins "
                                 f"{square_to_str(moveable_pieces_of_type_and_colour)}")
            else:
                # we've found a single piece of the correct type and colour that can move to the destination square.
                # We assume the PGN files are valid, and that the move is legal
                # This sq is therefore the starting square for the move
                return moveable_pieces_of_type_and_colour

    def play(self, ply: PGNPly) -> None:
        logging.info(f"board playing ply: {ply}")

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
