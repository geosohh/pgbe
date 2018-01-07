"""
Tests for cpu/op.py
"""

import pytest
import cpu.op

"""
Fixtures act as test setup/teardown in py.test.
For each test method with a parameter, the parameter name is the setup method that will be called.
"""


@pytest.fixture
def register():
    """
    Create Register instance for testing.
    :return: new register instance
    """
    from cpu.register import Register
    return Register()


"""
Tests
"""


def assert_registers(reg, a=0x00, f=0x00, b=0x00, c=0x00, d=0x00, e=0x00, h=0x00, l=0x00, sp=0xFFFE, pc=0x0100):
    """
    Helper function to assert registers values.
    By default will check if values are the default, unless parameter is received.
    """
    assert reg.A == a
    assert reg.F == f
    assert reg.B == b
    assert reg.C == c
    assert reg.D == d
    assert reg.E == e
    assert reg.H == h
    assert reg.L == l
    assert reg.SP == sp
    assert reg.PC == pc


def test_code_00():
    """ NOP - Does nothing """
    cycles = cpu.op.code_00()
    assert cycles == 4


# noinspection PyShadowingNames
def test_code_01(register):
    """ LD BC,d16 - Stores given 16-bit value at BC """


# noinspection PyShadowingNames
def test_code_02(register):
    """ LD (BC),A - Stores reg at the address in BC """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_03(register):
    """ INC BC - BC=BC+1 """
    register.set_bc(0x0000)
    cycles = cpu.op.code_03(register)
    assert cycles == 8
    assert_registers(register, b=0x00, c=0x01)

    register.set_bc(0x00FF)
    cycles = cpu.op.code_03(register)
    assert cycles == 8
    assert_registers(register, b=0x01, c=0x00)

    register.set_bc(0x0FFF)
    cycles = cpu.op.code_03(register)
    assert cycles == 8
    assert_registers(register, b=0x10, c=0x00)

    register.set_bc(0xFFFF)
    cycles = cpu.op.code_03(register)
    assert cycles == 8
    assert_registers(register, b=0x00, c=0x00)

    
# noinspection PyShadowingNames
def test_code_04(register):
    """ INC B - B=B+1 """
    register.B = 0x00
    cycles = cpu.op.code_04(register)
    assert cycles == 4
    assert_registers(register, b=0x01, f=0b00000000)

    register.B = 0x0F
    cycles = cpu.op.code_04(register)
    assert cycles == 4
    assert_registers(register, b=0x10, f=0b00100000)

    register.B = 0xF0
    cycles = cpu.op.code_04(register)
    assert cycles == 4
    assert_registers(register, b=0xF1, f=0b00000000)

    register.B = 0xFF
    cycles = cpu.op.code_04(register)
    assert cycles == 4
    assert_registers(register, b=0x00, f=0b10100000)


# noinspection PyShadowingNames
def test_code_05(register):
    """ DEC B - B=B-1 """
    register.B = 0x00
    cycles = cpu.op.code_05(register)
    assert cycles == 4
    assert_registers(register, b=0xFF, f=0b01100000)

    register.B = 0x0F
    cycles = cpu.op.code_05(register)
    assert cycles == 4
    assert_registers(register, b=0x0E, f=0b01000000)

    register.B = 0x01
    cycles = cpu.op.code_05(register)
    assert cycles == 4
    assert_registers(register, b=0x00, f=0b11000000)


# noinspection PyShadowingNames
def test_code_06(register):
    """ LD B,d8 """
    cycles = cpu.op.code_06(register, 0x99)
    assert cycles == 8
    assert_registers(register,b=0x99)


# noinspection PyShadowingNames
def test_code_07(register):
    """ RLCA - Copy register A bit 7 to Carry flag, then rotate register A left """
    register.A = 0b11100010
    cycles = cpu.op.code_07(register)
    assert cycles == 4
    assert_registers(register, a=0b11000101, f=0b00010000)

    register.A = 0b00000000
    cycles = cpu.op.code_07(register)
    assert cycles == 4
    assert_registers(register, a=0b00000000, f=0b10000000)


# noinspection PyShadowingNames
def test_code_08(register):
    """ LD (a16),SP - Set SP value into address (a16) """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_09(register):
    """ ADD HL,BC - HL=HL+BC """
    register.set_hl(0x0000)
    register.set_bc(0x0001)
    cycles = cpu.op.code_09(register)
    assert cycles == 8
    assert_registers(register, b=0x00, c=0x01, h=0x00, l=0x01, f=0b00000000)

    register.set_hl(0x000F)
    register.set_bc(0x0001)
    cycles = cpu.op.code_09(register)
    assert cycles == 8
    assert_registers(register, b=0x00, c=0x01, h=0x00, l=0x10, f=0b00000000)

    register.set_hl(0xF000)
    register.set_bc(0x1000)
    cycles = cpu.op.code_09(register)
    assert cycles == 8
    assert_registers(register, b=0x10, c=0x00, h=0x00, l=0x00, f=0b00010000)

    register.set_hl(0x0FFF)
    register.set_bc(0x0001)
    cycles = cpu.op.code_09(register)
    assert cycles == 8
    assert_registers(register, b=0x00, c=0x01, h=0x10, l=0x00, f=0b00100000)

    register.set_hl(0xFFFF)
    register.set_bc(0x0001)
    cycles = cpu.op.code_09(register)
    assert cycles == 8
    assert_registers(register, b=0x00, c=0x01, h=0x00, l=0x00, f=0b00110000)

    register.set_hl(0xFFFF)
    register.set_bc(0x0002)
    cycles = cpu.op.code_09(register)
    assert cycles == 8
    assert_registers(register, b=0x00, c=0x02, h=0x00, l=0x01, f=0b00110000)


# noinspection PyShadowingNames
def test_code_0a(register):
    """ LD A,(BC) - Load reg with the value at the address in BC """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_0b(register):
    """ DEC BC - BC=BC-1 """
    register.set_bc(0x0000)
    cycles = cpu.op.code_0b(register)
    assert cycles == 8
    assert_registers(register, b=0xFF, c=0xFF)

    register.set_bc(0x0100)
    cycles = cpu.op.code_0b(register)
    assert cycles == 8
    assert_registers(register, b=0x00, c=0xFF)

    register.set_bc(0x1000)
    cycles = cpu.op.code_0b(register)
    assert cycles == 8
    assert_registers(register, b=0x0F, c=0xFF)


# noinspection PyShadowingNames
def test_code_0c(register):
    """ INC C - C=C+1 """
    register.C = 0x00
    cycles = cpu.op.code_0c(register)
    assert cycles == 4
    assert_registers(register, c=0x01, f=0b00000000)

    register.C = 0x0F
    cycles = cpu.op.code_0c(register)
    assert cycles == 4
    assert_registers(register, c=0x10, f=0b00100000)

    register.C = 0xF0
    cycles = cpu.op.code_0c(register)
    assert cycles == 4
    assert_registers(register, c=0xF1, f=0b00000000)

    register.C = 0xFF
    cycles = cpu.op.code_0c(register)
    assert cycles == 4
    assert_registers(register, c=0x00, f=0b10100000)


# noinspection PyShadowingNames
def test_code_0d(register):
    """ DEC C - C=C-1 """
    register.C = 0x00
    cycles = cpu.op.code_0d(register)
    assert cycles == 4
    assert_registers(register, c=0xFF, f=0b01100000)

    register.C = 0x0F
    cycles = cpu.op.code_0d(register)
    assert cycles == 4
    assert_registers(register, c=0x0E, f=0b01000000)

    register.C = 0x01
    cycles = cpu.op.code_0d(register)
    assert cycles == 4
    assert_registers(register, c=0x00, f=0b11000000)


# noinspection PyShadowingNames
def test_code_0e(register):
    """ LD C,d8 """
    cycles = cpu.op.code_0e(register, 0x99)
    assert cycles == 8
    assert_registers(register,c=0x99)


# noinspection PyShadowingNames
def test_code_0f(register):
    """ RRCA - Copy register A bit 0 to Carry flag, then rotate register A right """
    register.A = 0b11100011
    cycles = cpu.op.code_0f(register)
    assert cycles == 4
    assert_registers(register, a=0b11110001, f=0b00010000)

    register.A = 0b00000000
    cycles = cpu.op.code_0f(register)
    assert cycles == 4
    assert_registers(register, a=0b00000000, f=0b10000000)


# noinspection PyShadowingNames
def test_code_10(register):
    """
    STOP - Switch Game Boy into VERY low power standby mode. Halt CPU and LCD display until a button is pressed
    See: http://gbdev.gg8.se/wiki/articles/Reducing_Power_Consumption
    """
    # TODO after cpu and interrupts are implemented
    pass


# noinspection PyShadowingNames
def test_code_11(register):
    """ LD DE,d16 - Stores given 16-bit value at DE """
    cycles = cpu.op.code_11(register, 0x9933)  # Little-endian
    assert cycles == 12
    assert_registers(register,d=0x33,e=0x99)


# noinspection PyShadowingNames
def test_code_12(register):
    """ LD (DE),A - Stores reg at the address in DE """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_13(register):
    """ INC DE - DE=DE+1 """
    register.set_de(0x0000)
    cycles = cpu.op.code_13(register)
    assert cycles == 8
    assert_registers(register, d=0x00, e=0x01)

    register.set_de(0x00FF)
    cycles = cpu.op.code_13(register)
    assert cycles == 8
    assert_registers(register, d=0x01, e=0x00)

    register.set_de(0x0FFF)
    cycles = cpu.op.code_13(register)
    assert cycles == 8
    assert_registers(register, d=0x10, e=0x00)

    register.set_de(0xFFFF)
    cycles = cpu.op.code_13(register)
    assert cycles == 8
    assert_registers(register, d=0x00, e=0x00)


# noinspection PyShadowingNames
def test_code_14(register):
    """ INC D - D=D+1 """
    register.D = 0x00
    cycles = cpu.op.code_14(register)
    assert cycles == 4
    assert_registers(register, d=0x01, f=0b00000000)

    register.D = 0x0F
    cycles = cpu.op.code_14(register)
    assert cycles == 4
    assert_registers(register, d=0x10, f=0b00100000)

    register.D = 0xF0
    cycles = cpu.op.code_14(register)
    assert cycles == 4
    assert_registers(register, d=0xF1, f=0b00000000)

    register.D = 0xFF
    cycles = cpu.op.code_14(register)
    assert cycles == 4
    assert_registers(register, d=0x00, f=0b10100000)


# noinspection PyShadowingNames
def test_code_15(register):
    """ DEC D - D=D-1 """
    register.D = 0x00
    cycles = cpu.op.code_15(register)
    assert cycles == 4
    assert_registers(register, d=0xFF, f=0b01100000)

    register.D = 0x0F
    cycles = cpu.op.code_15(register)
    assert cycles == 4
    assert_registers(register, d=0x0E, f=0b01000000)

    register.D = 0x01
    cycles = cpu.op.code_15(register)
    assert cycles == 4
    assert_registers(register, d=0x00, f=0b11000000)


# noinspection PyShadowingNames
def test_code_16(register):
    """ LD D,d8 """
    cycles = cpu.op.code_16(register, 0x99)
    assert cycles == 8
    assert_registers(register,d=0x99)


# noinspection PyShadowingNames
def test_code_17(register):
    """ RLA - Copy register A bit 7 to temp, replace A bit 7 with Carry flag, rotate A left, copy temp to Carry flag """
    register.A = 0b11100010
    register.F = 0b00010000
    cycles = cpu.op.code_17(register)
    assert cycles == 4
    assert_registers(register, a=0b11000101, f=0b00010000)

    register.A = 0b00000000
    register.F = 0b00010000
    cycles = cpu.op.code_17(register)
    assert cycles == 4
    assert_registers(register, a=0b00000001, f=0b00000000)


# noinspection PyShadowingNames
def test_code_19(register):
    """ ADD HL,DE - HL=HL+DE """
    register.set_hl(0x0000)
    register.set_de(0x0001)
    cycles = cpu.op.code_19(register)
    assert cycles == 8
    assert_registers(register, d=0x00, e=0x01, h=0x00, l=0x01, f=0b00000000)

    register.set_hl(0x000F)
    register.set_de(0x0001)
    cycles = cpu.op.code_19(register)
    assert cycles == 8
    assert_registers(register, d=0x00, e=0x01, h=0x00, l=0x10, f=0b00000000)

    register.set_hl(0xF000)
    register.set_de(0x1000)
    cycles = cpu.op.code_19(register)
    assert cycles == 8
    assert_registers(register, d=0x10, e=0x00, h=0x00, l=0x00, f=0b00010000)

    register.set_hl(0x0FFF)
    register.set_de(0x0001)
    cycles = cpu.op.code_19(register)
    assert cycles == 8
    assert_registers(register, d=0x00, e=0x01, h=0x10, l=0x00, f=0b00100000)

    register.set_hl(0xFFFF)
    register.set_de(0x0001)
    cycles = cpu.op.code_19(register)
    assert cycles == 8
    assert_registers(register, d=0x00, e=0x01, h=0x00, l=0x00, f=0b00110000)

    register.set_hl(0xFFFF)
    register.set_de(0x0002)
    cycles = cpu.op.code_19(register)
    assert cycles == 8
    assert_registers(register, d=0x00, e=0x02, h=0x00, l=0x01, f=0b00110000)


# noinspection PyShadowingNames
def test_code_1a(register):
    """ LD A,(DE) - Load reg with the value at the address in DE """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_1b(register):
    """ DEC DE - DE=DE-1 """
    register.set_de(0x0000)
    cycles = cpu.op.code_1b(register)
    assert cycles == 8
    assert_registers(register, d=0xFF, e=0xFF)

    register.set_de(0x0100)
    cycles = cpu.op.code_1b(register)
    assert cycles == 8
    assert_registers(register, d=0x00, e=0xFF)

    register.set_de(0x1000)
    cycles = cpu.op.code_1b(register)
    assert cycles == 8
    assert_registers(register, d=0x0F, e=0xFF)


# noinspection PyShadowingNames
def test_code_1c(register):
    """ INC E - E=E+1 """
    register.E = 0x00
    cycles = cpu.op.code_1c(register)
    assert cycles == 4
    assert_registers(register, e=0x01, f=0b00000000)

    register.E = 0x0F
    cycles = cpu.op.code_1c(register)
    assert cycles == 4
    assert_registers(register, e=0x10, f=0b00100000)

    register.E = 0xF0
    cycles = cpu.op.code_1c(register)
    assert cycles == 4
    assert_registers(register, e=0xF1, f=0b00000000)

    register.E = 0xFF
    cycles = cpu.op.code_1c(register)
    assert cycles == 4
    assert_registers(register, e=0x00, f=0b10100000)


# noinspection PyShadowingNames
def test_code_1d(register):
    """ DEC E - E=E-1 """
    register.E = 0x00
    cycles = cpu.op.code_1d(register)
    assert cycles == 4
    assert_registers(register, e=0xFF, f=0b01100000)

    register.E = 0x0F
    cycles = cpu.op.code_1d(register)
    assert cycles == 4
    assert_registers(register, e=0x0E, f=0b01000000)

    register.E = 0x01
    cycles = cpu.op.code_1d(register)
    assert cycles == 4
    assert_registers(register, e=0x00, f=0b11000000)


# noinspection PyShadowingNames
def test_code_1e(register):
    """ LD E,d8 """
    cycles = cpu.op.code_1e(register, 0x99)
    assert cycles == 8
    assert_registers(register,e=0x99)


# noinspection PyShadowingNames
def test_code_1f(register):
    """ RRA - Copy register A bit 0 to temp, replace A bit 0 w/ Carry flag, rotate A right, copy temp to Carry flag """
    register.A = 0b11100011
    register.F = 0b00010000
    cycles = cpu.op.code_1f(register)
    assert cycles == 4
    assert_registers(register, a=0b11110001, f=0b00010000)

    register.A = 0b00000000
    register.F = 0b00010000
    cycles = cpu.op.code_1f(register)
    assert cycles == 4
    assert_registers(register, a=0b10000000, f=0b00000000)


# noinspection PyShadowingNames
def test_code_21(register):
    """ LD HL,d16 - Stores given 16-bit value at HL """
    cycles = cpu.op.code_21(register, 0x9933)  # Little-endian
    assert cycles == 12
    assert_registers(register,h=0x33,l=0x99)


# noinspection PyShadowingNames
def test_code_22(register):
    """ LD (HL+),A or LD (HLI),A or LDI (HL),A - Put value at A into address HL. Increment HL """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_23(register):
    """ INC HL - HL=HL+1 """
    register.set_hl(0x0000)
    cycles = cpu.op.code_23(register)
    assert cycles == 8
    assert_registers(register, h=0x00, l=0x01)

    register.set_hl(0x00FF)
    cycles = cpu.op.code_23(register)
    assert cycles == 8
    assert_registers(register, h=0x01, l=0x00)

    register.set_hl(0x0FFF)
    cycles = cpu.op.code_23(register)
    assert cycles == 8
    assert_registers(register, h=0x10, l=0x00)

    register.set_hl(0xFFFF)
    cycles = cpu.op.code_23(register)
    assert cycles == 8
    assert_registers(register, h=0x00, l=0x00)


# noinspection PyShadowingNames
def test_code_24(register):
    """ INC H - H=H+1 """
    register.H = 0x00
    cycles = cpu.op.code_24(register)
    assert cycles == 4
    assert_registers(register, h=0x01, f=0b00000000)

    register.H = 0x0F
    cycles = cpu.op.code_24(register)
    assert cycles == 4
    assert_registers(register, h=0x10, f=0b00100000)

    register.H = 0xF0
    cycles = cpu.op.code_24(register)
    assert cycles == 4
    assert_registers(register, h=0xF1, f=0b00000000)

    register.H = 0xFF
    cycles = cpu.op.code_24(register)
    assert cycles == 4
    assert_registers(register, h=0x00, f=0b10100000)


# noinspection PyShadowingNames
def test_code_25(register):
    """ DEC H - H=H-1 """
    register.H = 0x00
    cycles = cpu.op.code_25(register)
    assert cycles == 4
    assert_registers(register, h=0xFF, f=0b01100000)

    register.H = 0x0F
    cycles = cpu.op.code_25(register)
    assert cycles == 4
    assert_registers(register, h=0x0E, f=0b01000000)

    register.H = 0x01
    cycles = cpu.op.code_25(register)
    assert cycles == 4
    assert_registers(register, h=0x00, f=0b11000000)


# noinspection PyShadowingNames
def test_code_26(register):
    """ LD H,d8 """
    cycles = cpu.op.code_26(register, 0x99)
    assert cycles == 8
    assert_registers(register,h=0x99)


# noinspection PyShadowingNames
def test_code_27(register):
    """
    DAA - Adjust value in register A for Binary Coded Decimal representation (i.e. one 0-9 value per nibble)
    See:  http://gbdev.gg8.se/wiki/articles/DAA
    """
    register.A = 0b00111100  # 3|12 -> should be 4|2
    register.F = 0b00000000
    cycles = cpu.op.code_27(register)
    assert cycles == 4
    assert_registers(register, a=0b01000010, f=0b00000000)

    register.A = 0b01100100  # 6|4 -> should stay 6|4
    register.F = 0b00000000
    cycles = cpu.op.code_27(register)
    assert cycles == 4
    assert_registers(register, a=0b01100100, f=0b00000000)

    register.A = 0b10100000  # 10|0 -> should be 0|0 with Z flag
    register.F = 0b00000000
    cycles = cpu.op.code_27(register)
    assert cycles == 4
    assert_registers(register, a=0b00000000, f=0b10010000)

    register.A = 0b11000010  # 12|2 -> should be 2|2 with C flag
    register.F = 0b00000000
    cycles = cpu.op.code_27(register)
    assert cycles == 4
    assert_registers(register, a=0b00100010, f=0b00010000)

    register.A = 0b00001010  # 0|10 with N/H flag-> should be 0|4
    register.F = 0b01100000
    cycles = cpu.op.code_27(register)
    assert cycles == 4
    assert_registers(register, a=0b00000100, f=0b01000000)


# noinspection PyShadowingNames
def test_code_29(register):
    """ ADD HL,HL - HL=HL+HL """
    register.set_hl(0x0001)
    cycles = cpu.op.code_29(register)
    assert cycles == 8
    assert_registers(register, h=0x00, l=0x02, f=0b00000000)

    register.set_hl(0x0008)
    cycles = cpu.op.code_29(register)
    assert cycles == 8
    assert_registers(register, h=0x00, l=0x10, f=0b00000000)

    register.set_hl(0x8000)
    cycles = cpu.op.code_29(register)
    assert cycles == 8
    assert_registers(register, h=0x00, l=0x00, f=0b00010000)

    register.set_hl(0x0800)
    cycles = cpu.op.code_29(register)
    assert cycles == 8
    assert_registers(register, h=0x10, l=0x00, f=0b00100000)

    register.set_hl(0x8800)
    cycles = cpu.op.code_29(register)
    assert cycles == 8
    assert_registers(register, h=0x10, l=0x00, f=0b00110000)

    register.set_hl(0xFFFF)
    cycles = cpu.op.code_29(register)
    assert cycles == 8
    assert_registers(register, h=0xFF, l=0xFE, f=0b00110000)


# noinspection PyShadowingNames
def test_code_2a(register):
    """ LD A,(HL+) or LD A,(HLI) or LDI A,(HL) - Put value at address HL into A. Increment HL """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_2b(register):
    """ DEC HL - HL=HL-1 """
    register.set_hl(0x0000)
    cycles = cpu.op.code_2b(register)
    assert cycles == 8
    assert_registers(register, h=0xFF, l=0xFF)

    register.set_hl(0x0100)
    cycles = cpu.op.code_2b(register)
    assert cycles == 8
    assert_registers(register, h=0x00, l=0xFF)

    register.set_hl(0x1000)
    cycles = cpu.op.code_2b(register)
    assert cycles == 8
    assert_registers(register, h=0x0F, l=0xFF)


# noinspection PyShadowingNames
def test_code_2c(register):
    """ INC L - L=L+1 """
    register.L = 0x00
    cycles = cpu.op.code_2c(register)
    assert cycles == 4
    assert_registers(register, l=0x01, f=0b00000000)

    register.L = 0x0F
    cycles = cpu.op.code_2c(register)
    assert cycles == 4
    assert_registers(register, l=0x10, f=0b00100000)

    register.L = 0xF0
    cycles = cpu.op.code_2c(register)
    assert cycles == 4
    assert_registers(register, l=0xF1, f=0b00000000)

    register.L = 0xFF
    cycles = cpu.op.code_2c(register)
    assert cycles == 4
    assert_registers(register, l=0x00, f=0b10100000)


# noinspection PyShadowingNames
def test_code_2d(register):
    """ DEC L - L=L-1 """
    register.L = 0x00
    cycles = cpu.op.code_2d(register)
    assert cycles == 4
    assert_registers(register, l=0xFF, f=0b01100000)

    register.L = 0x0F
    cycles = cpu.op.code_2d(register)
    assert cycles == 4
    assert_registers(register, l=0x0E, f=0b01000000)

    register.L = 0x01
    cycles = cpu.op.code_2d(register)
    assert cycles == 4
    assert_registers(register, l=0x00, f=0b11000000)


# noinspection PyShadowingNames
def test_code_2e(register):
    """ LD L,d8 """
    cycles = cpu.op.code_2e(register, 0x99)
    assert cycles == 8
    assert_registers(register,l=0x99)


# noinspection PyShadowingNames
def test_code_2f(register):
    """ CPL - Logical complement of register A (i.e. flip all bits) """
    register.A = 0b00111100
    cycles = cpu.op.code_2f(register)
    assert cycles == 4
    assert_registers(register, a=0b11000011, f=0b01100000)


# noinspection PyShadowingNames
def test_code_31(register):
    """ LD SP,d16 - Stores given 16-bit value at SP """
    cycles = cpu.op.code_31(register, 0x9933)
    assert cycles == 12
    assert_registers(register,sp=0x3399)


# noinspection PyShadowingNames
def test_code_32(register):
    """ LD (HL-),A or LD (HLD),A or LDD (HL),A - Put value at A into address HL. Decrement HL """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_33(register):
    """ INC SP - SP=SP+1 """
    register.SP = 0x0000
    cycles = cpu.op.code_33(register)
    assert cycles == 8
    assert_registers(register, sp=0x0001)

    register.SP = 0x00FF
    cycles = cpu.op.code_33(register)
    assert cycles == 8
    assert_registers(register, sp=0x0100)

    register.SP = 0x0FFF
    cycles = cpu.op.code_33(register)
    assert cycles == 8
    assert_registers(register, sp=0x1000)

    register.SP = 0xFFFF
    cycles = cpu.op.code_33(register)
    assert cycles == 8
    assert_registers(register, sp=0x0000)


# noinspection PyShadowingNames
def test_code_34(register):
    """ INC (HL) - (value at address HL)=(value at address HL)+1 """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_35(register):
    """ DEC (HL) - (value at address HL)=(value at address HL)-1 """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_36(register):
    """ LD (HL),d8 - Stores d8 at the address in HL """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_37(register):
    """ SCF - Set carry flag """
    register.F = 0b00000000
    cycles = cpu.op.code_37(register)
    assert cycles == 4
    assert_registers(register, f=0b00010000)

    register.F = 0b11110000
    cycles = cpu.op.code_37(register)
    assert cycles == 4
    assert_registers(register, f=0b10010000)


# noinspection PyShadowingNames
def test_code_39(register):
    """ ADD HL,SP - HL=HL+SP """
    register.set_hl(0x0000)
    register.SP = 0x0001
    cycles = cpu.op.code_39(register)
    assert cycles == 8
    assert_registers(register, sp=0x0001, h=0x00, l=0x01, f=0b00000000)

    register.set_hl(0x000F)
    register.SP = 0x0001
    cycles = cpu.op.code_39(register)
    assert cycles == 8
    assert_registers(register, sp=0x0001, h=0x00, l=0x10, f=0b00000000)

    register.set_hl(0xF000)
    register.SP = 0x1000
    cycles = cpu.op.code_39(register)
    assert cycles == 8
    assert_registers(register, sp=0x1000, h=0x00, l=0x00, f=0b00010000)

    register.set_hl(0x0FFF)
    register.SP = 0x0001
    cycles = cpu.op.code_39(register)
    assert cycles == 8
    assert_registers(register, sp=0x0001, h=0x10, l=0x00, f=0b00100000)

    register.set_hl(0xFFFF)
    register.SP = 0x0001
    cycles = cpu.op.code_39(register)
    assert cycles == 8
    assert_registers(register, sp=0x0001, h=0x00, l=0x00, f=0b00110000)

    register.set_hl(0xFFFF)
    register.SP = 0x0002
    cycles = cpu.op.code_39(register)
    assert cycles == 8
    assert_registers(register, sp=0x0002, h=0x00, l=0x01, f=0b00110000)


# noinspection PyShadowingNames
def test_code_3a(register):
    """ LD A,(HL-) or LD A,(HLD) or LDD A,(HL) - Put value at address HL into A. Decrement HL """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_3b(register):
    """ DEC SP - SP=SP-1 """
    register.SP = 0x0000
    cycles = cpu.op.code_3b(register)
    assert cycles == 8
    assert_registers(register, sp=0xFFFF)

    register.SP = 0x0100
    cycles = cpu.op.code_3b(register)
    assert cycles == 8
    assert_registers(register, sp=0x00FF)

    register.SP = 0x1000
    cycles = cpu.op.code_3b(register)
    assert cycles == 8
    assert_registers(register, sp=0x0FFF)


# noinspection PyShadowingNames
def test_code_3c(register):
    """ INC A - A=A+1 """
    register.A = 0x00
    cycles = cpu.op.code_3c(register)
    assert cycles == 4
    assert_registers(register, a=0x01, f=0b00000000)

    register.A = 0x0F
    cycles = cpu.op.code_3c(register)
    assert cycles == 4
    assert_registers(register, a=0x10, f=0b00100000)

    register.A = 0xF0
    cycles = cpu.op.code_3c(register)
    assert cycles == 4
    assert_registers(register, a=0xF1, f=0b00000000)

    register.A = 0xFF
    cycles = cpu.op.code_3c(register)
    assert cycles == 4
    assert_registers(register, a=0x00, f=0b10100000)


# noinspection PyShadowingNames
def test_code_3e(register):
    """ LD A,d8 """
    cycles = cpu.op.code_3e(register, 0x99)
    assert cycles == 8
    assert_registers(register,a=0x99)


# noinspection PyShadowingNames
def test_code_3f(register):
    """ CCF - Invert carry flag """
    register.F = 0b00010000
    cycles = cpu.op.code_3f(register)
    assert cycles == 4
    assert_registers(register, f=0b00000000)

    register.F = 0b11100000
    cycles = cpu.op.code_3f(register)
    assert cycles == 4
    assert_registers(register, f=0b10010000)


# noinspection PyShadowingNames
def test_code_40(register):
    """ LD B,B (might be a newbie question but... why?) """
    register.B = 0x99
    cycles = cpu.op.code_40(register)
    assert cycles == 4
    assert_registers(register,b=0x99)


# noinspection PyShadowingNames
def test_code_41(register):
    """ LD B,C """
    register.C = 0x99
    cycles = cpu.op.code_41(register)
    assert cycles == 4
    assert_registers(register,b=0x99,c=0x99)


# noinspection PyShadowingNames
def test_code_42(register):
    """ LD B,D """
    register.D = 0x99
    cycles = cpu.op.code_42(register)
    assert cycles == 4
    assert_registers(register,b=0x99,d=0x99)


# noinspection PyShadowingNames
def test_code_43(register):
    """ LD B,E """
    register.E = 0x99
    cycles = cpu.op.code_43(register)
    assert cycles == 4
    assert_registers(register,b=0x99,e=0x99)


# noinspection PyShadowingNames
def test_code_44(register):
    """ LD B,H """
    register.H = 0x99
    cycles = cpu.op.code_44(register)
    assert cycles == 4
    assert_registers(register,b=0x99,h=0x99)


# noinspection PyShadowingNames
def test_code_45(register):
    """ LD B,L """
    register.L = 0x99
    cycles = cpu.op.code_45(register)
    assert cycles == 4
    assert_registers(register,b=0x99,l=0x99)


# noinspection PyShadowingNames
def test_code_46(register):
    """ LD B,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_47(register):
    """ LD B,A """
    register.A = 0x99
    cycles = cpu.op.code_47(register)
    assert cycles == 4
    assert_registers(register,a=0x99,b=0x99)


# noinspection PyShadowingNames
def test_code_48(register):
    """ LD C,B """
    register.B = 0x99
    cycles = cpu.op.code_48(register)
    assert cycles == 4
    assert_registers(register,b=0x99,c=0x99)


# noinspection PyShadowingNames
def test_code_49(register):
    """ LD C,C (might be a newbie question but... why?) """
    register.C = 0x99
    cycles = cpu.op.code_49(register)
    assert cycles == 4
    assert_registers(register,c=0x99)


# noinspection PyShadowingNames
def test_code_4a(register):
    """ LD C,D """
    register.D = 0x99
    cycles = cpu.op.code_4a(register)
    assert cycles == 4
    assert_registers(register,c=0x99,d=0x99)


# noinspection PyShadowingNames
def test_code_4b(register):
    """ LD C,E """
    register.E = 0x99
    cycles = cpu.op.code_4b(register)
    assert cycles == 4
    assert_registers(register,c=0x99,e=0x99)


# noinspection PyShadowingNames
def test_code_4c(register):
    """ LD C,H """
    register.H = 0x99
    cycles = cpu.op.code_4c(register)
    assert cycles == 4
    assert_registers(register,c=0x99,h=0x99)


# noinspection PyShadowingNames
def test_code_4d(register):
    """ LD C,L """
    register.L = 0x99
    cycles = cpu.op.code_4d(register)
    assert cycles == 4
    assert_registers(register,c=0x99,l=0x99)


# noinspection PyShadowingNames
def test_code_4e(register):
    """ LD C,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_4f(register):
    """ LD C,A """
    register.A = 0x99
    cycles = cpu.op.code_4f(register)
    assert cycles == 4
    assert_registers(register,a=0x99,c=0x99)


# noinspection PyShadowingNames
def test_code_50(register):
    """ LD D,B """
    register.B = 0x99
    cycles = cpu.op.code_50(register)
    assert cycles == 4
    assert_registers(register,b=0x99,d=0x99)


# noinspection PyShadowingNames
def test_code_51(register):
    """ LD D,C """
    register.C = 0x99
    cycles = cpu.op.code_51(register)
    assert cycles == 4
    assert_registers(register,c=0x99,d=0x99)


# noinspection PyShadowingNames
def test_code_52(register):
    """ LD D,D (might be a newbie question but... why?) """
    register.D = 0x99
    cycles = cpu.op.code_52(register)
    assert cycles == 4
    assert_registers(register,d=0x99)


# noinspection PyShadowingNames
def test_code_53(register):
    """ LD D,E """
    register.E = 0x99
    cycles = cpu.op.code_53(register)
    assert cycles == 4
    assert_registers(register,d=0x99,e=0x99)


# noinspection PyShadowingNames
def test_code_54(register):
    """ LD D,H """
    register.H = 0x99
    cycles = cpu.op.code_54(register)
    assert cycles == 4
    assert_registers(register,d=0x99,h=0x99)


# noinspection PyShadowingNames
def test_code_55(register):
    """ LD D,L """
    register.L = 0x99
    cycles = cpu.op.code_55(register)
    assert cycles == 4
    assert_registers(register,d=0x99,l=0x99)


# noinspection PyShadowingNames
def test_code_56(register):
    """ LD D,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_57(register):
    """ LD D,A """
    register.A = 0x99
    cycles = cpu.op.code_57(register)
    assert cycles == 4
    assert_registers(register,a=0x99,d=0x99)


# noinspection PyShadowingNames
def test_code_58(register):
    """ LD E,B """
    register.B = 0x99
    cycles = cpu.op.code_58(register)
    assert cycles == 4
    assert_registers(register,b=0x99,e=0x99)


# noinspection PyShadowingNames
def test_code_59(register):
    """ LD E,C """
    register.C = 0x99
    cycles = cpu.op.code_59(register)
    assert cycles == 4
    assert_registers(register,c=0x99,e=0x99)


# noinspection PyShadowingNames
def test_code_5a(register):
    """ LD E,D """
    register.D = 0x99
    cycles = cpu.op.code_5a(register)
    assert cycles == 4
    assert_registers(register,d=0x99,e=0x99)


# noinspection PyShadowingNames
def test_code_5b(register):
    """ LD E,E (might be a newbie question but... why?) """
    register.E = 0x99
    cycles = cpu.op.code_5b(register)
    assert cycles == 4
    assert_registers(register,e=0x99)


# noinspection PyShadowingNames
def test_code_5c(register):
    """ LD E,H """
    register.H = 0x99
    cycles = cpu.op.code_5c(register)
    assert cycles == 4
    assert_registers(register,e=0x99,h=0x99)


# noinspection PyShadowingNames
def test_code_5d(register):
    """ LD E,L """
    register.L = 0x99
    cycles = cpu.op.code_5d(register)
    assert cycles == 4
    assert_registers(register,e=0x99,l=0x99)


# noinspection PyShadowingNames
def test_code_5e(register):
    """ LD E,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_5f(register):
    """ LD E,A """
    register.A = 0x99
    cycles = cpu.op.code_5f(register)
    assert cycles == 4
    assert_registers(register,a=0x99,e=0x99)


# noinspection PyShadowingNames
def test_code_60(register):
    """ LD H,B """
    register.B = 0x99
    cycles = cpu.op.code_60(register)
    assert cycles == 4
    assert_registers(register, b=0x99, h=0x99)


# noinspection PyShadowingNames
def test_code_61(register):
    """ LD H,C """
    register.C = 0x99
    cycles = cpu.op.code_61(register)
    assert cycles == 4
    assert_registers(register, c=0x99, h=0x99)


# noinspection PyShadowingNames
def test_code_62(register):
    """ LD H,D """
    register.D = 0x99
    cycles = cpu.op.code_62(register)
    assert cycles == 4
    assert_registers(register, d=0x99, h=0x99)


# noinspection PyShadowingNames
def test_code_63(register):
    """ LD H,E """
    register.E = 0x99
    cycles = cpu.op.code_63(register)
    assert cycles == 4
    assert_registers(register, e=0x99, h=0x99)


# noinspection PyShadowingNames
def test_code_64(register):
    """ LD H,H (might be a newbie question but... why?) """
    register.H = 0x99
    cycles = cpu.op.code_64(register)
    assert cycles == 4
    assert_registers(register, h=0x99)


# noinspection PyShadowingNames
def test_code_65(register):
    """ LD H,L """
    register.L = 0x99
    cycles = cpu.op.code_65(register)
    assert cycles == 4
    assert_registers(register, h=0x99, l=0x99)


# noinspection PyShadowingNames
def test_code_66(register):
    """ LD H,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_67(register):
    """ LD H,A """
    register.A = 0x99
    cycles = cpu.op.code_67(register)
    assert cycles == 4
    assert_registers(register, a=0x99, h=0x99)


# noinspection PyShadowingNames
def test_code_68(register):
    """ LD L,B """
    register.B = 0x99
    cycles = cpu.op.code_68(register)
    assert cycles == 4
    assert_registers(register, b=0x99, l=0x99)


# noinspection PyShadowingNames
def test_code_69(register):
    """ LD L,C """
    register.C = 0x99
    cycles = cpu.op.code_69(register)
    assert cycles == 4
    assert_registers(register, c=0x99, l=0x99)


# noinspection PyShadowingNames
def test_code_6a(register):
    """ LD L,D """
    register.D = 0x99
    cycles = cpu.op.code_6a(register)
    assert cycles == 4
    assert_registers(register, d=0x99, l=0x99)


# noinspection PyShadowingNames
def test_code_6b(register):
    """ LD L,E """
    register.E = 0x99
    cycles = cpu.op.code_6b(register)
    assert cycles == 4
    assert_registers(register, e=0x99, l=0x99)


# noinspection PyShadowingNames
def test_code_6c(register):
    """ LD L,H """
    register.H = 0x99
    cycles = cpu.op.code_6c(register)
    assert cycles == 4
    assert_registers(register, h=0x99, l=0x99)


# noinspection PyShadowingNames
def test_code_6d(register):
    """ LD L,L (might be a newbie question but... why?) """
    register.L = 0x99
    cycles = cpu.op.code_6d(register)
    assert cycles == 4
    assert_registers(register, l=0x99)


# noinspection PyShadowingNames
def test_code_6e(register):
    """ LD L,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_6f(register):
    """ LD L,A """
    register.A = 0x99
    cycles = cpu.op.code_6f(register)
    assert cycles == 4
    assert_registers(register, a=0x99, l=0x99)


# noinspection PyShadowingNames
def test_code_70(register):
    """ LD (HL),B - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_71(register):
    """ LD (HL),C - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_72(register):
    """ LD (HL),D - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_73(register):
    """ LD (HL),E - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_74(register):
    """ LD (HL),H - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_75(register):
    """ LD (HL),L - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_76(register):
    """
    HALT - Power down CPU (by stopping the system clock) until an interrupt occurs
    See: http://gbdev.gg8.se/wiki/articles/Reducing_Power_Consumption
    """
    # TODO after cpu and interrupts are implemented
    pass


# noinspection PyShadowingNames
def test_code_77(register):
    """ LD (HL),A - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_78(register):
    """ LD A,B """
    register.B = 0x99
    cycles = cpu.op.code_78(register)
    assert cycles == 4
    assert_registers(register, a=0x99, b=0x99)


# noinspection PyShadowingNames
def test_code_79(register):
    """ LD A,C """
    register.C = 0x99
    cycles = cpu.op.code_79(register)
    assert cycles == 4
    assert_registers(register, a=0x99, c=0x99)


# noinspection PyShadowingNames
def test_code_7a(register):
    """ LD A,D """
    register.D = 0x99
    cycles = cpu.op.code_7a(register)
    assert cycles == 4
    assert_registers(register, a=0x99, d=0x99)


# noinspection PyShadowingNames
def test_code_7b(register):
    """ LD A,E """
    register.E = 0x99
    cycles = cpu.op.code_7b(register)
    assert cycles == 4
    assert_registers(register, a=0x99, e=0x99)


# noinspection PyShadowingNames
def test_code_7c(register):
    """ LD A,H """
    register.H = 0x99
    cycles = cpu.op.code_7c(register)
    assert cycles == 4
    assert_registers(register, a=0x99, h=0x99)


# noinspection PyShadowingNames
def test_code_7d(register):
    """ LD A,L """
    register.L = 0x99
    cycles = cpu.op.code_7d(register)
    assert cycles == 4
    assert_registers(register, a=0x99, l=0x99)


# noinspection PyShadowingNames
def test_code_7e(register):
    """ LD A,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_7f(register):
    """ LD A,A (might be a newbie question but... why?) """
    register.A = 0x99
    cycles = cpu.op.code_7f(register)
    assert cycles == 4
    assert_registers(register, a=0x99)


# noinspection PyShadowingNames
def test_code_80(register):
    """ ADD A,B - A=A+B """
    register.A = 0x00
    register.B = 0x00
    cycles = cpu.op.code_80(register)
    assert cycles == 4
    assert_registers(register, a=0x00, b=0x00, f=0b10000000)

    register.A = 0x00
    register.B = 0x01
    cycles = cpu.op.code_80(register)
    assert cycles == 4
    assert_registers(register, a=0x01, b=0x01, f=0b00000000)

    register.A = 0x0F
    register.B = 0x01
    cycles = cpu.op.code_80(register)
    assert cycles == 4
    assert_registers(register, a=0x10, b=0x01, f=0b00100000)

    register.A = 0xF0
    register.B = 0x10
    cycles = cpu.op.code_80(register)
    assert cycles == 4
    assert_registers(register, a=0x00, b=0x10, f=0b10010000)

    register.A = 0xFF
    register.B = 0x01
    cycles = cpu.op.code_80(register)
    assert cycles == 4
    assert_registers(register, a=0x00, b=0x01, f=0b10110000)

    register.A = 0xFF
    register.B = 0x02
    cycles = cpu.op.code_80(register)
    assert cycles == 4
    assert_registers(register, a=0x01, b=0x02, f=0b00110000)


# noinspection PyShadowingNames
def test_code_81(register):
    """ ADD A,C - A=A+C """
    register.A = 0x00
    register.C = 0x00
    cycles = cpu.op.code_81(register)
    assert cycles == 4
    assert_registers(register, a=0x00, c=0x00, f=0b10000000)

    register.A = 0x00
    register.C = 0x01
    cycles = cpu.op.code_81(register)
    assert cycles == 4
    assert_registers(register, a=0x01, c=0x01, f=0b00000000)

    register.A = 0x0F
    register.C = 0x01
    cycles = cpu.op.code_81(register)
    assert cycles == 4
    assert_registers(register, a=0x10, c=0x01, f=0b00100000)

    register.A = 0xF0
    register.C = 0x10
    cycles = cpu.op.code_81(register)
    assert cycles == 4
    assert_registers(register, a=0x00, c=0x10, f=0b10010000)

    register.A = 0xFF
    register.C = 0x01
    cycles = cpu.op.code_81(register)
    assert cycles == 4
    assert_registers(register, a=0x00, c=0x01, f=0b10110000)

    register.A = 0xFF
    register.C = 0x02
    cycles = cpu.op.code_81(register)
    assert cycles == 4
    assert_registers(register, a=0x01, c=0x02, f=0b00110000)


# noinspection PyShadowingNames
def test_code_82(register):
    """ ADD A,D - A=A+D """
    register.A = 0x00
    register.D = 0x00
    cycles = cpu.op.code_82(register)
    assert cycles == 4
    assert_registers(register, a=0x00, d=0x00, f=0b10000000)

    register.A = 0x00
    register.D = 0x01
    cycles = cpu.op.code_82(register)
    assert cycles == 4
    assert_registers(register, a=0x01, d=0x01, f=0b00000000)

    register.A = 0x0F
    register.D = 0x01
    cycles = cpu.op.code_82(register)
    assert cycles == 4
    assert_registers(register, a=0x10, d=0x01, f=0b00100000)

    register.A = 0xF0
    register.D = 0x10
    cycles = cpu.op.code_82(register)
    assert cycles == 4
    assert_registers(register, a=0x00, d=0x10, f=0b10010000)

    register.A = 0xFF
    register.D = 0x01
    cycles = cpu.op.code_82(register)
    assert cycles == 4
    assert_registers(register, a=0x00, d=0x01, f=0b10110000)

    register.A = 0xFF
    register.D = 0x02
    cycles = cpu.op.code_82(register)
    assert cycles == 4
    assert_registers(register, a=0x01, d=0x02, f=0b00110000)


# noinspection PyShadowingNames
def test_code_83(register):
    """ ADD A,E - A=A+E """
    register.A = 0x00
    register.E = 0x00
    cycles = cpu.op.code_83(register)
    assert cycles == 4
    assert_registers(register, a=0x00, e=0x00, f=0b10000000)

    register.A = 0x00
    register.E = 0x01
    cycles = cpu.op.code_83(register)
    assert cycles == 4
    assert_registers(register, a=0x01, e=0x01, f=0b00000000)

    register.A = 0x0F
    register.E = 0x01
    cycles = cpu.op.code_83(register)
    assert cycles == 4
    assert_registers(register, a=0x10, e=0x01, f=0b00100000)

    register.A = 0xF0
    register.E = 0x10
    cycles = cpu.op.code_83(register)
    assert cycles == 4
    assert_registers(register, a=0x00, e=0x10, f=0b10010000)

    register.A = 0xFF
    register.E = 0x01
    cycles = cpu.op.code_83(register)
    assert cycles == 4
    assert_registers(register, a=0x00, e=0x01, f=0b10110000)

    register.A = 0xFF
    register.E = 0x02
    cycles = cpu.op.code_83(register)
    assert cycles == 4
    assert_registers(register, a=0x01, e=0x02, f=0b00110000)


# noinspection PyShadowingNames
def test_code_84(register):
    """ ADD A,H - A=A+H """
    register.A = 0x00
    register.H = 0x00
    cycles = cpu.op.code_84(register)
    assert cycles == 4
    assert_registers(register, a=0x00, h=0x00, f=0b10000000)

    register.A = 0x00
    register.H = 0x01
    cycles = cpu.op.code_84(register)
    assert cycles == 4
    assert_registers(register, a=0x01, h=0x01, f=0b00000000)

    register.A = 0x0F
    register.H = 0x01
    cycles = cpu.op.code_84(register)
    assert cycles == 4
    assert_registers(register, a=0x10, h=0x01, f=0b00100000)

    register.A = 0xF0
    register.H = 0x10
    cycles = cpu.op.code_84(register)
    assert cycles == 4
    assert_registers(register, a=0x00, h=0x10, f=0b10010000)

    register.A = 0xFF
    register.H = 0x01
    cycles = cpu.op.code_84(register)
    assert cycles == 4
    assert_registers(register, a=0x00, h=0x01, f=0b10110000)

    register.A = 0xFF
    register.H = 0x02
    cycles = cpu.op.code_84(register)
    assert cycles == 4
    assert_registers(register, a=0x01, h=0x02, f=0b00110000)


# noinspection PyShadowingNames
def test_code_85(register):
    """ ADD A,L - A=A+L """
    register.A = 0x00
    register.L = 0x00
    cycles = cpu.op.code_85(register)
    assert cycles == 4
    assert_registers(register, a=0x00, l=0x00, f=0b10000000)

    register.A = 0x00
    register.L = 0x01
    cycles = cpu.op.code_85(register)
    assert cycles == 4
    assert_registers(register, a=0x01, l=0x01, f=0b00000000)

    register.A = 0x0F
    register.L = 0x01
    cycles = cpu.op.code_85(register)
    assert cycles == 4
    assert_registers(register, a=0x10, l=0x01, f=0b00100000)

    register.A = 0xF0
    register.L = 0x10
    cycles = cpu.op.code_85(register)
    assert cycles == 4
    assert_registers(register, a=0x00, l=0x10, f=0b10010000)

    register.A = 0xFF
    register.L = 0x01
    cycles = cpu.op.code_85(register)
    assert cycles == 4
    assert_registers(register, a=0x00, l=0x01, f=0b10110000)

    register.A = 0xFF
    register.L = 0x02
    cycles = cpu.op.code_85(register)
    assert cycles == 4
    assert_registers(register, a=0x01, l=0x02, f=0b00110000)


# noinspection PyShadowingNames
def test_code_86(register):
    """ ADD A,(HL) - A=A+(value at address HL) """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_87(register):
    """ ADD A,A - A=A+A """
    register.A = 0x00
    cycles = cpu.op.code_87(register)
    assert cycles == 4
    assert_registers(register, a=0x00, f=0b10000000)

    register.A = 0x01
    cycles = cpu.op.code_87(register)
    assert cycles == 4
    assert_registers(register, a=0x02, f=0b00000000)

    register.A = 0x08
    cycles = cpu.op.code_87(register)
    assert cycles == 4
    assert_registers(register, a=0x10, f=0b00100000)

    register.A = 0x80
    cycles = cpu.op.code_87(register)
    assert cycles == 4
    assert_registers(register, a=0x00, f=0b10010000)

    register.A = 0x88
    cycles = cpu.op.code_87(register)
    assert cycles == 4
    assert_registers(register, a=0x10, f=0b00110000)


# noinspection PyShadowingNames
def test_code_88(register):
    """ ADC A,B - A=A+B+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    register.A = 0x00
    register.B = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_88(register)
    assert cycles == 4
    assert_registers(register, a=0x00, b=0x00, f=0b10000000)

    register.A = 0x00
    register.B = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_88(register)
    assert cycles == 4
    assert_registers(register, a=0x01, b=0x00, f=0b00000000)

    register.A = 0x00
    register.B = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_88(register)
    assert cycles == 4
    assert_registers(register, a=0x02, b=0x01, f=0b00000000)

    register.A = 0x0E
    register.B = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_88(register)
    assert cycles == 4
    assert_registers(register, a=0x10, b=0x01, f=0b00100000)

    register.A = 0xF0
    register.B = 0x0F
    register.F = 0b00010000
    cycles = cpu.op.code_88(register)
    assert cycles == 4
    assert_registers(register, a=0x00, b=0x0F, f=0b10110000)

    register.A = 0xFE
    register.B = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_88(register)
    assert cycles == 4
    assert_registers(register, a=0x00, b=0x01, f=0b10110000)

    register.A = 0xFE
    register.B = 0x02
    register.F = 0b00010000
    cycles = cpu.op.code_88(register)
    assert cycles == 4
    assert_registers(register, a=0x01, b=0x02, f=0b00110000)


# noinspection PyShadowingNames
def test_code_89(register):
    """ ADC A,C - A=A+C+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    register.A = 0x00
    register.C = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_89(register)
    assert cycles == 4
    assert_registers(register, a=0x00, c=0x00, f=0b10000000)

    register.A = 0x00
    register.C = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_89(register)
    assert cycles == 4
    assert_registers(register, a=0x01, c=0x00, f=0b00000000)

    register.A = 0x00
    register.C = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_89(register)
    assert cycles == 4
    assert_registers(register, a=0x02, c=0x01, f=0b00000000)

    register.A = 0x0E
    register.C = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_89(register)
    assert cycles == 4
    assert_registers(register, a=0x10, c=0x01, f=0b00100000)

    register.A = 0xF0
    register.C = 0x0F
    register.F = 0b00010000
    cycles = cpu.op.code_89(register)
    assert cycles == 4
    assert_registers(register, a=0x00, c=0x0F, f=0b10110000)

    register.A = 0xFE
    register.C = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_89(register)
    assert cycles == 4
    assert_registers(register, a=0x00, c=0x01, f=0b10110000)

    register.A = 0xFE
    register.C = 0x02
    register.F = 0b00010000
    cycles = cpu.op.code_89(register)
    assert cycles == 4
    assert_registers(register, a=0x01, c=0x02, f=0b00110000)


# noinspection PyShadowingNames
def test_code_8a(register):
    """ ADC A,D - A=A+D+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    register.A = 0x00
    register.D = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_8a(register)
    assert cycles == 4
    assert_registers(register, a=0x00, d=0x00, f=0b10000000)

    register.A = 0x00
    register.D = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_8a(register)
    assert cycles == 4
    assert_registers(register, a=0x01, d=0x00, f=0b00000000)

    register.A = 0x00
    register.D = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_8a(register)
    assert cycles == 4
    assert_registers(register, a=0x02, d=0x01, f=0b00000000)

    register.A = 0x0E
    register.D = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_8a(register)
    assert cycles == 4
    assert_registers(register, a=0x10, d=0x01, f=0b00100000)

    register.A = 0xF0
    register.D = 0x0F
    register.F = 0b00010000
    cycles = cpu.op.code_8a(register)
    assert cycles == 4
    assert_registers(register, a=0x00, d=0x0F, f=0b10110000)

    register.A = 0xFE
    register.D = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_8a(register)
    assert cycles == 4
    assert_registers(register, a=0x00, d=0x01, f=0b10110000)

    register.A = 0xFE
    register.D = 0x02
    register.F = 0b00010000
    cycles = cpu.op.code_8a(register)
    assert cycles == 4
    assert_registers(register, a=0x01, d=0x02, f=0b00110000)


# noinspection PyShadowingNames
def test_code_8b(register):
    """ ADC A,E - A=A+E+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    register.A = 0x00
    register.E = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_8b(register)
    assert cycles == 4
    assert_registers(register, a=0x00, e=0x00, f=0b10000000)

    register.A = 0x00
    register.E = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_8b(register)
    assert cycles == 4
    assert_registers(register, a=0x01, e=0x00, f=0b00000000)

    register.A = 0x00
    register.E = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_8b(register)
    assert cycles == 4
    assert_registers(register, a=0x02, e=0x01, f=0b00000000)

    register.A = 0x0E
    register.E = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_8b(register)
    assert cycles == 4
    assert_registers(register, a=0x10, e=0x01, f=0b00100000)

    register.A = 0xF0
    register.E = 0x0F
    register.F = 0b00010000
    cycles = cpu.op.code_8b(register)
    assert cycles == 4
    assert_registers(register, a=0x00, e=0x0F, f=0b10110000)

    register.A = 0xFE
    register.E = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_8b(register)
    assert cycles == 4
    assert_registers(register, a=0x00, e=0x01, f=0b10110000)

    register.A = 0xFE
    register.E = 0x02
    register.F = 0b00010000
    cycles = cpu.op.code_8b(register)
    assert cycles == 4
    assert_registers(register, a=0x01, e=0x02, f=0b00110000)


# noinspection PyShadowingNames
def test_code_8c(register):
    """ ADC A,H - A=A+H+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    register.A = 0x00
    register.H = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_8c(register)
    assert cycles == 4
    assert_registers(register, a=0x00, h=0x00, f=0b10000000)

    register.A = 0x00
    register.H = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_8c(register)
    assert cycles == 4
    assert_registers(register, a=0x01, h=0x00, f=0b00000000)

    register.A = 0x00
    register.H = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_8c(register)
    assert cycles == 4
    assert_registers(register, a=0x02, h=0x01, f=0b00000000)

    register.A = 0x0E
    register.H = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_8c(register)
    assert cycles == 4
    assert_registers(register, a=0x10, h=0x01, f=0b00100000)

    register.A = 0xF0
    register.H = 0x0F
    register.F = 0b00010000
    cycles = cpu.op.code_8c(register)
    assert cycles == 4
    assert_registers(register, a=0x00, h=0x0F, f=0b10110000)

    register.A = 0xFE
    register.H = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_8c(register)
    assert cycles == 4
    assert_registers(register, a=0x00, h=0x01, f=0b10110000)

    register.A = 0xFE
    register.H = 0x02
    register.F = 0b00010000
    cycles = cpu.op.code_8c(register)
    assert cycles == 4
    assert_registers(register, a=0x01, h=0x02, f=0b00110000)


# noinspection PyShadowingNames
def test_code_8d(register):
    """ ADC A,L - A=A+L+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    register.A = 0x00
    register.L = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_8d(register)
    assert cycles == 4
    assert_registers(register, a=0x00, l=0x00, f=0b10000000)

    register.A = 0x00
    register.L = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_8d(register)
    assert cycles == 4
    assert_registers(register, a=0x01, l=0x00, f=0b00000000)

    register.A = 0x00
    register.L = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_8d(register)
    assert cycles == 4
    assert_registers(register, a=0x02, l=0x01, f=0b00000000)

    register.A = 0x0E
    register.L = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_8d(register)
    assert cycles == 4
    assert_registers(register, a=0x10, l=0x01, f=0b00100000)

    register.A = 0xF0
    register.L = 0x0F
    register.F = 0b00010000
    cycles = cpu.op.code_8d(register)
    assert cycles == 4
    assert_registers(register, a=0x00, l=0x0F, f=0b10110000)

    register.A = 0xFE
    register.L = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_8d(register)
    assert cycles == 4
    assert_registers(register, a=0x00, l=0x01, f=0b10110000)

    register.A = 0xFE
    register.L = 0x02
    register.F = 0b00010000
    cycles = cpu.op.code_8d(register)
    assert cycles == 4
    assert_registers(register, a=0x01, l=0x02, f=0b00110000)


# noinspection PyShadowingNames
def test_code_8e(register):
    """ ADC A,(HL) - A=A+(value at address HL)+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_8f(register):
    """ ADC A,A - A=A+A+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    register.A = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_8f(register)
    assert cycles == 4
    assert_registers(register, a=0x00, f=0b10000000)

    register.A = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_8f(register)
    assert cycles == 4
    assert_registers(register, a=0x01, f=0b00000000)

    register.A = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_8f(register)
    assert cycles == 4
    assert_registers(register, a=0x03, f=0b00000000)

    register.A = 0x08
    register.F = 0b00010000
    cycles = cpu.op.code_8f(register)
    assert cycles == 4
    assert_registers(register, a=0x11, f=0b00100000)

    register.A = 0x80
    register.F = 0b00000000
    cycles = cpu.op.code_8f(register)
    assert cycles == 4
    assert_registers(register, a=0x00, f=0b10010000)

    register.A = 0x80
    register.F = 0b00010000
    cycles = cpu.op.code_8f(register)
    assert cycles == 4
    assert_registers(register, a=0x01, f=0b00010000)

    register.A = 0xFF
    register.F = 0b00010000
    cycles = cpu.op.code_8f(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, f=0b00110000)


# noinspection PyShadowingNames
def test_code_90(register):
    """ SUB A,B - A=A-B """
    register.A = 0x00
    register.B = 0x00
    cycles = cpu.op.code_90(register)
    assert cycles == 4
    assert_registers(register, a=0x00, b=0x00, f=0b11000000)

    register.A = 0x00
    register.B = 0x01
    cycles = cpu.op.code_90(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, b=0x01, f=0b01110000)

    register.A = 0x0F
    register.B = 0x01
    cycles = cpu.op.code_90(register)
    assert cycles == 4
    assert_registers(register, a=0x0E, b=0x01, f=0b01000000)

    register.A = 0xF0
    register.B = 0x10
    cycles = cpu.op.code_90(register)
    assert cycles == 4
    assert_registers(register, a=0xE0, b=0x10, f=0b01000000)

    register.A = 0xFF
    register.B = 0x01
    cycles = cpu.op.code_90(register)
    assert cycles == 4
    assert_registers(register, a=0xFE, b=0x01, f=0b01000000)

    register.A = 0xFF
    register.B = 0xFE
    cycles = cpu.op.code_90(register)
    assert cycles == 4
    assert_registers(register, a=0x01, b=0xFE, f=0b01000000)


# noinspection PyShadowingNames
def test_code_91(register):
    """ SUB A,C - A=A-C """
    register.A = 0x00
    register.C = 0x00
    cycles = cpu.op.code_91(register)
    assert cycles == 4
    assert_registers(register, a=0x00, c=0x00, f=0b11000000)

    register.A = 0x00
    register.C = 0x01
    cycles = cpu.op.code_91(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, c=0x01, f=0b01110000)

    register.A = 0x0F
    register.C = 0x01
    cycles = cpu.op.code_91(register)
    assert cycles == 4
    assert_registers(register, a=0x0E, c=0x01, f=0b01000000)

    register.A = 0xF0
    register.C = 0x10
    cycles = cpu.op.code_91(register)
    assert cycles == 4
    assert_registers(register, a=0xE0, c=0x10, f=0b01000000)

    register.A = 0xFF
    register.C = 0x01
    cycles = cpu.op.code_91(register)
    assert cycles == 4
    assert_registers(register, a=0xFE, c=0x01, f=0b01000000)

    register.A = 0xFF
    register.C = 0xFE
    cycles = cpu.op.code_91(register)
    assert cycles == 4
    assert_registers(register, a=0x01, c=0xFE, f=0b01000000)


# noinspection PyShadowingNames
def test_code_92(register):
    """ SUB A,D - A=A-D """
    register.A = 0x00
    register.D = 0x00
    cycles = cpu.op.code_92(register)
    assert cycles == 4
    assert_registers(register, a=0x00, d=0x00, f=0b11000000)

    register.A = 0x00
    register.D = 0x01
    cycles = cpu.op.code_92(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, d=0x01, f=0b01110000)

    register.A = 0x0F
    register.D = 0x01
    cycles = cpu.op.code_92(register)
    assert cycles == 4
    assert_registers(register, a=0x0E, d=0x01, f=0b01000000)

    register.A = 0xF0
    register.D = 0x10
    cycles = cpu.op.code_92(register)
    assert cycles == 4
    assert_registers(register, a=0xE0, d=0x10, f=0b01000000)

    register.A = 0xFF
    register.D = 0x01
    cycles = cpu.op.code_92(register)
    assert cycles == 4
    assert_registers(register, a=0xFE, d=0x01, f=0b01000000)

    register.A = 0xFF
    register.D = 0xFE
    cycles = cpu.op.code_92(register)
    assert cycles == 4
    assert_registers(register, a=0x01, d=0xFE, f=0b01000000)


# noinspection PyShadowingNames
def test_code_93(register):
    """ SUB A,E - A=A-E """
    register.A = 0x00
    register.E = 0x00
    cycles = cpu.op.code_93(register)
    assert cycles == 4
    assert_registers(register, a=0x00, e=0x00, f=0b11000000)

    register.A = 0x00
    register.E = 0x01
    cycles = cpu.op.code_93(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, e=0x01, f=0b01110000)

    register.A = 0x0F
    register.E = 0x01
    cycles = cpu.op.code_93(register)
    assert cycles == 4
    assert_registers(register, a=0x0E, e=0x01, f=0b01000000)

    register.A = 0xF0
    register.E = 0x10
    cycles = cpu.op.code_93(register)
    assert cycles == 4
    assert_registers(register, a=0xE0, e=0x10, f=0b01000000)

    register.A = 0xFF
    register.E = 0x01
    cycles = cpu.op.code_93(register)
    assert cycles == 4
    assert_registers(register, a=0xFE, e=0x01, f=0b01000000)

    register.A = 0xFF
    register.E = 0xFE
    cycles = cpu.op.code_93(register)
    assert cycles == 4
    assert_registers(register, a=0x01, e=0xFE, f=0b01000000)


# noinspection PyShadowingNames
def test_code_94(register):
    """ SUB A,H - A=A-H """
    register.A = 0x00
    register.H = 0x00
    cycles = cpu.op.code_94(register)
    assert cycles == 4
    assert_registers(register, a=0x00, h=0x00, f=0b11000000)

    register.A = 0x00
    register.H = 0x01
    cycles = cpu.op.code_94(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, h=0x01, f=0b01110000)

    register.A = 0x0F
    register.H = 0x01
    cycles = cpu.op.code_94(register)
    assert cycles == 4
    assert_registers(register, a=0x0E, h=0x01, f=0b01000000)

    register.A = 0xF0
    register.H = 0x10
    cycles = cpu.op.code_94(register)
    assert cycles == 4
    assert_registers(register, a=0xE0, h=0x10, f=0b01000000)

    register.A = 0xFF
    register.H = 0x01
    cycles = cpu.op.code_94(register)
    assert cycles == 4
    assert_registers(register, a=0xFE, h=0x01, f=0b01000000)

    register.A = 0xFF
    register.H = 0xFE
    cycles = cpu.op.code_94(register)
    assert cycles == 4
    assert_registers(register, a=0x01, h=0xFE, f=0b01000000)


# noinspection PyShadowingNames
def test_code_95(register):
    """ SUB A,L - A=A-L """
    register.A = 0x00
    register.L = 0x00
    cycles = cpu.op.code_95(register)
    assert cycles == 4
    assert_registers(register, a=0x00, l=0x00, f=0b11000000)

    register.A = 0x00
    register.L = 0x01
    cycles = cpu.op.code_95(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, l=0x01, f=0b01110000)

    register.A = 0x0F
    register.L = 0x01
    cycles = cpu.op.code_95(register)
    assert cycles == 4
    assert_registers(register, a=0x0E, l=0x01, f=0b01000000)

    register.A = 0xF0
    register.L = 0x10
    cycles = cpu.op.code_95(register)
    assert cycles == 4
    assert_registers(register, a=0xE0, l=0x10, f=0b01000000)

    register.A = 0xFF
    register.L = 0x01
    cycles = cpu.op.code_95(register)
    assert cycles == 4
    assert_registers(register, a=0xFE, l=0x01, f=0b01000000)

    register.A = 0xFF
    register.L = 0xFE
    cycles = cpu.op.code_95(register)
    assert cycles == 4
    assert_registers(register, a=0x01, l=0xFE, f=0b01000000)


# noinspection PyShadowingNames
def test_code_96(register):
    """ SUB A,(HL) - A=A-(value at address HL) """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_97(register):
    """ SUB A,A - A=A-A """
    register.A = 0x00
    cycles = cpu.op.code_97(register)
    assert cycles == 4
    assert_registers(register, a=0x00, f=0b11000000)

    register.A = 0x01
    cycles = cpu.op.code_97(register)
    assert cycles == 4
    assert_registers(register, a=0x00, f=0b11000000)

    register.A = 0xFF
    cycles = cpu.op.code_97(register)
    assert cycles == 4
    assert_registers(register, a=0x00, f=0b11000000)


# noinspection PyShadowingNames
def test_code_98(register):
    """ SBC A,B - A=A-B-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    register.A = 0x00
    register.B = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_98(register)
    assert cycles == 4
    assert_registers(register, a=0x00, b=0x00, f=0b11000000)

    register.A = 0x02
    register.B = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_98(register)
    assert cycles == 4
    assert_registers(register, a=0x01, b=0x00, f=0b01000000)

    register.A = 0x00
    register.B = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_98(register)
    assert cycles == 4
    assert_registers(register, a=0xFE, b=0x01, f=0b01110000)

    register.A = 0x13
    register.B = 0x04
    register.F = 0b00010000
    cycles = cpu.op.code_98(register)
    assert cycles == 4
    assert_registers(register, a=0x0E, b=0x04, f=0b01100000)


# noinspection PyShadowingNames
def test_code_99(register):
    """ SBC A,C - A=A-C-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    register.A = 0x00
    register.C = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_99(register)
    assert cycles == 4
    assert_registers(register, a=0x00, c=0x00, f=0b11000000)

    register.A = 0x02
    register.C = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_99(register)
    assert cycles == 4
    assert_registers(register, a=0x01, c=0x00, f=0b01000000)

    register.A = 0x00
    register.C = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_99(register)
    assert cycles == 4
    assert_registers(register, a=0xFE, c=0x01, f=0b01110000)

    register.A = 0x13
    register.C = 0x04
    register.F = 0b00010000
    cycles = cpu.op.code_99(register)
    assert cycles == 4
    assert_registers(register, a=0x0E, c=0x04, f=0b01100000)


# noinspection PyShadowingNames
def test_code_9a(register):
    """ SBC A,D - A=A-D-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    register.A = 0x00
    register.D = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_9a(register)
    assert cycles == 4
    assert_registers(register, a=0x00, d=0x00, f=0b11000000)

    register.A = 0x02
    register.D = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_9a(register)
    assert cycles == 4
    assert_registers(register, a=0x01, d=0x00, f=0b01000000)

    register.A = 0x00
    register.D = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_9a(register)
    assert cycles == 4
    assert_registers(register, a=0xFE, d=0x01, f=0b01110000)

    register.A = 0x13
    register.D = 0x04
    register.F = 0b00010000
    cycles = cpu.op.code_9a(register)
    assert cycles == 4
    assert_registers(register, a=0x0E, d=0x04, f=0b01100000)


# noinspection PyShadowingNames
def test_code_9b(register):
    """ SBC A,E - A=A-E-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    register.A = 0x00
    register.E = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_9b(register)
    assert cycles == 4
    assert_registers(register, a=0x00, e=0x00, f=0b11000000)

    register.A = 0x02
    register.E = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_9b(register)
    assert cycles == 4
    assert_registers(register, a=0x01, e=0x00, f=0b01000000)

    register.A = 0x00
    register.E = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_9b(register)
    assert cycles == 4
    assert_registers(register, a=0xFE, e=0x01, f=0b01110000)

    register.A = 0x13
    register.E = 0x04
    register.F = 0b00010000
    cycles = cpu.op.code_9b(register)
    assert cycles == 4
    assert_registers(register, a=0x0E, e=0x04, f=0b01100000)


# noinspection PyShadowingNames
def test_code_9c(register):
    """ SBC A,H - A=A-H-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    register.A = 0x00
    register.H = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_9c(register)
    assert cycles == 4
    assert_registers(register, a=0x00, h=0x00, f=0b11000000)

    register.A = 0x02
    register.H = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_9c(register)
    assert cycles == 4
    assert_registers(register, a=0x01, h=0x00, f=0b01000000)

    register.A = 0x00
    register.H = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_9c(register)
    assert cycles == 4
    assert_registers(register, a=0xFE, h=0x01, f=0b01110000)

    register.A = 0x13
    register.H = 0x04
    register.F = 0b00010000
    cycles = cpu.op.code_9c(register)
    assert cycles == 4
    assert_registers(register, a=0x0E, h=0x04, f=0b01100000)


# noinspection PyShadowingNames
def test_code_9d(register):
    """ SBC A,L - A=A-L-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    register.A = 0x00
    register.L = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_9d(register)
    assert cycles == 4
    assert_registers(register, a=0x00, l=0x00, f=0b11000000)

    register.A = 0x02
    register.L = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_9d(register)
    assert cycles == 4
    assert_registers(register, a=0x01, l=0x00, f=0b01000000)

    register.A = 0x00
    register.L = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_9d(register)
    assert cycles == 4
    assert_registers(register, a=0xFE, l=0x01, f=0b01110000)

    register.A = 0x13
    register.L = 0x04
    register.F = 0b00010000
    cycles = cpu.op.code_9d(register)
    assert cycles == 4
    assert_registers(register, a=0x0E, l=0x04, f=0b01100000)


# noinspection PyShadowingNames
def test_code_9e(register):
    """ SBC A,(HL) - A=A-(value at address HL)-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_9f(register):
    """ SBC A,A - A=A-A-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    register.A = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_9f(register)
    assert cycles == 4
    assert_registers(register, a=0x00, f=0b11000000)

    register.A = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_9f(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, f=0b01110000)

    register.A = 0xFF
    register.F = 0b00010000
    cycles = cpu.op.code_9f(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, f=0b01110000)


# noinspection PyShadowingNames
def test_code_a0(register):
    """ AND B - A=Logical AND A with B """
    register.A = 0b10100011
    register.B = 0b01000100
    cycles = cpu.op.code_a0(register)
    assert cycles == 4
    assert_registers(register, a=0b00000000, b=0b01000100, f=0b10100000)

    register.A = 0b10100011
    register.B = 0b01100110
    cycles = cpu.op.code_a0(register)
    assert cycles == 4
    assert_registers(register, a=0b00100010, b=0b01100110, f=0b00100000)


# noinspection PyShadowingNames
def test_code_a1(register):
    """ AND C - A=Logical AND A with C """
    register.A = 0b10100011
    register.C = 0b01000100
    cycles = cpu.op.code_a1(register)
    assert cycles == 4
    assert_registers(register, a=0b00000000, c=0b01000100, f=0b10100000)

    register.A = 0b10100011
    register.C = 0b01100110
    cycles = cpu.op.code_a1(register)
    assert cycles == 4
    assert_registers(register, a=0b00100010, c=0b01100110, f=0b00100000)


# noinspection PyShadowingNames
def test_code_a2(register):
    """ AND D - A=Logical AND A with D """
    register.A = 0b10100011
    register.D = 0b01000100
    cycles = cpu.op.code_a2(register)
    assert cycles == 4
    assert_registers(register, a=0b00000000, d=0b01000100, f=0b10100000)

    register.A = 0b10100011
    register.D = 0b01100110
    cycles = cpu.op.code_a2(register)
    assert cycles == 4
    assert_registers(register, a=0b00100010, d=0b01100110, f=0b00100000)


# noinspection PyShadowingNames
def test_code_a3(register):
    """ AND E - A=Logical AND A with E """
    register.A = 0b10100011
    register.E = 0b01000100
    cycles = cpu.op.code_a3(register)
    assert cycles == 4
    assert_registers(register, a=0b00000000, e=0b01000100, f=0b10100000)

    register.A = 0b10100011
    register.E = 0b01100110
    cycles = cpu.op.code_a3(register)
    assert cycles == 4
    assert_registers(register, a=0b00100010, e=0b01100110, f=0b00100000)


# noinspection PyShadowingNames
def test_code_a4(register):
    """ AND H - A=Logical AND A with H """
    register.A = 0b10100011
    register.H = 0b01000100
    cycles = cpu.op.code_a4(register)
    assert cycles == 4
    assert_registers(register, a=0b00000000, h=0b01000100, f=0b10100000)

    register.A = 0b10100011
    register.H = 0b01100110
    cycles = cpu.op.code_a4(register)
    assert cycles == 4
    assert_registers(register, a=0b00100010, h=0b01100110, f=0b00100000)


# noinspection PyShadowingNames
def test_code_a5(register):
    """ AND L - A=Logical AND A with L """
    register.A = 0b10100011
    register.L = 0b01000100
    cycles = cpu.op.code_a5(register)
    assert cycles == 4
    assert_registers(register, a=0b00000000, l=0b01000100, f=0b10100000)

    register.A = 0b10100011
    register.L = 0b01100110
    cycles = cpu.op.code_a5(register)
    assert cycles == 4
    assert_registers(register, a=0b00100010, l=0b01100110, f=0b00100000)


# noinspection PyShadowingNames
def test_code_a6(register):
    """ AND (HL) - A=Logical AND A with (value at address HL) """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_a7(register):
    """ AND A - A=Logical AND A with A (why?) """
    register.A = 0b00000000
    cycles = cpu.op.code_a7(register)
    assert cycles == 4
    assert_registers(register, a=0b00000000, f=0b10100000)

    register.A = 0b00100011
    cycles = cpu.op.code_a7(register)
    assert cycles == 4
    assert_registers(register, a=0b00100011, f=0b00100000)


# noinspection PyShadowingNames
def test_code_a8(register):
    """ XOR B - A=Logical XOR A with B """
    register.A = 0b10100011
    register.B = 0b10100011
    cycles = cpu.op.code_a8(register)
    assert cycles == 4
    assert_registers(register, a=0b00000000, b=0b10100011, f=0b10000000)

    register.A = 0b10100011
    register.B = 0b01100110
    cycles = cpu.op.code_a8(register)
    assert cycles == 4
    assert_registers(register, a=0b11000101, b=0b01100110, f=0b00000000)


# noinspection PyShadowingNames
def test_code_a9(register):
    """ XOR C - A=Logical XOR A with C """
    register.A = 0b10100011
    register.C = 0b10100011
    cycles = cpu.op.code_a9(register)
    assert cycles == 4
    assert_registers(register, a=0b00000000, c=0b10100011, f=0b10000000)

    register.A = 0b10100011
    register.C = 0b01100110
    cycles = cpu.op.code_a9(register)
    assert cycles == 4
    assert_registers(register, a=0b11000101, c=0b01100110, f=0b00000000)


# noinspection PyShadowingNames
def test_code_aa(register):
    """ XOR D - A=Logical XOR A with D """
    register.A = 0b10100011
    register.D = 0b10100011
    cycles = cpu.op.code_aa(register)
    assert cycles == 4
    assert_registers(register, a=0b00000000, d=0b10100011, f=0b10000000)

    register.A = 0b10100011
    register.D = 0b01100110
    cycles = cpu.op.code_aa(register)
    assert cycles == 4
    assert_registers(register, a=0b11000101, d=0b01100110, f=0b00000000)


# noinspection PyShadowingNames
def test_code_ab(register):
    """ XOR E - A=Logical XOR A with E """
    register.A = 0b10100011
    register.E = 0b10100011
    cycles = cpu.op.code_ab(register)
    assert cycles == 4
    assert_registers(register, a=0b00000000, e=0b10100011, f=0b10000000)

    register.A = 0b10100011
    register.E = 0b01100110
    cycles = cpu.op.code_ab(register)
    assert cycles == 4
    assert_registers(register, a=0b11000101, e=0b01100110, f=0b00000000)


# noinspection PyShadowingNames
def test_code_ac(register):
    """ XOR H - A=Logical XOR A with H """
    register.A = 0b10100011
    register.H = 0b10100011
    cycles = cpu.op.code_ac(register)
    assert cycles == 4
    assert_registers(register, a=0b00000000, h=0b10100011, f=0b10000000)

    register.A = 0b10100011
    register.H = 0b01100110
    cycles = cpu.op.code_ac(register)
    assert cycles == 4
    assert_registers(register, a=0b11000101, h=0b01100110, f=0b00000000)


# noinspection PyShadowingNames
def test_code_ad(register):
    """ XOR L - A=Logical XOR A with L """
    register.A = 0b10100011
    register.L = 0b10100011
    cycles = cpu.op.code_ad(register)
    assert cycles == 4
    assert_registers(register, a=0b00000000, l=0b10100011, f=0b10000000)

    register.A = 0b10100011
    register.L = 0b01100110
    cycles = cpu.op.code_ad(register)
    assert cycles == 4
    assert_registers(register, a=0b11000101, l=0b01100110, f=0b00000000)


# noinspection PyShadowingNames
def test_code_ae(register):
    """ XOR (HL) - A=Logical XOR A with (value at address HL) """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_af(register):
    """ XOR A - A=Logical XOR A with A """
    register.A = 0b10100011
    cycles = cpu.op.code_af(register)
    assert cycles == 4
    assert_registers(register, a=0b00000000, f=0b10000000)

    register.A = 0b10100011
    cycles = cpu.op.code_af(register)
    assert cycles == 4
    assert_registers(register, a=0b00000000, f=0b10000000)


# noinspection PyShadowingNames
def test_code_b0(register):
    """ OR B - A=Logical OR A with B """
    register.A = 0b00000000
    register.B = 0b00000000
    cycles = cpu.op.code_b0(register)
    assert cycles == 4
    assert_registers(register, a=0b00000000, b=0b00000000, f=0b10000000)

    register.A = 0b10100011
    register.B = 0b01100110
    cycles = cpu.op.code_b0(register)
    assert cycles == 4
    assert_registers(register, a=0b11100111, b=0b01100110, f=0b00000000)


# noinspection PyShadowingNames
def test_code_b1(register):
    """ OR C - A=Logical OR A with C """
    register.A = 0b00000000
    register.C = 0b00000000
    cycles = cpu.op.code_b1(register)
    assert cycles == 4
    assert_registers(register, a=0b00000000, c=0b00000000, f=0b10000000)

    register.A = 0b10100011
    register.C = 0b01100110
    cycles = cpu.op.code_b1(register)
    assert cycles == 4
    assert_registers(register, a=0b11100111, c=0b01100110, f=0b00000000)


# noinspection PyShadowingNames
def test_code_b2(register):
    """ OR D - A=Logical OR A with D """
    register.A = 0b00000000
    register.D = 0b00000000
    cycles = cpu.op.code_b2(register)
    assert cycles == 4
    assert_registers(register, a=0b00000000, d=0b00000000, f=0b10000000)

    register.A = 0b10100011
    register.D = 0b01100110
    cycles = cpu.op.code_b2(register)
    assert cycles == 4
    assert_registers(register, a=0b11100111, d=0b01100110, f=0b00000000)


# noinspection PyShadowingNames
def test_code_b3(register):
    """ OR E - A=Logical OR A with E """
    register.A = 0b00000000
    register.E = 0b00000000
    cycles = cpu.op.code_b3(register)
    assert cycles == 4
    assert_registers(register, a=0b00000000, e=0b00000000, f=0b10000000)

    register.A = 0b10100011
    register.E = 0b01100110
    cycles = cpu.op.code_b3(register)
    assert cycles == 4
    assert_registers(register, a=0b11100111, e=0b01100110, f=0b00000000)


# noinspection PyShadowingNames
def test_code_b4(register):
    """ OR H - A=Logical OR A with H """
    register.A = 0b00000000
    register.H = 0b00000000
    cycles = cpu.op.code_b4(register)
    assert cycles == 4
    assert_registers(register, a=0b00000000, h=0b00000000, f=0b10000000)

    register.A = 0b10100011
    register.H = 0b01100110
    cycles = cpu.op.code_b4(register)
    assert cycles == 4
    assert_registers(register, a=0b11100111, h=0b01100110, f=0b00000000)


# noinspection PyShadowingNames
def test_code_b5(register):
    """ OR L - A=Logical OR A with L """
    register.A = 0b00000000
    register.L = 0b00000000
    cycles = cpu.op.code_b5(register)
    assert cycles == 4
    assert_registers(register, a=0b00000000, l=0b00000000, f=0b10000000)

    register.A = 0b10100011
    register.L = 0b01100110
    cycles = cpu.op.code_b5(register)
    assert cycles == 4
    assert_registers(register, a=0b11100111, l=0b01100110, f=0b00000000)


# noinspection PyShadowingNames
def test_code_b6(register):
    """ OR (HL) - A=Logical OR A with (value at address HL) """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_b7(register):
    """ OR L - A=Logical OR A with A (why?) """
    register.A = 0b00000000
    cycles = cpu.op.code_b7(register)
    assert cycles == 4
    assert_registers(register, a=0b00000000, f=0b10000000)

    register.A = 0b10100011
    cycles = cpu.op.code_b7(register)
    assert cycles == 4
    assert_registers(register, a=0b10100011, f=0b00000000)


# noinspection PyShadowingNames
def test_code_b8(register):
    """ CP A,B - same as SUB A,B but throw the result away, only set flags """
    register.A = 0x00
    register.B = 0x00
    cycles = cpu.op.code_b8(register)
    assert cycles == 4
    assert_registers(register, a=0x00, b=0x00, f=0b11000000)

    register.A = 0x00
    register.B = 0x01
    cycles = cpu.op.code_b8(register)
    assert cycles == 4
    assert_registers(register, a=0x00, b=0x01, f=0b01110000)

    register.A = 0x0F
    register.B = 0x01
    cycles = cpu.op.code_b8(register)
    assert cycles == 4
    assert_registers(register, a=0x0F, b=0x01, f=0b01000000)

    register.A = 0xF0
    register.B = 0x10
    cycles = cpu.op.code_b8(register)
    assert cycles == 4
    assert_registers(register, a=0xF0, b=0x10, f=0b01000000)

    register.A = 0xFF
    register.B = 0x01
    cycles = cpu.op.code_b8(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, b=0x01, f=0b01000000)

    register.A = 0xFF
    register.B = 0xFE
    cycles = cpu.op.code_b8(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, b=0xFE, f=0b01000000)


# noinspection PyShadowingNames
def test_code_b9(register):
    """ CP A,C - same as SUB A,C but throw the result away, only set flags """
    register.A = 0x00
    register.C = 0x00
    cycles = cpu.op.code_b9(register)
    assert cycles == 4
    assert_registers(register, a=0x00, c=0x00, f=0b11000000)

    register.A = 0x00
    register.C = 0x01
    cycles = cpu.op.code_b9(register)
    assert cycles == 4
    assert_registers(register, a=0x00, c=0x01, f=0b01110000)

    register.A = 0x0F
    register.C = 0x01
    cycles = cpu.op.code_b9(register)
    assert cycles == 4
    assert_registers(register, a=0x0F, c=0x01, f=0b01000000)

    register.A = 0xF0
    register.C = 0x10
    cycles = cpu.op.code_b9(register)
    assert cycles == 4
    assert_registers(register, a=0xF0, c=0x10, f=0b01000000)

    register.A = 0xFF
    register.C = 0x01
    cycles = cpu.op.code_b9(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, c=0x01, f=0b01000000)

    register.A = 0xFF
    register.C = 0xFE
    cycles = cpu.op.code_b9(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, c=0xFE, f=0b01000000)


# noinspection PyShadowingNames
def test_code_ba(register):
    """ CP A,D - same as SUB A,D but throw the result away, only set flags """
    register.A = 0x00
    register.D = 0x00
    cycles = cpu.op.code_ba(register)
    assert cycles == 4
    assert_registers(register, a=0x00, d=0x00, f=0b11000000)

    register.A = 0x00
    register.D = 0x01
    cycles = cpu.op.code_ba(register)
    assert cycles == 4
    assert_registers(register, a=0x00, d=0x01, f=0b01110000)

    register.A = 0x0F
    register.D = 0x01
    cycles = cpu.op.code_ba(register)
    assert cycles == 4
    assert_registers(register, a=0x0F, d=0x01, f=0b01000000)

    register.A = 0xF0
    register.D = 0x10
    cycles = cpu.op.code_ba(register)
    assert cycles == 4
    assert_registers(register, a=0xF0, d=0x10, f=0b01000000)

    register.A = 0xFF
    register.D = 0x01
    cycles = cpu.op.code_ba(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, d=0x01, f=0b01000000)

    register.A = 0xFF
    register.D = 0xFE
    cycles = cpu.op.code_ba(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, d=0xFE, f=0b01000000)


# noinspection PyShadowingNames
def test_code_bb(register):
    """ CP A,E - same as SUB A,E but throw the result away, only set flags """
    register.A = 0x00
    register.E = 0x00
    cycles = cpu.op.code_bb(register)
    assert cycles == 4
    assert_registers(register, a=0x00, e=0x00, f=0b11000000)

    register.A = 0x00
    register.E = 0x01
    cycles = cpu.op.code_bb(register)
    assert cycles == 4
    assert_registers(register, a=0x00, e=0x01, f=0b01110000)

    register.A = 0x0F
    register.E = 0x01
    cycles = cpu.op.code_bb(register)
    assert cycles == 4
    assert_registers(register, a=0x0F, e=0x01, f=0b01000000)

    register.A = 0xF0
    register.E = 0x10
    cycles = cpu.op.code_bb(register)
    assert cycles == 4
    assert_registers(register, a=0xF0, e=0x10, f=0b01000000)

    register.A = 0xFF
    register.E = 0x01
    cycles = cpu.op.code_bb(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, e=0x01, f=0b01000000)

    register.A = 0xFF
    register.E = 0xFE
    cycles = cpu.op.code_bb(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, e=0xFE, f=0b01000000)


# noinspection PyShadowingNames
def test_code_bc(register):
    """ CP A,H - same as SUB A,H but throw the result away, only set flags """
    register.A = 0x00
    register.H = 0x00
    cycles = cpu.op.code_bc(register)
    assert cycles == 4
    assert_registers(register, a=0x00, h=0x00, f=0b11000000)

    register.A = 0x00
    register.H = 0x01
    cycles = cpu.op.code_bc(register)
    assert cycles == 4
    assert_registers(register, a=0x00, h=0x01, f=0b01110000)

    register.A = 0x0F
    register.H = 0x01
    cycles = cpu.op.code_bc(register)
    assert cycles == 4
    assert_registers(register, a=0x0F, h=0x01, f=0b01000000)

    register.A = 0xF0
    register.H = 0x10
    cycles = cpu.op.code_bc(register)
    assert cycles == 4
    assert_registers(register, a=0xF0, h=0x10, f=0b01000000)

    register.A = 0xFF
    register.H = 0x01
    cycles = cpu.op.code_bc(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, h=0x01, f=0b01000000)

    register.A = 0xFF
    register.H = 0xFE
    cycles = cpu.op.code_bc(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, h=0xFE, f=0b01000000)


# noinspection PyShadowingNames
def test_code_bd(register):
    """ CP A,L - same as SUB A,L but throw the result away, only set flags """
    register.A = 0x00
    register.L = 0x00
    cycles = cpu.op.code_bd(register)
    assert cycles == 4
    assert_registers(register, a=0x00, l=0x00, f=0b11000000)

    register.A = 0x00
    register.L = 0x01
    cycles = cpu.op.code_bd(register)
    assert cycles == 4
    assert_registers(register, a=0x00, l=0x01, f=0b01110000)

    register.A = 0x0F
    register.L = 0x01
    cycles = cpu.op.code_bd(register)
    assert cycles == 4
    assert_registers(register, a=0x0F, l=0x01, f=0b01000000)

    register.A = 0xF0
    register.L = 0x10
    cycles = cpu.op.code_bd(register)
    assert cycles == 4
    assert_registers(register, a=0xF0, l=0x10, f=0b01000000)

    register.A = 0xFF
    register.L = 0x01
    cycles = cpu.op.code_bd(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, l=0x01, f=0b01000000)

    register.A = 0xFF
    register.L = 0xFE
    cycles = cpu.op.code_bd(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, l=0xFE, f=0b01000000)


# noinspection PyShadowingNames
def test_code_be(register):
    """ CP A,(HL) - same as SUB A,(HL) but throw the result away, only set flags """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_c1(register):
    """ POP BC - Copy 16-bit value from stack (i.e. SP address) into BC, then increment SP by 2 """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_c5(register):
    """ PUSH BC - Decrement SP by 2 then push BC value onto stack (i.e. SP address) """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_c6(register):
    """ ADD A,d8 - A=A+d8 """
    register.A = 0x00
    d8 = 0x00
    cycles = cpu.op.code_c6(register, d8)
    assert cycles == 8
    assert_registers(register, a=0x00, f=0b10000000)

    register.A = 0x00
    d8 = 0x01
    cycles = cpu.op.code_c6(register, d8)
    assert cycles == 8
    assert_registers(register, a=0x01, f=0b00000000)

    register.A = 0x0F
    d8 = 0x01
    cycles = cpu.op.code_c6(register, d8)
    assert cycles == 8
    assert_registers(register, a=0x10, f=0b00100000)

    register.A = 0xF0
    d8 = 0x10
    cycles = cpu.op.code_c6(register, d8)
    assert cycles == 8
    assert_registers(register, a=0x00, f=0b10010000)

    register.A = 0xFF
    d8 = 0x01
    cycles = cpu.op.code_c6(register, d8)
    assert cycles == 8
    assert_registers(register, a=0x00, f=0b10110000)

    register.A = 0xFF
    d8 = 0x02
    cycles = cpu.op.code_c6(register, d8)
    assert cycles == 8
    assert_registers(register, a=0x01, f=0b00110000)


# noinspection PyShadowingNames
def test_code_ce(register):
    """ ADC A,d8 - A=A+d8+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    register.A = 0x00
    d8 = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_ce(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x00, f=0b10000000)

    register.A = 0x00
    d8 = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_ce(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x01, f=0b00000000)

    register.A = 0x00
    d8 = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_ce(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x02, f=0b00000000)

    register.A = 0x0E
    d8 = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_ce(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x10, f=0b00100000)

    register.A = 0xF0
    d8 = 0x0F
    register.F = 0b00010000
    cycles = cpu.op.code_ce(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x00, f=0b10110000)

    register.A = 0xFE
    d8 = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_ce(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x00, f=0b10110000)

    register.A = 0xFE
    d8 = 0x02
    register.F = 0b00010000
    cycles = cpu.op.code_ce(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x01, f=0b00110000)


# noinspection PyShadowingNames
def test_code_d1(register):
    """ POP DE - Copy 16-bit value from stack (i.e. SP address) into DE, then increment SP by 2 """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_d5(register):
    """ PUSH DE - Decrement SP by 2 then push DE value onto stack (i.e. SP address) """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_d6(register):
    """ SUB A,d8 - A=A-d8 """
    register.A = 0x00
    d8 = 0x00
    cycles = cpu.op.code_d6(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x00, f=0b11000000)

    register.A = 0x00
    d8 = 0x01
    cycles = cpu.op.code_d6(register,d8)
    assert cycles == 8
    assert_registers(register, a=0xFF, f=0b01110000)

    register.A = 0x0F
    d8 = 0x01
    cycles = cpu.op.code_d6(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x0E, f=0b01000000)

    register.A = 0xF0
    d8 = 0x10
    cycles = cpu.op.code_d6(register,d8)
    assert cycles == 8
    assert_registers(register, a=0xE0, f=0b01000000)

    register.A = 0xFF
    d8 = 0x01
    cycles = cpu.op.code_d6(register,d8)
    assert cycles == 8
    assert_registers(register, a=0xFE, f=0b01000000)

    register.A = 0xFF
    d8 = 0xFE
    cycles = cpu.op.code_d6(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x01, f=0b01000000)


# noinspection PyShadowingNames
def test_code_de(register):
    """ SBC A,d8 - A=A-d8-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    register.A = 0x00
    d8 = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_de(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x00, f=0b11000000)

    register.A = 0x02
    d8 = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_de(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x01, f=0b01000000)

    register.A = 0x00
    d8 = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_de(register,d8)
    assert cycles == 8
    assert_registers(register, a=0xFE, f=0b01110000)

    register.A = 0x13
    d8 = 0x04
    register.F = 0b00010000
    cycles = cpu.op.code_de(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x0E, f=0b01100000)


# noinspection PyShadowingNames
def test_code_e0(register):
    """ LDH (d8),A or LD ($FF00+d8),A - Put A into address ($FF00 + d8) """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_e1(register):
    """ POP HL - Copy 16-bit value from stack (i.e. SP address) into HL, then increment SP by 2 """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_e2(register):
    """ LD (C),A or LD ($FF00+C),A - Put A into address ($FF00 + register C) """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_e5(register):
    """ PUSH HL - Decrement SP by 2 then push HL value onto stack (i.e. SP address) """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_e6(register):
    """ AND d8 - A=Logical AND A with d8 """
    register.A = 0b10100011
    d8 = 0b01000100
    cycles = cpu.op.code_e6(register,d8)
    assert cycles == 8
    assert_registers(register, a=0b00000000, f=0b10100000)

    register.A = 0b10100011
    d8 = 0b01100110
    cycles = cpu.op.code_e6(register,d8)
    assert cycles == 8
    assert_registers(register, a=0b00100010, f=0b00100000)


# noinspection PyShadowingNames
def test_code_e8(register):
    """ LD HL,SP+d8 or LDHL SP,r8 - Put result of SP+r8 into HL (r8 is a signed value) """
    register.SP = 0x0000
    cycles = cpu.op.code_e8(register, 0x0F)
    assert cycles == 16
    assert_registers(register, sp=0x000F, f=0b00000000)

    register.SP = 0x0101
    cycles = cpu.op.code_e8(register, 0x7F)
    assert cycles == 16
    assert_registers(register, sp=0x0180, f=0b00100000)

    register.SP = 0xFFFF
    cycles = cpu.op.code_e8(register, 0x01)
    assert cycles == 16
    assert_registers(register, sp=0x0000, f=0b00110000)

    register.SP = 0xFFFF
    cycles = cpu.op.code_e8(register, 0x80)  # negative value, -128
    assert cycles == 16
    assert_registers(register, sp=0xFF7F, f=0b00000000)


# noinspection PyShadowingNames
def test_code_ea(register):
    """ LD (a16),A - Stores reg at the address in a16 (least significant byte first) """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_ee(register):
    """ XOR d8 - A=Logical XOR A with d8 """
    register.A = 0b10100011
    d8 = 0b10100011
    cycles = cpu.op.code_ee(register,d8)
    assert cycles == 8
    assert_registers(register, a=0b00000000, f=0b10000000)

    register.A = 0b10100011
    d8 = 0b01100110
    cycles = cpu.op.code_ee(register,d8)
    assert cycles == 8
    assert_registers(register, a=0b11000101, f=0b00000000)


# noinspection PyShadowingNames
def test_code_f0(register):
    """ LDH A,(d8) or LD A,($FF00+d8) - Put value at address ($FF00 + d8) into A """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_f1(register):
    """ POP AF - Copy 16-bit value from stack (i.e. SP address) into AF, then increment SP by 2 """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_f2(register):
    """ LD A,(C) or LD A,($FF00+C) - Put value at address ($FF00 + register C) into A """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_f3(register):
    """ DI - Disable interrupts AFTER THE NEXT INSTRUCTION IS EXECUTED """
    # TODO after cpu and interrupts are implemented
    pass


# noinspection PyShadowingNames
def test_code_f5(register):
    """ PUSH AF - Decrement SP by 2 then push AF value onto stack (i.e. SP address) """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_f6(register):
    """ OR d8 - A=Logical OR A with d8 """
    register.A = 0b00000000
    d8 = 0b00000000
    cycles = cpu.op.code_f6(register,d8)
    assert cycles == 8
    assert_registers(register, a=0b00000000, f=0b10000000)

    register.A = 0b10100011
    d8 = 0b01100110
    cycles = cpu.op.code_f6(register,d8)
    assert cycles == 8
    assert_registers(register, a=0b11100111, f=0b00000000)


# noinspection PyShadowingNames
def test_code_f8(register):
    """ LD HL,SP+d8 or LDHL SP,r8 - Put result of SP+r8 into HL (r8 is a signed value) """
    register.SP = 0x0000
    cycles = cpu.op.code_f8(register, 0x0F)
    assert cycles == 12
    assert_registers(register, h=0x00, l=0x0F, sp=0x0000, f=0b00000000)

    register.SP = 0x0101
    cycles = cpu.op.code_f8(register, 0x7F)
    assert cycles == 12
    assert_registers(register, h=0x01, l=0x80, sp=0x0101, f=0b00100000)

    register.SP = 0xFFFF
    cycles = cpu.op.code_f8(register, 0x01)
    assert cycles == 12
    assert_registers(register, h=0x00, l=0x00, sp=0xFFFF, f=0b00110000)

    register.SP = 0xFFFF
    cycles = cpu.op.code_f8(register, 0x80)  # negative value, -128
    assert cycles == 12
    assert_registers(register, h=0xFF, l=0x7F, sp=0xFFFF, f=0b00000000)


# noinspection PyShadowingNames
def test_code_f9(register):
    """ LD SP,HL - Put HL value into SP """
    register.set_hl(0x9933)
    cycles = cpu.op.code_f9(register)
    assert cycles == 8
    assert_registers(register, h=0x99, l=0x33, sp=0x9933)


# noinspection PyShadowingNames
def test_code_fa(register):
    """ LD A,(a16) - Load reg with the value at the address in a16 (least significant byte first) """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_fb(register):
    """ EI - Enable interrupts AFTER THE NEXT INSTRUCTION IS EXECUTED """
    # TODO after cpu and interrupts are implemented
    pass


# noinspection PyShadowingNames
def test_code_fe(register):
    """ CP A,d8 - same as SUB A,d8 but throw the result away, only set flags """
    register.A = 0x00
    d8 = 0x00
    cycles = cpu.op.code_fe(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x00, f=0b11000000)

    register.A = 0x00
    d8 = 0x01
    cycles = cpu.op.code_fe(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x00, f=0b01110000)

    register.A = 0x0F
    d8 = 0x01
    cycles = cpu.op.code_fe(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x0F, f=0b01000000)

    register.A = 0xF0
    d8 = 0x10
    cycles = cpu.op.code_fe(register,d8)
    assert cycles == 8
    assert_registers(register, a=0xF0, f=0b01000000)

    register.A = 0xFF
    d8 = 0x01
    cycles = cpu.op.code_fe(register,d8)
    assert cycles == 8
    assert_registers(register, a=0xFF, f=0b01000000)

    register.A = 0xFF
    d8 = 0xFE
    cycles = cpu.op.code_fe(register,d8)
    assert cycles == 8
    assert_registers(register, a=0xFF, f=0b01000000)


# noinspection PyShadowingNames
def test_code_cb_00(register):
    """ RLC B - Copy register B bit 7 to Carry flag, then rotate register B left """
    register.B = 0b11100010
    cycles = cpu.op.code_cb_00(register)
    assert cycles == 8
    assert_registers(register, b=0b11000101, f=0b00010000)

    register.B = 0b00000000
    cycles = cpu.op.code_cb_00(register)
    assert cycles == 8
    assert_registers(register, b=0b00000000, f=0b10000000)


# noinspection PyShadowingNames
def test_code_cb_01(register):
    """ RLC C - Copy register C bit 7 to Carry flag, then rotate register C left """
    register.C = 0b11100010
    cycles = cpu.op.code_cb_01(register)
    assert cycles == 8
    assert_registers(register, c=0b11000101, f=0b00010000)

    register.C = 0b00000000
    cycles = cpu.op.code_cb_01(register)
    assert cycles == 8
    assert_registers(register, c=0b00000000, f=0b10000000)


# noinspection PyShadowingNames
def test_code_cb_02(register):
    """ RLC D - Copy register D bit 7 to Carry flag, then rotate register D left """
    register.D = 0b11100010
    cycles = cpu.op.code_cb_02(register)
    assert cycles == 8
    assert_registers(register, d=0b11000101, f=0b00010000)

    register.D = 0b00000000
    cycles = cpu.op.code_cb_02(register)
    assert cycles == 8
    assert_registers(register, d=0b00000000, f=0b10000000)


# noinspection PyShadowingNames
def test_code_cb_03(register):
    """ RLC E - Copy register E bit 7 to Carry flag, then rotate register E left """
    register.E = 0b11100010
    cycles = cpu.op.code_cb_03(register)
    assert cycles == 8
    assert_registers(register, e=0b11000101, f=0b00010000)

    register.E = 0b00000000
    cycles = cpu.op.code_cb_03(register)
    assert cycles == 8
    assert_registers(register, e=0b00000000, f=0b10000000)


# noinspection PyShadowingNames
def test_code_cb_04(register):
    """ RLC H - Copy register H bit 7 to Carry flag, then rotate register H left """
    register.H = 0b11100010
    cycles = cpu.op.code_cb_04(register)
    assert cycles == 8
    assert_registers(register, h=0b11000101, f=0b00010000)

    register.H = 0b00000000
    cycles = cpu.op.code_cb_04(register)
    assert cycles == 8
    assert_registers(register, h=0b00000000, f=0b10000000)


# noinspection PyShadowingNames
def test_code_cb_05(register):
    """ RLC L - Copy register L bit 7 to Carry flag, then rotate register L left """
    register.L = 0b11100010
    cycles = cpu.op.code_cb_05(register)
    assert cycles == 8
    assert_registers(register, l=0b11000101, f=0b00010000)

    register.L = 0b00000000
    cycles = cpu.op.code_cb_05(register)
    assert cycles == 8
    assert_registers(register, l=0b00000000, f=0b10000000)


# noinspection PyShadowingNames
def test_code_cb_06(register):
    """ RLC (HL) - Copy (value at address HL) bit 7 to Carry flag, then rotate (value at address HL) left """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_cb_07(register):
    """ RLC A - Copy register A bit 7 to Carry flag, then rotate register A left """
    register.A = 0b11100010
    cycles = cpu.op.code_cb_07(register)
    assert cycles == 8
    assert_registers(register, a=0b11000101, f=0b00010000)

    register.A = 0b00000000
    cycles = cpu.op.code_cb_07(register)
    assert cycles == 8
    assert_registers(register, a=0b00000000, f=0b10000000)


# noinspection PyShadowingNames
def test_code_cb_08(register):
    """ RRC B - Copy register B bit 0 to Carry flag, then rotate register B right """
    register.B = 0b11100011
    cycles = cpu.op.code_cb_08(register)
    assert cycles == 8
    assert_registers(register, b=0b11110001, f=0b00010000)

    register.B = 0b00000000
    cycles = cpu.op.code_cb_08(register)
    assert cycles == 8
    assert_registers(register, b=0b00000000, f=0b10000000)


# noinspection PyShadowingNames
def test_code_cb_09(register):
    """ RRC C - Copy register C bit 0 to Carry flag, then rotate register C right """
    register.C = 0b11100011
    cycles = cpu.op.code_cb_09(register)
    assert cycles == 8
    assert_registers(register, c=0b11110001, f=0b00010000)

    register.C = 0b00000000
    cycles = cpu.op.code_cb_09(register)
    assert cycles == 8
    assert_registers(register, c=0b00000000, f=0b10000000)


# noinspection PyShadowingNames
def test_code_cb_0a(register):
    """ RRC D - Copy register D bit 0 to Carry flag, then rotate register D right """
    register.D = 0b11100011
    cycles = cpu.op.code_cb_0a(register)
    assert cycles == 8
    assert_registers(register, d=0b11110001, f=0b00010000)

    register.D = 0b00000000
    cycles = cpu.op.code_cb_0a(register)
    assert cycles == 8
    assert_registers(register, d=0b00000000, f=0b10000000)


# noinspection PyShadowingNames
def test_code_cb_0b(register):
    """ RRC E - Copy register E bit 0 to Carry flag, then rotate register E right """
    register.E = 0b11100011
    cycles = cpu.op.code_cb_0b(register)
    assert cycles == 8
    assert_registers(register, e=0b11110001, f=0b00010000)

    register.E = 0b00000000
    cycles = cpu.op.code_cb_0b(register)
    assert cycles == 8
    assert_registers(register, e=0b00000000, f=0b10000000)


# noinspection PyShadowingNames
def test_code_cb_0c(register):
    """ RRC H - Copy register H bit 0 to Carry flag, then rotate register H right """
    register.H = 0b11100011
    cycles = cpu.op.code_cb_0c(register)
    assert cycles == 8
    assert_registers(register, h=0b11110001, f=0b00010000)

    register.H = 0b00000000
    cycles = cpu.op.code_cb_0c(register)
    assert cycles == 8
    assert_registers(register, h=0b00000000, f=0b10000000)


# noinspection PyShadowingNames
def test_code_cb_0d(register):
    """ RRC L - Copy register L bit 0 to Carry flag, then rotate register L right """
    register.L = 0b11100011
    cycles = cpu.op.code_cb_0d(register)
    assert cycles == 8
    assert_registers(register, l=0b11110001, f=0b00010000)

    register.L = 0b00000000
    cycles = cpu.op.code_cb_0d(register)
    assert cycles == 8
    assert_registers(register, l=0b00000000, f=0b10000000)


# noinspection PyShadowingNames
def test_code_cb_0e(register):
    """ RRC (HL) - Copy bit 0 to Carry flag, then rotate right """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_cb_0f(register):
    """ RRC A - Copy register A bit 0 to Carry flag, then rotate register A right """
    register.A = 0b11100011
    cycles = cpu.op.code_cb_0f(register)
    assert cycles == 8
    assert_registers(register, a=0b11110001, f=0b00010000)

    register.A = 0b00000000
    cycles = cpu.op.code_cb_0f(register)
    assert cycles == 8
    assert_registers(register, a=0b00000000, f=0b10000000)


# noinspection PyShadowingNames
def test_code_cb_10(register):
    """ RL B - Copy register B bit 7 to temp, replace B bit 7 w/ Carry flag, rotate B left, copy temp to Carry flag """
    register.B = 0b11100010
    register.F = 0b00010000
    cycles = cpu.op.code_cb_10(register)
    assert cycles == 8
    assert_registers(register, b=0b11000101, f=0b00010000)

    register.B = 0b00000000
    register.F = 0b00010000
    cycles = cpu.op.code_cb_10(register)
    assert cycles == 8
    assert_registers(register, b=0b00000001, f=0b00000000)


# noinspection PyShadowingNames
def test_code_cb_11(register):
    """ RL C - Copy register C bit 7 to temp, replace C bit 7 w/ Carry flag, rotate C left, copy temp to Carry flag """
    register.C = 0b11100010
    register.F = 0b00010000
    cycles = cpu.op.code_cb_11(register)
    assert cycles == 8
    assert_registers(register, c=0b11000101, f=0b00010000)

    register.C = 0b00000000
    register.F = 0b00010000
    cycles = cpu.op.code_cb_11(register)
    assert cycles == 8
    assert_registers(register, c=0b00000001, f=0b00000000)


# noinspection PyShadowingNames
def test_code_cb_12(register):
    """ RL D - Copy register D bit 7 to temp, replace D bit 7 w/ Carry flag, rotate D left, copy temp to Carry flag """
    register.D = 0b11100010
    register.F = 0b00010000
    cycles = cpu.op.code_cb_12(register)
    assert cycles == 8
    assert_registers(register, d=0b11000101, f=0b00010000)

    register.D = 0b00000000
    register.F = 0b00010000
    cycles = cpu.op.code_cb_12(register)
    assert cycles == 8
    assert_registers(register, d=0b00000001, f=0b00000000)


# noinspection PyShadowingNames
def test_code_cb_13(register):
    """ RL E - Copy register E bit 7 to temp, replace E bit 7 w/ Carry flag, rotate E left, copy temp to Carry flag """
    register.E = 0b11100010
    register.F = 0b00010000
    cycles = cpu.op.code_cb_13(register)
    assert cycles == 8
    assert_registers(register, e=0b11000101, f=0b00010000)

    register.E = 0b00000000
    register.F = 0b00010000
    cycles = cpu.op.code_cb_13(register)
    assert cycles == 8
    assert_registers(register, e=0b00000001, f=0b00000000)


# noinspection PyShadowingNames
def test_code_cb_14(register):
    """ RL H - Copy register H bit 7 to temp, replace H bit 7 w/ Carry flag, rotate H left, copy temp to Carry flag """
    register.H = 0b11100010
    register.F = 0b00010000
    cycles = cpu.op.code_cb_14(register)
    assert cycles == 8
    assert_registers(register, h=0b11000101, f=0b00010000)

    register.H = 0b00000000
    register.F = 0b00010000
    cycles = cpu.op.code_cb_14(register)
    assert cycles == 8
    assert_registers(register, h=0b00000001, f=0b00000000)


# noinspection PyShadowingNames
def test_code_cb_15(register):
    """ RL L - Copy register L bit 7 to temp, replace L bit 7 w/ Carry flag, rotate L left, copy temp to Carry flag """
    register.L = 0b11100010
    register.F = 0b00010000
    cycles = cpu.op.code_cb_15(register)
    assert cycles == 8
    assert_registers(register, l=0b11000101, f=0b00010000)

    register.L = 0b00000000
    register.F = 0b00010000
    cycles = cpu.op.code_cb_15(register)
    assert cycles == 8
    assert_registers(register, l=0b00000001, f=0b00000000)


# noinspection PyShadowingNames
def test_code_cb_16(register):
    """ RL (HL) - Copy bit 7 to temp, replace bit 7 w/ Carry flag, rotate left, copy temp to Carry flag """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_cb_17(register):
    """ RL A - Copy register A bit 7 to temp, replace A bit 7 w/ Carry flag, rotate A left, copy temp to Carry flag """
    register.A = 0b11100010
    register.F = 0b00010000
    cycles = cpu.op.code_cb_17(register)
    assert cycles == 8
    assert_registers(register, a=0b11000101, f=0b00010000)

    register.A = 0b00000000
    register.F = 0b00010000
    cycles = cpu.op.code_cb_17(register)
    assert cycles == 8
    assert_registers(register, a=0b00000001, f=0b00000000)


# noinspection PyShadowingNames
def test_code_cb_18(register):
    """ RR B - Copy register B bit 0 to temp, replace B bit 0 w/ Carry flag, rotate B right, copy temp to Carry flag """
    register.B = 0b11100011
    register.F = 0b00010000
    cycles = cpu.op.code_cb_18(register)
    assert cycles == 8
    assert_registers(register, b=0b11110001, f=0b00010000)

    register.B = 0b00000000
    register.F = 0b00010000
    cycles = cpu.op.code_cb_18(register)
    assert cycles == 8
    assert_registers(register, b=0b10000000, f=0b00000000)


# noinspection PyShadowingNames
def test_code_cb_19(register):
    """ RR C - Copy register C bit 0 to temp, replace C bit 0 w/ Carry flag, rotate C right, copy temp to Carry flag """
    register.C = 0b11100011
    register.F = 0b00010000
    cycles = cpu.op.code_cb_19(register)
    assert cycles == 8
    assert_registers(register, c=0b11110001, f=0b00010000)

    register.C = 0b00000000
    register.F = 0b00010000
    cycles = cpu.op.code_cb_19(register)
    assert cycles == 8
    assert_registers(register, c=0b10000000, f=0b00000000)


# noinspection PyShadowingNames
def test_code_cb_1a(register):
    """ RR D - Copy register D bit 0 to temp, replace D bit 0 w/ Carry flag, rotate D right, copy temp to Carry flag """
    register.D = 0b11100011
    register.F = 0b00010000
    cycles = cpu.op.code_cb_1a(register)
    assert cycles == 8
    assert_registers(register, d=0b11110001, f=0b00010000)

    register.D = 0b00000000
    register.F = 0b00010000
    cycles = cpu.op.code_cb_1a(register)
    assert cycles == 8
    assert_registers(register, d=0b10000000, f=0b00000000)


# noinspection PyShadowingNames
def test_code_cb_1b(register):
    """ RR E - Copy register E bit 0 to temp, replace E bit 0 w/ Carry flag, rotate E right, copy temp to Carry flag """
    register.E = 0b11100011
    register.F = 0b00010000
    cycles = cpu.op.code_cb_1b(register)
    assert cycles == 8
    assert_registers(register, e=0b11110001, f=0b00010000)

    register.E = 0b00000000
    register.F = 0b00010000
    cycles = cpu.op.code_cb_1b(register)
    assert cycles == 8
    assert_registers(register, e=0b10000000, f=0b00000000)


# noinspection PyShadowingNames
def test_code_cb_1c(register):
    """ RR H - Copy register H bit 0 to temp, replace H bit 0 w/ Carry flag, rotate H right, copy temp to Carry flag """
    register.H = 0b11100011
    register.F = 0b00010000
    cycles = cpu.op.code_cb_1c(register)
    assert cycles == 8
    assert_registers(register, h=0b11110001, f=0b00010000)

    register.H = 0b00000000
    register.F = 0b00010000
    cycles = cpu.op.code_cb_1c(register)
    assert cycles == 8
    assert_registers(register, h=0b10000000, f=0b00000000)


# noinspection PyShadowingNames
def test_code_cb_1d(register):
    """ RR L - Copy register L bit 0 to temp, replace L bit 0 w/ Carry flag, rotate L right, copy temp to Carry flag """
    register.L = 0b11100011
    register.F = 0b00010000
    cycles = cpu.op.code_cb_1d(register)
    assert cycles == 8
    assert_registers(register, l=0b11110001, f=0b00010000)

    register.L = 0b00000000
    register.F = 0b00010000
    cycles = cpu.op.code_cb_1d(register)
    assert cycles == 8
    assert_registers(register, l=0b10000000, f=0b00000000)


# noinspection PyShadowingNames
def test_code_cb_1e(register):
    """ RR (HL) - Copy (HL) bit 0 to temp, replace bit 0 w/ Carry flag, rotate right, copy temp to Carry flag """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_cb_1f(register):
    """ RR A - Copy register A bit 0 to temp, replace A bit 0 w/ Carry flag, rotate A right, copy temp to Carry flag """
    register.A = 0b11100011
    register.F = 0b00010000
    cycles = cpu.op.code_cb_1f(register)
    assert cycles == 8
    assert_registers(register, a=0b11110001, f=0b00010000)

    register.A = 0b00000000
    register.F = 0b00010000
    cycles = cpu.op.code_cb_1f(register)
    assert cycles == 8
    assert_registers(register, a=0b10000000, f=0b00000000)


# noinspection PyShadowingNames
def test_code_cb_20(register):
    """ SLA B - Copy B bit 7 to temp, replace B bit 7 w/ zero, rotate B left, copy temp to Carry flag """
    register.B = 0b11100010
    cycles = cpu.op.code_cb_20(register)
    assert cycles == 8
    assert_registers(register, b=0b11000100, f=0b00010000)

    register.B = 0b00000000
    cycles = cpu.op.code_cb_20(register)
    assert cycles == 8
    assert_registers(register, b=0b00000000, f=0b10000000)


# noinspection PyShadowingNames
def test_code_cb_21(register):
    """ SLA C - Copy C bit 7 to temp, replace C bit 7 w/ zero, rotate C left, copy temp to Carry flag """
    register.C = 0b11100010
    cycles = cpu.op.code_cb_21(register)
    assert cycles == 8
    assert_registers(register, c=0b11000100, f=0b00010000)

    register.C = 0b00000000
    cycles = cpu.op.code_cb_21(register)
    assert cycles == 8
    assert_registers(register, c=0b00000000, f=0b10000000)


# noinspection PyShadowingNames
def test_code_cb_22(register):
    """ SLA D - Copy D bit 7 to temp, replace D bit 7 w/ zero, rotate D left, copy temp to Carry flag """
    register.D = 0b11100010
    cycles = cpu.op.code_cb_22(register)
    assert cycles == 8
    assert_registers(register, d=0b11000100, f=0b00010000)

    register.D = 0b00000000
    cycles = cpu.op.code_cb_22(register)
    assert cycles == 8
    assert_registers(register, d=0b00000000, f=0b10000000)


# noinspection PyShadowingNames
def test_code_cb_23(register):
    """ SLA E - Copy E bit 7 to temp, replace E bit 7 w/ zero, rotate E left, copy temp to Carry flag """
    register.E = 0b11100010
    cycles = cpu.op.code_cb_23(register)
    assert cycles == 8
    assert_registers(register, e=0b11000100, f=0b00010000)

    register.E = 0b00000000
    cycles = cpu.op.code_cb_23(register)
    assert cycles == 8
    assert_registers(register, e=0b00000000, f=0b10000000)


# noinspection PyShadowingNames
def test_code_cb_24(register):
    """ SLA H - Copy H bit 7 to temp, replace H bit 7 w/ zero, rotate H left, copy temp to Carry flag """
    register.H = 0b11100010
    cycles = cpu.op.code_cb_24(register)
    assert cycles == 8
    assert_registers(register, h=0b11000100, f=0b00010000)

    register.H = 0b00000000
    cycles = cpu.op.code_cb_24(register)
    assert cycles == 8
    assert_registers(register, h=0b00000000, f=0b10000000)


# noinspection PyShadowingNames
def test_code_cb_25(register):
    """ SLA L - Copy L bit 7 to temp, replace L bit 7 w/ zero, rotate L left, copy temp to Carry flag """
    register.L = 0b11100010
    cycles = cpu.op.code_cb_25(register)
    assert cycles == 8
    assert_registers(register, l=0b11000100, f=0b00010000)

    register.L = 0b00000000
    cycles = cpu.op.code_cb_25(register)
    assert cycles == 8
    assert_registers(register, l=0b00000000, f=0b10000000)


# noinspection PyShadowingNames
def test_code_cb_26(register):
    """ SLA (HL) - Copy (HL) bit 7 to temp, replace bit 7 w/ zero, rotate left, copy temp to Carry flag """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_cb_27(register):
    """ SLA A - Copy A bit 7 to temp, replace A bit 7 w/ zero, rotate A left, copy temp to Carry flag """
    register.A = 0b11100010
    cycles = cpu.op.code_cb_27(register)
    assert cycles == 8
    assert_registers(register, a=0b11000100, f=0b00010000)

    register.A = 0b00000000
    cycles = cpu.op.code_cb_27(register)
    assert cycles == 8
    assert_registers(register, a=0b00000000, f=0b10000000)


# noinspection PyShadowingNames
def test_code_cb_28(register):
    """ SRA B - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    register.B = 0b10000001
    cycles = cpu.op.code_cb_28(register)
    assert cycles == 8
    assert_registers(register, b=0b11000000, f=0b00010000)

    register.B = 0b00000001
    register.F = 0b00000000
    cycles = cpu.op.code_cb_28(register)
    assert cycles == 8
    assert_registers(register, b=0b00000000, f=0b10010000)


# noinspection PyShadowingNames
def test_code_cb_29(register):
    """ SRA C - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    register.C = 0b10000001
    cycles = cpu.op.code_cb_29(register)
    assert cycles == 8
    assert_registers(register, c=0b11000000, f=0b00010000)

    register.C = 0b00000001
    register.F = 0b00000000
    cycles = cpu.op.code_cb_29(register)
    assert cycles == 8
    assert_registers(register, c=0b00000000, f=0b10010000)


# noinspection PyShadowingNames
def test_code_cb_2a(register):
    """ SRA D - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    register.D = 0b10000001
    cycles = cpu.op.code_cb_2a(register)
    assert cycles == 8
    assert_registers(register, d=0b11000000, f=0b00010000)

    register.D = 0b00000001
    register.F = 0b00000000
    cycles = cpu.op.code_cb_2a(register)
    assert cycles == 8
    assert_registers(register, d=0b00000000, f=0b10010000)


# noinspection PyShadowingNames
def test_code_cb_2b(register):
    """ SRA E - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    register.E = 0b10000001
    cycles = cpu.op.code_cb_2b(register)
    assert cycles == 8
    assert_registers(register, e=0b11000000, f=0b00010000)

    register.E = 0b00000001
    register.F = 0b00000000
    cycles = cpu.op.code_cb_2b(register)
    assert cycles == 8
    assert_registers(register, e=0b00000000, f=0b10010000)


# noinspection PyShadowingNames
def test_code_cb_2c(register):
    """ SRA H - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    register.H = 0b10000001
    cycles = cpu.op.code_cb_2c(register)
    assert cycles == 8
    assert_registers(register, h=0b11000000, f=0b00010000)

    register.H = 0b00000001
    register.F = 0b00000000
    cycles = cpu.op.code_cb_2c(register)
    assert cycles == 8
    assert_registers(register, h=0b00000000, f=0b10010000)


# noinspection PyShadowingNames
def test_code_cb_2d(register):
    """ SRA L - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    register.L = 0b10000001
    cycles = cpu.op.code_cb_2d(register)
    assert cycles == 8
    assert_registers(register, l=0b11000000, f=0b00010000)

    register.L = 0b00000001
    register.F = 0b00000000
    cycles = cpu.op.code_cb_2d(register)
    assert cycles == 8
    assert_registers(register, l=0b00000000, f=0b10010000)


# noinspection PyShadowingNames
def test_code_cb_2e(register):
    """ SRA (HL) - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_cb_2f(register):
    """ SRA A - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    register.A = 0b10000001
    cycles = cpu.op.code_cb_2f(register)
    assert cycles == 8
    assert_registers(register, a=0b11000000, f=0b00010000)

    register.A = 0b00000001
    register.F = 0b00000000
    cycles = cpu.op.code_cb_2f(register)
    assert cycles == 8
    assert_registers(register, a=0b00000000, f=0b10010000)


# noinspection PyShadowingNames
def test_code_cb_30(register):
    """ SWAP B - Swap upper and lower nibbles (nibble = 4 bits) """
    register.B = 0xAB
    cycles = cpu.op.code_cb_30(register)
    assert cycles == 8
    assert_registers(register, b=0xBA, f=0b00000000)

    register.B = 0x00
    cycles = cpu.op.code_cb_30(register)
    assert cycles == 8
    assert_registers(register, b=0x00, f=0b10000000)

    register.B = 0xF0
    cycles = cpu.op.code_cb_30(register)
    assert cycles == 8
    assert_registers(register, b=0x0F, f=0b00000000)


# noinspection PyShadowingNames
def test_code_cb_31(register):
    """ SWAP C - Swap upper and lower nibbles (nibble = 4 bits) """
    register.C = 0xAB
    cycles = cpu.op.code_cb_31(register)
    assert cycles == 8
    assert_registers(register, c=0xBA, f=0b00000000)

    register.C = 0x00
    cycles = cpu.op.code_cb_31(register)
    assert cycles == 8
    assert_registers(register, c=0x00, f=0b10000000)

    register.C = 0xF0
    cycles = cpu.op.code_cb_31(register)
    assert cycles == 8
    assert_registers(register, c=0x0F, f=0b00000000)


# noinspection PyShadowingNames
def test_code_cb_32(register):
    """ SWAP D - Swap upper and lower nibbles (nibble = 4 bits) """
    register.D = 0xAB
    cycles = cpu.op.code_cb_32(register)
    assert cycles == 8
    assert_registers(register, d=0xBA, f=0b00000000)

    register.D = 0x00
    cycles = cpu.op.code_cb_32(register)
    assert cycles == 8
    assert_registers(register, d=0x00, f=0b10000000)

    register.D = 0xF0
    cycles = cpu.op.code_cb_32(register)
    assert cycles == 8
    assert_registers(register, d=0x0F, f=0b00000000)


# noinspection PyShadowingNames
def test_code_cb_33(register):
    """ SWAP E - Swap upper and lower nibbles (nibble = 4 bits) """
    register.E = 0xAB
    cycles = cpu.op.code_cb_33(register)
    assert cycles == 8
    assert_registers(register, e=0xBA, f=0b00000000)

    register.E = 0x00
    cycles = cpu.op.code_cb_33(register)
    assert cycles == 8
    assert_registers(register, e=0x00, f=0b10000000)

    register.E = 0xF0
    cycles = cpu.op.code_cb_33(register)
    assert cycles == 8
    assert_registers(register, e=0x0F, f=0b00000000)


# noinspection PyShadowingNames
def test_code_cb_34(register):
    """ SWAP H - Swap upper and lower nibbles (nibble = 4 bits) """
    register.H = 0xAB
    cycles = cpu.op.code_cb_34(register)
    assert cycles == 8
    assert_registers(register, h=0xBA, f=0b00000000)

    register.H = 0x00
    cycles = cpu.op.code_cb_34(register)
    assert cycles == 8
    assert_registers(register, h=0x00, f=0b10000000)

    register.H = 0xF0
    cycles = cpu.op.code_cb_34(register)
    assert cycles == 8
    assert_registers(register, h=0x0F, f=0b00000000)


# noinspection PyShadowingNames
def test_code_cb_35(register):
    """ SWAP L - Swap upper and lower nibbles (nibble = 4 bits) """
    register.L = 0xAB
    cycles = cpu.op.code_cb_35(register)
    assert cycles == 8
    assert_registers(register, l=0xBA, f=0b00000000)

    register.L = 0x00
    cycles = cpu.op.code_cb_35(register)
    assert cycles == 8
    assert_registers(register, l=0x00, f=0b10000000)

    register.L = 0xF0
    cycles = cpu.op.code_cb_35(register)
    assert cycles == 8
    assert_registers(register, l=0x0F, f=0b00000000)


# noinspection PyShadowingNames
def test_code_cb_36(register):
    """ SWAP (HL) - Swap upper and lower nibbles (nibble = 4 bits) """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_cb_37(register):
    """ SWAP A - Swap upper and lower nibbles (nibble = 4 bits) """
    register.A = 0xAB
    cycles = cpu.op.code_cb_37(register)
    assert cycles == 8
    assert_registers(register, a=0xBA, f=0b00000000)

    register.A = 0x00
    cycles = cpu.op.code_cb_37(register)
    assert cycles == 8
    assert_registers(register, a=0x00, f=0b10000000)

    register.A = 0xF0
    cycles = cpu.op.code_cb_37(register)
    assert cycles == 8
    assert_registers(register, a=0x0F, f=0b00000000)


# noinspection PyShadowingNames
def test_code_cb_38(register):
    """ SRL B - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    register.B = 0b10000001
    cycles = cpu.op.code_cb_38(register)
    assert cycles == 8
    assert_registers(register, b=0b01000000, f=0b00010000)

    register.B = 0b00000001
    register.F = 0b00000000
    cycles = cpu.op.code_cb_38(register)
    assert cycles == 8
    assert_registers(register, b=0b00000000, f=0b10010000)


# noinspection PyShadowingNames
def test_code_cb_39(register):
    """ SRL C - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    register.C = 0b10000001
    cycles = cpu.op.code_cb_39(register)
    assert cycles == 8
    assert_registers(register, c=0b01000000, f=0b00010000)

    register.C = 0b00000001
    register.F = 0b00000000
    cycles = cpu.op.code_cb_39(register)
    assert cycles == 8
    assert_registers(register, c=0b00000000, f=0b10010000)


# noinspection PyShadowingNames
def test_code_cb_3a(register):
    """ SRL D - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    register.D = 0b10000001
    cycles = cpu.op.code_cb_3a(register)
    assert cycles == 8
    assert_registers(register, d=0b01000000, f=0b00010000)

    register.D = 0b00000001
    register.F = 0b00000000
    cycles = cpu.op.code_cb_3a(register)
    assert cycles == 8
    assert_registers(register, d=0b00000000, f=0b10010000)


# noinspection PyShadowingNames
def test_code_cb_3b(register):
    """ SRL E - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    register.E = 0b10000001
    cycles = cpu.op.code_cb_3b(register)
    assert cycles == 8
    assert_registers(register, e=0b01000000, f=0b00010000)

    register.E = 0b00000001
    register.F = 0b00000000
    cycles = cpu.op.code_cb_3b(register)
    assert cycles == 8
    assert_registers(register, e=0b00000000, f=0b10010000)


# noinspection PyShadowingNames
def test_code_cb_3c(register):
    """ SRL H - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    register.H = 0b10000001
    cycles = cpu.op.code_cb_3c(register)
    assert cycles == 8
    assert_registers(register, h=0b01000000, f=0b00010000)

    register.H = 0b00000001
    register.F = 0b00000000
    cycles = cpu.op.code_cb_3c(register)
    assert cycles == 8
    assert_registers(register, h=0b00000000, f=0b10010000)


# noinspection PyShadowingNames
def test_code_cb_3d(register):
    """ SRL L - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    register.L = 0b10000001
    cycles = cpu.op.code_cb_3d(register)
    assert cycles == 8
    assert_registers(register, l=0b01000000, f=0b00010000)

    register.L = 0b00000001
    register.F = 0b00000000
    cycles = cpu.op.code_cb_3d(register)
    assert cycles == 8
    assert_registers(register, l=0b00000000, f=0b10010000)


# noinspection PyShadowingNames
def test_code_cb_3e(register):
    """ SRL (HL) - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_cb_3f(register):
    """ SRL A - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    register.A = 0b10000001
    cycles = cpu.op.code_cb_3f(register)
    assert cycles == 8
    assert_registers(register, a=0b01000000, f=0b00010000)

    register.A = 0b00000001
    register.F = 0b00000000
    cycles = cpu.op.code_cb_3f(register)
    assert cycles == 8
    assert_registers(register, a=0b00000000, f=0b10010000)
