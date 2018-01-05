import cpu.util

"""
CPU Operations Codes

See:
- http://www.pastraiser.com/cpu/gameboy/gameboy_opcodes.html
- https://realboyemulator.files.wordpress.com/2013/01/gbcpuman.pdf (pages 61-118)
- https://datacrystal.romhacking.net/wiki/Endianness

- http://gbdev.gg8.se/files/docs/mirrors/pandocs.html#cpuinstructionset
- https://github.com/CTurt/Cinoop/blob/master/source/cpu.c
- https://github.com/CTurt/Cinoop/blob/master/source/memory.c
- https://github.com/xerpi/realboy-vita/blob/master/src/gboy_cpu.c

The Game Boy uses Little-endian, i.e. least significant byte first. Therefore, in order to properly execute opcodes
values have to be converted to Big-endian first.
"""


# OPCODES 0x
def code_00(register):
    pass


def code_01(register, d16):
    """ LD BC,d16 - Stores given 16-bit value at BC """
    d16 = cpu.util.convert_little_endian_to_big_endian(d16)
    register.set_bc(d16)
    return 8


def code_02(register):
    """ LD (BC),A - Stores reg at the address in BC """
    # TODO after memory is implemented
    pass


def code_03(register):
    pass


def code_04(register):
    pass


def code_05(register):
    pass


def code_06(register, d8):
    """ LD B,d8 """
    register.B = d8
    return 8


def code_07(register):
    pass


def code_08(register, a16):
    """ LD (a16),SP - Set SP value into address (a16) """
    a16 = cpu.util.convert_little_endian_to_big_endian(a16)
    # TODO after memory is implemented
    return 20


def code_09(register):
    pass


def code_0a(register):
    """ LD A,(BC) - Load reg with the value at the address in BC """
    # TODO after memory is implemented
    pass


def code_0b(register):
    pass


def code_0c(register):
    pass


def code_0d(register):
    pass


def code_0e(register, d8):
    """ LD C,d8 """
    register.C = d8
    return 8


def code_0f(register):
    pass


# OPCODES 1x
def code_10(register):
    pass


def code_11(register, d16):
    """ LD DE,d16 - Stores given 16-bit value at DE """
    d16 = cpu.util.convert_little_endian_to_big_endian(d16)
    register.set_de(d16)
    return 12


def code_12(register):
    """ LD (DE),A - Stores reg at the address in DE """
    # TODO after memory is implemented
    pass


def code_13(register):
    pass

def code_14(register):
    pass

def code_15(register):
    pass


def code_16(register, d8):
    """ LD D,d8 """
    register.D = d8
    return 8


def code_17(register):
    pass

def code_18(register):
    pass

def code_19(register):
    pass


def code_1a(register):
    """ LD A,(DE) - Load reg with the value at the address in DE """
    # TODO after memory is implemented
    pass


def code_1b(register):
    pass

def code_1c(register):
    pass

def code_1d(register):
    pass


def code_1e(register, d8):
    """ LD E,d8 """
    register.E = d8
    return 8


def code_1f(register):
    pass

# OPCODES 2x
def code_20(register):
    pass


def code_21(register, d16):
    """ LD HL,d16 - Stores given 16-bit value at HL """
    d16 = cpu.util.convert_little_endian_to_big_endian(d16)
    register.set_hl(d16)
    return 12


def code_22(register):
    """ LD (HL+),A or LD (HLI),A or LDI (HL),A - Put value at A into address HL. Increment HL """
    # TODO after memory is implemented
    register.add_hl(0x0001)  # TODO: what if HL is already 0xFFFF?


def code_23(register):
    pass

def code_24(register):
    pass

def code_25(register):
    pass


def code_26(register, d8):
    """ LD H,d8 """
    register.H = d8
    return 8


def code_27(register):
    pass

def code_28(register):
    pass

def code_29(register):
    pass


def code_2a(register):
    """ LD A,(HL+) or LD A,(HLI) or LDI A,(HL) - Put value at address HL into A. Increment HL """
    # TODO after memory is implemented
    register.add_hl(0x0001)  # TODO: what if HL is already 0xFFFF?


def code_2b(register):
    pass

def code_2c(register):
    pass

def code_2d(register):
    pass


def code_2e(register, d8):
    """ LD L,d8 """
    register.L = d8
    return 8


def code_2f(register):
    pass

# OPCODES 3x
def code_30(register):
    pass


def code_31(register, d16):
    """ LD SP,d16 - Stores given 16-bit value at SP """
    d16 = cpu.util.convert_little_endian_to_big_endian(d16)
    register.SP = d16
    return 12


def code_32(register):
    """ LD (HL-),A or LD (HLD),A or LDD (HL),A - Put value at A into address HL. Decrement HL """
    # TODO after memory is implemented
    register.sub_hl(0x0001)  # TODO: what if HL is already 0x0000?


def code_33(register):
    pass

def code_34(register):
    pass

def code_35(register):
    pass


def code_36(register, d8):
    """ LD (HL),d8 - Stores d8 at the address in HL """
    # TODO after memory is implemented
    pass


def code_37(register):
    pass

def code_38(register):
    pass

def code_39(register):
    pass


def code_3a(register):
    """ LD A,(HL-) or LD A,(HLD) or LDD A,(HL) - Put value at address HL into A. Decrement HL """
    # TODO after memory is implemented
    register.sub_hl(0x0001)  # TODO: what if HL is already 0x0000?


def code_3b(register):
    pass

def code_3c(register):
    pass

def code_3d(register):
    pass


def code_3e(register, d8):
    """ LD A,d8 """
    register.A = d8
    return 8


def code_3f(register):
    pass


# OPCODES 4x
def code_40(register):
    """ LD B,B (might be a newbie question but... why?) """
    register.B = register.B
    return 4


def code_41(register):
    """ LD B,C """
    register.B = register.C
    return 4


def code_42(register):
    """ LD B,D """
    register.B = register.D
    return 4


def code_43(register):
    """ LD B,E """
    register.B = register.E
    return 4


def code_44(register):
    """ LD B,H """
    register.B = register.H
    return 4


def code_45(register):
    """ LD B,L """
    register.B = register.L
    return 4


def code_46(register):
    """ LD B,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


def code_47(register):
    """ LD B,A """
    register.B = register.A
    return 4


def code_48(register):
    """ LD C,B """
    register.C = register.B
    return 4


def code_49(register):
    """ LD C,C (might be a newbie question but... why?) """
    register.C = register.C
    return 4


def code_4a(register):
    """ LD C,D """
    register.C = register.D
    return 4


def code_4b(register):
    """ LD C,E """
    register.C = register.E
    return 4


def code_4c(register):
    """ LD C,H """
    register.C = register.H
    return 4


def code_4d(register):
    """ LD C,L """
    register.C = register.L
    return 4


def code_4e(register):
    """ LD C,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


def code_4f(register):
    """ LD C,A """
    register.C = register.A
    return 4


# OPCODES 5x
def code_50(register):
    """ LD D,B """
    register.D = register.B
    return 4


def code_51(register):
    """ LD D,C """
    register.D = register.C
    return 4


def code_52(register):
    """ LD D,D (might be a newbie question but... why?) """
    register.D = register.D
    return 4


def code_53(register):
    """ LD D,E """
    register.D = register.E
    return 4


def code_54(register):
    """ LD D,H """
    register.D = register.H
    return 4


def code_55(register):
    """ LD D,L """
    register.D = register.L
    return 4


def code_56(register):
    """ LD D,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


def code_57(register):
    """ LD D,A """
    register.D = register.A
    return 4


def code_58(register):
    """ LD E,B """
    register.E = register.B
    return 4


def code_59(register):
    """ LD E,C """
    register.E = register.C
    return 4


def code_5a(register):
    """ LD E,D """
    register.E = register.D
    return 4


def code_5b(register):
    """ LD E,E (might be a newbie question but... why?) """
    register.E = register.E
    return 4


def code_5c(register):
    """ LD E,H """
    register.E = register.H
    return 4


def code_5d(register):
    """ LD E,L """
    register.E = register.L
    return 4


def code_5e(register):
    """ LD E,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


def code_5f(register):
    """ LD E,A """
    register.E = register.A
    return 4


# OPCODES 6x
def code_60(register):
    """ LD H,B """
    register.H = register.B
    return 4


def code_61(register):
    """ LD H,C """
    register.H = register.C
    return 4


def code_62(register):
    """ LD H,D """
    register.H = register.D
    return 4


def code_63(register):
    """ LD H,E """
    register.H = register.E
    return 4


def code_64(register):
    """ LD H,H (might be a newbie question but... why?) """
    register.H = register.H
    return 4


def code_65(register):
    """ LD H,L """
    register.H = register.L
    return 4


def code_66(register):
    """ LD H,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


def code_67(register):
    """ LD H,A """
    register.H = register.A
    return 4


def code_68(register):
    """ LD L,B """
    register.L = register.B
    return 4


def code_69(register):
    """ LD L,C """
    register.L = register.C
    return 4


def code_6a(register):
    """ LD L,D """
    register.L = register.D
    return 4


def code_6b(register):
    """ LD L,E """
    register.L = register.E
    return 4


def code_6c(register):
    """ LD L,H """
    register.L = register.H
    return 4


def code_6d(register):
    """ LD L,L (might be a newbie question but... why?) """
    register.L = register.L
    return 4


def code_6e(register):
    """ LD L,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


def code_6f(register):
    """ LD L,A """
    register.L = register.A
    return 4


# OPCODES 7x
def code_70(register):
    """ LD (HL),B - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


def code_71(register):
    """ LD (HL),C - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


def code_72(register):
    """ LD (HL),D - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


def code_73(register):
    """ LD (HL),E - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


def code_74(register):
    """ LD (HL),H - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


def code_75(register):
    """ LD (HL),L - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


def code_76(register):
    pass


def code_77(register):
    """ LD (HL),A - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


def code_78(register):
    """ LD A,B """
    register.A = register.B
    return 4


def code_79(register):
    """ LD A,C """
    register.A = register.C
    return 4


def code_7a(register):
    """ LD A,D """
    register.A = register.D
    return 4


def code_7b(register):
    """ LD A,E """
    register.A = register.E
    return 4


def code_7c(register):
    """ LD A,H """
    register.A = register.H
    return 4


def code_7d(register):
    """ LD A,L """
    register.A = register.L
    return 4


def code_7e(register):
    """ LD A,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


def code_7f(register):
    """ LD A,A (might be a newbie question but... why?) """
    register.A = register.A
    return 4


# OPCODES 8x
def code_80(register):
    """ ADD A,B - A=A+B """
    result = register.A + register.B

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(False)
    register.set_half_carry_flag(((register.A & 0x0F) + (register.B & 0x0F)) > 0x0F)
    register.set_carry_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


def code_81(register):
    """ ADD A,C - A=A+C """
    result = register.A + register.C

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(False)
    register.set_half_carry_flag(((register.A & 0x0F) + (register.C & 0x0F)) > 0x0F)
    register.set_carry_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


def code_82(register):
    """ ADD A,D - A=A+D """
    result = register.A + register.D

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(False)
    register.set_half_carry_flag(((register.A & 0x0F) + (register.D & 0x0F)) > 0x0F)
    register.set_carry_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


def code_83(register):
    """ ADD A,E - A=A+E """
    result = register.A + register.E

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(False)
    register.set_half_carry_flag(((register.A & 0x0F) + (register.E & 0x0F)) > 0x0F)
    register.set_carry_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


def code_84(register):
    """ ADD A,H - A=A+H """
    result = register.A + register.H

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(False)
    register.set_half_carry_flag(((register.A & 0x0F) + (register.H & 0x0F)) > 0x0F)
    register.set_carry_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


def code_85(register):
    """ ADD A,L - A=A+L """
    result = register.A + register.L

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(False)
    register.set_half_carry_flag(((register.A & 0x0F) + (register.L & 0x0F)) > 0x0F)
    register.set_carry_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


def code_86(register):
    """ ADD A,(HL) - A=A+(value at address HL) """
    # TODO after memory is implemented
    # result = register.A + register.C

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(False)
    # register.set_half_carry_flag(((register.A & 0x0F) + (register.C & 0x0F)) > 0x0F)
    register.set_carry_flag(result > 0xFF)

    register.A = result & 0xFF
    return 8


def code_87(register):
    """ ADD A,A - A=A+A """
    result = register.A + register.A

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(False)
    register.set_half_carry_flag(((register.A & 0x0F) + (register.A & 0x0F)) > 0x0F)
    register.set_carry_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


def code_88(register):
    """ ADC A,B - A=A+B+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = register.get_carry_flag()
    result = register.A + register.B + carry_flag

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(False)
    register.set_half_carry_flag(((register.A & 0x0F) + (register.B & 0x0F) + carry_flag) > 0x0F)
    register.set_carry_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


def code_89(register):
    """ ADC A,C - A=A+C+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = register.get_carry_flag()
    result = register.A + register.C + carry_flag

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(False)
    register.set_half_carry_flag(((register.A & 0x0F) + (register.C & 0x0F) + carry_flag) > 0x0F)
    register.set_carry_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


def code_8a(register):
    """ ADC A,D - A=A+D+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = register.get_carry_flag()
    result = register.A + register.D + carry_flag

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(False)
    register.set_half_carry_flag(((register.A & 0x0F) + (register.D & 0x0F) + carry_flag) > 0x0F)
    register.set_carry_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


def code_8b(register):
    """ ADC A,E - A=A+E+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = register.get_carry_flag()
    result = register.A + register.E + carry_flag

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(False)
    register.set_half_carry_flag(((register.A & 0x0F) + (register.E & 0x0F) + carry_flag) > 0x0F)
    register.set_carry_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


def code_8c(register):
    """ ADC A,H - A=A+H+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = register.get_carry_flag()
    result = register.A + register.H + carry_flag

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(False)
    register.set_half_carry_flag(((register.A & 0x0F) + (register.H & 0x0F) + carry_flag) > 0x0F)
    register.set_carry_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


def code_8d(register):
    """ ADC A,L - A=A+L+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = register.get_carry_flag()
    result = register.A + register.L + carry_flag

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(False)
    register.set_half_carry_flag(((register.A & 0x0F) + (register.L & 0x0F) + carry_flag) > 0x0F)
    register.set_carry_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


def code_8e(register):
    """ ADC A,(HL) - A=A+(value at address HL)+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = register.get_carry_flag()
    # TODO after memory is implemented
    # result = register.A + register.L + carry_flag

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(False)
    # register.set_half_carry_flag(((register.A & 0x0F) + (register.L & 0x0F) + carry_flag) > 0x0F)
    register.set_carry_flag(result > 0xFF)

    register.A = result & 0xFF
    return 8


def code_8f(register):
    """ ADC A,A - A=A+A+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = register.get_carry_flag()
    result = register.A + register.A + carry_flag

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(False)
    register.set_half_carry_flag(((register.A & 0x0F) + (register.A & 0x0F) + carry_flag) > 0x0F)
    register.set_carry_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


# OPCODES 9x
def code_90(register):
    """ SUB A,B - A=A-B """
    result = (register.A - register.B) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(True)
    register.set_half_carry_flag((register.B & 0x0F) > (register.A & 0x0F))
    register.set_carry_flag(register.B > register.A)

    register.A = result
    return 4


def code_91(register):
    """ SUB A,C - A=A-C """
    result = (register.A - register.C) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(True)
    register.set_half_carry_flag((register.C & 0x0F) > (register.A & 0x0F))
    register.set_carry_flag(register.C > register.A)

    register.A = result
    return 4


def code_92(register):
    """ SUB A,D - A=A-D """
    result = (register.A - register.D) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(True)
    register.set_half_carry_flag((register.D & 0x0F) > (register.A & 0x0F))
    register.set_carry_flag(register.D > register.A)

    register.A = result
    return 4


def code_93(register):
    """ SUB A,E - A=A-E """
    result = (register.A - register.E) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(True)
    register.set_half_carry_flag((register.E & 0x0F) > (register.A & 0x0F))
    register.set_carry_flag(register.E > register.A)

    register.A = result
    return 4


def code_94(register):
    """ SUB A,H - A=A-H """
    result = (register.A - register.H) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(True)
    register.set_half_carry_flag((register.H & 0x0F) > (register.A & 0x0F))
    register.set_carry_flag(register.H > register.A)

    register.A = result
    return 4


def code_95(register):
    """ SUB A,L - A=A-L """
    result = (register.A - register.L) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(True)
    register.set_half_carry_flag((register.L & 0x0F) > (register.A & 0x0F))
    register.set_carry_flag(register.L > register.A)

    register.A = result
    return 4


def code_96(register):
    """ SUB A,(HL) - A=A-(value at address HL) """
    # TODO after memory is implemented
    # result = (register.A - register.B) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(True)
    # register.set_half_carry_flag((register.B & 0x0F) > (register.A & 0x0F))
    # register.set_carry_flag(register.B > register.A)

    register.A = result
    return 8


def code_97(register):
    """ SUB A,A - A=A-A """
    register.set_zero_flag(True)
    register.set_subtract_flag(True)
    register.set_half_carry_flag(False)
    register.set_carry_flag(False)

    register.A = 0x00  # A-A, therefore result is zero, always
    return 4


def code_98(register):
    """ SBC A,B - A=A-B-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    value = register.B + register.get_carry_flag()
    result = (register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(True)
    register.set_half_carry_flag((value & 0x0F) > (register.A & 0x0F))
    register.set_carry_flag(value > register.A)

    register.A = result
    return 4


def code_99(register):
    """ SBC A,C - A=A-C-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    value = register.C + register.get_carry_flag()
    result = (register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(True)
    register.set_half_carry_flag((value & 0x0F) > (register.A & 0x0F))
    register.set_carry_flag(value > register.A)

    register.A = result
    return 4


def code_9a(register):
    """ SBC A,D - A=A-D-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    value = register.D + register.get_carry_flag()
    result = (register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(True)
    register.set_half_carry_flag((value & 0x0F) > (register.A & 0x0F))
    register.set_carry_flag(value > register.A)

    register.A = result
    return 4


def code_9b(register):
    """ SBC A,E - A=A-E-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    value = register.E + register.get_carry_flag()
    result = (register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(True)
    register.set_half_carry_flag((value & 0x0F) > (register.A & 0x0F))
    register.set_carry_flag(value > register.A)

    register.A = result
    return 4


def code_9c(register):
    """ SBC A,H - A=A-H-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    value = register.H + register.get_carry_flag()
    result = (register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(True)
    register.set_half_carry_flag((value & 0x0F) > (register.A & 0x0F))
    register.set_carry_flag(value > register.A)

    register.A = result
    return 4


def code_9d(register):
    """ SBC A,L - A=A-L-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    value = register.L + register.get_carry_flag()
    result = (register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(True)
    register.set_half_carry_flag((value & 0x0F) > (register.A & 0x0F))
    register.set_carry_flag(value > register.A)

    register.A = result
    return 4


def code_9e(register):
    """ SBC A,(HL) - A=A-(value at address HL)-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    # TODO after memory is implemented
    # value = register.L + register.get_carry_flag()
    result = (register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(True)
    register.set_half_carry_flag((value & 0x0F) > (register.A & 0x0F))
    register.set_carry_flag(value > register.A)

    register.A = result
    return 8


def code_9f(register):
    """ SBC A,A - A=A-A-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    carry_flag = register.get_carry_flag()
    result = (-carry_flag) & 0xFF  # A-A-carry_flag, therefore result is -carry_flag, always

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(True)
    register.set_half_carry_flag(carry_flag)
    register.set_carry_flag(carry_flag)

    register.A = result
    return 4

# OPCODES Ax
def code_a0(register):
    pass

def code_a1(register):
    pass

def code_a2(register):
    pass

def code_a3(register):
    pass

def code_a4(register):
    pass

def code_a5(register):
    pass

def code_a6(register):
    pass

def code_a7(register):
    pass

def code_a8(register):
    pass

def code_a9(register):
    pass

def code_aa(register):
    pass

def code_ab(register):
    pass

def code_ac(register):
    pass

def code_ad(register):
    pass

def code_ae(register):
    pass

def code_af(register):
    pass

# OPCODES Bx
def code_b0(register):
    pass

def code_b1(register):
    pass

def code_b2(register):
    pass

def code_b3(register):
    pass

def code_b4(register):
    pass

def code_b5(register):
    pass

def code_b6(register):
    pass

def code_b7(register):
    pass

def code_b8(register):
    pass

def code_b9(register):
    pass

def code_ba(register):
    pass

def code_bb(register):
    pass

def code_bc(register):
    pass

def code_bd(register):
    pass

def code_be(register):
    pass

def code_bf(register):
    pass

# OPCODES Cx
def code_c0(register):
    pass


def code_c1(register):
    """ POP BC - Copy 16-bit value from stack (i.e. SP address) into BC, then increment SP by 2 """
    # TODO after memory is implemented
    register.SP += 2
    return 12


def code_c2(register):
    pass

def code_c3(register):
    pass

def code_c4(register):
    pass


def code_c5(register):
    """ PUSH BC - Decrement SP by 2 then push BC value onto stack (i.e. SP address) """
    register.SP -= 2
    # TODO after memory is implemented
    return 16


def code_c6(register, d8):
    """ ADD A,d8 - A=A+d8 """
    result = register.A + d8

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(False)
    register.set_half_carry_flag(((register.A & 0x0F) + (d8 & 0x0F)) > 0x0F)
    register.set_carry_flag(result > 0xFF)

    register.A = result & 0xFF
    return 8


def code_c7(register):
    pass

def code_c8(register):
    pass

def code_c9(register):
    pass

def code_ca(register):
    pass

def code_cb(register):
    pass

def code_cc(register):
    pass

def code_cd(register):
    pass


def code_ce(register, d8):
    """ ADC A,d8 - A=A+d8+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = register.get_carry_flag()
    result = register.A + d8 + carry_flag

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(False)
    register.set_half_carry_flag(((register.A & 0x0F) + (d8 & 0x0F) + carry_flag) > 0x0F)
    register.set_carry_flag(result > 0xFF)

    register.A = result & 0xFF
    return 8


def code_cf(register):
    pass

# OPCODES Dx
def code_d0(register):
    pass


def code_d1(register):
    """ POP DE - Copy 16-bit value from stack (i.e. SP address) into DE, then increment SP by 2 """
    # TODO after memory is implemented
    register.SP += 2
    return 12


def code_d2(register):
    pass


def code_d3():
    """ Unused opcode """
    pass


def code_d4(register):
    pass


def code_d5(register):
    """ PUSH DE - Decrement SP by 2 then push DE value onto stack (i.e. SP address) """
    register.SP -= 2
    # TODO after memory is implemented
    return 16


def code_d6(register, d8):
    """ SUB A,d8 - A=A-d8 """
    result = (register.A - d8) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(True)
    register.set_half_carry_flag((d8 & 0x0F) > (register.A & 0x0F))
    register.set_carry_flag(d8 > register.A)

    register.A = result
    return 8


def code_d7(register):
    pass

def code_d8(register):
    pass

def code_d9(register):
    pass

def code_da(register):
    pass


def code_db():
    """ Unused opcode """
    pass


def code_dc(register):
    pass


def code_dd():
    """ Unused opcode """
    pass


def code_de(register, d8):
    """ SBC A,d8 - A=A-d8-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    value = d8 + register.get_carry_flag()
    result = (register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_zero_flag((result & 0xFF) == 0)
    register.set_subtract_flag(True)
    register.set_half_carry_flag((value & 0x0F) > (register.A & 0x0F))
    register.set_carry_flag(value > register.A)

    register.A = result
    return 8


def code_df(register):
    pass


# OPCODES Ex
def code_e0(register, d8):
    """ LDH (d8),A or LD ($FF00+d8),A - Put A into address ($FF00 + d8) """
    # TODO after memory is implemented
    pass


def code_e1(register):
    """ POP HL - Copy 16-bit value from stack (i.e. SP address) into HL, then increment SP by 2 """
    # TODO after memory is implemented
    register.SP += 2
    return 12


def code_e2(register):
    """ LD (C),A or LD ($FF00+C),A - Put A into address ($FF00 + register C) """
    # TODO after memory is implemented
    pass


def code_e3():
    """ Unused opcode """
    pass


def code_e4():
    """ Unused opcode """
    pass


def code_e5(register):
    """ PUSH HL - Decrement SP by 2 then push HL value onto stack (i.e. SP address) """
    register.SP -= 2
    # TODO after memory is implemented
    return 16


def code_e6(register):
    pass

def code_e7(register):
    pass

def code_e8(register):
    pass

def code_e9(register):
    pass


def code_ea(register, a16):
    """ LD (a16),A - Stores reg at the address in a16 (least significant byte first) """
    a16 = cpu.util.convert_little_endian_to_big_endian(a16)
    # TODO after memory is implemented
    pass


def code_eb():
    """ Unused opcode """
    pass


def code_ec():
    """ Unused opcode """
    pass


def code_ed():
    """ Unused opcode """
    pass


def code_ee(register):
    pass

def code_ef(register):
    pass


# OPCODES Fx
def code_f0(register, d8):
    """ LDH A,(d8) or LD A,($FF00+d8) - Put value at address ($FF00 + d8) into A """
    # TODO after memory is implemented
    pass


def code_f1(register):
    """ POP AF - Copy 16-bit value from stack (i.e. SP address) into AF, then increment SP by 2 """
    # TODO after memory is implemented
    register.SP += 2
    return 12


def code_f2(register):
    """ LD A,(C) or LD A,($FF00+C) - Put value at address ($FF00 + register C) into A """
    # TODO after memory is implemented
    pass


def code_f3(register):
    pass


def code_f4():
    """ Unused opcode """
    pass


def code_f5(register):
    """ PUSH AF - Decrement SP by 2 then push AF value onto stack (i.e. SP address) """
    register.SP -= 2
    # TODO after memory is implemented
    return 16


def code_f6(register):
    pass

def code_f7(register):
    pass


def code_f8(register, r8):
    """ LD HL,SP+d8 or LDHL SP,r8 - Put result of SP+r8 into HL (r8 is a signed value) """
    r8 = cpu.util.convert_unsigned_integer_to_signed(r8)
    result = register.SP + r8

    register.set_zero_flag(False)
    register.set_subtract_flag(False)
    register.set_half_carry_flag(((register.SP & 0x0F) + (r8 & 0x0F)) > 0x0F)
    register.set_carry_flag(result > 0xFFFF)

    register.set_hl(result & 0xFFFF)
    return 12


def code_f9(register):
    """ LD SP,HL - Put HL value into SP """
    register.SP = register.get_hl()
    return 8


def code_fa(register, a16):
    """ LD A,(a16) - Load reg with the value at the address in a16 (least significant byte first) """
    a16 = cpu.util.convert_little_endian_to_big_endian(a16)
    # TODO after memory is implemented
    pass


def code_fb(register):
    pass


def code_fc():
    """ Unused opcode """
    pass


def code_fd():
    """ Unused opcode """
    pass


def code_fe(register):
    pass

def code_ff(register):
    pass
