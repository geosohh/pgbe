"""
CPU Operations Codes

See:
- http://www.pastraiser.com/cpu/gameboy/gameboy_opcodes.html
- https://realboyemulator.files.wordpress.com/2013/01/gbcpuman.pdf (pages 61-118)
- https://datacrystal.romhacking.net/wiki/Endianness
- http://gameboy.mongenel.com/dmg/lesson1.html
- http://gameboy.mongenel.com/dmg/lesson2.html
- http://gameboy.mongenel.com/dmg/lesson3.html
- http://gameboy.mongenel.com/dmg/lesson4.html

- http://gbdev.gg8.se/files/docs/mirrors/pandocs.html#cpuinstructionset
- https://github.com/CTurt/Cinoop/blob/master/source/cpu.c
- https://github.com/CTurt/Cinoop/blob/master/source/memory.c
- https://github.com/xerpi/realboy-vita/blob/master/src/gboy_cpu.c

The Game Boy uses Little-endian, i.e. least significant byte first. Therefore, in order to properly execute opcodes
values have to be converted to Big-endian first.
"""


def execute(cpu,opcode):
    """
    Called by the CPU to execute an instruction.
    
    :param cpu: CPU instance 
    :param opcode: Instruction to execute
    """
    _instruction_dict[opcode](cpu)


def get_big_endian_value(msb, lsb):
    """
    Joins the two bytes received from the cartridge into a single, big-endian value.

    :param msb: Most significant byte
    :param lsb: Least significant byte
    :return: Big-endian value
    """
    return (msb << 8) | lsb


def get_little_endian_value(msb, lsb):
    """
    Joins the two bytes received from the cartridge into a single, little-endian value.

    :param msb: Most significant byte
    :param lsb: Least significant byte
    :return: Little-endian value
    """
    return (lsb << 8) | msb


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


# OPCODES 0x
# noinspection PyUnusedLocal
def code_00(cpu):
    """ NOP - Does nothing """
    return 4


def code_01(cpu):
    """ LD BC,d16 - Stores given 16-bit value at BC """
    lsb = cpu.read_next_byte_from_cartridge()
    msb = cpu.read_next_byte_from_cartridge()
    d16 = get_big_endian_value(msb, lsb)
    cpu.register.set_bc(d16)
    return 8


def code_02(cpu):
    """ LD (BC),A - Stores reg at the address in BC """
    a16 = cpu.register.get_bc()
    cpu.memory.write_8bit(a16,cpu.register.A)
    return 8


def code_03(cpu):
    """ INC BC - BC=BC+1 """
    cpu.register.set_bc((cpu.register.get_bc() + 1) & 0xFFFF)
    return 8


def code_04(cpu):
    """ INC B - B=B+1 """
    cpu.register.B = (cpu.register.B + 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.B == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag((cpu.register.B & 0x0F) == 0)
    return 4


def code_05(cpu):
    """ DEC B - B=B-1 """
    cpu.register.B = (cpu.register.B - 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.B == 0)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((cpu.register.B & 0x0F) == 0x0F)
    return 4


def code_06(cpu, d8):
    """ LD B,d8 """
    cpu.register.B = d8
    return 8


def code_07(cpu):
    """ RLCA - Copy register A bit 7 to Carry flag, then rotate register A left """
    bit_7 = cpu.register.A >> 7
    cpu.register.A = ((cpu.register.A << 1) + bit_7) & 0xFF
    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_7)
    return 4


def code_08(cpu):
    """ LD (a16),SP - Set SP value into address (a16) """
    lsb = cpu.read_next_byte_from_cartridge()
    msb = cpu.read_next_byte_from_cartridge()
    a16 = get_big_endian_value(msb, lsb)
    cpu.memory.write_16bit(a16,cpu.register.SP)
    return 20


def code_09(cpu):
    """ ADD HL,BC - HL=HL+BC """
    result = cpu.register.get_hl() + cpu.register.get_bc()
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(((cpu.register.get_hl() & 0x0FFF) + (cpu.register.get_bc() & 0x0FFF)) > 0x0FFF)
    cpu.register.set_c_flag(result > 0xFFFF)
    cpu.register.set_hl(result & 0xFFFF)
    return 8


def code_0a(cpu):
    """ LD A,(BC) - Load (value at the address in BC) to the register """
    d8 = cpu.memory.read_8bit(cpu.register.get_bc())
    cpu.register.A = d8
    return 8


def code_0b(cpu):
    """ DEC BC - BC=BC-1 """
    cpu.register.set_bc((cpu.register.get_bc() - 1) & 0xFFFF)
    return 8


def code_0c(cpu):
    """ INC C - C=C+1 """
    cpu.register.C = (cpu.register.C + 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.C == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag((cpu.register.C & 0x0F) == 0)
    return 4


def code_0d(cpu):
    """ DEC C - C=C-1 """
    cpu.register.C = (cpu.register.C - 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.C == 0)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((cpu.register.C & 0x0F) == 0x0F)
    return 4


def code_0e(cpu, d8):
    """ LD C,d8 """
    cpu.register.C = d8
    return 8


def code_0f(cpu):
    """ RRCA - Copy register A bit 0 to Carry flag, then rotate register A right """
    bit_0 = cpu.register.A & 0b00000001
    cpu.register.A = ((bit_0 << 7) + (cpu.register.A >> 1)) & 0xFF
    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 4


# OPCODES 1x
def code_10(cpu):
    """
    STOP - Switch Game Boy into VERY low power standby mode. Halt CPU and LCD display until a button is pressed
    See: http://gbdev.gg8.se/wiki/articles/Reducing_Power_Consumption
    """
    # TODO after cpu and interrupts are implemented
    pass


def code_11(cpu, d16):
    """ LD DE,d16 - Stores given 16-bit value at DE """
    d16 = cpu.util.convert_little_endian_to_big_endian(d16)
    cpu.register.set_de(d16)
    return 12


def code_12(cpu):
    """ LD (DE),A - Stores reg at the address in DE """
    # TODO after memory is implemented
    pass


def code_13(cpu):
    """ INC DE - DE=DE+1 """
    cpu.register.set_de((cpu.register.get_de() + 1) & 0xFFFF)
    return 8


def code_14(cpu):
    """ INC D - D=D+1 """
    cpu.register.D = (cpu.register.D + 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.D == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag((cpu.register.D & 0x0F) == 0)
    return 4


def code_15(cpu):
    """ DEC D - D=D-1 """
    cpu.register.D = (cpu.register.D - 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.D == 0)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((cpu.register.D & 0x0F) == 0x0F)
    return 4


def code_16(cpu, d8):
    """ LD D,d8 """
    cpu.register.D = d8
    return 8


def code_17(cpu):
    """ RLA - Copy register A bit 7 to temp, replace A bit 7 with Carry flag, rotate A left, copy temp to Carry flag """
    bit_7 = cpu.register.A >> 7
    cpu.register.A = ((cpu.register.A << 1) + cpu.register.get_c_flag()) & 0xFF
    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_7)
    return 4


def code_18(cpu, r8):
    """ JP r8 - Add r8 to the current address and jump to it """
    r8 = cpu.util.convert_unsigned_integer_to_signed(r8)
    # TODO after cpu is implemented
    return 8


def code_19(cpu):
    """ ADD HL,DE - HL=HL+DE """
    result = cpu.register.get_hl() + cpu.register.get_de()

    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(((cpu.register.get_hl() & 0x0FFF) + (cpu.register.get_de() & 0x0FFF)) > 0x0FFF)
    cpu.register.set_c_flag(result > 0xFFFF)

    cpu.register.set_hl(result & 0xFFFF)
    return 8


def code_1a(cpu):
    """ LD A,(DE) - Load reg with the value at the address in DE """
    # TODO after memory is implemented
    pass


def code_1b(cpu):
    """ DEC DE - DE=DE-1 """
    cpu.register.set_de((cpu.register.get_de() - 1) & 0xFFFF)
    return 8


def code_1c(cpu):
    """ INC E - E=E+1 """
    cpu.register.E = (cpu.register.E + 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.E == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag((cpu.register.E & 0x0F) == 0)
    return 4


def code_1d(cpu):
    """ DEC E - E=E-1 """
    cpu.register.E = (cpu.register.E - 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.E == 0)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((cpu.register.E & 0x0F) == 0x0F)
    return 4


def code_1e(cpu, d8):
    """ LD E,d8 """
    cpu.register.E = d8
    return 8


def code_1f(cpu):
    """ RRA - Copy register A bit 0 to temp, replace A bit 0 w/ Carry flag, rotate A right, copy temp to Carry flag """
    bit_0 = cpu.register.A & 0b00000001
    cpu.register.A = ((cpu.register.get_c_flag() << 7) + (cpu.register.A >> 1)) & 0xFF
    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 4


# OPCODES 2x
def code_20(cpu, r8):
    """ JR NZ,r8 - If flag Z is reset, add r8 to current address and jump to it """
    if not cpu.register.get_z_flag():
        r8 = cpu.util.convert_unsigned_integer_to_signed(r8)
        # TODO after cpu is implemented
        pass
    return 8


def code_21(cpu, d16):
    """ LD HL,d16 - Stores given 16-bit value at HL """
    d16 = cpu.util.convert_little_endian_to_big_endian(d16)
    cpu.register.set_hl(d16)
    return 12


def code_22(cpu):
    """ LD (HL+),A or LD (HLI),A or LDI (HL),A - Put value at A into address HL. Increment HL """
    # TODO after memory is implemented
    cpu.register.add_hl(0x0001)  # TODO: what if HL is already 0xFFFF?


def code_23(cpu):
    """ INC HL - HL=HL+1 """
    cpu.register.set_hl((cpu.register.get_hl() + 1) & 0xFFFF)
    return 8


def code_24(cpu):
    """ INC H - H=H+1 """
    cpu.register.H = (cpu.register.H + 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.H == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag((cpu.register.H & 0x0F) == 0)
    return 4


def code_25(cpu):
    """ DEC H - H=H-1 """
    cpu.register.H = (cpu.register.H - 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.H == 0)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((cpu.register.H & 0x0F) == 0x0F)
    return 4


def code_26(cpu, d8):
    """ LD H,d8 """
    cpu.register.H = d8
    return 8


def code_27(cpu):
    """
    DAA - Adjust value in register A for Binary Coded Decimal representation
    See:  http://gbdev.gg8.se/wiki/articles/DAA
    """
    n_flag = cpu.register.get_n_flag()
    h_flag = cpu.register.get_h_flag()
    c_flag = cpu.register.get_c_flag()
    if n_flag:
        if c_flag:
            cpu.register.A = (cpu.register.A - 0x60) & 0xFF
        if h_flag:
            cpu.register.A = (cpu.register.A - 0x06) & 0xFF
    else:
        if c_flag or cpu.register.A > 0x99:
            cpu.register.A = (cpu.register.A + 0x60) & 0xFF
            cpu.register.set_c_flag(True)
        if h_flag or (cpu.register.A & 0x0F) > 0x09:
            cpu.register.A = (cpu.register.A + 0x06) & 0xFF

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_h_flag(False)
    return 4


def code_28(cpu, r8):
    """ JR Z,r8 - If flag Z is set, add r8 to current address and jump to it """
    if cpu.register.get_z_flag():
        r8 = cpu.util.convert_unsigned_integer_to_signed(r8)
        # TODO after cpu is implemented
        pass
    return 8


def code_29(cpu):
    """ ADD HL,HL - HL=HL+HL """
    result = cpu.register.get_hl() * 2

    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(((cpu.register.get_hl() & 0x0FFF) * 2) > 0x0FFF)
    cpu.register.set_c_flag(result > 0xFFFF)

    cpu.register.set_hl(result & 0xFFFF)
    return 8


def code_2a(cpu):
    """ LD A,(HL+) or LD A,(HLI) or LDI A,(HL) - Put value at address HL into A. Increment HL """
    # TODO after memory is implemented
    cpu.register.add_hl(0x0001)  # TODO: what if HL is already 0xFFFF?


def code_2b(cpu):
    """ DEC HL - HL=HL-1 """
    cpu.register.set_hl((cpu.register.get_hl() - 1) & 0xFFFF)
    return 8


def code_2c(cpu):
    """ INC L - L=L+1 """
    cpu.register.L = (cpu.register.L + 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.L == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag((cpu.register.L & 0x0F) == 0)
    return 4


def code_2d(cpu):
    """ DEC L - L=L-1 """
    cpu.register.L = (cpu.register.L - 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.L == 0)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((cpu.register.L & 0x0F) == 0x0F)
    return 4


def code_2e(cpu, d8):
    """ LD L,d8 """
    cpu.register.L = d8
    return 8


def code_2f(cpu):
    """ CPL - Logical complement of register A (i.e. flip all bits) """
    cpu.register.A = (~ cpu.register.A) & 0xFF
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag(True)
    return 4


# OPCODES 3x
def code_30(cpu, r8):
    """ JR NC,r8 - If flag C is reset, add r8 to current address and jump to it """
    if not cpu.register.get_c_flag():
        r8 = cpu.util.convert_unsigned_integer_to_signed(r8)
        # TODO after cpu is implemented
        pass
    return 8


def code_31(cpu, d16):
    """ LD SP,d16 - Stores given 16-bit value at SP """
    d16 = cpu.util.convert_little_endian_to_big_endian(d16)
    cpu.register.SP = d16
    return 12


def code_32(cpu):
    """ LD (HL-),A or LD (HLD),A or LDD (HL),A - Put value at A into address HL. Decrement HL """
    # TODO after memory is implemented
    cpu.register.sub_hl(0x0001)  # TODO: what if HL is already 0x0000?


def code_33(cpu):
    """ INC SP - SP=SP+1 """
    cpu.register.SP = (cpu.register.SP + 1) & 0xFFFF
    return 8


def code_34(cpu):
    """ INC (HL) - (value at address HL)=(value at address HL)+1 """
    # TODO after memory is implemented
    # cpu.register.L = (cpu.register.L + 1) & 0xFF
    # cpu.register.set_zero_flag(cpu.register.L == 0)
    cpu.register.set_n_flag(False)
    # cpu.register.set_half_carry_flag((cpu.register.L & 0x0F) == 0)
    return 12


def code_35(cpu):
    """ DEC (HL) - (value at address HL)=(value at address HL)-1 """
    # TODO after memory is implemented
    # cpu.register.L = (cpu.register.L - 1) & 0xFF
    # cpu.register.set_zero_flag(cpu.register.L == 0)
    cpu.register.set_n_flag(True)
    # cpu.register.set_half_carry_flag((cpu.register.L & 0x0F) == 0x0F)
    return 12


def code_36(cpu, d8):
    """ LD (HL),d8 - Stores d8 at the address in HL """
    # TODO after memory is implemented
    pass


def code_37(cpu):
    """ SCF - Set carry flag """
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(True)
    return 4


def code_38(cpu, r8):
    """ JR C,r8 - If flag C is set, add r8 to current address and jump to it """
    if cpu.register.get_c_flag():
        r8 = cpu.util.convert_unsigned_integer_to_signed(r8)
        # TODO after cpu is implemented
        pass
    return 8


def code_39(cpu):
    """ ADD HL,SP - HL=HL+SP """
    result = cpu.register.get_hl() + cpu.register.SP

    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(((cpu.register.get_hl() & 0x0FFF) + (cpu.register.SP & 0x0FFF)) > 0x0FFF)
    cpu.register.set_c_flag(result > 0xFFFF)

    cpu.register.set_hl(result & 0xFFFF)
    return 8


def code_3a(cpu):
    """ LD A,(HL-) or LD A,(HLD) or LDD A,(HL) - Put value at address HL into A. Decrement HL """
    # TODO after memory is implemented
    cpu.register.sub_hl(0x0001)  # TODO: what if HL is already 0x0000?


def code_3b(cpu):
    """ DEC SP - SP=SP-1 """
    cpu.register.SP = (cpu.register.SP - 1) & 0xFFFF
    return 8


def code_3c(cpu):
    """ INC A - A=A+1 """
    cpu.register.A = (cpu.register.A + 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag((cpu.register.A & 0x0F) == 0)
    return 4


def code_3d(cpu):
    pass


def code_3e(cpu, d8):
    """ LD A,d8 """
    cpu.register.A = d8
    return 8


def code_3f(cpu):
    """ CCF - Invert carry flag """
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(not cpu.register.get_c_flag())
    return 4


# OPCODES 4x
def code_40(cpu):
    """ LD B,B (might be a newbie question but... why?) """
    cpu.register.B = cpu.register.B
    return 4


def code_41(cpu):
    """ LD B,C """
    cpu.register.B = cpu.register.C
    return 4


def code_42(cpu):
    """ LD B,D """
    cpu.register.B = cpu.register.D
    return 4


def code_43(cpu):
    """ LD B,E """
    cpu.register.B = cpu.register.E
    return 4


def code_44(cpu):
    """ LD B,H """
    cpu.register.B = cpu.register.H
    return 4


def code_45(cpu):
    """ LD B,L """
    cpu.register.B = cpu.register.L
    return 4


def code_46(cpu):
    """ LD B,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


def code_47(cpu):
    """ LD B,A """
    cpu.register.B = cpu.register.A
    return 4


def code_48(cpu):
    """ LD C,B """
    cpu.register.C = cpu.register.B
    return 4


def code_49(cpu):
    """ LD C,C (might be a newbie question but... why?) """
    cpu.register.C = cpu.register.C
    return 4


def code_4a(cpu):
    """ LD C,D """
    cpu.register.C = cpu.register.D
    return 4


def code_4b(cpu):
    """ LD C,E """
    cpu.register.C = cpu.register.E
    return 4


def code_4c(cpu):
    """ LD C,H """
    cpu.register.C = cpu.register.H
    return 4


def code_4d(cpu):
    """ LD C,L """
    cpu.register.C = cpu.register.L
    return 4


def code_4e(cpu):
    """ LD C,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


def code_4f(cpu):
    """ LD C,A """
    cpu.register.C = cpu.register.A
    return 4


# OPCODES 5x
def code_50(cpu):
    """ LD D,B """
    cpu.register.D = cpu.register.B
    return 4


def code_51(cpu):
    """ LD D,C """
    cpu.register.D = cpu.register.C
    return 4


def code_52(cpu):
    """ LD D,D (might be a newbie question but... why?) """
    cpu.register.D = cpu.register.D
    return 4


def code_53(cpu):
    """ LD D,E """
    cpu.register.D = cpu.register.E
    return 4


def code_54(cpu):
    """ LD D,H """
    cpu.register.D = cpu.register.H
    return 4


def code_55(cpu):
    """ LD D,L """
    cpu.register.D = cpu.register.L
    return 4


def code_56(cpu):
    """ LD D,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


def code_57(cpu):
    """ LD D,A """
    cpu.register.D = cpu.register.A
    return 4


def code_58(cpu):
    """ LD E,B """
    cpu.register.E = cpu.register.B
    return 4


def code_59(cpu):
    """ LD E,C """
    cpu.register.E = cpu.register.C
    return 4


def code_5a(cpu):
    """ LD E,D """
    cpu.register.E = cpu.register.D
    return 4


def code_5b(cpu):
    """ LD E,E (might be a newbie question but... why?) """
    cpu.register.E = cpu.register.E
    return 4


def code_5c(cpu):
    """ LD E,H """
    cpu.register.E = cpu.register.H
    return 4


def code_5d(cpu):
    """ LD E,L """
    cpu.register.E = cpu.register.L
    return 4


def code_5e(cpu):
    """ LD E,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


def code_5f(cpu):
    """ LD E,A """
    cpu.register.E = cpu.register.A
    return 4


# OPCODES 6x
def code_60(cpu):
    """ LD H,B """
    cpu.register.H = cpu.register.B
    return 4


def code_61(cpu):
    """ LD H,C """
    cpu.register.H = cpu.register.C
    return 4


def code_62(cpu):
    """ LD H,D """
    cpu.register.H = cpu.register.D
    return 4


def code_63(cpu):
    """ LD H,E """
    cpu.register.H = cpu.register.E
    return 4


def code_64(cpu):
    """ LD H,H (might be a newbie question but... why?) """
    cpu.register.H = cpu.register.H
    return 4


def code_65(cpu):
    """ LD H,L """
    cpu.register.H = cpu.register.L
    return 4


def code_66(cpu):
    """ LD H,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


def code_67(cpu):
    """ LD H,A """
    cpu.register.H = cpu.register.A
    return 4


def code_68(cpu):
    """ LD L,B """
    cpu.register.L = cpu.register.B
    return 4


def code_69(cpu):
    """ LD L,C """
    cpu.register.L = cpu.register.C
    return 4


def code_6a(cpu):
    """ LD L,D """
    cpu.register.L = cpu.register.D
    return 4


def code_6b(cpu):
    """ LD L,E """
    cpu.register.L = cpu.register.E
    return 4


def code_6c(cpu):
    """ LD L,H """
    cpu.register.L = cpu.register.H
    return 4


def code_6d(cpu):
    """ LD L,L (might be a newbie question but... why?) """
    cpu.register.L = cpu.register.L
    return 4


def code_6e(cpu):
    """ LD L,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


def code_6f(cpu):
    """ LD L,A """
    cpu.register.L = cpu.register.A
    return 4


# OPCODES 7x
def code_70(cpu):
    """ LD (HL),B - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


def code_71(cpu):
    """ LD (HL),C - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


def code_72(cpu):
    """ LD (HL),D - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


def code_73(cpu):
    """ LD (HL),E - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


def code_74(cpu):
    """ LD (HL),H - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


def code_75(cpu):
    """ LD (HL),L - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


def code_76(cpu):
    """
    HALT - Power down CPU (by stopping the system clock) until an interrupt occurs
    See: http://gbdev.gg8.se/wiki/articles/Reducing_Power_Consumption
    """
    # TODO after cpu and interrupts are implemented
    pass


def code_77(cpu):
    """ LD (HL),A - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


def code_78(cpu):
    """ LD A,B """
    cpu.register.A = cpu.register.B
    return 4


def code_79(cpu):
    """ LD A,C """
    cpu.register.A = cpu.register.C
    return 4


def code_7a(cpu):
    """ LD A,D """
    cpu.register.A = cpu.register.D
    return 4


def code_7b(cpu):
    """ LD A,E """
    cpu.register.A = cpu.register.E
    return 4


def code_7c(cpu):
    """ LD A,H """
    cpu.register.A = cpu.register.H
    return 4


def code_7d(cpu):
    """ LD A,L """
    cpu.register.A = cpu.register.L
    return 4


def code_7e(cpu):
    """ LD A,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


def code_7f(cpu):
    """ LD A,A (might be a newbie question but... why?) """
    cpu.register.A = cpu.register.A
    return 4


# OPCODES 8x
def code_80(cpu):
    """ ADD A,B - A=A+B """
    result = cpu.register.A + cpu.register.B

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(((cpu.register.A & 0x0F) + (cpu.register.B & 0x0F)) > 0x0F)
    cpu.register.set_c_flag(result > 0xFF)

    cpu.register.A = result & 0xFF
    return 4


def code_81(cpu):
    """ ADD A,C - A=A+C """
    result = cpu.register.A + cpu.register.C

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(((cpu.register.A & 0x0F) + (cpu.register.C & 0x0F)) > 0x0F)
    cpu.register.set_c_flag(result > 0xFF)

    cpu.register.A = result & 0xFF
    return 4


def code_82(cpu):
    """ ADD A,D - A=A+D """
    result = cpu.register.A + cpu.register.D

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(((cpu.register.A & 0x0F) + (cpu.register.D & 0x0F)) > 0x0F)
    cpu.register.set_c_flag(result > 0xFF)

    cpu.register.A = result & 0xFF
    return 4


def code_83(cpu):
    """ ADD A,E - A=A+E """
    result = cpu.register.A + cpu.register.E

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(((cpu.register.A & 0x0F) + (cpu.register.E & 0x0F)) > 0x0F)
    cpu.register.set_c_flag(result > 0xFF)

    cpu.register.A = result & 0xFF
    return 4


def code_84(cpu):
    """ ADD A,H - A=A+H """
    result = cpu.register.A + cpu.register.H

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(((cpu.register.A & 0x0F) + (cpu.register.H & 0x0F)) > 0x0F)
    cpu.register.set_c_flag(result > 0xFF)

    cpu.register.A = result & 0xFF
    return 4


def code_85(cpu):
    """ ADD A,L - A=A+L """
    result = cpu.register.A + cpu.register.L

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(((cpu.register.A & 0x0F) + (cpu.register.L & 0x0F)) > 0x0F)
    cpu.register.set_c_flag(result > 0xFF)

    cpu.register.A = result & 0xFF
    return 4


def code_86(cpu):
    """ ADD A,(HL) - A=A+(value at address HL) """
    # TODO after memory is implemented
    # result = cpu.register.A + cpu.register.C

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(False)
    # cpu.register.set_half_carry_flag(((cpu.register.A & 0x0F) + (cpu.register.C & 0x0F)) > 0x0F)
    cpu.register.set_c_flag(result > 0xFF)

    cpu.register.A = result & 0xFF
    return 8


def code_87(cpu):
    """ ADD A,A - A=A+A """
    result = cpu.register.A + cpu.register.A

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(((cpu.register.A & 0x0F) + (cpu.register.A & 0x0F)) > 0x0F)
    cpu.register.set_c_flag(result > 0xFF)

    cpu.register.A = result & 0xFF
    return 4


def code_88(cpu):
    """ ADC A,B - A=A+B+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = cpu.register.get_c_flag()
    result = cpu.register.A + cpu.register.B + carry_flag

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(((cpu.register.A & 0x0F) + (cpu.register.B & 0x0F) + carry_flag) > 0x0F)
    cpu.register.set_c_flag(result > 0xFF)

    cpu.register.A = result & 0xFF
    return 4


def code_89(cpu):
    """ ADC A,C - A=A+C+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = cpu.register.get_c_flag()
    result = cpu.register.A + cpu.register.C + carry_flag

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(((cpu.register.A & 0x0F) + (cpu.register.C & 0x0F) + carry_flag) > 0x0F)
    cpu.register.set_c_flag(result > 0xFF)

    cpu.register.A = result & 0xFF
    return 4


def code_8a(cpu):
    """ ADC A,D - A=A+D+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = cpu.register.get_c_flag()
    result = cpu.register.A + cpu.register.D + carry_flag

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(((cpu.register.A & 0x0F) + (cpu.register.D & 0x0F) + carry_flag) > 0x0F)
    cpu.register.set_c_flag(result > 0xFF)

    cpu.register.A = result & 0xFF
    return 4


def code_8b(cpu):
    """ ADC A,E - A=A+E+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = cpu.register.get_c_flag()
    result = cpu.register.A + cpu.register.E + carry_flag

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(((cpu.register.A & 0x0F) + (cpu.register.E & 0x0F) + carry_flag) > 0x0F)
    cpu.register.set_c_flag(result > 0xFF)

    cpu.register.A = result & 0xFF
    return 4


def code_8c(cpu):
    """ ADC A,H - A=A+H+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = cpu.register.get_c_flag()
    result = cpu.register.A + cpu.register.H + carry_flag

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(((cpu.register.A & 0x0F) + (cpu.register.H & 0x0F) + carry_flag) > 0x0F)
    cpu.register.set_c_flag(result > 0xFF)

    cpu.register.A = result & 0xFF
    return 4


def code_8d(cpu):
    """ ADC A,L - A=A+L+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = cpu.register.get_c_flag()
    result = cpu.register.A + cpu.register.L + carry_flag

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(((cpu.register.A & 0x0F) + (cpu.register.L & 0x0F) + carry_flag) > 0x0F)
    cpu.register.set_c_flag(result > 0xFF)

    cpu.register.A = result & 0xFF
    return 4


def code_8e(cpu):
    """ ADC A,(HL) - A=A+(value at address HL)+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = cpu.register.get_c_flag()
    # TODO after memory is implemented
    # result = cpu.register.A + cpu.register.L + carry_flag

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(False)
    # cpu.register.set_half_carry_flag(((cpu.register.A & 0x0F) + (cpu.register.L & 0x0F) + carry_flag) > 0x0F)
    cpu.register.set_c_flag(result > 0xFF)

    cpu.register.A = result & 0xFF
    return 8


def code_8f(cpu):
    """ ADC A,A - A=A+A+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = cpu.register.get_c_flag()
    result = cpu.register.A + cpu.register.A + carry_flag

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(((cpu.register.A & 0x0F) + (cpu.register.A & 0x0F) + carry_flag) > 0x0F)
    cpu.register.set_c_flag(result > 0xFF)

    cpu.register.A = result & 0xFF
    return 4


# OPCODES 9x
def code_90(cpu):
    """ SUB A,B - A=A-B """
    result = (cpu.register.A - cpu.register.B) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((cpu.register.B & 0x0F) > (cpu.register.A & 0x0F))
    cpu.register.set_c_flag(cpu.register.B > cpu.register.A)

    cpu.register.A = result
    return 4


def code_91(cpu):
    """ SUB A,C - A=A-C """
    result = (cpu.register.A - cpu.register.C) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((cpu.register.C & 0x0F) > (cpu.register.A & 0x0F))
    cpu.register.set_c_flag(cpu.register.C > cpu.register.A)

    cpu.register.A = result
    return 4


def code_92(cpu):
    """ SUB A,D - A=A-D """
    result = (cpu.register.A - cpu.register.D) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((cpu.register.D & 0x0F) > (cpu.register.A & 0x0F))
    cpu.register.set_c_flag(cpu.register.D > cpu.register.A)

    cpu.register.A = result
    return 4


def code_93(cpu):
    """ SUB A,E - A=A-E """
    result = (cpu.register.A - cpu.register.E) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((cpu.register.E & 0x0F) > (cpu.register.A & 0x0F))
    cpu.register.set_c_flag(cpu.register.E > cpu.register.A)

    cpu.register.A = result
    return 4


def code_94(cpu):
    """ SUB A,H - A=A-H """
    result = (cpu.register.A - cpu.register.H) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((cpu.register.H & 0x0F) > (cpu.register.A & 0x0F))
    cpu.register.set_c_flag(cpu.register.H > cpu.register.A)

    cpu.register.A = result
    return 4


def code_95(cpu):
    """ SUB A,L - A=A-L """
    result = (cpu.register.A - cpu.register.L) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((cpu.register.L & 0x0F) > (cpu.register.A & 0x0F))
    cpu.register.set_c_flag(cpu.register.L > cpu.register.A)

    cpu.register.A = result
    return 4


def code_96(cpu):
    """ SUB A,(HL) - A=A-(value at address HL) """
    # TODO after memory is implemented
    # result = (cpu.register.A - cpu.register.B) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(True)
    # cpu.register.set_half_carry_flag((cpu.register.B & 0x0F) > (cpu.register.A & 0x0F))
    # cpu.register.set_carry_flag(cpu.register.B > cpu.register.A)

    cpu.register.A = result
    return 8


def code_97(cpu):
    """ SUB A,A - A=A-A """
    cpu.register.set_z_flag(True)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)

    cpu.register.A = 0x00  # A-A, therefore result is zero, always
    return 4


def code_98(cpu):
    """ SBC A,B - A=A-B-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    value = cpu.register.B + cpu.register.get_c_flag()
    result = (cpu.register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((value & 0x0F) > (cpu.register.A & 0x0F))
    cpu.register.set_c_flag(value > cpu.register.A)

    cpu.register.A = result
    return 4


def code_99(cpu):
    """ SBC A,C - A=A-C-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    value = cpu.register.C + cpu.register.get_c_flag()
    result = (cpu.register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((value & 0x0F) > (cpu.register.A & 0x0F))
    cpu.register.set_c_flag(value > cpu.register.A)

    cpu.register.A = result
    return 4


def code_9a(cpu):
    """ SBC A,D - A=A-D-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    value = cpu.register.D + cpu.register.get_c_flag()
    result = (cpu.register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((value & 0x0F) > (cpu.register.A & 0x0F))
    cpu.register.set_c_flag(value > cpu.register.A)

    cpu.register.A = result
    return 4


def code_9b(cpu):
    """ SBC A,E - A=A-E-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    value = cpu.register.E + cpu.register.get_c_flag()
    result = (cpu.register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((value & 0x0F) > (cpu.register.A & 0x0F))
    cpu.register.set_c_flag(value > cpu.register.A)

    cpu.register.A = result
    return 4


def code_9c(cpu):
    """ SBC A,H - A=A-H-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    value = cpu.register.H + cpu.register.get_c_flag()
    result = (cpu.register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((value & 0x0F) > (cpu.register.A & 0x0F))
    cpu.register.set_c_flag(value > cpu.register.A)

    cpu.register.A = result
    return 4


def code_9d(cpu):
    """ SBC A,L - A=A-L-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    value = cpu.register.L + cpu.register.get_c_flag()
    result = (cpu.register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((value & 0x0F) > (cpu.register.A & 0x0F))
    cpu.register.set_c_flag(value > cpu.register.A)

    cpu.register.A = result
    return 4


def code_9e(cpu):
    """ SBC A,(HL) - A=A-(value at address HL)-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    # TODO after memory is implemented
    # value = cpu.register.L + cpu.register.get_carry_flag()
    result = (cpu.register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((value & 0x0F) > (cpu.register.A & 0x0F))
    cpu.register.set_c_flag(value > cpu.register.A)

    cpu.register.A = result
    return 8


def code_9f(cpu):
    """ SBC A,A - A=A-A-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    carry_flag = cpu.register.get_c_flag()
    result = (-carry_flag) & 0xFF  # A-A-carry_flag, therefore result is -carry_flag, always

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag(carry_flag)
    cpu.register.set_c_flag(carry_flag)

    cpu.register.A = result
    return 4


# OPCODES Ax
def code_a0(cpu):
    """ AND B - A=Logical AND A with B """
    cpu.register.A = cpu.register.A & cpu.register.B

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    cpu.register.set_c_flag(False)

    return 4


def code_a1(cpu):
    """ AND C - A=Logical AND A with C """
    cpu.register.A = cpu.register.A & cpu.register.C

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    cpu.register.set_c_flag(False)

    return 4


def code_a2(cpu):
    """ AND D - A=Logical AND A with D """
    cpu.register.A = cpu.register.A & cpu.register.D

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    cpu.register.set_c_flag(False)

    return 4


def code_a3(cpu):
    """ AND E - A=Logical AND A with E """
    cpu.register.A = cpu.register.A & cpu.register.E

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    cpu.register.set_c_flag(False)

    return 4


def code_a4(cpu):
    """ AND H - A=Logical AND A with H """
    cpu.register.A = cpu.register.A & cpu.register.H

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    cpu.register.set_c_flag(False)

    return 4


def code_a5(cpu):
    """ AND L - A=Logical AND A with L """
    cpu.register.A = cpu.register.A & cpu.register.L

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    cpu.register.set_c_flag(False)

    return 4


def code_a6(cpu):
    """ AND (HL) - A=Logical AND A with (value at address HL) """
    # TODO after memory is implemented
    # cpu.register.A = cpu.register.A & cpu.register.B

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    cpu.register.set_c_flag(False)

    return 8


def code_a7(cpu):
    """ AND A - A=Logical AND A with A (why?) """
    # cpu.register.A = cpu.register.A & cpu.register.A -- result is A=A, therefore useless

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    cpu.register.set_c_flag(False)

    return 4


def code_a8(cpu):
    """ XOR B - A=Logical XOR A with B """
    cpu.register.A = cpu.register.A ^ cpu.register.B

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)

    return 4


def code_a9(cpu):
    """ XOR C - A=Logical XOR A with C """
    cpu.register.A = cpu.register.A ^ cpu.register.C

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)

    return 4


def code_aa(cpu):
    """ XOR D - A=Logical XOR A with D """
    cpu.register.A = cpu.register.A ^ cpu.register.D

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)

    return 4


def code_ab(cpu):
    """ XOR E - A=Logical XOR A with E """
    cpu.register.A = cpu.register.A ^ cpu.register.E

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)

    return 4


def code_ac(cpu):
    """ XOR H - A=Logical XOR A with H """
    cpu.register.A = cpu.register.A ^ cpu.register.H

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)

    return 4


def code_ad(cpu):
    """ XOR L - A=Logical XOR A with L """
    cpu.register.A = cpu.register.A ^ cpu.register.L

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)

    return 4


def code_ae(cpu):
    """ XOR (HL) - A=Logical XOR A with (value at address HL) """
    # TODO after memory is implemented
    # cpu.register.A = cpu.register.A ^ cpu.register.D

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)

    return 8


def code_af(cpu):
    """ XOR A - A=Logical XOR A with A """
    cpu.register.A = 0

    cpu.register.set_z_flag(True)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)

    return 4


# OPCODES Bx
def code_b0(cpu):
    """ OR B - A=Logical OR A with B """
    cpu.register.A = cpu.register.A | cpu.register.B

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)

    return 4


def code_b1(cpu):
    """ OR C - A=Logical OR A with C """
    cpu.register.A = cpu.register.A | cpu.register.C

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)

    return 4


def code_b2(cpu):
    """ OR D - A=Logical OR A with D """
    cpu.register.A = cpu.register.A | cpu.register.D

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)

    return 4


def code_b3(cpu):
    """ OR E - A=Logical OR A with E """
    cpu.register.A = cpu.register.A | cpu.register.E

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)

    return 4


def code_b4(cpu):
    """ OR H - A=Logical OR A with H """
    cpu.register.A = cpu.register.A | cpu.register.H

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)

    return 4


def code_b5(cpu):
    """ OR L - A=Logical OR A with L """
    cpu.register.A = cpu.register.A | cpu.register.L

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)

    return 4


def code_b6(cpu):
    """ OR (HL) - A=Logical OR A with (value at address HL) """
    # TODO after memory is implemented
    # cpu.register.A = cpu.register.A | cpu.register.B

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)

    return 8


def code_b7(cpu):
    """ OR L - A=Logical OR A with A (why?) """
    # cpu.register.A = cpu.register.A | cpu.register.A -- result is A=A, therefore useless

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)

    return 4


def code_b8(cpu):
    """ CP A,B - same as SUB A,B but throw the result away, only set flags """
    cpu.register.set_z_flag(cpu.register.A == cpu.register.B)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((cpu.register.B & 0x0F) > (cpu.register.A & 0x0F))
    cpu.register.set_c_flag(cpu.register.B > cpu.register.A)
    return 4


def code_b9(cpu):
    """ CP A,C - same as SUB A,C but throw the result away, only set flags """
    cpu.register.set_z_flag(cpu.register.A == cpu.register.C)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((cpu.register.C & 0x0F) > (cpu.register.A & 0x0F))
    cpu.register.set_c_flag(cpu.register.C > cpu.register.A)
    return 4


def code_ba(cpu):
    """ CP A,D - same as SUB A,D but throw the result away, only set flags """
    cpu.register.set_z_flag(cpu.register.A == cpu.register.D)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((cpu.register.D & 0x0F) > (cpu.register.A & 0x0F))
    cpu.register.set_c_flag(cpu.register.D > cpu.register.A)
    return 4


def code_bb(cpu):
    """ CP A,E - same as SUB A,E but throw the result away, only set flags """
    cpu.register.set_z_flag(cpu.register.A == cpu.register.E)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((cpu.register.E & 0x0F) > (cpu.register.A & 0x0F))
    cpu.register.set_c_flag(cpu.register.E > cpu.register.A)
    return 4


def code_bc(cpu):
    """ CP A,H - same as SUB A,H but throw the result away, only set flags """
    cpu.register.set_z_flag(cpu.register.A == cpu.register.H)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((cpu.register.H & 0x0F) > (cpu.register.A & 0x0F))
    cpu.register.set_c_flag(cpu.register.H > cpu.register.A)
    return 4


def code_bd(cpu):
    """ CP A,L - same as SUB A,L but throw the result away, only set flags """
    cpu.register.set_z_flag(cpu.register.A == cpu.register.L)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((cpu.register.L & 0x0F) > (cpu.register.A & 0x0F))
    cpu.register.set_c_flag(cpu.register.L > cpu.register.A)
    return 4


def code_be(cpu):
    """ CP A,(HL) - same as SUB A,(HL) but throw the result away, only set flags """
    # TODO after memory is implemented
    # cpu.register.set_zero_flag(cpu.register.A == cpu.register.B)
    cpu.register.set_n_flag(True)
    # cpu.register.set_half_carry_flag((cpu.register.B & 0x0F) > (cpu.register.A & 0x0F))
    # cpu.register.set_carry_flag(cpu.register.B > cpu.register.A)
    return 8


def code_bf(cpu):
    """ CP A,A - same as SUB A,A but throw the result away, only set flags """
    cpu.register.set_z_flag(True)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)
    return 4


# OPCODES Cx
def code_c0(cpu):
    """ RET NZ - Return if flag Z is reset """
    if not cpu.register.get_z_flag():
        # TODO: after cpu is implemented
        pass
    return 8


def code_c1(cpu):
    """ POP BC - Copy 16-bit value from stack (i.e. SP address) into BC, then increment SP by 2 """
    # TODO after memory is implemented
    cpu.register.SP += 2
    return 12


def code_c2(cpu, a16):
    """ JP NZ,a16 - Jump to address a16 if Z flag is reset """
    a16 = cpu.util.convert_little_endian_to_big_endian(a16)
    if not cpu.register.get_z_flag():
        # TODO: after memory and cpu are implemented
        pass
    return 12


def code_c3(cpu):
    """ JP a16 - Jump to address a16 """
    # TODO: after memory and cpu are implemented
    return 12


def code_c4(cpu, a16):
    """ CALL NZ,a16 - Call address a16 if flag Z is reset """
    if not cpu.register.get_z_flag():
        a16 = cpu.util.convert_little_endian_to_big_endian(a16)
        # TODO after cpu is implemented
        pass
    return 12


def code_c5(cpu):
    """ PUSH BC - Decrement SP by 2 then push BC value onto stack (i.e. SP address) """
    cpu.register.SP -= 2
    # TODO after memory is implemented
    return 16


def code_c6(cpu, d8):
    """ ADD A,d8 - A=A+d8 """
    result = cpu.register.A + d8

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(((cpu.register.A & 0x0F) + (d8 & 0x0F)) > 0x0F)
    cpu.register.set_c_flag(result > 0xFF)

    cpu.register.A = result & 0xFF
    return 8


def code_c7(cpu):
    """ RST 00H - Push present address onto stack, jump to address $0000 + 00H """
    # TODO: after memory and cpu are implemented
    return 32


def code_c8(cpu):
    """ RET Z - Return if flag Z is set """
    if cpu.register.get_z_flag():
        # TODO: after cpu is implemented
        pass
    return 8


def code_c9(cpu):
    """ RET - Pop two bytes from stask and jump to that address """
    # TODO: after cpu is implemented
    return 8


def code_ca(cpu, a16):
    """ JP Z,a16 - Jump to address a16 if Z flag is set """
    a16 = cpu.util.convert_little_endian_to_big_endian(a16)
    if cpu.register.get_z_flag():
        # TODO: after memory and cpu are implemented
        pass
    return 12


def code_cb(cpu):
    """ PREFIX CB - Prefix for accessing the extra CB functions """
    opcode = cpu.read_next_byte_from_cartridge()
    print("Executing CB {:02X} ".format(opcode))
    return 4 + _instruction_cb_dict[opcode](cpu)


def code_cc(cpu, a16):
    """ CALL Z,a16 - Call address a16 if flag Z is set """
    if cpu.register.get_z_flag():
        a16 = cpu.util.convert_little_endian_to_big_endian(a16)
        # TODO after cpu is implemented
        pass
    return 12


def code_cd(cpu, a16):
    """ CALL a16 - Push address of next instruction onto stack then jump to address a16 """
    a16 = cpu.util.convert_little_endian_to_big_endian(a16)
    # TODO: after cpu are implemented
    return 12


def code_ce(cpu, d8):
    """ ADC A,d8 - A=A+d8+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = cpu.register.get_c_flag()
    result = cpu.register.A + d8 + carry_flag

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(((cpu.register.A & 0x0F) + (d8 & 0x0F) + carry_flag) > 0x0F)
    cpu.register.set_c_flag(result > 0xFF)

    cpu.register.A = result & 0xFF
    return 8


def code_cf(cpu):
    """ RST 08H - Push present address onto stack, jump to address $0000 + 08H """
    # TODO: after memory and cpu are implemented
    return 32


# OPCODES Dx
def code_d0(cpu):
    """ RET NC - Return if flag C is reset """
    if not cpu.register.get_c_flag():
        # TODO: after cpu is implemented
        pass
    return 8


def code_d1(cpu):
    """ POP DE - Copy 16-bit value from stack (i.e. SP address) into DE, then increment SP by 2 """
    # TODO after memory is implemented
    cpu.register.SP += 2
    return 12


def code_d2(cpu, a16):
    """ JP NC,a16 - Jump to address a16 if C flag is reset """
    a16 = cpu.util.convert_little_endian_to_big_endian(a16)
    if not cpu.register.get_c_flag():
        # TODO: after memory and cpu are implemented
        pass
    return 12


def code_d3():
    """ Unused opcode """
    pass


def code_d4(cpu, a16):
    """ CALL NC,a16 - Call address a16 if flag C is reset """
    if not cpu.register.get_c_flag():
        a16 = cpu.util.convert_little_endian_to_big_endian(a16)
        # TODO after cpu is implemented
        pass
    return 12


def code_d5(cpu):
    """ PUSH DE - Decrement SP by 2 then push DE value onto stack (i.e. SP address) """
    cpu.register.SP -= 2
    # TODO after memory is implemented
    return 16


def code_d6(cpu, d8):
    """ SUB A,d8 - A=A-d8 """
    result = (cpu.register.A - d8) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((d8 & 0x0F) > (cpu.register.A & 0x0F))
    cpu.register.set_c_flag(d8 > cpu.register.A)

    cpu.register.A = result
    return 8


def code_d7(cpu):
    """ RST 10H - Push present address onto stack, jump to address $0000 + 10H """
    # TODO: after memory and cpu are implemented
    return 32


def code_d8(cpu):
    """ RET C - Return if flag C is set """
    if cpu.register.get_c_flag():
        # TODO: after cpu is implemented
        pass
    return 8


def code_d9(cpu):
    """ RETI - Pop two bytes from stask and jump to that address then enable interrupts """
    # TODO: after memory, cpu and interrupts are implemented
    return 8


def code_da(cpu):
    """ JP C,a16 - Jump to address a16 if C flag is set """
    a16 = cpu.util.convert_little_endian_to_big_endian(a16)
    if cpu.register.get_c_flag():
        # TODO: after memory and cpu are implemented
        pass
    return 12


def code_db():
    """ Unused opcode """
    pass


def code_dc(cpu, a16):
    """ CALL C,a16 - Call address a16 if flag C is set """
    if cpu.register.get_c_flag():
        a16 = cpu.util.convert_little_endian_to_big_endian(a16)
        # TODO after cpu is implemented
        pass
    return 12


def code_dd():
    """ Unused opcode """
    pass


def code_de(cpu, d8):
    """ SBC A,d8 - A=A-d8-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    value = d8 + cpu.register.get_c_flag()
    result = (cpu.register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned

    cpu.register.set_z_flag((result & 0xFF) == 0)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((value & 0x0F) > (cpu.register.A & 0x0F))
    cpu.register.set_c_flag(value > cpu.register.A)

    cpu.register.A = result
    return 8


def code_df(cpu):
    """ RST 18H - Push present address onto stack, jump to address $0000 + 18H """
    # TODO: after memory and cpu are implemented
    return 32


# OPCODES Ex
def code_e0(cpu, d8):
    """ LDH (d8),A or LD ($FF00+d8),A - Put A into address ($FF00 + d8) """
    # TODO after memory is implemented
    pass


def code_e1(cpu):
    """ POP HL - Copy 16-bit value from stack (i.e. SP address) into HL, then increment SP by 2 """
    # TODO after memory is implemented
    cpu.register.SP += 2
    return 12


def code_e2(cpu):
    """ LD (C),A or LD ($FF00+C),A - Put A into address ($FF00 + register C) """
    # TODO after memory is implemented
    pass


def code_e3():
    """ Unused opcode """
    pass


def code_e4():
    """ Unused opcode """
    pass


def code_e5(cpu):
    """ PUSH HL - Decrement SP by 2 then push HL value onto stack (i.e. SP address) """
    cpu.register.SP -= 2
    # TODO after memory is implemented
    return 16


def code_e6(cpu, d8):
    """ AND d8 - A=Logical AND A with d8 """
    cpu.register.A = cpu.register.A & d8

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    cpu.register.set_c_flag(False)

    return 8


def code_e7(cpu):
    """ RST 20H - Push present address onto stack, jump to address $0000 + 20H """
    # TODO: after memory and cpu are implemented
    return 32


def code_e8(cpu, r8):
    """ ADD SP,r8 - SP=SP+r8 (r8 is a signed value) """
    r8 = cpu.util.convert_unsigned_integer_to_signed(r8)
    result = cpu.register.SP + r8

    cpu.register.set_z_flag(False)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(((cpu.register.SP & 0x0F) + (r8 & 0x0F)) > 0x0F)
    cpu.register.set_c_flag(result > 0xFFFF)

    cpu.register.SP = result & 0xFFFF
    return 16


def code_e9(cpu):
    """ JP (HL) - Jump to address contained in HL """
    # TODO after memory and cpu is implemented
    return 4


def code_ea(cpu, a16):
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


def code_ee(cpu, d8):
    """ XOR d8 - A=Logical XOR A with d8 """
    cpu.register.A = cpu.register.A ^ d8

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)

    return 8


def code_ef(cpu):
    """ RST 28H - Push present address onto stack, jump to address $0000 + 28H """
    # TODO: after memory and cpu are implemented
    return 32


# OPCODES Fx
def code_f0(cpu, d8):
    """ LDH A,(d8) or LD A,($FF00+d8) - Put value at address ($FF00 + d8) into A """
    # TODO after memory is implemented
    pass


def code_f1(cpu):
    """ POP AF - Copy 16-bit value from stack (i.e. SP address) into AF, then increment SP by 2 """
    # TODO after memory is implemented
    cpu.register.SP += 2
    return 12


def code_f2(cpu):
    """ LD A,(C) or LD A,($FF00+C) - Put value at address ($FF00 + register C) into A """
    # TODO after memory is implemented
    pass


def code_f3(cpu):
    """ DI - Disable interrupts AFTER THE NEXT INSTRUCTION IS EXECUTED """
    # TODO after cpu and interrupts are implemented
    pass


def code_f4():
    """ Unused opcode """
    pass


def code_f5(cpu):
    """ PUSH AF - Decrement SP by 2 then push AF value onto stack (i.e. SP address) """
    cpu.register.SP -= 2
    # TODO after memory is implemented
    return 16


def code_f6(cpu, d8):
    """ OR d8 - A=Logical OR A with d8 """
    cpu.register.A = cpu.register.A | d8

    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)

    return 8


def code_f7(cpu):
    """ RST 30H - Push present address onto stack, jump to address $0000 + 30H """
    # TODO: after memory and cpu are implemented
    return 32


def code_f8(cpu, r8):
    """ LD HL,SP+d8 or LDHL SP,r8 - Put result of SP+r8 into HL (r8 is a signed value) """
    r8 = cpu.util.convert_unsigned_integer_to_signed(r8)
    result = cpu.register.SP + r8

    cpu.register.set_z_flag(False)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(((cpu.register.SP & 0x0F) + (r8 & 0x0F)) > 0x0F)
    cpu.register.set_c_flag(result > 0xFFFF)

    cpu.register.set_hl(result & 0xFFFF)
    return 12


def code_f9(cpu):
    """ LD SP,HL - Put HL value into SP """
    cpu.register.SP = cpu.register.get_hl()
    return 8


def code_fa(cpu, a16):
    """ LD A,(a16) - Load reg with the value at the address in a16 (least significant byte first) """
    a16 = cpu.util.convert_little_endian_to_big_endian(a16)
    # TODO after memory is implemented
    pass


def code_fb(cpu):
    """ EI - Enable interrupts AFTER THE NEXT INSTRUCTION IS EXECUTED """
    # TODO after cpu and interrupts are implemented
    pass


def code_fc():
    """ Unused opcode """
    pass


def code_fd():
    """ Unused opcode """
    pass


def code_fe(cpu, d8):
    """ CP A,d8 - same as SUB A,d8 but throw the result away, only set flags """
    cpu.register.set_z_flag(cpu.register.A == d8)
    cpu.register.set_n_flag(True)
    cpu.register.set_h_flag((d8 & 0x0F) > (cpu.register.A & 0x0F))
    cpu.register.set_c_flag(d8 > cpu.register.A)
    return 8


def code_ff(cpu):
    """ RST 38H - Push present address onto stack, jump to address $0000 + 38H """
    # TODO: after memory and cpu are implemented
    return 32


""" CB-Prefix operations """


# OPCODES CB 0x
def code_cb_00(cpu):
    """ RLC B - Copy register B bit 7 to Carry flag, then rotate register B left """
    bit_7 = cpu.register.B >> 7
    cpu.register.B = ((cpu.register.B << 1) + bit_7) & 0xFF
    cpu.register.set_z_flag(cpu.register.B == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_01(cpu):
    """ RLC C - Copy register C bit 7 to Carry flag, then rotate register C left """
    bit_7 = cpu.register.C >> 7
    cpu.register.C = ((cpu.register.C << 1) + bit_7) & 0xFF
    cpu.register.set_z_flag(cpu.register.C == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_02(cpu):
    """ RLC D - Copy register D bit 7 to Carry flag, then rotate register D left """
    bit_7 = cpu.register.D >> 7
    cpu.register.D = ((cpu.register.D << 1) + bit_7) & 0xFF
    cpu.register.set_z_flag(cpu.register.D == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_03(cpu):
    """ RLC E - Copy register E bit 7 to Carry flag, then rotate register E left """
    bit_7 = cpu.register.E >> 7
    cpu.register.E = ((cpu.register.E << 1) + bit_7) & 0xFF
    cpu.register.set_z_flag(cpu.register.E == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_04(cpu):
    """ RLC H - Copy register H bit 7 to Carry flag, then rotate register H left """
    bit_7 = cpu.register.H >> 7
    cpu.register.H = ((cpu.register.H << 1) + bit_7) & 0xFF
    cpu.register.set_z_flag(cpu.register.H == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_05(cpu):
    """ RLC L - Copy register L bit 7 to Carry flag, then rotate register L left """
    bit_7 = cpu.register.L >> 7
    cpu.register.L = ((cpu.register.L << 1) + bit_7) & 0xFF
    cpu.register.set_z_flag(cpu.register.L == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_06(cpu):
    """ RLC (HL) - Copy (value at address HL) bit 7 to Carry flag, then rotate (value at address HL) left """
    # TODO after memory is implemented
    # bit_7 = cpu.register.B >> 7
    # cpu.register.B = ((cpu.register.B << 1) + bit_7) & 0xFF
    # cpu.register.set_z_flag(cpu.register.B == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_7)
    return 16


def code_cb_07(cpu):
    """ RLC A - Copy register A bit 7 to Carry flag, then rotate register A left """
    code_07(cpu)  # Does exactly the same thing...
    return 8


def code_cb_08(cpu):
    """ RRC B - Copy register B bit 0 to Carry flag, then rotate register B right """
    bit_0 = cpu.register.B & 0b00000001
    cpu.register.B = ((bit_0 << 7) + (cpu.register.B >> 1)) & 0xFF
    cpu.register.set_z_flag(cpu.register.B == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_09(cpu):
    """ RRC C - Copy register C bit 0 to Carry flag, then rotate register C right """
    bit_0 = cpu.register.C & 0b00000001
    cpu.register.C = ((bit_0 << 7) + (cpu.register.C >> 1)) & 0xFF
    cpu.register.set_z_flag(cpu.register.C == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_0a(cpu):
    """ RRC D - Copy register D bit 0 to Carry flag, then rotate register D right """
    bit_0 = cpu.register.D & 0b00000001
    cpu.register.D = ((bit_0 << 7) + (cpu.register.D >> 1)) & 0xFF
    cpu.register.set_z_flag(cpu.register.D == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_0b(cpu):
    """ RRC E - Copy register E bit 0 to Carry flag, then rotate register E right """
    bit_0 = cpu.register.E & 0b00000001
    cpu.register.E = ((bit_0 << 7) + (cpu.register.E >> 1)) & 0xFF
    cpu.register.set_z_flag(cpu.register.E == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_0c(cpu):
    """ RRC H - Copy register H bit 0 to Carry flag, then rotate register H right """
    bit_0 = cpu.register.H & 0b00000001
    cpu.register.H = ((bit_0 << 7) + (cpu.register.H >> 1)) & 0xFF
    cpu.register.set_z_flag(cpu.register.H == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_0d(cpu):
    """ RRC L - Copy register L bit 0 to Carry flag, then rotate register L right """
    bit_0 = cpu.register.L & 0b00000001
    cpu.register.L = ((bit_0 << 7) + (cpu.register.L >> 1)) & 0xFF
    cpu.register.set_z_flag(cpu.register.L == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_0e(cpu):
    """ RRC (HL) - Copy bit 0 to Carry flag, then rotate right """
    # TODO after memory is implemented
    # bit_0 = cpu.register.B & 0b00000001
    # cpu.register.B = ((bit_0 << 7) + (cpu.register.B >> 1)) & 0xFF
    # cpu.register.set_z_flag(cpu.register.B == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 16


def code_cb_0f(cpu):
    """ RRCA - Copy register A bit 0 to Carry flag, then rotate register A right """
    code_0f(cpu)  # Does exactly the same thing...
    return 8


# OPCODES CB 1x
def code_cb_10(cpu):
    """ RL B - Copy register B bit 7 to temp, replace B bit 7 w/ Carry flag, rotate B left, copy temp to Carry flag """
    bit_7 = cpu.register.B >> 7
    cpu.register.B = ((cpu.register.B << 1) + cpu.register.get_c_flag()) & 0xFF
    cpu.register.set_z_flag(cpu.register.B == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_11(cpu):
    """ RL C - Copy register C bit 7 to temp, replace C bit 7 w/ Carry flag, rotate C left, copy temp to Carry flag """
    bit_7 = cpu.register.C >> 7
    cpu.register.C = ((cpu.register.C << 1) + cpu.register.get_c_flag()) & 0xFF
    cpu.register.set_z_flag(cpu.register.C == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_12(cpu):
    """ RL D - Copy register D bit 7 to temp, replace D bit 7 w/ Carry flag, rotate D left, copy temp to Carry flag """
    bit_7 = cpu.register.D >> 7
    cpu.register.D = ((cpu.register.D << 1) + cpu.register.get_c_flag()) & 0xFF
    cpu.register.set_z_flag(cpu.register.D == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_13(cpu):
    """ RL E - Copy register E bit 7 to temp, replace E bit 7 w/ Carry flag, rotate E left, copy temp to Carry flag """
    bit_7 = cpu.register.E >> 7
    cpu.register.E = ((cpu.register.E << 1) + cpu.register.get_c_flag()) & 0xFF
    cpu.register.set_z_flag(cpu.register.E == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_14(cpu):
    """ RL H - Copy register H bit 7 to temp, replace H bit 7 w/ Carry flag, rotate H left, copy temp to Carry flag """
    bit_7 = cpu.register.H >> 7
    cpu.register.H = ((cpu.register.H << 1) + cpu.register.get_c_flag()) & 0xFF
    cpu.register.set_z_flag(cpu.register.H == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_15(cpu):
    """ RL L - Copy register L bit 7 to temp, replace L bit 7 w/ Carry flag, rotate L left, copy temp to Carry flag """
    bit_7 = cpu.register.L >> 7
    cpu.register.L = ((cpu.register.L << 1) + cpu.register.get_c_flag()) & 0xFF
    cpu.register.set_z_flag(cpu.register.L == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_16(cpu):
    """ RL (HL) - Copy bit 7 to temp, replace bit 7 w/ Carry flag, rotate left, copy temp to Carry flag """
    # TODO after memory is implemented
    # bit_7 = cpu.register.B >> 7
    # cpu.register.B = ((cpu.register.B << 1) + cpu.register.get_c_flag()) & 0xFF
    # cpu.register.set_z_flag(cpu.register.B == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_7)
    return 16


def code_cb_17(cpu):
    """ RL A - Copy register A bit 7 to temp, replace A bit 7 w/ Carry flag, rotate A left, copy temp to Carry flag """
    code_17(cpu)  # Does exactly the same thing...
    return 8


def code_cb_18(cpu):
    """ RR B - Copy register B bit 0 to temp, replace bit 0 w/ Carry flag, rotate right, copy temp to Carry flag """
    bit_0 = cpu.register.B & 0b00000001
    cpu.register.B = ((cpu.register.get_c_flag() << 7) + (cpu.register.B >> 1)) & 0xFF
    cpu.register.set_z_flag(cpu.register.B == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_19(cpu):
    """ RR C - Copy register C bit 0 to temp, replace bit 0 w/ Carry flag, rotate right, copy temp to Carry flag """
    bit_0 = cpu.register.C & 0b00000001
    cpu.register.C = ((cpu.register.get_c_flag() << 7) + (cpu.register.C >> 1)) & 0xFF
    cpu.register.set_z_flag(cpu.register.C == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_1a(cpu):
    """ RR D - Copy register D bit 0 to temp, replace bit 0 w/ Carry flag, rotate right, copy temp to Carry flag """
    bit_0 = cpu.register.D & 0b00000001
    cpu.register.D = ((cpu.register.get_c_flag() << 7) + (cpu.register.D >> 1)) & 0xFF
    cpu.register.set_z_flag(cpu.register.D == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_1b(cpu):
    """ RR E - Copy register E bit 0 to temp, replace bit 0 w/ Carry flag, rotate right, copy temp to Carry flag """
    bit_0 = cpu.register.E & 0b00000001
    cpu.register.E = ((cpu.register.get_c_flag() << 7) + (cpu.register.E >> 1)) & 0xFF
    cpu.register.set_z_flag(cpu.register.E == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_1c(cpu):
    """ RR H - Copy register H bit 0 to temp, replace bit 0 w/ Carry flag, rotate right, copy temp to Carry flag """
    bit_0 = cpu.register.H & 0b00000001
    cpu.register.H = ((cpu.register.get_c_flag() << 7) + (cpu.register.H >> 1)) & 0xFF
    cpu.register.set_z_flag(cpu.register.H == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_1d(cpu):
    """ RR L - Copy register L bit 0 to temp, replace bit 0 w/ Carry flag, rotate right, copy temp to Carry flag """
    bit_0 = cpu.register.L & 0b00000001
    cpu.register.L = ((cpu.register.get_c_flag() << 7) + (cpu.register.L >> 1)) & 0xFF
    cpu.register.set_z_flag(cpu.register.L == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_1e(cpu):
    """ RR (HL) - Copy (HL) bit 0 to temp, replace bit 0 w/ Carry flag, rotate right, copy temp to Carry flag """
    # TODO after memory is implemented
    # bit_0 = cpu.register.B & 0b00000001
    # cpu.register.B = ((cpu.register.get_c_flag() << 7) + (cpu.register.B >> 1)) & 0xFF
    # cpu.register.set_z_flag(cpu.register.B == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 16


def code_cb_1f(cpu):
    """ RRA - Copy register A bit 0 to temp, replace A bit 0 w/ Carry flag, rotate A right, copy temp to Carry flag """
    code_1f(cpu)  # Does exactly the same thing...
    return 8


# OPCODES CB 2x
def code_cb_20(cpu):
    """ SLA B - Copy register B bit 7 to temp, replace B bit 7 w/ zero, rotate B left, copy temp to Carry flag """
    bit_7 = cpu.register.B >> 7
    cpu.register.B = (cpu.register.B << 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.B == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_21(cpu):
    """ SLA C - Copy register C bit 7 to temp, replace C bit 7 w/ zero, rotate C left, copy temp to Carry flag """
    bit_7 = cpu.register.C >> 7
    cpu.register.C = (cpu.register.C << 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.C == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_22(cpu):
    """ SLA D - Copy register D bit 7 to temp, replace D bit 7 w/ zero, rotate D left, copy temp to Carry flag """
    bit_7 = cpu.register.D >> 7
    cpu.register.D = (cpu.register.D << 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.D == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_23(cpu):
    """ SLA E - Copy register E bit 7 to temp, replace E bit 7 w/ zero, rotate E left, copy temp to Carry flag """
    bit_7 = cpu.register.E >> 7
    cpu.register.E = (cpu.register.E << 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.E == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_24(cpu):
    """ SLA H - Copy register H bit 7 to temp, replace H bit 7 w/ zero, rotate H left, copy temp to Carry flag """
    bit_7 = cpu.register.H >> 7
    cpu.register.H = (cpu.register.H << 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.H == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_25(cpu):
    """ SLA L - Copy register L bit 7 to temp, replace L bit 7 w/ zero, rotate L left, copy temp to Carry flag """
    bit_7 = cpu.register.L >> 7
    cpu.register.L = (cpu.register.L << 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.L == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_26(cpu):
    """ SLA (HL) - Copy bit 7 to temp, replace bit 7 w/ zero, rotate left, copy temp to Carry flag """
    # TODO after memory is implemented
    # bit_7 = cpu.register.B >> 7
    # cpu.register.B = (cpu.register.B << 1) & 0xFF
    # cpu.register.set_z_flag(cpu.register.B == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_7)
    return 16


def code_cb_27(cpu):
    """ SLA A - Copy register A bit 7 to temp, replace A bit 7 w/ zero, rotate A left, copy temp to Carry flag """
    bit_7 = cpu.register.A >> 7
    cpu.register.A = (cpu.register.A << 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_28(cpu):
    """ SRA B - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_7 = cpu.register.B >> 7
    bit_0 = cpu.register.B & 0b00000001
    cpu.register.B = ((bit_7 << 7) + (cpu.register.B >> 1)) & 0xFF
    cpu.register.set_z_flag(cpu.register.B == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_29(cpu):
    """ SRA C - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_7 = cpu.register.C >> 7
    bit_0 = cpu.register.C & 0b00000001
    cpu.register.C = ((bit_7 << 7) + (cpu.register.C >> 1)) & 0xFF
    cpu.register.set_z_flag(cpu.register.C == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_2a(cpu):
    """ SRA D - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_7 = cpu.register.D >> 7
    bit_0 = cpu.register.D & 0b00000001
    cpu.register.D = ((bit_7 << 7) + (cpu.register.D >> 1)) & 0xFF
    cpu.register.set_z_flag(cpu.register.D == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_2b(cpu):
    """ SRA E - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_7 = cpu.register.E >> 7
    bit_0 = cpu.register.E & 0b00000001
    cpu.register.E = ((bit_7 << 7) + (cpu.register.E >> 1)) & 0xFF
    cpu.register.set_z_flag(cpu.register.E == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_2c(cpu):
    """ SRA H - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_7 = cpu.register.H >> 7
    bit_0 = cpu.register.H & 0b00000001
    cpu.register.H = ((bit_7 << 7) + (cpu.register.H >> 1)) & 0xFF
    cpu.register.set_z_flag(cpu.register.H == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_2d(cpu):
    """ SRA L - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_7 = cpu.register.L >> 7
    bit_0 = cpu.register.L & 0b00000001
    cpu.register.L = ((bit_7 << 7) + (cpu.register.L >> 1)) & 0xFF
    cpu.register.set_z_flag(cpu.register.L == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_2e(cpu):
    """ SRA (HL) - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    # TODO after memory is implemented
    # bit_7 = cpu.register.B >> 7
    # bit_0 = cpu.register.B & 0b00000001
    # cpu.register.B = ((bit_7 << 7) + (cpu.register.B >> 1)) & 0xFF
    # cpu.register.set_z_flag(cpu.register.B == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 16


def code_cb_2f(cpu):
    """ SRA A - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_7 = cpu.register.A >> 7
    bit_0 = cpu.register.A & 0b00000001
    cpu.register.A = ((bit_7 << 7) + (cpu.register.A >> 1)) & 0xFF
    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 8


# OPCODES CB 3x
def code_cb_30(cpu):
    """ SWAP B - Swap upper and lower nibbles (nibble = 4 bits) """
    lower_nibble = cpu.register.B & 0x0F
    upper_nibble = (cpu.register.B >> 4) & 0x0F
    cpu.register.B = (lower_nibble << 4) | upper_nibble
    cpu.register.set_z_flag(cpu.register.B == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)
    return 8


def code_cb_31(cpu):
    """ SWAP C - Swap upper and lower nibbles (nibble = 4 bits) """
    lower_nibble = cpu.register.C & 0x0F
    upper_nibble = (cpu.register.C >> 4) & 0x0F
    cpu.register.C = (lower_nibble << 4) | upper_nibble
    cpu.register.set_z_flag(cpu.register.C == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)
    return 8


def code_cb_32(cpu):
    """ SWAP D - Swap upper and lower nibbles (nibble = 4 bits) """
    lower_nibble = cpu.register.D & 0x0F
    upper_nibble = (cpu.register.D >> 4) & 0x0F
    cpu.register.D = (lower_nibble << 4) | upper_nibble
    cpu.register.set_z_flag(cpu.register.D == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)
    return 8


def code_cb_33(cpu):
    """ SWAP E - Swap upper and lower nibbles (nibble = 4 bits) """
    lower_nibble = cpu.register.E & 0x0F
    upper_nibble = (cpu.register.E >> 4) & 0x0F
    cpu.register.E = (lower_nibble << 4) | upper_nibble
    cpu.register.set_z_flag(cpu.register.E == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)
    return 8


def code_cb_34(cpu):
    """ SWAP H - Swap upper and lower nibbles (nibble = 4 bits) """
    lower_nibble = cpu.register.H & 0x0F
    upper_nibble = (cpu.register.H >> 4) & 0x0F
    cpu.register.H = (lower_nibble << 4) | upper_nibble
    cpu.register.set_z_flag(cpu.register.H == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)
    return 8


def code_cb_35(cpu):
    """ SWAP L - Swap upper and lower nibbles (nibble = 4 bits) """
    lower_nibble = cpu.register.L & 0x0F
    upper_nibble = (cpu.register.L >> 4) & 0x0F
    cpu.register.L = (lower_nibble << 4) | upper_nibble
    cpu.register.set_z_flag(cpu.register.L == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)
    return 8


def code_cb_36(cpu):
    """ SWAP (HL) - Swap upper and lower nibbles (nibble = 4 bits) """
    # lower_nibble = cpu.register.C & 0x0F
    # upper_nibble = (cpu.register.C >> 4) & 0x0F
    # cpu.register.C = (lower_nibble << 4) | upper_nibble
    # cpu.register.set_z_flag(cpu.register.C == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)
    return 16


def code_cb_37(cpu):
    """ SWAP A - Swap upper and lower nibbles (nibble = 4 bits) """
    lower_nibble = cpu.register.A & 0x0F
    upper_nibble = (cpu.register.A >> 4) & 0x0F
    cpu.register.A = (lower_nibble << 4) | upper_nibble
    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(False)
    return 8


def code_cb_38(cpu):
    """ SRL B - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_0 = cpu.register.B & 0b00000001
    cpu.register.B = (cpu.register.B >> 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.B == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_39(cpu):
    """ SRL C - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_0 = cpu.register.C & 0b00000001
    cpu.register.C = (cpu.register.C >> 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.C == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_3a(cpu):
    """ SRL D - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_0 = cpu.register.D & 0b00000001
    cpu.register.D = (cpu.register.D >> 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.D == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_3b(cpu):
    """ SRL E - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_0 = cpu.register.E & 0b00000001
    cpu.register.E = (cpu.register.E >> 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.E == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_3c(cpu):
    """ SRL H - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_0 = cpu.register.H & 0b00000001
    cpu.register.H = (cpu.register.H >> 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.H == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_3d(cpu):
    """ SRL L - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_0 = cpu.register.L & 0b00000001
    cpu.register.L = (cpu.register.L >> 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.L == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_3e(cpu):
    """ SRL (HL) - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    # TODO after memory is implemented
    # bit_0 = cpu.register.B & 0b00000001
    # cpu.register.B = (cpu.register.B >> 1) & 0xFF
    # cpu.register.set_z_flag(cpu.register.B == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 16


def code_cb_3f(cpu):
    """ SRL A - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_0 = cpu.register.A & 0b00000001
    cpu.register.A = (cpu.register.A >> 1) & 0xFF
    cpu.register.set_z_flag(cpu.register.A == 0)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(False)
    cpu.register.set_c_flag(bit_0)
    return 8


# OPCODES CB 4x
def code_cb_40(cpu):
    """ BIT 0,B - Test what is the value of bit 0 """
    bit_to_check = cpu.register.B & 0b00000001
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_41(cpu):
    """ BIT 0,C - Test what is the value of bit 0 """
    bit_to_check = cpu.register.C & 0b00000001
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_42(cpu):
    """ BIT 0,D - Test what is the value of bit 0 """
    bit_to_check = cpu.register.D & 0b00000001
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_43(cpu):
    """ BIT 0,E - Test what is the value of bit 0 """
    bit_to_check = cpu.register.E & 0b00000001
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_44(cpu):
    """ BIT 0,H - Test what is the value of bit 0 """
    bit_to_check = cpu.register.H & 0b00000001
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_45(cpu):
    """ BIT 0,L - Test what is the value of bit 0 """
    bit_to_check = cpu.register.L & 0b00000001
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_46(cpu):
    """ BIT 0,(HL) - Test what is the value of bit 0 """
    # TODO after memory is implemented
    # bit_to_check = cpu.register.B & 0b00000001
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 16


def code_cb_47(cpu):
    """ BIT 0,A - Test what is the value of bit 0 """
    bit_to_check = cpu.register.A & 0b00000001
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_48(cpu):
    """ BIT 1,B - Test what is the value of bit 1 """
    bit_to_check = (cpu.register.B & 0b00000010) >> 1
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_49(cpu):
    """ BIT 1,C - Test what is the value of bit 1 """
    bit_to_check = (cpu.register.C & 0b00000010) >> 1
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_4a(cpu):
    """ BIT 1,D - Test what is the value of bit 1 """
    bit_to_check = (cpu.register.D & 0b00000010) >> 1
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_4b(cpu):
    """ BIT 1,E - Test what is the value of bit 1 """
    bit_to_check = (cpu.register.E & 0b00000010) >> 1
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_4c(cpu):
    """ BIT 1,H - Test what is the value of bit 1 """
    bit_to_check = (cpu.register.H & 0b00000010) >> 1
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_4d(cpu):
    """ BIT 1,L - Test what is the value of bit 1 """
    bit_to_check = (cpu.register.L & 0b00000010) >> 1
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_4e(cpu):
    """ BIT 1,(HL) - Test what is the value of bit 1 """
    # TODO after memory is implemented
    # bit_to_check = (cpu.register.B & 0b00000010) >> 1
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 16


def code_cb_4f(cpu):
    """ BIT 1,A - Test what is the value of bit 1 """
    bit_to_check = (cpu.register.A & 0b00000010) >> 1
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


# OPCODES CB 5x
def code_cb_50(cpu):
    """ BIT 2,B - Test what is the value of bit 2 """
    bit_to_check = (cpu.register.B & 0b00000100) >> 2
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_51(cpu):
    """ BIT 2,C - Test what is the value of bit 2 """
    bit_to_check = (cpu.register.C & 0b00000100) >> 2
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_52(cpu):
    """ BIT 2,D - Test what is the value of bit 2 """
    bit_to_check = (cpu.register.D & 0b00000100) >> 2
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_53(cpu):
    """ BIT 2,E - Test what is the value of bit 2 """
    bit_to_check = (cpu.register.E & 0b00000100) >> 2
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_54(cpu):
    """ BIT 2,H - Test what is the value of bit 2 """
    bit_to_check = (cpu.register.H & 0b00000100) >> 2
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_55(cpu):
    """ BIT 2,L - Test what is the value of bit 2 """
    bit_to_check = (cpu.register.L & 0b00000100) >> 2
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_56(cpu):
    """ BIT 2,(HL) - Test what is the value of bit 2 """
    # TODO after memory is implemented
    # bit_to_check = (cpu.register.B & 0b00000100) >> 2
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 16


def code_cb_57(cpu):
    """ BIT 2,A - Test what is the value of bit 2 """
    bit_to_check = (cpu.register.A & 0b00000100) >> 2
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_58(cpu):
    """ BIT 3,B - Test what is the value of bit 3 """
    bit_to_check = (cpu.register.B & 0b00001000) >> 3
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_59(cpu):
    """ BIT 3,C - Test what is the value of bit 3 """
    bit_to_check = (cpu.register.C & 0b00001000) >> 3
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_5a(cpu):
    """ BIT 3,D - Test what is the value of bit 3 """
    bit_to_check = (cpu.register.D & 0b00001000) >> 3
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_5b(cpu):
    """ BIT 3,E - Test what is the value of bit 3 """
    bit_to_check = (cpu.register.E & 0b00001000) >> 3
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_5c(cpu):
    """ BIT 3,H - Test what is the value of bit 3 """
    bit_to_check = (cpu.register.H & 0b00001000) >> 3
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_5d(cpu):
    """ BIT 3,L - Test what is the value of bit 3 """
    bit_to_check = (cpu.register.L & 0b00001000) >> 3
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_5e(cpu):
    """ BIT 3,(HL) - Test what is the value of bit 3 """
    # TODO after memory is implemented
    # bit_to_check = (cpu.register.B & 0b00001000) >> 3
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 16


def code_cb_5f(cpu):
    """ BIT 3,A - Test what is the value of bit 3 """
    bit_to_check = (cpu.register.A & 0b00001000) >> 3
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


# OPCODES CB 6x
def code_cb_60(cpu):
    """ BIT 4,B - Test what is the value of bit 4 """
    bit_to_check = (cpu.register.B & 0b00010000) >> 4
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_61(cpu):
    """ BIT 4,C - Test what is the value of bit 4 """
    bit_to_check = (cpu.register.C & 0b00010000) >> 4
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_62(cpu):
    """ BIT 4,D - Test what is the value of bit 4 """
    bit_to_check = (cpu.register.D & 0b00010000) >> 4
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_63(cpu):
    """ BIT 4,E - Test what is the value of bit 4 """
    bit_to_check = (cpu.register.E & 0b00010000) >> 4
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_64(cpu):
    """ BIT 4,H - Test what is the value of bit 4 """
    bit_to_check = (cpu.register.H & 0b00010000) >> 4
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_65(cpu):
    """ BIT 4,L - Test what is the value of bit 4 """
    bit_to_check = (cpu.register.L & 0b00010000) >> 4
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_66(cpu):
    """ BIT 4,(HL) - Test what is the value of bit 4 """
    # TODO after memory is implemented
    # bit_to_check = (cpu.register.B & 0b00010000) >> 4
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 16


def code_cb_67(cpu):
    """ BIT 4,A - Test what is the value of bit 4 """
    bit_to_check = (cpu.register.A & 0b00010000) >> 4
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_68(cpu):
    """ BIT 5,B - Test what is the value of bit 5 """
    bit_to_check = (cpu.register.B & 0b00100000) >> 5
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_69(cpu):
    """ BIT 5,C - Test what is the value of bit 5 """
    bit_to_check = (cpu.register.C & 0b00100000) >> 5
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_6a(cpu):
    """ BIT 5,D - Test what is the value of bit 5 """
    bit_to_check = (cpu.register.D & 0b00100000) >> 5
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_6b(cpu):
    """ BIT 5,E - Test what is the value of bit 5 """
    bit_to_check = (cpu.register.E & 0b00100000) >> 5
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_6c(cpu):
    """ BIT 5,H - Test what is the value of bit 5 """
    bit_to_check = (cpu.register.H & 0b00100000) >> 5
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_6d(cpu):
    """ BIT 5,L - Test what is the value of bit 5 """
    bit_to_check = (cpu.register.L & 0b00100000) >> 5
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_6e(cpu):
    """ BIT 5,(HL) - Test what is the value of bit 5 """
    # TODO after memory is implemented
    # bit_to_check = (cpu.register.A & 0b00100000) >> 5
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 16


def code_cb_6f(cpu):
    """ BIT 5,A - Test what is the value of bit 5 """
    bit_to_check = (cpu.register.A & 0b00100000) >> 5
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


# OPCODES CB 7x
def code_cb_70(cpu):
    """ BIT 6,B - Test what is the value of bit 6 """
    bit_to_check = (cpu.register.B & 0b01000000) >> 6
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_71(cpu):
    """ BIT 6,C - Test what is the value of bit 6 """
    bit_to_check = (cpu.register.C & 0b01000000) >> 6
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_72(cpu):
    """ BIT 6,D - Test what is the value of bit 6 """
    bit_to_check = (cpu.register.D & 0b01000000) >> 6
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_73(cpu):
    """ BIT 6,E - Test what is the value of bit 6 """
    bit_to_check = (cpu.register.E & 0b01000000) >> 6
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_74(cpu):
    """ BIT 6,H - Test what is the value of bit 6 """
    bit_to_check = (cpu.register.H & 0b01000000) >> 6
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_75(cpu):
    """ BIT 6,L - Test what is the value of bit 6 """
    bit_to_check = (cpu.register.L & 0b01000000) >> 6
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_76(cpu):
    """ BIT 6,(HL) - Test what is the value of bit 6 """
    # TODO after memory is implemented
    # bit_to_check = (cpu.register.A & 0b01000000) >> 6
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 16


def code_cb_77(cpu):
    """ BIT 6,A - Test what is the value of bit 6 """
    bit_to_check = (cpu.register.A & 0b01000000) >> 6
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_78(cpu):
    """ BIT 7,B - Test what is the value of bit 7 """
    bit_to_check = (cpu.register.B & 0b10000000) >> 7
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_79(cpu):
    """ BIT 7,C - Test what is the value of bit 7 """
    bit_to_check = (cpu.register.C & 0b10000000) >> 7
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_7a(cpu):
    """ BIT 7,D - Test what is the value of bit 7 """
    bit_to_check = (cpu.register.D & 0b10000000) >> 7
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_7b(cpu):
    """ BIT 7,E - Test what is the value of bit 7 """
    bit_to_check = (cpu.register.E & 0b10000000) >> 7
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_7c(cpu):
    """ BIT 7,H - Test what is the value of bit 7 """
    bit_to_check = (cpu.register.H & 0b10000000) >> 7
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_7d(cpu):
    """ BIT 7,L - Test what is the value of bit 7 """
    bit_to_check = (cpu.register.L & 0b10000000) >> 7
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


def code_cb_7e(cpu):
    """ BIT 7,(HL) - Test what is the value of bit 7 """
    # TODO after memory is implemented
    # bit_to_check = (cpu.register.A & 0b10000000) >> 7
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 16


def code_cb_7f(cpu):
    """ BIT 7,A - Test what is the value of bit 7 """
    bit_to_check = (cpu.register.A & 0b10000000) >> 7
    cpu.register.set_z_flag(bit_to_check)
    cpu.register.set_n_flag(False)
    cpu.register.set_h_flag(True)
    return 8


# OPCODES CB 8x
def code_cb_80(cpu):
    """ RES 0,B - Reset the specified bit """
    cpu.register.B = cpu.register.B & 0b11111110
    return 8


def code_cb_81(cpu):
    """ RES 0,C - Reset the specified bit """
    cpu.register.C = cpu.register.C & 0b11111110
    return 8


def code_cb_82(cpu):
    """ RES 0,D - Reset the specified bit """
    cpu.register.D = cpu.register.D & 0b11111110
    return 8


def code_cb_83(cpu):
    """ RES 0,E - Reset the specified bit """
    cpu.register.E = cpu.register.E & 0b11111110
    return 8


def code_cb_84(cpu):
    """ RES 0,H - Reset the specified bit """
    cpu.register.H = cpu.register.H & 0b11111110
    return 8


def code_cb_85(cpu):
    """ RES 0,L - Reset the specified bit """
    cpu.register.L = cpu.register.L & 0b11111110
    return 8


def code_cb_86(cpu):
    """ RES 0,(HL) - Reset the specified bit """
    # TODO after memory is implemented
    # cpu.register.B = cpu.register.B & 0b11111110
    return 16


def code_cb_87(cpu):
    """ RES 0,A - Reset the specified bit """
    cpu.register.A = cpu.register.A & 0b11111110
    return 8


def code_cb_88(cpu):
    """ RES 1,B - Reset the specified bit """
    cpu.register.B = cpu.register.B & 0b11111101
    return 8


def code_cb_89(cpu):
    """ RES 1,C - Reset the specified bit """
    cpu.register.C = cpu.register.C & 0b11111101
    return 8


def code_cb_8a(cpu):
    """ RES 1,D - Reset the specified bit """
    cpu.register.D = cpu.register.D & 0b11111101
    return 8


def code_cb_8b(cpu):
    """ RES 1,E - Reset the specified bit """
    cpu.register.E = cpu.register.E & 0b11111101
    return 8


def code_cb_8c(cpu):
    """ RES 1,H - Reset the specified bit """
    cpu.register.H = cpu.register.H & 0b11111101
    return 8


def code_cb_8d(cpu):
    """ RES 1,L - Reset the specified bit """
    cpu.register.L = cpu.register.L & 0b11111101
    return 8


def code_cb_8e(cpu):
    """ RES 1,(HL) - Reset the specified bit """
    # TODO after memory is implemented
    # cpu.register.B = cpu.register.B & 0b11111101
    return 16


def code_cb_8f(cpu):
    """ RES 1,A - Reset the specified bit """
    cpu.register.A = cpu.register.A & 0b11111101
    return 8


# OPCODES CB 9x
def code_cb_90(cpu):
    """ RES 2,B - Reset the specified bit """
    cpu.register.B = cpu.register.B & 0b11111011
    return 8


def code_cb_91(cpu):
    """ RES 2,C - Reset the specified bit """
    cpu.register.C = cpu.register.C & 0b11111011
    return 8


def code_cb_92(cpu):
    """ RES 2,D - Reset the specified bit """
    cpu.register.D = cpu.register.D & 0b11111011
    return 8


def code_cb_93(cpu):
    """ RES 2,E - Reset the specified bit """
    cpu.register.E = cpu.register.E & 0b11111011
    return 8


def code_cb_94(cpu):
    """ RES 2,H - Reset the specified bit """
    cpu.register.H = cpu.register.H & 0b11111011
    return 8


def code_cb_95(cpu):
    """ RES 2,L - Reset the specified bit """
    cpu.register.L = cpu.register.L & 0b11111011
    return 8


def code_cb_96(cpu):
    """ RES 2,(HL) - Reset the specified bit """
    # TODO after memory is implemented
    # cpu.register.B = cpu.register.B & 0b11111011
    return 16


def code_cb_97(cpu):
    """ RES 2,A - Reset the specified bit """
    cpu.register.A = cpu.register.A & 0b11111011
    return 8


def code_cb_98(cpu):
    """ RES 3,B - Reset the specified bit """
    cpu.register.B = cpu.register.B & 0b11110111
    return 8


def code_cb_99(cpu):
    """ RES 3,C - Reset the specified bit """
    cpu.register.C = cpu.register.C & 0b11110111
    return 8


def code_cb_9a(cpu):
    """ RES 3,D - Reset the specified bit """
    cpu.register.D = cpu.register.D & 0b11110111
    return 8


def code_cb_9b(cpu):
    """ RES 3,E - Reset the specified bit """
    cpu.register.E = cpu.register.E & 0b11110111
    return 8


def code_cb_9c(cpu):
    """ RES 3,H - Reset the specified bit """
    cpu.register.H = cpu.register.H & 0b11110111
    return 8


def code_cb_9d(cpu):
    """ RES 3,L - Reset the specified bit """
    cpu.register.L = cpu.register.L & 0b11110111
    return 8


def code_cb_9e(cpu):
    """ RES 3,(HL) - Reset the specified bit """
    # TODO after memory is implemented
    # cpu.register.B = cpu.register.B & 0b11110111
    return 16


def code_cb_9f(cpu):
    """ RES 3,A - Reset the specified bit """
    cpu.register.A = cpu.register.A & 0b11110111
    return 8


# OPCODES CB Ax
def code_cb_a0(cpu):
    """ RES 4,B - Reset the specified bit """
    cpu.register.B = cpu.register.B & 0b11101111
    return 8


def code_cb_a1(cpu):
    """ RES 4,C - Reset the specified bit """
    cpu.register.C = cpu.register.C & 0b11101111
    return 8


def code_cb_a2(cpu):
    """ RES 4,D - Reset the specified bit """
    cpu.register.D = cpu.register.D & 0b11101111
    return 8


def code_cb_a3(cpu):
    """ RES 4,E - Reset the specified bit """
    cpu.register.E = cpu.register.E & 0b11101111
    return 8


def code_cb_a4(cpu):
    """ RES 4,H - Reset the specified bit """
    cpu.register.H = cpu.register.H & 0b11101111
    return 8


def code_cb_a5(cpu):
    """ RES 4,L - Reset the specified bit """
    cpu.register.L = cpu.register.L & 0b11101111
    return 8


def code_cb_a6(cpu):
    """ RES 4,(HL) - Reset the specified bit """
    # TODO after memory is implemented
    # cpu.register.B = cpu.register.B & 0b11101111
    return 16


def code_cb_a7(cpu):
    """ RES 4,A - Reset the specified bit """
    cpu.register.A = cpu.register.A & 0b11101111
    return 8


def code_cb_a8(cpu):
    """ RES 5,B - Reset the specified bit """
    cpu.register.B = cpu.register.B & 0b11011111
    return 8


def code_cb_a9(cpu):
    """ RES 5,C - Reset the specified bit """
    cpu.register.C = cpu.register.C & 0b11011111
    return 8


def code_cb_aa(cpu):
    """ RES 5,D - Reset the specified bit """
    cpu.register.D = cpu.register.D & 0b11011111
    return 8


def code_cb_ab(cpu):
    """ RES 5,E - Reset the specified bit """
    cpu.register.E = cpu.register.E & 0b11011111
    return 8


def code_cb_ac(cpu):
    """ RES 5,H - Reset the specified bit """
    cpu.register.H = cpu.register.H & 0b11011111
    return 8


def code_cb_ad(cpu):
    """ RES 5,L - Reset the specified bit """
    cpu.register.L = cpu.register.L & 0b11011111
    return 8


def code_cb_ae(cpu):
    """ RES 5,(HL) - Reset the specified bit """
    # TODO after memory is implemented
    # cpu.register.B = cpu.register.B & 0b11011111
    return 16


def code_cb_af(cpu):
    """ RES 5,A - Reset the specified bit """
    cpu.register.A = cpu.register.A & 0b11011111
    return 8


# OPCODES CB Bx
def code_cb_b0(cpu):
    """ RES 6,B - Reset the specified bit """
    cpu.register.B = cpu.register.B & 0b10111111
    return 8


def code_cb_b1(cpu):
    """ RES 6,C - Reset the specified bit """
    cpu.register.C = cpu.register.C & 0b10111111
    return 8


def code_cb_b2(cpu):
    """ RES 6,D - Reset the specified bit """
    cpu.register.D = cpu.register.D & 0b10111111
    return 8


def code_cb_b3(cpu):
    """ RES 6,E - Reset the specified bit """
    cpu.register.E = cpu.register.E & 0b10111111
    return 8


def code_cb_b4(cpu):
    """ RES 6,H - Reset the specified bit """
    cpu.register.H = cpu.register.H & 0b10111111
    return 8


def code_cb_b5(cpu):
    """ RES 6,L - Reset the specified bit """
    cpu.register.L = cpu.register.L & 0b10111111
    return 8


def code_cb_b6(cpu):
    """ RES 6,(HL) - Reset the specified bit """
    # TODO after memory is implemented
    # cpu.register.B = cpu.register.B & 0b10111111
    return 16


def code_cb_b7(cpu):
    """ RES 6,A - Reset the specified bit """
    cpu.register.A = cpu.register.A & 0b10111111
    return 8


def code_cb_b8(cpu):
    """ RES 7,B - Reset the specified bit """
    cpu.register.B = cpu.register.B & 0b01111111
    return 8


def code_cb_b9(cpu):
    """ RES 7,C - Reset the specified bit """
    cpu.register.C = cpu.register.C & 0b01111111
    return 8


def code_cb_ba(cpu):
    """ RES 7,D - Reset the specified bit """
    cpu.register.D = cpu.register.D & 0b01111111
    return 8


def code_cb_bb(cpu):
    """ RES 7,E - Reset the specified bit """
    cpu.register.E = cpu.register.E & 0b01111111
    return 8


def code_cb_bc(cpu):
    """ RES 7,H - Reset the specified bit """
    cpu.register.H = cpu.register.H & 0b01111111
    return 8


def code_cb_bd(cpu):
    """ RES 7,L - Reset the specified bit """
    cpu.register.L = cpu.register.L & 0b01111111
    return 8


def code_cb_be(cpu):
    """ RES 7,(HL) - Reset the specified bit """
    # TODO after memory is implemented
    # cpu.register.B = cpu.register.B & 0b01111111
    return 16


def code_cb_bf(cpu):
    """ RES 7,A - Reset the specified bit """
    cpu.register.A = cpu.register.A & 0b01111111
    return 8


# OPCODES CB Cx
def code_cb_c0(cpu):
    """ SET 0,B - Set the specified bit """
    cpu.register.B = cpu.register.B | 0b00000001
    return 8


def code_cb_c1(cpu):
    """ SET 0,C - Set the specified bit """
    cpu.register.C = cpu.register.C | 0b00000001
    return 8


def code_cb_c2(cpu):
    """ SET 0,D - Set the specified bit """
    cpu.register.D = cpu.register.D | 0b00000001
    return 8


def code_cb_c3(cpu):
    """ SET 0,E - Set the specified bit """
    cpu.register.E = cpu.register.E | 0b00000001
    return 8


def code_cb_c4(cpu):
    """ SET 0,H - Set the specified bit """
    cpu.register.H = cpu.register.H | 0b00000001
    return 8


def code_cb_c5(cpu):
    """ SET 0,L - Set the specified bit """
    cpu.register.L = cpu.register.L | 0b00000001
    return 8


def code_cb_c6(cpu):
    """ SET 0,(HL) - Set the specified bit """
    # TODO after memory is implemented
    # cpu.register.B = cpu.register.B | 0b00000001
    return 16


def code_cb_c7(cpu):
    """ SET 0,A - Set the specified bit """
    cpu.register.A = cpu.register.A | 0b00000001
    return 8


def code_cb_c8(cpu):
    """ SET 1,B - Set the specified bit """
    cpu.register.B = cpu.register.B | 0b00000010
    return 8


def code_cb_c9(cpu):
    """ SET 1,C - Set the specified bit """
    cpu.register.C = cpu.register.C | 0b00000010
    return 8


def code_cb_ca(cpu):
    """ SET 1,D - Set the specified bit """
    cpu.register.D = cpu.register.D | 0b00000010
    return 8


def code_cb_cb(cpu):
    """ SET 1,E - Set the specified bit """
    cpu.register.E = cpu.register.E | 0b00000010
    return 8


def code_cb_cc(cpu):
    """ SET 1,H - Set the specified bit """
    cpu.register.H = cpu.register.H | 0b00000010
    return 8


def code_cb_cd(cpu):
    """ SET 1,L - Set the specified bit """
    cpu.register.L = cpu.register.L | 0b00000010
    return 8


def code_cb_ce(cpu):
    """ SET 1,(HL) - Set the specified bit """
    # TODO after memory is implemented
    # cpu.register.B = cpu.register.B | 0b00000010
    return 16


def code_cb_cf(cpu):
    """ SET 1,A - Set the specified bit """
    cpu.register.A = cpu.register.A | 0b00000010
    return 8


# OPCODES CB Dx
def code_cb_d0(cpu):
    """ SET 2,B - Set the specified bit """
    cpu.register.B = cpu.register.B | 0b00000100
    return 8


def code_cb_d1(cpu):
    """ SET 2,C - Set the specified bit """
    cpu.register.C = cpu.register.C | 0b00000100
    return 8


def code_cb_d2(cpu):
    """ SET 2,D - Set the specified bit """
    cpu.register.D = cpu.register.D | 0b00000100
    return 8


def code_cb_d3(cpu):
    """ SET 2,E - Set the specified bit """
    cpu.register.E = cpu.register.E | 0b00000100
    return 8


def code_cb_d4(cpu):
    """ SET 2,H - Set the specified bit """
    cpu.register.H = cpu.register.H | 0b00000100
    return 8


def code_cb_d5(cpu):
    """ SET 2,L - Set the specified bit """
    cpu.register.L = cpu.register.L | 0b00000100
    return 8


def code_cb_d6(cpu):
    """ SET 2,(HL) - Set the specified bit """
    # TODO after memory is implemented
    # cpu.register.B = cpu.register.B | 0b00000100
    return 16


def code_cb_d7(cpu):
    """ SET 2,A - Set the specified bit """
    cpu.register.A = cpu.register.A | 0b00000100
    return 8


def code_cb_d8(cpu):
    """ SET 3,B - Set the specified bit """
    cpu.register.B = cpu.register.B | 0b00001000
    return 8


def code_cb_d9(cpu):
    """ SET 3,C - Set the specified bit """
    cpu.register.C = cpu.register.C | 0b00001000
    return 8


def code_cb_da(cpu):
    """ SET 3,D - Set the specified bit """
    cpu.register.D = cpu.register.D | 0b00001000
    return 8


def code_cb_db(cpu):
    """ SET 3,E - Set the specified bit """
    cpu.register.E = cpu.register.E | 0b00001000
    return 8


def code_cb_dc(cpu):
    """ SET 3,H - Set the specified bit """
    cpu.register.H = cpu.register.H | 0b00001000
    return 8


def code_cb_dd(cpu):
    """ SET 3,L - Set the specified bit """
    cpu.register.L = cpu.register.L | 0b00001000
    return 8


def code_cb_de(cpu):
    """ SET 3,(HL) - Set the specified bit """
    # TODO after memory is implemented
    # cpu.register.B = cpu.register.B | 0b00001000
    return 16


def code_cb_df(cpu):
    """ SET 3,A - Set the specified bit """
    cpu.register.A = cpu.register.A | 0b00001000
    return 8


# OPCODES CB Ex
def code_cb_e0(cpu):
    """ SET 4,B - Set the specified bit """
    cpu.register.B = cpu.register.B | 0b00010000
    return 8


def code_cb_e1(cpu):
    """ SET 4,C - Set the specified bit """
    cpu.register.C = cpu.register.C | 0b00010000
    return 8


def code_cb_e2(cpu):
    """ SET 4,D - Set the specified bit """
    cpu.register.D = cpu.register.D | 0b00010000
    return 8


def code_cb_e3(cpu):
    """ SET 4,E - Set the specified bit """
    cpu.register.E = cpu.register.E | 0b00010000
    return 8


def code_cb_e4(cpu):
    """ SET 4,H - Set the specified bit """
    cpu.register.H = cpu.register.H | 0b00010000
    return 8


def code_cb_e5(cpu):
    """ SET 4,L - Set the specified bit """
    cpu.register.L = cpu.register.L | 0b00010000
    return 8


def code_cb_e6(cpu):
    """ SET 4,(HL) - Set the specified bit """
    # TODO after memory is implemented
    # cpu.register.B = cpu.register.B | 0b00010000
    return 16


def code_cb_e7(cpu):
    """ SET 4,A - Set the specified bit """
    cpu.register.A = cpu.register.A | 0b00010000
    return 8


def code_cb_e8(cpu):
    """ SET 5,B - Set the specified bit """
    cpu.register.B = cpu.register.B | 0b00100000
    return 8


def code_cb_e9(cpu):
    """ SET 5,C - Set the specified bit """
    cpu.register.C = cpu.register.C | 0b00100000
    return 8


def code_cb_ea(cpu):
    """ SET 5,D - Set the specified bit """
    cpu.register.D = cpu.register.D | 0b00100000
    return 8


def code_cb_eb(cpu):
    """ SET 5,E - Set the specified bit """
    cpu.register.E = cpu.register.E | 0b00100000
    return 8


def code_cb_ec(cpu):
    """ SET 5,H - Set the specified bit """
    cpu.register.H = cpu.register.H | 0b00100000
    return 8


def code_cb_ed(cpu):
    """ SET 5,L - Set the specified bit """
    cpu.register.L = cpu.register.L | 0b00100000
    return 8


def code_cb_ee(cpu):
    """ SET 5,(HL) - Set the specified bit """
    # TODO after memory is implemented
    # cpu.register.B = cpu.register.B | 0b00100000
    return 16


def code_cb_ef(cpu):
    """ SET 5,A - Set the specified bit """
    cpu.register.A = cpu.register.A | 0b00100000
    return 8


# OPCODES CB Fx
def code_cb_f0(cpu):
    """ SET 6,B - Set the specified bit """
    cpu.register.B = cpu.register.B | 0b01000000
    return 8


def code_cb_f1(cpu):
    """ SET 6,C - Set the specified bit """
    cpu.register.C = cpu.register.C | 0b01000000
    return 8


def code_cb_f2(cpu):
    """ SET 6,D - Set the specified bit """
    cpu.register.D = cpu.register.D | 0b01000000
    return 8


def code_cb_f3(cpu):
    """ SET 6,E - Set the specified bit """
    cpu.register.E = cpu.register.E | 0b01000000
    return 8


def code_cb_f4(cpu):
    """ SET 6,H - Set the specified bit """
    cpu.register.H = cpu.register.H | 0b01000000
    return 8


def code_cb_f5(cpu):
    """ SET 6,L - Set the specified bit """
    cpu.register.L = cpu.register.L | 0b01000000
    return 8


def code_cb_f6(cpu):
    """ SET 6,(HL) - Set the specified bit """
    # TODO after memory is implemented
    # cpu.register.B = cpu.register.B | 0b01000000
    return 16


def code_cb_f7(cpu):
    """ SET 6,A - Set the specified bit """
    cpu.register.A = cpu.register.A | 0b01000000
    return 8


def code_cb_f8(cpu):
    """ SET 7,B - Set the specified bit """
    cpu.register.B = cpu.register.B | 0b10000000
    return 8


def code_cb_f9(cpu):
    """ SET 7,C - Set the specified bit """
    cpu.register.C = cpu.register.C | 0b10000000
    return 8


def code_cb_fa(cpu):
    """ SET 7,D - Set the specified bit """
    cpu.register.D = cpu.register.D | 0b10000000
    return 8


def code_cb_fb(cpu):
    """ SET 7,E - Set the specified bit """
    cpu.register.E = cpu.register.E | 0b10000000
    return 8


def code_cb_fc(cpu):
    """ SET 7,H - Set the specified bit """
    cpu.register.H = cpu.register.H | 0b10000000
    return 8


def code_cb_fd(cpu):
    """ SET 7,L - Set the specified bit """
    cpu.register.L = cpu.register.L | 0b10000000
    return 8


def code_cb_fe(cpu):
    """ SET 7,(HL) - Set the specified bit """
    # TODO after memory is implemented
    # cpu.register.B = cpu.register.B | 0b10000000
    return 16


def code_cb_ff(cpu):
    """ SET 7,A - Set the specified bit """
    cpu.register.A = cpu.register.A | 0b10000000
    return 8


_instruction_dict = {
    0x00:code_00, 0x01:code_01, 0x02:code_02, 0x03:code_03, 0x04:code_04, 0x05:code_05, 0x06:code_06, 0x07:code_07,
    0x08:code_08, 0x09:code_09, 0x0a:code_0a, 0x0b:code_0b, 0x0c:code_0c, 0x0d:code_0d, 0x0e:code_0e, 0x0f:code_0f,
    0x10:code_10, 0x11:code_11, 0x12:code_12, 0x13:code_13, 0x14:code_14, 0x15:code_15, 0x16:code_16, 0x17:code_17,
    0x18:code_18, 0x19:code_19, 0x1a:code_1a, 0x1b:code_1b, 0x1c:code_1c, 0x1d:code_1d, 0x1e:code_1e, 0x1f:code_1f,
    0x20:code_20, 0x21:code_21, 0x22:code_22, 0x23:code_23, 0x24:code_24, 0x25:code_25, 0x26:code_26, 0x27:code_27,
    0x28:code_28, 0x29:code_29, 0x2a:code_2a, 0x2b:code_2b, 0x2c:code_2c, 0x2d:code_2d, 0x2e:code_2e, 0x2f:code_2f,
    0x30:code_30, 0x31:code_31, 0x32:code_32, 0x33:code_33, 0x34:code_34, 0x35:code_35, 0x36:code_36, 0x37:code_37,
    0x38:code_38, 0x39:code_39, 0x3a:code_3a, 0x3b:code_3b, 0x3c:code_3c, 0x3d:code_3d, 0x3e:code_3e, 0x3f:code_3f,
    0x40:code_40, 0x41:code_41, 0x42:code_42, 0x43:code_43, 0x44:code_44, 0x45:code_45, 0x46:code_46, 0x47:code_47,
    0x48:code_48, 0x49:code_49, 0x4a:code_4a, 0x4b:code_4b, 0x4c:code_4c, 0x4d:code_4d, 0x4e:code_4e, 0x4f:code_4f,
    0x50:code_50, 0x51:code_51, 0x52:code_52, 0x53:code_53, 0x54:code_54, 0x55:code_55, 0x56:code_56, 0x57:code_57,
    0x58:code_58, 0x59:code_59, 0x5a:code_5a, 0x5b:code_5b, 0x5c:code_5c, 0x5d:code_5d, 0x5e:code_5e, 0x5f:code_5f,
    0x60:code_60, 0x61:code_61, 0x62:code_62, 0x63:code_63, 0x64:code_64, 0x65:code_65, 0x66:code_66, 0x67:code_67,
    0x68:code_68, 0x69:code_69, 0x6a:code_6a, 0x6b:code_6b, 0x6c:code_6c, 0x6d:code_6d, 0x6e:code_6e, 0x6f:code_6f,
    0x70:code_70, 0x71:code_71, 0x72:code_72, 0x73:code_73, 0x74:code_74, 0x75:code_75, 0x76:code_76, 0x77:code_77,
    0x78:code_78, 0x79:code_79, 0x7a:code_7a, 0x7b:code_7b, 0x7c:code_7c, 0x7d:code_7d, 0x7e:code_7e, 0x7f:code_7f,
    0x80:code_80, 0x81:code_81, 0x82:code_82, 0x83:code_83, 0x84:code_84, 0x85:code_85, 0x86:code_86, 0x87:code_87,
    0x88:code_88, 0x89:code_89, 0x8a:code_8a, 0x8b:code_8b, 0x8c:code_8c, 0x8d:code_8d, 0x8e:code_8e, 0x8f:code_8f,
    0x90:code_90, 0x91:code_91, 0x92:code_92, 0x93:code_93, 0x94:code_94, 0x95:code_95, 0x96:code_96, 0x97:code_97,
    0x98:code_98, 0x99:code_99, 0x9a:code_9a, 0x9b:code_9b, 0x9c:code_9c, 0x9d:code_9d, 0x9e:code_9e, 0x9f:code_9f,
    0xa0:code_a0, 0xa1:code_a1, 0xa2:code_a2, 0xa3:code_a3, 0xa4:code_a4, 0xa5:code_a5, 0xa6:code_a6, 0xa7:code_a7,
    0xa8:code_a8, 0xa9:code_a9, 0xaa:code_aa, 0xab:code_ab, 0xac:code_ac, 0xad:code_ad, 0xae:code_ae, 0xaf:code_af,
    0xb0:code_b0, 0xb1:code_b1, 0xb2:code_b2, 0xb3:code_b3, 0xb4:code_b4, 0xb5:code_b5, 0xb6:code_b6, 0xb7:code_b7,
    0xb8:code_b8, 0xb9:code_b9, 0xba:code_ba, 0xbb:code_bb, 0xbc:code_bc, 0xbd:code_bd, 0xbe:code_be, 0xbf:code_bf,
    0xc0:code_c0, 0xc1:code_c1, 0xc2:code_c2, 0xc3:code_c3, 0xc4:code_c4, 0xc5:code_c5, 0xc6:code_c6, 0xc7:code_c7,
    0xc8:code_c8, 0xc9:code_c9, 0xca:code_ca, 0xcb:code_cb, 0xcc:code_cc, 0xcd:code_cd, 0xce:code_ce, 0xcf:code_cf,
    0xd0:code_d0, 0xd1:code_d1, 0xd2:code_d2, 0xd3:code_d3, 0xd4:code_d4, 0xd5:code_d5, 0xd6:code_d6, 0xd7:code_d7,
    0xd8:code_d8, 0xd9:code_d9, 0xda:code_da, 0xdb:code_db, 0xdc:code_dc, 0xdd:code_dd, 0xde:code_de, 0xdf:code_df,
    0xe0:code_e0, 0xe1:code_e1, 0xe2:code_e2, 0xe3:code_e3, 0xe4:code_e4, 0xe5:code_e5, 0xe6:code_e6, 0xe7:code_e7,
    0xe8:code_e8, 0xe9:code_e9, 0xea:code_ea, 0xeb:code_eb, 0xec:code_ec, 0xed:code_ed, 0xee:code_ee, 0xef:code_ef,
    0xf0:code_f0, 0xf1:code_f1, 0xf2:code_f2, 0xf3:code_f3, 0xf4:code_f4, 0xf5:code_f5, 0xf6:code_f6, 0xf7:code_f7,
    0xf8:code_f8, 0xf9:code_f9, 0xfa:code_fa, 0xfb:code_fb, 0xfc:code_fc, 0xfd:code_fd, 0xfe:code_fe, 0xff:code_ff
}

_instruction_cb_dict = {
    0x00:code_cb_00,0x01:code_cb_01,0x02:code_cb_02,0x03:code_cb_03,0x04:code_cb_04,0x05:code_cb_05,0x06:code_cb_06,
    0x07:code_cb_07,0x08:code_cb_08,0x09:code_cb_09,0x0a:code_cb_0a,0x0b:code_cb_0b,0x0c:code_cb_0c,0x0d:code_cb_0d,
    0x0e:code_cb_0e,0x0f:code_cb_0f,0x10:code_cb_10,0x11:code_cb_11,0x12:code_cb_12,0x13:code_cb_13,0x14:code_cb_14,
    0x15:code_cb_15,0x16:code_cb_16,0x17:code_cb_17,0x18:code_cb_18,0x19:code_cb_19,0x1a:code_cb_1a,0x1b:code_cb_1b,
    0x1c:code_cb_1c,0x1d:code_cb_1d,0x1e:code_cb_1e,0x1f:code_cb_1f,0x20:code_cb_20,0x21:code_cb_21,0x22:code_cb_22,
    0x23:code_cb_23,0x24:code_cb_24,0x25:code_cb_25,0x26:code_cb_26,0x27:code_cb_27,0x28:code_cb_28,0x29:code_cb_29,
    0x2a:code_cb_2a,0x2b:code_cb_2b,0x2c:code_cb_2c,0x2d:code_cb_2d,0x2e:code_cb_2e,0x2f:code_cb_2f,0x30:code_cb_30,
    0x31:code_cb_31,0x32:code_cb_32,0x33:code_cb_33,0x34:code_cb_34,0x35:code_cb_35,0x36:code_cb_36,0x37:code_cb_37,
    0x38:code_cb_38,0x39:code_cb_39,0x3a:code_cb_3a,0x3b:code_cb_3b,0x3c:code_cb_3c,0x3d:code_cb_3d,0x3e:code_cb_3e,
    0x3f:code_cb_3f,0x40:code_cb_40,0x41:code_cb_41,0x42:code_cb_42,0x43:code_cb_43,0x44:code_cb_44,0x45:code_cb_45,
    0x46:code_cb_46,0x47:code_cb_47,0x48:code_cb_48,0x49:code_cb_49,0x4a:code_cb_4a,0x4b:code_cb_4b,0x4c:code_cb_4c,
    0x4d:code_cb_4d,0x4e:code_cb_4e,0x4f:code_cb_4f,0x50:code_cb_50,0x51:code_cb_51,0x52:code_cb_52,0x53:code_cb_53,
    0x54:code_cb_54,0x55:code_cb_55,0x56:code_cb_56,0x57:code_cb_57,0x58:code_cb_58,0x59:code_cb_59,0x5a:code_cb_5a,
    0x5b:code_cb_5b,0x5c:code_cb_5c,0x5d:code_cb_5d,0x5e:code_cb_5e,0x5f:code_cb_5f,0x60:code_cb_60,0x61:code_cb_61,
    0x62:code_cb_62,0x63:code_cb_63,0x64:code_cb_64,0x65:code_cb_65,0x66:code_cb_66,0x67:code_cb_67,0x68:code_cb_68,
    0x69:code_cb_69,0x6a:code_cb_6a,0x6b:code_cb_6b,0x6c:code_cb_6c,0x6d:code_cb_6d,0x6e:code_cb_6e,0x6f:code_cb_6f,
    0x70:code_cb_70,0x71:code_cb_71,0x72:code_cb_72,0x73:code_cb_73,0x74:code_cb_74,0x75:code_cb_75,0x76:code_cb_76,
    0x77:code_cb_77,0x78:code_cb_78,0x79:code_cb_79,0x7a:code_cb_7a,0x7b:code_cb_7b,0x7c:code_cb_7c,0x7d:code_cb_7d,
    0x7e:code_cb_7e,0x7f:code_cb_7f,0x80:code_cb_80,0x81:code_cb_81,0x82:code_cb_82,0x83:code_cb_83,0x84:code_cb_84,
    0x85:code_cb_85,0x86:code_cb_86,0x87:code_cb_87,0x88:code_cb_88,0x89:code_cb_89,0x8a:code_cb_8a,0x8b:code_cb_8b,
    0x8c:code_cb_8c,0x8d:code_cb_8d,0x8e:code_cb_8e,0x8f:code_cb_8f,0x90:code_cb_90,0x91:code_cb_91,0x92:code_cb_92,
    0x93:code_cb_93,0x94:code_cb_94,0x95:code_cb_95,0x96:code_cb_96,0x97:code_cb_97,0x98:code_cb_98,0x99:code_cb_99,
    0x9a:code_cb_9a,0x9b:code_cb_9b,0x9c:code_cb_9c,0x9d:code_cb_9d,0x9e:code_cb_9e,0x9f:code_cb_9f,0xa0:code_cb_a0,
    0xa1:code_cb_a1,0xa2:code_cb_a2,0xa3:code_cb_a3,0xa4:code_cb_a4,0xa5:code_cb_a5,0xa6:code_cb_a6,0xa7:code_cb_a7,
    0xa8:code_cb_a8,0xa9:code_cb_a9,0xaa:code_cb_aa,0xab:code_cb_ab,0xac:code_cb_ac,0xad:code_cb_ad,0xae:code_cb_ae,
    0xaf:code_cb_af,0xb0:code_cb_b0,0xb1:code_cb_b1,0xb2:code_cb_b2,0xb3:code_cb_b3,0xb4:code_cb_b4,0xb5:code_cb_b5,
    0xb6:code_cb_b6,0xb7:code_cb_b7,0xb8:code_cb_b8,0xb9:code_cb_b9,0xba:code_cb_ba,0xbb:code_cb_bb,0xbc:code_cb_bc,
    0xbd:code_cb_bd,0xbe:code_cb_be,0xbf:code_cb_bf,0xc0:code_cb_c0,0xc1:code_cb_c1,0xc2:code_cb_c2,0xc3:code_cb_c3,
    0xc4:code_cb_c4,0xc5:code_cb_c5,0xc6:code_cb_c6,0xc7:code_cb_c7,0xc8:code_cb_c8,0xc9:code_cb_c9,0xca:code_cb_ca,
    0xcb:code_cb_cb,0xcc:code_cb_cc,0xcd:code_cb_cd,0xce:code_cb_ce,0xcf:code_cb_cf,0xd0:code_cb_d0,0xd1:code_cb_d1,
    0xd2:code_cb_d2,0xd3:code_cb_d3,0xd4:code_cb_d4,0xd5:code_cb_d5,0xd6:code_cb_d6,0xd7:code_cb_d7,0xd8:code_cb_d8,
    0xd9:code_cb_d9,0xda:code_cb_da,0xdb:code_cb_db,0xdc:code_cb_dc,0xdd:code_cb_dd,0xde:code_cb_de,0xdf:code_cb_df,
    0xe0:code_cb_e0,0xe1:code_cb_e1,0xe2:code_cb_e2,0xe3:code_cb_e3,0xe4:code_cb_e4,0xe5:code_cb_e5,0xe6:code_cb_e6,
    0xe7:code_cb_e7,0xe8:code_cb_e8,0xe9:code_cb_e9,0xea:code_cb_ea,0xeb:code_cb_eb,0xec:code_cb_ec,0xed:code_cb_ed,
    0xee:code_cb_ee,0xef:code_cb_ef,0xf0:code_cb_f0,0xf1:code_cb_f1,0xf2:code_cb_f2,0xf3:code_cb_f3,0xf4:code_cb_f4,
    0xf5:code_cb_f5,0xf6:code_cb_f6,0xf7:code_cb_f7,0xf8:code_cb_f8,0xf9:code_cb_f9,0xfa:code_cb_fa,0xfb:code_cb_fb,
    0xfc:code_cb_fc,0xfd:code_cb_fd,0xfe:code_cb_fe,0xff:code_cb_ff
}
