import pgn_logging
import bit_utils

A8 = 2**63
B8 = 2**62
C8 = 2**61
D8 = 2**60
E8 = 2**59
F8 = 2**58
G8 = 2**57
H8 = 2**56

A7 = 2**55
B7 = 2**54
C7 = 2**53
D7 = 2**52
E7 = 2**51
F7 = 2**50
G7 = 2**49
H7 = 2**48

A6 = 2**47
B6 = 2**46
C6 = 2**45
D6 = 2**44
E6 = 2**43
F6 = 2**42
G6 = 2**41
H6 = 2**40

A5 = 2**39
B5 = 2**38
C5 = 2**37
D5 = 2**36
E5 = 2**35
F5 = 2**34
G5 = 2**33
H5 = 2**32

A4 = 2**31
B4 = 2**30
C4 = 2**29
D4 = 2**28
E4 = 2**27
F4 = 2**26
G4 = 2**25
H4 = 2**24

A3 = 2**23
B3 = 2**22
C3 = 2**21
D3 = 2**20
E3 = 2**19
F3 = 2**18
G3 = 2**17
H3 = 2**16

A2 = 2**15
B2 = 2**14
C2 = 2**13
D2 = 2**12
E2 = 2**11
F2 = 2**10
G2 = 2**9
H2 = 2**8

A1 = 2**7
B1 = 2**6
C1 = 2**5
D1 = 2**4
E1 = 2**3
F1 = 2**2
G1 = 2**1
H1 = 2**0

COL_A = A1 | A2 | A3 | A4 | A5 | A6 | A7 | A8
COL_B = B1 | B2 | B3 | B4 | B5 | B6 | B7 | B8
COL_C = C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8
COL_D = D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8
COL_E = E1 | E2 | E3 | E4 | E5 | E6 | E7 | E8
COL_F = F1 | F2 | F3 | F4 | F5 | F6 | F7 | F8
COL_G = G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8
COL_H = H1 | H2 | H3 | H4 | H5 | H6 | H7 | H8

ALL_COLS = (COL_A, COL_B, COL_C, COL_D, COL_E, COL_F, COL_G, COL_H)

ROW_1 = A1 | B1 | C1 | D1 | E1 | F1 | G1 | H1
ROW_2 = A2 | B2 | C2 | D2 | E2 | F2 | G2 | H2
ROW_3 = A3 | B3 | C3 | D3 | E3 | F3 | G3 | H3
ROW_4 = A4 | B4 | C4 | D4 | E4 | F4 | G4 | H4
ROW_5 = A5 | B5 | C5 | D5 | E5 | F5 | G5 | H5
ROW_6 = A6 | B6 | C6 | D6 | E6 | F6 | G6 | H6
ROW_7 = A7 | B7 | C7 | D7 | E7 | F7 | G7 | H7
ROW_8 = A8 | B8 | C8 | D8 | E8 | F8 | G8 | H8

ALL_ROWS = (ROW_1, ROW_2, ROW_3, ROW_4, ROW_5, ROW_6, ROW_7, ROW_8)

# diagonals bottom left (A1) to top right (H8)
DIAGONAL_1  = A2 | B1
DIAGONAL_2  = A3 | B2 | C1
DIAGONAL_3  = A4 | B3 | C2 | D1
DIAGONAL_4  = A5 | B4 | C3 | D2 | E1
DIAGONAL_5  = A6 | B5 | C4 | D3 | E2 | F1
DIAGONAL_6  = A7 | B6 | C5 | D4 | E3 | F2 | G1
DIAGONAL_7  = A8 | B7 | C6 | D5 | E4 | F3 | G2 | H1
DIAGONAL_8  =      B8 | C7 | D6 | E5 | F4 | G3 | H2
DIAGONAL_9  =           C8 | D7 | E6 | F5 | G4 | H3
DIAGONAL_10 =                D8 | E7 | F6 | G5 | H4
DIAGONAL_11 =                     E8 | F7 | G6 | H5
DIAGONAL_12 =                          F8 | G7 | H6
DIAGONAL_13 =                               G8 | H7

# diagonals bottom right (H8) to top left (A8)
DIAGONAL_14 =                               G1 | H2
DIAGONAL_15 =                          F1 | G2 | H3
DIAGONAL_16 =                     E1 | F2 | G3 | H4
DIAGONAL_17 =                D1 | E2 | F3 | G4 | H5
DIAGONAL_18 =           C1 | D2 | E3 | F4 | G5 | H6
DIAGONAL_19 =      B1 | C2 | D3 | E4 | F5 | G6 | H7
DIAGONAL_20 = A1 | B2 | C3 | D4 | E5 | F6 | G7 | H8
DIAGONAL_21 = A2 | B3 | C4 | D5 | E6 | F7 | G8
DIAGONAL_22 = A3 | B4 | C5 | D6 | E7 | F8
DIAGONAL_23 = A4 | B5 | C6 | D7 | E8
DIAGONAL_24 = A5 | B6 | C7 | D8
DIAGONAL_25 = A6 | B7 | C8
DIAGONAL_26 = A7 | B8

ALL_DIAGONALS = (
    DIAGONAL_1,
    DIAGONAL_2,
    DIAGONAL_3,
    DIAGONAL_4,
    DIAGONAL_5,
    DIAGONAL_6,
    DIAGONAL_7,
    DIAGONAL_8,
    DIAGONAL_9,
    DIAGONAL_10,
    DIAGONAL_11,
    DIAGONAL_12,
    DIAGONAL_13,
    DIAGONAL_14,
    DIAGONAL_15,
    DIAGONAL_16,
    DIAGONAL_17,
    DIAGONAL_18,
    DIAGONAL_19,
    DIAGONAL_20,
    DIAGONAL_21,
    DIAGONAL_22,
    DIAGONAL_23,
    DIAGONAL_24,
    DIAGONAL_25,
    DIAGONAL_26
)

def square_to_str(bitmap):
    bitmap_str = {
        A1: "A1", A2: "A2", A3: "A3", A4: "A4", A5: "A5", A6: "A6", A7: "A7", A8: "A8",
        B1: "B1", B2: "B2", B3: "B3", B4: "B4", B5: "B5", B6: "B6", B7: "B7", B8: "B8",
        C1: "C1", C2: "C2", C3: "C3", C4: "C4", C5: "C5", C6: "C6", C7: "C7", C8: "C8",
        D1: "D1", D2: "D2", D3: "D3", D4: "D4", D5: "D5", D6: "D6", D7: "D7", D8: "D8",
        E1: "E1", E2: "E2", E3: "E3", E4: "E4", E5: "E5", E6: "E6", E7: "E7", E8: "E8",
        F1: "F1", F2: "F2", F3: "F3", F4: "F4", F5: "F5", F6: "F6", F7: "F7", F8: "F8",
        G1: "G1", G2: "G2", G3: "G3", G4: "G4", G5: "G5", G6: "G6", G7: "G7", G8: "G8",
        H1: "H1", H2: "H2", H3: "H3", H4: "H4", H5: "H5", H6: "H6", H7: "H7", H8: "H8"
    }

    matches = ""
    for square, square_str in bitmap_str.items():
        if bit_utils.is_mask_set(bitmap, square):
            if len(matches) != 0:
                matches += ','
            matches += square_str
    return matches

def find_row(origin_sq):
    """
    find the row containing the origin_sq
    :param origin_sq:
    :return:
    """
    for row in ALL_ROWS:
        if bit_utils.is_mask_set(row, origin_sq):
            return row
    return 0


def find_col(origin_sq):
    """
    find the col containing the origin square
    :param origin_sq:
    :return:
    """
    for col in ALL_COLS:
        if bit_utils.is_mask_set(col, origin_sq):
            return col
    return 0


def find_diagonal(origin_sq):
    matching = 0
    for diagonal in ALL_DIAGONALS:
        pgn_logging.logger.debug(f"find_diagonal({square_to_str(origin_sq)})/next diagonal/{square_to_str(diagonal)}")
        if bit_utils.is_mask_set(diagonal, origin_sq):
            pgn_logging.logger.debug(f"find_diagonal({square_to_str(origin_sq)})/adding diagonal/{square_to_str(diagonal)}")
            matching |= diagonal
    pgn_logging.logger.debug(f"find_diagonal()/result/{square_to_str(matching)}")
    return matching
