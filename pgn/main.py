# TODO
# need a SAN_parser that processes the output of SAN_Scanner
# The SAN Parser should use the PGN board and the tokens from the scanner to create "move" objects which can be "played"
# forward and backwards on a board
# tasks
# 1. create SAN_parser class to process SAN scanner tokens
# 2. create a PGNBoard class. Since PGN files typically only contain the destination square and piece type and colour
#       we need to find which of the pieces of the same colour/type can move to the destination square
# 3. SAN Parser to output a list of PGNMove objects
# 4. end result should be ability to print list of PGNMove objects, with each move object showing piece type, colour
# , source square, dest sq, and so on.

from pgn_board import PGNBoard
from pgn_token import Token
from pgn.expr import PrintASTVisitor
from pgn.pgn_parser import PGNParser
from pgn.pgn_scanner import PGNScanner
from pgn.regex_scanner import RegexSANScanner
from pgn.san_parser import SANParser
from pathlib import Path
import sys
from pgn_logging import logger


def main():
    try:
        args = sys.argv[1:]
        if len(args) != 1:
            logger.debug("expected pgn file name as arg")

            exit(-1)

        pgn_file = Path(args[0]).read_text()
        scanner = PGNScanner(pgn_file)
        scanner.scan_tokens()
        scanner.print_tokens()
        if scanner.has_errors():
            scanner.print_errors()

        parser = PGNParser(scanner.tokens())
        pgn_database = parser.parse()
        if parser.has_errors():
            parser.print_errors()

        for j, pgn_game in enumerate(pgn_database.games):
            logger.info(f"***************GAME {j+1}****************8")

            san_parser = SANParser()
            for elem in pgn_game.move_text.element_sequence.elements:
                if len(elem.san_moves) == 0:
                    raise ValueError("expected at least one ply")

                # we have a white ply
                white_token: Token = elem.san_moves[0]
                #san_scanner = SANScanner(white_token.lexeme)
                san_scanner = RegexSANScanner(white_token.lexeme)
                white_san_tokens: [Token] = san_scanner.scan_tokens()

                # we have a black ply
                black_san_tokens = []
                if len(elem.san_moves) == 2:
                    black_token: Token = elem.san_moves[1]
                   # san_scanner = SANScanner(black_token.lexeme)
                    san_scanner = RegexSANScanner(black_token.lexeme)
                    black_san_tokens: [Token] = san_scanner.scan_tokens()

                san_parser.parse_san_move(white_san_tokens, black_san_tokens)

            pgn_moves = san_parser.collect()

            # TODO add the event information to the list of PGN moves
            board = PGNBoard()
            for i, pgn_move in enumerate(pgn_moves):
                logger.info(f"==============GAME {j+1} / MOVE {i+1} ===============")
                board.play(pgn_move.white_ply)
                if pgn_move.black_ply:
                    board.play(pgn_move.black_ply)
                logger.debug(board)

        visitor = PrintASTVisitor()
        pgn_database.accept(visitor)
    except ValueError as err:
        logger.exception("Error is main")

    exit(0)


if __name__ == "__main__":
    main()
