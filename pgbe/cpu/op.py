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

import cpu.util


# OPCODES 0x
def code_00():
    """ NOP - Does nothing """
    return 4


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
    """ INC BC - BC=BC+1 """
    register.set_bc((register.get_bc() + 1) & 0xFFFF)
    return 8


def code_04(register):
    """ INC B - B=B+1 """
    register.B = (register.B + 1) & 0xFF
    register.set_z_flag(register.B == 0)
    register.set_n_flag(False)
    register.set_h_flag((register.B & 0x0F) == 0)
    return 4


def code_05(register):
    """ DEC B - B=B-1 """
    register.B = (register.B - 1) & 0xFF
    register.set_z_flag(register.B == 0)
    register.set_n_flag(True)
    register.set_h_flag((register.B & 0x0F) == 0x0F)
    return 4


def code_06(register, d8):
    """ LD B,d8 """
    register.B = d8
    return 8


def code_07(register):
    """ RLCA - Copy register A bit 7 to Carry flag, then rotate register A left """
    bit_7 = register.A >> 7
    register.A = ((register.A << 1) + bit_7) & 0xFF
    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_7)
    return 4


def code_08(register, a16):
    """ LD (a16),SP - Set SP value into address (a16) """
    a16 = cpu.util.convert_little_endian_to_big_endian(a16)
    # TODO after memory is implemented
    return 20


def code_09(register):
    """ ADD HL,BC - HL=HL+BC """
    result = register.get_hl() + register.get_bc()

    register.set_n_flag(False)
    register.set_h_flag(((register.get_hl() & 0x0FFF) + (register.get_bc() & 0x0FFF)) > 0x0FFF)
    register.set_c_flag(result > 0xFFFF)

    register.set_hl(result & 0xFFFF)
    return 8


def code_0a(register):
    """ LD A,(BC) - Load reg with the value at the address in BC """
    # TODO after memory is implemented
    pass


def code_0b(register):
    """ DEC BC - BC=BC-1 """
    register.set_bc((register.get_bc() - 1) & 0xFFFF)
    return 8


def code_0c(register):
    """ INC C - C=C+1 """
    register.C = (register.C + 1) & 0xFF
    register.set_z_flag(register.C == 0)
    register.set_n_flag(False)
    register.set_h_flag((register.C & 0x0F) == 0)
    return 4


def code_0d(register):
    """ DEC C - C=C-1 """
    register.C = (register.C - 1) & 0xFF
    register.set_z_flag(register.C == 0)
    register.set_n_flag(True)
    register.set_h_flag((register.C & 0x0F) == 0x0F)
    return 4


def code_0e(register, d8):
    """ LD C,d8 """
    register.C = d8
    return 8


def code_0f(register):
    """ RRCA - Copy register A bit 0 to Carry flag, then rotate register A right """
    bit_0 = register.A & 0b00000001
    register.A = ((bit_0 << 7) + (register.A >> 1)) & 0xFF
    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 4


# OPCODES 1x
def code_10(register):
    """
    STOP - Switch Game Boy into VERY low power standby mode. Halt CPU and LCD display until a button is pressed
    See: http://gbdev.gg8.se/wiki/articles/Reducing_Power_Consumption
    """
    # TODO after cpu and interrupts are implemented
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
    """ INC DE - DE=DE+1 """
    register.set_de((register.get_de() + 1) & 0xFFFF)
    return 8


def code_14(register):
    """ INC D - D=D+1 """
    register.D = (register.D + 1) & 0xFF
    register.set_z_flag(register.D == 0)
    register.set_n_flag(False)
    register.set_h_flag((register.D & 0x0F) == 0)
    return 4


def code_15(register):
    """ DEC D - D=D-1 """
    register.D = (register.D - 1) & 0xFF
    register.set_z_flag(register.D == 0)
    register.set_n_flag(True)
    register.set_h_flag((register.D & 0x0F) == 0x0F)
    return 4


def code_16(register, d8):
    """ LD D,d8 """
    register.D = d8
    return 8


def code_17(register):
    """ RLA - Copy register A bit 7 to temp, replace A bit 7 with Carry flag, rotate A left, copy temp to Carry flag """
    bit_7 = register.A >> 7
    register.A = ((register.A << 1) + register.get_c_flag()) & 0xFF
    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_7)
    return 4


def code_18(register):
    pass


def code_19(register):
    """ ADD HL,DE - HL=HL+DE """
    result = register.get_hl() + register.get_de()

    register.set_n_flag(False)
    register.set_h_flag(((register.get_hl() & 0x0FFF) + (register.get_de() & 0x0FFF)) > 0x0FFF)
    register.set_c_flag(result > 0xFFFF)

    register.set_hl(result & 0xFFFF)
    return 8


def code_1a(register):
    """ LD A,(DE) - Load reg with the value at the address in DE """
    # TODO after memory is implemented
    pass


def code_1b(register):
    """ DEC DE - DE=DE-1 """
    register.set_de((register.get_de() - 1) & 0xFFFF)
    return 8


def code_1c(register):
    """ INC E - E=E+1 """
    register.E = (register.E + 1) & 0xFF
    register.set_z_flag(register.E == 0)
    register.set_n_flag(False)
    register.set_h_flag((register.E & 0x0F) == 0)
    return 4


def code_1d(register):
    """ DEC E - E=E-1 """
    register.E = (register.E - 1) & 0xFF
    register.set_z_flag(register.E == 0)
    register.set_n_flag(True)
    register.set_h_flag((register.E & 0x0F) == 0x0F)
    return 4


def code_1e(register, d8):
    """ LD E,d8 """
    register.E = d8
    return 8


def code_1f(register):
    """ RRA - Copy register A bit 0 to temp, replace A bit 0 w/ Carry flag, rotate A right, copy temp to Carry flag """
    bit_0 = register.A & 0b00000001
    register.A = ((register.get_c_flag() << 7) + (register.A >> 1)) & 0xFF
    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 4


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
    """ INC HL - HL=HL+1 """
    register.set_hl((register.get_hl() + 1) & 0xFFFF)
    return 8


def code_24(register):
    """ INC H - H=H+1 """
    register.H = (register.H + 1) & 0xFF
    register.set_z_flag(register.H == 0)
    register.set_n_flag(False)
    register.set_h_flag((register.H & 0x0F) == 0)
    return 4


def code_25(register):
    """ DEC H - H=H-1 """
    register.H = (register.H - 1) & 0xFF
    register.set_z_flag(register.H == 0)
    register.set_n_flag(True)
    register.set_h_flag((register.H & 0x0F) == 0x0F)
    return 4


def code_26(register, d8):
    """ LD H,d8 """
    register.H = d8
    return 8


def code_27(register):
    """
    DAA - Adjust value in register A for Binary Coded Decimal representation
    See:  http://gbdev.gg8.se/wiki/articles/DAA
    """
    n_flag = register.get_n_flag()
    h_flag = register.get_h_flag()
    c_flag = register.get_c_flag()
    if n_flag:
        if c_flag:
            register.A = (register.A - 0x60) & 0xFF
        if h_flag:
            register.A = (register.A - 0x06) & 0xFF
    else:
        if c_flag or register.A > 0x99:
            register.A = (register.A + 0x60) & 0xFF
            register.set_c_flag(True)
        if h_flag or (register.A & 0x0F) > 0x09:
            register.A = (register.A + 0x06) & 0xFF

    register.set_z_flag(register.A == 0)
    register.set_h_flag(False)
    return 4


def code_28(register):
    pass


def code_29(register):
    """ ADD HL,HL - HL=HL+HL """
    result = register.get_hl() * 2

    register.set_n_flag(False)
    register.set_h_flag(((register.get_hl() & 0x0FFF) * 2) > 0x0FFF)
    register.set_c_flag(result > 0xFFFF)

    register.set_hl(result & 0xFFFF)
    return 8


def code_2a(register):
    """ LD A,(HL+) or LD A,(HLI) or LDI A,(HL) - Put value at address HL into A. Increment HL """
    # TODO after memory is implemented
    register.add_hl(0x0001)  # TODO: what if HL is already 0xFFFF?


def code_2b(register):
    """ DEC HL - HL=HL-1 """
    register.set_hl((register.get_hl() - 1) & 0xFFFF)
    return 8


def code_2c(register):
    """ INC L - L=L+1 """
    register.L = (register.L + 1) & 0xFF
    register.set_z_flag(register.L == 0)
    register.set_n_flag(False)
    register.set_h_flag((register.L & 0x0F) == 0)
    return 4


def code_2d(register):
    """ DEC L - L=L-1 """
    register.L = (register.L - 1) & 0xFF
    register.set_z_flag(register.L == 0)
    register.set_n_flag(True)
    register.set_h_flag((register.L & 0x0F) == 0x0F)
    return 4


def code_2e(register, d8):
    """ LD L,d8 """
    register.L = d8
    return 8


def code_2f(register):
    """ CPL - Logical complement of register A (i.e. flip all bits) """
    register.A = (~ register.A) & 0xFF
    register.set_n_flag(True)
    register.set_h_flag(True)
    return 4


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
    """ INC SP - SP=SP+1 """
    register.SP = (register.SP + 1) & 0xFFFF
    return 8


def code_34(register):
    """ INC (HL) - (value at address HL)=(value at address HL)+1 """
    # TODO after memory is implemented
    # register.L = (register.L + 1) & 0xFF
    # register.set_zero_flag(register.L == 0)
    register.set_n_flag(False)
    # register.set_half_carry_flag((register.L & 0x0F) == 0)
    return 12


def code_35(register):
    """ DEC (HL) - (value at address HL)=(value at address HL)-1 """
    # TODO after memory is implemented
    # register.L = (register.L - 1) & 0xFF
    # register.set_zero_flag(register.L == 0)
    register.set_n_flag(True)
    # register.set_half_carry_flag((register.L & 0x0F) == 0x0F)
    return 12


def code_36(register, d8):
    """ LD (HL),d8 - Stores d8 at the address in HL """
    # TODO after memory is implemented
    pass


def code_37(register):
    """ SCF - Set carry flag """
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(True)
    return 4


def code_38(register):
    pass


def code_39(register):
    """ ADD HL,SP - HL=HL+SP """
    result = register.get_hl() + register.SP

    register.set_n_flag(False)
    register.set_h_flag(((register.get_hl() & 0x0FFF) + (register.SP & 0x0FFF)) > 0x0FFF)
    register.set_c_flag(result > 0xFFFF)

    register.set_hl(result & 0xFFFF)
    return 8


def code_3a(register):
    """ LD A,(HL-) or LD A,(HLD) or LDD A,(HL) - Put value at address HL into A. Decrement HL """
    # TODO after memory is implemented
    register.sub_hl(0x0001)  # TODO: what if HL is already 0x0000?


def code_3b(register):
    """ DEC SP - SP=SP-1 """
    register.SP = (register.SP - 1) & 0xFFFF
    return 8


def code_3c(register):
    """ INC A - A=A+1 """
    register.A = (register.A + 1) & 0xFF
    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag((register.A & 0x0F) == 0)
    return 4


def code_3d(register):
    pass


def code_3e(register, d8):
    """ LD A,d8 """
    register.A = d8
    return 8


def code_3f(register):
    """ CCF - Invert carry flag """
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(not register.get_c_flag())
    return 4


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
    """
    HALT - Power down CPU (by stopping the system clock) until an interrupt occurs
    See: http://gbdev.gg8.se/wiki/articles/Reducing_Power_Consumption
    """
    # TODO after cpu and interrupts are implemented
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

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(False)
    register.set_h_flag(((register.A & 0x0F) + (register.B & 0x0F)) > 0x0F)
    register.set_c_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


def code_81(register):
    """ ADD A,C - A=A+C """
    result = register.A + register.C

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(False)
    register.set_h_flag(((register.A & 0x0F) + (register.C & 0x0F)) > 0x0F)
    register.set_c_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


def code_82(register):
    """ ADD A,D - A=A+D """
    result = register.A + register.D

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(False)
    register.set_h_flag(((register.A & 0x0F) + (register.D & 0x0F)) > 0x0F)
    register.set_c_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


def code_83(register):
    """ ADD A,E - A=A+E """
    result = register.A + register.E

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(False)
    register.set_h_flag(((register.A & 0x0F) + (register.E & 0x0F)) > 0x0F)
    register.set_c_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


def code_84(register):
    """ ADD A,H - A=A+H """
    result = register.A + register.H

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(False)
    register.set_h_flag(((register.A & 0x0F) + (register.H & 0x0F)) > 0x0F)
    register.set_c_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


def code_85(register):
    """ ADD A,L - A=A+L """
    result = register.A + register.L

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(False)
    register.set_h_flag(((register.A & 0x0F) + (register.L & 0x0F)) > 0x0F)
    register.set_c_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


def code_86(register):
    """ ADD A,(HL) - A=A+(value at address HL) """
    # TODO after memory is implemented
    # result = register.A + register.C

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(False)
    # register.set_half_carry_flag(((register.A & 0x0F) + (register.C & 0x0F)) > 0x0F)
    register.set_c_flag(result > 0xFF)

    register.A = result & 0xFF
    return 8


def code_87(register):
    """ ADD A,A - A=A+A """
    result = register.A + register.A

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(False)
    register.set_h_flag(((register.A & 0x0F) + (register.A & 0x0F)) > 0x0F)
    register.set_c_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


def code_88(register):
    """ ADC A,B - A=A+B+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = register.get_c_flag()
    result = register.A + register.B + carry_flag

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(False)
    register.set_h_flag(((register.A & 0x0F) + (register.B & 0x0F) + carry_flag) > 0x0F)
    register.set_c_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


def code_89(register):
    """ ADC A,C - A=A+C+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = register.get_c_flag()
    result = register.A + register.C + carry_flag

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(False)
    register.set_h_flag(((register.A & 0x0F) + (register.C & 0x0F) + carry_flag) > 0x0F)
    register.set_c_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


def code_8a(register):
    """ ADC A,D - A=A+D+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = register.get_c_flag()
    result = register.A + register.D + carry_flag

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(False)
    register.set_h_flag(((register.A & 0x0F) + (register.D & 0x0F) + carry_flag) > 0x0F)
    register.set_c_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


def code_8b(register):
    """ ADC A,E - A=A+E+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = register.get_c_flag()
    result = register.A + register.E + carry_flag

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(False)
    register.set_h_flag(((register.A & 0x0F) + (register.E & 0x0F) + carry_flag) > 0x0F)
    register.set_c_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


def code_8c(register):
    """ ADC A,H - A=A+H+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = register.get_c_flag()
    result = register.A + register.H + carry_flag

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(False)
    register.set_h_flag(((register.A & 0x0F) + (register.H & 0x0F) + carry_flag) > 0x0F)
    register.set_c_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


def code_8d(register):
    """ ADC A,L - A=A+L+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = register.get_c_flag()
    result = register.A + register.L + carry_flag

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(False)
    register.set_h_flag(((register.A & 0x0F) + (register.L & 0x0F) + carry_flag) > 0x0F)
    register.set_c_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


def code_8e(register):
    """ ADC A,(HL) - A=A+(value at address HL)+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = register.get_c_flag()
    # TODO after memory is implemented
    # result = register.A + register.L + carry_flag

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(False)
    # register.set_half_carry_flag(((register.A & 0x0F) + (register.L & 0x0F) + carry_flag) > 0x0F)
    register.set_c_flag(result > 0xFF)

    register.A = result & 0xFF
    return 8


def code_8f(register):
    """ ADC A,A - A=A+A+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = register.get_c_flag()
    result = register.A + register.A + carry_flag

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(False)
    register.set_h_flag(((register.A & 0x0F) + (register.A & 0x0F) + carry_flag) > 0x0F)
    register.set_c_flag(result > 0xFF)

    register.A = result & 0xFF
    return 4


# OPCODES 9x
def code_90(register):
    """ SUB A,B - A=A-B """
    result = (register.A - register.B) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(True)
    register.set_h_flag((register.B & 0x0F) > (register.A & 0x0F))
    register.set_c_flag(register.B > register.A)

    register.A = result
    return 4


def code_91(register):
    """ SUB A,C - A=A-C """
    result = (register.A - register.C) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(True)
    register.set_h_flag((register.C & 0x0F) > (register.A & 0x0F))
    register.set_c_flag(register.C > register.A)

    register.A = result
    return 4


def code_92(register):
    """ SUB A,D - A=A-D """
    result = (register.A - register.D) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(True)
    register.set_h_flag((register.D & 0x0F) > (register.A & 0x0F))
    register.set_c_flag(register.D > register.A)

    register.A = result
    return 4


def code_93(register):
    """ SUB A,E - A=A-E """
    result = (register.A - register.E) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(True)
    register.set_h_flag((register.E & 0x0F) > (register.A & 0x0F))
    register.set_c_flag(register.E > register.A)

    register.A = result
    return 4


def code_94(register):
    """ SUB A,H - A=A-H """
    result = (register.A - register.H) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(True)
    register.set_h_flag((register.H & 0x0F) > (register.A & 0x0F))
    register.set_c_flag(register.H > register.A)

    register.A = result
    return 4


def code_95(register):
    """ SUB A,L - A=A-L """
    result = (register.A - register.L) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(True)
    register.set_h_flag((register.L & 0x0F) > (register.A & 0x0F))
    register.set_c_flag(register.L > register.A)

    register.A = result
    return 4


def code_96(register):
    """ SUB A,(HL) - A=A-(value at address HL) """
    # TODO after memory is implemented
    # result = (register.A - register.B) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(True)
    # register.set_half_carry_flag((register.B & 0x0F) > (register.A & 0x0F))
    # register.set_carry_flag(register.B > register.A)

    register.A = result
    return 8


def code_97(register):
    """ SUB A,A - A=A-A """
    register.set_z_flag(True)
    register.set_n_flag(True)
    register.set_h_flag(False)
    register.set_c_flag(False)

    register.A = 0x00  # A-A, therefore result is zero, always
    return 4


def code_98(register):
    """ SBC A,B - A=A-B-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    value = register.B + register.get_c_flag()
    result = (register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(True)
    register.set_h_flag((value & 0x0F) > (register.A & 0x0F))
    register.set_c_flag(value > register.A)

    register.A = result
    return 4


def code_99(register):
    """ SBC A,C - A=A-C-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    value = register.C + register.get_c_flag()
    result = (register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(True)
    register.set_h_flag((value & 0x0F) > (register.A & 0x0F))
    register.set_c_flag(value > register.A)

    register.A = result
    return 4


def code_9a(register):
    """ SBC A,D - A=A-D-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    value = register.D + register.get_c_flag()
    result = (register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(True)
    register.set_h_flag((value & 0x0F) > (register.A & 0x0F))
    register.set_c_flag(value > register.A)

    register.A = result
    return 4


def code_9b(register):
    """ SBC A,E - A=A-E-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    value = register.E + register.get_c_flag()
    result = (register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(True)
    register.set_h_flag((value & 0x0F) > (register.A & 0x0F))
    register.set_c_flag(value > register.A)

    register.A = result
    return 4


def code_9c(register):
    """ SBC A,H - A=A-H-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    value = register.H + register.get_c_flag()
    result = (register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(True)
    register.set_h_flag((value & 0x0F) > (register.A & 0x0F))
    register.set_c_flag(value > register.A)

    register.A = result
    return 4


def code_9d(register):
    """ SBC A,L - A=A-L-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    value = register.L + register.get_c_flag()
    result = (register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(True)
    register.set_h_flag((value & 0x0F) > (register.A & 0x0F))
    register.set_c_flag(value > register.A)

    register.A = result
    return 4


def code_9e(register):
    """ SBC A,(HL) - A=A-(value at address HL)-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    # TODO after memory is implemented
    # value = register.L + register.get_carry_flag()
    result = (register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(True)
    register.set_h_flag((value & 0x0F) > (register.A & 0x0F))
    register.set_c_flag(value > register.A)

    register.A = result
    return 8


def code_9f(register):
    """ SBC A,A - A=A-A-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    carry_flag = register.get_c_flag()
    result = (-carry_flag) & 0xFF  # A-A-carry_flag, therefore result is -carry_flag, always

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(True)
    register.set_h_flag(carry_flag)
    register.set_c_flag(carry_flag)

    register.A = result
    return 4


# OPCODES Ax
def code_a0(register):
    """ AND B - A=Logical AND A with B """
    register.A = register.A & register.B

    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(True)
    register.set_c_flag(False)

    return 4


def code_a1(register):
    """ AND C - A=Logical AND A with C """
    register.A = register.A & register.C

    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(True)
    register.set_c_flag(False)

    return 4


def code_a2(register):
    """ AND D - A=Logical AND A with D """
    register.A = register.A & register.D

    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(True)
    register.set_c_flag(False)

    return 4


def code_a3(register):
    """ AND E - A=Logical AND A with E """
    register.A = register.A & register.E

    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(True)
    register.set_c_flag(False)

    return 4


def code_a4(register):
    """ AND H - A=Logical AND A with H """
    register.A = register.A & register.H

    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(True)
    register.set_c_flag(False)

    return 4


def code_a5(register):
    """ AND L - A=Logical AND A with L """
    register.A = register.A & register.L

    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(True)
    register.set_c_flag(False)

    return 4


def code_a6(register):
    """ AND (HL) - A=Logical AND A with (value at address HL) """
    # TODO after memory is implemented
    # register.A = register.A & register.B

    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(True)
    register.set_c_flag(False)

    return 8


def code_a7(register):
    """ AND A - A=Logical AND A with A (why?) """
    # register.A = register.A & register.A -- result is A=A, therefore useless

    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(True)
    register.set_c_flag(False)

    return 4


def code_a8(register):
    """ XOR B - A=Logical XOR A with B """
    register.A = register.A ^ register.B

    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(False)

    return 4


def code_a9(register):
    """ XOR C - A=Logical XOR A with C """
    register.A = register.A ^ register.C

    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(False)

    return 4


def code_aa(register):
    """ XOR D - A=Logical XOR A with D """
    register.A = register.A ^ register.D

    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(False)

    return 4


def code_ab(register):
    """ XOR E - A=Logical XOR A with E """
    register.A = register.A ^ register.E

    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(False)

    return 4


def code_ac(register):
    """ XOR H - A=Logical XOR A with H """
    register.A = register.A ^ register.H

    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(False)

    return 4


def code_ad(register):
    """ XOR L - A=Logical XOR A with L """
    register.A = register.A ^ register.L

    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(False)

    return 4


def code_ae(register):
    """ XOR (HL) - A=Logical XOR A with (value at address HL) """
    # TODO after memory is implemented
    # register.A = register.A ^ register.D

    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(False)

    return 8


def code_af(register):
    """ XOR A - A=Logical XOR A with A """
    register.A = 0

    register.set_z_flag(True)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(False)

    return 4


# OPCODES Bx
def code_b0(register):
    """ OR B - A=Logical OR A with B """
    register.A = register.A | register.B

    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(False)

    return 4


def code_b1(register):
    """ OR C - A=Logical OR A with C """
    register.A = register.A | register.C

    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(False)

    return 4


def code_b2(register):
    """ OR D - A=Logical OR A with D """
    register.A = register.A | register.D

    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(False)

    return 4


def code_b3(register):
    """ OR E - A=Logical OR A with E """
    register.A = register.A | register.E

    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(False)

    return 4


def code_b4(register):
    """ OR H - A=Logical OR A with H """
    register.A = register.A | register.H

    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(False)

    return 4


def code_b5(register):
    """ OR L - A=Logical OR A with L """
    register.A = register.A | register.L

    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(False)

    return 4


def code_b6(register):
    """ OR (HL) - A=Logical OR A with (value at address HL) """
    # TODO after memory is implemented
    # register.A = register.A | register.B

    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(False)

    return 8


def code_b7(register):
    """ OR L - A=Logical OR A with A (why?) """
    # register.A = register.A | register.A -- result is A=A, therefore useless

    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(False)

    return 4


def code_b8(register):
    """ CP A,B - same as SUB A,B but throw the result away, only set flags """
    register.set_z_flag(register.A == register.B)
    register.set_n_flag(True)
    register.set_h_flag((register.B & 0x0F) > (register.A & 0x0F))
    register.set_c_flag(register.B > register.A)
    return 4


def code_b9(register):
    """ CP A,C - same as SUB A,C but throw the result away, only set flags """
    register.set_z_flag(register.A == register.C)
    register.set_n_flag(True)
    register.set_h_flag((register.C & 0x0F) > (register.A & 0x0F))
    register.set_c_flag(register.C > register.A)
    return 4


def code_ba(register):
    """ CP A,D - same as SUB A,D but throw the result away, only set flags """
    register.set_z_flag(register.A == register.D)
    register.set_n_flag(True)
    register.set_h_flag((register.D & 0x0F) > (register.A & 0x0F))
    register.set_c_flag(register.D > register.A)
    return 4


def code_bb(register):
    """ CP A,E - same as SUB A,E but throw the result away, only set flags """
    register.set_z_flag(register.A == register.E)
    register.set_n_flag(True)
    register.set_h_flag((register.E & 0x0F) > (register.A & 0x0F))
    register.set_c_flag(register.E > register.A)
    return 4


def code_bc(register):
    """ CP A,H - same as SUB A,H but throw the result away, only set flags """
    register.set_z_flag(register.A == register.H)
    register.set_n_flag(True)
    register.set_h_flag((register.H & 0x0F) > (register.A & 0x0F))
    register.set_c_flag(register.H > register.A)
    return 4


def code_bd(register):
    """ CP A,L - same as SUB A,L but throw the result away, only set flags """
    register.set_z_flag(register.A == register.L)
    register.set_n_flag(True)
    register.set_h_flag((register.L & 0x0F) > (register.A & 0x0F))
    register.set_c_flag(register.L > register.A)
    return 4


def code_be(register):
    """ CP A,(HL) - same as SUB A,(HL) but throw the result away, only set flags """
    # TODO after memory is implemented
    # register.set_zero_flag(register.A == register.B)
    register.set_n_flag(True)
    # register.set_half_carry_flag((register.B & 0x0F) > (register.A & 0x0F))
    # register.set_carry_flag(register.B > register.A)
    return 8


def code_bf(register):
    """ CP A,A - same as SUB A,A but throw the result away, only set flags """
    register.set_z_flag(True)
    register.set_n_flag(True)
    register.set_h_flag(False)
    register.set_c_flag(False)
    return 4


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

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(False)
    register.set_h_flag(((register.A & 0x0F) + (d8 & 0x0F)) > 0x0F)
    register.set_c_flag(result > 0xFF)

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
    carry_flag = register.get_c_flag()
    result = register.A + d8 + carry_flag

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(False)
    register.set_h_flag(((register.A & 0x0F) + (d8 & 0x0F) + carry_flag) > 0x0F)
    register.set_c_flag(result > 0xFF)

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

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(True)
    register.set_h_flag((d8 & 0x0F) > (register.A & 0x0F))
    register.set_c_flag(d8 > register.A)

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
    value = d8 + register.get_c_flag()
    result = (register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    register.set_z_flag((result & 0xFF) == 0)
    register.set_n_flag(True)
    register.set_h_flag((value & 0x0F) > (register.A & 0x0F))
    register.set_c_flag(value > register.A)

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


def code_e6(register, d8):
    """ AND d8 - A=Logical AND A with d8 """
    register.A = register.A & d8

    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(True)
    register.set_c_flag(False)

    return 8


def code_e7(register):
    pass


def code_e8(register, r8):
    """ ADD SP,r8 - SP=SP+r8 (r8 is a signed value) """
    r8 = cpu.util.convert_unsigned_integer_to_signed(r8)
    result = register.SP + r8

    register.set_z_flag(False)
    register.set_n_flag(False)
    register.set_h_flag(((register.SP & 0x0F) + (r8 & 0x0F)) > 0x0F)
    register.set_c_flag(result > 0xFFFF)

    register.SP = result & 0xFFFF
    return 16


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


def code_ee(register, d8):
    """ XOR d8 - A=Logical XOR A with d8 """
    register.A = register.A ^ d8

    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(False)

    return 8


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
    """ DI - Disable interrupts AFTER THE NEXT INSTRUCTION IS EXECUTED """
    # TODO after cpu and interrupts are implemented
    pass


def code_f4():
    """ Unused opcode """
    pass


def code_f5(register):
    """ PUSH AF - Decrement SP by 2 then push AF value onto stack (i.e. SP address) """
    register.SP -= 2
    # TODO after memory is implemented
    return 16


def code_f6(register, d8):
    """ OR d8 - A=Logical OR A with d8 """
    register.A = register.A | d8

    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(False)

    return 8


def code_f7(register):
    pass


def code_f8(register, r8):
    """ LD HL,SP+d8 or LDHL SP,r8 - Put result of SP+r8 into HL (r8 is a signed value) """
    r8 = cpu.util.convert_unsigned_integer_to_signed(r8)
    result = register.SP + r8

    register.set_z_flag(False)
    register.set_n_flag(False)
    register.set_h_flag(((register.SP & 0x0F) + (r8 & 0x0F)) > 0x0F)
    register.set_c_flag(result > 0xFFFF)

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
    """ EI - Enable interrupts AFTER THE NEXT INSTRUCTION IS EXECUTED """
    # TODO after cpu and interrupts are implemented
    pass


def code_fc():
    """ Unused opcode """
    pass


def code_fd():
    """ Unused opcode """
    pass


def code_fe(register, d8):
    """ CP A,d8 - same as SUB A,d8 but throw the result away, only set flags """
    register.set_z_flag(register.A == d8)
    register.set_n_flag(True)
    register.set_h_flag((d8 & 0x0F) > (register.A & 0x0F))
    register.set_c_flag(d8 > register.A)
    return 8


def code_ff(register):
    pass


""" CB-Prefix operations """


# OPCODES CB 0x
def code_cb_00(register):
    """ RLC B - Copy register B bit 7 to Carry flag, then rotate register B left """
    bit_7 = register.B >> 7
    register.B = ((register.B << 1) + bit_7) & 0xFF
    register.set_z_flag(register.B == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_7)
    return 8


def code_cb_01(register):
    """ RLC C - Copy register C bit 7 to Carry flag, then rotate register C left """
    bit_7 = register.C >> 7
    register.C = ((register.C << 1) + bit_7) & 0xFF
    register.set_z_flag(register.C == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_7)
    return 8


def code_cb_02(register):
    """ RLC D - Copy register D bit 7 to Carry flag, then rotate register D left """
    bit_7 = register.D >> 7
    register.D = ((register.D << 1) + bit_7) & 0xFF
    register.set_z_flag(register.D == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_7)
    return 8


def code_cb_03(register):
    """ RLC E - Copy register E bit 7 to Carry flag, then rotate register E left """
    bit_7 = register.E >> 7
    register.E = ((register.E << 1) + bit_7) & 0xFF
    register.set_z_flag(register.E == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_7)
    return 8


def code_cb_04(register):
    """ RLC H - Copy register H bit 7 to Carry flag, then rotate register H left """
    bit_7 = register.H >> 7
    register.H = ((register.H << 1) + bit_7) & 0xFF
    register.set_z_flag(register.H == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_7)
    return 8


def code_cb_05(register):
    """ RLC L - Copy register L bit 7 to Carry flag, then rotate register L left """
    bit_7 = register.L >> 7
    register.L = ((register.L << 1) + bit_7) & 0xFF
    register.set_z_flag(register.L == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_7)
    return 8


def code_cb_06(register):
    """ RLC (HL) - Copy (value at address HL) bit 7 to Carry flag, then rotate (value at address HL) left """
    # TODO after memory is implemented
    # bit_7 = register.B >> 7
    # register.B = ((register.B << 1) + bit_7) & 0xFF
    # register.set_z_flag(register.B == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_7)
    return 16


def code_cb_07(register):
    """ RLC A - Copy register A bit 7 to Carry flag, then rotate register A left """
    code_07(register)  # Does exactly the same thing...
    return 8


def code_cb_08(register):
    """ RRC B - Copy register B bit 0 to Carry flag, then rotate register B right """
    bit_0 = register.B & 0b00000001
    register.B = ((bit_0 << 7) + (register.B >> 1)) & 0xFF
    register.set_z_flag(register.B == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 8


def code_cb_09(register):
    """ RRC C - Copy register C bit 0 to Carry flag, then rotate register C right """
    bit_0 = register.C & 0b00000001
    register.C = ((bit_0 << 7) + (register.C >> 1)) & 0xFF
    register.set_z_flag(register.C == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 8


def code_cb_0a(register):
    """ RRC D - Copy register D bit 0 to Carry flag, then rotate register D right """
    bit_0 = register.D & 0b00000001
    register.D = ((bit_0 << 7) + (register.D >> 1)) & 0xFF
    register.set_z_flag(register.D == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 8


def code_cb_0b(register):
    """ RRC E - Copy register E bit 0 to Carry flag, then rotate register E right """
    bit_0 = register.E & 0b00000001
    register.E = ((bit_0 << 7) + (register.E >> 1)) & 0xFF
    register.set_z_flag(register.E == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 8


def code_cb_0c(register):
    """ RRC H - Copy register H bit 0 to Carry flag, then rotate register H right """
    bit_0 = register.H & 0b00000001
    register.H = ((bit_0 << 7) + (register.H >> 1)) & 0xFF
    register.set_z_flag(register.H == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 8


def code_cb_0d(register):
    """ RRC L - Copy register L bit 0 to Carry flag, then rotate register L right """
    bit_0 = register.L & 0b00000001
    register.L = ((bit_0 << 7) + (register.L >> 1)) & 0xFF
    register.set_z_flag(register.L == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 8


def code_cb_0e(register):
    """ RRC (HL) - Copy bit 0 to Carry flag, then rotate right """
    # TODO after memory is implemented
    # bit_0 = register.B & 0b00000001
    # register.B = ((bit_0 << 7) + (register.B >> 1)) & 0xFF
    # register.set_z_flag(register.B == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 16


def code_cb_0f(register):
    """ RRCA - Copy register A bit 0 to Carry flag, then rotate register A right """
    code_0f(register)  # Does exactly the same thing...
    return 8


# OPCODES CB 1x
def code_cb_10(register):
    """ RL B - Copy register B bit 7 to temp, replace B bit 7 w/ Carry flag, rotate B left, copy temp to Carry flag """
    bit_7 = register.B >> 7
    register.B = ((register.B << 1) + register.get_c_flag()) & 0xFF
    register.set_z_flag(register.B == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_7)
    return 8


def code_cb_11(register):
    """ RL C - Copy register C bit 7 to temp, replace C bit 7 w/ Carry flag, rotate C left, copy temp to Carry flag """
    bit_7 = register.C >> 7
    register.C = ((register.C << 1) + register.get_c_flag()) & 0xFF
    register.set_z_flag(register.C == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_7)
    return 8


def code_cb_12(register):
    """ RL D - Copy register D bit 7 to temp, replace D bit 7 w/ Carry flag, rotate D left, copy temp to Carry flag """
    bit_7 = register.D >> 7
    register.D = ((register.D << 1) + register.get_c_flag()) & 0xFF
    register.set_z_flag(register.D == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_7)
    return 8


def code_cb_13(register):
    """ RL E - Copy register E bit 7 to temp, replace E bit 7 w/ Carry flag, rotate E left, copy temp to Carry flag """
    bit_7 = register.E >> 7
    register.E = ((register.E << 1) + register.get_c_flag()) & 0xFF
    register.set_z_flag(register.E == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_7)
    return 8


def code_cb_14(register):
    """ RL H - Copy register H bit 7 to temp, replace H bit 7 w/ Carry flag, rotate H left, copy temp to Carry flag """
    bit_7 = register.H >> 7
    register.H = ((register.H << 1) + register.get_c_flag()) & 0xFF
    register.set_z_flag(register.H == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_7)
    return 8


def code_cb_15(register):
    """ RL L - Copy register L bit 7 to temp, replace L bit 7 w/ Carry flag, rotate L left, copy temp to Carry flag """
    bit_7 = register.L >> 7
    register.L = ((register.L << 1) + register.get_c_flag()) & 0xFF
    register.set_z_flag(register.L == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_7)
    return 8


def code_cb_16(register):
    """ RL (HL) - Copy bit 7 to temp, replace bit 7 w/ Carry flag, rotate left, copy temp to Carry flag """
    # TODO after memory is implemented
    # bit_7 = register.B >> 7
    # register.B = ((register.B << 1) + register.get_c_flag()) & 0xFF
    # register.set_z_flag(register.B == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_7)
    return 16


def code_cb_17(register):
    """ RL A - Copy register A bit 7 to temp, replace A bit 7 w/ Carry flag, rotate A left, copy temp to Carry flag """
    code_17(register)  # Does exactly the same thing...
    return 8


def code_cb_18(register):
    """ RR B - Copy register B bit 0 to temp, replace bit 0 w/ Carry flag, rotate right, copy temp to Carry flag """
    bit_0 = register.B & 0b00000001
    register.B = ((register.get_c_flag() << 7) + (register.B >> 1)) & 0xFF
    register.set_z_flag(register.B == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 8


def code_cb_19(register):
    """ RR C - Copy register C bit 0 to temp, replace bit 0 w/ Carry flag, rotate right, copy temp to Carry flag """
    bit_0 = register.C & 0b00000001
    register.C = ((register.get_c_flag() << 7) + (register.C >> 1)) & 0xFF
    register.set_z_flag(register.C == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 8


def code_cb_1a(register):
    """ RR D - Copy register D bit 0 to temp, replace bit 0 w/ Carry flag, rotate right, copy temp to Carry flag """
    bit_0 = register.D & 0b00000001
    register.D = ((register.get_c_flag() << 7) + (register.D >> 1)) & 0xFF
    register.set_z_flag(register.D == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 8


def code_cb_1b(register):
    """ RR E - Copy register E bit 0 to temp, replace bit 0 w/ Carry flag, rotate right, copy temp to Carry flag """
    bit_0 = register.E & 0b00000001
    register.E = ((register.get_c_flag() << 7) + (register.E >> 1)) & 0xFF
    register.set_z_flag(register.E == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 8


def code_cb_1c(register):
    """ RR H - Copy register H bit 0 to temp, replace bit 0 w/ Carry flag, rotate right, copy temp to Carry flag """
    bit_0 = register.H & 0b00000001
    register.H = ((register.get_c_flag() << 7) + (register.H >> 1)) & 0xFF
    register.set_z_flag(register.H == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 8


def code_cb_1d(register):
    """ RR L - Copy register L bit 0 to temp, replace bit 0 w/ Carry flag, rotate right, copy temp to Carry flag """
    bit_0 = register.L & 0b00000001
    register.L = ((register.get_c_flag() << 7) + (register.L >> 1)) & 0xFF
    register.set_z_flag(register.L == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 8


def code_cb_1e(register):
    """ RR (HL) - Copy (HL) bit 0 to temp, replace bit 0 w/ Carry flag, rotate right, copy temp to Carry flag """
    # TODO after memory is implemented
    # bit_0 = register.B & 0b00000001
    # register.B = ((register.get_c_flag() << 7) + (register.B >> 1)) & 0xFF
    # register.set_z_flag(register.B == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 16


def code_cb_1f(register):
    """ RRA - Copy register A bit 0 to temp, replace A bit 0 w/ Carry flag, rotate A right, copy temp to Carry flag """
    code_1f(register)  # Does exactly the same thing...
    return 8


# OPCODES CB 2x
def code_cb_20(register):
    """ SLA B - Copy register B bit 7 to temp, replace B bit 7 w/ zero, rotate B left, copy temp to Carry flag """
    bit_7 = register.B >> 7
    register.B = (register.B << 1) & 0xFF
    register.set_z_flag(register.B == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_7)
    return 8


def code_cb_21(register):
    """ SLA C - Copy register C bit 7 to temp, replace C bit 7 w/ zero, rotate C left, copy temp to Carry flag """
    bit_7 = register.C >> 7
    register.C = (register.C << 1) & 0xFF
    register.set_z_flag(register.C == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_7)
    return 8


def code_cb_22(register):
    """ SLA D - Copy register D bit 7 to temp, replace D bit 7 w/ zero, rotate D left, copy temp to Carry flag """
    bit_7 = register.D >> 7
    register.D = (register.D << 1) & 0xFF
    register.set_z_flag(register.D == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_7)
    return 8


def code_cb_23(register):
    """ SLA E - Copy register E bit 7 to temp, replace E bit 7 w/ zero, rotate E left, copy temp to Carry flag """
    bit_7 = register.E >> 7
    register.E = (register.E << 1) & 0xFF
    register.set_z_flag(register.E == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_7)
    return 8


def code_cb_24(register):
    """ SLA H - Copy register H bit 7 to temp, replace H bit 7 w/ zero, rotate H left, copy temp to Carry flag """
    bit_7 = register.H >> 7
    register.H = (register.H << 1) & 0xFF
    register.set_z_flag(register.H == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_7)
    return 8


def code_cb_25(register):
    """ SLA L - Copy register L bit 7 to temp, replace L bit 7 w/ zero, rotate L left, copy temp to Carry flag """
    bit_7 = register.L >> 7
    register.L = (register.L << 1) & 0xFF
    register.set_z_flag(register.L == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_7)
    return 8


def code_cb_26(register):
    """ SLA (HL) - Copy bit 7 to temp, replace bit 7 w/ zero, rotate left, copy temp to Carry flag """
    # TODO after memory is implemented
    # bit_7 = register.B >> 7
    # register.B = (register.B << 1) & 0xFF
    # register.set_z_flag(register.B == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_7)
    return 16


def code_cb_27(register):
    """ SLA A - Copy register A bit 7 to temp, replace A bit 7 w/ zero, rotate A left, copy temp to Carry flag """
    bit_7 = register.A >> 7
    register.A = (register.A << 1) & 0xFF
    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_7)
    return 8


def code_cb_28(register):
    """ SRA B - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_7 = register.B >> 7
    bit_0 = register.B & 0b00000001
    register.B = ((bit_7 << 7) + (register.B >> 1)) & 0xFF
    register.set_z_flag(register.B == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 8


def code_cb_29(register):
    """ SRA C - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_7 = register.C >> 7
    bit_0 = register.C & 0b00000001
    register.C = ((bit_7 << 7) + (register.C >> 1)) & 0xFF
    register.set_z_flag(register.C == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 8


def code_cb_2a(register):
    """ SRA D - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_7 = register.D >> 7
    bit_0 = register.D & 0b00000001
    register.D = ((bit_7 << 7) + (register.D >> 1)) & 0xFF
    register.set_z_flag(register.D == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 8


def code_cb_2b(register):
    """ SRA E - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_7 = register.E >> 7
    bit_0 = register.E & 0b00000001
    register.E = ((bit_7 << 7) + (register.E >> 1)) & 0xFF
    register.set_z_flag(register.E == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 8


def code_cb_2c(register):
    """ SRA H - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_7 = register.H >> 7
    bit_0 = register.H & 0b00000001
    register.H = ((bit_7 << 7) + (register.H >> 1)) & 0xFF
    register.set_z_flag(register.H == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 8


def code_cb_2d(register):
    """ SRA L - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_7 = register.L >> 7
    bit_0 = register.L & 0b00000001
    register.L = ((bit_7 << 7) + (register.L >> 1)) & 0xFF
    register.set_z_flag(register.L == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 8


def code_cb_2e(register):
    """ SRA (HL) - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    # TODO after memory is implemented
    # bit_7 = register.B >> 7
    # bit_0 = register.B & 0b00000001
    # register.B = ((bit_7 << 7) + (register.B >> 1)) & 0xFF
    # register.set_z_flag(register.B == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 16


def code_cb_2f(register):
    """ SRA A - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_7 = register.A >> 7
    bit_0 = register.A & 0b00000001
    register.A = ((bit_7 << 7) + (register.A >> 1)) & 0xFF
    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 8


# OPCODES CB 3x
def code_cb_30(register):
    """ SWAP B - Swap upper and lower nibbles (nibble = 4 bits) """
    lower_nibble = register.B & 0x0F
    upper_nibble = (register.B >> 4) & 0x0F
    register.B = (lower_nibble << 4) | upper_nibble
    register.set_z_flag(register.B == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(False)
    return 8


def code_cb_31(register):
    """ SWAP C - Swap upper and lower nibbles (nibble = 4 bits) """
    lower_nibble = register.C & 0x0F
    upper_nibble = (register.C >> 4) & 0x0F
    register.C = (lower_nibble << 4) | upper_nibble
    register.set_z_flag(register.C == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(False)
    return 8


def code_cb_32(register):
    """ SWAP D - Swap upper and lower nibbles (nibble = 4 bits) """
    lower_nibble = register.D & 0x0F
    upper_nibble = (register.D >> 4) & 0x0F
    register.D = (lower_nibble << 4) | upper_nibble
    register.set_z_flag(register.D == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(False)
    return 8


def code_cb_33(register):
    """ SWAP E - Swap upper and lower nibbles (nibble = 4 bits) """
    lower_nibble = register.E & 0x0F
    upper_nibble = (register.E >> 4) & 0x0F
    register.E = (lower_nibble << 4) | upper_nibble
    register.set_z_flag(register.E == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(False)
    return 8


def code_cb_34(register):
    """ SWAP H - Swap upper and lower nibbles (nibble = 4 bits) """
    lower_nibble = register.H & 0x0F
    upper_nibble = (register.H >> 4) & 0x0F
    register.H = (lower_nibble << 4) | upper_nibble
    register.set_z_flag(register.H == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(False)
    return 8


def code_cb_35(register):
    """ SWAP L - Swap upper and lower nibbles (nibble = 4 bits) """
    lower_nibble = register.L & 0x0F
    upper_nibble = (register.L >> 4) & 0x0F
    register.L = (lower_nibble << 4) | upper_nibble
    register.set_z_flag(register.L == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(False)
    return 8


def code_cb_36(register):
    """ SWAP (HL) - Swap upper and lower nibbles (nibble = 4 bits) """
    # lower_nibble = register.C & 0x0F
    # upper_nibble = (register.C >> 4) & 0x0F
    # register.C = (lower_nibble << 4) | upper_nibble
    # register.set_z_flag(register.C == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(False)
    return 16


def code_cb_37(register):
    """ SWAP A - Swap upper and lower nibbles (nibble = 4 bits) """
    lower_nibble = register.A & 0x0F
    upper_nibble = (register.A >> 4) & 0x0F
    register.A = (lower_nibble << 4) | upper_nibble
    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(False)
    return 8


def code_cb_38(register):
    """ SRL B - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_0 = register.B & 0b00000001
    register.B = (register.B >> 1) & 0xFF
    register.set_z_flag(register.B == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 8


def code_cb_39(register):
    """ SRL C - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_0 = register.C & 0b00000001
    register.C = (register.C >> 1) & 0xFF
    register.set_z_flag(register.C == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 8


def code_cb_3a(register):
    """ SRL D - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_0 = register.D & 0b00000001
    register.D = (register.D >> 1) & 0xFF
    register.set_z_flag(register.D == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 8


def code_cb_3b(register):
    """ SRL E - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_0 = register.E & 0b00000001
    register.E = (register.E >> 1) & 0xFF
    register.set_z_flag(register.E == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 8


def code_cb_3c(register):
    """ SRL H - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_0 = register.H & 0b00000001
    register.H = (register.H >> 1) & 0xFF
    register.set_z_flag(register.H == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 8


def code_cb_3d(register):
    """ SRL L - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_0 = register.L & 0b00000001
    register.L = (register.L >> 1) & 0xFF
    register.set_z_flag(register.L == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 8


def code_cb_3e(register):
    """ SRL (HL) - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    # TODO after memory is implemented
    # bit_0 = register.B & 0b00000001
    # register.B = (register.B >> 1) & 0xFF
    # register.set_z_flag(register.B == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 16


def code_cb_3f(register):
    """ SRL A - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_0 = register.A & 0b00000001
    register.A = (register.A >> 1) & 0xFF
    register.set_z_flag(register.A == 0)
    register.set_n_flag(False)
    register.set_h_flag(False)
    register.set_c_flag(bit_0)
    return 8


# OPCODES CB 4x
def code_cb_40(register):
    """ BIT 0,B - Test what is the value of bit 0 """
    bit_to_check = register.B & 0b00000001
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_41(register):
    """ BIT 0,C - Test what is the value of bit 0 """
    bit_to_check = register.C & 0b00000001
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_42(register):
    """ BIT 0,D - Test what is the value of bit 0 """
    bit_to_check = register.D & 0b00000001
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_43(register):
    """ BIT 0,E - Test what is the value of bit 0 """
    bit_to_check = register.E & 0b00000001
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_44(register):
    """ BIT 0,H - Test what is the value of bit 0 """
    bit_to_check = register.H & 0b00000001
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_45(register):
    """ BIT 0,L - Test what is the value of bit 0 """
    bit_to_check = register.L & 0b00000001
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_46(register):
    """ BIT 0,(HL) - Test what is the value of bit 0 """
    # TODO after memory is implemented
    # bit_to_check = register.B & 0b00000001
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 16


def code_cb_47(register):
    """ BIT 0,A - Test what is the value of bit 0 """
    bit_to_check = register.A & 0b00000001
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_48(register):
    """ BIT 1,B - Test what is the value of bit 1 """
    bit_to_check = (register.B & 0b00000010) >> 1
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_49(register):
    """ BIT 1,C - Test what is the value of bit 1 """
    bit_to_check = (register.C & 0b00000010) >> 1
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_4a(register):
    """ BIT 1,D - Test what is the value of bit 1 """
    bit_to_check = (register.D & 0b00000010) >> 1
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_4b(register):
    """ BIT 1,E - Test what is the value of bit 1 """
    bit_to_check = (register.E & 0b00000010) >> 1
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_4c(register):
    """ BIT 1,H - Test what is the value of bit 1 """
    bit_to_check = (register.H & 0b00000010) >> 1
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_4d(register):
    """ BIT 1,L - Test what is the value of bit 1 """
    bit_to_check = (register.L & 0b00000010) >> 1
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_4e(register):
    """ BIT 1,(HL) - Test what is the value of bit 1 """
    # TODO after memory is implemented
    # bit_to_check = (register.B & 0b00000010) >> 1
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 16


def code_cb_4f(register):
    """ BIT 1,A - Test what is the value of bit 1 """
    bit_to_check = (register.A & 0b00000010) >> 1
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


# OPCODES CB 5x
def code_cb_50(register):
    """ BIT 2,B - Test what is the value of bit 2 """
    bit_to_check = (register.B & 0b00000100) >> 2
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_51(register):
    """ BIT 2,C - Test what is the value of bit 2 """
    bit_to_check = (register.C & 0b00000100) >> 2
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_52(register):
    """ BIT 2,D - Test what is the value of bit 2 """
    bit_to_check = (register.D & 0b00000100) >> 2
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_53(register):
    """ BIT 2,E - Test what is the value of bit 2 """
    bit_to_check = (register.E & 0b00000100) >> 2
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_54(register):
    """ BIT 2,H - Test what is the value of bit 2 """
    bit_to_check = (register.H & 0b00000100) >> 2
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_55(register):
    """ BIT 2,L - Test what is the value of bit 2 """
    bit_to_check = (register.L & 0b00000100) >> 2
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_56(register):
    """ BIT 2,(HL) - Test what is the value of bit 2 """
    # TODO after memory is implemented
    # bit_to_check = (register.B & 0b00000100) >> 2
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 16


def code_cb_57(register):
    """ BIT 2,A - Test what is the value of bit 2 """
    bit_to_check = (register.A & 0b00000100) >> 2
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_58(register):
    """ BIT 3,B - Test what is the value of bit 3 """
    bit_to_check = (register.B & 0b00001000) >> 3
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_59(register):
    """ BIT 3,C - Test what is the value of bit 3 """
    bit_to_check = (register.C & 0b00001000) >> 3
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_5a(register):
    """ BIT 3,D - Test what is the value of bit 3 """
    bit_to_check = (register.D & 0b00001000) >> 3
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_5b(register):
    """ BIT 3,E - Test what is the value of bit 3 """
    bit_to_check = (register.E & 0b00001000) >> 3
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_5c(register):
    """ BIT 3,H - Test what is the value of bit 3 """
    bit_to_check = (register.H & 0b00001000) >> 3
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_5d(register):
    """ BIT 3,L - Test what is the value of bit 3 """
    bit_to_check = (register.L & 0b00001000) >> 3
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_5e(register):
    """ BIT 3,(HL) - Test what is the value of bit 3 """
    # TODO after memory is implemented
    # bit_to_check = (register.B & 0b00001000) >> 3
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 16


def code_cb_5f(register):
    """ BIT 3,A - Test what is the value of bit 3 """
    bit_to_check = (register.A & 0b00001000) >> 3
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


# OPCODES CB 6x
def code_cb_60(register):
    """ BIT 4,B - Test what is the value of bit 4 """
    bit_to_check = (register.B & 0b00010000) >> 4
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_61(register):
    """ BIT 4,C - Test what is the value of bit 4 """
    bit_to_check = (register.C & 0b00010000) >> 4
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_62(register):
    """ BIT 4,D - Test what is the value of bit 4 """
    bit_to_check = (register.D & 0b00010000) >> 4
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_63(register):
    """ BIT 4,E - Test what is the value of bit 4 """
    bit_to_check = (register.E & 0b00010000) >> 4
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_64(register):
    """ BIT 4,H - Test what is the value of bit 4 """
    bit_to_check = (register.H & 0b00010000) >> 4
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_65(register):
    """ BIT 4,L - Test what is the value of bit 4 """
    bit_to_check = (register.L & 0b00010000) >> 4
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_66(register):
    """ BIT 4,(HL) - Test what is the value of bit 4 """
    # TODO after memory is implemented
    # bit_to_check = (register.B & 0b00010000) >> 4
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 16


def code_cb_67(register):
    """ BIT 4,A - Test what is the value of bit 4 """
    bit_to_check = (register.A & 0b00010000) >> 4
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_68(register):
    """ BIT 5,B - Test what is the value of bit 5 """
    bit_to_check = (register.B & 0b00100000) >> 5
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_69(register):
    """ BIT 5,C - Test what is the value of bit 5 """
    bit_to_check = (register.C & 0b00100000) >> 5
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_6a(register):
    """ BIT 5,D - Test what is the value of bit 5 """
    bit_to_check = (register.D & 0b00100000) >> 5
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_6b(register):
    """ BIT 5,E - Test what is the value of bit 5 """
    bit_to_check = (register.E & 0b00100000) >> 5
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_6c(register):
    """ BIT 5,H - Test what is the value of bit 5 """
    bit_to_check = (register.H & 0b00100000) >> 5
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_6d(register):
    """ BIT 5,L - Test what is the value of bit 5 """
    bit_to_check = (register.L & 0b00100000) >> 5
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_6e(register):
    """ BIT 5,(HL) - Test what is the value of bit 5 """
    # TODO after memory is implemented
    # bit_to_check = (register.A & 0b00100000) >> 5
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 16


def code_cb_6f(register):
    """ BIT 5,A - Test what is the value of bit 5 """
    bit_to_check = (register.A & 0b00100000) >> 5
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


# OPCODES CB 7x
def code_cb_70(register):
    """ BIT 6,B - Test what is the value of bit 6 """
    bit_to_check = (register.B & 0b01000000) >> 6
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_71(register):
    """ BIT 6,C - Test what is the value of bit 6 """
    bit_to_check = (register.C & 0b01000000) >> 6
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_72(register):
    """ BIT 6,D - Test what is the value of bit 6 """
    bit_to_check = (register.D & 0b01000000) >> 6
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_73(register):
    """ BIT 6,E - Test what is the value of bit 6 """
    bit_to_check = (register.E & 0b01000000) >> 6
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_74(register):
    """ BIT 6,H - Test what is the value of bit 6 """
    bit_to_check = (register.H & 0b01000000) >> 6
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_75(register):
    """ BIT 6,L - Test what is the value of bit 6 """
    bit_to_check = (register.L & 0b01000000) >> 6
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_76(register):
    """ BIT 6,(HL) - Test what is the value of bit 6 """
    # TODO after memory is implemented
    # bit_to_check = (register.A & 0b01000000) >> 6
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 16


def code_cb_77(register):
    """ BIT 6,A - Test what is the value of bit 6 """
    bit_to_check = (register.A & 0b01000000) >> 6
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_78(register):
    """ BIT 7,B - Test what is the value of bit 7 """
    bit_to_check = (register.B & 0b10000000) >> 7
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_79(register):
    """ BIT 7,C - Test what is the value of bit 7 """
    bit_to_check = (register.C & 0b10000000) >> 7
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_7a(register):
    """ BIT 7,D - Test what is the value of bit 7 """
    bit_to_check = (register.D & 0b10000000) >> 7
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_7b(register):
    """ BIT 7,E - Test what is the value of bit 7 """
    bit_to_check = (register.E & 0b10000000) >> 7
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_7c(register):
    """ BIT 7,H - Test what is the value of bit 7 """
    bit_to_check = (register.H & 0b10000000) >> 7
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_7d(register):
    """ BIT 7,L - Test what is the value of bit 7 """
    bit_to_check = (register.L & 0b10000000) >> 7
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


def code_cb_7e(register):
    """ BIT 7,(HL) - Test what is the value of bit 7 """
    # TODO after memory is implemented
    # bit_to_check = (register.A & 0b10000000) >> 7
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 16


def code_cb_7f(register):
    """ BIT 7,A - Test what is the value of bit 7 """
    bit_to_check = (register.A & 0b10000000) >> 7
    register.set_z_flag(bit_to_check)
    register.set_n_flag(False)
    register.set_h_flag(True)
    return 8


# OPCODES CB 8x
def code_cb_80(register):
    pass

def code_cb_81(register):
    pass

def code_cb_82(register):
    pass

def code_cb_83(register):
    pass

def code_cb_84(register):
    pass

def code_cb_85(register):
    pass

def code_cb_86(register):
    pass

def code_cb_87(register):
    pass

def code_cb_88(register):
    pass

def code_cb_89(register):
    pass

def code_cb_8a(register):
    pass

def code_cb_8b(register):
    pass

def code_cb_8c(register):
    pass

def code_cb_8d(register):
    pass

def code_cb_8e(register):
    pass

def code_cb_8f(register):
    pass

# OPCODES CB 9x
def code_cb_90(register):
    pass

def code_cb_91(register):
    pass

def code_cb_92(register):
    pass

def code_cb_93(register):
    pass

def code_cb_94(register):
    pass

def code_cb_95(register):
    pass

def code_cb_96(register):
    pass

def code_cb_97(register):
    pass

def code_cb_98(register):
    pass

def code_cb_99(register):
    pass

def code_cb_9a(register):
    pass

def code_cb_9b(register):
    pass

def code_cb_9c(register):
    pass

def code_cb_9d(register):
    pass

def code_cb_9e(register):
    pass

def code_cb_9f(register):
    pass

# OPCODES CB Ax
def code_cb_a0(register):
    pass

def code_cb_a1(register):
    pass

def code_cb_a2(register):
    pass

def code_cb_a3(register):
    pass

def code_cb_a4(register):
    pass

def code_cb_a5(register):
    pass

def code_cb_a6(register):
    pass

def code_cb_a7(register):
    pass

def code_cb_a8(register):
    pass

def code_cb_a9(register):
    pass

def code_cb_aa(register):
    pass

def code_cb_ab(register):
    pass

def code_cb_ac(register):
    pass

def code_cb_ad(register):
    pass

def code_cb_ae(register):
    pass

def code_cb_af(register):
    pass

# OPCODES CB Bx
def code_cb_b0(register):
    pass

def code_cb_b1(register):
    pass

def code_cb_b2(register):
    pass

def code_cb_b3(register):
    pass

def code_cb_b4(register):
    pass

def code_cb_b5(register):
    pass

def code_cb_b6(register):
    pass

def code_cb_b7(register):
    pass

def code_cb_b8(register):
    pass

def code_cb_b9(register):
    pass

def code_cb_ba(register):
    pass

def code_cb_bb(register):
    pass

def code_cb_bc(register):
    pass

def code_cb_bd(register):
    pass

def code_cb_be(register):
    pass

def code_cb_bf(register):
    pass


# OPCODES CB Cx
def code_cb_c0(register):
    """ SET 0,B - Set the specified bit """
    register.B = register.B | 0b00000001
    return 8


def code_cb_c1(register):
    """ SET 0,C - Set the specified bit """
    register.C = register.C | 0b00000001
    return 8


def code_cb_c2(register):
    """ SET 0,D - Set the specified bit """
    register.D = register.D | 0b00000001
    return 8


def code_cb_c3(register):
    """ SET 0,E - Set the specified bit """
    register.E = register.E | 0b00000001
    return 8


def code_cb_c4(register):
    """ SET 0,H - Set the specified bit """
    register.H = register.H | 0b00000001
    return 8


def code_cb_c5(register):
    """ SET 0,L - Set the specified bit """
    register.L = register.L | 0b00000001
    return 8


def code_cb_c6(register):
    """ SET 0,(HL) - Set the specified bit """
    # TODO after memory is implemented
    # register.B = register.B | 0b00000001
    return 16


def code_cb_c7(register):
    """ SET 0,A - Set the specified bit """
    register.A = register.A | 0b00000001
    return 8


def code_cb_c8(register):
    """ SET 1,B - Set the specified bit """
    register.B = register.B | 0b00000010
    return 8


def code_cb_c9(register):
    """ SET 1,C - Set the specified bit """
    register.C = register.C | 0b00000010
    return 8


def code_cb_ca(register):
    """ SET 1,D - Set the specified bit """
    register.D = register.D | 0b00000010
    return 8


def code_cb_cb(register):
    """ SET 1,E - Set the specified bit """
    register.E = register.E | 0b00000010
    return 8


def code_cb_cc(register):
    """ SET 1,H - Set the specified bit """
    register.H = register.H | 0b00000010
    return 8


def code_cb_cd(register):
    """ SET 1,L - Set the specified bit """
    register.L = register.L | 0b00000010
    return 8


def code_cb_ce(register):
    """ SET 1,(HL) - Set the specified bit """
    # TODO after memory is implemented
    # register.B = register.B | 0b00000010
    return 16


def code_cb_cf(register):
    """ SET 1,A - Set the specified bit """
    register.A = register.A | 0b00000010
    return 8


# OPCODES CB Dx
def code_cb_d0(register):
    """ SET 2,B - Set the specified bit """
    register.B = register.B | 0b00000100
    return 8


def code_cb_d1(register):
    """ SET 2,C - Set the specified bit """
    register.C = register.C | 0b00000100
    return 8


def code_cb_d2(register):
    """ SET 2,D - Set the specified bit """
    register.D = register.D | 0b00000100
    return 8


def code_cb_d3(register):
    """ SET 2,E - Set the specified bit """
    register.E = register.E | 0b00000100
    return 8


def code_cb_d4(register):
    """ SET 2,H - Set the specified bit """
    register.H = register.H | 0b00000100
    return 8


def code_cb_d5(register):
    """ SET 2,L - Set the specified bit """
    register.L = register.L | 0b00000100
    return 8


def code_cb_d6(register):
    """ SET 2,(HL) - Set the specified bit """
    # TODO after memory is implemented
    # register.B = register.B | 0b00000100
    return 16


def code_cb_d7(register):
    """ SET 2,A - Set the specified bit """
    register.A = register.A | 0b00000100
    return 8


def code_cb_d8(register):
    """ SET 3,B - Set the specified bit """
    register.B = register.B | 0b00001000
    return 8


def code_cb_d9(register):
    """ SET 3,C - Set the specified bit """
    register.C = register.C | 0b00001000
    return 8


def code_cb_da(register):
    """ SET 3,D - Set the specified bit """
    register.D = register.D | 0b00001000
    return 8


def code_cb_db(register):
    """ SET 3,E - Set the specified bit """
    register.E = register.E | 0b00001000
    return 8


def code_cb_dc(register):
    """ SET 3,H - Set the specified bit """
    register.H = register.H | 0b00001000
    return 8


def code_cb_dd(register):
    """ SET 3,L - Set the specified bit """
    register.L = register.L | 0b00001000
    return 8


def code_cb_de(register):
    """ SET 3,(HL) - Set the specified bit """
    # TODO after memory is implemented
    # register.B = register.B | 0b00001000
    return 16


def code_cb_df(register):
    """ SET 3,A - Set the specified bit """
    register.A = register.A | 0b00001000
    return 8


# OPCODES CB Ex
def code_cb_e0(register):
    """ SET 4,B - Set the specified bit """
    register.B = register.B | 0b00010000
    return 8


def code_cb_e1(register):
    """ SET 4,C - Set the specified bit """
    register.C = register.C | 0b00010000
    return 8


def code_cb_e2(register):
    """ SET 4,D - Set the specified bit """
    register.D = register.D | 0b00010000
    return 8


def code_cb_e3(register):
    """ SET 4,E - Set the specified bit """
    register.E = register.E | 0b00010000
    return 8


def code_cb_e4(register):
    """ SET 4,H - Set the specified bit """
    register.H = register.H | 0b00010000
    return 8


def code_cb_e5(register):
    """ SET 4,L - Set the specified bit """
    register.L = register.L | 0b00010000
    return 8


def code_cb_e6(register):
    """ SET 4,(HL) - Set the specified bit """
    # TODO after memory is implemented
    # register.B = register.B | 0b00010000
    return 16


def code_cb_e7(register):
    """ SET 4,A - Set the specified bit """
    register.A = register.A | 0b00010000
    return 8


def code_cb_e8(register):
    """ SET 5,B - Set the specified bit """
    register.B = register.B | 0b00100000
    return 8


def code_cb_e9(register):
    """ SET 5,C - Set the specified bit """
    register.C = register.C | 0b00100000
    return 8


def code_cb_ea(register):
    """ SET 5,D - Set the specified bit """
    register.D = register.D | 0b00100000
    return 8


def code_cb_eb(register):
    """ SET 5,E - Set the specified bit """
    register.E = register.E | 0b00100000
    return 8


def code_cb_ec(register):
    """ SET 5,H - Set the specified bit """
    register.H = register.H | 0b00100000
    return 8


def code_cb_ed(register):
    """ SET 5,L - Set the specified bit """
    register.L = register.L | 0b00100000
    return 8


def code_cb_ee(register):
    """ SET 5,(HL) - Set the specified bit """
    # TODO after memory is implemented
    # register.B = register.B | 0b00100000
    return 16


def code_cb_ef(register):
    """ SET 5,A - Set the specified bit """
    register.A = register.A | 0b00100000
    return 8


# OPCODES CB Fx
def code_cb_f0(register):
    """ SET 6,B - Set the specified bit """
    register.B = register.B | 0b01000000
    return 8


def code_cb_f1(register):
    """ SET 6,C - Set the specified bit """
    register.C = register.C | 0b01000000
    return 8


def code_cb_f2(register):
    """ SET 6,D - Set the specified bit """
    register.D = register.D | 0b01000000
    return 8


def code_cb_f3(register):
    """ SET 6,E - Set the specified bit """
    register.E = register.E | 0b01000000
    return 8


def code_cb_f4(register):
    """ SET 6,H - Set the specified bit """
    register.H = register.H | 0b01000000
    return 8


def code_cb_f5(register):
    """ SET 6,L - Set the specified bit """
    register.L = register.L | 0b01000000
    return 8


def code_cb_f6(register):
    """ SET 6,(HL) - Set the specified bit """
    # TODO after memory is implemented
    # register.B = register.B | 0b01000000
    return 16


def code_cb_f7(register):
    """ SET 6,A - Set the specified bit """
    register.A = register.A | 0b01000000
    return 8


def code_cb_f8(register):
    """ SET 7,B - Set the specified bit """
    register.B = register.B | 0b10000000
    return 8


def code_cb_f9(register):
    """ SET 7,C - Set the specified bit """
    register.C = register.C | 0b10000000
    return 8


def code_cb_fa(register):
    """ SET 7,D - Set the specified bit """
    register.D = register.D | 0b10000000
    return 8


def code_cb_fb(register):
    """ SET 7,E - Set the specified bit """
    register.E = register.E | 0b10000000
    return 8


def code_cb_fc(register):
    """ SET 7,H - Set the specified bit """
    register.H = register.H | 0b10000000
    return 8


def code_cb_fd(register):
    """ SET 7,L - Set the specified bit """
    register.L = register.L | 0b10000000
    return 8


def code_cb_fe(register):
    """ SET 7,(HL) - Set the specified bit """
    # TODO after memory is implemented
    # register.B = register.B | 0b10000000
    return 16


def code_cb_ff(register):
    """ SET 7,A - Set the specified bit """
    register.A = register.A | 0b10000000
    return 8
