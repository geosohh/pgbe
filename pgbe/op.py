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

The GameBoy uses Little-endian, i.e. least significant byte first. Therefore, in order to properly execute opcodes
values have to be converted to Big-endian first.
"""
import util


def execute(gb, opcode: int):
    """
    Called by the CPU to execute an instruction.
    
    :param gb instance
    :type gb: gb.GB
    :param opcode: Instruction to execute
    """
    return _instruction_dict[opcode](gb)


def get_big_endian_value(msb: int, lsb: int):
    """
    Joins the two bytes received from the cartridge into a single, big-endian value.

    :param msb: Most significant byte
    :param lsb: Least significant byte
    :return: Big-endian value
    """
    return (msb << 8) | lsb


def get_little_endian_value(msb: int, lsb: int):
    """
    Joins the two bytes received from the cartridge into a single, little-endian value.

    :param msb: Most significant byte
    :param lsb: Least significant byte
    :return: Little-endian value
    """
    return (lsb << 8) | msb


# OPCODES 0x
# noinspection PyUnusedLocal
def code_00(gb):
    """ NOP - Does nothing """
    return 4


def code_01(gb):
    """ LD BC,d16 - Stores given 16-bit value at BC """
    lsb = gb.cpu.read_next_byte_from_cartridge()
    msb = gb.cpu.read_next_byte_from_cartridge()
    d16 = get_big_endian_value(msb, lsb)
    gb.cpu.register.set_bc(d16)
    return 12


def code_02(gb):
    """ LD (BC),A - Stores reg at the address in BC """
    a16 = gb.cpu.register.get_bc()
    gb.memory.write_8bit(a16,gb.cpu.register.A)
    return 8


def code_03(gb):
    """ INC BC - BC=BC+1 """
    gb.cpu.register.set_bc((gb.cpu.register.get_bc() + 1) & 0xFFFF)
    return 8


def code_04(gb):
    """ INC B - B=B+1 """
    gb.cpu.register.set_b((gb.cpu.register.B + 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.B == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag((gb.cpu.register.B & 0x0F) == 0)
    return 4


def code_05(gb):
    """ DEC B - B=B-1 """
    gb.cpu.register.set_b((gb.cpu.register.B - 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.B == 0)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((gb.cpu.register.B & 0x0F) == 0x0F)
    return 4


def code_06(gb):
    """ LD B,d8 """
    d8 = gb.cpu.read_next_byte_from_cartridge()
    gb.cpu.register.set_b(d8)
    return 8


def code_07(gb):
    """ RLCA - Copy register A bit 7 to Carry flag, then rotate register A left """
    bit_7 = gb.cpu.register.A >> 7
    gb.cpu.register.set_a(((gb.cpu.register.A << 1) + bit_7) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_7)
    return 4


def code_08(gb):
    """ LD (a16),SP - Set SP value into address (a16) """
    lsb = gb.cpu.read_next_byte_from_cartridge()
    msb = gb.cpu.read_next_byte_from_cartridge()
    a16 = get_big_endian_value(msb, lsb)
    gb.memory.write_16bit(a16,gb.cpu.register.SP)
    return 20


def code_09(gb):
    """ ADD HL,BC - HL=HL+BC """
    result = gb.cpu.register.get_hl() + gb.cpu.register.get_bc()
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(((gb.cpu.register.get_hl() & 0x0FFF) + (gb.cpu.register.get_bc() & 0x0FFF)) > 0x0FFF)
    gb.cpu.register.set_c_flag(result > 0xFFFF)
    gb.cpu.register.set_hl(result & 0xFFFF)
    return 8


def code_0a(gb):
    """ LD A,(BC) - Load (value at the address in BC) to the register """
    d8 = gb.memory.read_8bit(gb.cpu.register.get_bc())
    gb.cpu.register.set_a(d8)
    return 8


def code_0b(gb):
    """ DEC BC - BC=BC-1 """
    gb.cpu.register.set_bc((gb.cpu.register.get_bc() - 1) & 0xFFFF)
    return 8


def code_0c(gb):
    """ INC C - C=C+1 """
    gb.cpu.register.set_c((gb.cpu.register.C + 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.C == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag((gb.cpu.register.C & 0x0F) == 0)
    return 4


def code_0d(gb):
    """ DEC C - C=C-1 """
    gb.cpu.register.set_c((gb.cpu.register.C - 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.C == 0)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((gb.cpu.register.C & 0x0F) == 0x0F)
    return 4


def code_0e(gb):
    """ LD C,d8 """
    d8 = gb.cpu.read_next_byte_from_cartridge()
    gb.cpu.register.set_c(d8)
    return 8


def code_0f(gb):
    """ RRCA - Copy register A bit 0 to Carry flag, then rotate register A right """
    bit_0 = gb.cpu.register.A & 0b00000001
    gb.cpu.register.set_a(((bit_0 << 7) + (gb.cpu.register.A >> 1)) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 4


# OPCODES 1x
def code_10(gb):
    """
    STOP - Switch GameBoy into VERY low power standby mode. Halt CPU and LCD display until a button is pressed
    See: http://gbdev.gg8.se/wiki/articles/Reducing_Power_Consumption
    """
    gb.cpu.stopped = True
    return 4


def code_11(gb):
    """ LD DE,d16 - Stores given 16-bit value at DE """
    lsb = gb.cpu.read_next_byte_from_cartridge()
    msb = gb.cpu.read_next_byte_from_cartridge()
    d16 = get_big_endian_value(msb, lsb)
    gb.cpu.register.set_de(d16)
    return 12


def code_12(gb):
    """ LD (DE),A - Stores reg at the address in DE """
    a16 = gb.cpu.register.get_de()
    gb.memory.write_8bit(a16, gb.cpu.register.A)
    return 8


def code_13(gb):
    """ INC DE - DE=DE+1 """
    gb.cpu.register.set_de((gb.cpu.register.get_de() + 1) & 0xFFFF)
    return 8


def code_14(gb):
    """ INC D - D=D+1 """
    gb.cpu.register.set_d((gb.cpu.register.D + 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.D == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag((gb.cpu.register.D & 0x0F) == 0)
    return 4


def code_15(gb):
    """ DEC D - D=D-1 """
    gb.cpu.register.set_d((gb.cpu.register.D - 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.D == 0)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((gb.cpu.register.D & 0x0F) == 0x0F)
    return 4


def code_16(gb):
    """ LD D,d8 """
    d8 = gb.cpu.read_next_byte_from_cartridge()
    gb.cpu.register.set_d(d8)
    return 8


def code_17(gb):
    """ RLA - Copy register A bit 7 to temp, replace A bit 7 with Carry flag, rotate A left, copy temp to Carry flag """
    bit_7 = gb.cpu.register.A >> 7
    gb.cpu.register.set_a(((gb.cpu.register.A << 1) + gb.cpu.register.get_c_flag()) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_7)
    return 4


def code_18(gb):
    """ JP r8 - make the command at address (current address + r8) the next to be executed (r8 is signed) """
    r8 = gb.cpu.read_next_byte_from_cartridge()
    r8 = util.convert_unsigned_integer_to_signed(r8)
    gb.cpu.register.set_pc((gb.cpu.register.PC + r8) & 0xFFFF)
    return 12


def code_19(gb):
    """ ADD HL,DE - HL=HL+DE """
    result = gb.cpu.register.get_hl() + gb.cpu.register.get_de()
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(((gb.cpu.register.get_hl() & 0x0FFF) + (gb.cpu.register.get_de() & 0x0FFF)) > 0x0FFF)
    gb.cpu.register.set_c_flag(result > 0xFFFF)
    gb.cpu.register.set_hl(result & 0xFFFF)
    return 8


def code_1a(gb):
    """ LD A,(DE) - Load reg with the value at the address in DE """
    d8 = gb.memory.read_8bit(gb.cpu.register.get_de())
    gb.cpu.register.set_a(d8)
    return 8


def code_1b(gb):
    """ DEC DE - DE=DE-1 """
    gb.cpu.register.set_de((gb.cpu.register.get_de() - 1) & 0xFFFF)
    return 8


def code_1c(gb):
    """ INC E - E=E+1 """
    gb.cpu.register.set_e((gb.cpu.register.E + 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.E == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag((gb.cpu.register.E & 0x0F) == 0)
    return 4


def code_1d(gb):
    """ DEC E - E=E-1 """
    gb.cpu.register.set_e((gb.cpu.register.E - 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.E == 0)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((gb.cpu.register.E & 0x0F) == 0x0F)
    return 4


def code_1e(gb):
    """ LD E,d8 """
    d8 = gb.cpu.read_next_byte_from_cartridge()
    gb.cpu.register.set_e(d8)
    return 8


def code_1f(gb):
    """ RRA - Copy register A bit 0 to temp, replace A bit 0 w/ Carry flag, rotate A right, copy temp to Carry flag """
    bit_0 = gb.cpu.register.A & 0b00000001
    gb.cpu.register.set_a(((gb.cpu.register.get_c_flag() << 7) + (gb.cpu.register.A >> 1)) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 4


# OPCODES 2x
def code_20(gb):
    """ JR NZ,r8 - If flag Z is reset, add r8 to current address and jump to it """
    r8 = gb.cpu.read_next_byte_from_cartridge()  # Has to be read even if it is not going to be used
    if not gb.cpu.register.get_z_flag():
        r8 = util.convert_unsigned_integer_to_signed(r8)
        gb.cpu.register.set_pc((gb.cpu.register.PC + r8) & 0xFFFF)
        return 12
    return 8


def code_21(gb):
    """ LD HL,d16 - Stores given 16-bit value at HL """
    lsb = gb.cpu.read_next_byte_from_cartridge()
    msb = gb.cpu.read_next_byte_from_cartridge()
    d16 = get_big_endian_value(msb,lsb)
    gb.cpu.register.set_hl(d16)
    return 12


def code_22(gb):
    """ LD (HL+),A or LD (HLI),A or LDI (HL),A - Put value at A into address HL. Increment HL """
    gb.memory.write_8bit(gb.cpu.register.get_hl(),gb.cpu.register.A)
    gb.cpu.register.set_hl((gb.cpu.register.get_hl() + 1) & 0xFFFF)
    return 8


def code_23(gb):
    """ INC HL - HL=HL+1 """
    gb.cpu.register.set_hl((gb.cpu.register.get_hl() + 1) & 0xFFFF)
    return 8


def code_24(gb):
    """ INC H - H=H+1 """
    gb.cpu.register.set_h((gb.cpu.register.H + 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.H == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag((gb.cpu.register.H & 0x0F) == 0)
    return 4


def code_25(gb):
    """ DEC H - H=H-1 """
    gb.cpu.register.set_h((gb.cpu.register.H - 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.H == 0)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((gb.cpu.register.H & 0x0F) == 0x0F)
    return 4


def code_26(gb):
    """ LD H,d8 """
    d8 = gb.cpu.read_next_byte_from_cartridge()
    gb.cpu.register.set_h(d8)
    return 8


def code_27(gb):
    """
    DAA - Adjust value in register A for Binary Coded Decimal representation
    See:  http://gbdev.gg8.se/wiki/articles/DAA
    """
    n_flag = gb.cpu.register.get_n_flag()
    h_flag = gb.cpu.register.get_h_flag()
    c_flag = gb.cpu.register.get_c_flag()
    if n_flag:
        if c_flag:
            gb.cpu.register.set_a((gb.cpu.register.A - 0x60) & 0xFF)
        if h_flag:
            gb.cpu.register.set_a((gb.cpu.register.A - 0x06) & 0xFF)
    else:
        if c_flag or gb.cpu.register.A > 0x99:
            gb.cpu.register.set_a((gb.cpu.register.A + 0x60) & 0xFF)
            gb.cpu.register.set_c_flag(True)
        if h_flag or (gb.cpu.register.A & 0x0F) > 0x09:
            gb.cpu.register.set_a((gb.cpu.register.A + 0x06) & 0xFF)

    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_h_flag(False)
    return 4


def code_28(gb):
    """ JR Z,r8 - If flag Z is set, add r8 to current address and jump to it """
    r8 = gb.cpu.read_next_byte_from_cartridge()  # Has to be read even if it is not going to be used
    if gb.cpu.register.get_z_flag():
        r8 = util.convert_unsigned_integer_to_signed(r8)
        gb.cpu.register.set_pc((gb.cpu.register.PC + r8) & 0xFFFF)
        return 12
    return 8


def code_29(gb):
    """ ADD HL,HL - HL=HL+HL """
    result = gb.cpu.register.get_hl() * 2
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(((gb.cpu.register.get_hl() & 0x0FFF) * 2) > 0x0FFF)
    gb.cpu.register.set_c_flag(result > 0xFFFF)
    gb.cpu.register.set_hl(result & 0xFFFF)
    return 8


def code_2a(gb):
    """ LD A,(HL+) or LD A,(HLI) or LDI A,(HL) - Put value at address HL into A. Increment HL """
    gb.cpu.register.set_a(gb.memory.read_8bit(gb.cpu.register.get_hl()))
    gb.cpu.register.set_hl((gb.cpu.register.get_hl() + 1) & 0xFFFF)
    return 8


def code_2b(gb):
    """ DEC HL - HL=HL-1 """
    gb.cpu.register.set_hl((gb.cpu.register.get_hl() - 1) & 0xFFFF)
    return 8


def code_2c(gb):
    """ INC L - L=L+1 """
    gb.cpu.register.set_l((gb.cpu.register.L + 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.L == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag((gb.cpu.register.L & 0x0F) == 0)
    return 4


def code_2d(gb):
    """ DEC L - L=L-1 """
    gb.cpu.register.set_l((gb.cpu.register.L - 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.L == 0)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((gb.cpu.register.L & 0x0F) == 0x0F)
    return 4


def code_2e(gb):
    """ LD L,d8 """
    d8 = gb.cpu.read_next_byte_from_cartridge()
    gb.cpu.register.set_l(d8)
    return 8


def code_2f(gb):
    """ CPL - Logical complement of register A (i.e. flip all bits) """
    gb.cpu.register.set_a((~ gb.cpu.register.A) & 0xFF)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag(True)
    return 4


# OPCODES 3x
def code_30(gb):
    """ JR NC,r8 - If flag C is reset, add r8 to current address and jump to it """
    r8 = gb.cpu.read_next_byte_from_cartridge()  # Has to be read even if it is not going to be used
    if not gb.cpu.register.get_c_flag():
        r8 = util.convert_unsigned_integer_to_signed(r8)
        gb.cpu.register.set_pc((gb.cpu.register.PC + r8) & 0xFFFF)
        return 12
    return 8


def code_31(gb):
    """ LD SP,d16 - Stores given 16-bit value at SP """
    lsb = gb.cpu.read_next_byte_from_cartridge()
    msb = gb.cpu.read_next_byte_from_cartridge()
    d16 = get_big_endian_value(msb, lsb)
    gb.cpu.register.set_sp(d16)
    return 12


def code_32(gb):
    """ LD (HL-),A or LD (HLD),A or LDD (HL),A - Put value at A into address HL. Decrement HL """
    gb.memory.write_8bit(gb.cpu.register.get_hl(), gb.cpu.register.A)
    gb.cpu.register.set_hl((gb.cpu.register.get_hl() - 1) & 0xFFFF)
    return 8


def code_33(gb):
    """ INC SP - SP=SP+1 """
    gb.cpu.register.set_sp((gb.cpu.register.SP + 1) & 0xFFFF)
    return 8


def code_34(gb):
    """ INC (HL) - (value at address HL)=(value at address HL)+1 """
    current_value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    new_value = (current_value + 1) & 0xFF
    gb.memory.write_8bit(gb.cpu.register.get_hl(), new_value)
    gb.cpu.register.set_z_flag(new_value == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag((new_value & 0x0F) == 0)
    return 12


def code_35(gb):
    """ DEC (HL) - (value at address HL)=(value at address HL)-1 """
    current_value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    new_value = (current_value - 1) & 0xFF
    gb.memory.write_8bit(gb.cpu.register.get_hl(), new_value)
    gb.cpu.register.set_z_flag(new_value == 0)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((new_value & 0x0F) == 0x0F)
    return 12


def code_36(gb):
    """ LD (HL),d8 - Stores d8 at the address in HL """
    d8 = gb.cpu.read_next_byte_from_cartridge()
    gb.memory.write_8bit(gb.cpu.register.get_hl(), d8)
    return 12


def code_37(gb):
    """ SCF - Set carry flag """
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(True)
    return 4


def code_38(gb):
    """ JR C,r8 - If flag C is set, add r8 to current address and jump to it """
    r8 = gb.cpu.read_next_byte_from_cartridge()  # Has to be read even if it is not going to be used
    if gb.cpu.register.get_c_flag():
        r8 = util.convert_unsigned_integer_to_signed(r8)
        gb.cpu.register.set_pc((gb.cpu.register.PC + r8) & 0xFFFF)
        return 12
    return 8


def code_39(gb):
    """ ADD HL,SP - HL=HL+SP """
    result = gb.cpu.register.get_hl() + gb.cpu.register.SP
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(((gb.cpu.register.get_hl() & 0x0FFF) + (gb.cpu.register.SP & 0x0FFF)) > 0x0FFF)
    gb.cpu.register.set_c_flag(result > 0xFFFF)
    gb.cpu.register.set_hl(result & 0xFFFF)
    return 8


def code_3a(gb):
    """ LD A,(HL-) or LD A,(HLD) or LDD A,(HL) - Put value at address HL into A. Decrement HL """
    gb.cpu.register.set_a(gb.memory.read_8bit(gb.cpu.register.get_hl()))
    gb.cpu.register.set_hl((gb.cpu.register.get_hl() - 1) & 0xFFFF)
    return 8


def code_3b(gb):
    """ DEC SP - SP=SP-1 """
    gb.cpu.register.set_sp((gb.cpu.register.SP - 1) & 0xFFFF)
    return 8


def code_3c(gb):
    """ INC A - A=A+1 """
    gb.cpu.register.set_a((gb.cpu.register.A + 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag((gb.cpu.register.A & 0x0F) == 0)
    return 4


def code_3d(gb):
    """ DEC A - A=A-1 """
    gb.cpu.register.set_a((gb.cpu.register.A - 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((gb.cpu.register.A & 0x0F) == 0x0F)
    return 4


def code_3e(gb):
    """ LD A,d8 """
    d8 = gb.cpu.read_next_byte_from_cartridge()
    gb.cpu.register.set_a(d8)
    return 8


def code_3f(gb):
    """ CCF - Invert carry flag """
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(not gb.cpu.register.get_c_flag())
    return 4


# OPCODES 4x
# noinspection PyUnusedLocal
def code_40(gb):
    """ LD B,B (...why?) """
    return 4


def code_41(gb):
    """ LD B,C """
    gb.cpu.register.set_b(gb.cpu.register.C)
    return 4


def code_42(gb):
    """ LD B,D """
    gb.cpu.register.set_b(gb.cpu.register.D)
    return 4


def code_43(gb):
    """ LD B,E """
    gb.cpu.register.set_b(gb.cpu.register.E)
    return 4


def code_44(gb):
    """ LD B,H """
    gb.cpu.register.set_b(gb.cpu.register.H)
    return 4


def code_45(gb):
    """ LD B,L """
    gb.cpu.register.set_b(gb.cpu.register.L)
    return 4


def code_46(gb):
    """ LD B,(HL) - Load reg with the value at the address in HL """
    gb.cpu.register.set_b(gb.memory.read_8bit(gb.cpu.register.get_hl()))
    return 8


def code_47(gb):
    """ LD B,A """
    gb.cpu.register.set_b(gb.cpu.register.A)
    return 4


def code_48(gb):
    """ LD C,B """
    gb.cpu.register.set_c(gb.cpu.register.B)
    return 4


# noinspection PyUnusedLocal
def code_49(gb):
    """ LD C,C (...why?) """
    return 4


def code_4a(gb):
    """ LD C,D """
    gb.cpu.register.set_c(gb.cpu.register.D)
    return 4


def code_4b(gb):
    """ LD C,E """
    gb.cpu.register.set_c(gb.cpu.register.E)
    return 4


def code_4c(gb):
    """ LD C,H """
    gb.cpu.register.set_c(gb.cpu.register.H)
    return 4


def code_4d(gb):
    """ LD C,L """
    gb.cpu.register.set_c(gb.cpu.register.L)
    return 4


def code_4e(gb):
    """ LD C,(HL) - Load reg with the value at the address in HL """
    gb.cpu.register.set_c(gb.memory.read_8bit(gb.cpu.register.get_hl()))
    return 8


def code_4f(gb):
    """ LD C,A """
    gb.cpu.register.set_c(gb.cpu.register.A)
    return 4


# OPCODES 5x
def code_50(gb):
    """ LD D,B """
    gb.cpu.register.set_d(gb.cpu.register.B)
    return 4


def code_51(gb):
    """ LD D,C """
    gb.cpu.register.set_d(gb.cpu.register.C)
    return 4


# noinspection PyUnusedLocal
def code_52(gb):
    """ LD D,D (...why?) """
    return 4


def code_53(gb):
    """ LD D,E """
    gb.cpu.register.set_d(gb.cpu.register.E)
    return 4


def code_54(gb):
    """ LD D,H """
    gb.cpu.register.set_d(gb.cpu.register.H)
    return 4


def code_55(gb):
    """ LD D,L """
    gb.cpu.register.set_d(gb.cpu.register.L)
    return 4


def code_56(gb):
    """ LD D,(HL) - Load reg with the value at the address in HL """
    gb.cpu.register.set_d(gb.memory.read_8bit(gb.cpu.register.get_hl()))
    return 8


def code_57(gb):
    """ LD D,A """
    gb.cpu.register.set_d(gb.cpu.register.A)
    return 4


def code_58(gb):
    """ LD E,B """
    gb.cpu.register.set_e(gb.cpu.register.B)
    return 4


def code_59(gb):
    """ LD E,C """
    gb.cpu.register.set_e(gb.cpu.register.C)
    return 4


def code_5a(gb):
    """ LD E,D """
    gb.cpu.register.set_e(gb.cpu.register.D)
    return 4


# noinspection PyUnusedLocal
def code_5b(gb):
    """ LD E,E (...why?) """
    return 4


def code_5c(gb):
    """ LD E,H """
    gb.cpu.register.set_e(gb.cpu.register.H)
    return 4


def code_5d(gb):
    """ LD E,L """
    gb.cpu.register.set_e(gb.cpu.register.L)
    return 4


def code_5e(gb):
    """ LD E,(HL) - Load reg with the value at the address in HL """
    gb.cpu.register.set_e(gb.memory.read_8bit(gb.cpu.register.get_hl()))
    return 8


def code_5f(gb):
    """ LD E,A """
    gb.cpu.register.set_e(gb.cpu.register.A)
    return 4


# OPCODES 6x
def code_60(gb):
    """ LD H,B """
    gb.cpu.register.set_h(gb.cpu.register.B)
    return 4


def code_61(gb):
    """ LD H,C """
    gb.cpu.register.set_h(gb.cpu.register.C)
    return 4


def code_62(gb):
    """ LD H,D """
    gb.cpu.register.set_h(gb.cpu.register.D)
    return 4


def code_63(gb):
    """ LD H,E """
    gb.cpu.register.set_h(gb.cpu.register.E)
    return 4


# noinspection PyUnusedLocal
def code_64(gb):
    """ LD H,H (...why?) """
    return 4


def code_65(gb):
    """ LD H,L """
    gb.cpu.register.set_h(gb.cpu.register.L)
    return 4


def code_66(gb):
    """ LD H,(HL) - Load reg with the value at the address in HL """
    gb.cpu.register.set_h(gb.memory.read_8bit(gb.cpu.register.get_hl()))
    return 8


def code_67(gb):
    """ LD H,A """
    gb.cpu.register.set_h(gb.cpu.register.A)
    return 4


def code_68(gb):
    """ LD L,B """
    gb.cpu.register.set_l(gb.cpu.register.B)
    return 4


def code_69(gb):
    """ LD L,C """
    gb.cpu.register.set_l(gb.cpu.register.C)
    return 4


def code_6a(gb):
    """ LD L,D """
    gb.cpu.register.set_l(gb.cpu.register.D)
    return 4


def code_6b(gb):
    """ LD L,E """
    gb.cpu.register.set_l(gb.cpu.register.E)
    return 4


def code_6c(gb):
    """ LD L,H """
    gb.cpu.register.set_l(gb.cpu.register.H)
    return 4


# noinspection PyUnusedLocal
def code_6d(gb):
    """ LD L,L (...why?) """
    return 4


def code_6e(gb):
    """ LD L,(HL) - Load reg with the value at the address in HL """
    gb.cpu.register.set_l(gb.memory.read_8bit(gb.cpu.register.get_hl()))
    return 8


def code_6f(gb):
    """ LD L,A """
    gb.cpu.register.set_l(gb.cpu.register.A)
    return 4


# OPCODES 7x
def code_70(gb):
    """ LD (HL),B - Stores reg at the address in HL """
    gb.memory.write_8bit(gb.cpu.register.get_hl(), gb.cpu.register.B)
    return 8


def code_71(gb):
    """ LD (HL),C - Stores reg at the address in HL """
    gb.memory.write_8bit(gb.cpu.register.get_hl(), gb.cpu.register.C)
    return 8


def code_72(gb):
    """ LD (HL),D - Stores reg at the address in HL """
    gb.memory.write_8bit(gb.cpu.register.get_hl(), gb.cpu.register.D)
    return 8


def code_73(gb):
    """ LD (HL),E - Stores reg at the address in HL """
    gb.memory.write_8bit(gb.cpu.register.get_hl(), gb.cpu.register.E)
    return 8


def code_74(gb):
    """ LD (HL),H - Stores reg at the address in HL """
    gb.memory.write_8bit(gb.cpu.register.get_hl(), gb.cpu.register.H)
    return 8


def code_75(gb):
    """ LD (HL),L - Stores reg at the address in HL """
    gb.memory.write_8bit(gb.cpu.register.get_hl(), gb.cpu.register.L)
    return 8


def code_76(gb):
    """
    HALT - Power down CPU (by stopping the system clock) until an interrupt occurs
    See: http://gbdev.gg8.se/wiki/articles/Reducing_Power_Consumption
    """
    gb.cpu.halted = True
    return 4


def code_77(gb):
    """ LD (HL),A - Stores reg at the address in HL """
    gb.memory.write_8bit(gb.cpu.register.get_hl(), gb.cpu.register.A)
    return 8


def code_78(gb):
    """ LD A,B """
    gb.cpu.register.set_a(gb.cpu.register.B)
    return 4


def code_79(gb):
    """ LD A,C """
    gb.cpu.register.set_a(gb.cpu.register.C)
    return 4


def code_7a(gb):
    """ LD A,D """
    gb.cpu.register.set_a(gb.cpu.register.D)
    return 4


def code_7b(gb):
    """ LD A,E """
    gb.cpu.register.set_a(gb.cpu.register.E)
    return 4


def code_7c(gb):
    """ LD A,H """
    gb.cpu.register.set_a(gb.cpu.register.H)
    return 4


def code_7d(gb):
    """ LD A,L """
    gb.cpu.register.set_a(gb.cpu.register.L)
    return 4


def code_7e(gb):
    """ LD A,(HL) - Load reg with the value at the address in HL """
    gb.cpu.register.set_a(gb.memory.read_8bit(gb.cpu.register.get_hl()))
    return 8


# noinspection PyUnusedLocal
def code_7f(gb):
    """ LD A,A (...why?) """
    return 4


# OPCODES 8x
def code_80(gb):
    """ ADD A,B - A=A+B """
    result = gb.cpu.register.A + gb.cpu.register.B
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(((gb.cpu.register.A & 0x0F) + (gb.cpu.register.B & 0x0F)) > 0x0F)
    gb.cpu.register.set_c_flag(result > 0xFF)
    gb.cpu.register.set_a(result & 0xFF)
    return 4


def code_81(gb):
    """ ADD A,C - A=A+C """
    result = gb.cpu.register.A + gb.cpu.register.C
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(((gb.cpu.register.A & 0x0F) + (gb.cpu.register.C & 0x0F)) > 0x0F)
    gb.cpu.register.set_c_flag(result > 0xFF)
    gb.cpu.register.set_a(result & 0xFF)
    return 4


def code_82(gb):
    """ ADD A,D - A=A+D """
    result = gb.cpu.register.A + gb.cpu.register.D
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(((gb.cpu.register.A & 0x0F) + (gb.cpu.register.D & 0x0F)) > 0x0F)
    gb.cpu.register.set_c_flag(result > 0xFF)
    gb.cpu.register.set_a(result & 0xFF)
    return 4


def code_83(gb):
    """ ADD A,E - A=A+E """
    result = gb.cpu.register.A + gb.cpu.register.E
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(((gb.cpu.register.A & 0x0F) + (gb.cpu.register.E & 0x0F)) > 0x0F)
    gb.cpu.register.set_c_flag(result > 0xFF)
    gb.cpu.register.set_a(result & 0xFF)
    return 4


def code_84(gb):
    """ ADD A,H - A=A+H """
    result = gb.cpu.register.A + gb.cpu.register.H
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(((gb.cpu.register.A & 0x0F) + (gb.cpu.register.H & 0x0F)) > 0x0F)
    gb.cpu.register.set_c_flag(result > 0xFF)
    gb.cpu.register.set_a(result & 0xFF)
    return 4


def code_85(gb):
    """ ADD A,L - A=A+L """
    result = gb.cpu.register.A + gb.cpu.register.L
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(((gb.cpu.register.A & 0x0F) + (gb.cpu.register.L & 0x0F)) > 0x0F)
    gb.cpu.register.set_c_flag(result > 0xFF)
    gb.cpu.register.set_a(result & 0xFF)
    return 4


def code_86(gb):
    """ ADD A,(HL) - A=A+(value at address HL) """
    mem_hl = gb.memory.read_8bit(gb.cpu.register.get_hl())
    result = gb.cpu.register.A + mem_hl
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(((gb.cpu.register.A & 0x0F) + (mem_hl & 0x0F)) > 0x0F)
    gb.cpu.register.set_c_flag(result > 0xFF)
    gb.cpu.register.set_a(result & 0xFF)
    return 8


def code_87(gb):
    """ ADD A,A - A=A+A """
    result = gb.cpu.register.A + gb.cpu.register.A
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(((gb.cpu.register.A & 0x0F) + (gb.cpu.register.A & 0x0F)) > 0x0F)
    gb.cpu.register.set_c_flag(result > 0xFF)
    gb.cpu.register.set_a(result & 0xFF)
    return 4


def code_88(gb):
    """ ADC A,B - A=A+B+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = gb.cpu.register.get_c_flag()
    result = gb.cpu.register.A + gb.cpu.register.B + carry_flag
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(((gb.cpu.register.A & 0x0F) + (gb.cpu.register.B & 0x0F) + carry_flag) > 0x0F)
    gb.cpu.register.set_c_flag(result > 0xFF)
    gb.cpu.register.set_a(result & 0xFF)
    return 4


def code_89(gb):
    """ ADC A,C - A=A+C+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = gb.cpu.register.get_c_flag()
    result = gb.cpu.register.A + gb.cpu.register.C + carry_flag
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(((gb.cpu.register.A & 0x0F) + (gb.cpu.register.C & 0x0F) + carry_flag) > 0x0F)
    gb.cpu.register.set_c_flag(result > 0xFF)
    gb.cpu.register.set_a(result & 0xFF)
    return 4


def code_8a(gb):
    """ ADC A,D - A=A+D+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = gb.cpu.register.get_c_flag()
    result = gb.cpu.register.A + gb.cpu.register.D + carry_flag
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(((gb.cpu.register.A & 0x0F) + (gb.cpu.register.D & 0x0F) + carry_flag) > 0x0F)
    gb.cpu.register.set_c_flag(result > 0xFF)
    gb.cpu.register.set_a(result & 0xFF)
    return 4


def code_8b(gb):
    """ ADC A,E - A=A+E+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = gb.cpu.register.get_c_flag()
    result = gb.cpu.register.A + gb.cpu.register.E + carry_flag
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(((gb.cpu.register.A & 0x0F) + (gb.cpu.register.E & 0x0F) + carry_flag) > 0x0F)
    gb.cpu.register.set_c_flag(result > 0xFF)
    gb.cpu.register.set_a(result & 0xFF)
    return 4


def code_8c(gb):
    """ ADC A,H - A=A+H+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = gb.cpu.register.get_c_flag()
    result = gb.cpu.register.A + gb.cpu.register.H + carry_flag
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(((gb.cpu.register.A & 0x0F) + (gb.cpu.register.H & 0x0F) + carry_flag) > 0x0F)
    gb.cpu.register.set_c_flag(result > 0xFF)
    gb.cpu.register.set_a(result & 0xFF)
    return 4


def code_8d(gb):
    """ ADC A,L - A=A+L+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = gb.cpu.register.get_c_flag()
    result = gb.cpu.register.A + gb.cpu.register.L + carry_flag
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(((gb.cpu.register.A & 0x0F) + (gb.cpu.register.L & 0x0F) + carry_flag) > 0x0F)
    gb.cpu.register.set_c_flag(result > 0xFF)
    gb.cpu.register.set_a(result & 0xFF)
    return 4


def code_8e(gb):
    """ ADC A,(HL) - A=A+(value at address HL)+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = gb.cpu.register.get_c_flag()
    mem_hl = gb.memory.read_8bit(gb.cpu.register.get_hl())
    result = gb.cpu.register.A + mem_hl + carry_flag
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(((gb.cpu.register.A & 0x0F) + (mem_hl & 0x0F) + carry_flag) > 0x0F)
    gb.cpu.register.set_c_flag(result > 0xFF)
    gb.cpu.register.set_a(result & 0xFF)
    return 8


def code_8f(gb):
    """ ADC A,A - A=A+A+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    carry_flag = gb.cpu.register.get_c_flag()
    result = gb.cpu.register.A + gb.cpu.register.A + carry_flag
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(((gb.cpu.register.A & 0x0F) + (gb.cpu.register.A & 0x0F) + carry_flag) > 0x0F)
    gb.cpu.register.set_c_flag(result > 0xFF)
    gb.cpu.register.set_a(result & 0xFF)
    return 4


# OPCODES 9x
def code_90(gb):
    """ SUB A,B - A=A-B """
    result = (gb.cpu.register.A - gb.cpu.register.B) & 0xFF  # '& 0xFF' = convert signed integer to unsigned
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((gb.cpu.register.B & 0x0F) > (gb.cpu.register.A & 0x0F))
    gb.cpu.register.set_c_flag(gb.cpu.register.B > gb.cpu.register.A)
    gb.cpu.register.set_a(result)
    return 4


def code_91(gb):
    """ SUB A,C - A=A-C """
    result = (gb.cpu.register.A - gb.cpu.register.C) & 0xFF  # '& 0xFF' = convert signed integer to unsigned
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((gb.cpu.register.C & 0x0F) > (gb.cpu.register.A & 0x0F))
    gb.cpu.register.set_c_flag(gb.cpu.register.C > gb.cpu.register.A)
    gb.cpu.register.set_a(result)
    return 4


def code_92(gb):
    """ SUB A,D - A=A-D """
    result = (gb.cpu.register.A - gb.cpu.register.D) & 0xFF  # '& 0xFF' = convert signed integer to unsigned
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((gb.cpu.register.D & 0x0F) > (gb.cpu.register.A & 0x0F))
    gb.cpu.register.set_c_flag(gb.cpu.register.D > gb.cpu.register.A)
    gb.cpu.register.set_a(result)
    return 4


def code_93(gb):
    """ SUB A,E - A=A-E """
    result = (gb.cpu.register.A - gb.cpu.register.E) & 0xFF  # '& 0xFF' = convert signed integer to unsigned
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((gb.cpu.register.E & 0x0F) > (gb.cpu.register.A & 0x0F))
    gb.cpu.register.set_c_flag(gb.cpu.register.E > gb.cpu.register.A)
    gb.cpu.register.set_a(result)
    return 4


def code_94(gb):
    """ SUB A,H - A=A-H """
    result = (gb.cpu.register.A - gb.cpu.register.H) & 0xFF  # '& 0xFF' = convert signed integer to unsigned
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((gb.cpu.register.H & 0x0F) > (gb.cpu.register.A & 0x0F))
    gb.cpu.register.set_c_flag(gb.cpu.register.H > gb.cpu.register.A)
    gb.cpu.register.set_a(result)
    return 4


def code_95(gb):
    """ SUB A,L - A=A-L """
    result = (gb.cpu.register.A - gb.cpu.register.L) & 0xFF  # '& 0xFF' = convert signed integer to unsigned
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((gb.cpu.register.L & 0x0F) > (gb.cpu.register.A & 0x0F))
    gb.cpu.register.set_c_flag(gb.cpu.register.L > gb.cpu.register.A)
    gb.cpu.register.set_a(result)
    return 4


def code_96(gb):
    """ SUB A,(HL) - A=A-(value at address HL) """
    mem_hl = gb.memory.read_8bit(gb.cpu.register.get_hl())
    result = (gb.cpu.register.A - mem_hl) & 0xFF  # '& 0xFF' = convert signed integer to unsigned
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((mem_hl & 0x0F) > (gb.cpu.register.A & 0x0F))
    gb.cpu.register.set_c_flag(mem_hl > gb.cpu.register.A)
    gb.cpu.register.set_a(result)
    return 8


def code_97(gb):
    """ SUB A,A - A=A-A """
    gb.cpu.register.set_z_flag(True)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    gb.cpu.register.set_a(0x00)  # A-A, therefore result is zero, always
    return 4


def code_98(gb):
    """ SBC A,B - A=A-B-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    value = gb.cpu.register.B + gb.cpu.register.get_c_flag()
    result = (gb.cpu.register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((value & 0x0F) > (gb.cpu.register.A & 0x0F))
    gb.cpu.register.set_c_flag(value > gb.cpu.register.A)
    gb.cpu.register.set_a(result)
    return 4


def code_99(gb):
    """ SBC A,C - A=A-C-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    value = gb.cpu.register.C + gb.cpu.register.get_c_flag()
    result = (gb.cpu.register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((value & 0x0F) > (gb.cpu.register.A & 0x0F))
    gb.cpu.register.set_c_flag(value > gb.cpu.register.A)
    gb.cpu.register.set_a(result)
    return 4


def code_9a(gb):
    """ SBC A,D - A=A-D-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    value = gb.cpu.register.D + gb.cpu.register.get_c_flag()
    result = (gb.cpu.register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((value & 0x0F) > (gb.cpu.register.A & 0x0F))
    gb.cpu.register.set_c_flag(value > gb.cpu.register.A)
    gb.cpu.register.set_a(result)
    return 4


def code_9b(gb):
    """ SBC A,E - A=A-E-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    value = gb.cpu.register.E + gb.cpu.register.get_c_flag()
    result = (gb.cpu.register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((value & 0x0F) > (gb.cpu.register.A & 0x0F))
    gb.cpu.register.set_c_flag(value > gb.cpu.register.A)
    gb.cpu.register.set_a(result)
    return 4


def code_9c(gb):
    """ SBC A,H - A=A-H-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    value = gb.cpu.register.H + gb.cpu.register.get_c_flag()
    result = (gb.cpu.register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((value & 0x0F) > (gb.cpu.register.A & 0x0F))
    gb.cpu.register.set_c_flag(value > gb.cpu.register.A)
    gb.cpu.register.set_a(result)
    return 4


def code_9d(gb):
    """ SBC A,L - A=A-L-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    value = gb.cpu.register.L + gb.cpu.register.get_c_flag()
    result = (gb.cpu.register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((value & 0x0F) > (gb.cpu.register.A & 0x0F))
    gb.cpu.register.set_c_flag(value > gb.cpu.register.A)
    gb.cpu.register.set_a(result)
    return 4


def code_9e(gb):
    """ SBC A,(HL) - A=A-(value at address HL)-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    mem_hl = gb.memory.read_8bit(gb.cpu.register.get_hl())
    value = mem_hl + gb.cpu.register.get_c_flag()
    result = (gb.cpu.register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((value & 0x0F) > (gb.cpu.register.A & 0x0F))
    gb.cpu.register.set_c_flag(value > gb.cpu.register.A)
    gb.cpu.register.set_a(result)
    return 8


def code_9f(gb):
    """ SBC A,A - A=A-A-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    carry_flag = gb.cpu.register.get_c_flag()
    result = (-carry_flag) & 0xFF  # A-A-carry_flag, therefore result is -carry_flag, always
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag(carry_flag)
    gb.cpu.register.set_c_flag(carry_flag)
    gb.cpu.register.set_a(result)
    return 4


# OPCODES Ax
def code_a0(gb):
    """ AND B - A=Logical AND A with B """
    gb.cpu.register.set_a(gb.cpu.register.A & gb.cpu.register.B)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    gb.cpu.register.set_c_flag(False)
    return 4


def code_a1(gb):
    """ AND C - A=Logical AND A with C """
    gb.cpu.register.set_a(gb.cpu.register.A & gb.cpu.register.C)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    gb.cpu.register.set_c_flag(False)
    return 4


def code_a2(gb):
    """ AND D - A=Logical AND A with D """
    gb.cpu.register.set_a(gb.cpu.register.A & gb.cpu.register.D)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    gb.cpu.register.set_c_flag(False)
    return 4


def code_a3(gb):
    """ AND E - A=Logical AND A with E """
    gb.cpu.register.set_a(gb.cpu.register.A & gb.cpu.register.E)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    gb.cpu.register.set_c_flag(False)
    return 4


def code_a4(gb):
    """ AND H - A=Logical AND A with H """
    gb.cpu.register.set_a(gb.cpu.register.A & gb.cpu.register.H)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    gb.cpu.register.set_c_flag(False)
    return 4


def code_a5(gb):
    """ AND L - A=Logical AND A with L """
    gb.cpu.register.set_a(gb.cpu.register.A & gb.cpu.register.L)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    gb.cpu.register.set_c_flag(False)
    return 4


def code_a6(gb):
    """ AND (HL) - A=Logical AND A with (value at address HL) """
    gb.cpu.register.set_a(gb.cpu.register.A & gb.memory.read_8bit(gb.cpu.register.get_hl()))
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    gb.cpu.register.set_c_flag(False)
    return 8


def code_a7(gb):
    """ AND A - A=Logical AND A with A (why?) """
    # gb.cpu.register.set_a(gb.cpu.register.A & gb.cpu.register.A -- result is A=A, therefore useless
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    gb.cpu.register.set_c_flag(False)
    return 4


def code_a8(gb):
    """ XOR B - A=Logical XOR A with B """
    gb.cpu.register.set_a(gb.cpu.register.A ^ gb.cpu.register.B)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    return 4


def code_a9(gb):
    """ XOR C - A=Logical XOR A with C """
    gb.cpu.register.set_a(gb.cpu.register.A ^ gb.cpu.register.C)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    return 4


def code_aa(gb):
    """ XOR D - A=Logical XOR A with D """
    gb.cpu.register.set_a(gb.cpu.register.A ^ gb.cpu.register.D)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    return 4


def code_ab(gb):
    """ XOR E - A=Logical XOR A with E """
    gb.cpu.register.set_a(gb.cpu.register.A ^ gb.cpu.register.E)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    return 4


def code_ac(gb):
    """ XOR H - A=Logical XOR A with H """
    gb.cpu.register.set_a(gb.cpu.register.A ^ gb.cpu.register.H)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    return 4


def code_ad(gb):
    """ XOR L - A=Logical XOR A with L """
    gb.cpu.register.set_a(gb.cpu.register.A ^ gb.cpu.register.L)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    return 4


def code_ae(gb):
    """ XOR (HL) - A=Logical XOR A with (value at address HL) """
    gb.cpu.register.set_a(gb.cpu.register.A ^ gb.memory.read_8bit(gb.cpu.register.get_hl()))
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    return 8


def code_af(gb):
    """ XOR A - A=Logical XOR A with A """
    gb.cpu.register.set_a(0)
    gb.cpu.register.set_z_flag(True)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    return 4


# OPCODES Bx
def code_b0(gb):
    """ OR B - A=Logical OR A with B """
    gb.cpu.register.set_a(gb.cpu.register.A | gb.cpu.register.B)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    return 4


def code_b1(gb):
    """ OR C - A=Logical OR A with C """
    gb.cpu.register.set_a(gb.cpu.register.A | gb.cpu.register.C)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    return 4


def code_b2(gb):
    """ OR D - A=Logical OR A with D """
    gb.cpu.register.set_a(gb.cpu.register.A | gb.cpu.register.D)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    return 4


def code_b3(gb):
    """ OR E - A=Logical OR A with E """
    gb.cpu.register.set_a(gb.cpu.register.A | gb.cpu.register.E)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    return 4


def code_b4(gb):
    """ OR H - A=Logical OR A with H """
    gb.cpu.register.set_a(gb.cpu.register.A | gb.cpu.register.H)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    return 4


def code_b5(gb):
    """ OR L - A=Logical OR A with L """
    gb.cpu.register.set_a(gb.cpu.register.A | gb.cpu.register.L)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    return 4


def code_b6(gb):
    """ OR (HL) - A=Logical OR A with (value at address HL) """
    gb.cpu.register.set_a(gb.cpu.register.A | gb.memory.read_8bit(gb.cpu.register.get_hl()))
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    return 8


def code_b7(gb):
    """ OR L - A=Logical OR A with A (why?) """
    # gb.cpu.register.set_a(gb.cpu.register.A | gb.cpu.register.A -- result is A=A, therefore useless
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    return 4


def code_b8(gb):
    """ CP A,B - same as SUB A,B but throw the result away, only set flags """
    gb.cpu.register.set_z_flag(gb.cpu.register.A == gb.cpu.register.B)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((gb.cpu.register.B & 0x0F) > (gb.cpu.register.A & 0x0F))
    gb.cpu.register.set_c_flag(gb.cpu.register.B > gb.cpu.register.A)
    return 4


def code_b9(gb):
    """ CP A,C - same as SUB A,C but throw the result away, only set flags """
    gb.cpu.register.set_z_flag(gb.cpu.register.A == gb.cpu.register.C)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((gb.cpu.register.C & 0x0F) > (gb.cpu.register.A & 0x0F))
    gb.cpu.register.set_c_flag(gb.cpu.register.C > gb.cpu.register.A)
    return 4


def code_ba(gb):
    """ CP A,D - same as SUB A,D but throw the result away, only set flags """
    gb.cpu.register.set_z_flag(gb.cpu.register.A == gb.cpu.register.D)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((gb.cpu.register.D & 0x0F) > (gb.cpu.register.A & 0x0F))
    gb.cpu.register.set_c_flag(gb.cpu.register.D > gb.cpu.register.A)
    return 4


def code_bb(gb):
    """ CP A,E - same as SUB A,E but throw the result away, only set flags """
    gb.cpu.register.set_z_flag(gb.cpu.register.A == gb.cpu.register.E)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((gb.cpu.register.E & 0x0F) > (gb.cpu.register.A & 0x0F))
    gb.cpu.register.set_c_flag(gb.cpu.register.E > gb.cpu.register.A)
    return 4


def code_bc(gb):
    """ CP A,H - same as SUB A,H but throw the result away, only set flags """
    gb.cpu.register.set_z_flag(gb.cpu.register.A == gb.cpu.register.H)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((gb.cpu.register.H & 0x0F) > (gb.cpu.register.A & 0x0F))
    gb.cpu.register.set_c_flag(gb.cpu.register.H > gb.cpu.register.A)
    return 4


def code_bd(gb):
    """ CP A,L - same as SUB A,L but throw the result away, only set flags """
    gb.cpu.register.set_z_flag(gb.cpu.register.A == gb.cpu.register.L)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((gb.cpu.register.L & 0x0F) > (gb.cpu.register.A & 0x0F))
    gb.cpu.register.set_c_flag(gb.cpu.register.L > gb.cpu.register.A)
    return 4


def code_be(gb):
    """ CP A,(HL) - same as SUB A,(HL) but throw the result away, only set flags """
    mem_hl = gb.memory.read_8bit(gb.cpu.register.get_hl())
    gb.cpu.register.set_z_flag(gb.cpu.register.A == mem_hl)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((mem_hl & 0x0F) > (gb.cpu.register.A & 0x0F))
    gb.cpu.register.set_c_flag(mem_hl > gb.cpu.register.A)
    return 8


def code_bf(gb):
    """ CP A,A - same as SUB A,A but throw the result away, only set flags """
    gb.cpu.register.set_z_flag(True)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    return 4


# OPCODES Cx
def code_c0(gb):
    """ RET NZ - Return if flag Z is reset """
    if not gb.cpu.register.get_z_flag():
        code_c9(gb)
        return 20  # Yes, ignore cycle count from C9
    return 8


def code_c1(gb):
    """ POP BC - Copy 16-bit value from stack (i.e. SP address) into BC, then increment SP by 2 """
    lsb = gb.memory.read_8bit(gb.cpu.register.SP)
    msb = gb.memory.read_8bit(gb.cpu.register.SP + 1)
    gb.cpu.register.set_bc(get_big_endian_value(msb,lsb))
    gb.cpu.register.set_sp((gb.cpu.register.SP + 2) & 0xFFFF)
    return 12


def code_c2(gb):
    """ JP NZ,a16 - Jump to address a16 if Z flag is reset """
    lsb = gb.cpu.read_next_byte_from_cartridge()
    msb = gb.cpu.read_next_byte_from_cartridge()
    a16 = get_big_endian_value(msb,lsb)
    if not gb.cpu.register.get_z_flag():
        gb.cpu.register.set_pc(a16)
        return 16
    return 12


def code_c3(gb):
    """ JP a16 - Jump to address a16 """
    lsb = gb.cpu.read_next_byte_from_cartridge()
    msb = gb.cpu.read_next_byte_from_cartridge()
    a16 = get_big_endian_value(msb,lsb)
    gb.cpu.register.set_pc(a16)
    return 16


def code_c4(gb):
    """ CALL NZ,a16 - Call address a16 if flag Z is reset """
    lsb = gb.cpu.read_next_byte_from_cartridge()
    msb = gb.cpu.read_next_byte_from_cartridge()
    a16 = get_big_endian_value(msb,lsb)
    if not gb.cpu.register.get_z_flag():
        gb.cpu.register.set_sp((gb.cpu.register.SP - 2) & 0xFFFF)
        gb.memory.write_16bit(gb.cpu.register.SP, gb.cpu.register.PC)
        gb.cpu.register.set_pc(a16)
        return 24
    return 12


def code_c5(gb):
    """ PUSH BC - Decrement SP by 2 then push BC value onto stack (i.e. SP address) """
    gb.cpu.register.set_sp((gb.cpu.register.SP - 2) & 0xFFFF)
    gb.memory.write_16bit(gb.cpu.register.SP, gb.cpu.register.get_bc())
    return 16


def code_c6(gb):
    """ ADD A,d8 - A=A+d8 """
    d8 = gb.cpu.read_next_byte_from_cartridge()
    result = gb.cpu.register.A + d8
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(((gb.cpu.register.A & 0x0F) + (d8 & 0x0F)) > 0x0F)
    gb.cpu.register.set_c_flag(result > 0xFF)
    gb.cpu.register.set_a(result & 0xFF)
    return 8


def code_c7(gb):
    """ RST 00H - Push present address onto stack, jump to address $0000 + 00H """
    gb.cpu.register.set_sp((gb.cpu.register.SP - 2) & 0xFFFF)  # Increase stack
    gb.memory.write_16bit(gb.cpu.register.SP, gb.cpu.register.PC)  # Store PC into new stack element
    gb.cpu.register.set_pc(0x0000)
    return 16


def code_c8(gb):
    """ RET Z - Return if flag Z is set """
    if gb.cpu.register.get_z_flag():
        code_c9(gb)
        return 20  # Yes, ignore cycle count from C9
    return 8


def code_c9(gb):
    """ RET - Pop two bytes from stack and jump to that address """
    # Stack starts at FFFE and grows in inverse order (FFFD, FFFC, etc), and data is stored in little endian,
    # therefore (SP) contains lsb and (SP+1) contains msb.
    return_address_lsb = gb.memory.read_8bit(gb.cpu.register.SP)
    return_address_msb = gb.memory.read_8bit(gb.cpu.register.SP + 1)
    gb.cpu.register.set_pc(get_big_endian_value(return_address_msb, return_address_lsb))
    gb.cpu.register.set_sp((gb.cpu.register.SP + 2) & 0xFFFF)
    return 16


def code_ca(gb):
    """ JP Z,a16 - Jump to address a16 if Z flag is set """
    lsb = gb.cpu.read_next_byte_from_cartridge()
    msb = gb.cpu.read_next_byte_from_cartridge()
    a16 = get_big_endian_value(msb, lsb)
    if gb.cpu.register.get_z_flag():
        gb.cpu.register.set_pc(a16)
        return 16
    return 12


def code_cb(gb):
    """ PREFIX CB - Prefix for accessing the extra CB functions """
    opcode = gb.cpu.read_next_byte_from_cartridge()
    return 4 + _instruction_cb_dict[opcode](gb)


def code_cc(gb):
    """ CALL Z,a16 - Call address a16 if flag Z is set """
    lsb = gb.cpu.read_next_byte_from_cartridge()
    msb = gb.cpu.read_next_byte_from_cartridge()
    a16 = get_big_endian_value(msb, lsb)
    if gb.cpu.register.get_z_flag():
        gb.cpu.register.set_sp((gb.cpu.register.SP - 2) & 0xFFFF)
        gb.memory.write_16bit(gb.cpu.register.SP, gb.cpu.register.PC)
        gb.cpu.register.set_pc(a16)
        return 24
    return 12


def code_cd(gb):
    """ CALL a16 - Push address of next instruction onto stack then jump to address a16 """
    lsb = gb.cpu.read_next_byte_from_cartridge()
    msb = gb.cpu.read_next_byte_from_cartridge()
    a16 = get_big_endian_value(msb, lsb)
    gb.cpu.register.set_sp((gb.cpu.register.SP - 2) & 0xFFFF)
    gb.memory.write_16bit(gb.cpu.register.SP, gb.cpu.register.PC)
    gb.cpu.register.set_pc(a16)
    return 24


def code_ce(gb):
    """ ADC A,d8 - A=A+d8+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    d8 = gb.cpu.read_next_byte_from_cartridge()
    carry_flag = gb.cpu.register.get_c_flag()
    result = gb.cpu.register.A + d8 + carry_flag
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(((gb.cpu.register.A & 0x0F) + (d8 & 0x0F) + carry_flag) > 0x0F)
    gb.cpu.register.set_c_flag(result > 0xFF)
    gb.cpu.register.set_a(result & 0xFF)
    return 8


def code_cf(gb):
    """ RST 08H - Push present address onto stack, jump to address $0000 + 08H """
    gb.cpu.register.set_sp((gb.cpu.register.SP - 2) & 0xFFFF)  # Increase stack
    gb.memory.write_16bit(gb.cpu.register.SP, gb.cpu.register.PC)  # Store PC into new stack element
    gb.cpu.register.set_pc(0x0008)
    return 16


# OPCODES Dx
def code_d0(gb):
    """ RET NC - Return if flag C is reset """
    if not gb.cpu.register.get_c_flag():
        return 4 + code_c9(gb)
    return 8


def code_d1(gb):
    """ POP DE - Copy 16-bit value from stack (i.e. SP address) into DE, then increment SP by 2 """
    lsb = gb.memory.read_8bit(gb.cpu.register.SP)
    msb = gb.memory.read_8bit(gb.cpu.register.SP + 1)
    gb.cpu.register.set_de(get_big_endian_value(msb, lsb))
    gb.cpu.register.set_sp((gb.cpu.register.SP + 2) & 0xFFFF)
    return 12


def code_d2(gb):
    """ JP NC,a16 - Jump to address a16 if C flag is reset """
    lsb = gb.cpu.read_next_byte_from_cartridge()
    msb = gb.cpu.read_next_byte_from_cartridge()
    a16 = get_big_endian_value(msb, lsb)
    if not gb.cpu.register.get_c_flag():
        gb.cpu.register.set_pc(a16)
        return 16
    return 12


# noinspection PyUnusedLocal
def code_d3(gb):
    """ Unused opcode """
    return 0


def code_d4(gb):
    """ CALL NC,a16 - Call address a16 if flag C is reset """
    lsb = gb.cpu.read_next_byte_from_cartridge()
    msb = gb.cpu.read_next_byte_from_cartridge()
    a16 = get_big_endian_value(msb, lsb)
    if not gb.cpu.register.get_c_flag():
        gb.cpu.register.set_sp((gb.cpu.register.SP - 2) & 0xFFFF)
        gb.memory.write_16bit(gb.cpu.register.SP, gb.cpu.register.PC)
        gb.cpu.register.set_pc(a16)
        return 24
    return 12


def code_d5(gb):
    """ PUSH DE - Decrement SP by 2 then push DE value onto stack (i.e. SP address) """
    gb.cpu.register.set_sp((gb.cpu.register.SP - 2) & 0xFFFF)
    gb.memory.write_16bit(gb.cpu.register.SP, gb.cpu.register.get_de())
    return 16


def code_d6(gb):
    """ SUB A,d8 - A=A-d8 """
    d8 = gb.cpu.read_next_byte_from_cartridge()
    result = (gb.cpu.register.A - d8) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((d8 & 0x0F) > (gb.cpu.register.A & 0x0F))
    gb.cpu.register.set_c_flag(d8 > gb.cpu.register.A)
    gb.cpu.register.set_a(result)
    return 8


def code_d7(gb):
    """ RST 10H - Push present address onto stack, jump to address $0000 + 10H """
    gb.cpu.register.set_sp((gb.cpu.register.SP - 2) & 0xFFFF)  # Increase stack
    gb.memory.write_16bit(gb.cpu.register.SP, gb.cpu.register.PC)  # Store PC into new stack element
    gb.cpu.register.set_pc(0x0010)
    return 16


def code_d8(gb):
    """ RET C - Return if flag C is set """
    if gb.cpu.register.get_c_flag():
        return 4 + code_c9(gb)
    return 8


def code_d9(gb):
    """ RETI - Pop two bytes from stack and jump to that address then enable interrupts  - same as EI + RET """
    code_c9(gb)
    # Interrupt update will execute next. EI enables interrupts after next instruction, but since the next instruction
    # has already been executed (RET), interrupts must be enabled now. For the sake of keeping equal to EI and DI,
    # interrupts will be enabled at the interrupt update step and not here (see: Interrupts.update()).
    return 16


def code_da(gb):
    """ JP C,a16 - Jump to address a16 if C flag is set """
    lsb = gb.cpu.read_next_byte_from_cartridge()
    msb = gb.cpu.read_next_byte_from_cartridge()
    a16 = get_big_endian_value(msb, lsb)
    if gb.cpu.register.get_c_flag():
        gb.cpu.register.set_pc(a16)
        return 16
    return 12


# noinspection PyUnusedLocal
def code_db(gb):
    """ Unused opcode """
    return 0


def code_dc(gb):
    """ CALL C,a16 - Call address a16 if flag C is set """
    lsb = gb.cpu.read_next_byte_from_cartridge()
    msb = gb.cpu.read_next_byte_from_cartridge()
    a16 = get_big_endian_value(msb, lsb)
    if gb.cpu.register.get_c_flag():
        gb.cpu.register.set_sp((gb.cpu.register.SP - 2) & 0xFFFF)
        gb.memory.write_16bit(gb.cpu.register.SP, gb.cpu.register.PC)
        gb.cpu.register.set_pc(a16)
        return 24
    return 12


# noinspection PyUnusedLocal
def code_dd(gb):
    """ Unused opcode """
    return 0


def code_de(gb):
    """ SBC A,d8 - A=A-d8-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    d8 = gb.cpu.read_next_byte_from_cartridge()
    value = d8 + gb.cpu.register.get_c_flag()
    result = (gb.cpu.register.A - value) & 0xFF  # '& 0xFF' is necessary to convert signed integer to unsigned
    gb.cpu.register.set_z_flag((result & 0xFF) == 0)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((value & 0x0F) > (gb.cpu.register.A & 0x0F))
    gb.cpu.register.set_c_flag(value > gb.cpu.register.A)
    gb.cpu.register.set_a(result)
    return 8


def code_df(gb):
    """ RST 18H - Push present address onto stack, jump to address $0000 + 18H """
    gb.cpu.register.set_sp((gb.cpu.register.SP - 2) & 0xFFFF)  # Increase stack
    gb.memory.write_16bit(gb.cpu.register.SP, gb.cpu.register.PC)  # Store PC into new stack element
    gb.cpu.register.set_pc(0x0018)
    return 16


# OPCODES Ex
def code_e0(gb):
    """ LDH (d8),A or LD ($FF00+d8),A - Put A into address ($FF00 + d8) """
    d8 = gb.cpu.read_next_byte_from_cartridge()
    address = (0xFF00 + d8) & 0xFFFF
    gb.memory.write_8bit(address,gb.cpu.register.A)
    return 12


def code_e1(gb):
    """ POP HL - Copy 16-bit value from stack (i.e. SP address) into HL, then increment SP by 2 """
    lsb = gb.memory.read_8bit(gb.cpu.register.SP)
    msb = gb.memory.read_8bit(gb.cpu.register.SP + 1)
    gb.cpu.register.set_hl(get_big_endian_value(msb, lsb))
    gb.cpu.register.set_sp((gb.cpu.register.SP + 2) & 0xFFFF)
    return 12


def code_e2(gb):
    """ LD (C),A or LD ($FF00+C),A - Put A into address ($FF00 + register C) """
    address = (0xFF00 + gb.cpu.register.C) & 0xFFFF
    gb.memory.write_8bit(address, gb.cpu.register.A)
    return 8


# noinspection PyUnusedLocal
def code_e3(gb):
    """ Unused opcode """
    return 0


# noinspection PyUnusedLocal
def code_e4(gb):
    """ Unused opcode """
    return 0


def code_e5(gb):
    """ PUSH HL - Decrement SP by 2 then push HL value onto stack (i.e. SP address) """
    gb.cpu.register.set_sp((gb.cpu.register.SP - 2) & 0xFFFF)
    gb.memory.write_16bit(gb.cpu.register.SP, gb.cpu.register.get_hl())
    return 16


def code_e6(gb):
    """ AND d8 - A=Logical AND A with d8 """
    d8 = gb.cpu.read_next_byte_from_cartridge()
    gb.cpu.register.set_a(gb.cpu.register.A & d8)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    gb.cpu.register.set_c_flag(False)
    return 8


def code_e7(gb):
    """ RST 20H - Push present address onto stack, jump to address $0000 + 20H """
    gb.cpu.register.set_sp((gb.cpu.register.SP - 2) & 0xFFFF)  # Increase stack
    gb.memory.write_16bit(gb.cpu.register.SP, gb.cpu.register.PC)  # Store PC into new stack element
    gb.cpu.register.set_pc(0x0020)
    return 16


def code_e8(gb):
    """ ADD SP,r8 - SP=SP+r8 (r8 is a signed value) """
    r8 = gb.cpu.read_next_byte_from_cartridge()
    r8 = util.convert_unsigned_integer_to_signed(r8)
    result = gb.cpu.register.SP + r8
    gb.cpu.register.set_z_flag(False)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(((gb.cpu.register.SP & 0x0F) + (r8 & 0x0F)) > 0x0F)
    gb.cpu.register.set_c_flag(result > 0xFFFF)
    gb.cpu.register.set_sp(result & 0xFFFF)
    return 16


def code_e9(gb):
    """ JP (HL) - Jump to address contained in HL """
    gb.cpu.register.set_pc(gb.memory.read_16bit(gb.cpu.register.get_hl()))
    return 4


def code_ea(gb):
    """ LD (a16),A - Stores reg at the address in a16 (least significant byte first) """
    lsb = gb.cpu.read_next_byte_from_cartridge()
    msb = gb.cpu.read_next_byte_from_cartridge()
    a16 = get_big_endian_value(msb,lsb)
    gb.memory.write_8bit(a16,gb.cpu.register.A)
    return 16


# noinspection PyUnusedLocal
def code_eb(gb):
    """ Unused opcode """
    return 0


# noinspection PyUnusedLocal
def code_ec(gb):
    """ Unused opcode """
    return 0


# noinspection PyUnusedLocal
def code_ed(gb):
    """ Unused opcode """
    return 0


def code_ee(gb):
    """ XOR d8 - A=Logical XOR A with d8 """
    d8 = gb.cpu.read_next_byte_from_cartridge()
    gb.cpu.register.set_a(gb.cpu.register.A ^ d8)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    return 8


def code_ef(gb):
    """ RST 28H - Push present address onto stack, jump to address $0000 + 28H """
    gb.cpu.register.set_sp((gb.cpu.register.SP - 2) & 0xFFFF)  # Increase stack
    gb.memory.write_16bit(gb.cpu.register.SP, gb.cpu.register.PC)  # Store PC into new stack element
    gb.cpu.register.set_pc(0x0028)
    return 16


# OPCODES Fx
def code_f0(gb):
    """ LDH A,(d8) or LD A,($FF00+d8) - Put value at address ($FF00 + d8) into A """
    d8 = gb.cpu.read_next_byte_from_cartridge()
    address = (0xFF00 + d8) & 0xFFFF
    gb.cpu.register.set_a(gb.memory.read_8bit(address))
    return 12


def code_f1(gb):
    """ POP AF - Copy 16-bit value from stack (i.e. SP address) into AF, then increment SP by 2 """
    lsb = gb.memory.read_8bit(gb.cpu.register.SP)
    msb = gb.memory.read_8bit(gb.cpu.register.SP + 1)
    gb.cpu.register.set_af(get_big_endian_value(msb, lsb))
    gb.cpu.register.set_sp((gb.cpu.register.SP + 2) & 0xFFFF)
    return 12


def code_f2(gb):
    """ LD A,(C) or LD A,($FF00+C) - Put value at address ($FF00 + register C) into A """
    address = (0xFF00 + gb.cpu.register.C) & 0xFFFF
    gb.cpu.register.set_a(gb.memory.read_8bit(address))
    return 8


# noinspection PyUnusedLocal
def code_f3(gb):
    """ DI - Disable interrupts AFTER THE NEXT INSTRUCTION IS EXECUTED """
    # Interrupt update will execute next. Since the disable is only after the next instruction, the boolean
    # "disable_IME_after_next_instruction" will be set to true during the interrupt step and not here.
    return 4


# noinspection PyUnusedLocal
def code_f4(gb):
    """ Unused opcode """
    return 0


def code_f5(gb):
    """ PUSH AF - Decrement SP by 2 then push AF value onto stack (i.e. SP address) """
    gb.cpu.register.set_sp((gb.cpu.register.SP - 2) & 0xFFFF)
    gb.memory.write_16bit(gb.cpu.register.SP, gb.cpu.register.get_af())
    return 16


def code_f6(gb):
    """ OR d8 - A=Logical OR A with d8 """
    d8 = gb.cpu.read_next_byte_from_cartridge()
    gb.cpu.register.set_a(gb.cpu.register.A | d8)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    return 8


def code_f7(gb):
    """ RST 30H - Push present address onto stack, jump to address $0000 + 30H """
    gb.cpu.register.set_sp((gb.cpu.register.SP - 2) & 0xFFFF)  # Increase stack
    gb.memory.write_16bit(gb.cpu.register.SP, gb.cpu.register.PC)  # Store PC into new stack element
    gb.cpu.register.set_pc(0x0030)
    return 16


def code_f8(gb):
    """ LD HL,SP+d8 or LDHL SP,r8 - Put result of SP+r8 into HL (r8 is a signed value) """
    r8 = gb.cpu.read_next_byte_from_cartridge()
    r8 = util.convert_unsigned_integer_to_signed(r8)
    result = gb.cpu.register.SP + r8
    gb.cpu.register.set_z_flag(False)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(((gb.cpu.register.SP & 0x0F) + (r8 & 0x0F)) > 0x0F)
    gb.cpu.register.set_c_flag(result > 0xFFFF)
    gb.cpu.register.set_hl(result & 0xFFFF)
    return 12


def code_f9(gb):
    """ LD SP,HL - Put HL value into SP """
    gb.cpu.register.set_sp(gb.cpu.register.get_hl())
    return 8


def code_fa(gb):
    """ LD A,(a16) - Load reg with the value at the address in a16 """
    lsb = gb.cpu.read_next_byte_from_cartridge()
    msb = gb.cpu.read_next_byte_from_cartridge()
    a16 = get_big_endian_value(msb, lsb)
    gb.cpu.register.set_a(gb.memory.read_8bit(a16))
    return 16


# noinspection PyUnusedLocal
def code_fb(gb):
    """ EI - Enable interrupts AFTER THE NEXT INSTRUCTION IS EXECUTED """
    # Interrupt update will execute next. Since the enable is only after the next instruction, the boolean
    # "enable_IME_after_next_instruction" will be set to true during the interrupt step and not here.
    return 4


# noinspection PyUnusedLocal
def code_fc(gb):
    """ Unused opcode """
    return 0


# noinspection PyUnusedLocal
def code_fd(gb):
    """ Unused opcode """
    return 0


def code_fe(gb):
    """ CP A,d8 - same as SUB A,d8 but throw the result away, only set flags """
    d8 = gb.cpu.read_next_byte_from_cartridge()
    gb.cpu.register.set_z_flag(gb.cpu.register.A == d8)
    gb.cpu.register.set_n_flag(True)
    gb.cpu.register.set_h_flag((d8 & 0x0F) > (gb.cpu.register.A & 0x0F))
    gb.cpu.register.set_c_flag(d8 > gb.cpu.register.A)
    return 8


def code_ff(gb):
    """ RST 38H - Push present address onto stack, jump to address $0000 + 38H """
    gb.cpu.register.set_sp((gb.cpu.register.SP - 2) & 0xFFFF)  # Increase stack
    gb.memory.write_16bit(gb.cpu.register.SP, gb.cpu.register.PC)  # Store PC into new stack element
    gb.cpu.register.set_pc(0x0038)
    return 16


""" CB-Prefix operations """


# OPCODES CB 0x
def code_cb_00(gb):
    """ RLC B - Copy register B bit 7 to Carry flag, then rotate register B left """
    bit_7 = gb.cpu.register.B >> 7
    gb.cpu.register.set_b(((gb.cpu.register.B << 1) + bit_7) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.B == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_01(gb):
    """ RLC C - Copy register C bit 7 to Carry flag, then rotate register C left """
    bit_7 = gb.cpu.register.C >> 7
    gb.cpu.register.set_c(((gb.cpu.register.C << 1) + bit_7) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.C == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_02(gb):
    """ RLC D - Copy register D bit 7 to Carry flag, then rotate register D left """
    bit_7 = gb.cpu.register.D >> 7
    gb.cpu.register.set_d(((gb.cpu.register.D << 1) + bit_7) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.D == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_03(gb):
    """ RLC E - Copy register E bit 7 to Carry flag, then rotate register E left """
    bit_7 = gb.cpu.register.E >> 7
    gb.cpu.register.set_e(((gb.cpu.register.E << 1) + bit_7) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.E == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_04(gb):
    """ RLC H - Copy register H bit 7 to Carry flag, then rotate register H left """
    bit_7 = gb.cpu.register.H >> 7
    gb.cpu.register.set_h(((gb.cpu.register.H << 1) + bit_7) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.H == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_05(gb):
    """ RLC L - Copy register L bit 7 to Carry flag, then rotate register L left """
    bit_7 = gb.cpu.register.L >> 7
    gb.cpu.register.set_l(((gb.cpu.register.L << 1) + bit_7) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.L == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_06(gb):
    """ RLC (HL) - Copy (value at address HL) bit 7 to Carry flag, then rotate (value at address HL) left """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    bit_7 = value >> 7
    value = ((value << 1) + bit_7) & 0xFF
    gb.cpu.register.set_z_flag(value == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_7)
    gb.memory.write_8bit(gb.cpu.register.get_hl(),value)
    return 16


def code_cb_07(gb):
    """ RLC A - Copy register A bit 7 to Carry flag, then rotate register A left """
    code_07(gb)  # Does exactly the same thing...
    return 8


def code_cb_08(gb):
    """ RRC B - Copy register B bit 0 to Carry flag, then rotate register B right """
    bit_0 = gb.cpu.register.B & 0b00000001
    gb.cpu.register.set_b(((bit_0 << 7) + (gb.cpu.register.B >> 1)) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.B == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_09(gb):
    """ RRC C - Copy register C bit 0 to Carry flag, then rotate register C right """
    bit_0 = gb.cpu.register.C & 0b00000001
    gb.cpu.register.set_c(((bit_0 << 7) + (gb.cpu.register.C >> 1)) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.C == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_0a(gb):
    """ RRC D - Copy register D bit 0 to Carry flag, then rotate register D right """
    bit_0 = gb.cpu.register.D & 0b00000001
    gb.cpu.register.set_d(((bit_0 << 7) + (gb.cpu.register.D >> 1)) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.D == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_0b(gb):
    """ RRC E - Copy register E bit 0 to Carry flag, then rotate register E right """
    bit_0 = gb.cpu.register.E & 0b00000001
    gb.cpu.register.set_e(((bit_0 << 7) + (gb.cpu.register.E >> 1)) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.E == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_0c(gb):
    """ RRC H - Copy register H bit 0 to Carry flag, then rotate register H right """
    bit_0 = gb.cpu.register.H & 0b00000001
    gb.cpu.register.set_h(((bit_0 << 7) + (gb.cpu.register.H >> 1)) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.H == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_0d(gb):
    """ RRC L - Copy register L bit 0 to Carry flag, then rotate register L right """
    bit_0 = gb.cpu.register.L & 0b00000001
    gb.cpu.register.set_l(((bit_0 << 7) + (gb.cpu.register.L >> 1)) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.L == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_0e(gb):
    """ RRC (HL) - Copy bit 0 to Carry flag, then rotate right """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    bit_0 = value & 0b00000001
    value = ((bit_0 << 7) + (value >> 1)) & 0xFF
    gb.cpu.register.set_z_flag(value == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    gb.memory.write_8bit(gb.cpu.register.get_hl(),value)
    return 16


def code_cb_0f(gb):
    """ RRCA - Copy register A bit 0 to Carry flag, then rotate register A right """
    code_0f(gb)  # Does exactly the same thing...
    return 8


# OPCODES CB 1x
def code_cb_10(gb):
    """ RL B - Copy register B bit 7 to temp, replace B bit 7 w/ Carry flag, rotate B left, copy temp to Carry flag """
    bit_7 = gb.cpu.register.B >> 7
    gb.cpu.register.set_b(((gb.cpu.register.B << 1) + gb.cpu.register.get_c_flag()) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.B == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_11(gb):
    """ RL C - Copy register C bit 7 to temp, replace C bit 7 w/ Carry flag, rotate C left, copy temp to Carry flag """
    bit_7 = gb.cpu.register.C >> 7
    gb.cpu.register.set_c(((gb.cpu.register.C << 1) + gb.cpu.register.get_c_flag()) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.C == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_12(gb):
    """ RL D - Copy register D bit 7 to temp, replace D bit 7 w/ Carry flag, rotate D left, copy temp to Carry flag """
    bit_7 = gb.cpu.register.D >> 7
    gb.cpu.register.set_d(((gb.cpu.register.D << 1) + gb.cpu.register.get_c_flag()) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.D == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_13(gb):
    """ RL E - Copy register E bit 7 to temp, replace E bit 7 w/ Carry flag, rotate E left, copy temp to Carry flag """
    bit_7 = gb.cpu.register.E >> 7
    gb.cpu.register.set_e(((gb.cpu.register.E << 1) + gb.cpu.register.get_c_flag()) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.E == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_14(gb):
    """ RL H - Copy register H bit 7 to temp, replace H bit 7 w/ Carry flag, rotate H left, copy temp to Carry flag """
    bit_7 = gb.cpu.register.H >> 7
    gb.cpu.register.set_h(((gb.cpu.register.H << 1) + gb.cpu.register.get_c_flag()) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.H == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_15(gb):
    """ RL L - Copy register L bit 7 to temp, replace L bit 7 w/ Carry flag, rotate L left, copy temp to Carry flag """
    bit_7 = gb.cpu.register.L >> 7
    gb.cpu.register.set_l(((gb.cpu.register.L << 1) + gb.cpu.register.get_c_flag()) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.L == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_16(gb):
    """ RL (HL) - Copy bit 7 to temp, replace bit 7 w/ Carry flag, rotate left, copy temp to Carry flag """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    bit_7 = value >> 7
    value = ((value << 1) + gb.cpu.register.get_c_flag()) & 0xFF
    gb.cpu.register.set_z_flag(value == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_7)
    gb.memory.write_8bit(gb.cpu.register.get_hl(),value)
    return 16


def code_cb_17(gb):
    """ RL A - Copy register A bit 7 to temp, replace A bit 7 w/ Carry flag, rotate A left, copy temp to Carry flag """
    code_17(gb)  # Does exactly the same thing...
    return 8


def code_cb_18(gb):
    """ RR B - Copy register B bit 0 to temp, replace bit 0 w/ Carry flag, rotate right, copy temp to Carry flag """
    bit_0 = gb.cpu.register.B & 0b00000001
    gb.cpu.register.set_b(((gb.cpu.register.get_c_flag() << 7) + (gb.cpu.register.B >> 1)) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.B == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_19(gb):
    """ RR C - Copy register C bit 0 to temp, replace bit 0 w/ Carry flag, rotate right, copy temp to Carry flag """
    bit_0 = gb.cpu.register.C & 0b00000001
    gb.cpu.register.set_c(((gb.cpu.register.get_c_flag() << 7) + (gb.cpu.register.C >> 1)) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.C == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_1a(gb):
    """ RR D - Copy register D bit 0 to temp, replace bit 0 w/ Carry flag, rotate right, copy temp to Carry flag """
    bit_0 = gb.cpu.register.D & 0b00000001
    gb.cpu.register.set_d(((gb.cpu.register.get_c_flag() << 7) + (gb.cpu.register.D >> 1)) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.D == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_1b(gb):
    """ RR E - Copy register E bit 0 to temp, replace bit 0 w/ Carry flag, rotate right, copy temp to Carry flag """
    bit_0 = gb.cpu.register.E & 0b00000001
    gb.cpu.register.set_e(((gb.cpu.register.get_c_flag() << 7) + (gb.cpu.register.E >> 1)) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.E == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_1c(gb):
    """ RR H - Copy register H bit 0 to temp, replace bit 0 w/ Carry flag, rotate right, copy temp to Carry flag """
    bit_0 = gb.cpu.register.H & 0b00000001
    gb.cpu.register.set_h(((gb.cpu.register.get_c_flag() << 7) + (gb.cpu.register.H >> 1)) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.H == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_1d(gb):
    """ RR L - Copy register L bit 0 to temp, replace bit 0 w/ Carry flag, rotate right, copy temp to Carry flag """
    bit_0 = gb.cpu.register.L & 0b00000001
    gb.cpu.register.set_l(((gb.cpu.register.get_c_flag() << 7) + (gb.cpu.register.L >> 1)) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.L == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_1e(gb):
    """ RR (HL) - Copy (HL) bit 0 to temp, replace bit 0 w/ Carry flag, rotate right, copy temp to Carry flag """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    bit_0 = value & 0b00000001
    value = ((gb.cpu.register.get_c_flag() << 7) + (value >> 1)) & 0xFF
    gb.cpu.register.set_z_flag(value == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    gb.memory.write_8bit(gb.cpu.register.get_hl(),value)
    return 16


def code_cb_1f(gb):
    """ RRA - Copy register A bit 0 to temp, replace A bit 0 w/ Carry flag, rotate A right, copy temp to Carry flag """
    code_1f(gb)  # Does exactly the same thing...
    return 8


# OPCODES CB 2x
def code_cb_20(gb):
    """ SLA B - Copy register B bit 7 to temp, replace B bit 7 w/ zero, rotate B left, copy temp to Carry flag """
    bit_7 = gb.cpu.register.B >> 7
    gb.cpu.register.set_b((gb.cpu.register.B << 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.B == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_21(gb):
    """ SLA C - Copy register C bit 7 to temp, replace C bit 7 w/ zero, rotate C left, copy temp to Carry flag """
    bit_7 = gb.cpu.register.C >> 7
    gb.cpu.register.set_c((gb.cpu.register.C << 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.C == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_22(gb):
    """ SLA D - Copy register D bit 7 to temp, replace D bit 7 w/ zero, rotate D left, copy temp to Carry flag """
    bit_7 = gb.cpu.register.D >> 7
    gb.cpu.register.set_d((gb.cpu.register.D << 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.D == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_23(gb):
    """ SLA E - Copy register E bit 7 to temp, replace E bit 7 w/ zero, rotate E left, copy temp to Carry flag """
    bit_7 = gb.cpu.register.E >> 7
    gb.cpu.register.set_e((gb.cpu.register.E << 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.E == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_24(gb):
    """ SLA H - Copy register H bit 7 to temp, replace H bit 7 w/ zero, rotate H left, copy temp to Carry flag """
    bit_7 = gb.cpu.register.H >> 7
    gb.cpu.register.set_h((gb.cpu.register.H << 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.H == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_25(gb):
    """ SLA L - Copy register L bit 7 to temp, replace L bit 7 w/ zero, rotate L left, copy temp to Carry flag """
    bit_7 = gb.cpu.register.L >> 7
    gb.cpu.register.set_l((gb.cpu.register.L << 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.L == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_26(gb):
    """ SLA (HL) - Copy bit 7 to temp, replace bit 7 w/ zero, rotate left, copy temp to Carry flag """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    bit_7 = value >> 7
    value = (value << 1) & 0xFF
    gb.cpu.register.set_z_flag(value == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_7)
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_27(gb):
    """ SLA A - Copy register A bit 7 to temp, replace A bit 7 w/ zero, rotate A left, copy temp to Carry flag """
    bit_7 = gb.cpu.register.A >> 7
    gb.cpu.register.set_a((gb.cpu.register.A << 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_7)
    return 8


def code_cb_28(gb):
    """ SRA B - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_7 = gb.cpu.register.B >> 7
    bit_0 = gb.cpu.register.B & 0b00000001
    gb.cpu.register.set_b(((bit_7 << 7) + (gb.cpu.register.B >> 1)) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.B == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_29(gb):
    """ SRA C - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_7 = gb.cpu.register.C >> 7
    bit_0 = gb.cpu.register.C & 0b00000001
    gb.cpu.register.set_c(((bit_7 << 7) + (gb.cpu.register.C >> 1)) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.C == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_2a(gb):
    """ SRA D - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_7 = gb.cpu.register.D >> 7
    bit_0 = gb.cpu.register.D & 0b00000001
    gb.cpu.register.set_d(((bit_7 << 7) + (gb.cpu.register.D >> 1)) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.D == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_2b(gb):
    """ SRA E - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_7 = gb.cpu.register.E >> 7
    bit_0 = gb.cpu.register.E & 0b00000001
    gb.cpu.register.set_e(((bit_7 << 7) + (gb.cpu.register.E >> 1)) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.E == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_2c(gb):
    """ SRA H - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_7 = gb.cpu.register.H >> 7
    bit_0 = gb.cpu.register.H & 0b00000001
    gb.cpu.register.set_h(((bit_7 << 7) + (gb.cpu.register.H >> 1)) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.H == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_2d(gb):
    """ SRA L - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_7 = gb.cpu.register.L >> 7
    bit_0 = gb.cpu.register.L & 0b00000001
    gb.cpu.register.set_l(((bit_7 << 7) + (gb.cpu.register.L >> 1)) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.L == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_2e(gb):
    """ SRA (HL) - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    bit_7 = value >> 7
    bit_0 = value & 0b00000001
    value = ((bit_7 << 7) + (value >> 1)) & 0xFF
    gb.cpu.register.set_z_flag(value == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_2f(gb):
    """ SRA A - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_7 = gb.cpu.register.A >> 7
    bit_0 = gb.cpu.register.A & 0b00000001
    gb.cpu.register.set_a(((bit_7 << 7) + (gb.cpu.register.A >> 1)) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 8


# OPCODES CB 3x
def code_cb_30(gb):
    """ SWAP B - Swap upper and lower nibbles (nibble = 4 bits) """
    lower_nibble = gb.cpu.register.B & 0x0F
    upper_nibble = (gb.cpu.register.B >> 4) & 0x0F
    gb.cpu.register.set_b((lower_nibble << 4) | upper_nibble)
    gb.cpu.register.set_z_flag(gb.cpu.register.B == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    return 8


def code_cb_31(gb):
    """ SWAP C - Swap upper and lower nibbles (nibble = 4 bits) """
    lower_nibble = gb.cpu.register.C & 0x0F
    upper_nibble = (gb.cpu.register.C >> 4) & 0x0F
    gb.cpu.register.set_c((lower_nibble << 4) | upper_nibble)
    gb.cpu.register.set_z_flag(gb.cpu.register.C == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    return 8


def code_cb_32(gb):
    """ SWAP D - Swap upper and lower nibbles (nibble = 4 bits) """
    lower_nibble = gb.cpu.register.D & 0x0F
    upper_nibble = (gb.cpu.register.D >> 4) & 0x0F
    gb.cpu.register.set_d((lower_nibble << 4) | upper_nibble)
    gb.cpu.register.set_z_flag(gb.cpu.register.D == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    return 8


def code_cb_33(gb):
    """ SWAP E - Swap upper and lower nibbles (nibble = 4 bits) """
    lower_nibble = gb.cpu.register.E & 0x0F
    upper_nibble = (gb.cpu.register.E >> 4) & 0x0F
    gb.cpu.register.set_e((lower_nibble << 4) | upper_nibble)
    gb.cpu.register.set_z_flag(gb.cpu.register.E == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    return 8


def code_cb_34(gb):
    """ SWAP H - Swap upper and lower nibbles (nibble = 4 bits) """
    lower_nibble = gb.cpu.register.H & 0x0F
    upper_nibble = (gb.cpu.register.H >> 4) & 0x0F
    gb.cpu.register.set_h((lower_nibble << 4) | upper_nibble)
    gb.cpu.register.set_z_flag(gb.cpu.register.H == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    return 8


def code_cb_35(gb):
    """ SWAP L - Swap upper and lower nibbles (nibble = 4 bits) """
    lower_nibble = gb.cpu.register.L & 0x0F
    upper_nibble = (gb.cpu.register.L >> 4) & 0x0F
    gb.cpu.register.set_l((lower_nibble << 4) | upper_nibble)
    gb.cpu.register.set_z_flag(gb.cpu.register.L == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    return 8


def code_cb_36(gb):
    """ SWAP (HL) - Swap upper and lower nibbles (nibble = 4 bits) """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    lower_nibble = value & 0x0F
    upper_nibble = (value >> 4) & 0x0F
    value = (lower_nibble << 4) | upper_nibble
    gb.cpu.register.set_z_flag(value == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_37(gb):
    """ SWAP A - Swap upper and lower nibbles (nibble = 4 bits) """
    lower_nibble = gb.cpu.register.A & 0x0F
    upper_nibble = (gb.cpu.register.A >> 4) & 0x0F
    gb.cpu.register.set_a((lower_nibble << 4) | upper_nibble)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(False)
    return 8


def code_cb_38(gb):
    """ SRL B - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_0 = gb.cpu.register.B & 0b00000001
    gb.cpu.register.set_b((gb.cpu.register.B >> 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.B == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_39(gb):
    """ SRL C - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_0 = gb.cpu.register.C & 0b00000001
    gb.cpu.register.set_c((gb.cpu.register.C >> 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.C == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_3a(gb):
    """ SRL D - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_0 = gb.cpu.register.D & 0b00000001
    gb.cpu.register.set_d((gb.cpu.register.D >> 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.D == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_3b(gb):
    """ SRL E - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_0 = gb.cpu.register.E & 0b00000001
    gb.cpu.register.set_e((gb.cpu.register.E >> 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.E == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_3c(gb):
    """ SRL H - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_0 = gb.cpu.register.H & 0b00000001
    gb.cpu.register.set_h((gb.cpu.register.H >> 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.H == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_3d(gb):
    """ SRL L - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_0 = gb.cpu.register.L & 0b00000001
    gb.cpu.register.set_l((gb.cpu.register.L >> 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.L == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 8


def code_cb_3e(gb):
    """ SRL (HL) - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    bit_0 = value & 0b00000001
    value = (value >> 1) & 0xFF
    gb.cpu.register.set_z_flag(value == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_3f(gb):
    """ SRL A - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    bit_0 = gb.cpu.register.A & 0b00000001
    gb.cpu.register.set_a((gb.cpu.register.A >> 1) & 0xFF)
    gb.cpu.register.set_z_flag(gb.cpu.register.A == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(False)
    gb.cpu.register.set_c_flag(bit_0)
    return 8


# OPCODES CB 4x
def code_cb_40(gb):
    """ BIT 0,B - Test what is the value of bit 0 """
    bit_to_check = gb.cpu.register.B & 0b00000001
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_41(gb):
    """ BIT 0,C - Test what is the value of bit 0 """
    bit_to_check = gb.cpu.register.C & 0b00000001
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_42(gb):
    """ BIT 0,D - Test what is the value of bit 0 """
    bit_to_check = gb.cpu.register.D & 0b00000001
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_43(gb):
    """ BIT 0,E - Test what is the value of bit 0 """
    bit_to_check = gb.cpu.register.E & 0b00000001
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_44(gb):
    """ BIT 0,H - Test what is the value of bit 0 """
    bit_to_check = gb.cpu.register.H & 0b00000001
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_45(gb):
    """ BIT 0,L - Test what is the value of bit 0 """
    bit_to_check = gb.cpu.register.L & 0b00000001
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_46(gb):
    """ BIT 0,(HL) - Test what is the value of bit 0 """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    bit_to_check = value & 0b00000001
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_47(gb):
    """ BIT 0,A - Test what is the value of bit 0 """
    bit_to_check = gb.cpu.register.A & 0b00000001
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_48(gb):
    """ BIT 1,B - Test what is the value of bit 1 """
    bit_to_check = (gb.cpu.register.B & 0b00000010) >> 1
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_49(gb):
    """ BIT 1,C - Test what is the value of bit 1 """
    bit_to_check = (gb.cpu.register.C & 0b00000010) >> 1
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_4a(gb):
    """ BIT 1,D - Test what is the value of bit 1 """
    bit_to_check = (gb.cpu.register.D & 0b00000010) >> 1
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_4b(gb):
    """ BIT 1,E - Test what is the value of bit 1 """
    bit_to_check = (gb.cpu.register.E & 0b00000010) >> 1
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_4c(gb):
    """ BIT 1,H - Test what is the value of bit 1 """
    bit_to_check = (gb.cpu.register.H & 0b00000010) >> 1
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_4d(gb):
    """ BIT 1,L - Test what is the value of bit 1 """
    bit_to_check = (gb.cpu.register.L & 0b00000010) >> 1
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_4e(gb):
    """ BIT 1,(HL) - Test what is the value of bit 1 """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    bit_to_check = (value & 0b00000010) >> 1
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_4f(gb):
    """ BIT 1,A - Test what is the value of bit 1 """
    bit_to_check = (gb.cpu.register.A & 0b00000010) >> 1
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


# OPCODES CB 5x
def code_cb_50(gb):
    """ BIT 2,B - Test what is the value of bit 2 """
    bit_to_check = (gb.cpu.register.B & 0b00000100) >> 2
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_51(gb):
    """ BIT 2,C - Test what is the value of bit 2 """
    bit_to_check = (gb.cpu.register.C & 0b00000100) >> 2
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_52(gb):
    """ BIT 2,D - Test what is the value of bit 2 """
    bit_to_check = (gb.cpu.register.D & 0b00000100) >> 2
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_53(gb):
    """ BIT 2,E - Test what is the value of bit 2 """
    bit_to_check = (gb.cpu.register.E & 0b00000100) >> 2
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_54(gb):
    """ BIT 2,H - Test what is the value of bit 2 """
    bit_to_check = (gb.cpu.register.H & 0b00000100) >> 2
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_55(gb):
    """ BIT 2,L - Test what is the value of bit 2 """
    bit_to_check = (gb.cpu.register.L & 0b00000100) >> 2
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_56(gb):
    """ BIT 2,(HL) - Test what is the value of bit 2 """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    bit_to_check = (value & 0b00000100) >> 2
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_57(gb):
    """ BIT 2,A - Test what is the value of bit 2 """
    bit_to_check = (gb.cpu.register.A & 0b00000100) >> 2
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_58(gb):
    """ BIT 3,B - Test what is the value of bit 3 """
    bit_to_check = (gb.cpu.register.B & 0b00001000) >> 3
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_59(gb):
    """ BIT 3,C - Test what is the value of bit 3 """
    bit_to_check = (gb.cpu.register.C & 0b00001000) >> 3
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_5a(gb):
    """ BIT 3,D - Test what is the value of bit 3 """
    bit_to_check = (gb.cpu.register.D & 0b00001000) >> 3
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_5b(gb):
    """ BIT 3,E - Test what is the value of bit 3 """
    bit_to_check = (gb.cpu.register.E & 0b00001000) >> 3
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_5c(gb):
    """ BIT 3,H - Test what is the value of bit 3 """
    bit_to_check = (gb.cpu.register.H & 0b00001000) >> 3
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_5d(gb):
    """ BIT 3,L - Test what is the value of bit 3 """
    bit_to_check = (gb.cpu.register.L & 0b00001000) >> 3
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_5e(gb):
    """ BIT 3,(HL) - Test what is the value of bit 3 """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    bit_to_check = (value & 0b00001000) >> 3
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_5f(gb):
    """ BIT 3,A - Test what is the value of bit 3 """
    bit_to_check = (gb.cpu.register.A & 0b00001000) >> 3
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


# OPCODES CB 6x
def code_cb_60(gb):
    """ BIT 4,B - Test what is the value of bit 4 """
    bit_to_check = (gb.cpu.register.B & 0b00010000) >> 4
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_61(gb):
    """ BIT 4,C - Test what is the value of bit 4 """
    bit_to_check = (gb.cpu.register.C & 0b00010000) >> 4
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_62(gb):
    """ BIT 4,D - Test what is the value of bit 4 """
    bit_to_check = (gb.cpu.register.D & 0b00010000) >> 4
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_63(gb):
    """ BIT 4,E - Test what is the value of bit 4 """
    bit_to_check = (gb.cpu.register.E & 0b00010000) >> 4
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_64(gb):
    """ BIT 4,H - Test what is the value of bit 4 """
    bit_to_check = (gb.cpu.register.H & 0b00010000) >> 4
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_65(gb):
    """ BIT 4,L - Test what is the value of bit 4 """
    bit_to_check = (gb.cpu.register.L & 0b00010000) >> 4
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_66(gb):
    """ BIT 4,(HL) - Test what is the value of bit 4 """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    bit_to_check = (value & 0b00010000) >> 4
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_67(gb):
    """ BIT 4,A - Test what is the value of bit 4 """
    bit_to_check = (gb.cpu.register.A & 0b00010000) >> 4
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_68(gb):
    """ BIT 5,B - Test what is the value of bit 5 """
    bit_to_check = (gb.cpu.register.B & 0b00100000) >> 5
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_69(gb):
    """ BIT 5,C - Test what is the value of bit 5 """
    bit_to_check = (gb.cpu.register.C & 0b00100000) >> 5
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_6a(gb):
    """ BIT 5,D - Test what is the value of bit 5 """
    bit_to_check = (gb.cpu.register.D & 0b00100000) >> 5
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_6b(gb):
    """ BIT 5,E - Test what is the value of bit 5 """
    bit_to_check = (gb.cpu.register.E & 0b00100000) >> 5
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_6c(gb):
    """ BIT 5,H - Test what is the value of bit 5 """
    bit_to_check = (gb.cpu.register.H & 0b00100000) >> 5
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_6d(gb):
    """ BIT 5,L - Test what is the value of bit 5 """
    bit_to_check = (gb.cpu.register.L & 0b00100000) >> 5
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_6e(gb):
    """ BIT 5,(HL) - Test what is the value of bit 5 """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    bit_to_check = (value & 0b00100000) >> 5
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_6f(gb):
    """ BIT 5,A - Test what is the value of bit 5 """
    bit_to_check = (gb.cpu.register.A & 0b00100000) >> 5
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


# OPCODES CB 7x
def code_cb_70(gb):
    """ BIT 6,B - Test what is the value of bit 6 """
    bit_to_check = (gb.cpu.register.B & 0b01000000) >> 6
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_71(gb):
    """ BIT 6,C - Test what is the value of bit 6 """
    bit_to_check = (gb.cpu.register.C & 0b01000000) >> 6
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_72(gb):
    """ BIT 6,D - Test what is the value of bit 6 """
    bit_to_check = (gb.cpu.register.D & 0b01000000) >> 6
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_73(gb):
    """ BIT 6,E - Test what is the value of bit 6 """
    bit_to_check = (gb.cpu.register.E & 0b01000000) >> 6
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_74(gb):
    """ BIT 6,H - Test what is the value of bit 6 """
    bit_to_check = (gb.cpu.register.H & 0b01000000) >> 6
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_75(gb):
    """ BIT 6,L - Test what is the value of bit 6 """
    bit_to_check = (gb.cpu.register.L & 0b01000000) >> 6
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_76(gb):
    """ BIT 6,(HL) - Test what is the value of bit 6 """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    bit_to_check = (value & 0b01000000) >> 6
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_77(gb):
    """ BIT 6,A - Test what is the value of bit 6 """
    bit_to_check = (gb.cpu.register.A & 0b01000000) >> 6
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_78(gb):
    """ BIT 7,B - Test what is the value of bit 7 """
    bit_to_check = (gb.cpu.register.B & 0b10000000) >> 7
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_79(gb):
    """ BIT 7,C - Test what is the value of bit 7 """
    bit_to_check = (gb.cpu.register.C & 0b10000000) >> 7
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_7a(gb):
    """ BIT 7,D - Test what is the value of bit 7 """
    bit_to_check = (gb.cpu.register.D & 0b10000000) >> 7
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_7b(gb):
    """ BIT 7,E - Test what is the value of bit 7 """
    bit_to_check = (gb.cpu.register.E & 0b10000000) >> 7
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_7c(gb):
    """ BIT 7,H - Test what is the value of bit 7 """
    bit_to_check = (gb.cpu.register.H & 0b10000000) >> 7
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_7d(gb):
    """ BIT 7,L - Test what is the value of bit 7 """
    bit_to_check = (gb.cpu.register.L & 0b10000000) >> 7
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


def code_cb_7e(gb):
    """ BIT 7,(HL) - Test what is the value of bit 7 """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    bit_to_check = (value & 0b10000000) >> 7
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_7f(gb):
    """ BIT 7,A - Test what is the value of bit 7 """
    bit_to_check = (gb.cpu.register.A & 0b10000000) >> 7
    gb.cpu.register.set_z_flag(bit_to_check == 0)
    gb.cpu.register.set_n_flag(False)
    gb.cpu.register.set_h_flag(True)
    return 8


# OPCODES CB 8x
def code_cb_80(gb):
    """ RES 0,B - Reset the specified bit """
    gb.cpu.register.set_b(gb.cpu.register.B & 0b11111110)
    return 8


def code_cb_81(gb):
    """ RES 0,C - Reset the specified bit """
    gb.cpu.register.set_c(gb.cpu.register.C & 0b11111110)
    return 8


def code_cb_82(gb):
    """ RES 0,D - Reset the specified bit """
    gb.cpu.register.set_d(gb.cpu.register.D & 0b11111110)
    return 8


def code_cb_83(gb):
    """ RES 0,E - Reset the specified bit """
    gb.cpu.register.set_e(gb.cpu.register.E & 0b11111110)
    return 8


def code_cb_84(gb):
    """ RES 0,H - Reset the specified bit """
    gb.cpu.register.set_h(gb.cpu.register.H & 0b11111110)
    return 8


def code_cb_85(gb):
    """ RES 0,L - Reset the specified bit """
    gb.cpu.register.set_l(gb.cpu.register.L & 0b11111110)
    return 8


def code_cb_86(gb):
    """ RES 0,(HL) - Reset the specified bit """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    value = value & 0b11111110
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_87(gb):
    """ RES 0,A - Reset the specified bit """
    gb.cpu.register.set_a(gb.cpu.register.A & 0b11111110)
    return 8


def code_cb_88(gb):
    """ RES 1,B - Reset the specified bit """
    gb.cpu.register.set_b(gb.cpu.register.B & 0b11111101)
    return 8


def code_cb_89(gb):
    """ RES 1,C - Reset the specified bit """
    gb.cpu.register.set_c(gb.cpu.register.C & 0b11111101)
    return 8


def code_cb_8a(gb):
    """ RES 1,D - Reset the specified bit """
    gb.cpu.register.set_d(gb.cpu.register.D & 0b11111101)
    return 8


def code_cb_8b(gb):
    """ RES 1,E - Reset the specified bit """
    gb.cpu.register.set_e(gb.cpu.register.E & 0b11111101)
    return 8


def code_cb_8c(gb):
    """ RES 1,H - Reset the specified bit """
    gb.cpu.register.set_h(gb.cpu.register.H & 0b11111101)
    return 8


def code_cb_8d(gb):
    """ RES 1,L - Reset the specified bit """
    gb.cpu.register.set_l(gb.cpu.register.L & 0b11111101)
    return 8


def code_cb_8e(gb):
    """ RES 1,(HL) - Reset the specified bit """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    value = value & 0b11111101
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_8f(gb):
    """ RES 1,A - Reset the specified bit """
    gb.cpu.register.set_a(gb.cpu.register.A & 0b11111101)
    return 8


# OPCODES CB 9x
def code_cb_90(gb):
    """ RES 2,B - Reset the specified bit """
    gb.cpu.register.set_b(gb.cpu.register.B & 0b11111011)
    return 8


def code_cb_91(gb):
    """ RES 2,C - Reset the specified bit """
    gb.cpu.register.set_c(gb.cpu.register.C & 0b11111011)
    return 8


def code_cb_92(gb):
    """ RES 2,D - Reset the specified bit """
    gb.cpu.register.set_d(gb.cpu.register.D & 0b11111011)
    return 8


def code_cb_93(gb):
    """ RES 2,E - Reset the specified bit """
    gb.cpu.register.set_e(gb.cpu.register.E & 0b11111011)
    return 8


def code_cb_94(gb):
    """ RES 2,H - Reset the specified bit """
    gb.cpu.register.set_h(gb.cpu.register.H & 0b11111011)
    return 8


def code_cb_95(gb):
    """ RES 2,L - Reset the specified bit """
    gb.cpu.register.set_l(gb.cpu.register.L & 0b11111011)
    return 8


def code_cb_96(gb):
    """ RES 2,(HL) - Reset the specified bit """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    value = value & 0b11111011
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_97(gb):
    """ RES 2,A - Reset the specified bit """
    gb.cpu.register.set_a(gb.cpu.register.A & 0b11111011)
    return 8


def code_cb_98(gb):
    """ RES 3,B - Reset the specified bit """
    gb.cpu.register.set_b(gb.cpu.register.B & 0b11110111)
    return 8


def code_cb_99(gb):
    """ RES 3,C - Reset the specified bit """
    gb.cpu.register.set_c(gb.cpu.register.C & 0b11110111)
    return 8


def code_cb_9a(gb):
    """ RES 3,D - Reset the specified bit """
    gb.cpu.register.set_d(gb.cpu.register.D & 0b11110111)
    return 8


def code_cb_9b(gb):
    """ RES 3,E - Reset the specified bit """
    gb.cpu.register.set_e(gb.cpu.register.E & 0b11110111)
    return 8


def code_cb_9c(gb):
    """ RES 3,H - Reset the specified bit """
    gb.cpu.register.set_h(gb.cpu.register.H & 0b11110111)
    return 8


def code_cb_9d(gb):
    """ RES 3,L - Reset the specified bit """
    gb.cpu.register.set_l(gb.cpu.register.L & 0b11110111)
    return 8


def code_cb_9e(gb):
    """ RES 3,(HL) - Reset the specified bit """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    value = value & 0b11110111
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_9f(gb):
    """ RES 3,A - Reset the specified bit """
    gb.cpu.register.set_a(gb.cpu.register.A & 0b11110111)
    return 8


# OPCODES CB Ax
def code_cb_a0(gb):
    """ RES 4,B - Reset the specified bit """
    gb.cpu.register.set_b(gb.cpu.register.B & 0b11101111)
    return 8


def code_cb_a1(gb):
    """ RES 4,C - Reset the specified bit """
    gb.cpu.register.set_c(gb.cpu.register.C & 0b11101111)
    return 8


def code_cb_a2(gb):
    """ RES 4,D - Reset the specified bit """
    gb.cpu.register.set_d(gb.cpu.register.D & 0b11101111)
    return 8


def code_cb_a3(gb):
    """ RES 4,E - Reset the specified bit """
    gb.cpu.register.set_e(gb.cpu.register.E & 0b11101111)
    return 8


def code_cb_a4(gb):
    """ RES 4,H - Reset the specified bit """
    gb.cpu.register.set_h(gb.cpu.register.H & 0b11101111)
    return 8


def code_cb_a5(gb):
    """ RES 4,L - Reset the specified bit """
    gb.cpu.register.set_l(gb.cpu.register.L & 0b11101111)
    return 8


def code_cb_a6(gb):
    """ RES 4,(HL) - Reset the specified bit """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    value = value & 0b11101111
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_a7(gb):
    """ RES 4,A - Reset the specified bit """
    gb.cpu.register.set_a(gb.cpu.register.A & 0b11101111)
    return 8


def code_cb_a8(gb):
    """ RES 5,B - Reset the specified bit """
    gb.cpu.register.set_b(gb.cpu.register.B & 0b11011111)
    return 8


def code_cb_a9(gb):
    """ RES 5,C - Reset the specified bit """
    gb.cpu.register.set_c(gb.cpu.register.C & 0b11011111)
    return 8


def code_cb_aa(gb):
    """ RES 5,D - Reset the specified bit """
    gb.cpu.register.set_d(gb.cpu.register.D & 0b11011111)
    return 8


def code_cb_ab(gb):
    """ RES 5,E - Reset the specified bit """
    gb.cpu.register.set_e(gb.cpu.register.E & 0b11011111)
    return 8


def code_cb_ac(gb):
    """ RES 5,H - Reset the specified bit """
    gb.cpu.register.set_h(gb.cpu.register.H & 0b11011111)
    return 8


def code_cb_ad(gb):
    """ RES 5,L - Reset the specified bit """
    gb.cpu.register.set_l(gb.cpu.register.L & 0b11011111)
    return 8


def code_cb_ae(gb):
    """ RES 5,(HL) - Reset the specified bit """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    value = value & 0b11011111
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_af(gb):
    """ RES 5,A - Reset the specified bit """
    gb.cpu.register.set_a(gb.cpu.register.A & 0b11011111)
    return 8


# OPCODES CB Bx
def code_cb_b0(gb):
    """ RES 6,B - Reset the specified bit """
    gb.cpu.register.set_b(gb.cpu.register.B & 0b10111111)
    return 8


def code_cb_b1(gb):
    """ RES 6,C - Reset the specified bit """
    gb.cpu.register.set_c(gb.cpu.register.C & 0b10111111)
    return 8


def code_cb_b2(gb):
    """ RES 6,D - Reset the specified bit """
    gb.cpu.register.set_d(gb.cpu.register.D & 0b10111111)
    return 8


def code_cb_b3(gb):
    """ RES 6,E - Reset the specified bit """
    gb.cpu.register.set_e(gb.cpu.register.E & 0b10111111)
    return 8


def code_cb_b4(gb):
    """ RES 6,H - Reset the specified bit """
    gb.cpu.register.set_h(gb.cpu.register.H & 0b10111111)
    return 8


def code_cb_b5(gb):
    """ RES 6,L - Reset the specified bit """
    gb.cpu.register.set_l(gb.cpu.register.L & 0b10111111)
    return 8


def code_cb_b6(gb):
    """ RES 6,(HL) - Reset the specified bit """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    value = value & 0b10111111
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_b7(gb):
    """ RES 6,A - Reset the specified bit """
    gb.cpu.register.set_a(gb.cpu.register.A & 0b10111111)
    return 8


def code_cb_b8(gb):
    """ RES 7,B - Reset the specified bit """
    gb.cpu.register.set_b(gb.cpu.register.B & 0b01111111)
    return 8


def code_cb_b9(gb):
    """ RES 7,C - Reset the specified bit """
    gb.cpu.register.set_c(gb.cpu.register.C & 0b01111111)
    return 8


def code_cb_ba(gb):
    """ RES 7,D - Reset the specified bit """
    gb.cpu.register.set_d(gb.cpu.register.D & 0b01111111)
    return 8


def code_cb_bb(gb):
    """ RES 7,E - Reset the specified bit """
    gb.cpu.register.set_e(gb.cpu.register.E & 0b01111111)
    return 8


def code_cb_bc(gb):
    """ RES 7,H - Reset the specified bit """
    gb.cpu.register.set_h(gb.cpu.register.H & 0b01111111)
    return 8


def code_cb_bd(gb):
    """ RES 7,L - Reset the specified bit """
    gb.cpu.register.set_l(gb.cpu.register.L & 0b01111111)
    return 8


def code_cb_be(gb):
    """ RES 7,(HL) - Reset the specified bit """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    value = value & 0b01111111
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_bf(gb):
    """ RES 7,A - Reset the specified bit """
    gb.cpu.register.set_a(gb.cpu.register.A & 0b01111111)
    return 8


# OPCODES CB Cx
def code_cb_c0(gb):
    """ SET 0,B - Set the specified bit """
    gb.cpu.register.set_b(gb.cpu.register.B | 0b00000001)
    return 8


def code_cb_c1(gb):
    """ SET 0,C - Set the specified bit """
    gb.cpu.register.set_c(gb.cpu.register.C | 0b00000001)
    return 8


def code_cb_c2(gb):
    """ SET 0,D - Set the specified bit """
    gb.cpu.register.set_d(gb.cpu.register.D | 0b00000001)
    return 8


def code_cb_c3(gb):
    """ SET 0,E - Set the specified bit """
    gb.cpu.register.set_e(gb.cpu.register.E | 0b00000001)
    return 8


def code_cb_c4(gb):
    """ SET 0,H - Set the specified bit """
    gb.cpu.register.set_h(gb.cpu.register.H | 0b00000001)
    return 8


def code_cb_c5(gb):
    """ SET 0,L - Set the specified bit """
    gb.cpu.register.set_l(gb.cpu.register.L | 0b00000001)
    return 8


def code_cb_c6(gb):
    """ SET 0,(HL) - Set the specified bit """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    value = value | 0b00000001
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_c7(gb):
    """ SET 0,A - Set the specified bit """
    gb.cpu.register.set_a(gb.cpu.register.A | 0b00000001)
    return 8


def code_cb_c8(gb):
    """ SET 1,B - Set the specified bit """
    gb.cpu.register.set_b(gb.cpu.register.B | 0b00000010)
    return 8


def code_cb_c9(gb):
    """ SET 1,C - Set the specified bit """
    gb.cpu.register.set_c(gb.cpu.register.C | 0b00000010)
    return 8


def code_cb_ca(gb):
    """ SET 1,D - Set the specified bit """
    gb.cpu.register.set_d(gb.cpu.register.D | 0b00000010)
    return 8


def code_cb_cb(gb):
    """ SET 1,E - Set the specified bit """
    gb.cpu.register.set_e(gb.cpu.register.E | 0b00000010)
    return 8


def code_cb_cc(gb):
    """ SET 1,H - Set the specified bit """
    gb.cpu.register.set_h(gb.cpu.register.H | 0b00000010)
    return 8


def code_cb_cd(gb):
    """ SET 1,L - Set the specified bit """
    gb.cpu.register.set_l(gb.cpu.register.L | 0b00000010)
    return 8


def code_cb_ce(gb):
    """ SET 1,(HL) - Set the specified bit """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    value = value | 0b00000010
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_cf(gb):
    """ SET 1,A - Set the specified bit """
    gb.cpu.register.set_a(gb.cpu.register.A | 0b00000010)
    return 8


# OPCODES CB Dx
def code_cb_d0(gb):
    """ SET 2,B - Set the specified bit """
    gb.cpu.register.set_b(gb.cpu.register.B | 0b00000100)
    return 8


def code_cb_d1(gb):
    """ SET 2,C - Set the specified bit """
    gb.cpu.register.set_c(gb.cpu.register.C | 0b00000100)
    return 8


def code_cb_d2(gb):
    """ SET 2,D - Set the specified bit """
    gb.cpu.register.set_d(gb.cpu.register.D | 0b00000100)
    return 8


def code_cb_d3(gb):
    """ SET 2,E - Set the specified bit """
    gb.cpu.register.set_e(gb.cpu.register.E | 0b00000100)
    return 8


def code_cb_d4(gb):
    """ SET 2,H - Set the specified bit """
    gb.cpu.register.set_h(gb.cpu.register.H | 0b00000100)
    return 8


def code_cb_d5(gb):
    """ SET 2,L - Set the specified bit """
    gb.cpu.register.set_l(gb.cpu.register.L | 0b00000100)
    return 8


def code_cb_d6(gb):
    """ SET 2,(HL) - Set the specified bit """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    value = value | 0b00000100
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_d7(gb):
    """ SET 2,A - Set the specified bit """
    gb.cpu.register.set_a(gb.cpu.register.A | 0b00000100)
    return 8


def code_cb_d8(gb):
    """ SET 3,B - Set the specified bit """
    gb.cpu.register.set_b(gb.cpu.register.B | 0b00001000)
    return 8


def code_cb_d9(gb):
    """ SET 3,C - Set the specified bit """
    gb.cpu.register.set_c(gb.cpu.register.C | 0b00001000)
    return 8


def code_cb_da(gb):
    """ SET 3,D - Set the specified bit """
    gb.cpu.register.set_d(gb.cpu.register.D | 0b00001000)
    return 8


def code_cb_db(gb):
    """ SET 3,E - Set the specified bit """
    gb.cpu.register.set_e(gb.cpu.register.E | 0b00001000)
    return 8


def code_cb_dc(gb):
    """ SET 3,H - Set the specified bit """
    gb.cpu.register.set_h(gb.cpu.register.H | 0b00001000)
    return 8


def code_cb_dd(gb):
    """ SET 3,L - Set the specified bit """
    gb.cpu.register.set_l(gb.cpu.register.L | 0b00001000)
    return 8


def code_cb_de(gb):
    """ SET 3,(HL) - Set the specified bit """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    value = value | 0b00001000
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_df(gb):
    """ SET 3,A - Set the specified bit """
    gb.cpu.register.set_a(gb.cpu.register.A | 0b00001000)
    return 8


# OPCODES CB Ex
def code_cb_e0(gb):
    """ SET 4,B - Set the specified bit """
    gb.cpu.register.set_b(gb.cpu.register.B | 0b00010000)
    return 8


def code_cb_e1(gb):
    """ SET 4,C - Set the specified bit """
    gb.cpu.register.set_c(gb.cpu.register.C | 0b00010000)
    return 8


def code_cb_e2(gb):
    """ SET 4,D - Set the specified bit """
    gb.cpu.register.set_d(gb.cpu.register.D | 0b00010000)
    return 8


def code_cb_e3(gb):
    """ SET 4,E - Set the specified bit """
    gb.cpu.register.set_e(gb.cpu.register.E | 0b00010000)
    return 8


def code_cb_e4(gb):
    """ SET 4,H - Set the specified bit """
    gb.cpu.register.set_h(gb.cpu.register.H | 0b00010000)
    return 8


def code_cb_e5(gb):
    """ SET 4,L - Set the specified bit """
    gb.cpu.register.set_l(gb.cpu.register.L | 0b00010000)
    return 8


def code_cb_e6(gb):
    """ SET 4,(HL) - Set the specified bit """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    value = value | 0b00010000
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_e7(gb):
    """ SET 4,A - Set the specified bit """
    gb.cpu.register.set_a(gb.cpu.register.A | 0b00010000)
    return 8


def code_cb_e8(gb):
    """ SET 5,B - Set the specified bit """
    gb.cpu.register.set_b(gb.cpu.register.B | 0b00100000)
    return 8


def code_cb_e9(gb):
    """ SET 5,C - Set the specified bit """
    gb.cpu.register.set_c(gb.cpu.register.C | 0b00100000)
    return 8


def code_cb_ea(gb):
    """ SET 5,D - Set the specified bit """
    gb.cpu.register.set_d(gb.cpu.register.D | 0b00100000)
    return 8


def code_cb_eb(gb):
    """ SET 5,E - Set the specified bit """
    gb.cpu.register.set_e(gb.cpu.register.E | 0b00100000)
    return 8


def code_cb_ec(gb):
    """ SET 5,H - Set the specified bit """
    gb.cpu.register.set_h(gb.cpu.register.H | 0b00100000)
    return 8


def code_cb_ed(gb):
    """ SET 5,L - Set the specified bit """
    gb.cpu.register.set_l(gb.cpu.register.L | 0b00100000)
    return 8


def code_cb_ee(gb):
    """ SET 5,(HL) - Set the specified bit """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    value = value | 0b00100000
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_ef(gb):
    """ SET 5,A - Set the specified bit """
    gb.cpu.register.set_a(gb.cpu.register.A | 0b00100000)
    return 8


# OPCODES CB Fx
def code_cb_f0(gb):
    """ SET 6,B - Set the specified bit """
    gb.cpu.register.set_b(gb.cpu.register.B | 0b01000000)
    return 8


def code_cb_f1(gb):
    """ SET 6,C - Set the specified bit """
    gb.cpu.register.set_c(gb.cpu.register.C | 0b01000000)
    return 8


def code_cb_f2(gb):
    """ SET 6,D - Set the specified bit """
    gb.cpu.register.set_d(gb.cpu.register.D | 0b01000000)
    return 8


def code_cb_f3(gb):
    """ SET 6,E - Set the specified bit """
    gb.cpu.register.set_e(gb.cpu.register.E | 0b01000000)
    return 8


def code_cb_f4(gb):
    """ SET 6,H - Set the specified bit """
    gb.cpu.register.set_h(gb.cpu.register.H | 0b01000000)
    return 8


def code_cb_f5(gb):
    """ SET 6,L - Set the specified bit """
    gb.cpu.register.set_l(gb.cpu.register.L | 0b01000000)
    return 8


def code_cb_f6(gb):
    """ SET 6,(HL) - Set the specified bit """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    value = value | 0b01000000
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_f7(gb):
    """ SET 6,A - Set the specified bit """
    gb.cpu.register.set_a(gb.cpu.register.A | 0b01000000)
    return 8


def code_cb_f8(gb):
    """ SET 7,B - Set the specified bit """
    gb.cpu.register.set_b(gb.cpu.register.B | 0b10000000)
    return 8


def code_cb_f9(gb):
    """ SET 7,C - Set the specified bit """
    gb.cpu.register.set_c(gb.cpu.register.C | 0b10000000)
    return 8


def code_cb_fa(gb):
    """ SET 7,D - Set the specified bit """
    gb.cpu.register.set_d(gb.cpu.register.D | 0b10000000)
    return 8


def code_cb_fb(gb):
    """ SET 7,E - Set the specified bit """
    gb.cpu.register.set_e(gb.cpu.register.E | 0b10000000)
    return 8


def code_cb_fc(gb):
    """ SET 7,H - Set the specified bit """
    gb.cpu.register.set_h(gb.cpu.register.H | 0b10000000)
    return 8


def code_cb_fd(gb):
    """ SET 7,L - Set the specified bit """
    gb.cpu.register.set_l(gb.cpu.register.L | 0b10000000)
    return 8


def code_cb_fe(gb):
    """ SET 7,(HL) - Set the specified bit """
    value = gb.memory.read_8bit(gb.cpu.register.get_hl())
    value = value | 0b10000000
    gb.memory.write_8bit(gb.cpu.register.get_hl(), value)
    return 16


def code_cb_ff(gb):
    """ SET 7,A - Set the specified bit """
    gb.cpu.register.set_a(gb.cpu.register.A | 0b10000000)
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
