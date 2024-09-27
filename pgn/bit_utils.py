def print_bitmap(msg, bitmap):
    print("{:064b}".format(bitmap), msg, "\n")


def set_mask(bitmap, sq):
    """ where sq is the bitmask (not the 0-63 number of the sq)"""
    return bitmap | sq


def is_mask_set(bitmap, sq):
    """ where sq is the bitmask (not the 0-63 number of the sq)"""
    if type(sq) != int:
        print("calling is_mask_set with non-int sq")
    if type(bitmap) != int:
        print("calling is_mask_set with non_int bitmap")

    return (bitmap & sq) == sq


def toggle_mask(bitmap, sq):
    """ where sq is the bitmask (not the 0-63 number of the sq)"""
    return bitmap ^ sq


def clear_mask(bitmap, sq):
    """ where sq is the bitmask (not the 0-63 number of the sq)"""
    return bitmap & ~sq


def for_each_bit_set(bitmap: int, highest_bit: int, func: object) -> int:
    """
    Execute the supplied function for each bit set in the bitmap
    Accumulate the results of the function and return to caller
    :param bitmap:
    :param highest_bit
    :param func:
    :return:
    """
    sq = highest_bit
    result_bitmap = 0
    while sq > 0:
        if is_mask_set(bitmap, sq):
            result_bitmap |= func(sq)
        sq = sq >> 1
    return result_bitmap


def number_of_bits_set(bitmap, highest_bit):
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
