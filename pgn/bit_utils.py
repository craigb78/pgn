def set_bit(bitmap, sq):
    """ where sq is the number of the square from 0-63 rather than the bitmask """
    return bitmap | (0x1 << sq)

def is_bit_set(bitmap, sq):
    (bitmap >> sq) & 0x1
def toggle_bit(bitmap, sq):
    return bitmap ^ (bitmap << sq)

def clearbit(bitmap, sq):
    return bitmap & ~(0x1 << sq)

