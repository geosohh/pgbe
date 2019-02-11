"""
Utility methods used throughout the code
"""


def convert_unsigned_integer_to_signed(value: int, bit_length: int = 8):
    """
    Python does not have an "unsigned" integer, but since its integer is "infinite", when converting hex/bin to int the
    value will be converted as if it was an unsigned hex/bin (e.g. int(0xFF) will return 255, not -1). This function
    makes the conversion considering that the input is signed.

    See: https://stackoverflow.com/a/11612456

    :param value: Value to be converted to signed int
    :param bit_length: Number of bits in the value
    :return: Signed int value
    """
    mask = (2 ** bit_length) - 1  # same as 0xFFFFF...
    if value & (1 << (bit_length - 1)):  # first bit is sign flag; if it is set then treat value as negative
        return value | ~mask
    else:
        return value  # otherwise just treat it as positive, i.e. no need to do anything
