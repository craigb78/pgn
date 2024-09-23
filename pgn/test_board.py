import unittest
from pgn_board import *

class TestBoard(unittest.TestCase):
    def test_to_str(self):
        # given
        b = PGNBoard()
        expected_b_str = """	-		-		-		-		-		-		-		-	
|	♜	|	♞	|	♝	|	♚	|	♛	|	♝	|	♞	|	♜	|
	-		-		-		-		-		-		-		-	
|	♟	|	♟	|	♟	|	♟	|	♟	|	♟	|	♟	|	♟	|
	-		-		-		-		-		-		-		-	
|	 	|	 	|	 	|	 	|	 	|	 	|	 	|	 	|
	-		-		-		-		-		-		-		-	
|	 	|	 	|	 	|	 	|	 	|	 	|	 	|	 	|
	-		-		-		-		-		-		-		-	
|	 	|	 	|	 	|	 	|	 	|	 	|	 	|	 	|
	-		-		-		-		-		-		-		-	
|	 	|	 	|	 	|	 	|	 	|	 	|	 	|	 	|
	-		-		-		-		-		-		-		-	
|	♙	|	♙	|	♙	|	♙	|	♙	|	♙	|	♙	|	♙	|
	-		-		-		-		-		-		-		-	
|	♖	|	♘	|	♗	|	♔	|	♕	|	♗	|	♘	|	♖	|
	-		-		-		-		-		-		-		-"""

        # when
        b_str = str(b)

        # then
        print(b_str)
        self.assertEqual(b_str, expected_b_str)