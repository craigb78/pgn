from pgn.expr import PrintASTVisitor
from pgn.pgn_parser import PGNParser
from pgn.pgn_scanner import PGNScanner
from pathlib import Path
import sys
def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print("expected pgn file name as arg")
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