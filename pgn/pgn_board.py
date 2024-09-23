import copy
from pgn_squares import *
from piece_type import *
from piece_colours import *
import pretty_print


class PGNBoard:

    def __init__(self):
        """ starting positions for a standard game """
        self.__black_king = H5
        self.__black_queen = H4
        self.__black_bishop = H3 | H6
        self.__black_knight = H2 | H7
        self.__black_rook = H1 | H8
        self.__black_pawn = FILE_G

        self.__white_queen = A4
        self.__white_king = A5
        self.__white_bishop = A3 | A6
        self.__white_knight = A2 | A7
        self.__white_rook = A1 | A8
        self.__white_pawn = FILE_B

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
        if self.is_set(self.__white_pawn, sq):
            return (WHITE, PAWN,)
        elif self.is_set(self.__white_rook, sq):
            return (WHITE, ROOK, )
        elif self.is_set(self.__white_knight, sq):
            return WHITE, KNIGHT,
        elif self.is_set(self.__white_bishop, sq):
            return (WHITE, BISHOP,)
        elif self.is_set(self.__white_queen, sq):
            return (WHITE, QUEEN,)
        elif self.is_set(self.__white_king, sq):
            return (WHITE, KING,)
        elif self.is_set(self.__black_pawn, sq):
            return (BLACK, PAWN,)
        elif self.is_set(self.__black_rook, sq):
            return (BLACK, ROOK,)
        elif self.is_set(self.__black_knight, sq):
            return (BLACK, KNIGHT, )
        elif self.is_set(self.__black_bishop, sq):
            return (BLACK, BISHOP,)
        elif self.is_set(self.__black_queen, sq):
            return (BLACK, QUEEN,)
        elif self.is_set(self.__black_king, sq):
            return (BLACK, KING,)

        return (-1, -1)

    def is_set(self, board, sq):
        return (board & sq) == sq

    @staticmethod
    def move(original_board, move):
        origin_sq = (move.piece_type, move.colour, move.destination_sq)

        cloned_board = copy.deepcopy(original_board)
        cloned_board.make_move(move.piece_type, move.colour, origin_sq, move.destination_sq)

        return cloned_board

    def make_move(self, piece_type, colour, origin_sq, destination_sq):
        if colour == WHITE:
            if piece_type == PAWN:
                self.__white_pawn = self.__replace(self.__white_pawn, origin_sq, destination_sq)
            elif piece_type == ROOK:
                self.__white_rook = self.__replace(self.__white_rook, origin_sq, destination_sq)
            elif piece_type == KNIGHT:
                self.__white_knight = self.__replace(self.__white_knight, origin_sq, destination_sq)
            elif piece_type == BISHOP:
                self.__white_bishop = self.__replace(self.__white_bishop, origin_sq, destination_sq)
            elif piece_type == QUEEN:
                self.__white_queen = self.__replace(self.__white_queen, origin_sq, destination_sq)
            elif piece_type == KING:
                self.__white_king = self.__replace(self.__white_king, origin_sq, destination_sq)
        else:
            if piece_type == PAWN:
                self.__black_pawn = self.__replace(self.__black_pawn, origin_sq, destination_sq)
            elif piece_type == ROOK:
                self.__black_rook = self.__replace(self.__black_rook, origin_sq, destination_sq)
            elif piece_type == KNIGHT:
                self.__black_knight = self.__replace(self.__black_knight, origin_sq, destination_sq)
            elif piece_type == BISHOP:
                self.__black_bishop = self.__replace(self.__black_bishop, origin_sq, destination_sq)
            elif piece_type == QUEEN:
                self.__black_queen = self.__replace(self.__black_queen, origin_sq, destination_sq)
            elif piece_type == KING:
                self.__black_king = self.__replace(self.__black_king, origin_sq, destination_sq)

    def __replace(self, bitmap, origin_sq, dest_sq):
        """ move the piece from the origin sq to the dest sq"""
        bitmap = bitmap ^ origin_sq
        bitmap = bitmap | dest_sq
        return bitmap

    def __str__(self):
        board_str  = '\t-\t' * 8 + "\n"
        file_str = ""
        sq = H8
        while sq > 0:
            (colour, piece_type) = self.get_piece(sq)
            file_str += '|\t'+pretty_print.get_icon(colour, piece_type)+'\t'
            sq = (sq >> 1)
            if len(file_str) == 32:
                board_str += file_str + "|\n"
                board_str += '\t-\t' * 8 + "\n"
                file_str = ""


        return board_str.rstrip() # rstrip to remove trailing \n

