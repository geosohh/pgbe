"""
Tests for cpu/op.py
"""

import pytest
import op

"""
Fixtures act as test setup/teardown in py.test.
For each test method with a parameter, the parameter name is the setup method that will be called.
"""


@pytest.fixture
def gb():
    """
    Create Register instance for testing.
    :return: new register instance
    """
    from memory import Memory
    from gb import GB
    gb = GB()
    gb.memory = Memory(gb)  # To remove all memory initialization made by other components
    return gb


"""
Tests
"""


def assert_registers(gb, A=0x00, F=0x00, B=0x00, C=0x00, D=0x00, E=0x00, H=0x00, L=0x00, SP=0xFFFE, PC=0x0100):
    """
    Helper function to assert registers values.
    For each register, checks if value is the same as the parameter. If no parameter received, checks default value.
    """
    assert gb.cpu.register.A == A
    assert gb.cpu.register.F == F
    assert gb.cpu.register.B == B
    assert gb.cpu.register.C == C
    assert gb.cpu.register.D == D
    assert gb.cpu.register.E == E
    assert gb.cpu.register.H == H
    assert gb.cpu.register.L == L
    assert gb.cpu.register.SP == SP
    assert gb.cpu.register.PC == PC


# noinspection PyProtectedMember
def assert_memory(gb, custom_address=None):
    """
    Helper function to assert memory values.
    If an address is not in the custom_address dictionary, will check for default value.
    :param gb:              CPU instance to access memory
    :param custom_address:  dict with format address:value
    """
    for address in range(0,len(gb.memory._memory_map)):
        if custom_address is not None and address in custom_address:
            if gb.memory._memory_map[address] != custom_address[address]:
                print("Memory address", hex(address), "contains", hex(gb.memory._memory_map[address]),
                      "instead of",hex(custom_address[address]))
            assert gb.memory._memory_map[address] == custom_address[address]
        else:
            if gb.memory._memory_map[address] != 0:
                print("Memory address", hex(address), "contains", hex(gb.memory._memory_map[address]),
                      "instead of",0)
            assert gb.memory._memory_map[address] == 0


# noinspection PyShadowingNames
def test_code_00(gb):
    """ NOP - Does nothing """
    cycles = op.code_00(gb)
    assert cycles == 4
    assert_registers(gb)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_01(gb):
    """ LD BC,d16 - Stores given 16-bit value at BC """
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("FF 55")
    cycles = op.code_01(gb)
    assert cycles == 12
    assert_registers(gb,B=0x55,C=0xFF,PC=0x0002)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_02(gb):
    """ LD (BC),A - Stores reg at the address in BC """
    gb.cpu.register.set_bc(0x4050)
    gb.cpu.register.A = 0x99
    cycles = op.code_02(gb)
    assert cycles == 8
    assert_registers(gb,A=0x99,B=0x40,C=0x50)
    assert_memory(gb,{0x4050:0x99})


# noinspection PyShadowingNames
def test_code_03(gb):
    """ INC BC - BC=BC+1 """
    gb.cpu.register.set_bc(0x0000)
    cycles = op.code_03(gb)
    assert cycles == 8
    assert_registers(gb, B=0x00, C=0x01)

    gb.cpu.register.set_bc(0x00FF)
    cycles = op.code_03(gb)
    assert cycles == 8
    assert_registers(gb, B=0x01, C=0x00)

    gb.cpu.register.set_bc(0x0FFF)
    cycles = op.code_03(gb)
    assert cycles == 8
    assert_registers(gb, B=0x10, C=0x00)

    gb.cpu.register.set_bc(0xFFFF)
    cycles = op.code_03(gb)
    assert cycles == 8
    assert_registers(gb, B=0x00, C=0x00)

    assert_memory(gb)

    
# noinspection PyShadowingNames
def test_code_04(gb):
    """ INC B - B=B+1 """
    gb.cpu.register.B = 0x00
    cycles = op.code_04(gb)
    assert cycles == 4
    assert_registers(gb, B=0x01, F=0b00000000)

    gb.cpu.register.B = 0x0F
    cycles = op.code_04(gb)
    assert cycles == 4
    assert_registers(gb, B=0x10, F=0b00100000)

    gb.cpu.register.B = 0xF0
    cycles = op.code_04(gb)
    assert cycles == 4
    assert_registers(gb, B=0xF1, F=0b00000000)

    gb.cpu.register.B = 0xFF
    cycles = op.code_04(gb)
    assert cycles == 4
    assert_registers(gb, B=0x00, F=0b10100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_05(gb):
    """ DEC B - B=B-1 """
    gb.cpu.register.B = 0x00
    cycles = op.code_05(gb)
    assert cycles == 4
    assert_registers(gb, B=0xFF, F=0b01100000)

    gb.cpu.register.B = 0x0F
    cycles = op.code_05(gb)
    assert cycles == 4
    assert_registers(gb, B=0x0E, F=0b01000000)

    gb.cpu.register.B = 0x01
    cycles = op.code_05(gb)
    assert cycles == 4
    assert_registers(gb, B=0x00, F=0b11000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_06(gb):
    """ LD B,d8 """
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("99")
    cycles = op.code_06(gb)
    assert cycles == 8
    assert_registers(gb,B=0x99,PC=0x0001)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_07(gb):
    """ RLCA - Copy register A bit 7 to Carry flag, then rotate register A left """
    gb.cpu.register.A = 0b11100010
    cycles = op.code_07(gb)
    assert cycles == 4
    assert_registers(gb, A=0b11000101, F=0b00010000)

    gb.cpu.register.A = 0b00000000
    cycles = op.code_07(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000000, F=0b10000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_08(gb):
    """ LD (a16),SP - Set SP value into address (a16) """
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("22 FF")
    gb.cpu.register.SP = 0x8842
    cycles = op.code_08(gb)
    assert cycles == 20
    assert_registers(gb,SP=0x8842,PC=0x0002)
    assert_memory(gb,{0xFF22:0x42, 0xFF23:0x88})


# noinspection PyShadowingNames
def test_code_09(gb):
    """ ADD HL,BC - HL=HL+BC """
    gb.cpu.register.set_hl(0x0000)
    gb.cpu.register.set_bc(0x0001)
    cycles = op.code_09(gb)
    assert cycles == 8
    assert_registers(gb, B=0x00, C=0x01, H=0x00, L=0x01, F=0b00000000)

    gb.cpu.register.set_hl(0x000F)
    gb.cpu.register.set_bc(0x0001)
    cycles = op.code_09(gb)
    assert cycles == 8
    assert_registers(gb, B=0x00, C=0x01, H=0x00, L=0x10, F=0b00000000)

    gb.cpu.register.set_hl(0xF000)
    gb.cpu.register.set_bc(0x1000)
    cycles = op.code_09(gb)
    assert cycles == 8
    assert_registers(gb, B=0x10, C=0x00, H=0x00, L=0x00, F=0b00010000)

    gb.cpu.register.set_hl(0x0FFF)
    gb.cpu.register.set_bc(0x0001)
    cycles = op.code_09(gb)
    assert cycles == 8
    assert_registers(gb, B=0x00, C=0x01, H=0x10, L=0x00, F=0b00100000)

    gb.cpu.register.set_hl(0xFFFF)
    gb.cpu.register.set_bc(0x0001)
    cycles = op.code_09(gb)
    assert cycles == 8
    assert_registers(gb, B=0x00, C=0x01, H=0x00, L=0x00, F=0b00110000)

    gb.cpu.register.set_hl(0xFFFF)
    gb.cpu.register.set_bc(0x0002)
    cycles = op.code_09(gb)
    assert cycles == 8
    assert_registers(gb, B=0x00, C=0x02, H=0x00, L=0x01, F=0b00110000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_0a(gb):
    """ LD A,(BC) - Load reg with the value at the address in BC """
    gb.memory.write_8bit(0x1234,0x11)
    gb.cpu.register.set_bc(0x1234)
    cycles = op.code_0a(gb)
    assert cycles == 8
    assert_registers(gb,A=0x11,B=0x12,C=0x34)
    assert_memory(gb, {0x1234:0x11})


# noinspection PyShadowingNames
def test_code_0b(gb):
    """ DEC BC - BC=BC-1 """
    gb.cpu.register.set_bc(0x0000)
    cycles = op.code_0b(gb)
    assert cycles == 8
    assert_registers(gb, B=0xFF, C=0xFF)

    gb.cpu.register.set_bc(0x0100)
    cycles = op.code_0b(gb)
    assert cycles == 8
    assert_registers(gb, B=0x00, C=0xFF)

    gb.cpu.register.set_bc(0x1000)
    cycles = op.code_0b(gb)
    assert cycles == 8
    assert_registers(gb, B=0x0F, C=0xFF)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_0c(gb):
    """ INC C - C=C+1 """
    gb.cpu.register.C = 0x00
    cycles = op.code_0c(gb)
    assert cycles == 4
    assert_registers(gb, C=0x01, F=0b00000000)

    gb.cpu.register.C = 0x0F
    cycles = op.code_0c(gb)
    assert cycles == 4
    assert_registers(gb, C=0x10, F=0b00100000)

    gb.cpu.register.C = 0xF0
    cycles = op.code_0c(gb)
    assert cycles == 4
    assert_registers(gb, C=0xF1, F=0b00000000)

    gb.cpu.register.C = 0xFF
    cycles = op.code_0c(gb)
    assert cycles == 4
    assert_registers(gb, C=0x00, F=0b10100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_0d(gb):
    """ DEC C - C=C-1 """
    gb.cpu.register.C = 0x00
    cycles = op.code_0d(gb)
    assert cycles == 4
    assert_registers(gb, C=0xFF, F=0b01100000)

    gb.cpu.register.C = 0x0F
    cycles = op.code_0d(gb)
    assert cycles == 4
    assert_registers(gb, C=0x0E, F=0b01000000)

    gb.cpu.register.C = 0x01
    cycles = op.code_0d(gb)
    assert cycles == 4
    assert_registers(gb, C=0x00, F=0b11000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_0e(gb):
    """ LD C,d8 """
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("99")
    cycles = op.code_0e(gb)
    assert cycles == 8
    assert_registers(gb,C=0x99,PC=0x0001)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_0f(gb):
    """ RRCA - Copy register A bit 0 to Carry flag, then rotate register A right """
    gb.cpu.register.A = 0b11100011
    cycles = op.code_0f(gb)
    assert cycles == 4
    assert_registers(gb, A=0b11110001, F=0b00010000)

    gb.cpu.register.A = 0b00000000
    cycles = op.code_0f(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000000, F=0b10000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_10(gb):
    """
    STOP - Switch Game Boy into VERY low power standby mode. Halt CPU and LCD display until a button is pressed
    See: http://gbdev.gg8.se/wiki/articles/Reducing_Power_Consumption
    """
    cycles = op.code_10(gb)
    assert cycles == 4
    assert gb.cpu.stopped is True
    assert_registers(gb)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_11(gb):
    """ LD DE,d16 - Stores given 16-bit value at DE """
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("33 99")
    cycles = op.code_11(gb)
    assert cycles == 12
    assert_registers(gb,D=0x99,E=0x33,PC=0x0002)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_12(gb):
    """ LD (DE),A - Stores reg at the address in DE """
    gb.cpu.register.set_de(0x0110)
    gb.cpu.register.A = 0x66
    cycles = op.code_12(gb)
    assert cycles == 8
    assert_registers(gb,A=0x66,D=0x01,E=0x10)
    assert_memory(gb,{0x0110:0x66})


# noinspection PyShadowingNames
def test_code_13(gb):
    """ INC DE - DE=DE+1 """
    gb.cpu.register.set_de(0x0000)
    cycles = op.code_13(gb)
    assert cycles == 8
    assert_registers(gb, D=0x00, E=0x01)

    gb.cpu.register.set_de(0x00FF)
    cycles = op.code_13(gb)
    assert cycles == 8
    assert_registers(gb, D=0x01, E=0x00)

    gb.cpu.register.set_de(0x0FFF)
    cycles = op.code_13(gb)
    assert cycles == 8
    assert_registers(gb, D=0x10, E=0x00)

    gb.cpu.register.set_de(0xFFFF)
    cycles = op.code_13(gb)
    assert cycles == 8
    assert_registers(gb, D=0x00, E=0x00)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_14(gb):
    """ INC D - D=D+1 """
    gb.cpu.register.D = 0x00
    cycles = op.code_14(gb)
    assert cycles == 4
    assert_registers(gb, D=0x01, F=0b00000000)

    gb.cpu.register.D = 0x0F
    cycles = op.code_14(gb)
    assert cycles == 4
    assert_registers(gb, D=0x10, F=0b00100000)

    gb.cpu.register.D = 0xF0
    cycles = op.code_14(gb)
    assert cycles == 4
    assert_registers(gb, D=0xF1, F=0b00000000)

    gb.cpu.register.D = 0xFF
    cycles = op.code_14(gb)
    assert cycles == 4
    assert_registers(gb, D=0x00, F=0b10100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_15(gb):
    """ DEC D - D=D-1 """
    gb.cpu.register.D = 0x00
    cycles = op.code_15(gb)
    assert cycles == 4
    assert_registers(gb, D=0xFF, F=0b01100000)

    gb.cpu.register.D = 0x0F
    cycles = op.code_15(gb)
    assert cycles == 4
    assert_registers(gb, D=0x0E, F=0b01000000)

    gb.cpu.register.D = 0x01
    cycles = op.code_15(gb)
    assert cycles == 4
    assert_registers(gb, D=0x00, F=0b11000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_16(gb):
    """ LD D,d8 """
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("99")
    cycles = op.code_16(gb)
    assert cycles == 8
    assert_registers(gb,D=0x99,PC=0x0001)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_17(gb):
    """ RLA - Copy register A bit 7 to temp, replace A bit 7 with Carry flag, rotate A left, copy temp to Carry flag """
    gb.cpu.register.A = 0b11100010
    gb.cpu.register.F = 0b00010000
    cycles = op.code_17(gb)
    assert cycles == 4
    assert_registers(gb, A=0b11000101, F=0b00010000)

    gb.cpu.register.A = 0b00000000
    gb.cpu.register.F = 0b00010000
    cycles = op.code_17(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000001, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_18(gb):
    """ JP r8 - make the command at address (current address + r8) the next to be executed (r8 is signed) """
    gb.cpu.register.PC = 0x0000
    gb.cpu._cartridge_data = bytes.fromhex("03")
    cycles = op.code_18(gb)
    assert cycles == 12
    assert_registers(gb,PC=0x0004)

    gb.cpu.register.PC = 0x0000
    gb.cpu._cartridge_data = bytes.fromhex("FD")  # -3
    cycles = op.code_18(gb)
    assert cycles == 12
    assert_registers(gb, PC=0xFFFE)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_19(gb):
    """ ADD HL,DE - HL=HL+DE """
    gb.cpu.register.set_hl(0x0000)
    gb.cpu.register.set_de(0x0001)
    cycles = op.code_19(gb)
    assert cycles == 8
    assert_registers(gb, D=0x00, E=0x01, H=0x00, L=0x01, F=0b00000000)

    gb.cpu.register.set_hl(0x000F)
    gb.cpu.register.set_de(0x0001)
    cycles = op.code_19(gb)
    assert cycles == 8
    assert_registers(gb, D=0x00, E=0x01, H=0x00, L=0x10, F=0b00000000)

    gb.cpu.register.set_hl(0xF000)
    gb.cpu.register.set_de(0x1000)
    cycles = op.code_19(gb)
    assert cycles == 8
    assert_registers(gb, D=0x10, E=0x00, H=0x00, L=0x00, F=0b00010000)

    gb.cpu.register.set_hl(0x0FFF)
    gb.cpu.register.set_de(0x0001)
    cycles = op.code_19(gb)
    assert cycles == 8
    assert_registers(gb, D=0x00, E=0x01, H=0x10, L=0x00, F=0b00100000)

    gb.cpu.register.set_hl(0xFFFF)
    gb.cpu.register.set_de(0x0001)
    cycles = op.code_19(gb)
    assert cycles == 8
    assert_registers(gb, D=0x00, E=0x01, H=0x00, L=0x00, F=0b00110000)

    gb.cpu.register.set_hl(0xFFFF)
    gb.cpu.register.set_de(0x0002)
    cycles = op.code_19(gb)
    assert cycles == 8
    assert_registers(gb, D=0x00, E=0x02, H=0x00, L=0x01, F=0b00110000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_1a(gb):
    """ LD A,(DE) - Load reg with the value at the address in DE """
    gb.memory.write_8bit(0x1234, 0x11)
    gb.cpu.register.set_de(0x1234)
    cycles = op.code_1a(gb)
    assert cycles == 8
    assert_registers(gb, A=0x11, D=0x12, E=0x34)
    assert_memory(gb, {0x1234: 0x11})


# noinspection PyShadowingNames
def test_code_1b(gb):
    """ DEC DE - DE=DE-1 """
    gb.cpu.register.set_de(0x0000)
    cycles = op.code_1b(gb)
    assert cycles == 8
    assert_registers(gb, D=0xFF, E=0xFF)

    gb.cpu.register.set_de(0x0100)
    cycles = op.code_1b(gb)
    assert cycles == 8
    assert_registers(gb, D=0x00, E=0xFF)

    gb.cpu.register.set_de(0x1000)
    cycles = op.code_1b(gb)
    assert cycles == 8
    assert_registers(gb, D=0x0F, E=0xFF)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_1c(gb):
    """ INC E - E=E+1 """
    gb.cpu.register.E = 0x00
    cycles = op.code_1c(gb)
    assert cycles == 4
    assert_registers(gb, E=0x01, F=0b00000000)

    gb.cpu.register.E = 0x0F
    cycles = op.code_1c(gb)
    assert cycles == 4
    assert_registers(gb, E=0x10, F=0b00100000)

    gb.cpu.register.E = 0xF0
    cycles = op.code_1c(gb)
    assert cycles == 4
    assert_registers(gb, E=0xF1, F=0b00000000)

    gb.cpu.register.E = 0xFF
    cycles = op.code_1c(gb)
    assert cycles == 4
    assert_registers(gb, E=0x00, F=0b10100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_1d(gb):
    """ DEC E - E=E-1 """
    gb.cpu.register.E = 0x00
    cycles = op.code_1d(gb)
    assert cycles == 4
    assert_registers(gb, E=0xFF, F=0b01100000)

    gb.cpu.register.E = 0x0F
    cycles = op.code_1d(gb)
    assert cycles == 4
    assert_registers(gb, E=0x0E, F=0b01000000)

    gb.cpu.register.E = 0x01
    cycles = op.code_1d(gb)
    assert cycles == 4
    assert_registers(gb, E=0x00, F=0b11000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_1e(gb):
    """ LD E,d8 """
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("99")
    cycles = op.code_1e(gb)
    assert cycles == 8
    assert_registers(gb,E=0x99,PC=0x0001)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_1f(gb):
    """ RRA - Copy register A bit 0 to temp, replace A bit 0 w/ Carry flag, rotate A right, copy temp to Carry flag """
    gb.cpu.register.A = 0b11100011
    gb.cpu.register.F = 0b00010000
    cycles = op.code_1f(gb)
    assert cycles == 4
    assert_registers(gb, A=0b11110001, F=0b00010000)

    gb.cpu.register.A = 0b00000000
    gb.cpu.register.F = 0b00010000
    cycles = op.code_1f(gb)
    assert cycles == 4
    assert_registers(gb, A=0b10000000, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_20(gb):
    """ JR NZ,r8 - If flag Z is reset, add r8 to current address and jump to it """
    gb.cpu.register.PC = 0x0000
    gb.cpu.register.F = 0b00000000
    gb.cpu._cartridge_data = bytes.fromhex("03")
    cycles = op.code_20(gb)
    assert cycles == 12
    assert_registers(gb, PC=0x0004)

    gb.cpu.register.PC = 0x0000
    gb.cpu.register.F = 0b10000000
    gb.cpu._cartridge_data = bytes.fromhex("FD")  # -3
    cycles = op.code_20(gb)
    assert cycles == 8
    assert_registers(gb, PC=0x0001, F=0b10000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_21(gb):
    """ LD HL,d16 - Stores given 16-bit value at HL """
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("33 99")
    cycles = op.code_21(gb)
    assert cycles == 12
    assert_registers(gb,H=0x99,L=0x33, PC=0x0002)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_22(gb):
    """ LD (HL+),A or LD (HLI),A or LDI (HL),A - Put value at A into address HL. Increment HL """
    gb.cpu.register.A = 0x69
    gb.cpu.register.set_hl(0x1010)
    cycles = op.code_22(gb)
    assert cycles == 8
    assert_registers(gb,A=0x69,H=0x10,L=0x11)
    assert_memory(gb,{0x1010:0x69})


# noinspection PyShadowingNames
def test_code_23(gb):
    """ INC HL - HL=HL+1 """
    gb.cpu.register.set_hl(0x0000)
    cycles = op.code_23(gb)
    assert cycles == 8
    assert_registers(gb, H=0x00, L=0x01)

    gb.cpu.register.set_hl(0x00FF)
    cycles = op.code_23(gb)
    assert cycles == 8
    assert_registers(gb, H=0x01, L=0x00)

    gb.cpu.register.set_hl(0x0FFF)
    cycles = op.code_23(gb)
    assert cycles == 8
    assert_registers(gb, H=0x10, L=0x00)

    gb.cpu.register.set_hl(0xFFFF)
    cycles = op.code_23(gb)
    assert cycles == 8
    assert_registers(gb, H=0x00, L=0x00)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_24(gb):
    """ INC H - H=H+1 """
    gb.cpu.register.H = 0x00
    cycles = op.code_24(gb)
    assert cycles == 4
    assert_registers(gb, H=0x01, F=0b00000000)

    gb.cpu.register.H = 0x0F
    cycles = op.code_24(gb)
    assert cycles == 4
    assert_registers(gb, H=0x10, F=0b00100000)

    gb.cpu.register.H = 0xF0
    cycles = op.code_24(gb)
    assert cycles == 4
    assert_registers(gb, H=0xF1, F=0b00000000)

    gb.cpu.register.H = 0xFF
    cycles = op.code_24(gb)
    assert cycles == 4
    assert_registers(gb, H=0x00, F=0b10100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_25(gb):
    """ DEC H - H=H-1 """
    gb.cpu.register.H = 0x00
    cycles = op.code_25(gb)
    assert cycles == 4
    assert_registers(gb, H=0xFF, F=0b01100000)

    gb.cpu.register.H = 0x0F
    cycles = op.code_25(gb)
    assert cycles == 4
    assert_registers(gb, H=0x0E, F=0b01000000)

    gb.cpu.register.H = 0x01
    cycles = op.code_25(gb)
    assert cycles == 4
    assert_registers(gb, H=0x00, F=0b11000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_26(gb):
    """ LD H,d8 """
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("99")
    cycles = op.code_26(gb)
    assert cycles == 8
    assert_registers(gb,H=0x99,PC=0x0001)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_27(gb):
    """
    DAA - Adjust value in register A for Binary Coded Decimal representation (i.e. one 0-9 value per nibble)
    See:  http://gbdev.gg8.se/wiki/articles/DAA
    """
    gb.cpu.register.A = 0b00111100  # 3|12 -> should be 4|2
    gb.cpu.register.F = 0b00000000
    cycles = op.code_27(gb)
    assert cycles == 4
    assert_registers(gb, A=0b01000010, F=0b00000000)

    gb.cpu.register.A = 0b01100100  # 6|4 -> should stay 6|4
    gb.cpu.register.F = 0b00000000
    cycles = op.code_27(gb)
    assert cycles == 4
    assert_registers(gb, A=0b01100100, F=0b00000000)

    gb.cpu.register.A = 0b10100000  # 10|0 -> should be 0|0 with Z flag
    gb.cpu.register.F = 0b00000000
    cycles = op.code_27(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000000, F=0b10010000)

    gb.cpu.register.A = 0b11000010  # 12|2 -> should be 2|2 with C flag
    gb.cpu.register.F = 0b00000000
    cycles = op.code_27(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00100010, F=0b00010000)

    gb.cpu.register.A = 0b00001010  # 0|10 with N/H flag-> should be 0|4
    gb.cpu.register.F = 0b01100000
    cycles = op.code_27(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000100, F=0b01000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_28(gb):
    """ JR Z,r8 - If flag Z is set, add r8 to current address and jump to it """
    gb.cpu.register.PC = 0x0000
    gb.cpu.register.F = 0b10000000
    gb.cpu._cartridge_data = bytes.fromhex("03")
    cycles = op.code_28(gb)
    assert cycles == 12
    assert_registers(gb, PC=0x0004, F=0b10000000)

    gb.cpu.register.PC = 0x0000
    gb.cpu.register.F = 0b00000000
    gb.cpu._cartridge_data = bytes.fromhex("FD")  # -3
    cycles = op.code_28(gb)
    assert cycles == 8
    assert_registers(gb, PC=0x0001)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_29(gb):
    """ ADD HL,HL - HL=HL+HL """
    gb.cpu.register.set_hl(0x0001)
    cycles = op.code_29(gb)
    assert cycles == 8
    assert_registers(gb, H=0x00, L=0x02, F=0b00000000)

    gb.cpu.register.set_hl(0x0008)
    cycles = op.code_29(gb)
    assert cycles == 8
    assert_registers(gb, H=0x00, L=0x10, F=0b00000000)

    gb.cpu.register.set_hl(0x8000)
    cycles = op.code_29(gb)
    assert cycles == 8
    assert_registers(gb, H=0x00, L=0x00, F=0b00010000)

    gb.cpu.register.set_hl(0x0800)
    cycles = op.code_29(gb)
    assert cycles == 8
    assert_registers(gb, H=0x10, L=0x00, F=0b00100000)

    gb.cpu.register.set_hl(0x8800)
    cycles = op.code_29(gb)
    assert cycles == 8
    assert_registers(gb, H=0x10, L=0x00, F=0b00110000)

    gb.cpu.register.set_hl(0xFFFF)
    cycles = op.code_29(gb)
    assert cycles == 8
    assert_registers(gb, H=0xFF, L=0xFE, F=0b00110000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_2a(gb):
    """ LD A,(HL+) or LD A,(HLI) or LDI A,(HL) - Put value at address HL into A. Increment HL """
    gb.memory.write_8bit(0x1010,0x69)
    gb.cpu.register.set_hl(0x1010)
    cycles = op.code_2a(gb)
    assert cycles == 8
    assert_registers(gb, A=0x69, H=0x10, L=0x11)
    assert_memory(gb, {0x1010: 0x69})


# noinspection PyShadowingNames
def test_code_2b(gb):
    """ DEC HL - HL=HL-1 """
    gb.cpu.register.set_hl(0x0000)
    cycles = op.code_2b(gb)
    assert cycles == 8
    assert_registers(gb, H=0xFF, L=0xFF)

    gb.cpu.register.set_hl(0x0100)
    cycles = op.code_2b(gb)
    assert cycles == 8
    assert_registers(gb, H=0x00, L=0xFF)

    gb.cpu.register.set_hl(0x1000)
    cycles = op.code_2b(gb)
    assert cycles == 8
    assert_registers(gb, H=0x0F, L=0xFF)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_2c(gb):
    """ INC L - L=L+1 """
    gb.cpu.register.L = 0x00
    cycles = op.code_2c(gb)
    assert cycles == 4
    assert_registers(gb, L=0x01, F=0b00000000)

    gb.cpu.register.L = 0x0F
    cycles = op.code_2c(gb)
    assert cycles == 4
    assert_registers(gb, L=0x10, F=0b00100000)

    gb.cpu.register.L = 0xF0
    cycles = op.code_2c(gb)
    assert cycles == 4
    assert_registers(gb, L=0xF1, F=0b00000000)

    gb.cpu.register.L = 0xFF
    cycles = op.code_2c(gb)
    assert cycles == 4
    assert_registers(gb, L=0x00, F=0b10100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_2d(gb):
    """ DEC L - L=L-1 """
    gb.cpu.register.L = 0x00
    cycles = op.code_2d(gb)
    assert cycles == 4
    assert_registers(gb, L=0xFF, F=0b01100000)

    gb.cpu.register.L = 0x0F
    cycles = op.code_2d(gb)
    assert cycles == 4
    assert_registers(gb, L=0x0E, F=0b01000000)

    gb.cpu.register.L = 0x01
    cycles = op.code_2d(gb)
    assert cycles == 4
    assert_registers(gb, L=0x00, F=0b11000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_2e(gb):
    """ LD L,d8 """
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("99")
    cycles = op.code_2e(gb)
    assert cycles == 8
    assert_registers(gb,L=0x99,PC=0x0001)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_2f(gb):
    """ CPL - Logical complement of register A (i.e. flip all bits) """
    gb.cpu.register.A = 0b00111100
    cycles = op.code_2f(gb)
    assert cycles == 4
    assert_registers(gb, A=0b11000011, F=0b01100000)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_30(gb):
    """ JR NC,r8 - If flag C is reset, add r8 to current address and jump to it """
    gb.cpu.register.PC = 0x0000
    gb.cpu.register.F = 0b00000000
    gb.cpu._cartridge_data = bytes.fromhex("03")
    cycles = op.code_30(gb)
    assert cycles == 12
    assert_registers(gb, PC=0x0004)

    gb.cpu.register.PC = 0x0000
    gb.cpu.register.F = 0b00010000
    gb.cpu._cartridge_data = bytes.fromhex("FD")  # -3
    cycles = op.code_30(gb)
    assert cycles == 8
    assert_registers(gb, PC=0x0001, F=0b00010000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_31(gb):
    """ LD SP,d16 - Stores given 16-bit value at SP """
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("33 99")
    cycles = op.code_31(gb)
    assert cycles == 12
    assert_registers(gb, SP=0x9933, PC=0x0002)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_32(gb):
    """ LD (HL-),A or LD (HLD),A or LDD (HL),A - Put value at A into address HL. Decrement HL """
    gb.cpu.register.A = 0x69
    gb.cpu.register.set_hl(0x1010)
    cycles = op.code_32(gb)
    assert cycles == 8
    assert_registers(gb, A=0x69, H=0x10, L=0x0F)
    assert_memory(gb, {0x1010: 0x69})


# noinspection PyShadowingNames
def test_code_33(gb):
    """ INC SP - SP=SP+1 """
    gb.cpu.register.SP = 0x0000
    cycles = op.code_33(gb)
    assert cycles == 8
    assert_registers(gb, SP=0x0001)

    gb.cpu.register.SP = 0x00FF
    cycles = op.code_33(gb)
    assert cycles == 8
    assert_registers(gb, SP=0x0100)

    gb.cpu.register.SP = 0x0FFF
    cycles = op.code_33(gb)
    assert cycles == 8
    assert_registers(gb, SP=0x1000)

    gb.cpu.register.SP = 0xFFFF
    cycles = op.code_33(gb)
    assert cycles == 8
    assert_registers(gb, SP=0x0000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_34(gb):
    """ INC (HL) - (value at address HL)=(value at address HL)+1 """
    gb.memory.write_8bit(0x1010,0x00)
    gb.cpu.register.set_hl(0x1010)
    cycles = op.code_34(gb)
    assert cycles == 12
    assert_registers(gb, H=0x10, L=0x10, F=0b00000000)
    assert_memory(gb,{0x1010:0x01})

    gb.memory.write_8bit(0x1010, 0x0F)
    gb.cpu.register.set_hl(0x1010)
    cycles = op.code_34(gb)
    assert cycles == 12
    assert_registers(gb, H=0x10, L=0x10, F=0b00100000)
    assert_memory(gb, {0x1010: 0x10})

    gb.memory.write_8bit(0x1010, 0xF0)
    gb.cpu.register.set_hl(0x1010)
    cycles = op.code_34(gb)
    assert cycles == 12
    assert_registers(gb, H=0x10, L=0x10, F=0b00000000)
    assert_memory(gb, {0x1010: 0xF1})

    gb.memory.write_8bit(0x1010, 0xFF)
    gb.cpu.register.set_hl(0x1010)
    cycles = op.code_34(gb)
    assert cycles == 12
    assert_registers(gb, H=0x10, L=0x10, F=0b10100000)
    assert_memory(gb, {0x1010: 0x00})


# noinspection PyShadowingNames
def test_code_35(gb):
    """ DEC (HL) - (value at address HL)=(value at address HL)-1 """
    gb.memory.write_8bit(0x1010, 0x00)
    gb.cpu.register.set_hl(0x1010)
    cycles = op.code_35(gb)
    assert cycles == 12
    assert_registers(gb, H=0x10, L=0x10, F=0b01100000)
    assert_memory(gb, {0x1010: 0xFF})

    gb.memory.write_8bit(0x1010, 0x0F)
    gb.cpu.register.set_hl(0x1010)
    cycles = op.code_35(gb)
    assert cycles == 12
    assert_registers(gb, H=0x10, L=0x10, F=0b01000000)
    assert_memory(gb, {0x1010: 0x0E})

    gb.memory.write_8bit(0x1010, 0x01)
    gb.cpu.register.set_hl(0x1010)
    cycles = op.code_35(gb)
    assert cycles == 12
    assert_registers(gb, H=0x10, L=0x10, F=0b11000000)
    assert_memory(gb, {0x1010: 0x00})


# noinspection PyShadowingNames
def test_code_36(gb):
    """ LD (HL),d8 - Stores d8 at the address in HL """
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("99")
    gb.cpu.register.set_hl(0x1010)
    cycles = op.code_36(gb)
    assert cycles == 12
    assert_registers(gb, H=0x10, L=0x10, PC=0x0001)
    assert_memory(gb, {0x1010:0x99})


# noinspection PyShadowingNames
def test_code_37(gb):
    """ SCF - Set carry flag """
    gb.cpu.register.F = 0b00000000
    cycles = op.code_37(gb)
    assert cycles == 4
    assert_registers(gb, F=0b00010000)

    gb.cpu.register.F = 0b11110000
    cycles = op.code_37(gb)
    assert cycles == 4
    assert_registers(gb, F=0b10010000)


# noinspection PyShadowingNames
def test_code_38(gb):
    """ JR C,r8 - If flag C is set, add r8 to current address and jump to it """
    gb.cpu.register.PC = 0x0000
    gb.cpu.register.F = 0b00010000
    gb.cpu._cartridge_data = bytes.fromhex("03")
    cycles = op.code_38(gb)
    assert cycles == 12
    assert_registers(gb, PC=0x0004, F=0b00010000)

    gb.cpu.register.PC = 0x0000
    gb.cpu.register.F = 0b00000000
    gb.cpu._cartridge_data = bytes.fromhex("FD")  # -3
    cycles = op.code_38(gb)
    assert cycles == 8
    assert_registers(gb, PC=0x0001)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_39(gb):
    """ ADD HL,SP - HL=HL+SP """
    gb.cpu.register.set_hl(0x0000)
    gb.cpu.register.SP = 0x0001
    cycles = op.code_39(gb)
    assert cycles == 8
    assert_registers(gb, SP=0x0001, H=0x00, L=0x01, F=0b00000000)

    gb.cpu.register.set_hl(0x000F)
    gb.cpu.register.SP = 0x0001
    cycles = op.code_39(gb)
    assert cycles == 8
    assert_registers(gb, SP=0x0001, H=0x00, L=0x10, F=0b00000000)

    gb.cpu.register.set_hl(0xF000)
    gb.cpu.register.SP = 0x1000
    cycles = op.code_39(gb)
    assert cycles == 8
    assert_registers(gb, SP=0x1000, H=0x00, L=0x00, F=0b00010000)

    gb.cpu.register.set_hl(0x0FFF)
    gb.cpu.register.SP = 0x0001
    cycles = op.code_39(gb)
    assert cycles == 8
    assert_registers(gb, SP=0x0001, H=0x10, L=0x00, F=0b00100000)

    gb.cpu.register.set_hl(0xFFFF)
    gb.cpu.register.SP = 0x0001
    cycles = op.code_39(gb)
    assert cycles == 8
    assert_registers(gb, SP=0x0001, H=0x00, L=0x00, F=0b00110000)

    gb.cpu.register.set_hl(0xFFFF)
    gb.cpu.register.SP = 0x0002
    cycles = op.code_39(gb)
    assert cycles == 8
    assert_registers(gb, SP=0x0002, H=0x00, L=0x01, F=0b00110000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_3a(gb):
    """ LD A,(HL-) or LD A,(HLD) or LDD A,(HL) - Put value at address HL into A. Decrement HL """
    gb.memory.write_8bit(0x1010, 0x69)
    gb.cpu.register.set_hl(0x1010)
    cycles = op.code_3a(gb)
    assert cycles == 8
    assert_registers(gb, A=0x69, H=0x10, L=0x0F)
    assert_memory(gb, {0x1010: 0x69})


# noinspection PyShadowingNames
def test_code_3b(gb):
    """ DEC SP - SP=SP-1 """
    gb.cpu.register.SP = 0x0000
    cycles = op.code_3b(gb)
    assert cycles == 8
    assert_registers(gb, SP=0xFFFF)

    gb.cpu.register.SP = 0x0100
    cycles = op.code_3b(gb)
    assert cycles == 8
    assert_registers(gb, SP=0x00FF)

    gb.cpu.register.SP = 0x1000
    cycles = op.code_3b(gb)
    assert cycles == 8
    assert_registers(gb, SP=0x0FFF)


# noinspection PyShadowingNames
def test_code_3c(gb):
    """ INC A - A=A+1 """
    gb.cpu.register.A = 0x00
    cycles = op.code_3c(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, F=0b00000000)

    gb.cpu.register.A = 0x0F
    cycles = op.code_3c(gb)
    assert cycles == 4
    assert_registers(gb, A=0x10, F=0b00100000)

    gb.cpu.register.A = 0xF0
    cycles = op.code_3c(gb)
    assert cycles == 4
    assert_registers(gb, A=0xF1, F=0b00000000)

    gb.cpu.register.A = 0xFF
    cycles = op.code_3c(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, F=0b10100000)


# noinspection PyShadowingNames
def test_code_3d(gb):
    """ DEC A - A=A-1 """
    gb.cpu.register.A = 0x00
    cycles = op.code_3d(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFF, F=0b01100000)

    gb.cpu.register.A = 0x0F
    cycles = op.code_3d(gb)
    assert cycles == 4
    assert_registers(gb, A=0x0E, F=0b01000000)

    gb.cpu.register.A = 0x01
    cycles = op.code_3d(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, F=0b11000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_3e(gb):
    """ LD A,d8 """
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("99")
    cycles = op.code_3e(gb)
    assert cycles == 8
    assert_registers(gb,A=0x99,PC=0x0001)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_3f(gb):
    """ CCF - Invert carry flag """
    gb.cpu.register.F = 0b00010000
    cycles = op.code_3f(gb)
    assert cycles == 4
    assert_registers(gb, F=0b00000000)

    gb.cpu.register.F = 0b11100000
    cycles = op.code_3f(gb)
    assert cycles == 4
    assert_registers(gb, F=0b10010000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_40(gb):
    """ LD B,B (...why?) """
    gb.cpu.register.B = 0x99
    cycles = op.code_40(gb)
    assert cycles == 4
    assert_registers(gb,B=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_41(gb):
    """ LD B,C """
    gb.cpu.register.C = 0x99
    cycles = op.code_41(gb)
    assert cycles == 4
    assert_registers(gb,B=0x99,C=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_42(gb):
    """ LD B,D """
    gb.cpu.register.D = 0x99
    cycles = op.code_42(gb)
    assert cycles == 4
    assert_registers(gb,B=0x99,D=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_43(gb):
    """ LD B,E """
    gb.cpu.register.E = 0x99
    cycles = op.code_43(gb)
    assert cycles == 4
    assert_registers(gb,B=0x99,E=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_44(gb):
    """ LD B,H """
    gb.cpu.register.H = 0x99
    cycles = op.code_44(gb)
    assert cycles == 4
    assert_registers(gb,B=0x99,H=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_45(gb):
    """ LD B,L """
    gb.cpu.register.L = 0x99
    cycles = op.code_45(gb)
    assert cycles == 4
    assert_registers(gb,B=0x99,L=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_46(gb):
    """ LD B,(HL) - Load reg with the value at the address in HL """
    gb.memory.write_8bit(0x1010, 0x99)
    gb.cpu.register.set_hl(0x1010)
    cycles = op.code_46(gb)
    assert cycles == 8
    assert_registers(gb, B=0x99, H=0x10, L=0x10)
    assert_memory(gb,{0x1010:0x99})


# noinspection PyShadowingNames
def test_code_47(gb):
    """ LD B,A """
    gb.cpu.register.A = 0x99
    cycles = op.code_47(gb)
    assert cycles == 4
    assert_registers(gb,A=0x99,B=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_48(gb):
    """ LD C,B """
    gb.cpu.register.B = 0x99
    cycles = op.code_48(gb)
    assert cycles == 4
    assert_registers(gb,B=0x99,C=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_49(gb):
    """ LD C,C (...why?) """
    gb.cpu.register.C = 0x99
    cycles = op.code_49(gb)
    assert cycles == 4
    assert_registers(gb,C=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_4a(gb):
    """ LD C,D """
    gb.cpu.register.D = 0x99
    cycles = op.code_4a(gb)
    assert cycles == 4
    assert_registers(gb,C=0x99,D=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_4b(gb):
    """ LD C,E """
    gb.cpu.register.E = 0x99
    cycles = op.code_4b(gb)
    assert cycles == 4
    assert_registers(gb,C=0x99,E=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_4c(gb):
    """ LD C,H """
    gb.cpu.register.H = 0x99
    cycles = op.code_4c(gb)
    assert cycles == 4
    assert_registers(gb,C=0x99,H=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_4d(gb):
    """ LD C,L """
    gb.cpu.register.L = 0x99
    cycles = op.code_4d(gb)
    assert cycles == 4
    assert_registers(gb,C=0x99,L=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_4e(gb):
    """ LD C,(HL) - Load reg with the value at the address in HL """
    gb.memory.write_8bit(0x1010, 0x99)
    gb.cpu.register.set_hl(0x1010)
    cycles = op.code_4e(gb)
    assert cycles == 8
    assert_registers(gb, C=0x99, H=0x10, L=0x10)
    assert_memory(gb, {0x1010: 0x99})


# noinspection PyShadowingNames
def test_code_4f(gb):
    """ LD C,A """
    gb.cpu.register.A = 0x99
    cycles = op.code_4f(gb)
    assert cycles == 4
    assert_registers(gb,A=0x99,C=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_50(gb):
    """ LD D,B """
    gb.cpu.register.B = 0x99
    cycles = op.code_50(gb)
    assert cycles == 4
    assert_registers(gb,B=0x99,D=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_51(gb):
    """ LD D,C """
    gb.cpu.register.C = 0x99
    cycles = op.code_51(gb)
    assert cycles == 4
    assert_registers(gb,C=0x99,D=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_52(gb):
    """ LD D,D (...why?) """
    gb.cpu.register.D = 0x99
    cycles = op.code_52(gb)
    assert cycles == 4
    assert_registers(gb,D=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_53(gb):
    """ LD D,E """
    gb.cpu.register.E = 0x99
    cycles = op.code_53(gb)
    assert cycles == 4
    assert_registers(gb,D=0x99,E=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_54(gb):
    """ LD D,H """
    gb.cpu.register.H = 0x99
    cycles = op.code_54(gb)
    assert cycles == 4
    assert_registers(gb,D=0x99,H=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_55(gb):
    """ LD D,L """
    gb.cpu.register.L = 0x99
    cycles = op.code_55(gb)
    assert cycles == 4
    assert_registers(gb,D=0x99,L=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_56(gb):
    """ LD D,(HL) - Load reg with the value at the address in HL """
    gb.memory.write_8bit(0x1010, 0x99)
    gb.cpu.register.set_hl(0x1010)
    cycles = op.code_56(gb)
    assert cycles == 8
    assert_registers(gb, D=0x99, H=0x10, L=0x10)
    assert_memory(gb, {0x1010: 0x99})


# noinspection PyShadowingNames
def test_code_57(gb):
    """ LD D,A """
    gb.cpu.register.A = 0x99
    cycles = op.code_57(gb)
    assert cycles == 4
    assert_registers(gb,A=0x99,D=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_58(gb):
    """ LD E,B """
    gb.cpu.register.B = 0x99
    cycles = op.code_58(gb)
    assert cycles == 4
    assert_registers(gb,B=0x99,E=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_59(gb):
    """ LD E,C """
    gb.cpu.register.C = 0x99
    cycles = op.code_59(gb)
    assert cycles == 4
    assert_registers(gb,C=0x99,E=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_5a(gb):
    """ LD E,D """
    gb.cpu.register.D = 0x99
    cycles = op.code_5a(gb)
    assert cycles == 4
    assert_registers(gb,D=0x99,E=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_5b(gb):
    """ LD E,E (...why?) """
    gb.cpu.register.E = 0x99
    cycles = op.code_5b(gb)
    assert cycles == 4
    assert_registers(gb,E=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_5c(gb):
    """ LD E,H """
    gb.cpu.register.H = 0x99
    cycles = op.code_5c(gb)
    assert cycles == 4
    assert_registers(gb,E=0x99,H=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_5d(gb):
    """ LD E,L """
    gb.cpu.register.L = 0x99
    cycles = op.code_5d(gb)
    assert cycles == 4
    assert_registers(gb,E=0x99,L=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_5e(gb):
    """ LD E,(HL) - Load reg with the value at the address in HL """
    gb.memory.write_8bit(0x1010, 0x99)
    gb.cpu.register.set_hl(0x1010)
    cycles = op.code_5e(gb)
    assert cycles == 8
    assert_registers(gb, E=0x99, H=0x10, L=0x10)
    assert_memory(gb, {0x1010: 0x99})


# noinspection PyShadowingNames
def test_code_5f(gb):
    """ LD E,A """
    gb.cpu.register.A = 0x99
    cycles = op.code_5f(gb)
    assert cycles == 4
    assert_registers(gb,A=0x99,E=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_60(gb):
    """ LD H,B """
    gb.cpu.register.B = 0x99
    cycles = op.code_60(gb)
    assert cycles == 4
    assert_registers(gb, B=0x99, H=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_61(gb):
    """ LD H,C """
    gb.cpu.register.C = 0x99
    cycles = op.code_61(gb)
    assert cycles == 4
    assert_registers(gb, C=0x99, H=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_62(gb):
    """ LD H,D """
    gb.cpu.register.D = 0x99
    cycles = op.code_62(gb)
    assert cycles == 4
    assert_registers(gb, D=0x99, H=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_63(gb):
    """ LD H,E """
    gb.cpu.register.E = 0x99
    cycles = op.code_63(gb)
    assert cycles == 4
    assert_registers(gb, E=0x99, H=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_64(gb):
    """ LD H,H (...why?) """
    gb.cpu.register.H = 0x99
    cycles = op.code_64(gb)
    assert cycles == 4
    assert_registers(gb, H=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_65(gb):
    """ LD H,L """
    gb.cpu.register.L = 0x99
    cycles = op.code_65(gb)
    assert cycles == 4
    assert_registers(gb, H=0x99, L=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_66(gb):
    """ LD H,(HL) - Load reg with the value at the address in HL """
    gb.memory.write_8bit(0x1010, 0x99)
    gb.cpu.register.set_hl(0x1010)
    cycles = op.code_66(gb)
    assert cycles == 8
    assert_registers(gb, H=0x99, L=0x10)
    assert_memory(gb, {0x1010: 0x99})


# noinspection PyShadowingNames
def test_code_67(gb):
    """ LD H,A """
    gb.cpu.register.A = 0x99
    cycles = op.code_67(gb)
    assert cycles == 4
    assert_registers(gb, A=0x99, H=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_68(gb):
    """ LD L,B """
    gb.cpu.register.B = 0x99
    cycles = op.code_68(gb)
    assert cycles == 4
    assert_registers(gb, B=0x99, L=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_69(gb):
    """ LD L,C """
    gb.cpu.register.C = 0x99
    cycles = op.code_69(gb)
    assert cycles == 4
    assert_registers(gb, C=0x99, L=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_6a(gb):
    """ LD L,D """
    gb.cpu.register.D = 0x99
    cycles = op.code_6a(gb)
    assert cycles == 4
    assert_registers(gb, D=0x99, L=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_6b(gb):
    """ LD L,E """
    gb.cpu.register.E = 0x99
    cycles = op.code_6b(gb)
    assert cycles == 4
    assert_registers(gb, E=0x99, L=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_6c(gb):
    """ LD L,H """
    gb.cpu.register.H = 0x99
    cycles = op.code_6c(gb)
    assert cycles == 4
    assert_registers(gb, H=0x99, L=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_6d(gb):
    """ LD L,L (might be a newbie question but... why?) """
    gb.cpu.register.L = 0x99
    cycles = op.code_6d(gb)
    assert cycles == 4
    assert_registers(gb, L=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_6e(gb):
    """ LD L,(HL) - Load reg with the value at the address in HL """
    gb.memory.write_8bit(0x1010, 0x99)
    gb.cpu.register.set_hl(0x1010)
    cycles = op.code_6e(gb)
    assert cycles == 8
    assert_registers(gb, H=0x10, L=0x99)
    assert_memory(gb, {0x1010: 0x99})


# noinspection PyShadowingNames
def test_code_6f(gb):
    """ LD L,A """
    gb.cpu.register.A = 0x99
    cycles = op.code_6f(gb)
    assert cycles == 4
    assert_registers(gb, A=0x99, L=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_70(gb):
    """ LD (HL),B - Stores reg at the address in HL """
    gb.cpu.register.B = 0x99
    gb.cpu.register.set_hl(0x1010)
    cycles = op.code_70(gb)
    assert cycles == 8
    assert_registers(gb,B=0x99,H=0x10,L=0x10)
    assert_memory(gb,{0x1010:0x99})


# noinspection PyShadowingNames
def test_code_71(gb):
    """ LD (HL),C - Stores reg at the address in HL """
    gb.cpu.register.C = 0x99
    gb.cpu.register.set_hl(0x1010)
    cycles = op.code_71(gb)
    assert cycles == 8
    assert_registers(gb, C=0x99, H=0x10, L=0x10)
    assert_memory(gb, {0x1010: 0x99})


# noinspection PyShadowingNames
def test_code_72(gb):
    """ LD (HL),D - Stores reg at the address in HL """
    gb.cpu.register.D = 0x99
    gb.cpu.register.set_hl(0x1010)
    cycles = op.code_72(gb)
    assert cycles == 8
    assert_registers(gb, D=0x99, H=0x10, L=0x10)
    assert_memory(gb, {0x1010: 0x99})


# noinspection PyShadowingNames
def test_code_73(gb):
    """ LD (HL),E - Stores reg at the address in HL """
    gb.cpu.register.E = 0x99
    gb.cpu.register.set_hl(0x1010)
    cycles = op.code_73(gb)
    assert cycles == 8
    assert_registers(gb, E=0x99, H=0x10, L=0x10)
    assert_memory(gb, {0x1010: 0x99})


# noinspection PyShadowingNames
def test_code_74(gb):
    """ LD (HL),H - Stores reg at the address in HL """
    gb.cpu.register.set_hl(0x1110)
    cycles = op.code_74(gb)
    assert cycles == 8
    assert_registers(gb, H=0x11, L=0x10)
    assert_memory(gb, {0x1110: 0x11})


# noinspection PyShadowingNames
def test_code_75(gb):
    """ LD (HL),L - Stores reg at the address in HL """
    gb.cpu.register.set_hl(0x1011)
    cycles = op.code_75(gb)
    assert cycles == 8
    assert_registers(gb, H=0x10, L=0x11)
    assert_memory(gb, {0x1011: 0x11})


# noinspection PyShadowingNames
def test_code_76(gb):
    """
    HALT - Power down CPU (by stopping the system clock) until an interrupt occurs
    See: http://gbdev.gg8.se/wiki/articles/Reducing_Power_Consumption
    """
    cycles = op.code_76(gb)
    assert cycles == 4
    assert gb.cpu.halted is True
    assert_registers(gb)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_77(gb):
    """ LD (HL),A - Stores reg at the address in HL """
    gb.cpu.register.A = 0x99
    gb.cpu.register.set_hl(0x1010)
    cycles = op.code_77(gb)
    assert cycles == 8
    assert_registers(gb, A=0x99, H=0x10, L=0x10)
    assert_memory(gb, {0x1010: 0x99})


# noinspection PyShadowingNames
def test_code_78(gb):
    """ LD A,B """
    gb.cpu.register.B = 0x99
    cycles = op.code_78(gb)
    assert cycles == 4
    assert_registers(gb, A=0x99, B=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_79(gb):
    """ LD A,C """
    gb.cpu.register.C = 0x99
    cycles = op.code_79(gb)
    assert cycles == 4
    assert_registers(gb, A=0x99, C=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_7a(gb):
    """ LD A,D """
    gb.cpu.register.D = 0x99
    cycles = op.code_7a(gb)
    assert cycles == 4
    assert_registers(gb, A=0x99, D=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_7b(gb):
    """ LD A,E """
    gb.cpu.register.E = 0x99
    cycles = op.code_7b(gb)
    assert cycles == 4
    assert_registers(gb, A=0x99, E=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_7c(gb):
    """ LD A,H """
    gb.cpu.register.H = 0x99
    cycles = op.code_7c(gb)
    assert cycles == 4
    assert_registers(gb, A=0x99, H=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_7d(gb):
    """ LD A,L """
    gb.cpu.register.L = 0x99
    cycles = op.code_7d(gb)
    assert cycles == 4
    assert_registers(gb, A=0x99, L=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_7e(gb):
    """ LD A,(HL) - Load reg with the value at the address in HL """
    gb.memory.write_8bit(0x1010, 0x99)
    gb.cpu.register.set_hl(0x1010)
    cycles = op.code_7e(gb)
    assert cycles == 8
    assert_registers(gb, A=0x99, H=0x10, L=0x10)
    assert_memory(gb, {0x1010: 0x99})


# noinspection PyShadowingNames
def test_code_7f(gb):
    """ LD A,A (might be a newbie question but... why?) """
    gb.cpu.register.A = 0x99
    cycles = op.code_7f(gb)
    assert cycles == 4
    assert_registers(gb, A=0x99)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_80(gb):
    """ ADD A,B - A=A+B """
    gb.cpu.register.A = 0x00
    gb.cpu.register.B = 0x00
    cycles = op.code_80(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, B=0x00, F=0b10000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.B = 0x01
    cycles = op.code_80(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, B=0x01, F=0b00000000)

    gb.cpu.register.A = 0x0F
    gb.cpu.register.B = 0x01
    cycles = op.code_80(gb)
    assert cycles == 4
    assert_registers(gb, A=0x10, B=0x01, F=0b00100000)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.B = 0x10
    cycles = op.code_80(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, B=0x10, F=0b10010000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.B = 0x01
    cycles = op.code_80(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, B=0x01, F=0b10110000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.B = 0x02
    cycles = op.code_80(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, B=0x02, F=0b00110000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_81(gb):
    """ ADD A,C - A=A+C """
    gb.cpu.register.A = 0x00
    gb.cpu.register.C = 0x00
    cycles = op.code_81(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, C=0x00, F=0b10000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.C = 0x01
    cycles = op.code_81(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, C=0x01, F=0b00000000)

    gb.cpu.register.A = 0x0F
    gb.cpu.register.C = 0x01
    cycles = op.code_81(gb)
    assert cycles == 4
    assert_registers(gb, A=0x10, C=0x01, F=0b00100000)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.C = 0x10
    cycles = op.code_81(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, C=0x10, F=0b10010000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.C = 0x01
    cycles = op.code_81(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, C=0x01, F=0b10110000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.C = 0x02
    cycles = op.code_81(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, C=0x02, F=0b00110000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_82(gb):
    """ ADD A,D - A=A+D """
    gb.cpu.register.A = 0x00
    gb.cpu.register.D = 0x00
    cycles = op.code_82(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, D=0x00, F=0b10000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.D = 0x01
    cycles = op.code_82(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, D=0x01, F=0b00000000)

    gb.cpu.register.A = 0x0F
    gb.cpu.register.D = 0x01
    cycles = op.code_82(gb)
    assert cycles == 4
    assert_registers(gb, A=0x10, D=0x01, F=0b00100000)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.D = 0x10
    cycles = op.code_82(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, D=0x10, F=0b10010000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.D = 0x01
    cycles = op.code_82(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, D=0x01, F=0b10110000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.D = 0x02
    cycles = op.code_82(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, D=0x02, F=0b00110000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_83(gb):
    """ ADD A,E - A=A+E """
    gb.cpu.register.A = 0x00
    gb.cpu.register.E = 0x00
    cycles = op.code_83(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, E=0x00, F=0b10000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.E = 0x01
    cycles = op.code_83(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, E=0x01, F=0b00000000)

    gb.cpu.register.A = 0x0F
    gb.cpu.register.E = 0x01
    cycles = op.code_83(gb)
    assert cycles == 4
    assert_registers(gb, A=0x10, E=0x01, F=0b00100000)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.E = 0x10
    cycles = op.code_83(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, E=0x10, F=0b10010000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.E = 0x01
    cycles = op.code_83(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, E=0x01, F=0b10110000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.E = 0x02
    cycles = op.code_83(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, E=0x02, F=0b00110000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_84(gb):
    """ ADD A,H - A=A+H """
    gb.cpu.register.A = 0x00
    gb.cpu.register.H = 0x00
    cycles = op.code_84(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, H=0x00, F=0b10000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.H = 0x01
    cycles = op.code_84(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, H=0x01, F=0b00000000)

    gb.cpu.register.A = 0x0F
    gb.cpu.register.H = 0x01
    cycles = op.code_84(gb)
    assert cycles == 4
    assert_registers(gb, A=0x10, H=0x01, F=0b00100000)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.H = 0x10
    cycles = op.code_84(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, H=0x10, F=0b10010000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.H = 0x01
    cycles = op.code_84(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, H=0x01, F=0b10110000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.H = 0x02
    cycles = op.code_84(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, H=0x02, F=0b00110000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_85(gb):
    """ ADD A,L - A=A+L """
    gb.cpu.register.A = 0x00
    gb.cpu.register.L = 0x00
    cycles = op.code_85(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, L=0x00, F=0b10000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.L = 0x01
    cycles = op.code_85(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, L=0x01, F=0b00000000)

    gb.cpu.register.A = 0x0F
    gb.cpu.register.L = 0x01
    cycles = op.code_85(gb)
    assert cycles == 4
    assert_registers(gb, A=0x10, L=0x01, F=0b00100000)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.L = 0x10
    cycles = op.code_85(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, L=0x10, F=0b10010000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.L = 0x01
    cycles = op.code_85(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, L=0x01, F=0b10110000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.L = 0x02
    cycles = op.code_85(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, L=0x02, F=0b00110000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_86(gb):
    """ ADD A,(HL) - A=A+(value at address HL) """
    gb.cpu.register.set_hl(0x1010)
    gb.cpu.register.A = 0x00
    gb.memory.write_8bit(0x1010, 0x00)
    cycles = op.code_86(gb)
    assert cycles == 8
    assert_registers(gb, A=0x00, H=0x10, L=0x10, F=0b10000000)
    assert_memory(gb)

    gb.cpu.register.A = 0x00
    gb.memory.write_8bit(0x1010, 0x01)
    cycles = op.code_86(gb)
    assert cycles == 8
    assert_registers(gb, A=0x01, H=0x10, L=0x10, F=0b00000000)
    assert_memory(gb,{0x1010:0x01})

    gb.cpu.register.A = 0x0F
    gb.memory.write_8bit(0x1010, 0x01)
    cycles = op.code_86(gb)
    assert cycles == 8
    assert_registers(gb, A=0x10, H=0x10, L=0x10, F=0b00100000)
    assert_memory(gb, {0x1010: 0x01})

    gb.cpu.register.A = 0xF0
    gb.memory.write_8bit(0x1010, 0x10)
    cycles = op.code_86(gb)
    assert cycles == 8
    assert_registers(gb, A=0x00, H=0x10, L=0x10, F=0b10010000)
    assert_memory(gb, {0x1010: 0x10})

    gb.cpu.register.A = 0xFF
    gb.memory.write_8bit(0x1010, 0x01)
    cycles = op.code_86(gb)
    assert cycles == 8
    assert_registers(gb, A=0x00, H=0x10, L=0x10, F=0b10110000)
    assert_memory(gb, {0x1010: 0x01})

    gb.cpu.register.A = 0xFF
    gb.memory.write_8bit(0x1010, 0x02)
    cycles = op.code_86(gb)
    assert cycles == 8
    assert_registers(gb, A=0x01, H=0x10, L=0x10, F=0b00110000)
    assert_memory(gb, {0x1010: 0x02})


# noinspection PyShadowingNames
def test_code_87(gb):
    """ ADD A,A - A=A+A """
    gb.cpu.register.A = 0x00
    cycles = op.code_87(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, F=0b10000000)

    gb.cpu.register.A = 0x01
    cycles = op.code_87(gb)
    assert cycles == 4
    assert_registers(gb, A=0x02, F=0b00000000)

    gb.cpu.register.A = 0x08
    cycles = op.code_87(gb)
    assert cycles == 4
    assert_registers(gb, A=0x10, F=0b00100000)

    gb.cpu.register.A = 0x80
    cycles = op.code_87(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, F=0b10010000)

    gb.cpu.register.A = 0x88
    cycles = op.code_87(gb)
    assert cycles == 4
    assert_registers(gb, A=0x10, F=0b00110000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_88(gb):
    """ ADC A,B - A=A+B+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    gb.cpu.register.A = 0x00
    gb.cpu.register.B = 0x00
    gb.cpu.register.F = 0b00000000
    cycles = op.code_88(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, B=0x00, F=0b10000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.B = 0x00
    gb.cpu.register.F = 0b00010000
    cycles = op.code_88(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, B=0x00, F=0b00000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.B = 0x01
    gb.cpu.register.F = 0b00010000
    cycles = op.code_88(gb)
    assert cycles == 4
    assert_registers(gb, A=0x02, B=0x01, F=0b00000000)

    gb.cpu.register.A = 0x0E
    gb.cpu.register.B = 0x01
    gb.cpu.register.F = 0b00010000
    cycles = op.code_88(gb)
    assert cycles == 4
    assert_registers(gb, A=0x10, B=0x01, F=0b00100000)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.B = 0x0F
    gb.cpu.register.F = 0b00010000
    cycles = op.code_88(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, B=0x0F, F=0b10110000)

    gb.cpu.register.A = 0xFE
    gb.cpu.register.B = 0x01
    gb.cpu.register.F = 0b00010000
    cycles = op.code_88(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, B=0x01, F=0b10110000)

    gb.cpu.register.A = 0xFE
    gb.cpu.register.B = 0x02
    gb.cpu.register.F = 0b00010000
    cycles = op.code_88(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, B=0x02, F=0b00110000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_89(gb):
    """ ADC A,C - A=A+C+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    gb.cpu.register.A = 0x00
    gb.cpu.register.C = 0x00
    gb.cpu.register.F = 0b00000000
    cycles = op.code_89(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, C=0x00, F=0b10000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.C = 0x00
    gb.cpu.register.F = 0b00010000
    cycles = op.code_89(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, C=0x00, F=0b00000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.C = 0x01
    gb.cpu.register.F = 0b00010000
    cycles = op.code_89(gb)
    assert cycles == 4
    assert_registers(gb, A=0x02, C=0x01, F=0b00000000)

    gb.cpu.register.A = 0x0E
    gb.cpu.register.C = 0x01
    gb.cpu.register.F = 0b00010000
    cycles = op.code_89(gb)
    assert cycles == 4
    assert_registers(gb, A=0x10, C=0x01, F=0b00100000)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.C = 0x0F
    gb.cpu.register.F = 0b00010000
    cycles = op.code_89(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, C=0x0F, F=0b10110000)

    gb.cpu.register.A = 0xFE
    gb.cpu.register.C = 0x01
    gb.cpu.register.F = 0b00010000
    cycles = op.code_89(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, C=0x01, F=0b10110000)

    gb.cpu.register.A = 0xFE
    gb.cpu.register.C = 0x02
    gb.cpu.register.F = 0b00010000
    cycles = op.code_89(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, C=0x02, F=0b00110000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_8a(gb):
    """ ADC A,D - A=A+D+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    gb.cpu.register.A = 0x00
    gb.cpu.register.D = 0x00
    gb.cpu.register.F = 0b00000000
    cycles = op.code_8a(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, D=0x00, F=0b10000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.D = 0x00
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8a(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, D=0x00, F=0b00000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.D = 0x01
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8a(gb)
    assert cycles == 4
    assert_registers(gb, A=0x02, D=0x01, F=0b00000000)

    gb.cpu.register.A = 0x0E
    gb.cpu.register.D = 0x01
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8a(gb)
    assert cycles == 4
    assert_registers(gb, A=0x10, D=0x01, F=0b00100000)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.D = 0x0F
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8a(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, D=0x0F, F=0b10110000)

    gb.cpu.register.A = 0xFE
    gb.cpu.register.D = 0x01
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8a(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, D=0x01, F=0b10110000)

    gb.cpu.register.A = 0xFE
    gb.cpu.register.D = 0x02
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8a(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, D=0x02, F=0b00110000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_8b(gb):
    """ ADC A,E - A=A+E+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    gb.cpu.register.A = 0x00
    gb.cpu.register.E = 0x00
    gb.cpu.register.F = 0b00000000
    cycles = op.code_8b(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, E=0x00, F=0b10000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.E = 0x00
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8b(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, E=0x00, F=0b00000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.E = 0x01
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8b(gb)
    assert cycles == 4
    assert_registers(gb, A=0x02, E=0x01, F=0b00000000)

    gb.cpu.register.A = 0x0E
    gb.cpu.register.E = 0x01
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8b(gb)
    assert cycles == 4
    assert_registers(gb, A=0x10, E=0x01, F=0b00100000)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.E = 0x0F
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8b(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, E=0x0F, F=0b10110000)

    gb.cpu.register.A = 0xFE
    gb.cpu.register.E = 0x01
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8b(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, E=0x01, F=0b10110000)

    gb.cpu.register.A = 0xFE
    gb.cpu.register.E = 0x02
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8b(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, E=0x02, F=0b00110000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_8c(gb):
    """ ADC A,H - A=A+H+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    gb.cpu.register.A = 0x00
    gb.cpu.register.H = 0x00
    gb.cpu.register.F = 0b00000000
    cycles = op.code_8c(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, H=0x00, F=0b10000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.H = 0x00
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8c(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, H=0x00, F=0b00000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.H = 0x01
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8c(gb)
    assert cycles == 4
    assert_registers(gb, A=0x02, H=0x01, F=0b00000000)

    gb.cpu.register.A = 0x0E
    gb.cpu.register.H = 0x01
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8c(gb)
    assert cycles == 4
    assert_registers(gb, A=0x10, H=0x01, F=0b00100000)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.H = 0x0F
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8c(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, H=0x0F, F=0b10110000)

    gb.cpu.register.A = 0xFE
    gb.cpu.register.H = 0x01
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8c(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, H=0x01, F=0b10110000)

    gb.cpu.register.A = 0xFE
    gb.cpu.register.H = 0x02
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8c(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, H=0x02, F=0b00110000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_8d(gb):
    """ ADC A,L - A=A+L+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    gb.cpu.register.A = 0x00
    gb.cpu.register.L = 0x00
    gb.cpu.register.F = 0b00000000
    cycles = op.code_8d(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, L=0x00, F=0b10000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.L = 0x00
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8d(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, L=0x00, F=0b00000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.L = 0x01
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8d(gb)
    assert cycles == 4
    assert_registers(gb, A=0x02, L=0x01, F=0b00000000)

    gb.cpu.register.A = 0x0E
    gb.cpu.register.L = 0x01
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8d(gb)
    assert cycles == 4
    assert_registers(gb, A=0x10, L=0x01, F=0b00100000)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.L = 0x0F
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8d(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, L=0x0F, F=0b10110000)

    gb.cpu.register.A = 0xFE
    gb.cpu.register.L = 0x01
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8d(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, L=0x01, F=0b10110000)

    gb.cpu.register.A = 0xFE
    gb.cpu.register.L = 0x02
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8d(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, L=0x02, F=0b00110000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_8e(gb):
    """ ADC A,(HL) - A=A+(value at address HL)+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    gb.cpu.register.set_hl(0x1010)

    gb.cpu.register.A = 0x00
    gb.memory.write_8bit(0x1010, 0x00)
    gb.cpu.register.F = 0b00000000
    cycles = op.code_8e(gb)
    assert cycles == 8
    assert_registers(gb, A=0x00, H=0x10, L=0x10, F=0b10000000)
    assert_memory(gb)

    gb.cpu.register.A = 0x00
    gb.memory.write_8bit(0x1010, 0x00)
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8e(gb)
    assert cycles == 8
    assert_registers(gb, A=0x01, H=0x10, L=0x10, F=0b00000000)
    assert_memory(gb)

    gb.cpu.register.A = 0x00
    gb.memory.write_8bit(0x1010, 0x01)
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8e(gb)
    assert cycles == 8
    assert_registers(gb, A=0x02, H=0x10, L=0x10, F=0b00000000)
    assert_memory(gb,{0x1010:0x01})

    gb.cpu.register.A = 0x0E
    gb.memory.write_8bit(0x1010, 0x01)
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8e(gb)
    assert cycles == 8
    assert_registers(gb, A=0x10, H=0x10, L=0x10, F=0b00100000)
    assert_memory(gb, {0x1010:0x01})

    gb.cpu.register.A = 0xF0
    gb.memory.write_8bit(0x1010, 0x0F)
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8e(gb)
    assert cycles == 8
    assert_registers(gb, A=0x00, H=0x10, L=0x10, F=0b10110000)
    assert_memory(gb, {0x1010:0x0F})

    gb.cpu.register.A = 0xFE
    gb.memory.write_8bit(0x1010, 0x01)
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8e(gb)
    assert cycles == 8
    assert_registers(gb, A=0x00, H=0x10, L=0x10, F=0b10110000)
    assert_memory(gb, {0x1010:0x01})

    gb.cpu.register.A = 0xFE
    gb.memory.write_8bit(0x1010, 0x02)
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8e(gb)
    assert cycles == 8
    assert_registers(gb, A=0x01, H=0x10, L=0x10, F=0b00110000)
    assert_memory(gb, {0x1010:0x02})


# noinspection PyShadowingNames
def test_code_8f(gb):
    """ ADC A,A - A=A+A+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    gb.cpu.register.A = 0x00
    gb.cpu.register.F = 0b00000000
    cycles = op.code_8f(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, F=0b10000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8f(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, F=0b00000000)

    gb.cpu.register.A = 0x01
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8f(gb)
    assert cycles == 4
    assert_registers(gb, A=0x03, F=0b00000000)

    gb.cpu.register.A = 0x08
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8f(gb)
    assert cycles == 4
    assert_registers(gb, A=0x11, F=0b00100000)

    gb.cpu.register.A = 0x80
    gb.cpu.register.F = 0b00000000
    cycles = op.code_8f(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, F=0b10010000)

    gb.cpu.register.A = 0x80
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8f(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, F=0b00010000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.F = 0b00010000
    cycles = op.code_8f(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFF, F=0b00110000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_90(gb):
    """ SUB A,B - A=A-B """
    gb.cpu.register.A = 0x00
    gb.cpu.register.B = 0x00
    cycles = op.code_90(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, B=0x00, F=0b11000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.B = 0x01
    cycles = op.code_90(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFF, B=0x01, F=0b01110000)

    gb.cpu.register.A = 0x0F
    gb.cpu.register.B = 0x01
    cycles = op.code_90(gb)
    assert cycles == 4
    assert_registers(gb, A=0x0E, B=0x01, F=0b01000000)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.B = 0x10
    cycles = op.code_90(gb)
    assert cycles == 4
    assert_registers(gb, A=0xE0, B=0x10, F=0b01000000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.B = 0x01
    cycles = op.code_90(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFE, B=0x01, F=0b01000000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.B = 0xFE
    cycles = op.code_90(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, B=0xFE, F=0b01000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_91(gb):
    """ SUB A,C - A=A-C """
    gb.cpu.register.A = 0x00
    gb.cpu.register.C = 0x00
    cycles = op.code_91(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, C=0x00, F=0b11000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.C = 0x01
    cycles = op.code_91(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFF, C=0x01, F=0b01110000)

    gb.cpu.register.A = 0x0F
    gb.cpu.register.C = 0x01
    cycles = op.code_91(gb)
    assert cycles == 4
    assert_registers(gb, A=0x0E, C=0x01, F=0b01000000)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.C = 0x10
    cycles = op.code_91(gb)
    assert cycles == 4
    assert_registers(gb, A=0xE0, C=0x10, F=0b01000000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.C = 0x01
    cycles = op.code_91(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFE, C=0x01, F=0b01000000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.C = 0xFE
    cycles = op.code_91(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, C=0xFE, F=0b01000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_92(gb):
    """ SUB A,D - A=A-D """
    gb.cpu.register.A = 0x00
    gb.cpu.register.D = 0x00
    cycles = op.code_92(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, D=0x00, F=0b11000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.D = 0x01
    cycles = op.code_92(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFF, D=0x01, F=0b01110000)

    gb.cpu.register.A = 0x0F
    gb.cpu.register.D = 0x01
    cycles = op.code_92(gb)
    assert cycles == 4
    assert_registers(gb, A=0x0E, D=0x01, F=0b01000000)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.D = 0x10
    cycles = op.code_92(gb)
    assert cycles == 4
    assert_registers(gb, A=0xE0, D=0x10, F=0b01000000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.D = 0x01
    cycles = op.code_92(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFE, D=0x01, F=0b01000000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.D = 0xFE
    cycles = op.code_92(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, D=0xFE, F=0b01000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_93(gb):
    """ SUB A,E - A=A-E """
    gb.cpu.register.A = 0x00
    gb.cpu.register.E = 0x00
    cycles = op.code_93(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, E=0x00, F=0b11000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.E = 0x01
    cycles = op.code_93(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFF, E=0x01, F=0b01110000)

    gb.cpu.register.A = 0x0F
    gb.cpu.register.E = 0x01
    cycles = op.code_93(gb)
    assert cycles == 4
    assert_registers(gb, A=0x0E, E=0x01, F=0b01000000)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.E = 0x10
    cycles = op.code_93(gb)
    assert cycles == 4
    assert_registers(gb, A=0xE0, E=0x10, F=0b01000000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.E = 0x01
    cycles = op.code_93(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFE, E=0x01, F=0b01000000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.E = 0xFE
    cycles = op.code_93(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, E=0xFE, F=0b01000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_94(gb):
    """ SUB A,H - A=A-H """
    gb.cpu.register.A = 0x00
    gb.cpu.register.H = 0x00
    cycles = op.code_94(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, H=0x00, F=0b11000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.H = 0x01
    cycles = op.code_94(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFF, H=0x01, F=0b01110000)

    gb.cpu.register.A = 0x0F
    gb.cpu.register.H = 0x01
    cycles = op.code_94(gb)
    assert cycles == 4
    assert_registers(gb, A=0x0E, H=0x01, F=0b01000000)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.H = 0x10
    cycles = op.code_94(gb)
    assert cycles == 4
    assert_registers(gb, A=0xE0, H=0x10, F=0b01000000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.H = 0x01
    cycles = op.code_94(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFE, H=0x01, F=0b01000000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.H = 0xFE
    cycles = op.code_94(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, H=0xFE, F=0b01000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_95(gb):
    """ SUB A,L - A=A-L """
    gb.cpu.register.A = 0x00
    gb.cpu.register.L = 0x00
    cycles = op.code_95(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, L=0x00, F=0b11000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.L = 0x01
    cycles = op.code_95(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFF, L=0x01, F=0b01110000)

    gb.cpu.register.A = 0x0F
    gb.cpu.register.L = 0x01
    cycles = op.code_95(gb)
    assert cycles == 4
    assert_registers(gb, A=0x0E, L=0x01, F=0b01000000)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.L = 0x10
    cycles = op.code_95(gb)
    assert cycles == 4
    assert_registers(gb, A=0xE0, L=0x10, F=0b01000000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.L = 0x01
    cycles = op.code_95(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFE, L=0x01, F=0b01000000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.L = 0xFE
    cycles = op.code_95(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, L=0xFE, F=0b01000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_96(gb):
    """ SUB A,(HL) - A=A-(value at address HL) """
    gb.cpu.register.set_hl(0x1010)

    gb.cpu.register.A = 0x00
    gb.memory.write_8bit(0x1010, 0x00)
    cycles = op.code_96(gb)
    assert cycles == 8
    assert_registers(gb, A=0x00, H=0x10, L=0x10, F=0b11000000)
    assert_memory(gb)

    gb.cpu.register.A = 0x00
    gb.memory.write_8bit(0x1010, 0x01)
    cycles = op.code_96(gb)
    assert cycles == 8
    assert_registers(gb, A=0xFF, H=0x10, L=0x10, F=0b01110000)
    assert_memory(gb,{0x1010:0x01})

    gb.cpu.register.A = 0x0F
    gb.memory.write_8bit(0x1010, 0x01)
    cycles = op.code_96(gb)
    assert cycles == 8
    assert_registers(gb, A=0x0E, H=0x10, L=0x10, F=0b01000000)
    assert_memory(gb, {0x1010: 0x01})

    gb.cpu.register.A = 0xF0
    gb.memory.write_8bit(0x1010, 0x10)
    cycles = op.code_96(gb)
    assert cycles == 8
    assert_registers(gb, A=0xE0, H=0x10, L=0x10, F=0b01000000)
    assert_memory(gb, {0x1010: 0x10})

    gb.cpu.register.A = 0xFF
    gb.memory.write_8bit(0x1010, 0x01)
    cycles = op.code_96(gb)
    assert cycles == 8
    assert_registers(gb, A=0xFE, H=0x10, L=0x10, F=0b01000000)
    assert_memory(gb, {0x1010: 0x01})

    gb.cpu.register.A = 0xFF
    gb.memory.write_8bit(0x1010, 0xFE)
    cycles = op.code_96(gb)
    assert cycles == 8
    assert_registers(gb, A=0x01, H=0x10, L=0x10, F=0b01000000)
    assert_memory(gb, {0x1010: 0xFE})


# noinspection PyShadowingNames
def test_code_97(gb):
    """ SUB A,A - A=A-A """
    gb.cpu.register.A = 0x00
    cycles = op.code_97(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, F=0b11000000)

    gb.cpu.register.A = 0x01
    cycles = op.code_97(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, F=0b11000000)

    gb.cpu.register.A = 0xFF
    cycles = op.code_97(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, F=0b11000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_98(gb):
    """ SBC A,B - A=A-B-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    gb.cpu.register.A = 0x00
    gb.cpu.register.B = 0x00
    gb.cpu.register.F = 0b00000000
    cycles = op.code_98(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, B=0x00, F=0b11000000)

    gb.cpu.register.A = 0x02
    gb.cpu.register.B = 0x00
    gb.cpu.register.F = 0b00010000
    cycles = op.code_98(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, B=0x00, F=0b01000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.B = 0x01
    gb.cpu.register.F = 0b00010000
    cycles = op.code_98(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFE, B=0x01, F=0b01110000)

    gb.cpu.register.A = 0x13
    gb.cpu.register.B = 0x04
    gb.cpu.register.F = 0b00010000
    cycles = op.code_98(gb)
    assert cycles == 4
    assert_registers(gb, A=0x0E, B=0x04, F=0b01100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_99(gb):
    """ SBC A,C - A=A-C-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    gb.cpu.register.A = 0x00
    gb.cpu.register.C = 0x00
    gb.cpu.register.F = 0b00000000
    cycles = op.code_99(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, C=0x00, F=0b11000000)

    gb.cpu.register.A = 0x02
    gb.cpu.register.C = 0x00
    gb.cpu.register.F = 0b00010000
    cycles = op.code_99(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, C=0x00, F=0b01000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.C = 0x01
    gb.cpu.register.F = 0b00010000
    cycles = op.code_99(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFE, C=0x01, F=0b01110000)

    gb.cpu.register.A = 0x13
    gb.cpu.register.C = 0x04
    gb.cpu.register.F = 0b00010000
    cycles = op.code_99(gb)
    assert cycles == 4
    assert_registers(gb, A=0x0E, C=0x04, F=0b01100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_9a(gb):
    """ SBC A,D - A=A-D-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    gb.cpu.register.A = 0x00
    gb.cpu.register.D = 0x00
    gb.cpu.register.F = 0b00000000
    cycles = op.code_9a(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, D=0x00, F=0b11000000)

    gb.cpu.register.A = 0x02
    gb.cpu.register.D = 0x00
    gb.cpu.register.F = 0b00010000
    cycles = op.code_9a(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, D=0x00, F=0b01000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.D = 0x01
    gb.cpu.register.F = 0b00010000
    cycles = op.code_9a(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFE, D=0x01, F=0b01110000)

    gb.cpu.register.A = 0x13
    gb.cpu.register.D = 0x04
    gb.cpu.register.F = 0b00010000
    cycles = op.code_9a(gb)
    assert cycles == 4
    assert_registers(gb, A=0x0E, D=0x04, F=0b01100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_9b(gb):
    """ SBC A,E - A=A-E-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    gb.cpu.register.A = 0x00
    gb.cpu.register.E = 0x00
    gb.cpu.register.F = 0b00000000
    cycles = op.code_9b(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, E=0x00, F=0b11000000)

    gb.cpu.register.A = 0x02
    gb.cpu.register.E = 0x00
    gb.cpu.register.F = 0b00010000
    cycles = op.code_9b(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, E=0x00, F=0b01000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.E = 0x01
    gb.cpu.register.F = 0b00010000
    cycles = op.code_9b(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFE, E=0x01, F=0b01110000)

    gb.cpu.register.A = 0x13
    gb.cpu.register.E = 0x04
    gb.cpu.register.F = 0b00010000
    cycles = op.code_9b(gb)
    assert cycles == 4
    assert_registers(gb, A=0x0E, E=0x04, F=0b01100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_9c(gb):
    """ SBC A,H - A=A-H-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    gb.cpu.register.A = 0x00
    gb.cpu.register.H = 0x00
    gb.cpu.register.F = 0b00000000
    cycles = op.code_9c(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, H=0x00, F=0b11000000)

    gb.cpu.register.A = 0x02
    gb.cpu.register.H = 0x00
    gb.cpu.register.F = 0b00010000
    cycles = op.code_9c(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, H=0x00, F=0b01000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.H = 0x01
    gb.cpu.register.F = 0b00010000
    cycles = op.code_9c(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFE, H=0x01, F=0b01110000)

    gb.cpu.register.A = 0x13
    gb.cpu.register.H = 0x04
    gb.cpu.register.F = 0b00010000
    cycles = op.code_9c(gb)
    assert cycles == 4
    assert_registers(gb, A=0x0E, H=0x04, F=0b01100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_9d(gb):
    """ SBC A,L - A=A-L-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    gb.cpu.register.A = 0x00
    gb.cpu.register.L = 0x00
    gb.cpu.register.F = 0b00000000
    cycles = op.code_9d(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, L=0x00, F=0b11000000)

    gb.cpu.register.A = 0x02
    gb.cpu.register.L = 0x00
    gb.cpu.register.F = 0b00010000
    cycles = op.code_9d(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, L=0x00, F=0b01000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.L = 0x01
    gb.cpu.register.F = 0b00010000
    cycles = op.code_9d(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFE, L=0x01, F=0b01110000)

    gb.cpu.register.A = 0x13
    gb.cpu.register.L = 0x04
    gb.cpu.register.F = 0b00010000
    cycles = op.code_9d(gb)
    assert cycles == 4
    assert_registers(gb, A=0x0E, L=0x04, F=0b01100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_9e(gb):
    """ SBC A,(HL) - A=A-(value at address HL)-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    gb.cpu.register.set_hl(0x1010)

    gb.cpu.register.A = 0x00
    gb.memory.write_8bit(0x1010, 0x00)
    gb.cpu.register.F = 0b00000000
    cycles = op.code_9e(gb)
    assert cycles == 8
    assert_registers(gb, A=0x00, H=0x10, L=0x10, F=0b11000000)
    assert_memory(gb)

    gb.cpu.register.A = 0x02
    gb.memory.write_8bit(0x1010, 0x00)
    gb.cpu.register.F = 0b00010000
    cycles = op.code_9e(gb)
    assert cycles == 8
    assert_registers(gb, A=0x01, H=0x10, L=0x10, F=0b01000000)
    assert_memory(gb)

    gb.cpu.register.A = 0x00
    gb.memory.write_8bit(0x1010, 0x01)
    gb.cpu.register.F = 0b00010000
    cycles = op.code_9e(gb)
    assert cycles == 8
    assert_registers(gb, A=0xFE, H=0x10, L=0x10, F=0b01110000)
    assert_memory(gb,{0x1010:0x01})

    gb.cpu.register.A = 0x13
    gb.memory.write_8bit(0x1010, 0x04)
    gb.cpu.register.F = 0b00010000
    cycles = op.code_9e(gb)
    assert cycles == 8
    assert_registers(gb, A=0x0E, H=0x10, L=0x10, F=0b01100000)
    assert_memory(gb, {0x1010: 0x04})


# noinspection PyShadowingNames
def test_code_9f(gb):
    """ SBC A,A - A=A-A-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    gb.cpu.register.A = 0x00
    gb.cpu.register.F = 0b00000000
    cycles = op.code_9f(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, F=0b11000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.F = 0b00010000
    cycles = op.code_9f(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFF, F=0b01110000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.F = 0b00010000
    cycles = op.code_9f(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFF, F=0b01110000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_a0(gb):
    """ AND B - A=Logical AND A with B """
    gb.cpu.register.A = 0b10100011
    gb.cpu.register.B = 0b01000100
    cycles = op.code_a0(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000000, B=0b01000100, F=0b10100000)

    gb.cpu.register.A = 0b10100011
    gb.cpu.register.B = 0b01100110
    cycles = op.code_a0(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00100010, B=0b01100110, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_a1(gb):
    """ AND C - A=Logical AND A with C """
    gb.cpu.register.A = 0b10100011
    gb.cpu.register.C = 0b01000100
    cycles = op.code_a1(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000000, C=0b01000100, F=0b10100000)

    gb.cpu.register.A = 0b10100011
    gb.cpu.register.C = 0b01100110
    cycles = op.code_a1(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00100010, C=0b01100110, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_a2(gb):
    """ AND D - A=Logical AND A with D """
    gb.cpu.register.A = 0b10100011
    gb.cpu.register.D = 0b01000100
    cycles = op.code_a2(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000000, D=0b01000100, F=0b10100000)

    gb.cpu.register.A = 0b10100011
    gb.cpu.register.D = 0b01100110
    cycles = op.code_a2(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00100010, D=0b01100110, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_a3(gb):
    """ AND E - A=Logical AND A with E """
    gb.cpu.register.A = 0b10100011
    gb.cpu.register.E = 0b01000100
    cycles = op.code_a3(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000000, E=0b01000100, F=0b10100000)

    gb.cpu.register.A = 0b10100011
    gb.cpu.register.E = 0b01100110
    cycles = op.code_a3(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00100010, E=0b01100110, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_a4(gb):
    """ AND H - A=Logical AND A with H """
    gb.cpu.register.A = 0b10100011
    gb.cpu.register.H = 0b01000100
    cycles = op.code_a4(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000000, H=0b01000100, F=0b10100000)

    gb.cpu.register.A = 0b10100011
    gb.cpu.register.H = 0b01100110
    cycles = op.code_a4(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00100010, H=0b01100110, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_a5(gb):
    """ AND L - A=Logical AND A with L """
    gb.cpu.register.A = 0b10100011
    gb.cpu.register.L = 0b01000100
    cycles = op.code_a5(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000000, L=0b01000100, F=0b10100000)

    gb.cpu.register.A = 0b10100011
    gb.cpu.register.L = 0b01100110
    cycles = op.code_a5(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00100010, L=0b01100110, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_a6(gb):
    """ AND (HL) - A=Logical AND A with (value at address HL) """
    gb.cpu.register.set_hl(0x1010)

    gb.cpu.register.A = 0b10100011
    gb.memory.write_8bit(0x1010,0b01000100)
    cycles = op.code_a6(gb)
    assert cycles == 8
    assert_registers(gb, A=0b00000000, H=0x10, L=0x10, F=0b10100000)

    gb.cpu.register.A = 0b10100011
    gb.memory.write_8bit(0x1010, 0b01100110)
    cycles = op.code_a6(gb)
    assert cycles == 8
    assert_registers(gb, A=0b00100010, H=0x10, L=0x10, F=0b00100000)


# noinspection PyShadowingNames
def test_code_a7(gb):
    """ AND A - A=Logical AND A with A (why?) """
    gb.cpu.register.A = 0b00000000
    cycles = op.code_a7(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000000, F=0b10100000)

    gb.cpu.register.A = 0b00100011
    cycles = op.code_a7(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00100011, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_a8(gb):
    """ XOR B - A=Logical XOR A with B """
    gb.cpu.register.A = 0b10100011
    gb.cpu.register.B = 0b10100011
    cycles = op.code_a8(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000000, B=0b10100011, F=0b10000000)

    gb.cpu.register.A = 0b10100011
    gb.cpu.register.B = 0b01100110
    cycles = op.code_a8(gb)
    assert cycles == 4
    assert_registers(gb, A=0b11000101, B=0b01100110, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_a9(gb):
    """ XOR C - A=Logical XOR A with C """
    gb.cpu.register.A = 0b10100011
    gb.cpu.register.C = 0b10100011
    cycles = op.code_a9(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000000, C=0b10100011, F=0b10000000)

    gb.cpu.register.A = 0b10100011
    gb.cpu.register.C = 0b01100110
    cycles = op.code_a9(gb)
    assert cycles == 4
    assert_registers(gb, A=0b11000101, C=0b01100110, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_aa(gb):
    """ XOR D - A=Logical XOR A with D """
    gb.cpu.register.A = 0b10100011
    gb.cpu.register.D = 0b10100011
    cycles = op.code_aa(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000000, D=0b10100011, F=0b10000000)

    gb.cpu.register.A = 0b10100011
    gb.cpu.register.D = 0b01100110
    cycles = op.code_aa(gb)
    assert cycles == 4
    assert_registers(gb, A=0b11000101, D=0b01100110, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_ab(gb):
    """ XOR E - A=Logical XOR A with E """
    gb.cpu.register.A = 0b10100011
    gb.cpu.register.E = 0b10100011
    cycles = op.code_ab(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000000, E=0b10100011, F=0b10000000)

    gb.cpu.register.A = 0b10100011
    gb.cpu.register.E = 0b01100110
    cycles = op.code_ab(gb)
    assert cycles == 4
    assert_registers(gb, A=0b11000101, E=0b01100110, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_ac(gb):
    """ XOR H - A=Logical XOR A with H """
    gb.cpu.register.A = 0b10100011
    gb.cpu.register.H = 0b10100011
    cycles = op.code_ac(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000000, H=0b10100011, F=0b10000000)

    gb.cpu.register.A = 0b10100011
    gb.cpu.register.H = 0b01100110
    cycles = op.code_ac(gb)
    assert cycles == 4
    assert_registers(gb, A=0b11000101, H=0b01100110, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_ad(gb):
    """ XOR L - A=Logical XOR A with L """
    gb.cpu.register.A = 0b10100011
    gb.cpu.register.L = 0b10100011
    cycles = op.code_ad(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000000, L=0b10100011, F=0b10000000)

    gb.cpu.register.A = 0b10100011
    gb.cpu.register.L = 0b01100110
    cycles = op.code_ad(gb)
    assert cycles == 4
    assert_registers(gb, A=0b11000101, L=0b01100110, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_ae(gb):
    """ XOR (HL) - A=Logical XOR A with (value at address HL) """
    gb.cpu.register.set_hl(0x1010)

    gb.cpu.register.A = 0b10100011
    gb.memory.write_8bit(0x1010, 0b10100011)
    cycles = op.code_ae(gb)
    assert cycles == 8
    assert_registers(gb, A=0b00000000, H=0x10, L=0x10, F=0b10000000)
    assert_memory(gb,{0x1010:0b10100011})

    gb.cpu.register.A = 0b10100011
    gb.memory.write_8bit(0x1010, 0b01100110)
    cycles = op.code_ae(gb)
    assert cycles == 8
    assert_registers(gb, A=0b11000101, H=0x10, L=0x10, F=0b00000000)
    assert_memory(gb, {0x1010: 0b01100110})


# noinspection PyShadowingNames
def test_code_af(gb):
    """ XOR A - A=Logical XOR A with A """
    gb.cpu.register.A = 0b10100011
    cycles = op.code_af(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000000, F=0b10000000)

    gb.cpu.register.A = 0b10100011
    cycles = op.code_af(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000000, F=0b10000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_b0(gb):
    """ OR B - A=Logical OR A with B """
    gb.cpu.register.A = 0b00000000
    gb.cpu.register.B = 0b00000000
    cycles = op.code_b0(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000000, B=0b00000000, F=0b10000000)

    gb.cpu.register.A = 0b10100011
    gb.cpu.register.B = 0b01100110
    cycles = op.code_b0(gb)
    assert cycles == 4
    assert_registers(gb, A=0b11100111, B=0b01100110, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_b1(gb):
    """ OR C - A=Logical OR A with C """
    gb.cpu.register.A = 0b00000000
    gb.cpu.register.C = 0b00000000
    cycles = op.code_b1(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000000, C=0b00000000, F=0b10000000)

    gb.cpu.register.A = 0b10100011
    gb.cpu.register.C = 0b01100110
    cycles = op.code_b1(gb)
    assert cycles == 4
    assert_registers(gb, A=0b11100111, C=0b01100110, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_b2(gb):
    """ OR D - A=Logical OR A with D """
    gb.cpu.register.A = 0b00000000
    gb.cpu.register.D = 0b00000000
    cycles = op.code_b2(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000000, D=0b00000000, F=0b10000000)

    gb.cpu.register.A = 0b10100011
    gb.cpu.register.D = 0b01100110
    cycles = op.code_b2(gb)
    assert cycles == 4
    assert_registers(gb, A=0b11100111, D=0b01100110, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_b3(gb):
    """ OR E - A=Logical OR A with E """
    gb.cpu.register.A = 0b00000000
    gb.cpu.register.E = 0b00000000
    cycles = op.code_b3(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000000, E=0b00000000, F=0b10000000)

    gb.cpu.register.A = 0b10100011
    gb.cpu.register.E = 0b01100110
    cycles = op.code_b3(gb)
    assert cycles == 4
    assert_registers(gb, A=0b11100111, E=0b01100110, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_b4(gb):
    """ OR H - A=Logical OR A with H """
    gb.cpu.register.A = 0b00000000
    gb.cpu.register.H = 0b00000000
    cycles = op.code_b4(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000000, H=0b00000000, F=0b10000000)

    gb.cpu.register.A = 0b10100011
    gb.cpu.register.H = 0b01100110
    cycles = op.code_b4(gb)
    assert cycles == 4
    assert_registers(gb, A=0b11100111, H=0b01100110, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_b5(gb):
    """ OR L - A=Logical OR A with L """
    gb.cpu.register.A = 0b00000000
    gb.cpu.register.L = 0b00000000
    cycles = op.code_b5(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000000, L=0b00000000, F=0b10000000)

    gb.cpu.register.A = 0b10100011
    gb.cpu.register.L = 0b01100110
    cycles = op.code_b5(gb)
    assert cycles == 4
    assert_registers(gb, A=0b11100111, L=0b01100110, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_b6(gb):
    """ OR (HL) - A=Logical OR A with (value at address HL) """
    gb.cpu.register.set_hl(0x1010)

    gb.cpu.register.A = 0b00000000
    gb.memory.write_8bit(0x1010,0b00000000)
    cycles = op.code_b6(gb)
    assert cycles == 8
    assert_registers(gb, A=0b00000000, H=0x10, L=0x10, F=0b10000000)
    assert_memory(gb)

    gb.cpu.register.A = 0b10100011
    gb.memory.write_8bit(0x1010,0b01100110)
    cycles = op.code_b6(gb)
    assert cycles == 8
    assert_registers(gb, A=0b11100111, H=0x10, L=0x10, F=0b00000000)
    assert_memory(gb,{0x1010:0b01100110})


# noinspection PyShadowingNames
def test_code_b7(gb):
    """ OR L - A=Logical OR A with A (why?) """
    gb.cpu.register.A = 0b00000000
    cycles = op.code_b7(gb)
    assert cycles == 4
    assert_registers(gb, A=0b00000000, F=0b10000000)

    gb.cpu.register.A = 0b10100011
    cycles = op.code_b7(gb)
    assert cycles == 4
    assert_registers(gb, A=0b10100011, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_b8(gb):
    """ CP A,B - same as SUB A,B but throw the result away, only set flags """
    gb.cpu.register.A = 0x00
    gb.cpu.register.B = 0x00
    cycles = op.code_b8(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, B=0x00, F=0b11000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.B = 0x01
    cycles = op.code_b8(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, B=0x01, F=0b01110000)

    gb.cpu.register.A = 0x0F
    gb.cpu.register.B = 0x01
    cycles = op.code_b8(gb)
    assert cycles == 4
    assert_registers(gb, A=0x0F, B=0x01, F=0b01000000)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.B = 0x10
    cycles = op.code_b8(gb)
    assert cycles == 4
    assert_registers(gb, A=0xF0, B=0x10, F=0b01000000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.B = 0x01
    cycles = op.code_b8(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFF, B=0x01, F=0b01000000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.B = 0xFE
    cycles = op.code_b8(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFF, B=0xFE, F=0b01000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_b9(gb):
    """ CP A,C - same as SUB A,C but throw the result away, only set flags """
    gb.cpu.register.A = 0x00
    gb.cpu.register.C = 0x00
    cycles = op.code_b9(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, C=0x00, F=0b11000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.C = 0x01
    cycles = op.code_b9(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, C=0x01, F=0b01110000)

    gb.cpu.register.A = 0x0F
    gb.cpu.register.C = 0x01
    cycles = op.code_b9(gb)
    assert cycles == 4
    assert_registers(gb, A=0x0F, C=0x01, F=0b01000000)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.C = 0x10
    cycles = op.code_b9(gb)
    assert cycles == 4
    assert_registers(gb, A=0xF0, C=0x10, F=0b01000000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.C = 0x01
    cycles = op.code_b9(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFF, C=0x01, F=0b01000000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.C = 0xFE
    cycles = op.code_b9(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFF, C=0xFE, F=0b01000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_ba(gb):
    """ CP A,D - same as SUB A,D but throw the result away, only set flags """
    gb.cpu.register.A = 0x00
    gb.cpu.register.D = 0x00
    cycles = op.code_ba(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, D=0x00, F=0b11000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.D = 0x01
    cycles = op.code_ba(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, D=0x01, F=0b01110000)

    gb.cpu.register.A = 0x0F
    gb.cpu.register.D = 0x01
    cycles = op.code_ba(gb)
    assert cycles == 4
    assert_registers(gb, A=0x0F, D=0x01, F=0b01000000)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.D = 0x10
    cycles = op.code_ba(gb)
    assert cycles == 4
    assert_registers(gb, A=0xF0, D=0x10, F=0b01000000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.D = 0x01
    cycles = op.code_ba(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFF, D=0x01, F=0b01000000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.D = 0xFE
    cycles = op.code_ba(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFF, D=0xFE, F=0b01000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_bb(gb):
    """ CP A,E - same as SUB A,E but throw the result away, only set flags """
    gb.cpu.register.A = 0x00
    gb.cpu.register.E = 0x00
    cycles = op.code_bb(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, E=0x00, F=0b11000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.E = 0x01
    cycles = op.code_bb(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, E=0x01, F=0b01110000)

    gb.cpu.register.A = 0x0F
    gb.cpu.register.E = 0x01
    cycles = op.code_bb(gb)
    assert cycles == 4
    assert_registers(gb, A=0x0F, E=0x01, F=0b01000000)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.E = 0x10
    cycles = op.code_bb(gb)
    assert cycles == 4
    assert_registers(gb, A=0xF0, E=0x10, F=0b01000000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.E = 0x01
    cycles = op.code_bb(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFF, E=0x01, F=0b01000000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.E = 0xFE
    cycles = op.code_bb(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFF, E=0xFE, F=0b01000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_bc(gb):
    """ CP A,H - same as SUB A,H but throw the result away, only set flags """
    gb.cpu.register.A = 0x00
    gb.cpu.register.H = 0x00
    cycles = op.code_bc(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, H=0x00, F=0b11000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.H = 0x01
    cycles = op.code_bc(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, H=0x01, F=0b01110000)

    gb.cpu.register.A = 0x0F
    gb.cpu.register.H = 0x01
    cycles = op.code_bc(gb)
    assert cycles == 4
    assert_registers(gb, A=0x0F, H=0x01, F=0b01000000)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.H = 0x10
    cycles = op.code_bc(gb)
    assert cycles == 4
    assert_registers(gb, A=0xF0, H=0x10, F=0b01000000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.H = 0x01
    cycles = op.code_bc(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFF, H=0x01, F=0b01000000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.H = 0xFE
    cycles = op.code_bc(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFF, H=0xFE, F=0b01000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_bd(gb):
    """ CP A,L - same as SUB A,L but throw the result away, only set flags """
    gb.cpu.register.A = 0x00
    gb.cpu.register.L = 0x00
    cycles = op.code_bd(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, L=0x00, F=0b11000000)

    gb.cpu.register.A = 0x00
    gb.cpu.register.L = 0x01
    cycles = op.code_bd(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, L=0x01, F=0b01110000)

    gb.cpu.register.A = 0x0F
    gb.cpu.register.L = 0x01
    cycles = op.code_bd(gb)
    assert cycles == 4
    assert_registers(gb, A=0x0F, L=0x01, F=0b01000000)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.L = 0x10
    cycles = op.code_bd(gb)
    assert cycles == 4
    assert_registers(gb, A=0xF0, L=0x10, F=0b01000000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.L = 0x01
    cycles = op.code_bd(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFF, L=0x01, F=0b01000000)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.L = 0xFE
    cycles = op.code_bd(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFF, L=0xFE, F=0b01000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_be(gb):
    """ CP A,(HL) - same as SUB A,(HL) but throw the result away, only set flags """
    gb.cpu.register.set_hl(0x1010)

    gb.cpu.register.A = 0x00
    gb.memory.write_8bit(0x1010,0x00)
    cycles = op.code_be(gb)
    assert cycles == 8
    assert_registers(gb, A=0x00, H=0x10, L=0x10, F=0b11000000)
    assert_memory(gb)

    gb.cpu.register.A = 0x00
    gb.memory.write_8bit(0x1010, 0x01)
    cycles = op.code_be(gb)
    assert cycles == 8
    assert_registers(gb, A=0x00, H=0x10, L=0x10, F=0b01110000)
    assert_memory(gb, {0x1010:0x01})

    gb.cpu.register.A = 0x0F
    gb.memory.write_8bit(0x1010, 0x01)
    cycles = op.code_be(gb)
    assert cycles == 8
    assert_registers(gb, A=0x0F, H=0x10, L=0x10, F=0b01000000)
    assert_memory(gb, {0x1010: 0x01})

    gb.cpu.register.A = 0xF0
    gb.memory.write_8bit(0x1010, 0x10)
    cycles = op.code_be(gb)
    assert cycles == 8
    assert_registers(gb, A=0xF0, H=0x10, L=0x10, F=0b01000000)
    assert_memory(gb, {0x1010: 0x10})

    gb.cpu.register.A = 0xFF
    gb.memory.write_8bit(0x1010, 0x01)
    cycles = op.code_be(gb)
    assert cycles == 8
    assert_registers(gb, A=0xFF, H=0x10, L=0x10, F=0b01000000)
    assert_memory(gb, {0x1010: 0x01})

    gb.cpu.register.A = 0xFF
    gb.memory.write_8bit(0x1010, 0xFE)
    cycles = op.code_be(gb)
    assert cycles == 8
    assert_registers(gb, A=0xFF, H=0x10, L=0x10, F=0b01000000)
    assert_memory(gb, {0x1010: 0xFE})


# noinspection PyShadowingNames
def test_code_bf(gb):
    """ CP A,A - same as SUB A,A but throw the result away, only set flags """
    gb.cpu.register.A = 0x00
    cycles = op.code_bf(gb)
    assert cycles == 4
    assert_registers(gb, A=0x00, F=0b11000000)

    gb.cpu.register.A = 0x01
    cycles = op.code_bf(gb)
    assert cycles == 4
    assert_registers(gb, A=0x01, F=0b11000000)

    gb.cpu.register.A = 0xFF
    cycles = op.code_bf(gb)
    assert cycles == 4
    assert_registers(gb, A=0xFF, F=0b11000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_c0(gb):
    """ RET NZ - Return if flag Z is reset """
    gb.memory.write_8bit(0x1010, 0x50)
    gb.memory.write_8bit(0x1011, 0x40)

    gb.cpu.register.SP = 0x1010
    gb.cpu.register.PC = 0x0000
    gb.cpu.register.F = 0b00000000
    cycles = op.code_c0(gb)
    assert cycles == 20
    assert_registers(gb, SP=0x1012, PC=0x4050)

    gb.cpu.register.SP = 0x1010
    gb.cpu.register.PC = 0x0000
    gb.cpu.register.F = 0b10000000
    cycles = op.code_c0(gb)
    assert cycles == 8
    assert_registers(gb, SP=0x1010, PC=0x0000, F=0b10000000)

    assert_memory(gb,{0x1010:0x50, 0x1011:0x40})


# noinspection PyShadowingNames
def test_code_c1(gb):
    """ POP BC - Copy 16-bit value from stack (i.e. SP address) into BC, then increment SP by 2 """
    gb.memory.write_16bit(0xFFFC,0x9933)
    gb.cpu.register.SP = 0xFFFC
    cycles = op.code_c1(gb)
    assert cycles == 12
    assert_registers(gb, B=0x99, C=0x33, SP=0xFFFE)
    assert_memory(gb,{0xFFFD:0x99,0xFFFC:0x33})


# noinspection PyShadowingNames
def test_code_c2(gb):
    """ JP NZ,a16 - Jump to address a16 if Z flag is reset """
    gb.cpu._cartridge_data = bytes.fromhex("FF 55")
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu.register.F = 0b00000000
    cycles = op.code_c2(gb)
    assert cycles == 16
    assert_registers(gb, PC=0x55FF)

    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu.register.F = 0b10000000
    cycles = op.code_c2(gb)
    assert cycles == 12
    assert_registers(gb, PC=0x0002, F=0b10000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_c3(gb):
    """ JP a16 - Jump to address a16 """
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("FF 55")
    cycles = op.code_c3(gb)
    assert cycles == 16
    assert_registers(gb, PC=0x55FF)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_c4(gb):
    """ CALL NZ,a16 - Call address a16 if flag Z is reset """
    gb.cpu._cartridge_data = bytes.fromhex("FF 55")

    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu.register.SP = 0xFFFE
    gb.cpu.register.F = 0b00000000
    cycles = op.code_c4(gb)
    assert cycles == 24
    assert_registers(gb, PC=0x55FF, SP=0xFFFC)
    assert_memory(gb,{0xFFFC:0x02,0xFFFD:0x00})

    gb.memory.write_16bit(0xFFFC, 0x0000)  # To reset memory before next test
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu.register.SP = 0xFFFE
    gb.cpu.register.F = 0b10000000
    cycles = op.code_c4(gb)
    assert cycles == 12
    assert_registers(gb, PC=0x0002, SP=0xFFFE, F=0b10000000)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_c5(gb):
    """ PUSH BC - Decrement SP by 2 then push BC value onto stack (i.e. SP address) """
    gb.cpu.register.set_bc(0x1122)
    cycles = op.code_c5(gb)
    assert cycles == 16
    assert_registers(gb,B=0x11,C=0x22,SP=0xFFFC)
    assert_memory(gb,{0xFFFC:0x22,0xFFFD:0x11})


# noinspection PyShadowingNames
def test_code_c6(gb):
    """ ADD A,d8 - A=A+d8 """
    gb.cpu.register.A = 0x00
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("00")
    cycles = op.code_c6(gb)
    assert cycles == 8
    assert_registers(gb, A=0x00, F=0b10000000, PC=0x0001)

    gb.cpu.register.A = 0x00
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("01")
    cycles = op.code_c6(gb)
    assert cycles == 8
    assert_registers(gb, A=0x01, F=0b00000000, PC=0x0001)

    gb.cpu.register.A = 0x0F
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("01")
    cycles = op.code_c6(gb)
    assert cycles == 8
    assert_registers(gb, A=0x10, F=0b00100000, PC=0x0001)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("10")
    cycles = op.code_c6(gb)
    assert cycles == 8
    assert_registers(gb, A=0x00, F=0b10010000, PC=0x0001)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("01")
    cycles = op.code_c6(gb)
    assert cycles == 8
    assert_registers(gb, A=0x00, F=0b10110000, PC=0x0001)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("02")
    cycles = op.code_c6(gb)
    assert cycles == 8
    assert_registers(gb, A=0x01, F=0b00110000, PC=0x0001)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_c7(gb):
    """ RST 00H - Push present address onto stack, jump to address $0000 + 00H """
    gb.cpu.register.PC = 0x2233
    gb.cpu.register.SP = 0x1010
    cycles = op.code_c7(gb)
    assert cycles == 16
    assert_registers(gb, PC=0x0000, SP=0x100E)
    assert_memory(gb,{0x100F:0x22, 0x100E:0x33})


# noinspection PyShadowingNames
def test_code_c8(gb):
    """ RET Z - Return if flag Z is set """
    gb.memory.write_8bit(0x1010, 0x50)
    gb.memory.write_8bit(0x1011, 0x40)

    gb.cpu.register.SP = 0x1010
    gb.cpu.register.PC = 0x0000
    gb.cpu.register.F = 0b10000000
    cycles = op.code_c8(gb)
    assert cycles == 20
    assert_registers(gb, SP=0x1012, PC=0x4050, F=0b10000000)

    gb.cpu.register.SP = 0x1010
    gb.cpu.register.PC = 0x0000
    gb.cpu.register.F = 0b00000000
    cycles = op.code_c8(gb)
    assert cycles == 8
    assert_registers(gb, SP=0x1010, PC=0x0000)

    assert_memory(gb, {0x1010: 0x50, 0x1011: 0x40})


# noinspection PyShadowingNames
def test_code_c9(gb):
    """ RET - Pop two bytes from stack and jump to that address """
    gb.memory.write_8bit(0x1010, 0x50)
    gb.memory.write_8bit(0x1011, 0x40)

    gb.cpu.register.SP = 0x1010
    gb.cpu.register.PC = 0x0000
    cycles = op.code_c9(gb)
    assert cycles == 16
    assert_registers(gb, SP=0x1012, PC=0x4050)

    assert_memory(gb, {0x1010: 0x50, 0x1011: 0x40})


# noinspection PyShadowingNames
def test_code_ca(gb):
    """ JP Z,a16 - Jump to address a16 if Z flag is set """
    gb.cpu._cartridge_data = bytes.fromhex("FF 55")
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu.register.F = 0b10000000
    cycles = op.code_ca(gb)
    assert cycles == 16
    assert_registers(gb, PC=0x55FF, F=0b10000000)

    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu.register.F = 0b00000000
    cycles = op.code_ca(gb)
    assert cycles == 12
    assert_registers(gb, PC=0x0002)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb(gb):
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("40")
    gb.cpu.register.B = 0b00000001
    cycles = op.code_cb(gb)
    assert cycles == 12  # 4 from CB + 8 from CB_40
    assert_registers(gb,B=0b00000001,F=0b10100000,PC=0x0001)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cc(gb):
    """ CALL Z,a16 - Call address a16 if flag Z is set """
    gb.cpu._cartridge_data = bytes.fromhex("FF 55")

    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu.register.SP = 0xFFFE
    gb.cpu.register.F = 0b10000000
    cycles = op.code_cc(gb)
    assert cycles == 24
    assert_registers(gb, PC=0x55FF, SP=0xFFFC, F=0b10000000)
    assert_memory(gb, {0xFFFC: 0x02, 0xFFFD: 0x00})

    gb.memory.write_16bit(0xFFFC, 0x0000)  # To reset memory before next test
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu.register.SP = 0xFFFE
    gb.cpu.register.F = 0b00000000
    cycles = op.code_cc(gb)
    assert cycles == 12
    assert_registers(gb, PC=0x0002, SP=0xFFFE)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cd(gb):
    """ CALL a16 - Push address of next instruction onto stack then jump to address a16 """
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("FF 55")
    gb.cpu.register.SP = 0xFFFE
    cycles = op.code_cd(gb)
    assert cycles == 24
    assert_registers(gb, PC=0x55FF, SP=0xFFFC,)
    assert_memory(gb, {0xFFFC: 0x02, 0xFFFD: 0x00})


# noinspection PyShadowingNames
def test_code_ce(gb):
    """ ADC A,d8 - A=A+d8+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    gb.cpu.register.A = 0x00
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("00")
    gb.cpu.register.F = 0b00000000
    cycles = op.code_ce(gb)
    assert cycles == 8
    assert_registers(gb, A=0x00, F=0b10000000, PC=0x0001)

    gb.cpu.register.A = 0x00
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("00")
    gb.cpu.register.F = 0b00010000
    cycles = op.code_ce(gb)
    assert cycles == 8
    assert_registers(gb, A=0x01, F=0b00000000, PC=0x0001)

    gb.cpu.register.A = 0x00
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("01")
    gb.cpu.register.F = 0b00010000
    cycles = op.code_ce(gb)
    assert cycles == 8
    assert_registers(gb, A=0x02, F=0b00000000, PC=0x0001)

    gb.cpu.register.A = 0x0E
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("01")
    gb.cpu.register.F = 0b00010000
    cycles = op.code_ce(gb)
    assert cycles == 8
    assert_registers(gb, A=0x10, F=0b00100000, PC=0x0001)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("0F")
    gb.cpu.register.F = 0b00010000
    cycles = op.code_ce(gb)
    assert cycles == 8
    assert_registers(gb, A=0x00, F=0b10110000, PC=0x0001)

    gb.cpu.register.A = 0xFE
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("01")
    gb.cpu.register.F = 0b00010000
    cycles = op.code_ce(gb)
    assert cycles == 8
    assert_registers(gb, A=0x00, F=0b10110000, PC=0x0001)

    gb.cpu.register.A = 0xFE
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("02")
    gb.cpu.register.F = 0b00010000
    cycles = op.code_ce(gb)
    assert cycles == 8
    assert_registers(gb, A=0x01, F=0b00110000, PC=0x0001)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cf(gb):
    """ RST 08H - Push present address onto stack, jump to address $0000 + 08H """
    gb.cpu.register.PC = 0x2233
    gb.cpu.register.SP = 0x1010
    cycles = op.code_cf(gb)
    assert cycles == 16
    assert_registers(gb, PC=0x0008, SP=0x100E)
    assert_memory(gb, {0x100F: 0x22, 0x100E: 0x33})


# noinspection PyShadowingNames
def test_code_d0(gb):
    """ RET NC - Return if flag C is reset """
    gb.memory.write_8bit(0x1010, 0x50)
    gb.memory.write_8bit(0x1011, 0x40)

    gb.cpu.register.SP = 0x1010
    gb.cpu.register.PC = 0x0000
    gb.cpu.register.F = 0b00000000
    cycles = op.code_d0(gb)
    assert cycles == 20
    assert_registers(gb, SP=0x1012, PC=0x4050)

    gb.cpu.register.SP = 0x1010
    gb.cpu.register.PC = 0x0000
    gb.cpu.register.F = 0b00010000
    cycles = op.code_d0(gb)
    assert cycles == 8
    assert_registers(gb, SP=0x1010, PC=0x0000, F=0b00010000)

    assert_memory(gb, {0x1010: 0x50, 0x1011: 0x40})


# noinspection PyShadowingNames
def test_code_d1(gb):
    """ POP DE - Copy 16-bit value from stack (i.e. SP address) into DE, then increment SP by 2 """
    gb.memory.write_16bit(0xFFFC, 0x9933)
    gb.cpu.register.SP = 0xFFFC
    cycles = op.code_d1(gb)
    assert cycles == 12
    assert_registers(gb, D=0x99, E=0x33, SP=0xFFFE)
    assert_memory(gb, {0xFFFD: 0x99, 0xFFFC: 0x33})


# noinspection PyShadowingNames
def test_code_d2(gb):
    """ JP NC,a16 - Jump to address a16 if C flag is reset """
    gb.cpu._cartridge_data = bytes.fromhex("FF 55")
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu.register.F = 0b00000000
    cycles = op.code_d2(gb)
    assert cycles == 16
    assert_registers(gb, PC=0x55FF)

    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu.register.F = 0b00010000
    cycles = op.code_d2(gb)
    assert cycles == 12
    assert_registers(gb, PC=0x0002, F=0b00010000)

    assert_memory(gb)


# OPCODE D3 is unused


# noinspection PyShadowingNames
def test_code_d4(gb):
    """ CALL NC,a16 - Call address a16 if flag C is reset """
    gb.cpu._cartridge_data = bytes.fromhex("FF 55")

    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu.register.SP = 0xFFFE
    gb.cpu.register.F = 0b00000000
    cycles = op.code_d4(gb)
    assert cycles == 24
    assert_registers(gb, PC=0x55FF, SP=0xFFFC)
    assert_memory(gb, {0xFFFC: 0x02, 0xFFFD: 0x00})

    gb.memory.write_16bit(0xFFFC, 0x0000)  # To reset memory before next test
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu.register.SP = 0xFFFE
    gb.cpu.register.F = 0b00010000
    cycles = op.code_d4(gb)
    assert cycles == 12
    assert_registers(gb, PC=0x0002, SP=0xFFFE, F=0b00010000)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_d5(gb):
    """ PUSH DE - Decrement SP by 2 then push DE value onto stack (i.e. SP address) """
    gb.cpu.register.set_de(0x1122)
    cycles = op.code_d5(gb)
    assert cycles == 16
    assert_registers(gb, D=0x11, E=0x22, SP=0xFFFC)
    assert_memory(gb, {0xFFFC: 0x22, 0xFFFD: 0x11})


# noinspection PyShadowingNames
def test_code_d6(gb):
    """ SUB A,d8 - A=A-d8 """
    gb.cpu.register.A = 0x00
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("00")
    cycles = op.code_d6(gb)
    assert cycles == 8
    assert_registers(gb, A=0x00, F=0b11000000, PC=0x0001)

    gb.cpu.register.A = 0x00
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("01")
    cycles = op.code_d6(gb)
    assert cycles == 8
    assert_registers(gb, A=0xFF, F=0b01110000, PC=0x0001)

    gb.cpu.register.A = 0x0F
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("01")
    cycles = op.code_d6(gb)
    assert cycles == 8
    assert_registers(gb, A=0x0E, F=0b01000000, PC=0x0001)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("10")
    cycles = op.code_d6(gb)
    assert cycles == 8
    assert_registers(gb, A=0xE0, F=0b01000000, PC=0x0001)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("01")
    cycles = op.code_d6(gb)
    assert cycles == 8
    assert_registers(gb, A=0xFE, F=0b01000000, PC=0x0001)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("FE")
    cycles = op.code_d6(gb)
    assert cycles == 8
    assert_registers(gb, A=0x01, F=0b01000000, PC=0x0001)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_d7(gb):
    """ RST 10H - Push present address onto stack, jump to address $0000 + 10H """
    gb.cpu.register.PC = 0x2233
    gb.cpu.register.SP = 0x1010
    cycles = op.code_d7(gb)
    assert cycles == 16
    assert_registers(gb, PC=0x0010, SP=0x100E)
    assert_memory(gb, {0x100F: 0x22, 0x100E: 0x33})


# noinspection PyShadowingNames
def test_code_d8(gb):
    """ RET C - Return if flag C is set """
    gb.memory.write_8bit(0x1010, 0x50)
    gb.memory.write_8bit(0x1011, 0x40)

    gb.cpu.register.SP = 0x1010
    gb.cpu.register.PC = 0x0000
    gb.cpu.register.F = 0b00010000
    cycles = op.code_d8(gb)
    assert cycles == 20
    assert_registers(gb, SP=0x1012, PC=0x4050, F=0b00010000)

    gb.cpu.register.SP = 0x1010
    gb.cpu.register.PC = 0x0000
    gb.cpu.register.F = 0b00000000
    cycles = op.code_d8(gb)
    assert cycles == 8
    assert_registers(gb, SP=0x1010, PC=0x0000)

    assert_memory(gb, {0x1010: 0x50, 0x1011: 0x40})


# noinspection PyShadowingNames
def test_code_d9(gb):
    """ RETI - Pop two bytes from stack and jump to that address then enable interrupts """
    gb.memory.write_8bit(0x1010, 0x50)
    gb.memory.write_8bit(0x1011, 0x40)

    gb.cpu.register.SP = 0x1010
    gb.cpu.register.PC = 0x0000
    cycles = op.code_d9(gb)
    assert cycles == 16
    assert_registers(gb, SP=0x1012, PC=0x4050)

    assert_memory(gb, {0x1010: 0x50, 0x1011: 0x40})
    # Since interrupt enable will be done during "interrupt update" step, it cannot be tested here


# noinspection PyShadowingNames
def test_code_da(gb):
    """ JP C,a16 - Jump to address a16 if C flag is set """
    gb.cpu._cartridge_data = bytes.fromhex("FF 55")
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu.register.F = 0b00010000
    cycles = op.code_da(gb)
    assert cycles == 16
    assert_registers(gb, PC=0x55FF, F=0b00010000)

    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu.register.F = 0b00000000
    cycles = op.code_da(gb)
    assert cycles == 12
    assert_registers(gb, PC=0x0002)

    assert_memory(gb)


# OPCODE DB is unused


# noinspection PyShadowingNames
def test_code_dc(gb):
    """ CALL C,a16 - Call address a16 if flag C is set """
    gb.cpu._cartridge_data = bytes.fromhex("FF 55")

    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu.register.SP = 0xFFFE
    gb.cpu.register.F = 0b00010000
    cycles = op.code_dc(gb)
    assert cycles == 24
    assert_registers(gb, PC=0x55FF, SP=0xFFFC, F=0b00010000)
    assert_memory(gb, {0xFFFC: 0x02, 0xFFFD: 0x00})

    gb.memory.write_16bit(0xFFFC, 0x0000)  # To reset memory before next test
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu.register.SP = 0xFFFE
    gb.cpu.register.F = 0b00000000
    cycles = op.code_dc(gb)
    assert cycles == 12
    assert_registers(gb, PC=0x0002, SP=0xFFFE)
    assert_memory(gb)


# OPCODE DD is unused


# noinspection PyShadowingNames
def test_code_de(gb):
    """ SBC A,d8 - A=A-d8-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    gb.cpu.register.A = 0x00
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("00")
    gb.cpu.register.F = 0b00000000
    cycles = op.code_de(gb)
    assert cycles == 8
    assert_registers(gb, A=0x00, F=0b11000000, PC=0x0001)

    gb.cpu.register.A = 0x02
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("00")
    gb.cpu.register.F = 0b00010000
    cycles = op.code_de(gb)
    assert cycles == 8
    assert_registers(gb, A=0x01, F=0b01000000, PC=0x0001)

    gb.cpu.register.A = 0x00
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("01")
    gb.cpu.register.F = 0b00010000
    cycles = op.code_de(gb)
    assert cycles == 8
    assert_registers(gb, A=0xFE, F=0b01110000, PC=0x0001)

    gb.cpu.register.A = 0x13
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("04")
    gb.cpu.register.F = 0b00010000
    cycles = op.code_de(gb)
    assert cycles == 8
    assert_registers(gb, A=0x0E, F=0b01100000, PC=0x0001)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_df(gb):
    """ RST 18H - Push present address onto stack, jump to address $0000 + 18H """
    gb.cpu.register.PC = 0x2233
    gb.cpu.register.SP = 0x1010
    cycles = op.code_df(gb)
    assert cycles == 16
    assert_registers(gb, PC=0x0018, SP=0x100E)
    assert_memory(gb, {0x100F: 0x22, 0x100E: 0x33})


# noinspection PyShadowingNames
def test_code_e0(gb):
    """ LDH (d8),A or LD ($FF00+d8),A - Put A into address ($FF00 + d8) """
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("55")
    gb.cpu.register.A = 0x10
    cycles = op.code_e0(gb)
    assert cycles == 12
    assert_registers(gb,A=0x10,PC=0x0001)
    assert_memory(gb,{0xFF55:0x10})


# noinspection PyShadowingNames
def test_code_e1(gb):
    """ POP HL - Copy 16-bit value from stack (i.e. SP address) into HL, then increment SP by 2 """
    gb.memory.write_16bit(0xFFFC, 0x9933)
    gb.cpu.register.SP = 0xFFFC
    cycles = op.code_e1(gb)
    assert cycles == 12
    assert_registers(gb, H=0x99, L=0x33, SP=0xFFFE)
    assert_memory(gb, {0xFFFD: 0x99, 0xFFFC: 0x33})


# noinspection PyShadowingNames
def test_code_e2(gb):
    """ LD (C),A or LD ($FF00+C),A - Put A into address ($FF00 + register C) """
    gb.cpu.register.A = 0x10
    gb.cpu.register.C = 0x55
    cycles = op.code_e2(gb)
    assert cycles == 8
    assert_registers(gb, A=0x10, C=0x55)
    assert_memory(gb, {0xFF55: 0x10})


# OPCODE E3 is unused


# OPCODE E4 is unused


# noinspection PyShadowingNames
def test_code_e5(gb):
    """ PUSH HL - Decrement SP by 2 then push HL value onto stack (i.e. SP address) """
    gb.cpu.register.set_hl(0x1122)
    cycles = op.code_e5(gb)
    assert cycles == 16
    assert_registers(gb, H=0x11, L=0x22, SP=0xFFFC)
    assert_memory(gb, {0xFFFC: 0x22, 0xFFFD: 0x11})


# noinspection PyShadowingNames
def test_code_e6(gb):
    """ AND d8 - A=Logical AND A with d8 """
    gb.cpu.register.A = 0b10100011
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = 0b01000100.to_bytes(1,byteorder="big")
    cycles = op.code_e6(gb)
    assert cycles == 8
    assert_registers(gb, A=0b00000000, F=0b10100000, PC=0x0001)

    gb.cpu.register.A = 0b10100011
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = 0b01100110.to_bytes(1, byteorder="big")
    cycles = op.code_e6(gb)
    assert cycles == 8
    assert_registers(gb, A=0b00100010, F=0b00100000, PC=0x0001)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_e7(gb):
    """ RST 20H - Push present address onto stack, jump to address $0000 + 20H """
    gb.cpu.register.PC = 0x2233
    gb.cpu.register.SP = 0x1010
    cycles = op.code_e7(gb)
    assert cycles == 16
    assert_registers(gb, PC=0x0020, SP=0x100E)
    assert_memory(gb, {0x100F: 0x22, 0x100E: 0x33})


# noinspection PyShadowingNames
def test_code_e8(gb):
    """ LD HL,SP+d8 or LDHL SP,r8 - Put result of SP+r8 into HL (r8 is a signed value) """
    gb.cpu.register.SP = 0x0000
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("0F")
    cycles = op.code_e8(gb)
    assert cycles == 16
    assert_registers(gb, SP=0x000F, F=0b00000000, PC=0x0001)

    gb.cpu.register.SP = 0x0101
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("7F")
    cycles = op.code_e8(gb)
    assert cycles == 16
    assert_registers(gb, SP=0x0180, F=0b00100000, PC=0x0001)

    gb.cpu.register.SP = 0xFFFF
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("01")
    cycles = op.code_e8(gb)
    assert cycles == 16
    assert_registers(gb, SP=0x0000, F=0b00110000, PC=0x0001)

    gb.cpu.register.SP = 0xFFFF
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("80")  # negative value, -128
    cycles = op.code_e8(gb)
    assert cycles == 16
    assert_registers(gb, SP=0xFF7F, F=0b00000000, PC=0x0001)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_e9(gb):
    """ JP (HL) - Jump to address contained in HL """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_16bit(0x1010,0x5566)
    cycles = op.code_e9(gb)
    assert cycles == 4
    assert_registers(gb,H=0x10,L=0x10,PC=0x5566)
    assert_memory(gb,{0x1010:0x66,0x1011:0x55})


# noinspection PyShadowingNames
def test_code_ea(gb):
    """ LD (a16),A - Stores reg at the address in a16 (least significant byte first) """
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("11 10")
    gb.cpu.register.A = 0x99
    cycles = op.code_ea(gb)
    assert cycles == 16
    assert_registers(gb, A=0x99, PC=0x0002)
    assert_memory(gb,{0x1011:0x99})


# OPCODE EB is unused


# OPCODE EC is unused


# OPCODE ED is unused


# noinspection PyShadowingNames
def test_code_ee(gb):
    """ XOR d8 - A=Logical XOR A with d8 """
    gb.cpu.register.A = 0b10100011
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = 0b10100011.to_bytes(1, byteorder="big")
    cycles = op.code_ee(gb)
    assert cycles == 8
    assert_registers(gb, A=0b00000000, F=0b10000000, PC=0x0001)

    gb.cpu.register.A = 0b10100011
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = 0b01100110.to_bytes(1, byteorder="big")
    cycles = op.code_ee(gb)
    assert cycles == 8
    assert_registers(gb, A=0b11000101, F=0b00000000, PC=0x0001)


# noinspection PyShadowingNames
def test_code_ef(gb):
    """ RST 28H - Push present address onto stack, jump to address $0000 + 28H """
    gb.cpu.register.PC = 0x2233
    gb.cpu.register.SP = 0x1010
    cycles = op.code_ef(gb)
    assert cycles == 16
    assert_registers(gb, PC=0x0028, SP=0x100E)
    assert_memory(gb, {0x100F: 0x22, 0x100E: 0x33})


# noinspection PyShadowingNames
def test_code_f0(gb):
    """ LDH A,(d8) or LD A,($FF00+d8) - Put value at address ($FF00 + d8) into A """
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("11")
    gb.memory.write_8bit(0xFF11,0x55)
    cycles = op.code_f0(gb)
    assert cycles == 12
    assert_registers(gb,A=0x55,PC=0x0001)
    assert_memory(gb,{0xFF11:0x55})


# noinspection PyShadowingNames
def test_code_f1(gb):
    """ POP AF - Copy 16-bit value from stack (i.e. SP address) into AF, then increment SP by 2 """
    gb.memory.write_16bit(0xFFFC, 0x9933)
    gb.cpu.register.SP = 0xFFFC
    cycles = op.code_f1(gb)
    assert cycles == 12
    assert_registers(gb, A=0x99, F=0x33, SP=0xFFFE)
    assert_memory(gb, {0xFFFD: 0x99, 0xFFFC: 0x33})


# noinspection PyShadowingNames
def test_code_f2(gb):
    """ LD A,(C) or LD A,($FF00+C) - Put value at address ($FF00 + register C) into A """
    gb.cpu.register.C = 0x11
    gb.memory.write_8bit(0xFF11, 0x55)
    cycles = op.code_f2(gb)
    assert cycles == 8
    assert_registers(gb, A=0x55, C=0x11)
    assert_memory(gb, {0xFF11: 0x55})


# noinspection PyShadowingNames
def test_code_f3(gb):
    """ DI - Disable interrupts AFTER THE NEXT INSTRUCTION IS EXECUTED """
    cycles = op.code_f3(gb)
    assert cycles == 4
    assert_registers(gb)
    assert_memory(gb)
    # Since interrupt disable will be done during "interrupt update" step, it cannot be tested here


# OPCODE F4 is unused


# noinspection PyShadowingNames
def test_code_f5(gb):
    """ PUSH AF - Decrement SP by 2 then push AF value onto stack (i.e. SP address) """
    gb.cpu.register.set_af(0x1122)
    cycles = op.code_f5(gb)
    assert cycles == 16
    assert_registers(gb, A=0x11, F=0x22, SP=0xFFFC)
    assert_memory(gb, {0xFFFC: 0x22, 0xFFFD: 0x11})


# noinspection PyShadowingNames
def test_code_f6(gb):
    """ OR d8 - A=Logical OR A with d8 """
    gb.cpu.register.A = 0b00000000
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = 0b00000000.to_bytes(1, byteorder="big")
    cycles = op.code_f6(gb)
    assert cycles == 8
    assert_registers(gb, A=0b00000000, F=0b10000000, PC=0x0001)

    gb.cpu.register.A = 0b10100011
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = 0b01100110.to_bytes(1, byteorder="big")
    cycles = op.code_f6(gb)
    assert cycles == 8
    assert_registers(gb, A=0b11100111, F=0b00000000, PC=0x0001)


# noinspection PyShadowingNames
def test_code_f7(gb):
    """ RST 30H - Push present address onto stack, jump to address $0000 + 30H """
    gb.cpu.register.PC = 0x2233
    gb.cpu.register.SP = 0x1010
    cycles = op.code_f7(gb)
    assert cycles == 16
    assert_registers(gb, PC=0x0030, SP=0x100E)
    assert_memory(gb, {0x100F: 0x22, 0x100E: 0x33})


# noinspection PyShadowingNames
def test_code_f8(gb):
    """ LD HL,SP+d8 or LDHL SP,r8 - Put result of SP+r8 into HL (r8 is a signed value) """
    gb.cpu.register.SP = 0x0000
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("0F")
    cycles = op.code_f8(gb)
    assert cycles == 12
    assert_registers(gb, H=0x00, L=0x0F, SP=0x0000, F=0b00000000, PC=0x0001)

    gb.cpu.register.SP = 0x0101
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("7F")
    cycles = op.code_f8(gb)
    assert cycles == 12
    assert_registers(gb, H=0x01, L=0x80, SP=0x0101, F=0b00100000, PC=0x0001)

    gb.cpu.register.SP = 0xFFFF
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("01")
    cycles = op.code_f8(gb)
    assert cycles == 12
    assert_registers(gb, H=0x00, L=0x00, SP=0xFFFF, F=0b00110000, PC=0x0001)

    gb.cpu.register.SP = 0xFFFF
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("80")  # negative value, -128
    cycles = op.code_f8(gb)
    assert cycles == 12
    assert_registers(gb, H=0xFF, L=0x7F, SP=0xFFFF, F=0b00000000, PC=0x0001)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_f9(gb):
    """ LD SP,HL - Put HL value into SP """
    gb.cpu.register.set_hl(0x9933)
    cycles = op.code_f9(gb)
    assert cycles == 8
    assert_registers(gb, H=0x99, L=0x33, SP=0x9933)


# noinspection PyShadowingNames
def test_code_fa(gb):
    """ LD A,(a16) - Load reg with the value at the address in a16 (least significant byte first) """
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("11 10")
    gb.memory.write_8bit(0x1011,0x55)
    cycles = op.code_fa(gb)
    assert cycles == 16
    assert_registers(gb,A=0x55,PC=0x0002)
    assert_memory(gb,{0x1011:0x55})


# noinspection PyShadowingNames
def test_code_fb(gb):
    """ EI - Enable interrupts AFTER THE NEXT INSTRUCTION IS EXECUTED """
    cycles = op.code_fb(gb)
    assert cycles == 4
    assert_registers(gb)
    assert_memory(gb)
    # Since interrupt enable will be done during "interrupt update" step, it cannot be tested here


# OPCODE FC is unused


# OPCODE FD is unused


# noinspection PyShadowingNames
def test_code_fe(gb):
    """ CP A,d8 - same as SUB A,d8 but throw the result away, only set flags """
    gb.cpu.register.A = 0x00
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("00")
    cycles = op.code_fe(gb)
    assert cycles == 8
    assert_registers(gb, A=0x00, F=0b11000000, PC=0x0001)

    gb.cpu.register.A = 0x00
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("01")
    cycles = op.code_fe(gb)
    assert cycles == 8
    assert_registers(gb, A=0x00, F=0b01110000, PC=0x0001)

    gb.cpu.register.A = 0x0F
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("01")
    cycles = op.code_fe(gb)
    assert cycles == 8
    assert_registers(gb, A=0x0F, F=0b01000000, PC=0x0001)

    gb.cpu.register.A = 0xF0
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("10")
    cycles = op.code_fe(gb)
    assert cycles == 8
    assert_registers(gb, A=0xF0, F=0b01000000, PC=0x0001)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("01")
    cycles = op.code_fe(gb)
    assert cycles == 8
    assert_registers(gb, A=0xFF, F=0b01000000, PC=0x0001)

    gb.cpu.register.A = 0xFF
    gb.cpu.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    gb.cpu._cartridge_data = bytes.fromhex("FE")
    cycles = op.code_fe(gb)
    assert cycles == 8
    assert_registers(gb, A=0xFF, F=0b01000000, PC=0x0001)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_ff(gb):
    """ RST 38H - Push present address onto stack, jump to address $0000 + 38H """
    gb.cpu.register.PC = 0x2233
    gb.cpu.register.SP = 0x1010
    cycles = op.code_ff(gb)
    assert cycles == 16
    assert_registers(gb, PC=0x0038, SP=0x100E)
    assert_memory(gb, {0x100F: 0x22, 0x100E: 0x33})


""" CB-Prefix operations """


# noinspection PyShadowingNames
def test_code_cb_00(gb):
    """ RLC B - Copy register B bit 7 to Carry flag, then rotate register B left """
    gb.cpu.register.B = 0b11100010
    cycles = op.code_cb_00(gb)
    assert cycles == 8
    assert_registers(gb, B=0b11000101, F=0b00010000)

    gb.cpu.register.B = 0b00000000
    cycles = op.code_cb_00(gb)
    assert cycles == 8
    assert_registers(gb, B=0b00000000, F=0b10000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_01(gb):
    """ RLC C - Copy register C bit 7 to Carry flag, then rotate register C left """
    gb.cpu.register.C = 0b11100010
    cycles = op.code_cb_01(gb)
    assert cycles == 8
    assert_registers(gb, C=0b11000101, F=0b00010000)

    gb.cpu.register.C = 0b00000000
    cycles = op.code_cb_01(gb)
    assert cycles == 8
    assert_registers(gb, C=0b00000000, F=0b10000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_02(gb):
    """ RLC D - Copy register D bit 7 to Carry flag, then rotate register D left """
    gb.cpu.register.D = 0b11100010
    cycles = op.code_cb_02(gb)
    assert cycles == 8
    assert_registers(gb, D=0b11000101, F=0b00010000)

    gb.cpu.register.D = 0b00000000
    cycles = op.code_cb_02(gb)
    assert cycles == 8
    assert_registers(gb, D=0b00000000, F=0b10000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_03(gb):
    """ RLC E - Copy register E bit 7 to Carry flag, then rotate register E left """
    gb.cpu.register.E = 0b11100010
    cycles = op.code_cb_03(gb)
    assert cycles == 8
    assert_registers(gb, E=0b11000101, F=0b00010000)

    gb.cpu.register.E = 0b00000000
    cycles = op.code_cb_03(gb)
    assert cycles == 8
    assert_registers(gb, E=0b00000000, F=0b10000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_04(gb):
    """ RLC H - Copy register H bit 7 to Carry flag, then rotate register H left """
    gb.cpu.register.H = 0b11100010
    cycles = op.code_cb_04(gb)
    assert cycles == 8
    assert_registers(gb, H=0b11000101, F=0b00010000)

    gb.cpu.register.H = 0b00000000
    cycles = op.code_cb_04(gb)
    assert cycles == 8
    assert_registers(gb, H=0b00000000, F=0b10000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_05(gb):
    """ RLC L - Copy register L bit 7 to Carry flag, then rotate register L left """
    gb.cpu.register.L = 0b11100010
    cycles = op.code_cb_05(gb)
    assert cycles == 8
    assert_registers(gb, L=0b11000101, F=0b00010000)

    gb.cpu.register.L = 0b00000000
    cycles = op.code_cb_05(gb)
    assert cycles == 8
    assert_registers(gb, L=0b00000000, F=0b10000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_06(gb):
    """ RLC (HL) - Copy (value at address HL) bit 7 to Carry flag, then rotate (value at address HL) left """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010,0b11100010)
    cycles = op.code_cb_06(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b00010000)
    assert_memory(gb,{0x1010:0b11000101})

    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b00000000)
    cycles = op.code_cb_06(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b10000000)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_07(gb):
    """ RLC A - Copy register A bit 7 to Carry flag, then rotate register A left """
    gb.cpu.register.A = 0b11100010
    cycles = op.code_cb_07(gb)
    assert cycles == 8
    assert_registers(gb, A=0b11000101, F=0b00010000)

    gb.cpu.register.A = 0b00000000
    cycles = op.code_cb_07(gb)
    assert cycles == 8
    assert_registers(gb, A=0b00000000, F=0b10000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_08(gb):
    """ RRC B - Copy register B bit 0 to Carry flag, then rotate register B right """
    gb.cpu.register.B = 0b11100011
    cycles = op.code_cb_08(gb)
    assert cycles == 8
    assert_registers(gb, B=0b11110001, F=0b00010000)

    gb.cpu.register.B = 0b00000000
    cycles = op.code_cb_08(gb)
    assert cycles == 8
    assert_registers(gb, B=0b00000000, F=0b10000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_09(gb):
    """ RRC C - Copy register C bit 0 to Carry flag, then rotate register C right """
    gb.cpu.register.C = 0b11100011
    cycles = op.code_cb_09(gb)
    assert cycles == 8
    assert_registers(gb, C=0b11110001, F=0b00010000)

    gb.cpu.register.C = 0b00000000
    cycles = op.code_cb_09(gb)
    assert cycles == 8
    assert_registers(gb, C=0b00000000, F=0b10000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_0a(gb):
    """ RRC D - Copy register D bit 0 to Carry flag, then rotate register D right """
    gb.cpu.register.D = 0b11100011
    cycles = op.code_cb_0a(gb)
    assert cycles == 8
    assert_registers(gb, D=0b11110001, F=0b00010000)

    gb.cpu.register.D = 0b00000000
    cycles = op.code_cb_0a(gb)
    assert cycles == 8
    assert_registers(gb, D=0b00000000, F=0b10000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_0b(gb):
    """ RRC E - Copy register E bit 0 to Carry flag, then rotate register E right """
    gb.cpu.register.E = 0b11100011
    cycles = op.code_cb_0b(gb)
    assert cycles == 8
    assert_registers(gb, E=0b11110001, F=0b00010000)

    gb.cpu.register.E = 0b00000000
    cycles = op.code_cb_0b(gb)
    assert cycles == 8
    assert_registers(gb, E=0b00000000, F=0b10000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_0c(gb):
    """ RRC H - Copy register H bit 0 to Carry flag, then rotate register H right """
    gb.cpu.register.H = 0b11100011
    cycles = op.code_cb_0c(gb)
    assert cycles == 8
    assert_registers(gb, H=0b11110001, F=0b00010000)

    gb.cpu.register.H = 0b00000000
    cycles = op.code_cb_0c(gb)
    assert cycles == 8
    assert_registers(gb, H=0b00000000, F=0b10000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_0d(gb):
    """ RRC L - Copy register L bit 0 to Carry flag, then rotate register L right """
    gb.cpu.register.L = 0b11100011
    cycles = op.code_cb_0d(gb)
    assert cycles == 8
    assert_registers(gb, L=0b11110001, F=0b00010000)

    gb.cpu.register.L = 0b00000000
    cycles = op.code_cb_0d(gb)
    assert cycles == 8
    assert_registers(gb, L=0b00000000, F=0b10000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_0e(gb):
    """ RRC (HL) - Copy bit 0 to Carry flag, then rotate right """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010,0b11100011)
    cycles = op.code_cb_0e(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b00010000)
    assert_memory(gb,{0x1010:0b11110001})

    gb.memory.write_8bit(0x1010, 0b00000000)
    cycles = op.code_cb_0e(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b10000000)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_0f(gb):
    """ RRC A - Copy register A bit 0 to Carry flag, then rotate register A right """
    gb.cpu.register.A = 0b11100011
    cycles = op.code_cb_0f(gb)
    assert cycles == 8
    assert_registers(gb, A=0b11110001, F=0b00010000)

    gb.cpu.register.A = 0b00000000
    cycles = op.code_cb_0f(gb)
    assert cycles == 8
    assert_registers(gb, A=0b00000000, F=0b10000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_10(gb):
    """ RL B - Copy register B bit 7 to temp, replace B bit 7 w/ Carry flag, rotate B left, copy temp to Carry flag """
    gb.cpu.register.B = 0b11100010
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_10(gb)
    assert cycles == 8
    assert_registers(gb, B=0b11000101, F=0b00010000)

    gb.cpu.register.B = 0b00000000
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_10(gb)
    assert cycles == 8
    assert_registers(gb, B=0b00000001, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_11(gb):
    """ RL C - Copy register C bit 7 to temp, replace C bit 7 w/ Carry flag, rotate C left, copy temp to Carry flag """
    gb.cpu.register.C = 0b11100010
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_11(gb)
    assert cycles == 8
    assert_registers(gb, C=0b11000101, F=0b00010000)

    gb.cpu.register.C = 0b00000000
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_11(gb)
    assert cycles == 8
    assert_registers(gb, C=0b00000001, F=0b00000000)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_12(gb):
    """ RL D - Copy register D bit 7 to temp, replace D bit 7 w/ Carry flag, rotate D left, copy temp to Carry flag """
    gb.cpu.register.D = 0b11100010
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_12(gb)
    assert cycles == 8
    assert_registers(gb, D=0b11000101, F=0b00010000)

    gb.cpu.register.D = 0b00000000
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_12(gb)
    assert cycles == 8
    assert_registers(gb, D=0b00000001, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_13(gb):
    """ RL E - Copy register E bit 7 to temp, replace E bit 7 w/ Carry flag, rotate E left, copy temp to Carry flag """
    gb.cpu.register.E = 0b11100010
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_13(gb)
    assert cycles == 8
    assert_registers(gb, E=0b11000101, F=0b00010000)

    gb.cpu.register.E = 0b00000000
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_13(gb)
    assert cycles == 8
    assert_registers(gb, E=0b00000001, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_14(gb):
    """ RL H - Copy register H bit 7 to temp, replace H bit 7 w/ Carry flag, rotate H left, copy temp to Carry flag """
    gb.cpu.register.H = 0b11100010
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_14(gb)
    assert cycles == 8
    assert_registers(gb, H=0b11000101, F=0b00010000)

    gb.cpu.register.H = 0b00000000
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_14(gb)
    assert cycles == 8
    assert_registers(gb, H=0b00000001, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_15(gb):
    """ RL L - Copy register L bit 7 to temp, replace L bit 7 w/ Carry flag, rotate L left, copy temp to Carry flag """
    gb.cpu.register.L = 0b11100010
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_15(gb)
    assert cycles == 8
    assert_registers(gb, L=0b11000101, F=0b00010000)

    gb.cpu.register.L = 0b00000000
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_15(gb)
    assert cycles == 8
    assert_registers(gb, L=0b00000001, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_16(gb):
    """ RL (HL) - Copy bit 7 to temp, replace bit 7 w/ Carry flag, rotate left, copy temp to Carry flag """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b11100010)
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_16(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b00010000)
    assert_memory(gb,{0x1010:0b11000101})

    gb.memory.write_8bit(0x1010, 0b00000000)
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_16(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b00000000)
    assert_memory(gb, {0x1010: 0b00000001})


# noinspection PyShadowingNames
def test_code_cb_17(gb):
    """ RL A - Copy register A bit 7 to temp, replace A bit 7 w/ Carry flag, rotate A left, copy temp to Carry flag """
    gb.cpu.register.A = 0b11100010
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_17(gb)
    assert cycles == 8
    assert_registers(gb, A=0b11000101, F=0b00010000)

    gb.cpu.register.A = 0b00000000
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_17(gb)
    assert cycles == 8
    assert_registers(gb, A=0b00000001, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_18(gb):
    """ RR B - Copy register B bit 0 to temp, replace B bit 0 w/ Carry flag, rotate B right, copy temp to Carry flag """
    gb.cpu.register.B = 0b11100011
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_18(gb)
    assert cycles == 8
    assert_registers(gb, B=0b11110001, F=0b00010000)

    gb.cpu.register.B = 0b00000000
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_18(gb)
    assert cycles == 8
    assert_registers(gb, B=0b10000000, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_19(gb):
    """ RR C - Copy register C bit 0 to temp, replace C bit 0 w/ Carry flag, rotate C right, copy temp to Carry flag """
    gb.cpu.register.C = 0b11100011
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_19(gb)
    assert cycles == 8
    assert_registers(gb, C=0b11110001, F=0b00010000)

    gb.cpu.register.C = 0b00000000
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_19(gb)
    assert cycles == 8
    assert_registers(gb, C=0b10000000, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_1a(gb):
    """ RR D - Copy register D bit 0 to temp, replace D bit 0 w/ Carry flag, rotate D right, copy temp to Carry flag """
    gb.cpu.register.D = 0b11100011
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_1a(gb)
    assert cycles == 8
    assert_registers(gb, D=0b11110001, F=0b00010000)

    gb.cpu.register.D = 0b00000000
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_1a(gb)
    assert cycles == 8
    assert_registers(gb, D=0b10000000, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_1b(gb):
    """ RR E - Copy register E bit 0 to temp, replace E bit 0 w/ Carry flag, rotate E right, copy temp to Carry flag """
    gb.cpu.register.E = 0b11100011
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_1b(gb)
    assert cycles == 8
    assert_registers(gb, E=0b11110001, F=0b00010000)

    gb.cpu.register.E = 0b00000000
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_1b(gb)
    assert cycles == 8
    assert_registers(gb, E=0b10000000, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_1c(gb):
    """ RR H - Copy register H bit 0 to temp, replace H bit 0 w/ Carry flag, rotate H right, copy temp to Carry flag """
    gb.cpu.register.H = 0b11100011
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_1c(gb)
    assert cycles == 8
    assert_registers(gb, H=0b11110001, F=0b00010000)

    gb.cpu.register.H = 0b00000000
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_1c(gb)
    assert cycles == 8
    assert_registers(gb, H=0b10000000, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_1d(gb):
    """ RR L - Copy register L bit 0 to temp, replace L bit 0 w/ Carry flag, rotate L right, copy temp to Carry flag """
    gb.cpu.register.L = 0b11100011
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_1d(gb)
    assert cycles == 8
    assert_registers(gb, L=0b11110001, F=0b00010000)

    gb.cpu.register.L = 0b00000000
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_1d(gb)
    assert cycles == 8
    assert_registers(gb, L=0b10000000, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_1e(gb):
    """ RR (HL) - Copy (HL) bit 0 to temp, replace bit 0 w/ Carry flag, rotate right, copy temp to Carry flag """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b11100011)
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_1e(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b00010000)
    assert_memory(gb,{0x1010:0b11110001})

    gb.memory.write_8bit(0x1010, 0b00000000)
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_1e(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b00000000)
    assert_memory(gb, {0x1010: 0b10000000})


# noinspection PyShadowingNames
def test_code_cb_1f(gb):
    """ RR A - Copy register A bit 0 to temp, replace A bit 0 w/ Carry flag, rotate A right, copy temp to Carry flag """
    gb.cpu.register.A = 0b11100011
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_1f(gb)
    assert cycles == 8
    assert_registers(gb, A=0b11110001, F=0b00010000)

    gb.cpu.register.A = 0b00000000
    gb.cpu.register.F = 0b00010000
    cycles = op.code_cb_1f(gb)
    assert cycles == 8
    assert_registers(gb, A=0b10000000, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_20(gb):
    """ SLA B - Copy B bit 7 to temp, replace B bit 7 w/ zero, rotate B left, copy temp to Carry flag """
    gb.cpu.register.B = 0b11100010
    cycles = op.code_cb_20(gb)
    assert cycles == 8
    assert_registers(gb, B=0b11000100, F=0b00010000)

    gb.cpu.register.B = 0b00000000
    cycles = op.code_cb_20(gb)
    assert cycles == 8
    assert_registers(gb, B=0b00000000, F=0b10000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_21(gb):
    """ SLA C - Copy C bit 7 to temp, replace C bit 7 w/ zero, rotate C left, copy temp to Carry flag """
    gb.cpu.register.C = 0b11100010
    cycles = op.code_cb_21(gb)
    assert cycles == 8
    assert_registers(gb, C=0b11000100, F=0b00010000)

    gb.cpu.register.C = 0b00000000
    cycles = op.code_cb_21(gb)
    assert cycles == 8
    assert_registers(gb, C=0b00000000, F=0b10000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_22(gb):
    """ SLA D - Copy D bit 7 to temp, replace D bit 7 w/ zero, rotate D left, copy temp to Carry flag """
    gb.cpu.register.D = 0b11100010
    cycles = op.code_cb_22(gb)
    assert cycles == 8
    assert_registers(gb, D=0b11000100, F=0b00010000)

    gb.cpu.register.D = 0b00000000
    cycles = op.code_cb_22(gb)
    assert cycles == 8
    assert_registers(gb, D=0b00000000, F=0b10000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_23(gb):
    """ SLA E - Copy E bit 7 to temp, replace E bit 7 w/ zero, rotate E left, copy temp to Carry flag """
    gb.cpu.register.E = 0b11100010
    cycles = op.code_cb_23(gb)
    assert cycles == 8
    assert_registers(gb, E=0b11000100, F=0b00010000)

    gb.cpu.register.E = 0b00000000
    cycles = op.code_cb_23(gb)
    assert cycles == 8
    assert_registers(gb, E=0b00000000, F=0b10000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_24(gb):
    """ SLA H - Copy H bit 7 to temp, replace H bit 7 w/ zero, rotate H left, copy temp to Carry flag """
    gb.cpu.register.H = 0b11100010
    cycles = op.code_cb_24(gb)
    assert cycles == 8
    assert_registers(gb, H=0b11000100, F=0b00010000)

    gb.cpu.register.H = 0b00000000
    cycles = op.code_cb_24(gb)
    assert cycles == 8
    assert_registers(gb, H=0b00000000, F=0b10000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_25(gb):
    """ SLA L - Copy L bit 7 to temp, replace L bit 7 w/ zero, rotate L left, copy temp to Carry flag """
    gb.cpu.register.L = 0b11100010
    cycles = op.code_cb_25(gb)
    assert cycles == 8
    assert_registers(gb, L=0b11000100, F=0b00010000)

    gb.cpu.register.L = 0b00000000
    cycles = op.code_cb_25(gb)
    assert cycles == 8
    assert_registers(gb, L=0b00000000, F=0b10000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_26(gb):
    """ SLA (HL) - Copy (HL) bit 7 to temp, replace bit 7 w/ zero, rotate left, copy temp to Carry flag """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b11100010)
    cycles = op.code_cb_26(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b00010000)
    assert_memory(gb,{0x1010:0b11000100})

    gb.memory.write_8bit(0x1010, 0b00000000)
    cycles = op.code_cb_26(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b10000000)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_27(gb):
    """ SLA A - Copy A bit 7 to temp, replace A bit 7 w/ zero, rotate A left, copy temp to Carry flag """
    gb.cpu.register.A = 0b11100010
    cycles = op.code_cb_27(gb)
    assert cycles == 8
    assert_registers(gb, A=0b11000100, F=0b00010000)

    gb.cpu.register.A = 0b00000000
    cycles = op.code_cb_27(gb)
    assert cycles == 8
    assert_registers(gb, A=0b00000000, F=0b10000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_28(gb):
    """ SRA B - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    gb.cpu.register.B = 0b10000001
    cycles = op.code_cb_28(gb)
    assert cycles == 8
    assert_registers(gb, B=0b11000000, F=0b00010000)

    gb.cpu.register.B = 0b00000001
    gb.cpu.register.F = 0b00000000
    cycles = op.code_cb_28(gb)
    assert cycles == 8
    assert_registers(gb, B=0b00000000, F=0b10010000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_29(gb):
    """ SRA C - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    gb.cpu.register.C = 0b10000001
    cycles = op.code_cb_29(gb)
    assert cycles == 8
    assert_registers(gb, C=0b11000000, F=0b00010000)

    gb.cpu.register.C = 0b00000001
    gb.cpu.register.F = 0b00000000
    cycles = op.code_cb_29(gb)
    assert cycles == 8
    assert_registers(gb, C=0b00000000, F=0b10010000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_2a(gb):
    """ SRA D - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    gb.cpu.register.D = 0b10000001
    cycles = op.code_cb_2a(gb)
    assert cycles == 8
    assert_registers(gb, D=0b11000000, F=0b00010000)

    gb.cpu.register.D = 0b00000001
    gb.cpu.register.F = 0b00000000
    cycles = op.code_cb_2a(gb)
    assert cycles == 8
    assert_registers(gb, D=0b00000000, F=0b10010000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_2b(gb):
    """ SRA E - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    gb.cpu.register.E = 0b10000001
    cycles = op.code_cb_2b(gb)
    assert cycles == 8
    assert_registers(gb, E=0b11000000, F=0b00010000)

    gb.cpu.register.E = 0b00000001
    gb.cpu.register.F = 0b00000000
    cycles = op.code_cb_2b(gb)
    assert cycles == 8
    assert_registers(gb, E=0b00000000, F=0b10010000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_2c(gb):
    """ SRA H - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    gb.cpu.register.H = 0b10000001
    cycles = op.code_cb_2c(gb)
    assert cycles == 8
    assert_registers(gb, H=0b11000000, F=0b00010000)

    gb.cpu.register.H = 0b00000001
    gb.cpu.register.F = 0b00000000
    cycles = op.code_cb_2c(gb)
    assert cycles == 8
    assert_registers(gb, H=0b00000000, F=0b10010000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_2d(gb):
    """ SRA L - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    gb.cpu.register.L = 0b10000001
    cycles = op.code_cb_2d(gb)
    assert cycles == 8
    assert_registers(gb, L=0b11000000, F=0b00010000)

    gb.cpu.register.L = 0b00000001
    gb.cpu.register.F = 0b00000000
    cycles = op.code_cb_2d(gb)
    assert cycles == 8
    assert_registers(gb, L=0b00000000, F=0b10010000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_2e(gb):
    """ SRA (HL) - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b10000001)
    cycles = op.code_cb_2e(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b00010000)
    assert_memory(gb, {0x1010: 0b11000000})

    gb.memory.write_8bit(0x1010, 0b00000001)
    gb.cpu.register.F = 0b00000000
    cycles = op.code_cb_2e(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b10010000)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_2f(gb):
    """ SRA A - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    gb.cpu.register.A = 0b10000001
    cycles = op.code_cb_2f(gb)
    assert cycles == 8
    assert_registers(gb, A=0b11000000, F=0b00010000)

    gb.cpu.register.A = 0b00000001
    gb.cpu.register.F = 0b00000000
    cycles = op.code_cb_2f(gb)
    assert cycles == 8
    assert_registers(gb, A=0b00000000, F=0b10010000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_30(gb):
    """ SWAP B - Swap upper and lower nibbles (nibble = 4 bits) """
    gb.cpu.register.B = 0xAB
    cycles = op.code_cb_30(gb)
    assert cycles == 8
    assert_registers(gb, B=0xBA, F=0b00000000)

    gb.cpu.register.B = 0x00
    cycles = op.code_cb_30(gb)
    assert cycles == 8
    assert_registers(gb, B=0x00, F=0b10000000)

    gb.cpu.register.B = 0xF0
    cycles = op.code_cb_30(gb)
    assert cycles == 8
    assert_registers(gb, B=0x0F, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_31(gb):
    """ SWAP C - Swap upper and lower nibbles (nibble = 4 bits) """
    gb.cpu.register.C = 0xAB
    cycles = op.code_cb_31(gb)
    assert cycles == 8
    assert_registers(gb, C=0xBA, F=0b00000000)

    gb.cpu.register.C = 0x00
    cycles = op.code_cb_31(gb)
    assert cycles == 8
    assert_registers(gb, C=0x00, F=0b10000000)

    gb.cpu.register.C = 0xF0
    cycles = op.code_cb_31(gb)
    assert cycles == 8
    assert_registers(gb, C=0x0F, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_32(gb):
    """ SWAP D - Swap upper and lower nibbles (nibble = 4 bits) """
    gb.cpu.register.D = 0xAB
    cycles = op.code_cb_32(gb)
    assert cycles == 8
    assert_registers(gb, D=0xBA, F=0b00000000)

    gb.cpu.register.D = 0x00
    cycles = op.code_cb_32(gb)
    assert cycles == 8
    assert_registers(gb, D=0x00, F=0b10000000)

    gb.cpu.register.D = 0xF0
    cycles = op.code_cb_32(gb)
    assert cycles == 8
    assert_registers(gb, D=0x0F, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_33(gb):
    """ SWAP E - Swap upper and lower nibbles (nibble = 4 bits) """
    gb.cpu.register.E = 0xAB
    cycles = op.code_cb_33(gb)
    assert cycles == 8
    assert_registers(gb, E=0xBA, F=0b00000000)

    gb.cpu.register.E = 0x00
    cycles = op.code_cb_33(gb)
    assert cycles == 8
    assert_registers(gb, E=0x00, F=0b10000000)

    gb.cpu.register.E = 0xF0
    cycles = op.code_cb_33(gb)
    assert cycles == 8
    assert_registers(gb, E=0x0F, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_34(gb):
    """ SWAP H - Swap upper and lower nibbles (nibble = 4 bits) """
    gb.cpu.register.H = 0xAB
    cycles = op.code_cb_34(gb)
    assert cycles == 8
    assert_registers(gb, H=0xBA, F=0b00000000)

    gb.cpu.register.H = 0x00
    cycles = op.code_cb_34(gb)
    assert cycles == 8
    assert_registers(gb, H=0x00, F=0b10000000)

    gb.cpu.register.H = 0xF0
    cycles = op.code_cb_34(gb)
    assert cycles == 8
    assert_registers(gb, H=0x0F, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_35(gb):
    """ SWAP L - Swap upper and lower nibbles (nibble = 4 bits) """
    gb.cpu.register.L = 0xAB
    cycles = op.code_cb_35(gb)
    assert cycles == 8
    assert_registers(gb, L=0xBA, F=0b00000000)

    gb.cpu.register.L = 0x00
    cycles = op.code_cb_35(gb)
    assert cycles == 8
    assert_registers(gb, L=0x00, F=0b10000000)

    gb.cpu.register.L = 0xF0
    cycles = op.code_cb_35(gb)
    assert cycles == 8
    assert_registers(gb, L=0x0F, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_36(gb):
    """ SWAP (HL) - Swap upper and lower nibbles (nibble = 4 bits) """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0xAB)
    cycles = op.code_cb_36(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b00000000)
    assert_memory(gb,{0x1010:0xBA})

    gb.memory.write_8bit(0x1010, 0x00)
    cycles = op.code_cb_36(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b10000000)
    assert_memory(gb)

    gb.memory.write_8bit(0x1010, 0xF0)
    cycles = op.code_cb_36(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b00000000)
    assert_memory(gb, {0x1010: 0x0F})


# noinspection PyShadowingNames
def test_code_cb_37(gb):
    """ SWAP A - Swap upper and lower nibbles (nibble = 4 bits) """
    gb.cpu.register.A = 0xAB
    cycles = op.code_cb_37(gb)
    assert cycles == 8
    assert_registers(gb, A=0xBA, F=0b00000000)

    gb.cpu.register.A = 0x00
    cycles = op.code_cb_37(gb)
    assert cycles == 8
    assert_registers(gb, A=0x00, F=0b10000000)

    gb.cpu.register.A = 0xF0
    cycles = op.code_cb_37(gb)
    assert cycles == 8
    assert_registers(gb, A=0x0F, F=0b00000000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_38(gb):
    """ SRL B - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    gb.cpu.register.B = 0b10000001
    cycles = op.code_cb_38(gb)
    assert cycles == 8
    assert_registers(gb, B=0b01000000, F=0b00010000)

    gb.cpu.register.B = 0b00000001
    gb.cpu.register.F = 0b00000000
    cycles = op.code_cb_38(gb)
    assert cycles == 8
    assert_registers(gb, B=0b00000000, F=0b10010000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_39(gb):
    """ SRL C - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    gb.cpu.register.C = 0b10000001
    cycles = op.code_cb_39(gb)
    assert cycles == 8
    assert_registers(gb, C=0b01000000, F=0b00010000)

    gb.cpu.register.C = 0b00000001
    gb.cpu.register.F = 0b00000000
    cycles = op.code_cb_39(gb)
    assert cycles == 8
    assert_registers(gb, C=0b00000000, F=0b10010000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_3a(gb):
    """ SRL D - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    gb.cpu.register.D = 0b10000001
    cycles = op.code_cb_3a(gb)
    assert cycles == 8
    assert_registers(gb, D=0b01000000, F=0b00010000)

    gb.cpu.register.D = 0b00000001
    gb.cpu.register.F = 0b00000000
    cycles = op.code_cb_3a(gb)
    assert cycles == 8
    assert_registers(gb, D=0b00000000, F=0b10010000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_3b(gb):
    """ SRL E - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    gb.cpu.register.E = 0b10000001
    cycles = op.code_cb_3b(gb)
    assert cycles == 8
    assert_registers(gb, E=0b01000000, F=0b00010000)

    gb.cpu.register.E = 0b00000001
    gb.cpu.register.F = 0b00000000
    cycles = op.code_cb_3b(gb)
    assert cycles == 8
    assert_registers(gb, E=0b00000000, F=0b10010000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_3c(gb):
    """ SRL H - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    gb.cpu.register.H = 0b10000001
    cycles = op.code_cb_3c(gb)
    assert cycles == 8
    assert_registers(gb, H=0b01000000, F=0b00010000)

    gb.cpu.register.H = 0b00000001
    gb.cpu.register.F = 0b00000000
    cycles = op.code_cb_3c(gb)
    assert cycles == 8
    assert_registers(gb, H=0b00000000, F=0b10010000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_3d(gb):
    """ SRL L - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    gb.cpu.register.L = 0b10000001
    cycles = op.code_cb_3d(gb)
    assert cycles == 8
    assert_registers(gb, L=0b01000000, F=0b00010000)

    gb.cpu.register.L = 0b00000001
    gb.cpu.register.F = 0b00000000
    cycles = op.code_cb_3d(gb)
    assert cycles == 8
    assert_registers(gb, L=0b00000000, F=0b10010000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_3e(gb):
    """ SRL (HL) - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b10000001)
    cycles = op.code_cb_3e(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b00010000)
    assert_memory(gb, {0x1010: 0b01000000})

    gb.memory.write_8bit(0x1010, 0b00000001)
    gb.cpu.register.F = 0b00000000
    cycles = op.code_cb_3e(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b10010000)
    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_3f(gb):
    """ SRL A - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    gb.cpu.register.A = 0b10000001
    cycles = op.code_cb_3f(gb)
    assert cycles == 8
    assert_registers(gb, A=0b01000000, F=0b00010000)

    gb.cpu.register.A = 0b00000001
    gb.cpu.register.F = 0b00000000
    cycles = op.code_cb_3f(gb)
    assert cycles == 8
    assert_registers(gb, A=0b00000000, F=0b10010000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_40(gb):
    """ BIT 0,B - Test what is the value of bit 0 """
    gb.cpu.register.B = 0b00000001
    cycles = op.code_cb_40(gb)
    assert cycles == 8
    assert_registers(gb, B=0b00000001, F=0b10100000)

    gb.cpu.register.B = 0b11111110
    cycles = op.code_cb_40(gb)
    assert cycles == 8
    assert_registers(gb, B=0b11111110, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_41(gb):
    """ BIT 0,C - Test what is the value of bit 0 """
    gb.cpu.register.C = 0b00000001
    cycles = op.code_cb_41(gb)
    assert cycles == 8
    assert_registers(gb, C=0b00000001, F=0b10100000)

    gb.cpu.register.C = 0b11111110
    cycles = op.code_cb_41(gb)
    assert cycles == 8
    assert_registers(gb, C=0b11111110, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_42(gb):
    """ BIT 0,D - Test what is the value of bit 0 """
    gb.cpu.register.D = 0b00000001
    cycles = op.code_cb_42(gb)
    assert cycles == 8
    assert_registers(gb, D=0b00000001, F=0b10100000)

    gb.cpu.register.D = 0b11111110
    cycles = op.code_cb_42(gb)
    assert cycles == 8
    assert_registers(gb, D=0b11111110, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_43(gb):
    """ BIT 0,E - Test what is the value of bit 0 """
    gb.cpu.register.E = 0b00000001
    cycles = op.code_cb_43(gb)
    assert cycles == 8
    assert_registers(gb, E=0b00000001, F=0b10100000)

    gb.cpu.register.E = 0b11111110
    cycles = op.code_cb_43(gb)
    assert cycles == 8
    assert_registers(gb, E=0b11111110, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_44(gb):
    """ BIT 0,H - Test what is the value of bit 0 """
    gb.cpu.register.H = 0b00000001
    cycles = op.code_cb_44(gb)
    assert cycles == 8
    assert_registers(gb, H=0b00000001, F=0b10100000)

    gb.cpu.register.H = 0b11111110
    cycles = op.code_cb_44(gb)
    assert cycles == 8
    assert_registers(gb, H=0b11111110, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_45(gb):
    """ BIT 0,L - Test what is the value of bit 0 """
    gb.cpu.register.L = 0b00000001
    cycles = op.code_cb_45(gb)
    assert cycles == 8
    assert_registers(gb, L=0b00000001, F=0b10100000)

    gb.cpu.register.L = 0b11111110
    cycles = op.code_cb_45(gb)
    assert cycles == 8
    assert_registers(gb, L=0b11111110, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_46(gb):
    """ BIT 0,(HL) - Test what is the value of bit 0 """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b00000001)
    cycles = op.code_cb_46(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b10100000)
    assert_memory(gb,{0x1010:0b00000001})

    gb.memory.write_8bit(0x1010, 0b11111110)
    cycles = op.code_cb_46(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b00100000)
    assert_memory(gb, {0x1010: 0b11111110})


# noinspection PyShadowingNames
def test_code_cb_47(gb):
    """ BIT 0,A - Test what is the value of bit 0 """
    gb.cpu.register.A = 0b00000001
    cycles = op.code_cb_47(gb)
    assert cycles == 8
    assert_registers(gb, A=0b00000001, F=0b10100000)

    gb.cpu.register.A = 0b11111110
    cycles = op.code_cb_47(gb)
    assert cycles == 8
    assert_registers(gb, A=0b11111110, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_48(gb):
    """ BIT 1,B - Test what is the value of bit 1 """
    gb.cpu.register.B = 0b00000010
    cycles = op.code_cb_48(gb)
    assert cycles == 8
    assert_registers(gb, B=0b00000010, F=0b10100000)

    gb.cpu.register.B = 0b11111101
    cycles = op.code_cb_48(gb)
    assert cycles == 8
    assert_registers(gb, B=0b11111101, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_49(gb):
    """ BIT 1,C - Test what is the value of bit 1 """
    gb.cpu.register.C = 0b00000010
    cycles = op.code_cb_49(gb)
    assert cycles == 8
    assert_registers(gb, C=0b00000010, F=0b10100000)

    gb.cpu.register.C = 0b11111101
    cycles = op.code_cb_49(gb)
    assert cycles == 8
    assert_registers(gb, C=0b11111101, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_4a(gb):
    """ BIT 1,D - Test what is the value of bit 1 """
    gb.cpu.register.D = 0b00000010
    cycles = op.code_cb_4a(gb)
    assert cycles == 8
    assert_registers(gb, D=0b00000010, F=0b10100000)

    gb.cpu.register.D = 0b11111101
    cycles = op.code_cb_4a(gb)
    assert cycles == 8
    assert_registers(gb, D=0b11111101, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_4b(gb):
    """ BIT 1,E - Test what is the value of bit 1 """
    gb.cpu.register.E = 0b00000010
    cycles = op.code_cb_4b(gb)
    assert cycles == 8
    assert_registers(gb, E=0b00000010, F=0b10100000)

    gb.cpu.register.E = 0b11111101
    cycles = op.code_cb_4b(gb)
    assert cycles == 8
    assert_registers(gb, E=0b11111101, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_4c(gb):
    """ BIT 1,H - Test what is the value of bit 1 """
    gb.cpu.register.H = 0b00000010
    cycles = op.code_cb_4c(gb)
    assert cycles == 8
    assert_registers(gb, H=0b00000010, F=0b10100000)

    gb.cpu.register.H = 0b11111101
    cycles = op.code_cb_4c(gb)
    assert cycles == 8
    assert_registers(gb, H=0b11111101, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_4d(gb):
    """ BIT 1,L - Test what is the value of bit 1 """
    gb.cpu.register.L = 0b00000010
    cycles = op.code_cb_4d(gb)
    assert cycles == 8
    assert_registers(gb, L=0b00000010, F=0b10100000)

    gb.cpu.register.L = 0b11111101
    cycles = op.code_cb_4d(gb)
    assert cycles == 8
    assert_registers(gb, L=0b11111101, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_4e(gb):
    """ BIT 1,(HL) - Test what is the value of bit 1 """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b00000010)
    cycles = op.code_cb_4e(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b10100000)
    assert_memory(gb, {0x1010: 0b00000010})

    gb.memory.write_8bit(0x1010, 0b11111101)
    cycles = op.code_cb_4e(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b00100000)
    assert_memory(gb,{0x1010:0b11111101})


# noinspection PyShadowingNames
def test_code_cb_4f(gb):
    """ BIT 1,A - Test what is the value of bit 1 """
    gb.cpu.register.A = 0b00000010
    cycles = op.code_cb_4f(gb)
    assert cycles == 8
    assert_registers(gb, A=0b00000010, F=0b10100000)

    gb.cpu.register.A = 0b11111101
    cycles = op.code_cb_4f(gb)
    assert cycles == 8
    assert_registers(gb, A=0b11111101, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_50(gb):
    """ BIT 2,B - Test what is the value of bit 2 """
    gb.cpu.register.B = 0b00000100
    cycles = op.code_cb_50(gb)
    assert cycles == 8
    assert_registers(gb, B=0b00000100, F=0b10100000)

    gb.cpu.register.B = 0b11111011
    cycles = op.code_cb_50(gb)
    assert cycles == 8
    assert_registers(gb, B=0b11111011, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_51(gb):
    """ BIT 2,C - Test what is the value of bit 2 """
    gb.cpu.register.C = 0b00000100
    cycles = op.code_cb_51(gb)
    assert cycles == 8
    assert_registers(gb, C=0b00000100, F=0b10100000)

    gb.cpu.register.C = 0b11111011
    cycles = op.code_cb_51(gb)
    assert cycles == 8
    assert_registers(gb, C=0b11111011, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_52(gb):
    """ BIT 2,D - Test what is the value of bit 2 """
    gb.cpu.register.D = 0b00000100
    cycles = op.code_cb_52(gb)
    assert cycles == 8
    assert_registers(gb, D=0b00000100, F=0b10100000)

    gb.cpu.register.D = 0b11111011
    cycles = op.code_cb_52(gb)
    assert cycles == 8
    assert_registers(gb, D=0b11111011, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_53(gb):
    """ BIT 2,E - Test what is the value of bit 2 """
    gb.cpu.register.E = 0b00000100
    cycles = op.code_cb_53(gb)
    assert cycles == 8
    assert_registers(gb, E=0b00000100, F=0b10100000)

    gb.cpu.register.E = 0b11111011
    cycles = op.code_cb_53(gb)
    assert cycles == 8
    assert_registers(gb, E=0b11111011, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_54(gb):
    """ BIT 2,H - Test what is the value of bit 2 """
    gb.cpu.register.H = 0b00000100
    cycles = op.code_cb_54(gb)
    assert cycles == 8
    assert_registers(gb, H=0b00000100, F=0b10100000)

    gb.cpu.register.H = 0b11111011
    cycles = op.code_cb_54(gb)
    assert cycles == 8
    assert_registers(gb, H=0b11111011, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_55(gb):
    """ BIT 2,L - Test what is the value of bit 2 """
    gb.cpu.register.L = 0b00000100
    cycles = op.code_cb_55(gb)
    assert cycles == 8
    assert_registers(gb, L=0b00000100, F=0b10100000)

    gb.cpu.register.L = 0b11111011
    cycles = op.code_cb_55(gb)
    assert cycles == 8
    assert_registers(gb, L=0b11111011, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_56(gb):
    """ BIT 2,(HL) - Test what is the value of bit 2 """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b00000100)
    cycles = op.code_cb_56(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b10100000)
    assert_memory(gb, {0x1010: 0b00000100})

    gb.memory.write_8bit(0x1010, 0b11111011)
    cycles = op.code_cb_56(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b00100000)
    assert_memory(gb,{0x1010:0b11111011})


# noinspection PyShadowingNames
def test_code_cb_57(gb):
    """ BIT 2,A - Test what is the value of bit 2 """
    gb.cpu.register.A = 0b00000100
    cycles = op.code_cb_57(gb)
    assert cycles == 8
    assert_registers(gb, A=0b00000100, F=0b10100000)

    gb.cpu.register.A = 0b11111011
    cycles = op.code_cb_57(gb)
    assert cycles == 8
    assert_registers(gb, A=0b11111011, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_58(gb):
    """ BIT 3,B - Test what is the value of bit 3 """
    gb.cpu.register.B = 0b00001000
    cycles = op.code_cb_58(gb)
    assert cycles == 8
    assert_registers(gb, B=0b00001000, F=0b10100000)

    gb.cpu.register.B = 0b11110111
    cycles = op.code_cb_58(gb)
    assert cycles == 8
    assert_registers(gb, B=0b11110111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_59(gb):
    """ BIT 3,C - Test what is the value of bit 3 """
    gb.cpu.register.C = 0b00001000
    cycles = op.code_cb_59(gb)
    assert cycles == 8
    assert_registers(gb, C=0b00001000, F=0b10100000)

    gb.cpu.register.C = 0b11110111
    cycles = op.code_cb_59(gb)
    assert cycles == 8
    assert_registers(gb, C=0b11110111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_5a(gb):
    """ BIT 3,D - Test what is the value of bit 3 """
    gb.cpu.register.D = 0b00001000
    cycles = op.code_cb_5a(gb)
    assert cycles == 8
    assert_registers(gb, D=0b00001000, F=0b10100000)

    gb.cpu.register.D = 0b11110111
    cycles = op.code_cb_5a(gb)
    assert cycles == 8
    assert_registers(gb, D=0b11110111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_5b(gb):
    """ BIT 3,E - Test what is the value of bit 3 """
    gb.cpu.register.E = 0b00001000
    cycles = op.code_cb_5b(gb)
    assert cycles == 8
    assert_registers(gb, E=0b00001000, F=0b10100000)

    gb.cpu.register.E = 0b11110111
    cycles = op.code_cb_5b(gb)
    assert cycles == 8
    assert_registers(gb, E=0b11110111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_5c(gb):
    """ BIT 3,H - Test what is the value of bit 3 """
    gb.cpu.register.H = 0b00001000
    cycles = op.code_cb_5c(gb)
    assert cycles == 8
    assert_registers(gb, H=0b00001000, F=0b10100000)

    gb.cpu.register.H = 0b11110111
    cycles = op.code_cb_5c(gb)
    assert cycles == 8
    assert_registers(gb, H=0b11110111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_5d(gb):
    """ BIT 3,L - Test what is the value of bit 3 """
    gb.cpu.register.L = 0b00001000
    cycles = op.code_cb_5d(gb)
    assert cycles == 8
    assert_registers(gb, L=0b00001000, F=0b10100000)

    gb.cpu.register.L = 0b11110111
    cycles = op.code_cb_5d(gb)
    assert cycles == 8
    assert_registers(gb, L=0b11110111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_5e(gb):
    """ BIT 3,(HL) - Test what is the value of bit 3 """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b00001000)
    cycles = op.code_cb_5e(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b10100000)
    assert_memory(gb, {0x1010: 0b00001000})

    gb.memory.write_8bit(0x1010, 0b11110111)
    cycles = op.code_cb_5e(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b00100000)
    assert_memory(gb,{0x1010:0b11110111})


# noinspection PyShadowingNames
def test_code_cb_5f(gb):
    """ BIT 3,A - Test what is the value of bit 3 """
    gb.cpu.register.A = 0b00001000
    cycles = op.code_cb_5f(gb)
    assert cycles == 8
    assert_registers(gb, A=0b00001000, F=0b10100000)

    gb.cpu.register.A = 0b11110111
    cycles = op.code_cb_5f(gb)
    assert cycles == 8
    assert_registers(gb, A=0b11110111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_60(gb):
    """ BIT 4,B - Test what is the value of bit 4 """
    gb.cpu.register.B = 0b00010000
    cycles = op.code_cb_60(gb)
    assert cycles == 8
    assert_registers(gb, B=0b00010000, F=0b10100000)

    gb.cpu.register.B = 0b11101111
    cycles = op.code_cb_60(gb)
    assert cycles == 8
    assert_registers(gb, B=0b11101111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_61(gb):
    """ BIT 4,C - Test what is the value of bit 4 """
    gb.cpu.register.C = 0b00010000
    cycles = op.code_cb_61(gb)
    assert cycles == 8
    assert_registers(gb, C=0b00010000, F=0b10100000)

    gb.cpu.register.C = 0b11101111
    cycles = op.code_cb_61(gb)
    assert cycles == 8
    assert_registers(gb, C=0b11101111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_62(gb):
    """ BIT 4,D - Test what is the value of bit 4 """
    gb.cpu.register.D = 0b00010000
    cycles = op.code_cb_62(gb)
    assert cycles == 8
    assert_registers(gb, D=0b00010000, F=0b10100000)

    gb.cpu.register.D = 0b11101111
    cycles = op.code_cb_62(gb)
    assert cycles == 8
    assert_registers(gb, D=0b11101111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_63(gb):
    """ BIT 4,E - Test what is the value of bit 4 """
    gb.cpu.register.E = 0b00010000
    cycles = op.code_cb_63(gb)
    assert cycles == 8
    assert_registers(gb, E=0b00010000, F=0b10100000)

    gb.cpu.register.E = 0b11101111
    cycles = op.code_cb_63(gb)
    assert cycles == 8
    assert_registers(gb, E=0b11101111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_64(gb):
    """ BIT 4,H - Test what is the value of bit 4 """
    gb.cpu.register.H = 0b00010000
    cycles = op.code_cb_64(gb)
    assert cycles == 8
    assert_registers(gb, H=0b00010000, F=0b10100000)

    gb.cpu.register.H = 0b11101111
    cycles = op.code_cb_64(gb)
    assert cycles == 8
    assert_registers(gb, H=0b11101111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_65(gb):
    """ BIT 4,L - Test what is the value of bit 4 """
    gb.cpu.register.L = 0b00010000
    cycles = op.code_cb_65(gb)
    assert cycles == 8
    assert_registers(gb, L=0b00010000, F=0b10100000)

    gb.cpu.register.L = 0b11101111
    cycles = op.code_cb_65(gb)
    assert cycles == 8
    assert_registers(gb, L=0b11101111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_66(gb):
    """ BIT 4,(HL) - Test what is the value of bit 4 """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b00010000)
    cycles = op.code_cb_66(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b10100000)
    assert_memory(gb, {0x1010: 0b00010000})

    gb.memory.write_8bit(0x1010, 0b11101111)
    cycles = op.code_cb_66(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b00100000)
    assert_memory(gb,{0x1010:0b11101111})


# noinspection PyShadowingNames
def test_code_cb_67(gb):
    """ BIT 4,A - Test what is the value of bit 4 """
    gb.cpu.register.A = 0b00010000
    cycles = op.code_cb_67(gb)
    assert cycles == 8
    assert_registers(gb, A=0b00010000, F=0b10100000)

    gb.cpu.register.A = 0b11101111
    cycles = op.code_cb_67(gb)
    assert cycles == 8
    assert_registers(gb, A=0b11101111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_68(gb):
    """ BIT 5,B - Test what is the value of bit 5 """
    gb.cpu.register.B = 0b00100000
    cycles = op.code_cb_68(gb)
    assert cycles == 8
    assert_registers(gb, B=0b00100000, F=0b10100000)

    gb.cpu.register.B = 0b11011111
    cycles = op.code_cb_68(gb)
    assert cycles == 8
    assert_registers(gb, B=0b11011111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_69(gb):
    """ BIT 5,C - Test what is the value of bit 5 """
    gb.cpu.register.C = 0b00100000
    cycles = op.code_cb_69(gb)
    assert cycles == 8
    assert_registers(gb, C=0b00100000, F=0b10100000)

    gb.cpu.register.C = 0b11011111
    cycles = op.code_cb_69(gb)
    assert cycles == 8
    assert_registers(gb, C=0b11011111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_6a(gb):
    """ BIT 5,D - Test what is the value of bit 5 """
    gb.cpu.register.D = 0b00100000
    cycles = op.code_cb_6a(gb)
    assert cycles == 8
    assert_registers(gb, D=0b00100000, F=0b10100000)

    gb.cpu.register.D = 0b11011111
    cycles = op.code_cb_6a(gb)
    assert cycles == 8
    assert_registers(gb, D=0b11011111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_6b(gb):
    """ BIT 5,E - Test what is the value of bit 5 """
    gb.cpu.register.E = 0b00100000
    cycles = op.code_cb_6b(gb)
    assert cycles == 8
    assert_registers(gb, E=0b00100000, F=0b10100000)

    gb.cpu.register.E = 0b11011111
    cycles = op.code_cb_6b(gb)
    assert cycles == 8
    assert_registers(gb, E=0b11011111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_6c(gb):
    """ BIT 5,H - Test what is the value of bit 5 """
    gb.cpu.register.H = 0b00100000
    cycles = op.code_cb_6c(gb)
    assert cycles == 8
    assert_registers(gb, H=0b00100000, F=0b10100000)

    gb.cpu.register.H = 0b11011111
    cycles = op.code_cb_6c(gb)
    assert cycles == 8
    assert_registers(gb, H=0b11011111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_6d(gb):
    """ BIT 5,L - Test what is the value of bit 5 """
    gb.cpu.register.L = 0b00100000
    cycles = op.code_cb_6d(gb)
    assert cycles == 8
    assert_registers(gb, L=0b00100000, F=0b10100000)

    gb.cpu.register.L = 0b11011111
    cycles = op.code_cb_6d(gb)
    assert cycles == 8
    assert_registers(gb, L=0b11011111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_6e(gb):
    """ BIT 5,(HL) - Test what is the value of bit 5 """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b00100000)
    cycles = op.code_cb_6e(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b10100000)
    assert_memory(gb, {0x1010: 0b00100000})

    gb.memory.write_8bit(0x1010, 0b11011111)
    cycles = op.code_cb_6e(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b00100000)
    assert_memory(gb,{0x1010:0b11011111})


# noinspection PyShadowingNames
def test_code_cb_6f(gb):
    """ BIT 5,A - Test what is the value of bit 5 """
    gb.cpu.register.A = 0b00100000
    cycles = op.code_cb_6f(gb)
    assert cycles == 8
    assert_registers(gb, A=0b00100000, F=0b10100000)

    gb.cpu.register.A = 0b11011111
    cycles = op.code_cb_6f(gb)
    assert cycles == 8
    assert_registers(gb, A=0b11011111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_70(gb):
    """ BIT 6,B - Test what is the value of bit 6 """
    gb.cpu.register.B = 0b01000000
    cycles = op.code_cb_70(gb)
    assert cycles == 8
    assert_registers(gb, B=0b01000000, F=0b10100000)

    gb.cpu.register.B = 0b10111111
    cycles = op.code_cb_70(gb)
    assert cycles == 8
    assert_registers(gb, B=0b10111111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_71(gb):
    """ BIT 6,C - Test what is the value of bit 6 """
    gb.cpu.register.C = 0b01000000
    cycles = op.code_cb_71(gb)
    assert cycles == 8
    assert_registers(gb, C=0b01000000, F=0b10100000)

    gb.cpu.register.C = 0b10111111
    cycles = op.code_cb_71(gb)
    assert cycles == 8
    assert_registers(gb, C=0b10111111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_72(gb):
    """ BIT 6,D - Test what is the value of bit 6 """
    gb.cpu.register.D = 0b01000000
    cycles = op.code_cb_72(gb)
    assert cycles == 8
    assert_registers(gb, D=0b01000000, F=0b10100000)

    gb.cpu.register.D = 0b10111111
    cycles = op.code_cb_72(gb)
    assert cycles == 8
    assert_registers(gb, D=0b10111111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_73(gb):
    """ BIT 6,E - Test what is the value of bit 6 """
    gb.cpu.register.E = 0b01000000
    cycles = op.code_cb_73(gb)
    assert cycles == 8
    assert_registers(gb, E=0b01000000, F=0b10100000)

    gb.cpu.register.E = 0b10111111
    cycles = op.code_cb_73(gb)
    assert cycles == 8
    assert_registers(gb, E=0b10111111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_74(gb):
    """ BIT 6,H - Test what is the value of bit 6 """
    gb.cpu.register.H = 0b01000000
    cycles = op.code_cb_74(gb)
    assert cycles == 8
    assert_registers(gb, H=0b01000000, F=0b10100000)

    gb.cpu.register.H = 0b10111111
    cycles = op.code_cb_74(gb)
    assert cycles == 8
    assert_registers(gb, H=0b10111111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_75(gb):
    """ BIT 6,L - Test what is the value of bit 6 """
    gb.cpu.register.L = 0b01000000
    cycles = op.code_cb_75(gb)
    assert cycles == 8
    assert_registers(gb, L=0b01000000, F=0b10100000)

    gb.cpu.register.L = 0b10111111
    cycles = op.code_cb_75(gb)
    assert cycles == 8
    assert_registers(gb, L=0b10111111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_76(gb):
    """ BIT 6,(HL) - Test what is the value of bit 6 """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b01000000)
    cycles = op.code_cb_76(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b10100000)
    assert_memory(gb, {0x1010: 0b01000000})

    gb.memory.write_8bit(0x1010, 0b10111111)
    cycles = op.code_cb_76(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b00100000)
    assert_memory(gb,{0x1010:0b10111111})


# noinspection PyShadowingNames
def test_code_cb_77(gb):
    """ BIT 6,A - Test what is the value of bit 6 """
    gb.cpu.register.A = 0b01000000
    cycles = op.code_cb_77(gb)
    assert cycles == 8
    assert_registers(gb, A=0b01000000, F=0b10100000)

    gb.cpu.register.A = 0b10111111
    cycles = op.code_cb_77(gb)
    assert cycles == 8
    assert_registers(gb, A=0b10111111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_78(gb):
    """ BIT 7,B - Test what is the value of bit 7 """
    gb.cpu.register.B = 0b10000000
    cycles = op.code_cb_78(gb)
    assert cycles == 8
    assert_registers(gb, B=0b10000000, F=0b10100000)

    gb.cpu.register.B = 0b01111111
    cycles = op.code_cb_78(gb)
    assert cycles == 8
    assert_registers(gb, B=0b01111111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_79(gb):
    """ BIT 7,C - Test what is the value of bit 7 """
    gb.cpu.register.C = 0b10000000
    cycles = op.code_cb_79(gb)
    assert cycles == 8
    assert_registers(gb, C=0b10000000, F=0b10100000)

    gb.cpu.register.C = 0b01111111
    cycles = op.code_cb_79(gb)
    assert cycles == 8
    assert_registers(gb, C=0b01111111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_7a(gb):
    """ BIT 7,D - Test what is the value of bit 7 """
    gb.cpu.register.D = 0b10000000
    cycles = op.code_cb_7a(gb)
    assert cycles == 8
    assert_registers(gb, D=0b10000000, F=0b10100000)

    gb.cpu.register.D = 0b01111111
    cycles = op.code_cb_7a(gb)
    assert cycles == 8
    assert_registers(gb, D=0b01111111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_7b(gb):
    """ BIT 7,E - Test what is the value of bit 7 """
    gb.cpu.register.E = 0b10000000
    cycles = op.code_cb_7b(gb)
    assert cycles == 8
    assert_registers(gb, E=0b10000000, F=0b10100000)

    gb.cpu.register.E = 0b01111111
    cycles = op.code_cb_7b(gb)
    assert cycles == 8
    assert_registers(gb, E=0b01111111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_7c(gb):
    """ BIT 7,H - Test what is the value of bit 7 """
    gb.cpu.register.H = 0b10000000
    cycles = op.code_cb_7c(gb)
    assert cycles == 8
    assert_registers(gb, H=0b10000000, F=0b10100000)

    gb.cpu.register.H = 0b01111111
    cycles = op.code_cb_7c(gb)
    assert cycles == 8
    assert_registers(gb, H=0b01111111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_7d(gb):
    """ BIT 7,L - Test what is the value of bit 7 """
    gb.cpu.register.L = 0b10000000
    cycles = op.code_cb_7d(gb)
    assert cycles == 8
    assert_registers(gb, L=0b10000000, F=0b10100000)

    gb.cpu.register.L = 0b01111111
    cycles = op.code_cb_7d(gb)
    assert cycles == 8
    assert_registers(gb, L=0b01111111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_7e(gb):
    """ BIT 7,(HL) - Test what is the value of bit 7 """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b10000000)
    cycles = op.code_cb_7e(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b10100000)
    assert_memory(gb, {0x1010: 0b10000000})

    gb.memory.write_8bit(0x1010, 0b01111111)
    cycles = op.code_cb_7e(gb)
    assert cycles == 16
    assert_registers(gb, H=0x10, L=0x10, F=0b00100000)
    assert_memory(gb,{0x1010:0b01111111})


# noinspection PyShadowingNames
def test_code_cb_7f(gb):
    """ BIT 7,A - Test what is the value of bit 7 """
    gb.cpu.register.A = 0b10000000
    cycles = op.code_cb_7f(gb)
    assert cycles == 8
    assert_registers(gb, A=0b10000000, F=0b10100000)

    gb.cpu.register.A = 0b01111111
    cycles = op.code_cb_7f(gb)
    assert cycles == 8
    assert_registers(gb, A=0b01111111, F=0b00100000)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_80(gb):
    """ RES 0,B - Reset the specified bit """
    gb.cpu.register.B = 0b00000000
    cycle = op.code_cb_80(gb)
    assert cycle == 8
    assert_registers(gb, B=0b00000000)

    gb.cpu.register.B = 0b11111111
    cycle = op.code_cb_80(gb)
    assert cycle == 8
    assert_registers(gb, B=0b11111110)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_81(gb):
    """ RES 0,C - Reset the specified bit """
    gb.cpu.register.C = 0b00000000
    cycle = op.code_cb_81(gb)
    assert cycle == 8
    assert_registers(gb, C=0b00000000)

    gb.cpu.register.C = 0b11111111
    cycle = op.code_cb_81(gb)
    assert cycle == 8
    assert_registers(gb, C=0b11111110)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_82(gb):
    """ RES 0,D - Reset the specified bit """
    gb.cpu.register.D = 0b00000000
    cycle = op.code_cb_82(gb)
    assert cycle == 8
    assert_registers(gb, D=0b00000000)

    gb.cpu.register.D = 0b11111111
    cycle = op.code_cb_82(gb)
    assert cycle == 8
    assert_registers(gb, D=0b11111110)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_83(gb):
    """ RES 0,E - Reset the specified bit """
    gb.cpu.register.E = 0b00000000
    cycle = op.code_cb_83(gb)
    assert cycle == 8
    assert_registers(gb, E=0b00000000)

    gb.cpu.register.E = 0b11111111
    cycle = op.code_cb_83(gb)
    assert cycle == 8
    assert_registers(gb, E=0b11111110)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_84(gb):
    """ RES 0,H - Reset the specified bit """
    gb.cpu.register.H = 0b00000000
    cycle = op.code_cb_84(gb)
    assert cycle == 8
    assert_registers(gb, H=0b00000000)

    gb.cpu.register.H = 0b11111111
    cycle = op.code_cb_84(gb)
    assert cycle == 8
    assert_registers(gb, H=0b11111110)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_85(gb):
    """ RES 0,L - Reset the specified bit """
    gb.cpu.register.L = 0b00000000
    cycle = op.code_cb_85(gb)
    assert cycle == 8
    assert_registers(gb, L=0b00000000)

    gb.cpu.register.L = 0b11111111
    cycle = op.code_cb_85(gb)
    assert cycle == 8
    assert_registers(gb, L=0b11111110)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_86(gb):
    """ RES 0,(HL) - Reset the specified bit """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_86(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb)

    gb.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_86(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb,{0x1010:0b11111110})


# noinspection PyShadowingNames
def test_code_cb_87(gb):
    """ RES 0,A - Reset the specified bit """
    gb.cpu.register.A = 0b00000000
    cycle = op.code_cb_87(gb)
    assert cycle == 8
    assert_registers(gb, A=0b00000000)

    gb.cpu.register.A = 0b11111111
    cycle = op.code_cb_87(gb)
    assert cycle == 8
    assert_registers(gb, A=0b11111110)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_88(gb):
    """ RES 1,B - Reset the specified bit """
    gb.cpu.register.B = 0b00000000
    cycle = op.code_cb_88(gb)
    assert cycle == 8
    assert_registers(gb, B=0b00000000)

    gb.cpu.register.B = 0b11111111
    cycle = op.code_cb_88(gb)
    assert cycle == 8
    assert_registers(gb, B=0b11111101)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_89(gb):
    """ RES 1,C - Reset the specified bit """
    gb.cpu.register.C = 0b00000000
    cycle = op.code_cb_89(gb)
    assert cycle == 8
    assert_registers(gb, C=0b00000000)

    gb.cpu.register.C = 0b11111111
    cycle = op.code_cb_89(gb)
    assert cycle == 8
    assert_registers(gb, C=0b11111101)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_8a(gb):
    """ RES 1,D - Reset the specified bit """
    gb.cpu.register.D = 0b00000000
    cycle = op.code_cb_8a(gb)
    assert cycle == 8
    assert_registers(gb, D=0b00000000)

    gb.cpu.register.D = 0b11111111
    cycle = op.code_cb_8a(gb)
    assert cycle == 8
    assert_registers(gb, D=0b11111101)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_8b(gb):
    """ RES 1,E - Reset the specified bit """
    gb.cpu.register.E = 0b00000000
    cycle = op.code_cb_8b(gb)
    assert cycle == 8
    assert_registers(gb, E=0b00000000)

    gb.cpu.register.E = 0b11111111
    cycle = op.code_cb_8b(gb)
    assert cycle == 8
    assert_registers(gb, E=0b11111101)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_8c(gb):
    """ RES 1,H - Reset the specified bit """
    gb.cpu.register.H = 0b00000000
    cycle = op.code_cb_8c(gb)
    assert cycle == 8
    assert_registers(gb, H=0b00000000)

    gb.cpu.register.H = 0b11111111
    cycle = op.code_cb_8c(gb)
    assert cycle == 8
    assert_registers(gb, H=0b11111101)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_8d(gb):
    """ RES 1,L - Reset the specified bit """
    gb.cpu.register.L = 0b00000000
    cycle = op.code_cb_8d(gb)
    assert cycle == 8
    assert_registers(gb, L=0b00000000)

    gb.cpu.register.L = 0b11111111
    cycle = op.code_cb_8d(gb)
    assert cycle == 8
    assert_registers(gb, L=0b11111101)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_8e(gb):
    """ RES 1,(HL) - Reset the specified bit """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_8e(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb)

    gb.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_8e(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb,{0x1010:0b11111101})


# noinspection PyShadowingNames
def test_code_cb_8f(gb):
    """ RES 1,A - Reset the specified bit """
    gb.cpu.register.A = 0b00000000
    cycle = op.code_cb_8f(gb)
    assert cycle == 8
    assert_registers(gb, A=0b00000000)

    gb.cpu.register.A = 0b11111111
    cycle = op.code_cb_8f(gb)
    assert cycle == 8
    assert_registers(gb, A=0b11111101)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_90(gb):
    """ RES 2,B - Reset the specified bit """
    gb.cpu.register.B = 0b00000000
    cycle = op.code_cb_90(gb)
    assert cycle == 8
    assert_registers(gb, B=0b00000000)

    gb.cpu.register.B = 0b11111111
    cycle = op.code_cb_90(gb)
    assert cycle == 8
    assert_registers(gb, B=0b11111011)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_91(gb):
    """ RES 2,C - Reset the specified bit """
    gb.cpu.register.C = 0b00000000
    cycle = op.code_cb_91(gb)
    assert cycle == 8
    assert_registers(gb, C=0b00000000)

    gb.cpu.register.C = 0b11111111
    cycle = op.code_cb_91(gb)
    assert cycle == 8
    assert_registers(gb, C=0b11111011)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_92(gb):
    """ RES 2,D - Reset the specified bit """
    gb.cpu.register.D = 0b00000000
    cycle = op.code_cb_92(gb)
    assert cycle == 8
    assert_registers(gb, D=0b00000000)

    gb.cpu.register.D = 0b11111111
    cycle = op.code_cb_92(gb)
    assert cycle == 8
    assert_registers(gb, D=0b11111011)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_93(gb):
    """ RES 2,E - Reset the specified bit """
    gb.cpu.register.E = 0b00000000
    cycle = op.code_cb_93(gb)
    assert cycle == 8
    assert_registers(gb, E=0b00000000)

    gb.cpu.register.E = 0b11111111
    cycle = op.code_cb_93(gb)
    assert cycle == 8
    assert_registers(gb, E=0b11111011)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_94(gb):
    """ RES 2,H - Reset the specified bit """
    gb.cpu.register.H = 0b00000000
    cycle = op.code_cb_94(gb)
    assert cycle == 8
    assert_registers(gb, H=0b00000000)

    gb.cpu.register.H = 0b11111111
    cycle = op.code_cb_94(gb)
    assert cycle == 8
    assert_registers(gb, H=0b11111011)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_95(gb):
    """ RES 2,L - Reset the specified bit """
    gb.cpu.register.L = 0b00000000
    cycle = op.code_cb_95(gb)
    assert cycle == 8
    assert_registers(gb, L=0b00000000)

    gb.cpu.register.L = 0b11111111
    cycle = op.code_cb_95(gb)
    assert cycle == 8
    assert_registers(gb, L=0b11111011)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_96(gb):
    """ RES 2,(HL) - Reset the specified bit """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_96(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb)

    gb.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_96(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb,{0x1010:0b11111011})


# noinspection PyShadowingNames
def test_code_cb_97(gb):
    """ RES 2,A - Reset the specified bit """
    gb.cpu.register.A = 0b00000000
    cycle = op.code_cb_97(gb)
    assert cycle == 8
    assert_registers(gb, A=0b00000000)

    gb.cpu.register.A = 0b11111111
    cycle = op.code_cb_97(gb)
    assert cycle == 8
    assert_registers(gb, A=0b11111011)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_98(gb):
    """ RES 3,B - Reset the specified bit """
    gb.cpu.register.B = 0b00000000
    cycle = op.code_cb_98(gb)
    assert cycle == 8
    assert_registers(gb, B=0b00000000)

    gb.cpu.register.B = 0b11111111
    cycle = op.code_cb_98(gb)
    assert cycle == 8
    assert_registers(gb, B=0b11110111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_99(gb):
    """ RES 3,C - Reset the specified bit """
    gb.cpu.register.C = 0b00000000
    cycle = op.code_cb_99(gb)
    assert cycle == 8
    assert_registers(gb, C=0b00000000)

    gb.cpu.register.C = 0b11111111
    cycle = op.code_cb_99(gb)
    assert cycle == 8
    assert_registers(gb, C=0b11110111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_9a(gb):
    """ RES 3,D - Reset the specified bit """
    gb.cpu.register.D = 0b00000000
    cycle = op.code_cb_9a(gb)
    assert cycle == 8
    assert_registers(gb, D=0b00000000)

    gb.cpu.register.D = 0b11111111
    cycle = op.code_cb_9a(gb)
    assert cycle == 8
    assert_registers(gb, D=0b11110111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_9b(gb):
    """ RES 3,E - Reset the specified bit """
    gb.cpu.register.E = 0b00000000
    cycle = op.code_cb_9b(gb)
    assert cycle == 8
    assert_registers(gb, E=0b00000000)

    gb.cpu.register.E = 0b11111111
    cycle = op.code_cb_9b(gb)
    assert cycle == 8
    assert_registers(gb, E=0b11110111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_9c(gb):
    """ RES 3,H - Reset the specified bit """
    gb.cpu.register.H = 0b00000000
    cycle = op.code_cb_9c(gb)
    assert cycle == 8
    assert_registers(gb, H=0b00000000)

    gb.cpu.register.H = 0b11111111
    cycle = op.code_cb_9c(gb)
    assert cycle == 8
    assert_registers(gb, H=0b11110111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_9d(gb):
    """ RES 3,L - Reset the specified bit """
    gb.cpu.register.L = 0b00000000
    cycle = op.code_cb_9d(gb)
    assert cycle == 8
    assert_registers(gb, L=0b00000000)

    gb.cpu.register.L = 0b11111111
    cycle = op.code_cb_9d(gb)
    assert cycle == 8
    assert_registers(gb, L=0b11110111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_9e(gb):
    """ RES 3,(HL) - Reset the specified bit """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_9e(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb)

    gb.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_9e(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb,{0x1010:0b11110111})


# noinspection PyShadowingNames
def test_code_cb_9f(gb):
    """ RES 3,A - Reset the specified bit """
    gb.cpu.register.A = 0b00000000
    cycle = op.code_cb_9f(gb)
    assert cycle == 8
    assert_registers(gb, A=0b00000000)

    gb.cpu.register.A = 0b11111111
    cycle = op.code_cb_9f(gb)
    assert cycle == 8
    assert_registers(gb, A=0b11110111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_a0(gb):
    """ RES 4,B - Reset the specified bit """
    gb.cpu.register.B = 0b00000000
    cycle = op.code_cb_a0(gb)
    assert cycle == 8
    assert_registers(gb, B=0b00000000)

    gb.cpu.register.B = 0b11111111
    cycle = op.code_cb_a0(gb)
    assert cycle == 8
    assert_registers(gb, B=0b11101111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_a1(gb):
    """ RES 4,C - Reset the specified bit """
    gb.cpu.register.C = 0b00000000
    cycle = op.code_cb_a1(gb)
    assert cycle == 8
    assert_registers(gb, C=0b00000000)

    gb.cpu.register.C = 0b11111111
    cycle = op.code_cb_a1(gb)
    assert cycle == 8
    assert_registers(gb, C=0b11101111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_a2(gb):
    """ RES 4,D - Reset the specified bit """
    gb.cpu.register.D = 0b00000000
    cycle = op.code_cb_a2(gb)
    assert cycle == 8
    assert_registers(gb, D=0b00000000)

    gb.cpu.register.D = 0b11111111
    cycle = op.code_cb_a2(gb)
    assert cycle == 8
    assert_registers(gb, D=0b11101111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_a3(gb):
    """ RES 4,E - Reset the specified bit """
    gb.cpu.register.E = 0b00000000
    cycle = op.code_cb_a3(gb)
    assert cycle == 8
    assert_registers(gb, E=0b00000000)

    gb.cpu.register.E = 0b11111111
    cycle = op.code_cb_a3(gb)
    assert cycle == 8
    assert_registers(gb, E=0b11101111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_a4(gb):
    """ RES 4,H - Reset the specified bit """
    gb.cpu.register.H = 0b00000000
    cycle = op.code_cb_a4(gb)
    assert cycle == 8
    assert_registers(gb, H=0b00000000)

    gb.cpu.register.H = 0b11111111
    cycle = op.code_cb_a4(gb)
    assert cycle == 8
    assert_registers(gb, H=0b11101111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_a5(gb):
    """ RES 4,L - Reset the specified bit """
    gb.cpu.register.L = 0b00000000
    cycle = op.code_cb_a5(gb)
    assert cycle == 8
    assert_registers(gb, L=0b00000000)

    gb.cpu.register.L = 0b11111111
    cycle = op.code_cb_a5(gb)
    assert cycle == 8
    assert_registers(gb, L=0b11101111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_a6(gb):
    """ RES 4,(HL) - Reset the specified bit """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_a6(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb)

    gb.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_a6(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb,{0x1010:0b11101111})


# noinspection PyShadowingNames
def test_code_cb_a7(gb):
    """ RES 4,A - Reset the specified bit """
    gb.cpu.register.A = 0b00000000
    cycle = op.code_cb_a7(gb)
    assert cycle == 8
    assert_registers(gb, A=0b00000000)

    gb.cpu.register.A = 0b11111111
    cycle = op.code_cb_a7(gb)
    assert cycle == 8
    assert_registers(gb, A=0b11101111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_a8(gb):
    """ RES 5,B - Reset the specified bit """
    gb.cpu.register.B = 0b00000000
    cycle = op.code_cb_a8(gb)
    assert cycle == 8
    assert_registers(gb, B=0b00000000)

    gb.cpu.register.B = 0b11111111
    cycle = op.code_cb_a8(gb)
    assert cycle == 8
    assert_registers(gb, B=0b11011111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_a9(gb):
    """ RES 5,C - Reset the specified bit """
    gb.cpu.register.C = 0b00000000
    cycle = op.code_cb_a9(gb)
    assert cycle == 8
    assert_registers(gb, C=0b00000000)

    gb.cpu.register.C = 0b11111111
    cycle = op.code_cb_a9(gb)
    assert cycle == 8
    assert_registers(gb, C=0b11011111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_aa(gb):
    """ RES 5,D - Reset the specified bit """
    gb.cpu.register.D = 0b00000000
    cycle = op.code_cb_aa(gb)
    assert cycle == 8
    assert_registers(gb, D=0b00000000)

    gb.cpu.register.D = 0b11111111
    cycle = op.code_cb_aa(gb)
    assert cycle == 8
    assert_registers(gb, D=0b11011111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_ab(gb):
    """ RES 5,E - Reset the specified bit """
    gb.cpu.register.E = 0b00000000
    cycle = op.code_cb_ab(gb)
    assert cycle == 8
    assert_registers(gb, E=0b00000000)

    gb.cpu.register.E = 0b11111111
    cycle = op.code_cb_ab(gb)
    assert cycle == 8
    assert_registers(gb, E=0b11011111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_ac(gb):
    """ RES 5,H - Reset the specified bit """
    gb.cpu.register.H = 0b00000000
    cycle = op.code_cb_ac(gb)
    assert cycle == 8
    assert_registers(gb, H=0b00000000)

    gb.cpu.register.H = 0b11111111
    cycle = op.code_cb_ac(gb)
    assert cycle == 8
    assert_registers(gb, H=0b11011111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_ad(gb):
    """ RES 5,L - Reset the specified bit """
    gb.cpu.register.L = 0b00000000
    cycle = op.code_cb_ad(gb)
    assert cycle == 8
    assert_registers(gb, L=0b00000000)

    gb.cpu.register.L = 0b11111111
    cycle = op.code_cb_ad(gb)
    assert cycle == 8
    assert_registers(gb, L=0b11011111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_ae(gb):
    """ RES 5,(HL) - Reset the specified bit """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_ae(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb)

    gb.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_ae(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb,{0x1010:0b11011111})


# noinspection PyShadowingNames
def test_code_cb_af(gb):
    """ RES 5,A - Reset the specified bit """
    gb.cpu.register.A = 0b00000000
    cycle = op.code_cb_af(gb)
    assert cycle == 8
    assert_registers(gb, A=0b00000000)

    gb.cpu.register.A = 0b11111111
    cycle = op.code_cb_af(gb)
    assert cycle == 8
    assert_registers(gb, A=0b11011111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_b0(gb):
    """ RES 6,B - Reset the specified bit """
    gb.cpu.register.B = 0b00000000
    cycle = op.code_cb_b0(gb)
    assert cycle == 8
    assert_registers(gb, B=0b00000000)

    gb.cpu.register.B = 0b11111111
    cycle = op.code_cb_b0(gb)
    assert cycle == 8
    assert_registers(gb, B=0b10111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_b1(gb):
    """ RES 6,C - Reset the specified bit """
    gb.cpu.register.C = 0b00000000
    cycle = op.code_cb_b1(gb)
    assert cycle == 8
    assert_registers(gb, C=0b00000000)

    gb.cpu.register.C = 0b11111111
    cycle = op.code_cb_b1(gb)
    assert cycle == 8
    assert_registers(gb, C=0b10111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_b2(gb):
    """ RES 6,D - Reset the specified bit """
    gb.cpu.register.D = 0b00000000
    cycle = op.code_cb_b2(gb)
    assert cycle == 8
    assert_registers(gb, D=0b00000000)

    gb.cpu.register.D = 0b11111111
    cycle = op.code_cb_b2(gb)
    assert cycle == 8
    assert_registers(gb, D=0b10111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_b3(gb):
    """ RES 6,E - Reset the specified bit """
    gb.cpu.register.E = 0b00000000
    cycle = op.code_cb_b3(gb)
    assert cycle == 8
    assert_registers(gb, E=0b00000000)

    gb.cpu.register.E = 0b11111111
    cycle = op.code_cb_b3(gb)
    assert cycle == 8
    assert_registers(gb, E=0b10111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_b4(gb):
    """ RES 6,H - Reset the specified bit """
    gb.cpu.register.H = 0b00000000
    cycle = op.code_cb_b4(gb)
    assert cycle == 8
    assert_registers(gb, H=0b00000000)

    gb.cpu.register.H = 0b11111111
    cycle = op.code_cb_b4(gb)
    assert cycle == 8
    assert_registers(gb, H=0b10111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_b5(gb):
    """ RES 6,L - Reset the specified bit """
    gb.cpu.register.L = 0b00000000
    cycle = op.code_cb_b5(gb)
    assert cycle == 8
    assert_registers(gb, L=0b00000000)

    gb.cpu.register.L = 0b11111111
    cycle = op.code_cb_b5(gb)
    assert cycle == 8
    assert_registers(gb, L=0b10111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_b6(gb):
    """ RES 6,(HL) - Reset the specified bit """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_b6(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb)

    gb.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_b6(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb,{0x1010:0b10111111})


# noinspection PyShadowingNames
def test_code_cb_b7(gb):
    """ RES 6,A - Reset the specified bit """
    gb.cpu.register.A = 0b00000000
    cycle = op.code_cb_b7(gb)
    assert cycle == 8
    assert_registers(gb, A=0b00000000)

    gb.cpu.register.A = 0b11111111
    cycle = op.code_cb_b7(gb)
    assert cycle == 8
    assert_registers(gb, A=0b10111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_b8(gb):
    """ RES 7,B - Reset the specified bit """
    gb.cpu.register.B = 0b00000000
    cycle = op.code_cb_b8(gb)
    assert cycle == 8
    assert_registers(gb, B=0b00000000)

    gb.cpu.register.B = 0b11111111
    cycle = op.code_cb_b8(gb)
    assert cycle == 8
    assert_registers(gb, B=0b01111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_b9(gb):
    """ RES 7,C - Reset the specified bit """
    gb.cpu.register.C = 0b00000000
    cycle = op.code_cb_b9(gb)
    assert cycle == 8
    assert_registers(gb, C=0b00000000)

    gb.cpu.register.C = 0b11111111
    cycle = op.code_cb_b9(gb)
    assert cycle == 8
    assert_registers(gb, C=0b01111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_ba(gb):
    """ RES 7,D - Reset the specified bit """
    gb.cpu.register.D = 0b00000000
    cycle = op.code_cb_ba(gb)
    assert cycle == 8
    assert_registers(gb, D=0b00000000)

    gb.cpu.register.D = 0b11111111
    cycle = op.code_cb_ba(gb)
    assert cycle == 8
    assert_registers(gb, D=0b01111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_bb(gb):
    """ RES 7,E - Reset the specified bit """
    gb.cpu.register.E = 0b00000000
    cycle = op.code_cb_bb(gb)
    assert cycle == 8
    assert_registers(gb, E=0b00000000)

    gb.cpu.register.E = 0b11111111
    cycle = op.code_cb_bb(gb)
    assert cycle == 8
    assert_registers(gb, E=0b01111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_bc(gb):
    """ RES 7,H - Reset the specified bit """
    gb.cpu.register.H = 0b00000000
    cycle = op.code_cb_bc(gb)
    assert cycle == 8
    assert_registers(gb, H=0b00000000)

    gb.cpu.register.H = 0b11111111
    cycle = op.code_cb_bc(gb)
    assert cycle == 8
    assert_registers(gb, H=0b01111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_bd(gb):
    """ RES 7,L - Reset the specified bit """
    gb.cpu.register.L = 0b00000000
    cycle = op.code_cb_bd(gb)
    assert cycle == 8
    assert_registers(gb, L=0b00000000)

    gb.cpu.register.L = 0b11111111
    cycle = op.code_cb_bd(gb)
    assert cycle == 8
    assert_registers(gb, L=0b01111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_be(gb):
    """ RES 7,(HL) - Reset the specified bit """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_be(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb)

    gb.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_be(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb,{0x1010:0b01111111})


# noinspection PyShadowingNames
def test_code_cb_bf(gb):
    """ RES 7,A - Reset the specified bit """
    gb.cpu.register.A = 0b00000000
    cycle = op.code_cb_bf(gb)
    assert cycle == 8
    assert_registers(gb, A=0b00000000)

    gb.cpu.register.A = 0b11111111
    cycle = op.code_cb_bf(gb)
    assert cycle == 8
    assert_registers(gb, A=0b01111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_c0(gb):
    """ SET 0,B - Set the specified bit """
    gb.cpu.register.B = 0b00000000
    cycle = op.code_cb_c0(gb)
    assert cycle == 8
    assert_registers(gb, B=0b00000001)

    gb.cpu.register.B = 0b11111111
    cycle = op.code_cb_c0(gb)
    assert cycle == 8
    assert_registers(gb, B=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_c1(gb):
    """ SET 0,C - Set the specified bit """
    gb.cpu.register.C = 0b00000000
    cycle = op.code_cb_c1(gb)
    assert cycle == 8
    assert_registers(gb, C=0b00000001)

    gb.cpu.register.C = 0b11111111
    cycle = op.code_cb_c1(gb)
    assert cycle == 8
    assert_registers(gb, C=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_c2(gb):
    """ SET 0,D - Set the specified bit """
    gb.cpu.register.D = 0b00000000
    cycle = op.code_cb_c2(gb)
    assert cycle == 8
    assert_registers(gb, D=0b00000001)

    gb.cpu.register.D = 0b11111111
    cycle = op.code_cb_c2(gb)
    assert cycle == 8
    assert_registers(gb, D=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_c3(gb):
    """ SET 0,E - Set the specified bit """
    gb.cpu.register.E = 0b00000000
    cycle = op.code_cb_c3(gb)
    assert cycle == 8
    assert_registers(gb, E=0b00000001)

    gb.cpu.register.E = 0b11111111
    cycle = op.code_cb_c3(gb)
    assert cycle == 8
    assert_registers(gb, E=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_c4(gb):
    """ SET 0,H - Set the specified bit """
    gb.cpu.register.H = 0b00000000
    cycle = op.code_cb_c4(gb)
    assert cycle == 8
    assert_registers(gb, H=0b00000001)

    gb.cpu.register.H = 0b11111111
    cycle = op.code_cb_c4(gb)
    assert cycle == 8
    assert_registers(gb, H=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_c5(gb):
    """ SET 0,L - Set the specified bit """
    gb.cpu.register.L = 0b00000000
    cycle = op.code_cb_c5(gb)
    assert cycle == 8
    assert_registers(gb, L=0b00000001)

    gb.cpu.register.L = 0b11111111
    cycle = op.code_cb_c5(gb)
    assert cycle == 8
    assert_registers(gb, L=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_c6(gb):
    """ SET 0,(HL) - Set the specified bit """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_c6(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb, {0x1010: 0b00000001})

    gb.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_c6(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb,{0x1010:0b11111111})


# noinspection PyShadowingNames
def test_code_cb_c7(gb):
    """ SET 0,A - Set the specified bit """
    gb.cpu.register.A = 0b00000000
    cycle = op.code_cb_c7(gb)
    assert cycle == 8
    assert_registers(gb, A=0b00000001)

    gb.cpu.register.A = 0b11111111
    cycle = op.code_cb_c7(gb)
    assert cycle == 8
    assert_registers(gb, A=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_c8(gb):
    """ SET 1,B - Set the specified bit """
    gb.cpu.register.B = 0b00000000
    cycle = op.code_cb_c8(gb)
    assert cycle == 8
    assert_registers(gb, B=0b00000010)

    gb.cpu.register.B = 0b11111111
    cycle = op.code_cb_c8(gb)
    assert cycle == 8
    assert_registers(gb, B=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_c9(gb):
    """ SET 1,C - Set the specified bit """
    gb.cpu.register.C = 0b00000000
    cycle = op.code_cb_c9(gb)
    assert cycle == 8
    assert_registers(gb, C=0b00000010)

    gb.cpu.register.C = 0b11111111
    cycle = op.code_cb_c9(gb)
    assert cycle == 8
    assert_registers(gb, C=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_ca(gb):
    """ SET 1,D - Set the specified bit """
    gb.cpu.register.D = 0b00000000
    cycle = op.code_cb_ca(gb)
    assert cycle == 8
    assert_registers(gb, D=0b00000010)

    gb.cpu.register.D = 0b11111111
    cycle = op.code_cb_ca(gb)
    assert cycle == 8
    assert_registers(gb, D=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_cb(gb):
    """ SET 1,E - Set the specified bit """
    gb.cpu.register.E = 0b00000000
    cycle = op.code_cb_cb(gb)
    assert cycle == 8
    assert_registers(gb, E=0b00000010)

    gb.cpu.register.E = 0b11111111
    cycle = op.code_cb_cb(gb)
    assert cycle == 8
    assert_registers(gb, E=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_cc(gb):
    """ SET 1,H - Set the specified bit """
    gb.cpu.register.H = 0b00000000
    cycle = op.code_cb_cc(gb)
    assert cycle == 8
    assert_registers(gb, H=0b00000010)

    gb.cpu.register.H = 0b11111111
    cycle = op.code_cb_cc(gb)
    assert cycle == 8
    assert_registers(gb, H=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_cd(gb):
    """ SET 1,L - Set the specified bit """
    gb.cpu.register.L = 0b00000000
    cycle = op.code_cb_cd(gb)
    assert cycle == 8
    assert_registers(gb, L=0b00000010)

    gb.cpu.register.L = 0b11111111
    cycle = op.code_cb_cd(gb)
    assert cycle == 8
    assert_registers(gb, L=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_ce(gb):
    """ SET 1,(HL) - Set the specified bit """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_ce(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb, {0x1010: 0b00000010})

    gb.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_ce(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb,{0x1010:0b11111111})


# noinspection PyShadowingNames
def test_code_cb_cf(gb):
    """ SET 1,A - Set the specified bit """
    gb.cpu.register.A = 0b00000000
    cycle = op.code_cb_cf(gb)
    assert cycle == 8
    assert_registers(gb, A=0b00000010)

    gb.cpu.register.A = 0b11111111
    cycle = op.code_cb_cf(gb)
    assert cycle == 8
    assert_registers(gb, A=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_d0(gb):
    """ SET 2,B - Set the specified bit """
    gb.cpu.register.B = 0b00000000
    cycle = op.code_cb_d0(gb)
    assert cycle == 8
    assert_registers(gb, B=0b00000100)

    gb.cpu.register.B = 0b11111111
    cycle = op.code_cb_d0(gb)
    assert cycle == 8
    assert_registers(gb, B=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_d1(gb):
    """ SET 2,C - Set the specified bit """
    gb.cpu.register.C = 0b00000000
    cycle = op.code_cb_d1(gb)
    assert cycle == 8
    assert_registers(gb, C=0b00000100)

    gb.cpu.register.C = 0b11111111
    cycle = op.code_cb_d1(gb)
    assert cycle == 8
    assert_registers(gb, C=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_d2(gb):
    """ SET 2,D - Set the specified bit """
    gb.cpu.register.D = 0b00000000
    cycle = op.code_cb_d2(gb)
    assert cycle == 8
    assert_registers(gb, D=0b00000100)

    gb.cpu.register.D = 0b11111111
    cycle = op.code_cb_d2(gb)
    assert cycle == 8
    assert_registers(gb, D=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_d3(gb):
    """ SET 2,E - Set the specified bit """
    gb.cpu.register.E = 0b00000000
    cycle = op.code_cb_d3(gb)
    assert cycle == 8
    assert_registers(gb, E=0b00000100)

    gb.cpu.register.E = 0b11111111
    cycle = op.code_cb_d3(gb)
    assert cycle == 8
    assert_registers(gb, E=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_d4(gb):
    """ SET 2,H - Set the specified bit """
    gb.cpu.register.H = 0b00000000
    cycle = op.code_cb_d4(gb)
    assert cycle == 8
    assert_registers(gb, H=0b00000100)

    gb.cpu.register.H = 0b11111111
    cycle = op.code_cb_d4(gb)
    assert cycle == 8
    assert_registers(gb, H=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_d5(gb):
    """ SET 2,L - Set the specified bit """
    gb.cpu.register.L = 0b00000000
    cycle = op.code_cb_d5(gb)
    assert cycle == 8
    assert_registers(gb, L=0b00000100)

    gb.cpu.register.L = 0b11111111
    cycle = op.code_cb_d5(gb)
    assert cycle == 8
    assert_registers(gb, L=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_d6(gb):
    """ SET 2,(HL) - Set the specified bit """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_d6(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb, {0x1010: 0b00000100})

    gb.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_d6(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb,{0x1010:0b11111111})


# noinspection PyShadowingNames
def test_code_cb_d7(gb):
    """ SET 2,A - Set the specified bit """
    gb.cpu.register.A = 0b00000000
    cycle = op.code_cb_d7(gb)
    assert cycle == 8
    assert_registers(gb, A=0b00000100)

    gb.cpu.register.A = 0b11111111
    cycle = op.code_cb_d7(gb)
    assert cycle == 8
    assert_registers(gb, A=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_d8(gb):
    """ SET 3,B - Set the specified bit """
    gb.cpu.register.B = 0b00000000
    cycle = op.code_cb_d8(gb)
    assert cycle == 8
    assert_registers(gb, B=0b00001000)

    gb.cpu.register.B = 0b11111111
    cycle = op.code_cb_d8(gb)
    assert cycle == 8
    assert_registers(gb, B=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_d9(gb):
    """ SET 3,C - Set the specified bit """
    gb.cpu.register.C = 0b00000000
    cycle = op.code_cb_d9(gb)
    assert cycle == 8
    assert_registers(gb, C=0b00001000)

    gb.cpu.register.C = 0b11111111
    cycle = op.code_cb_d9(gb)
    assert cycle == 8
    assert_registers(gb, C=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_da(gb):
    """ SET 3,D - Set the specified bit """
    gb.cpu.register.D = 0b00000000
    cycle = op.code_cb_da(gb)
    assert cycle == 8
    assert_registers(gb, D=0b00001000)

    gb.cpu.register.D = 0b11111111
    cycle = op.code_cb_da(gb)
    assert cycle == 8
    assert_registers(gb, D=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_db(gb):
    """ SET 3,E - Set the specified bit """
    gb.cpu.register.E = 0b00000000
    cycle = op.code_cb_db(gb)
    assert cycle == 8
    assert_registers(gb, E=0b00001000)

    gb.cpu.register.E = 0b11111111
    cycle = op.code_cb_db(gb)
    assert cycle == 8
    assert_registers(gb, E=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_dc(gb):
    """ SET 3,H - Set the specified bit """
    gb.cpu.register.H = 0b00000000
    cycle = op.code_cb_dc(gb)
    assert cycle == 8
    assert_registers(gb, H=0b00001000)

    gb.cpu.register.H = 0b11111111
    cycle = op.code_cb_dc(gb)
    assert cycle == 8
    assert_registers(gb, H=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_dd(gb):
    """ SET 3,L - Set the specified bit """
    gb.cpu.register.L = 0b00000000
    cycle = op.code_cb_dd(gb)
    assert cycle == 8
    assert_registers(gb, L=0b00001000)

    gb.cpu.register.L = 0b11111111
    cycle = op.code_cb_dd(gb)
    assert cycle == 8
    assert_registers(gb, L=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_de(gb):
    """ SET 3,(HL) - Set the specified bit """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_de(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb, {0x1010: 0b00001000})

    gb.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_de(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb,{0x1010:0b11111111})


# noinspection PyShadowingNames
def test_code_cb_df(gb):
    """ SET 3,A - Set the specified bit """
    gb.cpu.register.A = 0b00000000
    cycle = op.code_cb_df(gb)
    assert cycle == 8
    assert_registers(gb, A=0b00001000)

    gb.cpu.register.A = 0b11111111
    cycle = op.code_cb_df(gb)
    assert cycle == 8
    assert_registers(gb, A=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_e0(gb):
    """ SET 4,B - Set the specified bit """
    gb.cpu.register.B = 0b00000000
    cycle = op.code_cb_e0(gb)
    assert cycle == 8
    assert_registers(gb, B=0b00010000)

    gb.cpu.register.B = 0b11111111
    cycle = op.code_cb_e0(gb)
    assert cycle == 8
    assert_registers(gb, B=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_e1(gb):
    """ SET 4,C - Set the specified bit """
    gb.cpu.register.C = 0b00000000
    cycle = op.code_cb_e1(gb)
    assert cycle == 8
    assert_registers(gb, C=0b00010000)

    gb.cpu.register.C = 0b11111111
    cycle = op.code_cb_e1(gb)
    assert cycle == 8
    assert_registers(gb, C=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_e2(gb):
    """ SET 4,D - Set the specified bit """
    gb.cpu.register.D = 0b00000000
    cycle = op.code_cb_e2(gb)
    assert cycle == 8
    assert_registers(gb, D=0b00010000)

    gb.cpu.register.D = 0b11111111
    cycle = op.code_cb_e2(gb)
    assert cycle == 8
    assert_registers(gb, D=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_e3(gb):
    """ SET 4,E - Set the specified bit """
    gb.cpu.register.E = 0b00000000
    cycle = op.code_cb_e3(gb)
    assert cycle == 8
    assert_registers(gb, E=0b00010000)

    gb.cpu.register.E = 0b11111111
    cycle = op.code_cb_e3(gb)
    assert cycle == 8
    assert_registers(gb, E=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_e4(gb):
    """ SET 4,H - Set the specified bit """
    gb.cpu.register.H = 0b00000000
    cycle = op.code_cb_e4(gb)
    assert cycle == 8
    assert_registers(gb, H=0b00010000)

    gb.cpu.register.H = 0b11111111
    cycle = op.code_cb_e4(gb)
    assert cycle == 8
    assert_registers(gb, H=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_e5(gb):
    """ SET 4,L - Set the specified bit """
    gb.cpu.register.L = 0b00000000
    cycle = op.code_cb_e5(gb)
    assert cycle == 8
    assert_registers(gb, L=0b00010000)

    gb.cpu.register.L = 0b11111111
    cycle = op.code_cb_e5(gb)
    assert cycle == 8
    assert_registers(gb, L=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_e6(gb):
    """ SET 4,(HL) - Set the specified bit """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_e6(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb, {0x1010: 0b00010000})

    gb.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_e6(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb,{0x1010:0b11111111})


# noinspection PyShadowingNames
def test_code_cb_e7(gb):
    """ SET 4,A - Set the specified bit """
    gb.cpu.register.A = 0b00000000
    cycle = op.code_cb_e7(gb)
    assert cycle == 8
    assert_registers(gb, A=0b00010000)

    gb.cpu.register.A = 0b11111111
    cycle = op.code_cb_e7(gb)
    assert cycle == 8
    assert_registers(gb, A=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_e8(gb):
    """ SET 5,B - Set the specified bit """
    gb.cpu.register.B = 0b00000000
    cycle = op.code_cb_e8(gb)
    assert cycle == 8
    assert_registers(gb, B=0b00100000)

    gb.cpu.register.B = 0b11111111
    cycle = op.code_cb_e8(gb)
    assert cycle == 8
    assert_registers(gb, B=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_e9(gb):
    """ SET 5,C - Set the specified bit """
    gb.cpu.register.C = 0b00000000
    cycle = op.code_cb_e9(gb)
    assert cycle == 8
    assert_registers(gb, C=0b00100000)

    gb.cpu.register.C = 0b11111111
    cycle = op.code_cb_e9(gb)
    assert cycle == 8
    assert_registers(gb, C=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_ea(gb):
    """ SET 5,D - Set the specified bit """
    gb.cpu.register.D = 0b00000000
    cycle = op.code_cb_ea(gb)
    assert cycle == 8
    assert_registers(gb, D=0b00100000)

    gb.cpu.register.D = 0b11111111
    cycle = op.code_cb_ea(gb)
    assert cycle == 8
    assert_registers(gb, D=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_eb(gb):
    """ SET 5,E - Set the specified bit """
    gb.cpu.register.E = 0b00000000
    cycle = op.code_cb_eb(gb)
    assert cycle == 8
    assert_registers(gb, E=0b00100000)

    gb.cpu.register.E = 0b11111111
    cycle = op.code_cb_eb(gb)
    assert cycle == 8
    assert_registers(gb, E=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_ec(gb):
    """ SET 5,H - Set the specified bit """
    gb.cpu.register.H = 0b00000000
    cycle = op.code_cb_ec(gb)
    assert cycle == 8
    assert_registers(gb, H=0b00100000)

    gb.cpu.register.H = 0b11111111
    cycle = op.code_cb_ec(gb)
    assert cycle == 8
    assert_registers(gb, H=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_ed(gb):
    """ SET 5,L - Set the specified bit """
    gb.cpu.register.L = 0b00000000
    cycle = op.code_cb_ed(gb)
    assert cycle == 8
    assert_registers(gb, L=0b00100000)

    gb.cpu.register.L = 0b11111111
    cycle = op.code_cb_ed(gb)
    assert cycle == 8
    assert_registers(gb, L=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_ee(gb):
    """ SET 5,(HL) - Set the specified bit """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_ee(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb, {0x1010: 0b00100000})

    gb.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_ee(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb,{0x1010:0b11111111})


# noinspection PyShadowingNames
def test_code_cb_ef(gb):
    """ SET 5,A - Set the specified bit """
    gb.cpu.register.A = 0b00000000
    cycle = op.code_cb_ef(gb)
    assert cycle == 8
    assert_registers(gb, A=0b00100000)

    gb.cpu.register.A = 0b11111111
    cycle = op.code_cb_ef(gb)
    assert cycle == 8
    assert_registers(gb, A=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_f0(gb):
    """ SET 6,B - Set the specified bit """
    gb.cpu.register.B = 0b00000000
    cycle = op.code_cb_f0(gb)
    assert cycle == 8
    assert_registers(gb, B=0b01000000)

    gb.cpu.register.B = 0b11111111
    cycle = op.code_cb_f0(gb)
    assert cycle == 8
    assert_registers(gb, B=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_f1(gb):
    """ SET 6,C - Set the specified bit """
    gb.cpu.register.C = 0b00000000
    cycle = op.code_cb_f1(gb)
    assert cycle == 8
    assert_registers(gb, C=0b01000000)

    gb.cpu.register.C = 0b11111111
    cycle = op.code_cb_f1(gb)
    assert cycle == 8
    assert_registers(gb, C=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_f2(gb):
    """ SET 6,D - Set the specified bit """
    gb.cpu.register.D = 0b00000000
    cycle = op.code_cb_f2(gb)
    assert cycle == 8
    assert_registers(gb, D=0b01000000)

    gb.cpu.register.D = 0b11111111
    cycle = op.code_cb_f2(gb)
    assert cycle == 8
    assert_registers(gb, D=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_f3(gb):
    """ SET 6,E - Set the specified bit """
    gb.cpu.register.E = 0b00000000
    cycle = op.code_cb_f3(gb)
    assert cycle == 8
    assert_registers(gb, E=0b01000000)

    gb.cpu.register.E = 0b11111111
    cycle = op.code_cb_f3(gb)
    assert cycle == 8
    assert_registers(gb, E=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_f4(gb):
    """ SET 6,H - Set the specified bit """
    gb.cpu.register.H = 0b00000000
    cycle = op.code_cb_f4(gb)
    assert cycle == 8
    assert_registers(gb, H=0b01000000)

    gb.cpu.register.H = 0b11111111
    cycle = op.code_cb_f4(gb)
    assert cycle == 8
    assert_registers(gb, H=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_f5(gb):
    """ SET 6,L - Set the specified bit """
    gb.cpu.register.L = 0b00000000
    cycle = op.code_cb_f5(gb)
    assert cycle == 8
    assert_registers(gb, L=0b01000000)

    gb.cpu.register.L = 0b11111111
    cycle = op.code_cb_f5(gb)
    assert cycle == 8
    assert_registers(gb, L=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_f6(gb):
    """ SET 6,(HL) - Set the specified bit """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_f6(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb, {0x1010: 0b01000000})

    gb.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_f6(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb,{0x1010:0b11111111})


# noinspection PyShadowingNames
def test_code_cb_f7(gb):
    """ SET 6,A - Set the specified bit """
    gb.cpu.register.A = 0b00000000
    cycle = op.code_cb_f7(gb)
    assert cycle == 8
    assert_registers(gb, A=0b01000000)

    gb.cpu.register.A = 0b11111111
    cycle = op.code_cb_f7(gb)
    assert cycle == 8
    assert_registers(gb, A=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_f8(gb):
    """ SET 7,B - Set the specified bit """
    gb.cpu.register.B = 0b00000000
    cycle = op.code_cb_f8(gb)
    assert cycle == 8
    assert_registers(gb, B=0b10000000)

    gb.cpu.register.B = 0b11111111
    cycle = op.code_cb_f8(gb)
    assert cycle == 8
    assert_registers(gb, B=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_f9(gb):
    """ SET 7,C - Set the specified bit """
    gb.cpu.register.C = 0b00000000
    cycle = op.code_cb_f9(gb)
    assert cycle == 8
    assert_registers(gb, C=0b10000000)

    gb.cpu.register.C = 0b11111111
    cycle = op.code_cb_f9(gb)
    assert cycle == 8
    assert_registers(gb, C=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_fa(gb):
    """ SET 7,D - Set the specified bit """
    gb.cpu.register.D = 0b00000000
    cycle = op.code_cb_fa(gb)
    assert cycle == 8
    assert_registers(gb, D=0b10000000)

    gb.cpu.register.D = 0b11111111
    cycle = op.code_cb_fa(gb)
    assert cycle == 8
    assert_registers(gb, D=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_fb(gb):
    """ SET 7,E - Set the specified bit """
    gb.cpu.register.E = 0b00000000
    cycle = op.code_cb_fb(gb)
    assert cycle == 8
    assert_registers(gb, E=0b10000000)

    gb.cpu.register.E = 0b11111111
    cycle = op.code_cb_fb(gb)
    assert cycle == 8
    assert_registers(gb, E=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_fc(gb):
    """ SET 7,H - Set the specified bit """
    gb.cpu.register.H = 0b00000000
    cycle = op.code_cb_fc(gb)
    assert cycle == 8
    assert_registers(gb, H=0b10000000)

    gb.cpu.register.H = 0b11111111
    cycle = op.code_cb_fc(gb)
    assert cycle == 8
    assert_registers(gb, H=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_fd(gb):
    """ SET 7,L - Set the specified bit """
    gb.cpu.register.L = 0b00000000
    cycle = op.code_cb_fd(gb)
    assert cycle == 8
    assert_registers(gb, L=0b10000000)

    gb.cpu.register.L = 0b11111111
    cycle = op.code_cb_fd(gb)
    assert cycle == 8
    assert_registers(gb, L=0b11111111)

    assert_memory(gb)


# noinspection PyShadowingNames
def test_code_cb_fe(gb):
    """ SET 7,(HL) - Set the specified bit """
    gb.cpu.register.set_hl(0x1010)
    gb.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_fe(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb, {0x1010: 0b10000000})

    gb.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_fe(gb)
    assert cycle == 16
    assert_registers(gb, H=0x10, L=0x10)
    assert_memory(gb,{0x1010:0b11111111})


# noinspection PyShadowingNames
def test_code_cb_ff(gb):
    """ SET 7,A - Set the specified bit """
    gb.cpu.register.A = 0b00000000
    cycle = op.code_cb_ff(gb)
    assert cycle == 8
    assert_registers(gb, A=0b10000000)

    gb.cpu.register.A = 0b11111111
    cycle = op.code_cb_ff(gb)
    assert cycle == 8
    assert_registers(gb, A=0b11111111)

    assert_memory(gb)
