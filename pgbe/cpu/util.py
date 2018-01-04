from register import Register
import op


def convert_little_endian_to_big_endian(little_endian_value):
    """
    Convert 16-bit values from little-endian (least significant byte first) to big-endian (least significant byte last).

    Since the parameter contains the actual value and not its string representation, and also the fact that Python
    integers are "infinite", there is not way of knowing if the parameter is actually 16 bits or if it is less. E.g.
    0x00FF is a valid input, but is the same as 0xFF.

    :param little_endian_value: Original value in little-endian format
    :return: Value converted to big-endian
    """
    most_significant_byte = little_endian_value & 0x00FF
    least_significant_byte = (little_endian_value >> 8) & 0x00FF

    big_endian_value = (most_significant_byte << 8) | least_significant_byte
    return big_endian_value


def convert_unsigned_integer_to_signed(value, bit_length=8):
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


if __name__ == '__main__':
    register = Register()

    register.B = 0x00
    register.C = 0x01
    print("B=" + str(hex(register.B)) + "(" + str(register.B) + ")")
    print("C=" + str(hex(register.C)) + "(" + str(register.C) + ")")

    register.sub_bc(0x0100)

    print("B=" + str(hex(register.B)) + "(" + str(register.B) + ")")
    print("C=" + str(hex(register.C)) + "(" + str(register.C) + ")")

    op.code_01(register,0x9933)
