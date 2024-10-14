def print_bitmap(msg: str, bitmap: int):
    print("{:064b}".format(bitmap), msg, "\n")


def set_mask(bitmap: int, sq: int):
    """ where sq is the bitmask (not the 0-63 number of the sq)"""
    return bitmap | sq


def is_mask_set(bitmap: int, sq: int):
    """ where sq is the bitmask (not the 0-63 number of the sq)"""
    if type(sq) != int:
        print("calling is_mask_set with non-int sq")
    if type(bitmap) != int:
        print("calling is_mask_set with non_int bitmap")

    return (bitmap & sq) == sq


def toggle_mask(bitmap: int, sq: int) -> int:
    """ where sq is the bitmask (not the 0-63 number of the sq)"""
    return bitmap ^ sq


def clear_mask(bitmap: int, sq: int):
    """ where sq is the bitmask (not the 0-63 number of the sq)"""
    return bitmap & ~sq


def for_each_bit_set(bitmap: int, highest_bit: int, lowest_bit: int = 0, func = lambda x: x) -> int:
    """
    Execute the supplied function for each bit set in the bitmap
    Accumulate the results of the function and return to caller
    :param bitmap:
    :param highest_bit (inclusive)
    :param lowest_bit (inclusive)
    :param func: defaults to identity function
    :return:
    """
    sq = highest_bit
    result_bitmap = 0
    while sq >= lowest_bit:
        if is_mask_set(bitmap, sq):
            result_bitmap |= func(sq)
        sq = sq >> 1
    return result_bitmap



def is_clear_run(bitmap: int, highest_bit: int, lowest_bit: int) -> bool:
    """
    Check that the range between highest bit and lowest bit is zero
    (excluding both highest and lowest bits).
    :param bitmap:
    :param highest_bit
    :param lowest_bit
    :return:
    """
    # because of right shift >> we need to move from the highest to the lowest bit
    if highest_bit < lowest_bit:
        highest_bit, lowest_bit = lowest_bit, highest_bit

    sq: int = highest_bit >> 1 # excluding the highest bit
    while sq > lowest_bit and sq > 0: # excluding the lowest bit
        if is_mask_set(bitmap, sq):
            return False
        sq = sq >> 1
    return True


def create_mask_exclusive(highest_bit: int, lowest_bit: int):
    """
    create mask of 1s from highest bit to lowest bit (exclusive of both)
    :param highest_bit:
    :param lowest_bit:
    :return:
    """
    if highest_bit < lowest_bit:
        highest_bit, lowest_bit = lowest_bit, highest_bit

    mask = 0
    sq: int = highest_bit >> 1 # excluding the highest bit
    while sq > lowest_bit and sq > 0: # excluding the lowest bit
        mask |= sq
        sq = sq >> 1
    return mask

def create_mask_inclusive(highest_bit: int, lowest_bit: int):
    if highest_bit < lowest_bit:
        highest_bit, lowest_bit = lowest_bit, highest_bit

    mask = 0
    sq: int = highest_bit # inccluding the highest bit
    while sq >= lowest_bit and sq >= 0: # excluding the lowest bit
        mask |= sq
        sq = sq >> 1
    return mask




def number_of_bits_set(bitmap: int, highest_bit: int):
    sq = highest_bit
    count = 0
    while sq > 0:
        if is_mask_set(bitmap, sq):
            count = count + 1
        sq = sq >> 1
    return count

# def set_bit(bitmap, sq):
#     """ where sq is the number of the square from 0-63 rather than the bitmask """
#     return bitmap | (0x1 << sq)
#
# def is_bit_set(bitmap, sq):
#     return (bitmap >> sq) & 0x1
#
# def toggle_bit(bitmap, sq):
#     return bitmap ^ (bitmap << sq)
#
# def clearbit(bitmap, sq):
#     return bitmap & ~(0x1 << sq)
