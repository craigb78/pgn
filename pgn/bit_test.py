from pgn_squares import *

rooks = A1
print("on A1", bin(rooks))

# remove rook from A1
rooks = rooks ^ A1
print("remove from A1", bin(rooks))

# move to A8
rooks = rooks | A8
print("move to A8", bin(rooks))
