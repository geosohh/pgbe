"""
Tests for cpu/util.py
"""

import cpu.util

"""
Tests
"""


def test_convert_little_endian_to_big_endian():
    assert cpu.util.convert_little_endian_to_big_endian(0x9933) == 0x3399
    assert cpu.util.convert_little_endian_to_big_endian(0x0000) == 0x0000
    assert cpu.util.convert_little_endian_to_big_endian(0xFFFF) == 0xFFFF
    assert cpu.util.convert_little_endian_to_big_endian(0xFF) == 0xFF00


def test_convert_unsigned_integer_to_signed():
    assert cpu.util.convert_unsigned_integer_to_signed(0xFF) == -1
    assert cpu.util.convert_unsigned_integer_to_signed(0xFE) == -2
    assert cpu.util.convert_unsigned_integer_to_signed(0x80) == -128
    assert cpu.util.convert_unsigned_integer_to_signed(0x7F) == 127
    assert cpu.util.convert_unsigned_integer_to_signed(0x70) == 112
