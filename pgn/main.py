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


# TODO



from pgn.expr import PrintASTVisitor
from pgn.pgn_parser import PGNParser
from pgn.pgn_scanner import PGNScanner
from pathlib import Path
import sys
from pgn_logging import logger


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        #print("expected pgn file name as arg")
        logger.debug("expected pgn file name as arg")

        exit(-1)

    pgn_file = Path(args[0]).read_text()
    scanner = PGNScanner(pgn_file)
    scanner.scan_tokens()
    scanner.print_tokens()
    if scanner.has_errors():
        scanner.print_errors()

    parser = PGNParser(scanner.tokens())
    ast = parser.parse()
    if parser.has_errors():
        parser.print_errors()

    visitor = PrintASTVisitor()
    ast.accept(visitor)

    exit(0)

if __name__ == "__main__":
    main()