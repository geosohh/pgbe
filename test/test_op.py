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
def cpu_object():
    """
    Create Register instance for testing.
    :return: new register instance
    """
    from cpu import CPU
    return CPU()


"""
Tests
"""


def assert_registers(cpu_obj, A=0x00, F=0x00, B=0x00, C=0x00, D=0x00, E=0x00, H=0x00, L=0x00, SP=0xFFFE, PC=0x0100):
    """
    Helper function to assert registers values.
    For each register, checks if value is the same as the parameter. If no parameter received, checks default value.
    """
    assert cpu_obj.register.A == A
    assert cpu_obj.register.F == F
    assert cpu_obj.register.B == B
    assert cpu_obj.register.C == C
    assert cpu_obj.register.D == D
    assert cpu_obj.register.E == E
    assert cpu_obj.register.H == H
    assert cpu_obj.register.L == L
    assert cpu_obj.register.SP == SP
    assert cpu_obj.register.PC == PC


# noinspection PyProtectedMember
def assert_memory(cpu_obj, custom_address=None):
    """
    Helper function to assert memory values.
    If an address is not in the custom_address dictionary, will check for default value.
    :param cpu_obj:         CPU instance to access memory
    :param custom_address:  dict with format address:value
    """
    for address in range(0,len(cpu_obj.memory._memory_map)):
        if custom_address is not None and address in custom_address:
            if cpu_obj.memory._memory_map[address] != custom_address[address]:
                print("Memory address", hex(address), "contains", hex(cpu_obj.memory._memory_map[address]),
                      "instead of",hex(custom_address[address]))
            assert cpu_obj.memory._memory_map[address] == custom_address[address]
        else:
            if cpu_obj.memory._memory_map[address] != 0:
                print("Memory address", hex(address), "contains", hex(cpu_obj.memory._memory_map[address]),
                      "instead of",0)
            assert cpu_obj.memory._memory_map[address] == 0


# noinspection PyShadowingNames
def test_code_00(cpu_object):
    """ NOP - Does nothing """
    cycles = op.code_00(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_01(cpu_object):
    """ LD BC,d16 - Stores given 16-bit value at BC """
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("FF 55")
    cycles = op.code_01(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object,B=0x55,C=0xFF,PC=0x0002)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_02(cpu_object):
    """ LD (BC),A - Stores reg at the address in BC """
    cpu_object.register.set_bc(0x4050)
    cpu_object.register.A = 0x99
    cycles = op.code_02(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object,A=0x99,B=0x40,C=0x50)
    assert_memory(cpu_object,{0x4050:0x99})


# noinspection PyShadowingNames
def test_code_03(cpu_object):
    """ INC BC - BC=BC+1 """
    cpu_object.register.set_bc(0x0000)
    cycles = op.code_03(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0x00, C=0x01)

    cpu_object.register.set_bc(0x00FF)
    cycles = op.code_03(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0x01, C=0x00)

    cpu_object.register.set_bc(0x0FFF)
    cycles = op.code_03(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0x10, C=0x00)

    cpu_object.register.set_bc(0xFFFF)
    cycles = op.code_03(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0x00, C=0x00)

    assert_memory(cpu_object)

    
# noinspection PyShadowingNames
def test_code_04(cpu_object):
    """ INC B - B=B+1 """
    cpu_object.register.B = 0x00
    cycles = op.code_04(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, B=0x01, F=0b00000000)

    cpu_object.register.B = 0x0F
    cycles = op.code_04(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, B=0x10, F=0b00100000)

    cpu_object.register.B = 0xF0
    cycles = op.code_04(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, B=0xF1, F=0b00000000)

    cpu_object.register.B = 0xFF
    cycles = op.code_04(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, B=0x00, F=0b10100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_05(cpu_object):
    """ DEC B - B=B-1 """
    cpu_object.register.B = 0x00
    cycles = op.code_05(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, B=0xFF, F=0b01100000)

    cpu_object.register.B = 0x0F
    cycles = op.code_05(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, B=0x0E, F=0b01000000)

    cpu_object.register.B = 0x01
    cycles = op.code_05(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, B=0x00, F=0b11000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_06(cpu_object):
    """ LD B,d8 """
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("99")
    cycles = op.code_06(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object,B=0x99,PC=0x0001)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_07(cpu_object):
    """ RLCA - Copy register A bit 7 to Carry flag, then rotate register A left """
    cpu_object.register.A = 0b11100010
    cycles = op.code_07(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b11000101, F=0b00010000)

    cpu_object.register.A = 0b00000000
    cycles = op.code_07(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000000, F=0b10000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_08(cpu_object):
    """ LD (a16),SP - Set SP value into address (a16) """
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("22 FF")
    cpu_object.register.SP = 0x8842
    cycles = op.code_08(cpu_object)
    assert cycles == 20
    assert_registers(cpu_object,SP=0x8842,PC=0x0002)
    assert_memory(cpu_object,{0xFF22:0x42, 0xFF23:0x88})


# noinspection PyShadowingNames
def test_code_09(cpu_object):
    """ ADD HL,BC - HL=HL+BC """
    cpu_object.register.set_hl(0x0000)
    cpu_object.register.set_bc(0x0001)
    cycles = op.code_09(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0x00, C=0x01, H=0x00, L=0x01, F=0b00000000)

    cpu_object.register.set_hl(0x000F)
    cpu_object.register.set_bc(0x0001)
    cycles = op.code_09(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0x00, C=0x01, H=0x00, L=0x10, F=0b00000000)

    cpu_object.register.set_hl(0xF000)
    cpu_object.register.set_bc(0x1000)
    cycles = op.code_09(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0x10, C=0x00, H=0x00, L=0x00, F=0b00010000)

    cpu_object.register.set_hl(0x0FFF)
    cpu_object.register.set_bc(0x0001)
    cycles = op.code_09(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0x00, C=0x01, H=0x10, L=0x00, F=0b00100000)

    cpu_object.register.set_hl(0xFFFF)
    cpu_object.register.set_bc(0x0001)
    cycles = op.code_09(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0x00, C=0x01, H=0x00, L=0x00, F=0b00110000)

    cpu_object.register.set_hl(0xFFFF)
    cpu_object.register.set_bc(0x0002)
    cycles = op.code_09(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0x00, C=0x02, H=0x00, L=0x01, F=0b00110000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_0a(cpu_object):
    """ LD A,(BC) - Load reg with the value at the address in BC """
    cpu_object.memory.write_8bit(0x1234,0x11)
    cpu_object.register.set_bc(0x1234)
    cycles = op.code_0a(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object,A=0x11,B=0x12,C=0x34)
    assert_memory(cpu_object, {0x1234:0x11})


# noinspection PyShadowingNames
def test_code_0b(cpu_object):
    """ DEC BC - BC=BC-1 """
    cpu_object.register.set_bc(0x0000)
    cycles = op.code_0b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0xFF, C=0xFF)

    cpu_object.register.set_bc(0x0100)
    cycles = op.code_0b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0x00, C=0xFF)

    cpu_object.register.set_bc(0x1000)
    cycles = op.code_0b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0x0F, C=0xFF)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_0c(cpu_object):
    """ INC C - C=C+1 """
    cpu_object.register.C = 0x00
    cycles = op.code_0c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, C=0x01, F=0b00000000)

    cpu_object.register.C = 0x0F
    cycles = op.code_0c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, C=0x10, F=0b00100000)

    cpu_object.register.C = 0xF0
    cycles = op.code_0c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, C=0xF1, F=0b00000000)

    cpu_object.register.C = 0xFF
    cycles = op.code_0c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, C=0x00, F=0b10100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_0d(cpu_object):
    """ DEC C - C=C-1 """
    cpu_object.register.C = 0x00
    cycles = op.code_0d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, C=0xFF, F=0b01100000)

    cpu_object.register.C = 0x0F
    cycles = op.code_0d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, C=0x0E, F=0b01000000)

    cpu_object.register.C = 0x01
    cycles = op.code_0d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, C=0x00, F=0b11000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_0e(cpu_object):
    """ LD C,d8 """
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("99")
    cycles = op.code_0e(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object,C=0x99,PC=0x0001)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_0f(cpu_object):
    """ RRCA - Copy register A bit 0 to Carry flag, then rotate register A right """
    cpu_object.register.A = 0b11100011
    cycles = op.code_0f(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b11110001, F=0b00010000)

    cpu_object.register.A = 0b00000000
    cycles = op.code_0f(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000000, F=0b10000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_10(cpu_object):
    """
    STOP - Switch Game Boy into VERY low power standby mode. Halt CPU and LCD display until a button is pressed
    See: http://gbdev.gg8.se/wiki/articles/Reducing_Power_Consumption
    """
    cycles = op.code_10(cpu_object)
    assert cycles == 4
    assert cpu_object.stopped is True
    assert_registers(cpu_object)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_11(cpu_object):
    """ LD DE,d16 - Stores given 16-bit value at DE """
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("33 99")
    cycles = op.code_11(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object,D=0x99,E=0x33,PC=0x0002)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_12(cpu_object):
    """ LD (DE),A - Stores reg at the address in DE """
    cpu_object.register.set_de(0x0110)
    cpu_object.register.A = 0x66
    cycles = op.code_12(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object,A=0x66,D=0x01,E=0x10)
    assert_memory(cpu_object,{0x0110:0x66})


# noinspection PyShadowingNames
def test_code_13(cpu_object):
    """ INC DE - DE=DE+1 """
    cpu_object.register.set_de(0x0000)
    cycles = op.code_13(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0x00, E=0x01)

    cpu_object.register.set_de(0x00FF)
    cycles = op.code_13(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0x01, E=0x00)

    cpu_object.register.set_de(0x0FFF)
    cycles = op.code_13(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0x10, E=0x00)

    cpu_object.register.set_de(0xFFFF)
    cycles = op.code_13(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0x00, E=0x00)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_14(cpu_object):
    """ INC D - D=D+1 """
    cpu_object.register.D = 0x00
    cycles = op.code_14(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, D=0x01, F=0b00000000)

    cpu_object.register.D = 0x0F
    cycles = op.code_14(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, D=0x10, F=0b00100000)

    cpu_object.register.D = 0xF0
    cycles = op.code_14(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, D=0xF1, F=0b00000000)

    cpu_object.register.D = 0xFF
    cycles = op.code_14(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, D=0x00, F=0b10100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_15(cpu_object):
    """ DEC D - D=D-1 """
    cpu_object.register.D = 0x00
    cycles = op.code_15(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, D=0xFF, F=0b01100000)

    cpu_object.register.D = 0x0F
    cycles = op.code_15(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, D=0x0E, F=0b01000000)

    cpu_object.register.D = 0x01
    cycles = op.code_15(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, D=0x00, F=0b11000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_16(cpu_object):
    """ LD D,d8 """
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("99")
    cycles = op.code_16(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object,D=0x99,PC=0x0001)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_17(cpu_object):
    """ RLA - Copy register A bit 7 to temp, replace A bit 7 with Carry flag, rotate A left, copy temp to Carry flag """
    cpu_object.register.A = 0b11100010
    cpu_object.register.F = 0b00010000
    cycles = op.code_17(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b11000101, F=0b00010000)

    cpu_object.register.A = 0b00000000
    cpu_object.register.F = 0b00010000
    cycles = op.code_17(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000001, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_18(cpu_object):
    """ JP r8 - make the command at address (current address + r8) the next to be executed (r8 is signed) """
    cpu_object.register.PC = 0x0000
    cpu_object._cartridge_data = bytes.fromhex("03")
    cycles = op.code_18(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object,PC=0x0004)

    cpu_object.register.PC = 0x0000
    cpu_object._cartridge_data = bytes.fromhex("FD")  # -3
    cycles = op.code_18(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, PC=0xFFFE)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_19(cpu_object):
    """ ADD HL,DE - HL=HL+DE """
    cpu_object.register.set_hl(0x0000)
    cpu_object.register.set_de(0x0001)
    cycles = op.code_19(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0x00, E=0x01, H=0x00, L=0x01, F=0b00000000)

    cpu_object.register.set_hl(0x000F)
    cpu_object.register.set_de(0x0001)
    cycles = op.code_19(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0x00, E=0x01, H=0x00, L=0x10, F=0b00000000)

    cpu_object.register.set_hl(0xF000)
    cpu_object.register.set_de(0x1000)
    cycles = op.code_19(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0x10, E=0x00, H=0x00, L=0x00, F=0b00010000)

    cpu_object.register.set_hl(0x0FFF)
    cpu_object.register.set_de(0x0001)
    cycles = op.code_19(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0x00, E=0x01, H=0x10, L=0x00, F=0b00100000)

    cpu_object.register.set_hl(0xFFFF)
    cpu_object.register.set_de(0x0001)
    cycles = op.code_19(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0x00, E=0x01, H=0x00, L=0x00, F=0b00110000)

    cpu_object.register.set_hl(0xFFFF)
    cpu_object.register.set_de(0x0002)
    cycles = op.code_19(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0x00, E=0x02, H=0x00, L=0x01, F=0b00110000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_1a(cpu_object):
    """ LD A,(DE) - Load reg with the value at the address in DE """
    cpu_object.memory.write_8bit(0x1234, 0x11)
    cpu_object.register.set_de(0x1234)
    cycles = op.code_1a(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x11, D=0x12, E=0x34)
    assert_memory(cpu_object, {0x1234: 0x11})


# noinspection PyShadowingNames
def test_code_1b(cpu_object):
    """ DEC DE - DE=DE-1 """
    cpu_object.register.set_de(0x0000)
    cycles = op.code_1b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0xFF, E=0xFF)

    cpu_object.register.set_de(0x0100)
    cycles = op.code_1b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0x00, E=0xFF)

    cpu_object.register.set_de(0x1000)
    cycles = op.code_1b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0x0F, E=0xFF)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_1c(cpu_object):
    """ INC E - E=E+1 """
    cpu_object.register.E = 0x00
    cycles = op.code_1c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, E=0x01, F=0b00000000)

    cpu_object.register.E = 0x0F
    cycles = op.code_1c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, E=0x10, F=0b00100000)

    cpu_object.register.E = 0xF0
    cycles = op.code_1c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, E=0xF1, F=0b00000000)

    cpu_object.register.E = 0xFF
    cycles = op.code_1c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, E=0x00, F=0b10100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_1d(cpu_object):
    """ DEC E - E=E-1 """
    cpu_object.register.E = 0x00
    cycles = op.code_1d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, E=0xFF, F=0b01100000)

    cpu_object.register.E = 0x0F
    cycles = op.code_1d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, E=0x0E, F=0b01000000)

    cpu_object.register.E = 0x01
    cycles = op.code_1d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, E=0x00, F=0b11000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_1e(cpu_object):
    """ LD E,d8 """
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("99")
    cycles = op.code_1e(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object,E=0x99,PC=0x0001)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_1f(cpu_object):
    """ RRA - Copy register A bit 0 to temp, replace A bit 0 w/ Carry flag, rotate A right, copy temp to Carry flag """
    cpu_object.register.A = 0b11100011
    cpu_object.register.F = 0b00010000
    cycles = op.code_1f(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b11110001, F=0b00010000)

    cpu_object.register.A = 0b00000000
    cpu_object.register.F = 0b00010000
    cycles = op.code_1f(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b10000000, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_20(cpu_object):
    """ JR NZ,r8 - If flag Z is reset, add r8 to current address and jump to it """
    cpu_object.register.PC = 0x0000
    cpu_object.register.F = 0b00000000
    cpu_object._cartridge_data = bytes.fromhex("03")
    cycles = op.code_20(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, PC=0x0004)

    cpu_object.register.PC = 0x0000
    cpu_object.register.F = 0b10000000
    cpu_object._cartridge_data = bytes.fromhex("FD")  # -3
    cycles = op.code_20(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, PC=0x0001, F=0b10000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_21(cpu_object):
    """ LD HL,d16 - Stores given 16-bit value at HL """
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("33 99")
    cycles = op.code_21(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object,H=0x99,L=0x33, PC=0x0002)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_22(cpu_object):
    """ LD (HL+),A or LD (HLI),A or LDI (HL),A - Put value at A into address HL. Increment HL """
    cpu_object.register.A = 0x69
    cpu_object.register.set_hl(0x1010)
    cycles = op.code_22(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object,A=0x69,H=0x10,L=0x11)
    assert_memory(cpu_object,{0x1010:0x69})


# noinspection PyShadowingNames
def test_code_23(cpu_object):
    """ INC HL - HL=HL+1 """
    cpu_object.register.set_hl(0x0000)
    cycles = op.code_23(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0x00, L=0x01)

    cpu_object.register.set_hl(0x00FF)
    cycles = op.code_23(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0x01, L=0x00)

    cpu_object.register.set_hl(0x0FFF)
    cycles = op.code_23(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0x10, L=0x00)

    cpu_object.register.set_hl(0xFFFF)
    cycles = op.code_23(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0x00, L=0x00)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_24(cpu_object):
    """ INC H - H=H+1 """
    cpu_object.register.H = 0x00
    cycles = op.code_24(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, H=0x01, F=0b00000000)

    cpu_object.register.H = 0x0F
    cycles = op.code_24(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, H=0x10, F=0b00100000)

    cpu_object.register.H = 0xF0
    cycles = op.code_24(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, H=0xF1, F=0b00000000)

    cpu_object.register.H = 0xFF
    cycles = op.code_24(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, H=0x00, F=0b10100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_25(cpu_object):
    """ DEC H - H=H-1 """
    cpu_object.register.H = 0x00
    cycles = op.code_25(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, H=0xFF, F=0b01100000)

    cpu_object.register.H = 0x0F
    cycles = op.code_25(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, H=0x0E, F=0b01000000)

    cpu_object.register.H = 0x01
    cycles = op.code_25(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, H=0x00, F=0b11000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_26(cpu_object):
    """ LD H,d8 """
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("99")
    cycles = op.code_26(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object,H=0x99,PC=0x0001)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_27(cpu_object):
    """
    DAA - Adjust value in register A for Binary Coded Decimal representation (i.e. one 0-9 value per nibble)
    See:  http://gbdev.gg8.se/wiki/articles/DAA
    """
    cpu_object.register.A = 0b00111100  # 3|12 -> should be 4|2
    cpu_object.register.F = 0b00000000
    cycles = op.code_27(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b01000010, F=0b00000000)

    cpu_object.register.A = 0b01100100  # 6|4 -> should stay 6|4
    cpu_object.register.F = 0b00000000
    cycles = op.code_27(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b01100100, F=0b00000000)

    cpu_object.register.A = 0b10100000  # 10|0 -> should be 0|0 with Z flag
    cpu_object.register.F = 0b00000000
    cycles = op.code_27(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000000, F=0b10010000)

    cpu_object.register.A = 0b11000010  # 12|2 -> should be 2|2 with C flag
    cpu_object.register.F = 0b00000000
    cycles = op.code_27(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00100010, F=0b00010000)

    cpu_object.register.A = 0b00001010  # 0|10 with N/H flag-> should be 0|4
    cpu_object.register.F = 0b01100000
    cycles = op.code_27(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000100, F=0b01000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_28(cpu_object):
    """ JR Z,r8 - If flag Z is set, add r8 to current address and jump to it """
    cpu_object.register.PC = 0x0000
    cpu_object.register.F = 0b10000000
    cpu_object._cartridge_data = bytes.fromhex("03")
    cycles = op.code_28(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, PC=0x0004, F=0b10000000)

    cpu_object.register.PC = 0x0000
    cpu_object.register.F = 0b00000000
    cpu_object._cartridge_data = bytes.fromhex("FD")  # -3
    cycles = op.code_28(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, PC=0x0001)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_29(cpu_object):
    """ ADD HL,HL - HL=HL+HL """
    cpu_object.register.set_hl(0x0001)
    cycles = op.code_29(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0x00, L=0x02, F=0b00000000)

    cpu_object.register.set_hl(0x0008)
    cycles = op.code_29(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0x00, L=0x10, F=0b00000000)

    cpu_object.register.set_hl(0x8000)
    cycles = op.code_29(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0x00, L=0x00, F=0b00010000)

    cpu_object.register.set_hl(0x0800)
    cycles = op.code_29(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0x10, L=0x00, F=0b00100000)

    cpu_object.register.set_hl(0x8800)
    cycles = op.code_29(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0x10, L=0x00, F=0b00110000)

    cpu_object.register.set_hl(0xFFFF)
    cycles = op.code_29(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0xFF, L=0xFE, F=0b00110000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_2a(cpu_object):
    """ LD A,(HL+) or LD A,(HLI) or LDI A,(HL) - Put value at address HL into A. Increment HL """
    cpu_object.memory.write_8bit(0x1010,0x69)
    cpu_object.register.set_hl(0x1010)
    cycles = op.code_2a(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x69, H=0x10, L=0x11)
    assert_memory(cpu_object, {0x1010: 0x69})


# noinspection PyShadowingNames
def test_code_2b(cpu_object):
    """ DEC HL - HL=HL-1 """
    cpu_object.register.set_hl(0x0000)
    cycles = op.code_2b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0xFF, L=0xFF)

    cpu_object.register.set_hl(0x0100)
    cycles = op.code_2b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0x00, L=0xFF)

    cpu_object.register.set_hl(0x1000)
    cycles = op.code_2b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0x0F, L=0xFF)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_2c(cpu_object):
    """ INC L - L=L+1 """
    cpu_object.register.L = 0x00
    cycles = op.code_2c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, L=0x01, F=0b00000000)

    cpu_object.register.L = 0x0F
    cycles = op.code_2c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, L=0x10, F=0b00100000)

    cpu_object.register.L = 0xF0
    cycles = op.code_2c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, L=0xF1, F=0b00000000)

    cpu_object.register.L = 0xFF
    cycles = op.code_2c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, L=0x00, F=0b10100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_2d(cpu_object):
    """ DEC L - L=L-1 """
    cpu_object.register.L = 0x00
    cycles = op.code_2d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, L=0xFF, F=0b01100000)

    cpu_object.register.L = 0x0F
    cycles = op.code_2d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, L=0x0E, F=0b01000000)

    cpu_object.register.L = 0x01
    cycles = op.code_2d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, L=0x00, F=0b11000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_2e(cpu_object):
    """ LD L,d8 """
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("99")
    cycles = op.code_2e(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object,L=0x99,PC=0x0001)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_2f(cpu_object):
    """ CPL - Logical complement of register A (i.e. flip all bits) """
    cpu_object.register.A = 0b00111100
    cycles = op.code_2f(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b11000011, F=0b01100000)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_30(cpu_object):
    """ JR NC,r8 - If flag C is reset, add r8 to current address and jump to it """
    cpu_object.register.PC = 0x0000
    cpu_object.register.F = 0b00000000
    cpu_object._cartridge_data = bytes.fromhex("03")
    cycles = op.code_30(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, PC=0x0004)

    cpu_object.register.PC = 0x0000
    cpu_object.register.F = 0b00010000
    cpu_object._cartridge_data = bytes.fromhex("FD")  # -3
    cycles = op.code_30(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, PC=0x0001, F=0b00010000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_31(cpu_object):
    """ LD SP,d16 - Stores given 16-bit value at SP """
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("33 99")
    cycles = op.code_31(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, SP=0x9933, PC=0x0002)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_32(cpu_object):
    """ LD (HL-),A or LD (HLD),A or LDD (HL),A - Put value at A into address HL. Decrement HL """
    cpu_object.register.A = 0x69
    cpu_object.register.set_hl(0x1010)
    cycles = op.code_32(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x69, H=0x10, L=0x0F)
    assert_memory(cpu_object, {0x1010: 0x69})


# noinspection PyShadowingNames
def test_code_33(cpu_object):
    """ INC SP - SP=SP+1 """
    cpu_object.register.SP = 0x0000
    cycles = op.code_33(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, SP=0x0001)

    cpu_object.register.SP = 0x00FF
    cycles = op.code_33(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, SP=0x0100)

    cpu_object.register.SP = 0x0FFF
    cycles = op.code_33(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, SP=0x1000)

    cpu_object.register.SP = 0xFFFF
    cycles = op.code_33(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, SP=0x0000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_34(cpu_object):
    """ INC (HL) - (value at address HL)=(value at address HL)+1 """
    cpu_object.memory.write_8bit(0x1010,0x00)
    cpu_object.register.set_hl(0x1010)
    cycles = op.code_34(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b00000000)
    assert_memory(cpu_object,{0x1010:0x01})

    cpu_object.memory.write_8bit(0x1010, 0x0F)
    cpu_object.register.set_hl(0x1010)
    cycles = op.code_34(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b00100000)
    assert_memory(cpu_object, {0x1010: 0x10})

    cpu_object.memory.write_8bit(0x1010, 0xF0)
    cpu_object.register.set_hl(0x1010)
    cycles = op.code_34(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b00000000)
    assert_memory(cpu_object, {0x1010: 0xF1})

    cpu_object.memory.write_8bit(0x1010, 0xFF)
    cpu_object.register.set_hl(0x1010)
    cycles = op.code_34(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b10100000)
    assert_memory(cpu_object, {0x1010: 0x00})


# noinspection PyShadowingNames
def test_code_35(cpu_object):
    """ DEC (HL) - (value at address HL)=(value at address HL)-1 """
    cpu_object.memory.write_8bit(0x1010, 0x00)
    cpu_object.register.set_hl(0x1010)
    cycles = op.code_35(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b01100000)
    assert_memory(cpu_object, {0x1010: 0xFF})

    cpu_object.memory.write_8bit(0x1010, 0x0F)
    cpu_object.register.set_hl(0x1010)
    cycles = op.code_35(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b01000000)
    assert_memory(cpu_object, {0x1010: 0x0E})

    cpu_object.memory.write_8bit(0x1010, 0x01)
    cpu_object.register.set_hl(0x1010)
    cycles = op.code_35(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b11000000)
    assert_memory(cpu_object, {0x1010: 0x00})


# noinspection PyShadowingNames
def test_code_36(cpu_object):
    """ LD (HL),d8 - Stores d8 at the address in HL """
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("99")
    cpu_object.register.set_hl(0x1010)
    cycles = op.code_36(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, H=0x10, L=0x10, PC=0x0001)
    assert_memory(cpu_object, {0x1010:0x99})


# noinspection PyShadowingNames
def test_code_37(cpu_object):
    """ SCF - Set carry flag """
    cpu_object.register.F = 0b00000000
    cycles = op.code_37(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, F=0b00010000)

    cpu_object.register.F = 0b11110000
    cycles = op.code_37(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, F=0b10010000)


# noinspection PyShadowingNames
def test_code_38(cpu_object):
    """ JR C,r8 - If flag C is set, add r8 to current address and jump to it """
    cpu_object.register.PC = 0x0000
    cpu_object.register.F = 0b00010000
    cpu_object._cartridge_data = bytes.fromhex("03")
    cycles = op.code_38(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, PC=0x0004, F=0b00010000)

    cpu_object.register.PC = 0x0000
    cpu_object.register.F = 0b00000000
    cpu_object._cartridge_data = bytes.fromhex("FD")  # -3
    cycles = op.code_38(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, PC=0x0001)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_39(cpu_object):
    """ ADD HL,SP - HL=HL+SP """
    cpu_object.register.set_hl(0x0000)
    cpu_object.register.SP = 0x0001
    cycles = op.code_39(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, SP=0x0001, H=0x00, L=0x01, F=0b00000000)

    cpu_object.register.set_hl(0x000F)
    cpu_object.register.SP = 0x0001
    cycles = op.code_39(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, SP=0x0001, H=0x00, L=0x10, F=0b00000000)

    cpu_object.register.set_hl(0xF000)
    cpu_object.register.SP = 0x1000
    cycles = op.code_39(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, SP=0x1000, H=0x00, L=0x00, F=0b00010000)

    cpu_object.register.set_hl(0x0FFF)
    cpu_object.register.SP = 0x0001
    cycles = op.code_39(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, SP=0x0001, H=0x10, L=0x00, F=0b00100000)

    cpu_object.register.set_hl(0xFFFF)
    cpu_object.register.SP = 0x0001
    cycles = op.code_39(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, SP=0x0001, H=0x00, L=0x00, F=0b00110000)

    cpu_object.register.set_hl(0xFFFF)
    cpu_object.register.SP = 0x0002
    cycles = op.code_39(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, SP=0x0002, H=0x00, L=0x01, F=0b00110000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_3a(cpu_object):
    """ LD A,(HL-) or LD A,(HLD) or LDD A,(HL) - Put value at address HL into A. Decrement HL """
    cpu_object.memory.write_8bit(0x1010, 0x69)
    cpu_object.register.set_hl(0x1010)
    cycles = op.code_3a(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x69, H=0x10, L=0x0F)
    assert_memory(cpu_object, {0x1010: 0x69})


# noinspection PyShadowingNames
def test_code_3b(cpu_object):
    """ DEC SP - SP=SP-1 """
    cpu_object.register.SP = 0x0000
    cycles = op.code_3b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, SP=0xFFFF)

    cpu_object.register.SP = 0x0100
    cycles = op.code_3b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, SP=0x00FF)

    cpu_object.register.SP = 0x1000
    cycles = op.code_3b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, SP=0x0FFF)


# noinspection PyShadowingNames
def test_code_3c(cpu_object):
    """ INC A - A=A+1 """
    cpu_object.register.A = 0x00
    cycles = op.code_3c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, F=0b00000000)

    cpu_object.register.A = 0x0F
    cycles = op.code_3c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x10, F=0b00100000)

    cpu_object.register.A = 0xF0
    cycles = op.code_3c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xF1, F=0b00000000)

    cpu_object.register.A = 0xFF
    cycles = op.code_3c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, F=0b10100000)


# noinspection PyShadowingNames
def test_code_3d(cpu_object):
    """ DEC A - A=A-1 """
    cpu_object.register.A = 0x00
    cycles = op.code_3d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFF, F=0b01100000)

    cpu_object.register.A = 0x0F
    cycles = op.code_3d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x0E, F=0b01000000)

    cpu_object.register.A = 0x01
    cycles = op.code_3d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, F=0b11000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_3e(cpu_object):
    """ LD A,d8 """
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("99")
    cycles = op.code_3e(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object,A=0x99,PC=0x0001)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_3f(cpu_object):
    """ CCF - Invert carry flag """
    cpu_object.register.F = 0b00010000
    cycles = op.code_3f(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, F=0b00000000)

    cpu_object.register.F = 0b11100000
    cycles = op.code_3f(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, F=0b10010000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_40(cpu_object):
    """ LD B,B (...why?) """
    cpu_object.register.B = 0x99
    cycles = op.code_40(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,B=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_41(cpu_object):
    """ LD B,C """
    cpu_object.register.C = 0x99
    cycles = op.code_41(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,B=0x99,C=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_42(cpu_object):
    """ LD B,D """
    cpu_object.register.D = 0x99
    cycles = op.code_42(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,B=0x99,D=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_43(cpu_object):
    """ LD B,E """
    cpu_object.register.E = 0x99
    cycles = op.code_43(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,B=0x99,E=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_44(cpu_object):
    """ LD B,H """
    cpu_object.register.H = 0x99
    cycles = op.code_44(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,B=0x99,H=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_45(cpu_object):
    """ LD B,L """
    cpu_object.register.L = 0x99
    cycles = op.code_45(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,B=0x99,L=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_46(cpu_object):
    """ LD B,(HL) - Load reg with the value at the address in HL """
    cpu_object.memory.write_8bit(0x1010, 0x99)
    cpu_object.register.set_hl(0x1010)
    cycles = op.code_46(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0x99, H=0x10, L=0x10)
    assert_memory(cpu_object,{0x1010:0x99})


# noinspection PyShadowingNames
def test_code_47(cpu_object):
    """ LD B,A """
    cpu_object.register.A = 0x99
    cycles = op.code_47(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,A=0x99,B=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_48(cpu_object):
    """ LD C,B """
    cpu_object.register.B = 0x99
    cycles = op.code_48(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,B=0x99,C=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_49(cpu_object):
    """ LD C,C (...why?) """
    cpu_object.register.C = 0x99
    cycles = op.code_49(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,C=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_4a(cpu_object):
    """ LD C,D """
    cpu_object.register.D = 0x99
    cycles = op.code_4a(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,C=0x99,D=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_4b(cpu_object):
    """ LD C,E """
    cpu_object.register.E = 0x99
    cycles = op.code_4b(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,C=0x99,E=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_4c(cpu_object):
    """ LD C,H """
    cpu_object.register.H = 0x99
    cycles = op.code_4c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,C=0x99,H=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_4d(cpu_object):
    """ LD C,L """
    cpu_object.register.L = 0x99
    cycles = op.code_4d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,C=0x99,L=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_4e(cpu_object):
    """ LD C,(HL) - Load reg with the value at the address in HL """
    cpu_object.memory.write_8bit(0x1010, 0x99)
    cpu_object.register.set_hl(0x1010)
    cycles = op.code_4e(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0x99, H=0x10, L=0x10)
    assert_memory(cpu_object, {0x1010: 0x99})


# noinspection PyShadowingNames
def test_code_4f(cpu_object):
    """ LD C,A """
    cpu_object.register.A = 0x99
    cycles = op.code_4f(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,A=0x99,C=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_50(cpu_object):
    """ LD D,B """
    cpu_object.register.B = 0x99
    cycles = op.code_50(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,B=0x99,D=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_51(cpu_object):
    """ LD D,C """
    cpu_object.register.C = 0x99
    cycles = op.code_51(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,C=0x99,D=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_52(cpu_object):
    """ LD D,D (...why?) """
    cpu_object.register.D = 0x99
    cycles = op.code_52(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,D=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_53(cpu_object):
    """ LD D,E """
    cpu_object.register.E = 0x99
    cycles = op.code_53(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,D=0x99,E=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_54(cpu_object):
    """ LD D,H """
    cpu_object.register.H = 0x99
    cycles = op.code_54(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,D=0x99,H=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_55(cpu_object):
    """ LD D,L """
    cpu_object.register.L = 0x99
    cycles = op.code_55(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,D=0x99,L=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_56(cpu_object):
    """ LD D,(HL) - Load reg with the value at the address in HL """
    cpu_object.memory.write_8bit(0x1010, 0x99)
    cpu_object.register.set_hl(0x1010)
    cycles = op.code_56(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0x99, H=0x10, L=0x10)
    assert_memory(cpu_object, {0x1010: 0x99})


# noinspection PyShadowingNames
def test_code_57(cpu_object):
    """ LD D,A """
    cpu_object.register.A = 0x99
    cycles = op.code_57(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,A=0x99,D=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_58(cpu_object):
    """ LD E,B """
    cpu_object.register.B = 0x99
    cycles = op.code_58(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,B=0x99,E=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_59(cpu_object):
    """ LD E,C """
    cpu_object.register.C = 0x99
    cycles = op.code_59(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,C=0x99,E=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_5a(cpu_object):
    """ LD E,D """
    cpu_object.register.D = 0x99
    cycles = op.code_5a(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,D=0x99,E=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_5b(cpu_object):
    """ LD E,E (...why?) """
    cpu_object.register.E = 0x99
    cycles = op.code_5b(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,E=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_5c(cpu_object):
    """ LD E,H """
    cpu_object.register.H = 0x99
    cycles = op.code_5c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,E=0x99,H=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_5d(cpu_object):
    """ LD E,L """
    cpu_object.register.L = 0x99
    cycles = op.code_5d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,E=0x99,L=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_5e(cpu_object):
    """ LD E,(HL) - Load reg with the value at the address in HL """
    cpu_object.memory.write_8bit(0x1010, 0x99)
    cpu_object.register.set_hl(0x1010)
    cycles = op.code_5e(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0x99, H=0x10, L=0x10)
    assert_memory(cpu_object, {0x1010: 0x99})


# noinspection PyShadowingNames
def test_code_5f(cpu_object):
    """ LD E,A """
    cpu_object.register.A = 0x99
    cycles = op.code_5f(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,A=0x99,E=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_60(cpu_object):
    """ LD H,B """
    cpu_object.register.B = 0x99
    cycles = op.code_60(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, B=0x99, H=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_61(cpu_object):
    """ LD H,C """
    cpu_object.register.C = 0x99
    cycles = op.code_61(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, C=0x99, H=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_62(cpu_object):
    """ LD H,D """
    cpu_object.register.D = 0x99
    cycles = op.code_62(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, D=0x99, H=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_63(cpu_object):
    """ LD H,E """
    cpu_object.register.E = 0x99
    cycles = op.code_63(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, E=0x99, H=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_64(cpu_object):
    """ LD H,H (...why?) """
    cpu_object.register.H = 0x99
    cycles = op.code_64(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, H=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_65(cpu_object):
    """ LD H,L """
    cpu_object.register.L = 0x99
    cycles = op.code_65(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, H=0x99, L=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_66(cpu_object):
    """ LD H,(HL) - Load reg with the value at the address in HL """
    cpu_object.memory.write_8bit(0x1010, 0x99)
    cpu_object.register.set_hl(0x1010)
    cycles = op.code_66(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0x99, L=0x10)
    assert_memory(cpu_object, {0x1010: 0x99})


# noinspection PyShadowingNames
def test_code_67(cpu_object):
    """ LD H,A """
    cpu_object.register.A = 0x99
    cycles = op.code_67(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x99, H=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_68(cpu_object):
    """ LD L,B """
    cpu_object.register.B = 0x99
    cycles = op.code_68(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, B=0x99, L=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_69(cpu_object):
    """ LD L,C """
    cpu_object.register.C = 0x99
    cycles = op.code_69(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, C=0x99, L=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_6a(cpu_object):
    """ LD L,D """
    cpu_object.register.D = 0x99
    cycles = op.code_6a(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, D=0x99, L=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_6b(cpu_object):
    """ LD L,E """
    cpu_object.register.E = 0x99
    cycles = op.code_6b(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, E=0x99, L=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_6c(cpu_object):
    """ LD L,H """
    cpu_object.register.H = 0x99
    cycles = op.code_6c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, H=0x99, L=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_6d(cpu_object):
    """ LD L,L (might be a newbie question but... why?) """
    cpu_object.register.L = 0x99
    cycles = op.code_6d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, L=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_6e(cpu_object):
    """ LD L,(HL) - Load reg with the value at the address in HL """
    cpu_object.memory.write_8bit(0x1010, 0x99)
    cpu_object.register.set_hl(0x1010)
    cycles = op.code_6e(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0x10, L=0x99)
    assert_memory(cpu_object, {0x1010: 0x99})


# noinspection PyShadowingNames
def test_code_6f(cpu_object):
    """ LD L,A """
    cpu_object.register.A = 0x99
    cycles = op.code_6f(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x99, L=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_70(cpu_object):
    """ LD (HL),B - Stores reg at the address in HL """
    cpu_object.register.B = 0x99
    cpu_object.register.set_hl(0x1010)
    cycles = op.code_70(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object,B=0x99,H=0x10,L=0x10)
    assert_memory(cpu_object,{0x1010:0x99})


# noinspection PyShadowingNames
def test_code_71(cpu_object):
    """ LD (HL),C - Stores reg at the address in HL """
    cpu_object.register.C = 0x99
    cpu_object.register.set_hl(0x1010)
    cycles = op.code_71(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0x99, H=0x10, L=0x10)
    assert_memory(cpu_object, {0x1010: 0x99})


# noinspection PyShadowingNames
def test_code_72(cpu_object):
    """ LD (HL),D - Stores reg at the address in HL """
    cpu_object.register.D = 0x99
    cpu_object.register.set_hl(0x1010)
    cycles = op.code_72(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0x99, H=0x10, L=0x10)
    assert_memory(cpu_object, {0x1010: 0x99})


# noinspection PyShadowingNames
def test_code_73(cpu_object):
    """ LD (HL),E - Stores reg at the address in HL """
    cpu_object.register.E = 0x99
    cpu_object.register.set_hl(0x1010)
    cycles = op.code_73(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0x99, H=0x10, L=0x10)
    assert_memory(cpu_object, {0x1010: 0x99})


# noinspection PyShadowingNames
def test_code_74(cpu_object):
    """ LD (HL),H - Stores reg at the address in HL """
    cpu_object.register.set_hl(0x1110)
    cycles = op.code_74(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0x11, L=0x10)
    assert_memory(cpu_object, {0x1110: 0x11})


# noinspection PyShadowingNames
def test_code_75(cpu_object):
    """ LD (HL),L - Stores reg at the address in HL """
    cpu_object.register.set_hl(0x1011)
    cycles = op.code_75(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0x10, L=0x11)
    assert_memory(cpu_object, {0x1011: 0x11})


# noinspection PyShadowingNames
def test_code_76(cpu_object):
    """
    HALT - Power down CPU (by stopping the system clock) until an interrupt occurs
    See: http://gbdev.gg8.se/wiki/articles/Reducing_Power_Consumption
    """
    cycles = op.code_76(cpu_object)
    assert cycles == 4
    assert cpu_object.halted is True
    assert_registers(cpu_object)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_77(cpu_object):
    """ LD (HL),A - Stores reg at the address in HL """
    cpu_object.register.A = 0x99
    cpu_object.register.set_hl(0x1010)
    cycles = op.code_77(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x99, H=0x10, L=0x10)
    assert_memory(cpu_object, {0x1010: 0x99})


# noinspection PyShadowingNames
def test_code_78(cpu_object):
    """ LD A,B """
    cpu_object.register.B = 0x99
    cycles = op.code_78(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x99, B=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_79(cpu_object):
    """ LD A,C """
    cpu_object.register.C = 0x99
    cycles = op.code_79(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x99, C=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_7a(cpu_object):
    """ LD A,D """
    cpu_object.register.D = 0x99
    cycles = op.code_7a(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x99, D=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_7b(cpu_object):
    """ LD A,E """
    cpu_object.register.E = 0x99
    cycles = op.code_7b(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x99, E=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_7c(cpu_object):
    """ LD A,H """
    cpu_object.register.H = 0x99
    cycles = op.code_7c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x99, H=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_7d(cpu_object):
    """ LD A,L """
    cpu_object.register.L = 0x99
    cycles = op.code_7d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x99, L=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_7e(cpu_object):
    """ LD A,(HL) - Load reg with the value at the address in HL """
    cpu_object.memory.write_8bit(0x1010, 0x99)
    cpu_object.register.set_hl(0x1010)
    cycles = op.code_7e(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x99, H=0x10, L=0x10)
    assert_memory(cpu_object, {0x1010: 0x99})


# noinspection PyShadowingNames
def test_code_7f(cpu_object):
    """ LD A,A (might be a newbie question but... why?) """
    cpu_object.register.A = 0x99
    cycles = op.code_7f(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x99)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_80(cpu_object):
    """ ADD A,B - A=A+B """
    cpu_object.register.A = 0x00
    cpu_object.register.B = 0x00
    cycles = op.code_80(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, B=0x00, F=0b10000000)

    cpu_object.register.A = 0x00
    cpu_object.register.B = 0x01
    cycles = op.code_80(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, B=0x01, F=0b00000000)

    cpu_object.register.A = 0x0F
    cpu_object.register.B = 0x01
    cycles = op.code_80(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x10, B=0x01, F=0b00100000)

    cpu_object.register.A = 0xF0
    cpu_object.register.B = 0x10
    cycles = op.code_80(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, B=0x10, F=0b10010000)

    cpu_object.register.A = 0xFF
    cpu_object.register.B = 0x01
    cycles = op.code_80(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, B=0x01, F=0b10110000)

    cpu_object.register.A = 0xFF
    cpu_object.register.B = 0x02
    cycles = op.code_80(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, B=0x02, F=0b00110000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_81(cpu_object):
    """ ADD A,C - A=A+C """
    cpu_object.register.A = 0x00
    cpu_object.register.C = 0x00
    cycles = op.code_81(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, C=0x00, F=0b10000000)

    cpu_object.register.A = 0x00
    cpu_object.register.C = 0x01
    cycles = op.code_81(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, C=0x01, F=0b00000000)

    cpu_object.register.A = 0x0F
    cpu_object.register.C = 0x01
    cycles = op.code_81(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x10, C=0x01, F=0b00100000)

    cpu_object.register.A = 0xF0
    cpu_object.register.C = 0x10
    cycles = op.code_81(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, C=0x10, F=0b10010000)

    cpu_object.register.A = 0xFF
    cpu_object.register.C = 0x01
    cycles = op.code_81(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, C=0x01, F=0b10110000)

    cpu_object.register.A = 0xFF
    cpu_object.register.C = 0x02
    cycles = op.code_81(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, C=0x02, F=0b00110000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_82(cpu_object):
    """ ADD A,D - A=A+D """
    cpu_object.register.A = 0x00
    cpu_object.register.D = 0x00
    cycles = op.code_82(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, D=0x00, F=0b10000000)

    cpu_object.register.A = 0x00
    cpu_object.register.D = 0x01
    cycles = op.code_82(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, D=0x01, F=0b00000000)

    cpu_object.register.A = 0x0F
    cpu_object.register.D = 0x01
    cycles = op.code_82(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x10, D=0x01, F=0b00100000)

    cpu_object.register.A = 0xF0
    cpu_object.register.D = 0x10
    cycles = op.code_82(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, D=0x10, F=0b10010000)

    cpu_object.register.A = 0xFF
    cpu_object.register.D = 0x01
    cycles = op.code_82(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, D=0x01, F=0b10110000)

    cpu_object.register.A = 0xFF
    cpu_object.register.D = 0x02
    cycles = op.code_82(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, D=0x02, F=0b00110000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_83(cpu_object):
    """ ADD A,E - A=A+E """
    cpu_object.register.A = 0x00
    cpu_object.register.E = 0x00
    cycles = op.code_83(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, E=0x00, F=0b10000000)

    cpu_object.register.A = 0x00
    cpu_object.register.E = 0x01
    cycles = op.code_83(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, E=0x01, F=0b00000000)

    cpu_object.register.A = 0x0F
    cpu_object.register.E = 0x01
    cycles = op.code_83(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x10, E=0x01, F=0b00100000)

    cpu_object.register.A = 0xF0
    cpu_object.register.E = 0x10
    cycles = op.code_83(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, E=0x10, F=0b10010000)

    cpu_object.register.A = 0xFF
    cpu_object.register.E = 0x01
    cycles = op.code_83(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, E=0x01, F=0b10110000)

    cpu_object.register.A = 0xFF
    cpu_object.register.E = 0x02
    cycles = op.code_83(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, E=0x02, F=0b00110000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_84(cpu_object):
    """ ADD A,H - A=A+H """
    cpu_object.register.A = 0x00
    cpu_object.register.H = 0x00
    cycles = op.code_84(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, H=0x00, F=0b10000000)

    cpu_object.register.A = 0x00
    cpu_object.register.H = 0x01
    cycles = op.code_84(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, H=0x01, F=0b00000000)

    cpu_object.register.A = 0x0F
    cpu_object.register.H = 0x01
    cycles = op.code_84(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x10, H=0x01, F=0b00100000)

    cpu_object.register.A = 0xF0
    cpu_object.register.H = 0x10
    cycles = op.code_84(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, H=0x10, F=0b10010000)

    cpu_object.register.A = 0xFF
    cpu_object.register.H = 0x01
    cycles = op.code_84(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, H=0x01, F=0b10110000)

    cpu_object.register.A = 0xFF
    cpu_object.register.H = 0x02
    cycles = op.code_84(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, H=0x02, F=0b00110000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_85(cpu_object):
    """ ADD A,L - A=A+L """
    cpu_object.register.A = 0x00
    cpu_object.register.L = 0x00
    cycles = op.code_85(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, L=0x00, F=0b10000000)

    cpu_object.register.A = 0x00
    cpu_object.register.L = 0x01
    cycles = op.code_85(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, L=0x01, F=0b00000000)

    cpu_object.register.A = 0x0F
    cpu_object.register.L = 0x01
    cycles = op.code_85(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x10, L=0x01, F=0b00100000)

    cpu_object.register.A = 0xF0
    cpu_object.register.L = 0x10
    cycles = op.code_85(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, L=0x10, F=0b10010000)

    cpu_object.register.A = 0xFF
    cpu_object.register.L = 0x01
    cycles = op.code_85(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, L=0x01, F=0b10110000)

    cpu_object.register.A = 0xFF
    cpu_object.register.L = 0x02
    cycles = op.code_85(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, L=0x02, F=0b00110000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_86(cpu_object):
    """ ADD A,(HL) - A=A+(value at address HL) """
    cpu_object.register.set_hl(0x1010)
    cpu_object.register.A = 0x00
    cpu_object.memory.write_8bit(0x1010, 0x00)
    cycles = op.code_86(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x00, H=0x10, L=0x10, F=0b10000000)
    assert_memory(cpu_object)

    cpu_object.register.A = 0x00
    cpu_object.memory.write_8bit(0x1010, 0x01)
    cycles = op.code_86(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x01, H=0x10, L=0x10, F=0b00000000)
    assert_memory(cpu_object,{0x1010:0x01})

    cpu_object.register.A = 0x0F
    cpu_object.memory.write_8bit(0x1010, 0x01)
    cycles = op.code_86(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x10, H=0x10, L=0x10, F=0b00100000)
    assert_memory(cpu_object, {0x1010: 0x01})

    cpu_object.register.A = 0xF0
    cpu_object.memory.write_8bit(0x1010, 0x10)
    cycles = op.code_86(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x00, H=0x10, L=0x10, F=0b10010000)
    assert_memory(cpu_object, {0x1010: 0x10})

    cpu_object.register.A = 0xFF
    cpu_object.memory.write_8bit(0x1010, 0x01)
    cycles = op.code_86(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x00, H=0x10, L=0x10, F=0b10110000)
    assert_memory(cpu_object, {0x1010: 0x01})

    cpu_object.register.A = 0xFF
    cpu_object.memory.write_8bit(0x1010, 0x02)
    cycles = op.code_86(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x01, H=0x10, L=0x10, F=0b00110000)
    assert_memory(cpu_object, {0x1010: 0x02})


# noinspection PyShadowingNames
def test_code_87(cpu_object):
    """ ADD A,A - A=A+A """
    cpu_object.register.A = 0x00
    cycles = op.code_87(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, F=0b10000000)

    cpu_object.register.A = 0x01
    cycles = op.code_87(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x02, F=0b00000000)

    cpu_object.register.A = 0x08
    cycles = op.code_87(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x10, F=0b00100000)

    cpu_object.register.A = 0x80
    cycles = op.code_87(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, F=0b10010000)

    cpu_object.register.A = 0x88
    cycles = op.code_87(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x10, F=0b00110000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_88(cpu_object):
    """ ADC A,B - A=A+B+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    cpu_object.register.A = 0x00
    cpu_object.register.B = 0x00
    cpu_object.register.F = 0b00000000
    cycles = op.code_88(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, B=0x00, F=0b10000000)

    cpu_object.register.A = 0x00
    cpu_object.register.B = 0x00
    cpu_object.register.F = 0b00010000
    cycles = op.code_88(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, B=0x00, F=0b00000000)

    cpu_object.register.A = 0x00
    cpu_object.register.B = 0x01
    cpu_object.register.F = 0b00010000
    cycles = op.code_88(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x02, B=0x01, F=0b00000000)

    cpu_object.register.A = 0x0E
    cpu_object.register.B = 0x01
    cpu_object.register.F = 0b00010000
    cycles = op.code_88(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x10, B=0x01, F=0b00100000)

    cpu_object.register.A = 0xF0
    cpu_object.register.B = 0x0F
    cpu_object.register.F = 0b00010000
    cycles = op.code_88(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, B=0x0F, F=0b10110000)

    cpu_object.register.A = 0xFE
    cpu_object.register.B = 0x01
    cpu_object.register.F = 0b00010000
    cycles = op.code_88(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, B=0x01, F=0b10110000)

    cpu_object.register.A = 0xFE
    cpu_object.register.B = 0x02
    cpu_object.register.F = 0b00010000
    cycles = op.code_88(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, B=0x02, F=0b00110000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_89(cpu_object):
    """ ADC A,C - A=A+C+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    cpu_object.register.A = 0x00
    cpu_object.register.C = 0x00
    cpu_object.register.F = 0b00000000
    cycles = op.code_89(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, C=0x00, F=0b10000000)

    cpu_object.register.A = 0x00
    cpu_object.register.C = 0x00
    cpu_object.register.F = 0b00010000
    cycles = op.code_89(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, C=0x00, F=0b00000000)

    cpu_object.register.A = 0x00
    cpu_object.register.C = 0x01
    cpu_object.register.F = 0b00010000
    cycles = op.code_89(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x02, C=0x01, F=0b00000000)

    cpu_object.register.A = 0x0E
    cpu_object.register.C = 0x01
    cpu_object.register.F = 0b00010000
    cycles = op.code_89(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x10, C=0x01, F=0b00100000)

    cpu_object.register.A = 0xF0
    cpu_object.register.C = 0x0F
    cpu_object.register.F = 0b00010000
    cycles = op.code_89(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, C=0x0F, F=0b10110000)

    cpu_object.register.A = 0xFE
    cpu_object.register.C = 0x01
    cpu_object.register.F = 0b00010000
    cycles = op.code_89(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, C=0x01, F=0b10110000)

    cpu_object.register.A = 0xFE
    cpu_object.register.C = 0x02
    cpu_object.register.F = 0b00010000
    cycles = op.code_89(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, C=0x02, F=0b00110000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_8a(cpu_object):
    """ ADC A,D - A=A+D+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    cpu_object.register.A = 0x00
    cpu_object.register.D = 0x00
    cpu_object.register.F = 0b00000000
    cycles = op.code_8a(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, D=0x00, F=0b10000000)

    cpu_object.register.A = 0x00
    cpu_object.register.D = 0x00
    cpu_object.register.F = 0b00010000
    cycles = op.code_8a(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, D=0x00, F=0b00000000)

    cpu_object.register.A = 0x00
    cpu_object.register.D = 0x01
    cpu_object.register.F = 0b00010000
    cycles = op.code_8a(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x02, D=0x01, F=0b00000000)

    cpu_object.register.A = 0x0E
    cpu_object.register.D = 0x01
    cpu_object.register.F = 0b00010000
    cycles = op.code_8a(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x10, D=0x01, F=0b00100000)

    cpu_object.register.A = 0xF0
    cpu_object.register.D = 0x0F
    cpu_object.register.F = 0b00010000
    cycles = op.code_8a(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, D=0x0F, F=0b10110000)

    cpu_object.register.A = 0xFE
    cpu_object.register.D = 0x01
    cpu_object.register.F = 0b00010000
    cycles = op.code_8a(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, D=0x01, F=0b10110000)

    cpu_object.register.A = 0xFE
    cpu_object.register.D = 0x02
    cpu_object.register.F = 0b00010000
    cycles = op.code_8a(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, D=0x02, F=0b00110000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_8b(cpu_object):
    """ ADC A,E - A=A+E+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    cpu_object.register.A = 0x00
    cpu_object.register.E = 0x00
    cpu_object.register.F = 0b00000000
    cycles = op.code_8b(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, E=0x00, F=0b10000000)

    cpu_object.register.A = 0x00
    cpu_object.register.E = 0x00
    cpu_object.register.F = 0b00010000
    cycles = op.code_8b(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, E=0x00, F=0b00000000)

    cpu_object.register.A = 0x00
    cpu_object.register.E = 0x01
    cpu_object.register.F = 0b00010000
    cycles = op.code_8b(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x02, E=0x01, F=0b00000000)

    cpu_object.register.A = 0x0E
    cpu_object.register.E = 0x01
    cpu_object.register.F = 0b00010000
    cycles = op.code_8b(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x10, E=0x01, F=0b00100000)

    cpu_object.register.A = 0xF0
    cpu_object.register.E = 0x0F
    cpu_object.register.F = 0b00010000
    cycles = op.code_8b(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, E=0x0F, F=0b10110000)

    cpu_object.register.A = 0xFE
    cpu_object.register.E = 0x01
    cpu_object.register.F = 0b00010000
    cycles = op.code_8b(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, E=0x01, F=0b10110000)

    cpu_object.register.A = 0xFE
    cpu_object.register.E = 0x02
    cpu_object.register.F = 0b00010000
    cycles = op.code_8b(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, E=0x02, F=0b00110000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_8c(cpu_object):
    """ ADC A,H - A=A+H+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    cpu_object.register.A = 0x00
    cpu_object.register.H = 0x00
    cpu_object.register.F = 0b00000000
    cycles = op.code_8c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, H=0x00, F=0b10000000)

    cpu_object.register.A = 0x00
    cpu_object.register.H = 0x00
    cpu_object.register.F = 0b00010000
    cycles = op.code_8c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, H=0x00, F=0b00000000)

    cpu_object.register.A = 0x00
    cpu_object.register.H = 0x01
    cpu_object.register.F = 0b00010000
    cycles = op.code_8c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x02, H=0x01, F=0b00000000)

    cpu_object.register.A = 0x0E
    cpu_object.register.H = 0x01
    cpu_object.register.F = 0b00010000
    cycles = op.code_8c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x10, H=0x01, F=0b00100000)

    cpu_object.register.A = 0xF0
    cpu_object.register.H = 0x0F
    cpu_object.register.F = 0b00010000
    cycles = op.code_8c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, H=0x0F, F=0b10110000)

    cpu_object.register.A = 0xFE
    cpu_object.register.H = 0x01
    cpu_object.register.F = 0b00010000
    cycles = op.code_8c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, H=0x01, F=0b10110000)

    cpu_object.register.A = 0xFE
    cpu_object.register.H = 0x02
    cpu_object.register.F = 0b00010000
    cycles = op.code_8c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, H=0x02, F=0b00110000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_8d(cpu_object):
    """ ADC A,L - A=A+L+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    cpu_object.register.A = 0x00
    cpu_object.register.L = 0x00
    cpu_object.register.F = 0b00000000
    cycles = op.code_8d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, L=0x00, F=0b10000000)

    cpu_object.register.A = 0x00
    cpu_object.register.L = 0x00
    cpu_object.register.F = 0b00010000
    cycles = op.code_8d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, L=0x00, F=0b00000000)

    cpu_object.register.A = 0x00
    cpu_object.register.L = 0x01
    cpu_object.register.F = 0b00010000
    cycles = op.code_8d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x02, L=0x01, F=0b00000000)

    cpu_object.register.A = 0x0E
    cpu_object.register.L = 0x01
    cpu_object.register.F = 0b00010000
    cycles = op.code_8d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x10, L=0x01, F=0b00100000)

    cpu_object.register.A = 0xF0
    cpu_object.register.L = 0x0F
    cpu_object.register.F = 0b00010000
    cycles = op.code_8d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, L=0x0F, F=0b10110000)

    cpu_object.register.A = 0xFE
    cpu_object.register.L = 0x01
    cpu_object.register.F = 0b00010000
    cycles = op.code_8d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, L=0x01, F=0b10110000)

    cpu_object.register.A = 0xFE
    cpu_object.register.L = 0x02
    cpu_object.register.F = 0b00010000
    cycles = op.code_8d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, L=0x02, F=0b00110000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_8e(cpu_object):
    """ ADC A,(HL) - A=A+(value at address HL)+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    cpu_object.register.set_hl(0x1010)

    cpu_object.register.A = 0x00
    cpu_object.memory.write_8bit(0x1010, 0x00)
    cpu_object.register.F = 0b00000000
    cycles = op.code_8e(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x00, H=0x10, L=0x10, F=0b10000000)
    assert_memory(cpu_object)

    cpu_object.register.A = 0x00
    cpu_object.memory.write_8bit(0x1010, 0x00)
    cpu_object.register.F = 0b00010000
    cycles = op.code_8e(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x01, H=0x10, L=0x10, F=0b00000000)
    assert_memory(cpu_object)

    cpu_object.register.A = 0x00
    cpu_object.memory.write_8bit(0x1010, 0x01)
    cpu_object.register.F = 0b00010000
    cycles = op.code_8e(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x02, H=0x10, L=0x10, F=0b00000000)
    assert_memory(cpu_object,{0x1010:0x01})

    cpu_object.register.A = 0x0E
    cpu_object.memory.write_8bit(0x1010, 0x01)
    cpu_object.register.F = 0b00010000
    cycles = op.code_8e(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x10, H=0x10, L=0x10, F=0b00100000)
    assert_memory(cpu_object, {0x1010:0x01})

    cpu_object.register.A = 0xF0
    cpu_object.memory.write_8bit(0x1010, 0x0F)
    cpu_object.register.F = 0b00010000
    cycles = op.code_8e(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x00, H=0x10, L=0x10, F=0b10110000)
    assert_memory(cpu_object, {0x1010:0x0F})

    cpu_object.register.A = 0xFE
    cpu_object.memory.write_8bit(0x1010, 0x01)
    cpu_object.register.F = 0b00010000
    cycles = op.code_8e(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x00, H=0x10, L=0x10, F=0b10110000)
    assert_memory(cpu_object, {0x1010:0x01})

    cpu_object.register.A = 0xFE
    cpu_object.memory.write_8bit(0x1010, 0x02)
    cpu_object.register.F = 0b00010000
    cycles = op.code_8e(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x01, H=0x10, L=0x10, F=0b00110000)
    assert_memory(cpu_object, {0x1010:0x02})


# noinspection PyShadowingNames
def test_code_8f(cpu_object):
    """ ADC A,A - A=A+A+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    cpu_object.register.A = 0x00
    cpu_object.register.F = 0b00000000
    cycles = op.code_8f(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, F=0b10000000)

    cpu_object.register.A = 0x00
    cpu_object.register.F = 0b00010000
    cycles = op.code_8f(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, F=0b00000000)

    cpu_object.register.A = 0x01
    cpu_object.register.F = 0b00010000
    cycles = op.code_8f(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x03, F=0b00000000)

    cpu_object.register.A = 0x08
    cpu_object.register.F = 0b00010000
    cycles = op.code_8f(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x11, F=0b00100000)

    cpu_object.register.A = 0x80
    cpu_object.register.F = 0b00000000
    cycles = op.code_8f(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, F=0b10010000)

    cpu_object.register.A = 0x80
    cpu_object.register.F = 0b00010000
    cycles = op.code_8f(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, F=0b00010000)

    cpu_object.register.A = 0xFF
    cpu_object.register.F = 0b00010000
    cycles = op.code_8f(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFF, F=0b00110000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_90(cpu_object):
    """ SUB A,B - A=A-B """
    cpu_object.register.A = 0x00
    cpu_object.register.B = 0x00
    cycles = op.code_90(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, B=0x00, F=0b11000000)

    cpu_object.register.A = 0x00
    cpu_object.register.B = 0x01
    cycles = op.code_90(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFF, B=0x01, F=0b01110000)

    cpu_object.register.A = 0x0F
    cpu_object.register.B = 0x01
    cycles = op.code_90(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x0E, B=0x01, F=0b01000000)

    cpu_object.register.A = 0xF0
    cpu_object.register.B = 0x10
    cycles = op.code_90(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xE0, B=0x10, F=0b01000000)

    cpu_object.register.A = 0xFF
    cpu_object.register.B = 0x01
    cycles = op.code_90(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFE, B=0x01, F=0b01000000)

    cpu_object.register.A = 0xFF
    cpu_object.register.B = 0xFE
    cycles = op.code_90(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, B=0xFE, F=0b01000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_91(cpu_object):
    """ SUB A,C - A=A-C """
    cpu_object.register.A = 0x00
    cpu_object.register.C = 0x00
    cycles = op.code_91(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, C=0x00, F=0b11000000)

    cpu_object.register.A = 0x00
    cpu_object.register.C = 0x01
    cycles = op.code_91(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFF, C=0x01, F=0b01110000)

    cpu_object.register.A = 0x0F
    cpu_object.register.C = 0x01
    cycles = op.code_91(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x0E, C=0x01, F=0b01000000)

    cpu_object.register.A = 0xF0
    cpu_object.register.C = 0x10
    cycles = op.code_91(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xE0, C=0x10, F=0b01000000)

    cpu_object.register.A = 0xFF
    cpu_object.register.C = 0x01
    cycles = op.code_91(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFE, C=0x01, F=0b01000000)

    cpu_object.register.A = 0xFF
    cpu_object.register.C = 0xFE
    cycles = op.code_91(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, C=0xFE, F=0b01000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_92(cpu_object):
    """ SUB A,D - A=A-D """
    cpu_object.register.A = 0x00
    cpu_object.register.D = 0x00
    cycles = op.code_92(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, D=0x00, F=0b11000000)

    cpu_object.register.A = 0x00
    cpu_object.register.D = 0x01
    cycles = op.code_92(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFF, D=0x01, F=0b01110000)

    cpu_object.register.A = 0x0F
    cpu_object.register.D = 0x01
    cycles = op.code_92(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x0E, D=0x01, F=0b01000000)

    cpu_object.register.A = 0xF0
    cpu_object.register.D = 0x10
    cycles = op.code_92(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xE0, D=0x10, F=0b01000000)

    cpu_object.register.A = 0xFF
    cpu_object.register.D = 0x01
    cycles = op.code_92(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFE, D=0x01, F=0b01000000)

    cpu_object.register.A = 0xFF
    cpu_object.register.D = 0xFE
    cycles = op.code_92(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, D=0xFE, F=0b01000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_93(cpu_object):
    """ SUB A,E - A=A-E """
    cpu_object.register.A = 0x00
    cpu_object.register.E = 0x00
    cycles = op.code_93(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, E=0x00, F=0b11000000)

    cpu_object.register.A = 0x00
    cpu_object.register.E = 0x01
    cycles = op.code_93(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFF, E=0x01, F=0b01110000)

    cpu_object.register.A = 0x0F
    cpu_object.register.E = 0x01
    cycles = op.code_93(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x0E, E=0x01, F=0b01000000)

    cpu_object.register.A = 0xF0
    cpu_object.register.E = 0x10
    cycles = op.code_93(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xE0, E=0x10, F=0b01000000)

    cpu_object.register.A = 0xFF
    cpu_object.register.E = 0x01
    cycles = op.code_93(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFE, E=0x01, F=0b01000000)

    cpu_object.register.A = 0xFF
    cpu_object.register.E = 0xFE
    cycles = op.code_93(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, E=0xFE, F=0b01000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_94(cpu_object):
    """ SUB A,H - A=A-H """
    cpu_object.register.A = 0x00
    cpu_object.register.H = 0x00
    cycles = op.code_94(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, H=0x00, F=0b11000000)

    cpu_object.register.A = 0x00
    cpu_object.register.H = 0x01
    cycles = op.code_94(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFF, H=0x01, F=0b01110000)

    cpu_object.register.A = 0x0F
    cpu_object.register.H = 0x01
    cycles = op.code_94(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x0E, H=0x01, F=0b01000000)

    cpu_object.register.A = 0xF0
    cpu_object.register.H = 0x10
    cycles = op.code_94(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xE0, H=0x10, F=0b01000000)

    cpu_object.register.A = 0xFF
    cpu_object.register.H = 0x01
    cycles = op.code_94(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFE, H=0x01, F=0b01000000)

    cpu_object.register.A = 0xFF
    cpu_object.register.H = 0xFE
    cycles = op.code_94(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, H=0xFE, F=0b01000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_95(cpu_object):
    """ SUB A,L - A=A-L """
    cpu_object.register.A = 0x00
    cpu_object.register.L = 0x00
    cycles = op.code_95(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, L=0x00, F=0b11000000)

    cpu_object.register.A = 0x00
    cpu_object.register.L = 0x01
    cycles = op.code_95(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFF, L=0x01, F=0b01110000)

    cpu_object.register.A = 0x0F
    cpu_object.register.L = 0x01
    cycles = op.code_95(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x0E, L=0x01, F=0b01000000)

    cpu_object.register.A = 0xF0
    cpu_object.register.L = 0x10
    cycles = op.code_95(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xE0, L=0x10, F=0b01000000)

    cpu_object.register.A = 0xFF
    cpu_object.register.L = 0x01
    cycles = op.code_95(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFE, L=0x01, F=0b01000000)

    cpu_object.register.A = 0xFF
    cpu_object.register.L = 0xFE
    cycles = op.code_95(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, L=0xFE, F=0b01000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_96(cpu_object):
    """ SUB A,(HL) - A=A-(value at address HL) """
    cpu_object.register.set_hl(0x1010)

    cpu_object.register.A = 0x00
    cpu_object.memory.write_8bit(0x1010, 0x00)
    cycles = op.code_96(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x00, H=0x10, L=0x10, F=0b11000000)
    assert_memory(cpu_object)

    cpu_object.register.A = 0x00
    cpu_object.memory.write_8bit(0x1010, 0x01)
    cycles = op.code_96(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0xFF, H=0x10, L=0x10, F=0b01110000)
    assert_memory(cpu_object,{0x1010:0x01})

    cpu_object.register.A = 0x0F
    cpu_object.memory.write_8bit(0x1010, 0x01)
    cycles = op.code_96(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x0E, H=0x10, L=0x10, F=0b01000000)
    assert_memory(cpu_object, {0x1010: 0x01})

    cpu_object.register.A = 0xF0
    cpu_object.memory.write_8bit(0x1010, 0x10)
    cycles = op.code_96(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0xE0, H=0x10, L=0x10, F=0b01000000)
    assert_memory(cpu_object, {0x1010: 0x10})

    cpu_object.register.A = 0xFF
    cpu_object.memory.write_8bit(0x1010, 0x01)
    cycles = op.code_96(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0xFE, H=0x10, L=0x10, F=0b01000000)
    assert_memory(cpu_object, {0x1010: 0x01})

    cpu_object.register.A = 0xFF
    cpu_object.memory.write_8bit(0x1010, 0xFE)
    cycles = op.code_96(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x01, H=0x10, L=0x10, F=0b01000000)
    assert_memory(cpu_object, {0x1010: 0xFE})


# noinspection PyShadowingNames
def test_code_97(cpu_object):
    """ SUB A,A - A=A-A """
    cpu_object.register.A = 0x00
    cycles = op.code_97(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, F=0b11000000)

    cpu_object.register.A = 0x01
    cycles = op.code_97(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, F=0b11000000)

    cpu_object.register.A = 0xFF
    cycles = op.code_97(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, F=0b11000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_98(cpu_object):
    """ SBC A,B - A=A-B-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    cpu_object.register.A = 0x00
    cpu_object.register.B = 0x00
    cpu_object.register.F = 0b00000000
    cycles = op.code_98(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, B=0x00, F=0b11000000)

    cpu_object.register.A = 0x02
    cpu_object.register.B = 0x00
    cpu_object.register.F = 0b00010000
    cycles = op.code_98(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, B=0x00, F=0b01000000)

    cpu_object.register.A = 0x00
    cpu_object.register.B = 0x01
    cpu_object.register.F = 0b00010000
    cycles = op.code_98(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFE, B=0x01, F=0b01110000)

    cpu_object.register.A = 0x13
    cpu_object.register.B = 0x04
    cpu_object.register.F = 0b00010000
    cycles = op.code_98(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x0E, B=0x04, F=0b01100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_99(cpu_object):
    """ SBC A,C - A=A-C-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    cpu_object.register.A = 0x00
    cpu_object.register.C = 0x00
    cpu_object.register.F = 0b00000000
    cycles = op.code_99(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, C=0x00, F=0b11000000)

    cpu_object.register.A = 0x02
    cpu_object.register.C = 0x00
    cpu_object.register.F = 0b00010000
    cycles = op.code_99(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, C=0x00, F=0b01000000)

    cpu_object.register.A = 0x00
    cpu_object.register.C = 0x01
    cpu_object.register.F = 0b00010000
    cycles = op.code_99(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFE, C=0x01, F=0b01110000)

    cpu_object.register.A = 0x13
    cpu_object.register.C = 0x04
    cpu_object.register.F = 0b00010000
    cycles = op.code_99(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x0E, C=0x04, F=0b01100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_9a(cpu_object):
    """ SBC A,D - A=A-D-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    cpu_object.register.A = 0x00
    cpu_object.register.D = 0x00
    cpu_object.register.F = 0b00000000
    cycles = op.code_9a(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, D=0x00, F=0b11000000)

    cpu_object.register.A = 0x02
    cpu_object.register.D = 0x00
    cpu_object.register.F = 0b00010000
    cycles = op.code_9a(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, D=0x00, F=0b01000000)

    cpu_object.register.A = 0x00
    cpu_object.register.D = 0x01
    cpu_object.register.F = 0b00010000
    cycles = op.code_9a(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFE, D=0x01, F=0b01110000)

    cpu_object.register.A = 0x13
    cpu_object.register.D = 0x04
    cpu_object.register.F = 0b00010000
    cycles = op.code_9a(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x0E, D=0x04, F=0b01100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_9b(cpu_object):
    """ SBC A,E - A=A-E-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    cpu_object.register.A = 0x00
    cpu_object.register.E = 0x00
    cpu_object.register.F = 0b00000000
    cycles = op.code_9b(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, E=0x00, F=0b11000000)

    cpu_object.register.A = 0x02
    cpu_object.register.E = 0x00
    cpu_object.register.F = 0b00010000
    cycles = op.code_9b(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, E=0x00, F=0b01000000)

    cpu_object.register.A = 0x00
    cpu_object.register.E = 0x01
    cpu_object.register.F = 0b00010000
    cycles = op.code_9b(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFE, E=0x01, F=0b01110000)

    cpu_object.register.A = 0x13
    cpu_object.register.E = 0x04
    cpu_object.register.F = 0b00010000
    cycles = op.code_9b(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x0E, E=0x04, F=0b01100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_9c(cpu_object):
    """ SBC A,H - A=A-H-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    cpu_object.register.A = 0x00
    cpu_object.register.H = 0x00
    cpu_object.register.F = 0b00000000
    cycles = op.code_9c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, H=0x00, F=0b11000000)

    cpu_object.register.A = 0x02
    cpu_object.register.H = 0x00
    cpu_object.register.F = 0b00010000
    cycles = op.code_9c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, H=0x00, F=0b01000000)

    cpu_object.register.A = 0x00
    cpu_object.register.H = 0x01
    cpu_object.register.F = 0b00010000
    cycles = op.code_9c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFE, H=0x01, F=0b01110000)

    cpu_object.register.A = 0x13
    cpu_object.register.H = 0x04
    cpu_object.register.F = 0b00010000
    cycles = op.code_9c(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x0E, H=0x04, F=0b01100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_9d(cpu_object):
    """ SBC A,L - A=A-L-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    cpu_object.register.A = 0x00
    cpu_object.register.L = 0x00
    cpu_object.register.F = 0b00000000
    cycles = op.code_9d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, L=0x00, F=0b11000000)

    cpu_object.register.A = 0x02
    cpu_object.register.L = 0x00
    cpu_object.register.F = 0b00010000
    cycles = op.code_9d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, L=0x00, F=0b01000000)

    cpu_object.register.A = 0x00
    cpu_object.register.L = 0x01
    cpu_object.register.F = 0b00010000
    cycles = op.code_9d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFE, L=0x01, F=0b01110000)

    cpu_object.register.A = 0x13
    cpu_object.register.L = 0x04
    cpu_object.register.F = 0b00010000
    cycles = op.code_9d(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x0E, L=0x04, F=0b01100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_9e(cpu_object):
    """ SBC A,(HL) - A=A-(value at address HL)-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    cpu_object.register.set_hl(0x1010)

    cpu_object.register.A = 0x00
    cpu_object.memory.write_8bit(0x1010, 0x00)
    cpu_object.register.F = 0b00000000
    cycles = op.code_9e(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x00, H=0x10, L=0x10, F=0b11000000)
    assert_memory(cpu_object)

    cpu_object.register.A = 0x02
    cpu_object.memory.write_8bit(0x1010, 0x00)
    cpu_object.register.F = 0b00010000
    cycles = op.code_9e(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x01, H=0x10, L=0x10, F=0b01000000)
    assert_memory(cpu_object)

    cpu_object.register.A = 0x00
    cpu_object.memory.write_8bit(0x1010, 0x01)
    cpu_object.register.F = 0b00010000
    cycles = op.code_9e(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0xFE, H=0x10, L=0x10, F=0b01110000)
    assert_memory(cpu_object,{0x1010:0x01})

    cpu_object.register.A = 0x13
    cpu_object.memory.write_8bit(0x1010, 0x04)
    cpu_object.register.F = 0b00010000
    cycles = op.code_9e(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x0E, H=0x10, L=0x10, F=0b01100000)
    assert_memory(cpu_object, {0x1010: 0x04})


# noinspection PyShadowingNames
def test_code_9f(cpu_object):
    """ SBC A,A - A=A-A-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    cpu_object.register.A = 0x00
    cpu_object.register.F = 0b00000000
    cycles = op.code_9f(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, F=0b11000000)

    cpu_object.register.A = 0x00
    cpu_object.register.F = 0b00010000
    cycles = op.code_9f(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFF, F=0b01110000)

    cpu_object.register.A = 0xFF
    cpu_object.register.F = 0b00010000
    cycles = op.code_9f(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFF, F=0b01110000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_a0(cpu_object):
    """ AND B - A=Logical AND A with B """
    cpu_object.register.A = 0b10100011
    cpu_object.register.B = 0b01000100
    cycles = op.code_a0(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000000, B=0b01000100, F=0b10100000)

    cpu_object.register.A = 0b10100011
    cpu_object.register.B = 0b01100110
    cycles = op.code_a0(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00100010, B=0b01100110, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_a1(cpu_object):
    """ AND C - A=Logical AND A with C """
    cpu_object.register.A = 0b10100011
    cpu_object.register.C = 0b01000100
    cycles = op.code_a1(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000000, C=0b01000100, F=0b10100000)

    cpu_object.register.A = 0b10100011
    cpu_object.register.C = 0b01100110
    cycles = op.code_a1(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00100010, C=0b01100110, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_a2(cpu_object):
    """ AND D - A=Logical AND A with D """
    cpu_object.register.A = 0b10100011
    cpu_object.register.D = 0b01000100
    cycles = op.code_a2(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000000, D=0b01000100, F=0b10100000)

    cpu_object.register.A = 0b10100011
    cpu_object.register.D = 0b01100110
    cycles = op.code_a2(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00100010, D=0b01100110, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_a3(cpu_object):
    """ AND E - A=Logical AND A with E """
    cpu_object.register.A = 0b10100011
    cpu_object.register.E = 0b01000100
    cycles = op.code_a3(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000000, E=0b01000100, F=0b10100000)

    cpu_object.register.A = 0b10100011
    cpu_object.register.E = 0b01100110
    cycles = op.code_a3(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00100010, E=0b01100110, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_a4(cpu_object):
    """ AND H - A=Logical AND A with H """
    cpu_object.register.A = 0b10100011
    cpu_object.register.H = 0b01000100
    cycles = op.code_a4(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000000, H=0b01000100, F=0b10100000)

    cpu_object.register.A = 0b10100011
    cpu_object.register.H = 0b01100110
    cycles = op.code_a4(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00100010, H=0b01100110, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_a5(cpu_object):
    """ AND L - A=Logical AND A with L """
    cpu_object.register.A = 0b10100011
    cpu_object.register.L = 0b01000100
    cycles = op.code_a5(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000000, L=0b01000100, F=0b10100000)

    cpu_object.register.A = 0b10100011
    cpu_object.register.L = 0b01100110
    cycles = op.code_a5(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00100010, L=0b01100110, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_a6(cpu_object):
    """ AND (HL) - A=Logical AND A with (value at address HL) """
    cpu_object.register.set_hl(0x1010)

    cpu_object.register.A = 0b10100011
    cpu_object.memory.write_8bit(0x1010,0b01000100)
    cycles = op.code_a6(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b00000000, H=0x10, L=0x10, F=0b10100000)

    cpu_object.register.A = 0b10100011
    cpu_object.memory.write_8bit(0x1010, 0b01100110)
    cycles = op.code_a6(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b00100010, H=0x10, L=0x10, F=0b00100000)


# noinspection PyShadowingNames
def test_code_a7(cpu_object):
    """ AND A - A=Logical AND A with A (why?) """
    cpu_object.register.A = 0b00000000
    cycles = op.code_a7(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000000, F=0b10100000)

    cpu_object.register.A = 0b00100011
    cycles = op.code_a7(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00100011, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_a8(cpu_object):
    """ XOR B - A=Logical XOR A with B """
    cpu_object.register.A = 0b10100011
    cpu_object.register.B = 0b10100011
    cycles = op.code_a8(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000000, B=0b10100011, F=0b10000000)

    cpu_object.register.A = 0b10100011
    cpu_object.register.B = 0b01100110
    cycles = op.code_a8(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b11000101, B=0b01100110, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_a9(cpu_object):
    """ XOR C - A=Logical XOR A with C """
    cpu_object.register.A = 0b10100011
    cpu_object.register.C = 0b10100011
    cycles = op.code_a9(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000000, C=0b10100011, F=0b10000000)

    cpu_object.register.A = 0b10100011
    cpu_object.register.C = 0b01100110
    cycles = op.code_a9(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b11000101, C=0b01100110, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_aa(cpu_object):
    """ XOR D - A=Logical XOR A with D """
    cpu_object.register.A = 0b10100011
    cpu_object.register.D = 0b10100011
    cycles = op.code_aa(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000000, D=0b10100011, F=0b10000000)

    cpu_object.register.A = 0b10100011
    cpu_object.register.D = 0b01100110
    cycles = op.code_aa(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b11000101, D=0b01100110, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_ab(cpu_object):
    """ XOR E - A=Logical XOR A with E """
    cpu_object.register.A = 0b10100011
    cpu_object.register.E = 0b10100011
    cycles = op.code_ab(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000000, E=0b10100011, F=0b10000000)

    cpu_object.register.A = 0b10100011
    cpu_object.register.E = 0b01100110
    cycles = op.code_ab(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b11000101, E=0b01100110, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_ac(cpu_object):
    """ XOR H - A=Logical XOR A with H """
    cpu_object.register.A = 0b10100011
    cpu_object.register.H = 0b10100011
    cycles = op.code_ac(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000000, H=0b10100011, F=0b10000000)

    cpu_object.register.A = 0b10100011
    cpu_object.register.H = 0b01100110
    cycles = op.code_ac(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b11000101, H=0b01100110, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_ad(cpu_object):
    """ XOR L - A=Logical XOR A with L """
    cpu_object.register.A = 0b10100011
    cpu_object.register.L = 0b10100011
    cycles = op.code_ad(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000000, L=0b10100011, F=0b10000000)

    cpu_object.register.A = 0b10100011
    cpu_object.register.L = 0b01100110
    cycles = op.code_ad(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b11000101, L=0b01100110, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_ae(cpu_object):
    """ XOR (HL) - A=Logical XOR A with (value at address HL) """
    cpu_object.register.set_hl(0x1010)

    cpu_object.register.A = 0b10100011
    cpu_object.memory.write_8bit(0x1010, 0b10100011)
    cycles = op.code_ae(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b00000000, H=0x10, L=0x10, F=0b10000000)
    assert_memory(cpu_object,{0x1010:0b10100011})

    cpu_object.register.A = 0b10100011
    cpu_object.memory.write_8bit(0x1010, 0b01100110)
    cycles = op.code_ae(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b11000101, H=0x10, L=0x10, F=0b00000000)
    assert_memory(cpu_object, {0x1010: 0b01100110})


# noinspection PyShadowingNames
def test_code_af(cpu_object):
    """ XOR A - A=Logical XOR A with A """
    cpu_object.register.A = 0b10100011
    cycles = op.code_af(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000000, F=0b10000000)

    cpu_object.register.A = 0b10100011
    cycles = op.code_af(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000000, F=0b10000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_b0(cpu_object):
    """ OR B - A=Logical OR A with B """
    cpu_object.register.A = 0b00000000
    cpu_object.register.B = 0b00000000
    cycles = op.code_b0(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000000, B=0b00000000, F=0b10000000)

    cpu_object.register.A = 0b10100011
    cpu_object.register.B = 0b01100110
    cycles = op.code_b0(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b11100111, B=0b01100110, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_b1(cpu_object):
    """ OR C - A=Logical OR A with C """
    cpu_object.register.A = 0b00000000
    cpu_object.register.C = 0b00000000
    cycles = op.code_b1(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000000, C=0b00000000, F=0b10000000)

    cpu_object.register.A = 0b10100011
    cpu_object.register.C = 0b01100110
    cycles = op.code_b1(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b11100111, C=0b01100110, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_b2(cpu_object):
    """ OR D - A=Logical OR A with D """
    cpu_object.register.A = 0b00000000
    cpu_object.register.D = 0b00000000
    cycles = op.code_b2(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000000, D=0b00000000, F=0b10000000)

    cpu_object.register.A = 0b10100011
    cpu_object.register.D = 0b01100110
    cycles = op.code_b2(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b11100111, D=0b01100110, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_b3(cpu_object):
    """ OR E - A=Logical OR A with E """
    cpu_object.register.A = 0b00000000
    cpu_object.register.E = 0b00000000
    cycles = op.code_b3(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000000, E=0b00000000, F=0b10000000)

    cpu_object.register.A = 0b10100011
    cpu_object.register.E = 0b01100110
    cycles = op.code_b3(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b11100111, E=0b01100110, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_b4(cpu_object):
    """ OR H - A=Logical OR A with H """
    cpu_object.register.A = 0b00000000
    cpu_object.register.H = 0b00000000
    cycles = op.code_b4(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000000, H=0b00000000, F=0b10000000)

    cpu_object.register.A = 0b10100011
    cpu_object.register.H = 0b01100110
    cycles = op.code_b4(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b11100111, H=0b01100110, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_b5(cpu_object):
    """ OR L - A=Logical OR A with L """
    cpu_object.register.A = 0b00000000
    cpu_object.register.L = 0b00000000
    cycles = op.code_b5(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000000, L=0b00000000, F=0b10000000)

    cpu_object.register.A = 0b10100011
    cpu_object.register.L = 0b01100110
    cycles = op.code_b5(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b11100111, L=0b01100110, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_b6(cpu_object):
    """ OR (HL) - A=Logical OR A with (value at address HL) """
    cpu_object.register.set_hl(0x1010)

    cpu_object.register.A = 0b00000000
    cpu_object.memory.write_8bit(0x1010,0b00000000)
    cycles = op.code_b6(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b00000000, H=0x10, L=0x10, F=0b10000000)
    assert_memory(cpu_object)

    cpu_object.register.A = 0b10100011
    cpu_object.memory.write_8bit(0x1010,0b01100110)
    cycles = op.code_b6(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b11100111, H=0x10, L=0x10, F=0b00000000)
    assert_memory(cpu_object,{0x1010:0b01100110})


# noinspection PyShadowingNames
def test_code_b7(cpu_object):
    """ OR L - A=Logical OR A with A (why?) """
    cpu_object.register.A = 0b00000000
    cycles = op.code_b7(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b00000000, F=0b10000000)

    cpu_object.register.A = 0b10100011
    cycles = op.code_b7(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0b10100011, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_b8(cpu_object):
    """ CP A,B - same as SUB A,B but throw the result away, only set flags """
    cpu_object.register.A = 0x00
    cpu_object.register.B = 0x00
    cycles = op.code_b8(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, B=0x00, F=0b11000000)

    cpu_object.register.A = 0x00
    cpu_object.register.B = 0x01
    cycles = op.code_b8(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, B=0x01, F=0b01110000)

    cpu_object.register.A = 0x0F
    cpu_object.register.B = 0x01
    cycles = op.code_b8(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x0F, B=0x01, F=0b01000000)

    cpu_object.register.A = 0xF0
    cpu_object.register.B = 0x10
    cycles = op.code_b8(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xF0, B=0x10, F=0b01000000)

    cpu_object.register.A = 0xFF
    cpu_object.register.B = 0x01
    cycles = op.code_b8(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFF, B=0x01, F=0b01000000)

    cpu_object.register.A = 0xFF
    cpu_object.register.B = 0xFE
    cycles = op.code_b8(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFF, B=0xFE, F=0b01000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_b9(cpu_object):
    """ CP A,C - same as SUB A,C but throw the result away, only set flags """
    cpu_object.register.A = 0x00
    cpu_object.register.C = 0x00
    cycles = op.code_b9(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, C=0x00, F=0b11000000)

    cpu_object.register.A = 0x00
    cpu_object.register.C = 0x01
    cycles = op.code_b9(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, C=0x01, F=0b01110000)

    cpu_object.register.A = 0x0F
    cpu_object.register.C = 0x01
    cycles = op.code_b9(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x0F, C=0x01, F=0b01000000)

    cpu_object.register.A = 0xF0
    cpu_object.register.C = 0x10
    cycles = op.code_b9(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xF0, C=0x10, F=0b01000000)

    cpu_object.register.A = 0xFF
    cpu_object.register.C = 0x01
    cycles = op.code_b9(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFF, C=0x01, F=0b01000000)

    cpu_object.register.A = 0xFF
    cpu_object.register.C = 0xFE
    cycles = op.code_b9(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFF, C=0xFE, F=0b01000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_ba(cpu_object):
    """ CP A,D - same as SUB A,D but throw the result away, only set flags """
    cpu_object.register.A = 0x00
    cpu_object.register.D = 0x00
    cycles = op.code_ba(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, D=0x00, F=0b11000000)

    cpu_object.register.A = 0x00
    cpu_object.register.D = 0x01
    cycles = op.code_ba(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, D=0x01, F=0b01110000)

    cpu_object.register.A = 0x0F
    cpu_object.register.D = 0x01
    cycles = op.code_ba(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x0F, D=0x01, F=0b01000000)

    cpu_object.register.A = 0xF0
    cpu_object.register.D = 0x10
    cycles = op.code_ba(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xF0, D=0x10, F=0b01000000)

    cpu_object.register.A = 0xFF
    cpu_object.register.D = 0x01
    cycles = op.code_ba(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFF, D=0x01, F=0b01000000)

    cpu_object.register.A = 0xFF
    cpu_object.register.D = 0xFE
    cycles = op.code_ba(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFF, D=0xFE, F=0b01000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_bb(cpu_object):
    """ CP A,E - same as SUB A,E but throw the result away, only set flags """
    cpu_object.register.A = 0x00
    cpu_object.register.E = 0x00
    cycles = op.code_bb(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, E=0x00, F=0b11000000)

    cpu_object.register.A = 0x00
    cpu_object.register.E = 0x01
    cycles = op.code_bb(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, E=0x01, F=0b01110000)

    cpu_object.register.A = 0x0F
    cpu_object.register.E = 0x01
    cycles = op.code_bb(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x0F, E=0x01, F=0b01000000)

    cpu_object.register.A = 0xF0
    cpu_object.register.E = 0x10
    cycles = op.code_bb(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xF0, E=0x10, F=0b01000000)

    cpu_object.register.A = 0xFF
    cpu_object.register.E = 0x01
    cycles = op.code_bb(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFF, E=0x01, F=0b01000000)

    cpu_object.register.A = 0xFF
    cpu_object.register.E = 0xFE
    cycles = op.code_bb(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFF, E=0xFE, F=0b01000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_bc(cpu_object):
    """ CP A,H - same as SUB A,H but throw the result away, only set flags """
    cpu_object.register.A = 0x00
    cpu_object.register.H = 0x00
    cycles = op.code_bc(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, H=0x00, F=0b11000000)

    cpu_object.register.A = 0x00
    cpu_object.register.H = 0x01
    cycles = op.code_bc(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, H=0x01, F=0b01110000)

    cpu_object.register.A = 0x0F
    cpu_object.register.H = 0x01
    cycles = op.code_bc(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x0F, H=0x01, F=0b01000000)

    cpu_object.register.A = 0xF0
    cpu_object.register.H = 0x10
    cycles = op.code_bc(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xF0, H=0x10, F=0b01000000)

    cpu_object.register.A = 0xFF
    cpu_object.register.H = 0x01
    cycles = op.code_bc(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFF, H=0x01, F=0b01000000)

    cpu_object.register.A = 0xFF
    cpu_object.register.H = 0xFE
    cycles = op.code_bc(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFF, H=0xFE, F=0b01000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_bd(cpu_object):
    """ CP A,L - same as SUB A,L but throw the result away, only set flags """
    cpu_object.register.A = 0x00
    cpu_object.register.L = 0x00
    cycles = op.code_bd(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, L=0x00, F=0b11000000)

    cpu_object.register.A = 0x00
    cpu_object.register.L = 0x01
    cycles = op.code_bd(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, L=0x01, F=0b01110000)

    cpu_object.register.A = 0x0F
    cpu_object.register.L = 0x01
    cycles = op.code_bd(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x0F, L=0x01, F=0b01000000)

    cpu_object.register.A = 0xF0
    cpu_object.register.L = 0x10
    cycles = op.code_bd(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xF0, L=0x10, F=0b01000000)

    cpu_object.register.A = 0xFF
    cpu_object.register.L = 0x01
    cycles = op.code_bd(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFF, L=0x01, F=0b01000000)

    cpu_object.register.A = 0xFF
    cpu_object.register.L = 0xFE
    cycles = op.code_bd(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFF, L=0xFE, F=0b01000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_be(cpu_object):
    """ CP A,(HL) - same as SUB A,(HL) but throw the result away, only set flags """
    cpu_object.register.set_hl(0x1010)

    cpu_object.register.A = 0x00
    cpu_object.memory.write_8bit(0x1010,0x00)
    cycles = op.code_be(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x00, H=0x10, L=0x10, F=0b11000000)
    assert_memory(cpu_object)

    cpu_object.register.A = 0x00
    cpu_object.memory.write_8bit(0x1010, 0x01)
    cycles = op.code_be(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x00, H=0x10, L=0x10, F=0b01110000)
    assert_memory(cpu_object, {0x1010:0x01})

    cpu_object.register.A = 0x0F
    cpu_object.memory.write_8bit(0x1010, 0x01)
    cycles = op.code_be(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x0F, H=0x10, L=0x10, F=0b01000000)
    assert_memory(cpu_object, {0x1010: 0x01})

    cpu_object.register.A = 0xF0
    cpu_object.memory.write_8bit(0x1010, 0x10)
    cycles = op.code_be(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0xF0, H=0x10, L=0x10, F=0b01000000)
    assert_memory(cpu_object, {0x1010: 0x10})

    cpu_object.register.A = 0xFF
    cpu_object.memory.write_8bit(0x1010, 0x01)
    cycles = op.code_be(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0xFF, H=0x10, L=0x10, F=0b01000000)
    assert_memory(cpu_object, {0x1010: 0x01})

    cpu_object.register.A = 0xFF
    cpu_object.memory.write_8bit(0x1010, 0xFE)
    cycles = op.code_be(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0xFF, H=0x10, L=0x10, F=0b01000000)
    assert_memory(cpu_object, {0x1010: 0xFE})


# noinspection PyShadowingNames
def test_code_bf(cpu_object):
    """ CP A,A - same as SUB A,A but throw the result away, only set flags """
    cpu_object.register.A = 0x00
    cycles = op.code_bf(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x00, F=0b11000000)

    cpu_object.register.A = 0x01
    cycles = op.code_bf(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0x01, F=0b11000000)

    cpu_object.register.A = 0xFF
    cycles = op.code_bf(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object, A=0xFF, F=0b11000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_c0(cpu_object):
    """ RET NZ - Return if flag Z is reset """
    cpu_object.memory.write_8bit(0x1010, 0x50)
    cpu_object.memory.write_8bit(0x1011, 0x40)

    cpu_object.register.SP = 0x1010
    cpu_object.register.PC = 0x0000
    cpu_object.register.F = 0b00000000
    cycles = op.code_c0(cpu_object)
    assert cycles == 20
    assert_registers(cpu_object, SP=0x1012, PC=0x4050)

    cpu_object.register.SP = 0x1010
    cpu_object.register.PC = 0x0000
    cpu_object.register.F = 0b10000000
    cycles = op.code_c0(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, SP=0x1010, PC=0x0000, F=0b10000000)

    assert_memory(cpu_object,{0x1010:0x50, 0x1011:0x40})


# noinspection PyShadowingNames
def test_code_c1(cpu_object):
    """ POP BC - Copy 16-bit value from stack (i.e. SP address) into BC, then increment SP by 2 """
    cpu_object.memory.write_16bit(0xFFFC,0x9933)
    cpu_object.register.SP = 0xFFFC
    cycles = op.code_c1(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, B=0x99, C=0x33, SP=0xFFFE)
    assert_memory(cpu_object,{0xFFFD:0x99,0xFFFC:0x33})


# noinspection PyShadowingNames
def test_code_c2(cpu_object):
    """ JP NZ,a16 - Jump to address a16 if Z flag is reset """
    cpu_object._cartridge_data = bytes.fromhex("FF 55")
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object.register.F = 0b00000000
    cycles = op.code_c2(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, PC=0x55FF)

    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object.register.F = 0b10000000
    cycles = op.code_c2(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, PC=0x0002, F=0b10000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_c3(cpu_object):
    """ JP a16 - Jump to address a16 """
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("FF 55")
    cycles = op.code_c3(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, PC=0x55FF)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_c4(cpu_object):
    """ CALL NZ,a16 - Call address a16 if flag Z is reset """
    cpu_object._cartridge_data = bytes.fromhex("FF 55")

    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object.register.SP = 0xFFFE
    cpu_object.register.F = 0b00000000
    cycles = op.code_c4(cpu_object)
    assert cycles == 24
    assert_registers(cpu_object, PC=0x55FF, SP=0xFFFC)
    assert_memory(cpu_object,{0xFFFC:0x02,0xFFFD:0x00})

    cpu_object.memory.write_16bit(0xFFFC, 0x0000)  # To reset memory before next test
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object.register.SP = 0xFFFE
    cpu_object.register.F = 0b10000000
    cycles = op.code_c4(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, PC=0x0002, SP=0xFFFE, F=0b10000000)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_c5(cpu_object):
    """ PUSH BC - Decrement SP by 2 then push BC value onto stack (i.e. SP address) """
    cpu_object.register.set_bc(0x1122)
    cycles = op.code_c5(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object,B=0x11,C=0x22,SP=0xFFFC)
    assert_memory(cpu_object,{0xFFFC:0x22,0xFFFD:0x11})


# noinspection PyShadowingNames
def test_code_c6(cpu_object):
    """ ADD A,d8 - A=A+d8 """
    cpu_object.register.A = 0x00
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("00")
    cycles = op.code_c6(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x00, F=0b10000000, PC=0x0001)

    cpu_object.register.A = 0x00
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("01")
    cycles = op.code_c6(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x01, F=0b00000000, PC=0x0001)

    cpu_object.register.A = 0x0F
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("01")
    cycles = op.code_c6(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x10, F=0b00100000, PC=0x0001)

    cpu_object.register.A = 0xF0
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("10")
    cycles = op.code_c6(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x00, F=0b10010000, PC=0x0001)

    cpu_object.register.A = 0xFF
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("01")
    cycles = op.code_c6(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x00, F=0b10110000, PC=0x0001)

    cpu_object.register.A = 0xFF
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("02")
    cycles = op.code_c6(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x01, F=0b00110000, PC=0x0001)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_c7(cpu_object):
    """ RST 00H - Push present address onto stack, jump to address $0000 + 00H """
    cpu_object.register.PC = 0x2233
    cpu_object.register.SP = 0x1010
    cycles = op.code_c7(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, PC=0x0000, SP=0x100E)
    assert_memory(cpu_object,{0x100F:0x22, 0x100E:0x33})


# noinspection PyShadowingNames
def test_code_c8(cpu_object):
    """ RET Z - Return if flag Z is set """
    cpu_object.memory.write_8bit(0x1010, 0x50)
    cpu_object.memory.write_8bit(0x1011, 0x40)

    cpu_object.register.SP = 0x1010
    cpu_object.register.PC = 0x0000
    cpu_object.register.F = 0b10000000
    cycles = op.code_c8(cpu_object)
    assert cycles == 20
    assert_registers(cpu_object, SP=0x1012, PC=0x4050, F=0b10000000)

    cpu_object.register.SP = 0x1010
    cpu_object.register.PC = 0x0000
    cpu_object.register.F = 0b00000000
    cycles = op.code_c8(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, SP=0x1010, PC=0x0000)

    assert_memory(cpu_object, {0x1010: 0x50, 0x1011: 0x40})


# noinspection PyShadowingNames
def test_code_c9(cpu_object):
    """ RET - Pop two bytes from stack and jump to that address """
    cpu_object.memory.write_8bit(0x1010, 0x50)
    cpu_object.memory.write_8bit(0x1011, 0x40)

    cpu_object.register.SP = 0x1010
    cpu_object.register.PC = 0x0000
    cycles = op.code_c9(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, SP=0x1012, PC=0x4050)

    assert_memory(cpu_object, {0x1010: 0x50, 0x1011: 0x40})


# noinspection PyShadowingNames
def test_code_ca(cpu_object):
    """ JP Z,a16 - Jump to address a16 if Z flag is set """
    cpu_object._cartridge_data = bytes.fromhex("FF 55")
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object.register.F = 0b10000000
    cycles = op.code_ca(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, PC=0x55FF, F=0b10000000)

    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object.register.F = 0b00000000
    cycles = op.code_ca(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, PC=0x0002)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb(cpu_object):
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("40")
    cpu_object.register.B = 0b00000001
    cycles = op.code_cb(cpu_object)
    assert cycles == 12  # 4 from CB + 8 from CB_40
    assert_registers(cpu_object,B=0b00000001,F=0b10100000,PC=0x0001)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cc(cpu_object):
    """ CALL Z,a16 - Call address a16 if flag Z is set """
    cpu_object._cartridge_data = bytes.fromhex("FF 55")

    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object.register.SP = 0xFFFE
    cpu_object.register.F = 0b10000000
    cycles = op.code_cc(cpu_object)
    assert cycles == 24
    assert_registers(cpu_object, PC=0x55FF, SP=0xFFFC, F=0b10000000)
    assert_memory(cpu_object, {0xFFFC: 0x02, 0xFFFD: 0x00})

    cpu_object.memory.write_16bit(0xFFFC, 0x0000)  # To reset memory before next test
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object.register.SP = 0xFFFE
    cpu_object.register.F = 0b00000000
    cycles = op.code_cc(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, PC=0x0002, SP=0xFFFE)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cd(cpu_object):
    """ CALL a16 - Push address of next instruction onto stack then jump to address a16 """
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("FF 55")
    cpu_object.register.SP = 0xFFFE
    cycles = op.code_cd(cpu_object)
    assert cycles == 24
    assert_registers(cpu_object, PC=0x55FF, SP=0xFFFC,)
    assert_memory(cpu_object, {0xFFFC: 0x02, 0xFFFD: 0x00})


# noinspection PyShadowingNames
def test_code_ce(cpu_object):
    """ ADC A,d8 - A=A+d8+carry_flag (yes, '+carry_flag' is just +1 or +0) """
    cpu_object.register.A = 0x00
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("00")
    cpu_object.register.F = 0b00000000
    cycles = op.code_ce(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x00, F=0b10000000, PC=0x0001)

    cpu_object.register.A = 0x00
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("00")
    cpu_object.register.F = 0b00010000
    cycles = op.code_ce(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x01, F=0b00000000, PC=0x0001)

    cpu_object.register.A = 0x00
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("01")
    cpu_object.register.F = 0b00010000
    cycles = op.code_ce(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x02, F=0b00000000, PC=0x0001)

    cpu_object.register.A = 0x0E
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("01")
    cpu_object.register.F = 0b00010000
    cycles = op.code_ce(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x10, F=0b00100000, PC=0x0001)

    cpu_object.register.A = 0xF0
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("0F")
    cpu_object.register.F = 0b00010000
    cycles = op.code_ce(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x00, F=0b10110000, PC=0x0001)

    cpu_object.register.A = 0xFE
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("01")
    cpu_object.register.F = 0b00010000
    cycles = op.code_ce(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x00, F=0b10110000, PC=0x0001)

    cpu_object.register.A = 0xFE
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("02")
    cpu_object.register.F = 0b00010000
    cycles = op.code_ce(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x01, F=0b00110000, PC=0x0001)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cf(cpu_object):
    """ RST 08H - Push present address onto stack, jump to address $0000 + 08H """
    cpu_object.register.PC = 0x2233
    cpu_object.register.SP = 0x1010
    cycles = op.code_cf(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, PC=0x0008, SP=0x100E)
    assert_memory(cpu_object, {0x100F: 0x22, 0x100E: 0x33})


# noinspection PyShadowingNames
def test_code_d0(cpu_object):
    """ RET NC - Return if flag C is reset """
    cpu_object.memory.write_8bit(0x1010, 0x50)
    cpu_object.memory.write_8bit(0x1011, 0x40)

    cpu_object.register.SP = 0x1010
    cpu_object.register.PC = 0x0000
    cpu_object.register.F = 0b00000000
    cycles = op.code_d0(cpu_object)
    assert cycles == 20
    assert_registers(cpu_object, SP=0x1012, PC=0x4050)

    cpu_object.register.SP = 0x1010
    cpu_object.register.PC = 0x0000
    cpu_object.register.F = 0b00010000
    cycles = op.code_d0(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, SP=0x1010, PC=0x0000, F=0b00010000)

    assert_memory(cpu_object, {0x1010: 0x50, 0x1011: 0x40})


# noinspection PyShadowingNames
def test_code_d1(cpu_object):
    """ POP DE - Copy 16-bit value from stack (i.e. SP address) into DE, then increment SP by 2 """
    cpu_object.memory.write_16bit(0xFFFC, 0x9933)
    cpu_object.register.SP = 0xFFFC
    cycles = op.code_d1(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, D=0x99, E=0x33, SP=0xFFFE)
    assert_memory(cpu_object, {0xFFFD: 0x99, 0xFFFC: 0x33})


# noinspection PyShadowingNames
def test_code_d2(cpu_object):
    """ JP NC,a16 - Jump to address a16 if C flag is reset """
    cpu_object._cartridge_data = bytes.fromhex("FF 55")
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object.register.F = 0b00000000
    cycles = op.code_d2(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, PC=0x55FF)

    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object.register.F = 0b00010000
    cycles = op.code_d2(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, PC=0x0002, F=0b00010000)

    assert_memory(cpu_object)


# OPCODE D3 is unused


# noinspection PyShadowingNames
def test_code_d4(cpu_object):
    """ CALL NC,a16 - Call address a16 if flag C is reset """
    cpu_object._cartridge_data = bytes.fromhex("FF 55")

    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object.register.SP = 0xFFFE
    cpu_object.register.F = 0b00000000
    cycles = op.code_d4(cpu_object)
    assert cycles == 24
    assert_registers(cpu_object, PC=0x55FF, SP=0xFFFC)
    assert_memory(cpu_object, {0xFFFC: 0x02, 0xFFFD: 0x00})

    cpu_object.memory.write_16bit(0xFFFC, 0x0000)  # To reset memory before next test
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object.register.SP = 0xFFFE
    cpu_object.register.F = 0b00010000
    cycles = op.code_d4(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, PC=0x0002, SP=0xFFFE, F=0b00010000)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_d5(cpu_object):
    """ PUSH DE - Decrement SP by 2 then push DE value onto stack (i.e. SP address) """
    cpu_object.register.set_de(0x1122)
    cycles = op.code_d5(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, D=0x11, E=0x22, SP=0xFFFC)
    assert_memory(cpu_object, {0xFFFC: 0x22, 0xFFFD: 0x11})


# noinspection PyShadowingNames
def test_code_d6(cpu_object):
    """ SUB A,d8 - A=A-d8 """
    cpu_object.register.A = 0x00
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("00")
    cycles = op.code_d6(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x00, F=0b11000000, PC=0x0001)

    cpu_object.register.A = 0x00
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("01")
    cycles = op.code_d6(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0xFF, F=0b01110000, PC=0x0001)

    cpu_object.register.A = 0x0F
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("01")
    cycles = op.code_d6(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x0E, F=0b01000000, PC=0x0001)

    cpu_object.register.A = 0xF0
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("10")
    cycles = op.code_d6(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0xE0, F=0b01000000, PC=0x0001)

    cpu_object.register.A = 0xFF
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("01")
    cycles = op.code_d6(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0xFE, F=0b01000000, PC=0x0001)

    cpu_object.register.A = 0xFF
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("FE")
    cycles = op.code_d6(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x01, F=0b01000000, PC=0x0001)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_d7(cpu_object):
    """ RST 10H - Push present address onto stack, jump to address $0000 + 10H """
    cpu_object.register.PC = 0x2233
    cpu_object.register.SP = 0x1010
    cycles = op.code_d7(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, PC=0x0010, SP=0x100E)
    assert_memory(cpu_object, {0x100F: 0x22, 0x100E: 0x33})


# noinspection PyShadowingNames
def test_code_d8(cpu_object):
    """ RET C - Return if flag C is set """
    cpu_object.memory.write_8bit(0x1010, 0x50)
    cpu_object.memory.write_8bit(0x1011, 0x40)

    cpu_object.register.SP = 0x1010
    cpu_object.register.PC = 0x0000
    cpu_object.register.F = 0b00010000
    cycles = op.code_d8(cpu_object)
    assert cycles == 20
    assert_registers(cpu_object, SP=0x1012, PC=0x4050, F=0b00010000)

    cpu_object.register.SP = 0x1010
    cpu_object.register.PC = 0x0000
    cpu_object.register.F = 0b00000000
    cycles = op.code_d8(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, SP=0x1010, PC=0x0000)

    assert_memory(cpu_object, {0x1010: 0x50, 0x1011: 0x40})


# noinspection PyShadowingNames
def test_code_d9(cpu_object):
    """ RETI - Pop two bytes from stack and jump to that address then enable interrupts """
    cpu_object.memory.write_8bit(0x1010, 0x50)
    cpu_object.memory.write_8bit(0x1011, 0x40)

    cpu_object.register.SP = 0x1010
    cpu_object.register.PC = 0x0000
    cycles = op.code_d9(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, SP=0x1012, PC=0x4050)

    assert_memory(cpu_object, {0x1010: 0x50, 0x1011: 0x40})
    # Since interrupt enable will be done during "interrupt update" step, it cannot be tested here


# noinspection PyShadowingNames
def test_code_da(cpu_object):
    """ JP C,a16 - Jump to address a16 if C flag is set """
    cpu_object._cartridge_data = bytes.fromhex("FF 55")
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object.register.F = 0b00010000
    cycles = op.code_da(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, PC=0x55FF, F=0b00010000)

    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object.register.F = 0b00000000
    cycles = op.code_da(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, PC=0x0002)

    assert_memory(cpu_object)


# OPCODE DB is unused


# noinspection PyShadowingNames
def test_code_dc(cpu_object):
    """ CALL C,a16 - Call address a16 if flag C is set """
    cpu_object._cartridge_data = bytes.fromhex("FF 55")

    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object.register.SP = 0xFFFE
    cpu_object.register.F = 0b00010000
    cycles = op.code_dc(cpu_object)
    assert cycles == 24
    assert_registers(cpu_object, PC=0x55FF, SP=0xFFFC, F=0b00010000)
    assert_memory(cpu_object, {0xFFFC: 0x02, 0xFFFD: 0x00})

    cpu_object.memory.write_16bit(0xFFFC, 0x0000)  # To reset memory before next test
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object.register.SP = 0xFFFE
    cpu_object.register.F = 0b00000000
    cycles = op.code_dc(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, PC=0x0002, SP=0xFFFE)
    assert_memory(cpu_object)


# OPCODE DD is unused


# noinspection PyShadowingNames
def test_code_de(cpu_object):
    """ SBC A,d8 - A=A-d8-carry_flag (yes, '-carry_flag' is just -1 or -0) """
    cpu_object.register.A = 0x00
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("00")
    cpu_object.register.F = 0b00000000
    cycles = op.code_de(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x00, F=0b11000000, PC=0x0001)

    cpu_object.register.A = 0x02
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("00")
    cpu_object.register.F = 0b00010000
    cycles = op.code_de(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x01, F=0b01000000, PC=0x0001)

    cpu_object.register.A = 0x00
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("01")
    cpu_object.register.F = 0b00010000
    cycles = op.code_de(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0xFE, F=0b01110000, PC=0x0001)

    cpu_object.register.A = 0x13
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("04")
    cpu_object.register.F = 0b00010000
    cycles = op.code_de(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x0E, F=0b01100000, PC=0x0001)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_df(cpu_object):
    """ RST 18H - Push present address onto stack, jump to address $0000 + 18H """
    cpu_object.register.PC = 0x2233
    cpu_object.register.SP = 0x1010
    cycles = op.code_df(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, PC=0x0018, SP=0x100E)
    assert_memory(cpu_object, {0x100F: 0x22, 0x100E: 0x33})


# noinspection PyShadowingNames
def test_code_e0(cpu_object):
    """ LDH (d8),A or LD ($FF00+d8),A - Put A into address ($FF00 + d8) """
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("55")
    cpu_object.register.A = 0x10
    cycles = op.code_e0(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object,A=0x10,PC=0x0001)
    assert_memory(cpu_object,{0xFF55:0x10})


# noinspection PyShadowingNames
def test_code_e1(cpu_object):
    """ POP HL - Copy 16-bit value from stack (i.e. SP address) into HL, then increment SP by 2 """
    cpu_object.memory.write_16bit(0xFFFC, 0x9933)
    cpu_object.register.SP = 0xFFFC
    cycles = op.code_e1(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, H=0x99, L=0x33, SP=0xFFFE)
    assert_memory(cpu_object, {0xFFFD: 0x99, 0xFFFC: 0x33})


# noinspection PyShadowingNames
def test_code_e2(cpu_object):
    """ LD (C),A or LD ($FF00+C),A - Put A into address ($FF00 + register C) """
    cpu_object.register.A = 0x10
    cpu_object.register.C = 0x55
    cycles = op.code_e2(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x10, C=0x55)
    assert_memory(cpu_object, {0xFF55: 0x10})


# OPCODE E3 is unused


# OPCODE E4 is unused


# noinspection PyShadowingNames
def test_code_e5(cpu_object):
    """ PUSH HL - Decrement SP by 2 then push HL value onto stack (i.e. SP address) """
    cpu_object.register.set_hl(0x1122)
    cycles = op.code_e5(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x11, L=0x22, SP=0xFFFC)
    assert_memory(cpu_object, {0xFFFC: 0x22, 0xFFFD: 0x11})


# noinspection PyShadowingNames
def test_code_e6(cpu_object):
    """ AND d8 - A=Logical AND A with d8 """
    cpu_object.register.A = 0b10100011
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = 0b01000100.to_bytes(1,byteorder="big")
    cycles = op.code_e6(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b00000000, F=0b10100000, PC=0x0001)

    cpu_object.register.A = 0b10100011
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = 0b01100110.to_bytes(1, byteorder="big")
    cycles = op.code_e6(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b00100010, F=0b00100000, PC=0x0001)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_e7(cpu_object):
    """ RST 20H - Push present address onto stack, jump to address $0000 + 20H """
    cpu_object.register.PC = 0x2233
    cpu_object.register.SP = 0x1010
    cycles = op.code_e7(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, PC=0x0020, SP=0x100E)
    assert_memory(cpu_object, {0x100F: 0x22, 0x100E: 0x33})


# noinspection PyShadowingNames
def test_code_e8(cpu_object):
    """ LD HL,SP+d8 or LDHL SP,r8 - Put result of SP+r8 into HL (r8 is a signed value) """
    cpu_object.register.SP = 0x0000
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("0F")
    cycles = op.code_e8(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, SP=0x000F, F=0b00000000, PC=0x0001)

    cpu_object.register.SP = 0x0101
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("7F")
    cycles = op.code_e8(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, SP=0x0180, F=0b00100000, PC=0x0001)

    cpu_object.register.SP = 0xFFFF
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("01")
    cycles = op.code_e8(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, SP=0x0000, F=0b00110000, PC=0x0001)

    cpu_object.register.SP = 0xFFFF
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("80")  # negative value, -128
    cycles = op.code_e8(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, SP=0xFF7F, F=0b00000000, PC=0x0001)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_e9(cpu_object):
    """ JP (HL) - Jump to address contained in HL """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_16bit(0x1010,0x5566)
    cycles = op.code_e9(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object,H=0x10,L=0x10,PC=0x5566)
    assert_memory(cpu_object,{0x1010:0x66,0x1011:0x55})


# noinspection PyShadowingNames
def test_code_ea(cpu_object):
    """ LD (a16),A - Stores reg at the address in a16 (least significant byte first) """
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("11 10")
    cpu_object.register.A = 0x99
    cycles = op.code_ea(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, A=0x99, PC=0x0002)
    assert_memory(cpu_object,{0x1011:0x99})


# OPCODE EB is unused


# OPCODE EC is unused


# OPCODE ED is unused


# noinspection PyShadowingNames
def test_code_ee(cpu_object):
    """ XOR d8 - A=Logical XOR A with d8 """
    cpu_object.register.A = 0b10100011
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = 0b10100011.to_bytes(1, byteorder="big")
    cycles = op.code_ee(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b00000000, F=0b10000000, PC=0x0001)

    cpu_object.register.A = 0b10100011
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = 0b01100110.to_bytes(1, byteorder="big")
    cycles = op.code_ee(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b11000101, F=0b00000000, PC=0x0001)


# noinspection PyShadowingNames
def test_code_ef(cpu_object):
    """ RST 28H - Push present address onto stack, jump to address $0000 + 28H """
    cpu_object.register.PC = 0x2233
    cpu_object.register.SP = 0x1010
    cycles = op.code_ef(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, PC=0x0028, SP=0x100E)
    assert_memory(cpu_object, {0x100F: 0x22, 0x100E: 0x33})


# noinspection PyShadowingNames
def test_code_f0(cpu_object):
    """ LDH A,(d8) or LD A,($FF00+d8) - Put value at address ($FF00 + d8) into A """
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("11")
    cpu_object.memory.write_8bit(0xFF11,0x55)
    cycles = op.code_f0(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object,A=0x55,PC=0x0001)
    assert_memory(cpu_object,{0xFF11:0x55})


# noinspection PyShadowingNames
def test_code_f1(cpu_object):
    """ POP AF - Copy 16-bit value from stack (i.e. SP address) into AF, then increment SP by 2 """
    cpu_object.memory.write_16bit(0xFFFC, 0x9933)
    cpu_object.register.SP = 0xFFFC
    cycles = op.code_f1(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, A=0x99, F=0x33, SP=0xFFFE)
    assert_memory(cpu_object, {0xFFFD: 0x99, 0xFFFC: 0x33})


# noinspection PyShadowingNames
def test_code_f2(cpu_object):
    """ LD A,(C) or LD A,($FF00+C) - Put value at address ($FF00 + register C) into A """
    cpu_object.register.C = 0x11
    cpu_object.memory.write_8bit(0xFF11, 0x55)
    cycles = op.code_f2(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x55, C=0x11)
    assert_memory(cpu_object, {0xFF11: 0x55})


# noinspection PyShadowingNames
def test_code_f3(cpu_object):
    """ DI - Disable interrupts AFTER THE NEXT INSTRUCTION IS EXECUTED """
    cycles = op.code_f3(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object)
    assert_memory(cpu_object)
    # Since interrupt disable will be done during "interrupt update" step, it cannot be tested here


# OPCODE F4 is unused


# noinspection PyShadowingNames
def test_code_f5(cpu_object):
    """ PUSH AF - Decrement SP by 2 then push AF value onto stack (i.e. SP address) """
    cpu_object.register.set_af(0x1122)
    cycles = op.code_f5(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, A=0x11, F=0x22, SP=0xFFFC)
    assert_memory(cpu_object, {0xFFFC: 0x22, 0xFFFD: 0x11})


# noinspection PyShadowingNames
def test_code_f6(cpu_object):
    """ OR d8 - A=Logical OR A with d8 """
    cpu_object.register.A = 0b00000000
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = 0b00000000.to_bytes(1, byteorder="big")
    cycles = op.code_f6(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b00000000, F=0b10000000, PC=0x0001)

    cpu_object.register.A = 0b10100011
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = 0b01100110.to_bytes(1, byteorder="big")
    cycles = op.code_f6(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b11100111, F=0b00000000, PC=0x0001)


# noinspection PyShadowingNames
def test_code_f7(cpu_object):
    """ RST 30H - Push present address onto stack, jump to address $0000 + 30H """
    cpu_object.register.PC = 0x2233
    cpu_object.register.SP = 0x1010
    cycles = op.code_f7(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, PC=0x0030, SP=0x100E)
    assert_memory(cpu_object, {0x100F: 0x22, 0x100E: 0x33})


# noinspection PyShadowingNames
def test_code_f8(cpu_object):
    """ LD HL,SP+d8 or LDHL SP,r8 - Put result of SP+r8 into HL (r8 is a signed value) """
    cpu_object.register.SP = 0x0000
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("0F")
    cycles = op.code_f8(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, H=0x00, L=0x0F, SP=0x0000, F=0b00000000, PC=0x0001)

    cpu_object.register.SP = 0x0101
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("7F")
    cycles = op.code_f8(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, H=0x01, L=0x80, SP=0x0101, F=0b00100000, PC=0x0001)

    cpu_object.register.SP = 0xFFFF
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("01")
    cycles = op.code_f8(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, H=0x00, L=0x00, SP=0xFFFF, F=0b00110000, PC=0x0001)

    cpu_object.register.SP = 0xFFFF
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("80")  # negative value, -128
    cycles = op.code_f8(cpu_object)
    assert cycles == 12
    assert_registers(cpu_object, H=0xFF, L=0x7F, SP=0xFFFF, F=0b00000000, PC=0x0001)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_f9(cpu_object):
    """ LD SP,HL - Put HL value into SP """
    cpu_object.register.set_hl(0x9933)
    cycles = op.code_f9(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0x99, L=0x33, SP=0x9933)


# noinspection PyShadowingNames
def test_code_fa(cpu_object):
    """ LD A,(a16) - Load reg with the value at the address in a16 (least significant byte first) """
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("11 10")
    cpu_object.memory.write_8bit(0x1011,0x55)
    cycles = op.code_fa(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object,A=0x55,PC=0x0002)
    assert_memory(cpu_object,{0x1011:0x55})


# noinspection PyShadowingNames
def test_code_fb(cpu_object):
    """ EI - Enable interrupts AFTER THE NEXT INSTRUCTION IS EXECUTED """
    cycles = op.code_fb(cpu_object)
    assert cycles == 4
    assert_registers(cpu_object)
    assert_memory(cpu_object)
    # Since interrupt enable will be done during "interrupt update" step, it cannot be tested here


# OPCODE FC is unused


# OPCODE FD is unused


# noinspection PyShadowingNames
def test_code_fe(cpu_object):
    """ CP A,d8 - same as SUB A,d8 but throw the result away, only set flags """
    cpu_object.register.A = 0x00
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("00")
    cycles = op.code_fe(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x00, F=0b11000000, PC=0x0001)

    cpu_object.register.A = 0x00
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("01")
    cycles = op.code_fe(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x00, F=0b01110000, PC=0x0001)

    cpu_object.register.A = 0x0F
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("01")
    cycles = op.code_fe(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x0F, F=0b01000000, PC=0x0001)

    cpu_object.register.A = 0xF0
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("10")
    cycles = op.code_fe(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0xF0, F=0b01000000, PC=0x0001)

    cpu_object.register.A = 0xFF
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("01")
    cycles = op.code_fe(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0xFF, F=0b01000000, PC=0x0001)

    cpu_object.register.A = 0xFF
    cpu_object.register.PC = 0x0000  # So we can test without having to add a lot of useless blank data to test array
    cpu_object._cartridge_data = bytes.fromhex("FE")
    cycles = op.code_fe(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0xFF, F=0b01000000, PC=0x0001)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_ff(cpu_object):
    """ RST 38H - Push present address onto stack, jump to address $0000 + 38H """
    cpu_object.register.PC = 0x2233
    cpu_object.register.SP = 0x1010
    cycles = op.code_ff(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, PC=0x0038, SP=0x100E)
    assert_memory(cpu_object, {0x100F: 0x22, 0x100E: 0x33})


""" CB-Prefix operations """


# noinspection PyShadowingNames
def test_code_cb_00(cpu_object):
    """ RLC B - Copy register B bit 7 to Carry flag, then rotate register B left """
    cpu_object.register.B = 0b11100010
    cycles = op.code_cb_00(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b11000101, F=0b00010000)

    cpu_object.register.B = 0b00000000
    cycles = op.code_cb_00(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b00000000, F=0b10000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_01(cpu_object):
    """ RLC C - Copy register C bit 7 to Carry flag, then rotate register C left """
    cpu_object.register.C = 0b11100010
    cycles = op.code_cb_01(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b11000101, F=0b00010000)

    cpu_object.register.C = 0b00000000
    cycles = op.code_cb_01(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b00000000, F=0b10000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_02(cpu_object):
    """ RLC D - Copy register D bit 7 to Carry flag, then rotate register D left """
    cpu_object.register.D = 0b11100010
    cycles = op.code_cb_02(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b11000101, F=0b00010000)

    cpu_object.register.D = 0b00000000
    cycles = op.code_cb_02(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b00000000, F=0b10000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_03(cpu_object):
    """ RLC E - Copy register E bit 7 to Carry flag, then rotate register E left """
    cpu_object.register.E = 0b11100010
    cycles = op.code_cb_03(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b11000101, F=0b00010000)

    cpu_object.register.E = 0b00000000
    cycles = op.code_cb_03(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b00000000, F=0b10000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_04(cpu_object):
    """ RLC H - Copy register H bit 7 to Carry flag, then rotate register H left """
    cpu_object.register.H = 0b11100010
    cycles = op.code_cb_04(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b11000101, F=0b00010000)

    cpu_object.register.H = 0b00000000
    cycles = op.code_cb_04(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b00000000, F=0b10000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_05(cpu_object):
    """ RLC L - Copy register L bit 7 to Carry flag, then rotate register L left """
    cpu_object.register.L = 0b11100010
    cycles = op.code_cb_05(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b11000101, F=0b00010000)

    cpu_object.register.L = 0b00000000
    cycles = op.code_cb_05(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b00000000, F=0b10000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_06(cpu_object):
    """ RLC (HL) - Copy (value at address HL) bit 7 to Carry flag, then rotate (value at address HL) left """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010,0b11100010)
    cycles = op.code_cb_06(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b00010000)
    assert_memory(cpu_object,{0x1010:0b11000101})

    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b00000000)
    cycles = op.code_cb_06(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b10000000)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_07(cpu_object):
    """ RLC A - Copy register A bit 7 to Carry flag, then rotate register A left """
    cpu_object.register.A = 0b11100010
    cycles = op.code_cb_07(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b11000101, F=0b00010000)

    cpu_object.register.A = 0b00000000
    cycles = op.code_cb_07(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b00000000, F=0b10000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_08(cpu_object):
    """ RRC B - Copy register B bit 0 to Carry flag, then rotate register B right """
    cpu_object.register.B = 0b11100011
    cycles = op.code_cb_08(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b11110001, F=0b00010000)

    cpu_object.register.B = 0b00000000
    cycles = op.code_cb_08(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b00000000, F=0b10000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_09(cpu_object):
    """ RRC C - Copy register C bit 0 to Carry flag, then rotate register C right """
    cpu_object.register.C = 0b11100011
    cycles = op.code_cb_09(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b11110001, F=0b00010000)

    cpu_object.register.C = 0b00000000
    cycles = op.code_cb_09(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b00000000, F=0b10000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_0a(cpu_object):
    """ RRC D - Copy register D bit 0 to Carry flag, then rotate register D right """
    cpu_object.register.D = 0b11100011
    cycles = op.code_cb_0a(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b11110001, F=0b00010000)

    cpu_object.register.D = 0b00000000
    cycles = op.code_cb_0a(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b00000000, F=0b10000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_0b(cpu_object):
    """ RRC E - Copy register E bit 0 to Carry flag, then rotate register E right """
    cpu_object.register.E = 0b11100011
    cycles = op.code_cb_0b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b11110001, F=0b00010000)

    cpu_object.register.E = 0b00000000
    cycles = op.code_cb_0b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b00000000, F=0b10000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_0c(cpu_object):
    """ RRC H - Copy register H bit 0 to Carry flag, then rotate register H right """
    cpu_object.register.H = 0b11100011
    cycles = op.code_cb_0c(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b11110001, F=0b00010000)

    cpu_object.register.H = 0b00000000
    cycles = op.code_cb_0c(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b00000000, F=0b10000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_0d(cpu_object):
    """ RRC L - Copy register L bit 0 to Carry flag, then rotate register L right """
    cpu_object.register.L = 0b11100011
    cycles = op.code_cb_0d(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b11110001, F=0b00010000)

    cpu_object.register.L = 0b00000000
    cycles = op.code_cb_0d(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b00000000, F=0b10000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_0e(cpu_object):
    """ RRC (HL) - Copy bit 0 to Carry flag, then rotate right """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010,0b11100011)
    cycles = op.code_cb_0e(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b00010000)
    assert_memory(cpu_object,{0x1010:0b11110001})

    cpu_object.memory.write_8bit(0x1010, 0b00000000)
    cycles = op.code_cb_0e(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b10000000)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_0f(cpu_object):
    """ RRC A - Copy register A bit 0 to Carry flag, then rotate register A right """
    cpu_object.register.A = 0b11100011
    cycles = op.code_cb_0f(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b11110001, F=0b00010000)

    cpu_object.register.A = 0b00000000
    cycles = op.code_cb_0f(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b00000000, F=0b10000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_10(cpu_object):
    """ RL B - Copy register B bit 7 to temp, replace B bit 7 w/ Carry flag, rotate B left, copy temp to Carry flag """
    cpu_object.register.B = 0b11100010
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_10(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b11000101, F=0b00010000)

    cpu_object.register.B = 0b00000000
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_10(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b00000001, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_11(cpu_object):
    """ RL C - Copy register C bit 7 to temp, replace C bit 7 w/ Carry flag, rotate C left, copy temp to Carry flag """
    cpu_object.register.C = 0b11100010
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_11(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b11000101, F=0b00010000)

    cpu_object.register.C = 0b00000000
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_11(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b00000001, F=0b00000000)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_12(cpu_object):
    """ RL D - Copy register D bit 7 to temp, replace D bit 7 w/ Carry flag, rotate D left, copy temp to Carry flag """
    cpu_object.register.D = 0b11100010
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_12(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b11000101, F=0b00010000)

    cpu_object.register.D = 0b00000000
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_12(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b00000001, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_13(cpu_object):
    """ RL E - Copy register E bit 7 to temp, replace E bit 7 w/ Carry flag, rotate E left, copy temp to Carry flag """
    cpu_object.register.E = 0b11100010
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_13(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b11000101, F=0b00010000)

    cpu_object.register.E = 0b00000000
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_13(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b00000001, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_14(cpu_object):
    """ RL H - Copy register H bit 7 to temp, replace H bit 7 w/ Carry flag, rotate H left, copy temp to Carry flag """
    cpu_object.register.H = 0b11100010
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_14(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b11000101, F=0b00010000)

    cpu_object.register.H = 0b00000000
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_14(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b00000001, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_15(cpu_object):
    """ RL L - Copy register L bit 7 to temp, replace L bit 7 w/ Carry flag, rotate L left, copy temp to Carry flag """
    cpu_object.register.L = 0b11100010
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_15(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b11000101, F=0b00010000)

    cpu_object.register.L = 0b00000000
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_15(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b00000001, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_16(cpu_object):
    """ RL (HL) - Copy bit 7 to temp, replace bit 7 w/ Carry flag, rotate left, copy temp to Carry flag """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b11100010)
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_16(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b00010000)
    assert_memory(cpu_object,{0x1010:0b11000101})

    cpu_object.memory.write_8bit(0x1010, 0b00000000)
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_16(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b00000000)
    assert_memory(cpu_object, {0x1010: 0b00000001})


# noinspection PyShadowingNames
def test_code_cb_17(cpu_object):
    """ RL A - Copy register A bit 7 to temp, replace A bit 7 w/ Carry flag, rotate A left, copy temp to Carry flag """
    cpu_object.register.A = 0b11100010
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_17(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b11000101, F=0b00010000)

    cpu_object.register.A = 0b00000000
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_17(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b00000001, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_18(cpu_object):
    """ RR B - Copy register B bit 0 to temp, replace B bit 0 w/ Carry flag, rotate B right, copy temp to Carry flag """
    cpu_object.register.B = 0b11100011
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_18(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b11110001, F=0b00010000)

    cpu_object.register.B = 0b00000000
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_18(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b10000000, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_19(cpu_object):
    """ RR C - Copy register C bit 0 to temp, replace C bit 0 w/ Carry flag, rotate C right, copy temp to Carry flag """
    cpu_object.register.C = 0b11100011
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_19(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b11110001, F=0b00010000)

    cpu_object.register.C = 0b00000000
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_19(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b10000000, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_1a(cpu_object):
    """ RR D - Copy register D bit 0 to temp, replace D bit 0 w/ Carry flag, rotate D right, copy temp to Carry flag """
    cpu_object.register.D = 0b11100011
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_1a(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b11110001, F=0b00010000)

    cpu_object.register.D = 0b00000000
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_1a(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b10000000, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_1b(cpu_object):
    """ RR E - Copy register E bit 0 to temp, replace E bit 0 w/ Carry flag, rotate E right, copy temp to Carry flag """
    cpu_object.register.E = 0b11100011
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_1b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b11110001, F=0b00010000)

    cpu_object.register.E = 0b00000000
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_1b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b10000000, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_1c(cpu_object):
    """ RR H - Copy register H bit 0 to temp, replace H bit 0 w/ Carry flag, rotate H right, copy temp to Carry flag """
    cpu_object.register.H = 0b11100011
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_1c(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b11110001, F=0b00010000)

    cpu_object.register.H = 0b00000000
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_1c(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b10000000, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_1d(cpu_object):
    """ RR L - Copy register L bit 0 to temp, replace L bit 0 w/ Carry flag, rotate L right, copy temp to Carry flag """
    cpu_object.register.L = 0b11100011
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_1d(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b11110001, F=0b00010000)

    cpu_object.register.L = 0b00000000
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_1d(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b10000000, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_1e(cpu_object):
    """ RR (HL) - Copy (HL) bit 0 to temp, replace bit 0 w/ Carry flag, rotate right, copy temp to Carry flag """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b11100011)
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_1e(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b00010000)
    assert_memory(cpu_object,{0x1010:0b11110001})

    cpu_object.memory.write_8bit(0x1010, 0b00000000)
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_1e(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b00000000)
    assert_memory(cpu_object, {0x1010: 0b10000000})


# noinspection PyShadowingNames
def test_code_cb_1f(cpu_object):
    """ RR A - Copy register A bit 0 to temp, replace A bit 0 w/ Carry flag, rotate A right, copy temp to Carry flag """
    cpu_object.register.A = 0b11100011
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_1f(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b11110001, F=0b00010000)

    cpu_object.register.A = 0b00000000
    cpu_object.register.F = 0b00010000
    cycles = op.code_cb_1f(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b10000000, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_20(cpu_object):
    """ SLA B - Copy B bit 7 to temp, replace B bit 7 w/ zero, rotate B left, copy temp to Carry flag """
    cpu_object.register.B = 0b11100010
    cycles = op.code_cb_20(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b11000100, F=0b00010000)

    cpu_object.register.B = 0b00000000
    cycles = op.code_cb_20(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b00000000, F=0b10000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_21(cpu_object):
    """ SLA C - Copy C bit 7 to temp, replace C bit 7 w/ zero, rotate C left, copy temp to Carry flag """
    cpu_object.register.C = 0b11100010
    cycles = op.code_cb_21(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b11000100, F=0b00010000)

    cpu_object.register.C = 0b00000000
    cycles = op.code_cb_21(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b00000000, F=0b10000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_22(cpu_object):
    """ SLA D - Copy D bit 7 to temp, replace D bit 7 w/ zero, rotate D left, copy temp to Carry flag """
    cpu_object.register.D = 0b11100010
    cycles = op.code_cb_22(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b11000100, F=0b00010000)

    cpu_object.register.D = 0b00000000
    cycles = op.code_cb_22(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b00000000, F=0b10000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_23(cpu_object):
    """ SLA E - Copy E bit 7 to temp, replace E bit 7 w/ zero, rotate E left, copy temp to Carry flag """
    cpu_object.register.E = 0b11100010
    cycles = op.code_cb_23(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b11000100, F=0b00010000)

    cpu_object.register.E = 0b00000000
    cycles = op.code_cb_23(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b00000000, F=0b10000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_24(cpu_object):
    """ SLA H - Copy H bit 7 to temp, replace H bit 7 w/ zero, rotate H left, copy temp to Carry flag """
    cpu_object.register.H = 0b11100010
    cycles = op.code_cb_24(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b11000100, F=0b00010000)

    cpu_object.register.H = 0b00000000
    cycles = op.code_cb_24(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b00000000, F=0b10000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_25(cpu_object):
    """ SLA L - Copy L bit 7 to temp, replace L bit 7 w/ zero, rotate L left, copy temp to Carry flag """
    cpu_object.register.L = 0b11100010
    cycles = op.code_cb_25(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b11000100, F=0b00010000)

    cpu_object.register.L = 0b00000000
    cycles = op.code_cb_25(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b00000000, F=0b10000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_26(cpu_object):
    """ SLA (HL) - Copy (HL) bit 7 to temp, replace bit 7 w/ zero, rotate left, copy temp to Carry flag """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b11100010)
    cycles = op.code_cb_26(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b00010000)
    assert_memory(cpu_object,{0x1010:0b11000100})

    cpu_object.memory.write_8bit(0x1010, 0b00000000)
    cycles = op.code_cb_26(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b10000000)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_27(cpu_object):
    """ SLA A - Copy A bit 7 to temp, replace A bit 7 w/ zero, rotate A left, copy temp to Carry flag """
    cpu_object.register.A = 0b11100010
    cycles = op.code_cb_27(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b11000100, F=0b00010000)

    cpu_object.register.A = 0b00000000
    cycles = op.code_cb_27(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b00000000, F=0b10000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_28(cpu_object):
    """ SRA B - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    cpu_object.register.B = 0b10000001
    cycles = op.code_cb_28(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b11000000, F=0b00010000)

    cpu_object.register.B = 0b00000001
    cpu_object.register.F = 0b00000000
    cycles = op.code_cb_28(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b00000000, F=0b10010000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_29(cpu_object):
    """ SRA C - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    cpu_object.register.C = 0b10000001
    cycles = op.code_cb_29(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b11000000, F=0b00010000)

    cpu_object.register.C = 0b00000001
    cpu_object.register.F = 0b00000000
    cycles = op.code_cb_29(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b00000000, F=0b10010000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_2a(cpu_object):
    """ SRA D - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    cpu_object.register.D = 0b10000001
    cycles = op.code_cb_2a(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b11000000, F=0b00010000)

    cpu_object.register.D = 0b00000001
    cpu_object.register.F = 0b00000000
    cycles = op.code_cb_2a(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b00000000, F=0b10010000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_2b(cpu_object):
    """ SRA E - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    cpu_object.register.E = 0b10000001
    cycles = op.code_cb_2b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b11000000, F=0b00010000)

    cpu_object.register.E = 0b00000001
    cpu_object.register.F = 0b00000000
    cycles = op.code_cb_2b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b00000000, F=0b10010000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_2c(cpu_object):
    """ SRA H - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    cpu_object.register.H = 0b10000001
    cycles = op.code_cb_2c(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b11000000, F=0b00010000)

    cpu_object.register.H = 0b00000001
    cpu_object.register.F = 0b00000000
    cycles = op.code_cb_2c(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b00000000, F=0b10010000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_2d(cpu_object):
    """ SRA L - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    cpu_object.register.L = 0b10000001
    cycles = op.code_cb_2d(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b11000000, F=0b00010000)

    cpu_object.register.L = 0b00000001
    cpu_object.register.F = 0b00000000
    cycles = op.code_cb_2d(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b00000000, F=0b10010000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_2e(cpu_object):
    """ SRA (HL) - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b10000001)
    cycles = op.code_cb_2e(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b00010000)
    assert_memory(cpu_object, {0x1010: 0b11000000})

    cpu_object.memory.write_8bit(0x1010, 0b00000001)
    cpu_object.register.F = 0b00000000
    cycles = op.code_cb_2e(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b10010000)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_2f(cpu_object):
    """ SRA A - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    cpu_object.register.A = 0b10000001
    cycles = op.code_cb_2f(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b11000000, F=0b00010000)

    cpu_object.register.A = 0b00000001
    cpu_object.register.F = 0b00000000
    cycles = op.code_cb_2f(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b00000000, F=0b10010000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_30(cpu_object):
    """ SWAP B - Swap upper and lower nibbles (nibble = 4 bits) """
    cpu_object.register.B = 0xAB
    cycles = op.code_cb_30(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0xBA, F=0b00000000)

    cpu_object.register.B = 0x00
    cycles = op.code_cb_30(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0x00, F=0b10000000)

    cpu_object.register.B = 0xF0
    cycles = op.code_cb_30(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0x0F, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_31(cpu_object):
    """ SWAP C - Swap upper and lower nibbles (nibble = 4 bits) """
    cpu_object.register.C = 0xAB
    cycles = op.code_cb_31(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0xBA, F=0b00000000)

    cpu_object.register.C = 0x00
    cycles = op.code_cb_31(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0x00, F=0b10000000)

    cpu_object.register.C = 0xF0
    cycles = op.code_cb_31(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0x0F, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_32(cpu_object):
    """ SWAP D - Swap upper and lower nibbles (nibble = 4 bits) """
    cpu_object.register.D = 0xAB
    cycles = op.code_cb_32(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0xBA, F=0b00000000)

    cpu_object.register.D = 0x00
    cycles = op.code_cb_32(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0x00, F=0b10000000)

    cpu_object.register.D = 0xF0
    cycles = op.code_cb_32(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0x0F, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_33(cpu_object):
    """ SWAP E - Swap upper and lower nibbles (nibble = 4 bits) """
    cpu_object.register.E = 0xAB
    cycles = op.code_cb_33(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0xBA, F=0b00000000)

    cpu_object.register.E = 0x00
    cycles = op.code_cb_33(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0x00, F=0b10000000)

    cpu_object.register.E = 0xF0
    cycles = op.code_cb_33(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0x0F, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_34(cpu_object):
    """ SWAP H - Swap upper and lower nibbles (nibble = 4 bits) """
    cpu_object.register.H = 0xAB
    cycles = op.code_cb_34(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0xBA, F=0b00000000)

    cpu_object.register.H = 0x00
    cycles = op.code_cb_34(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0x00, F=0b10000000)

    cpu_object.register.H = 0xF0
    cycles = op.code_cb_34(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0x0F, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_35(cpu_object):
    """ SWAP L - Swap upper and lower nibbles (nibble = 4 bits) """
    cpu_object.register.L = 0xAB
    cycles = op.code_cb_35(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0xBA, F=0b00000000)

    cpu_object.register.L = 0x00
    cycles = op.code_cb_35(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0x00, F=0b10000000)

    cpu_object.register.L = 0xF0
    cycles = op.code_cb_35(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0x0F, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_36(cpu_object):
    """ SWAP (HL) - Swap upper and lower nibbles (nibble = 4 bits) """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0xAB)
    cycles = op.code_cb_36(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b00000000)
    assert_memory(cpu_object,{0x1010:0xBA})

    cpu_object.memory.write_8bit(0x1010, 0x00)
    cycles = op.code_cb_36(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b10000000)
    assert_memory(cpu_object)

    cpu_object.memory.write_8bit(0x1010, 0xF0)
    cycles = op.code_cb_36(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b00000000)
    assert_memory(cpu_object, {0x1010: 0x0F})


# noinspection PyShadowingNames
def test_code_cb_37(cpu_object):
    """ SWAP A - Swap upper and lower nibbles (nibble = 4 bits) """
    cpu_object.register.A = 0xAB
    cycles = op.code_cb_37(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0xBA, F=0b00000000)

    cpu_object.register.A = 0x00
    cycles = op.code_cb_37(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x00, F=0b10000000)

    cpu_object.register.A = 0xF0
    cycles = op.code_cb_37(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0x0F, F=0b00000000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_38(cpu_object):
    """ SRL B - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    cpu_object.register.B = 0b10000001
    cycles = op.code_cb_38(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b01000000, F=0b00010000)

    cpu_object.register.B = 0b00000001
    cpu_object.register.F = 0b00000000
    cycles = op.code_cb_38(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b00000000, F=0b10010000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_39(cpu_object):
    """ SRL C - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    cpu_object.register.C = 0b10000001
    cycles = op.code_cb_39(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b01000000, F=0b00010000)

    cpu_object.register.C = 0b00000001
    cpu_object.register.F = 0b00000000
    cycles = op.code_cb_39(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b00000000, F=0b10010000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_3a(cpu_object):
    """ SRL D - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    cpu_object.register.D = 0b10000001
    cycles = op.code_cb_3a(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b01000000, F=0b00010000)

    cpu_object.register.D = 0b00000001
    cpu_object.register.F = 0b00000000
    cycles = op.code_cb_3a(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b00000000, F=0b10010000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_3b(cpu_object):
    """ SRL E - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    cpu_object.register.E = 0b10000001
    cycles = op.code_cb_3b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b01000000, F=0b00010000)

    cpu_object.register.E = 0b00000001
    cpu_object.register.F = 0b00000000
    cycles = op.code_cb_3b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b00000000, F=0b10010000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_3c(cpu_object):
    """ SRL H - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    cpu_object.register.H = 0b10000001
    cycles = op.code_cb_3c(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b01000000, F=0b00010000)

    cpu_object.register.H = 0b00000001
    cpu_object.register.F = 0b00000000
    cycles = op.code_cb_3c(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b00000000, F=0b10010000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_3d(cpu_object):
    """ SRL L - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    cpu_object.register.L = 0b10000001
    cycles = op.code_cb_3d(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b01000000, F=0b00010000)

    cpu_object.register.L = 0b00000001
    cpu_object.register.F = 0b00000000
    cycles = op.code_cb_3d(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b00000000, F=0b10010000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_3e(cpu_object):
    """ SRL (HL) - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b10000001)
    cycles = op.code_cb_3e(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b00010000)
    assert_memory(cpu_object, {0x1010: 0b01000000})

    cpu_object.memory.write_8bit(0x1010, 0b00000001)
    cpu_object.register.F = 0b00000000
    cycles = op.code_cb_3e(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b10010000)
    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_3f(cpu_object):
    """ SRL A - Copy bit 7 to temp, copy bit 0 to Carry flag, shift right, replace new bit 7 with temp """
    cpu_object.register.A = 0b10000001
    cycles = op.code_cb_3f(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b01000000, F=0b00010000)

    cpu_object.register.A = 0b00000001
    cpu_object.register.F = 0b00000000
    cycles = op.code_cb_3f(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b00000000, F=0b10010000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_40(cpu_object):
    """ BIT 0,B - Test what is the value of bit 0 """
    cpu_object.register.B = 0b00000001
    cycles = op.code_cb_40(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b00000001, F=0b10100000)

    cpu_object.register.B = 0b11111110
    cycles = op.code_cb_40(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b11111110, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_41(cpu_object):
    """ BIT 0,C - Test what is the value of bit 0 """
    cpu_object.register.C = 0b00000001
    cycles = op.code_cb_41(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b00000001, F=0b10100000)

    cpu_object.register.C = 0b11111110
    cycles = op.code_cb_41(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b11111110, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_42(cpu_object):
    """ BIT 0,D - Test what is the value of bit 0 """
    cpu_object.register.D = 0b00000001
    cycles = op.code_cb_42(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b00000001, F=0b10100000)

    cpu_object.register.D = 0b11111110
    cycles = op.code_cb_42(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b11111110, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_43(cpu_object):
    """ BIT 0,E - Test what is the value of bit 0 """
    cpu_object.register.E = 0b00000001
    cycles = op.code_cb_43(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b00000001, F=0b10100000)

    cpu_object.register.E = 0b11111110
    cycles = op.code_cb_43(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b11111110, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_44(cpu_object):
    """ BIT 0,H - Test what is the value of bit 0 """
    cpu_object.register.H = 0b00000001
    cycles = op.code_cb_44(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b00000001, F=0b10100000)

    cpu_object.register.H = 0b11111110
    cycles = op.code_cb_44(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b11111110, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_45(cpu_object):
    """ BIT 0,L - Test what is the value of bit 0 """
    cpu_object.register.L = 0b00000001
    cycles = op.code_cb_45(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b00000001, F=0b10100000)

    cpu_object.register.L = 0b11111110
    cycles = op.code_cb_45(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b11111110, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_46(cpu_object):
    """ BIT 0,(HL) - Test what is the value of bit 0 """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b00000001)
    cycles = op.code_cb_46(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b10100000)
    assert_memory(cpu_object,{0x1010:0b00000001})

    cpu_object.memory.write_8bit(0x1010, 0b11111110)
    cycles = op.code_cb_46(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b00100000)
    assert_memory(cpu_object, {0x1010: 0b11111110})


# noinspection PyShadowingNames
def test_code_cb_47(cpu_object):
    """ BIT 0,A - Test what is the value of bit 0 """
    cpu_object.register.A = 0b00000001
    cycles = op.code_cb_47(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b00000001, F=0b10100000)

    cpu_object.register.A = 0b11111110
    cycles = op.code_cb_47(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b11111110, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_48(cpu_object):
    """ BIT 1,B - Test what is the value of bit 1 """
    cpu_object.register.B = 0b00000010
    cycles = op.code_cb_48(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b00000010, F=0b10100000)

    cpu_object.register.B = 0b11111101
    cycles = op.code_cb_48(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b11111101, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_49(cpu_object):
    """ BIT 1,C - Test what is the value of bit 1 """
    cpu_object.register.C = 0b00000010
    cycles = op.code_cb_49(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b00000010, F=0b10100000)

    cpu_object.register.C = 0b11111101
    cycles = op.code_cb_49(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b11111101, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_4a(cpu_object):
    """ BIT 1,D - Test what is the value of bit 1 """
    cpu_object.register.D = 0b00000010
    cycles = op.code_cb_4a(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b00000010, F=0b10100000)

    cpu_object.register.D = 0b11111101
    cycles = op.code_cb_4a(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b11111101, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_4b(cpu_object):
    """ BIT 1,E - Test what is the value of bit 1 """
    cpu_object.register.E = 0b00000010
    cycles = op.code_cb_4b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b00000010, F=0b10100000)

    cpu_object.register.E = 0b11111101
    cycles = op.code_cb_4b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b11111101, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_4c(cpu_object):
    """ BIT 1,H - Test what is the value of bit 1 """
    cpu_object.register.H = 0b00000010
    cycles = op.code_cb_4c(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b00000010, F=0b10100000)

    cpu_object.register.H = 0b11111101
    cycles = op.code_cb_4c(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b11111101, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_4d(cpu_object):
    """ BIT 1,L - Test what is the value of bit 1 """
    cpu_object.register.L = 0b00000010
    cycles = op.code_cb_4d(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b00000010, F=0b10100000)

    cpu_object.register.L = 0b11111101
    cycles = op.code_cb_4d(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b11111101, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_4e(cpu_object):
    """ BIT 1,(HL) - Test what is the value of bit 1 """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b00000010)
    cycles = op.code_cb_4e(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b10100000)
    assert_memory(cpu_object, {0x1010: 0b00000010})

    cpu_object.memory.write_8bit(0x1010, 0b11111101)
    cycles = op.code_cb_4e(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b00100000)
    assert_memory(cpu_object,{0x1010:0b11111101})


# noinspection PyShadowingNames
def test_code_cb_4f(cpu_object):
    """ BIT 1,A - Test what is the value of bit 1 """
    cpu_object.register.A = 0b00000010
    cycles = op.code_cb_4f(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b00000010, F=0b10100000)

    cpu_object.register.A = 0b11111101
    cycles = op.code_cb_4f(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b11111101, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_50(cpu_object):
    """ BIT 2,B - Test what is the value of bit 2 """
    cpu_object.register.B = 0b00000100
    cycles = op.code_cb_50(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b00000100, F=0b10100000)

    cpu_object.register.B = 0b11111011
    cycles = op.code_cb_50(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b11111011, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_51(cpu_object):
    """ BIT 2,C - Test what is the value of bit 2 """
    cpu_object.register.C = 0b00000100
    cycles = op.code_cb_51(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b00000100, F=0b10100000)

    cpu_object.register.C = 0b11111011
    cycles = op.code_cb_51(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b11111011, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_52(cpu_object):
    """ BIT 2,D - Test what is the value of bit 2 """
    cpu_object.register.D = 0b00000100
    cycles = op.code_cb_52(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b00000100, F=0b10100000)

    cpu_object.register.D = 0b11111011
    cycles = op.code_cb_52(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b11111011, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_53(cpu_object):
    """ BIT 2,E - Test what is the value of bit 2 """
    cpu_object.register.E = 0b00000100
    cycles = op.code_cb_53(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b00000100, F=0b10100000)

    cpu_object.register.E = 0b11111011
    cycles = op.code_cb_53(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b11111011, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_54(cpu_object):
    """ BIT 2,H - Test what is the value of bit 2 """
    cpu_object.register.H = 0b00000100
    cycles = op.code_cb_54(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b00000100, F=0b10100000)

    cpu_object.register.H = 0b11111011
    cycles = op.code_cb_54(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b11111011, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_55(cpu_object):
    """ BIT 2,L - Test what is the value of bit 2 """
    cpu_object.register.L = 0b00000100
    cycles = op.code_cb_55(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b00000100, F=0b10100000)

    cpu_object.register.L = 0b11111011
    cycles = op.code_cb_55(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b11111011, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_56(cpu_object):
    """ BIT 2,(HL) - Test what is the value of bit 2 """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b00000100)
    cycles = op.code_cb_56(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b10100000)
    assert_memory(cpu_object, {0x1010: 0b00000100})

    cpu_object.memory.write_8bit(0x1010, 0b11111011)
    cycles = op.code_cb_56(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b00100000)
    assert_memory(cpu_object,{0x1010:0b11111011})


# noinspection PyShadowingNames
def test_code_cb_57(cpu_object):
    """ BIT 2,A - Test what is the value of bit 2 """
    cpu_object.register.A = 0b00000100
    cycles = op.code_cb_57(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b00000100, F=0b10100000)

    cpu_object.register.A = 0b11111011
    cycles = op.code_cb_57(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b11111011, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_58(cpu_object):
    """ BIT 3,B - Test what is the value of bit 3 """
    cpu_object.register.B = 0b00001000
    cycles = op.code_cb_58(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b00001000, F=0b10100000)

    cpu_object.register.B = 0b11110111
    cycles = op.code_cb_58(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b11110111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_59(cpu_object):
    """ BIT 3,C - Test what is the value of bit 3 """
    cpu_object.register.C = 0b00001000
    cycles = op.code_cb_59(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b00001000, F=0b10100000)

    cpu_object.register.C = 0b11110111
    cycles = op.code_cb_59(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b11110111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_5a(cpu_object):
    """ BIT 3,D - Test what is the value of bit 3 """
    cpu_object.register.D = 0b00001000
    cycles = op.code_cb_5a(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b00001000, F=0b10100000)

    cpu_object.register.D = 0b11110111
    cycles = op.code_cb_5a(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b11110111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_5b(cpu_object):
    """ BIT 3,E - Test what is the value of bit 3 """
    cpu_object.register.E = 0b00001000
    cycles = op.code_cb_5b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b00001000, F=0b10100000)

    cpu_object.register.E = 0b11110111
    cycles = op.code_cb_5b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b11110111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_5c(cpu_object):
    """ BIT 3,H - Test what is the value of bit 3 """
    cpu_object.register.H = 0b00001000
    cycles = op.code_cb_5c(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b00001000, F=0b10100000)

    cpu_object.register.H = 0b11110111
    cycles = op.code_cb_5c(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b11110111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_5d(cpu_object):
    """ BIT 3,L - Test what is the value of bit 3 """
    cpu_object.register.L = 0b00001000
    cycles = op.code_cb_5d(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b00001000, F=0b10100000)

    cpu_object.register.L = 0b11110111
    cycles = op.code_cb_5d(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b11110111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_5e(cpu_object):
    """ BIT 3,(HL) - Test what is the value of bit 3 """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b00001000)
    cycles = op.code_cb_5e(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b10100000)
    assert_memory(cpu_object, {0x1010: 0b00001000})

    cpu_object.memory.write_8bit(0x1010, 0b11110111)
    cycles = op.code_cb_5e(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b00100000)
    assert_memory(cpu_object,{0x1010:0b11110111})


# noinspection PyShadowingNames
def test_code_cb_5f(cpu_object):
    """ BIT 3,A - Test what is the value of bit 3 """
    cpu_object.register.A = 0b00001000
    cycles = op.code_cb_5f(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b00001000, F=0b10100000)

    cpu_object.register.A = 0b11110111
    cycles = op.code_cb_5f(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b11110111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_60(cpu_object):
    """ BIT 4,B - Test what is the value of bit 4 """
    cpu_object.register.B = 0b00010000
    cycles = op.code_cb_60(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b00010000, F=0b10100000)

    cpu_object.register.B = 0b11101111
    cycles = op.code_cb_60(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b11101111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_61(cpu_object):
    """ BIT 4,C - Test what is the value of bit 4 """
    cpu_object.register.C = 0b00010000
    cycles = op.code_cb_61(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b00010000, F=0b10100000)

    cpu_object.register.C = 0b11101111
    cycles = op.code_cb_61(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b11101111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_62(cpu_object):
    """ BIT 4,D - Test what is the value of bit 4 """
    cpu_object.register.D = 0b00010000
    cycles = op.code_cb_62(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b00010000, F=0b10100000)

    cpu_object.register.D = 0b11101111
    cycles = op.code_cb_62(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b11101111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_63(cpu_object):
    """ BIT 4,E - Test what is the value of bit 4 """
    cpu_object.register.E = 0b00010000
    cycles = op.code_cb_63(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b00010000, F=0b10100000)

    cpu_object.register.E = 0b11101111
    cycles = op.code_cb_63(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b11101111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_64(cpu_object):
    """ BIT 4,H - Test what is the value of bit 4 """
    cpu_object.register.H = 0b00010000
    cycles = op.code_cb_64(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b00010000, F=0b10100000)

    cpu_object.register.H = 0b11101111
    cycles = op.code_cb_64(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b11101111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_65(cpu_object):
    """ BIT 4,L - Test what is the value of bit 4 """
    cpu_object.register.L = 0b00010000
    cycles = op.code_cb_65(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b00010000, F=0b10100000)

    cpu_object.register.L = 0b11101111
    cycles = op.code_cb_65(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b11101111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_66(cpu_object):
    """ BIT 4,(HL) - Test what is the value of bit 4 """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b00010000)
    cycles = op.code_cb_66(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b10100000)
    assert_memory(cpu_object, {0x1010: 0b00010000})

    cpu_object.memory.write_8bit(0x1010, 0b11101111)
    cycles = op.code_cb_66(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b00100000)
    assert_memory(cpu_object,{0x1010:0b11101111})


# noinspection PyShadowingNames
def test_code_cb_67(cpu_object):
    """ BIT 4,A - Test what is the value of bit 4 """
    cpu_object.register.A = 0b00010000
    cycles = op.code_cb_67(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b00010000, F=0b10100000)

    cpu_object.register.A = 0b11101111
    cycles = op.code_cb_67(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b11101111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_68(cpu_object):
    """ BIT 5,B - Test what is the value of bit 5 """
    cpu_object.register.B = 0b00100000
    cycles = op.code_cb_68(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b00100000, F=0b10100000)

    cpu_object.register.B = 0b11011111
    cycles = op.code_cb_68(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b11011111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_69(cpu_object):
    """ BIT 5,C - Test what is the value of bit 5 """
    cpu_object.register.C = 0b00100000
    cycles = op.code_cb_69(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b00100000, F=0b10100000)

    cpu_object.register.C = 0b11011111
    cycles = op.code_cb_69(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b11011111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_6a(cpu_object):
    """ BIT 5,D - Test what is the value of bit 5 """
    cpu_object.register.D = 0b00100000
    cycles = op.code_cb_6a(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b00100000, F=0b10100000)

    cpu_object.register.D = 0b11011111
    cycles = op.code_cb_6a(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b11011111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_6b(cpu_object):
    """ BIT 5,E - Test what is the value of bit 5 """
    cpu_object.register.E = 0b00100000
    cycles = op.code_cb_6b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b00100000, F=0b10100000)

    cpu_object.register.E = 0b11011111
    cycles = op.code_cb_6b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b11011111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_6c(cpu_object):
    """ BIT 5,H - Test what is the value of bit 5 """
    cpu_object.register.H = 0b00100000
    cycles = op.code_cb_6c(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b00100000, F=0b10100000)

    cpu_object.register.H = 0b11011111
    cycles = op.code_cb_6c(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b11011111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_6d(cpu_object):
    """ BIT 5,L - Test what is the value of bit 5 """
    cpu_object.register.L = 0b00100000
    cycles = op.code_cb_6d(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b00100000, F=0b10100000)

    cpu_object.register.L = 0b11011111
    cycles = op.code_cb_6d(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b11011111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_6e(cpu_object):
    """ BIT 5,(HL) - Test what is the value of bit 5 """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b00100000)
    cycles = op.code_cb_6e(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b10100000)
    assert_memory(cpu_object, {0x1010: 0b00100000})

    cpu_object.memory.write_8bit(0x1010, 0b11011111)
    cycles = op.code_cb_6e(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b00100000)
    assert_memory(cpu_object,{0x1010:0b11011111})


# noinspection PyShadowingNames
def test_code_cb_6f(cpu_object):
    """ BIT 5,A - Test what is the value of bit 5 """
    cpu_object.register.A = 0b00100000
    cycles = op.code_cb_6f(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b00100000, F=0b10100000)

    cpu_object.register.A = 0b11011111
    cycles = op.code_cb_6f(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b11011111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_70(cpu_object):
    """ BIT 6,B - Test what is the value of bit 6 """
    cpu_object.register.B = 0b01000000
    cycles = op.code_cb_70(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b01000000, F=0b10100000)

    cpu_object.register.B = 0b10111111
    cycles = op.code_cb_70(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b10111111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_71(cpu_object):
    """ BIT 6,C - Test what is the value of bit 6 """
    cpu_object.register.C = 0b01000000
    cycles = op.code_cb_71(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b01000000, F=0b10100000)

    cpu_object.register.C = 0b10111111
    cycles = op.code_cb_71(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b10111111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_72(cpu_object):
    """ BIT 6,D - Test what is the value of bit 6 """
    cpu_object.register.D = 0b01000000
    cycles = op.code_cb_72(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b01000000, F=0b10100000)

    cpu_object.register.D = 0b10111111
    cycles = op.code_cb_72(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b10111111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_73(cpu_object):
    """ BIT 6,E - Test what is the value of bit 6 """
    cpu_object.register.E = 0b01000000
    cycles = op.code_cb_73(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b01000000, F=0b10100000)

    cpu_object.register.E = 0b10111111
    cycles = op.code_cb_73(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b10111111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_74(cpu_object):
    """ BIT 6,H - Test what is the value of bit 6 """
    cpu_object.register.H = 0b01000000
    cycles = op.code_cb_74(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b01000000, F=0b10100000)

    cpu_object.register.H = 0b10111111
    cycles = op.code_cb_74(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b10111111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_75(cpu_object):
    """ BIT 6,L - Test what is the value of bit 6 """
    cpu_object.register.L = 0b01000000
    cycles = op.code_cb_75(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b01000000, F=0b10100000)

    cpu_object.register.L = 0b10111111
    cycles = op.code_cb_75(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b10111111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_76(cpu_object):
    """ BIT 6,(HL) - Test what is the value of bit 6 """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b01000000)
    cycles = op.code_cb_76(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b10100000)
    assert_memory(cpu_object, {0x1010: 0b01000000})

    cpu_object.memory.write_8bit(0x1010, 0b10111111)
    cycles = op.code_cb_76(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b00100000)
    assert_memory(cpu_object,{0x1010:0b10111111})


# noinspection PyShadowingNames
def test_code_cb_77(cpu_object):
    """ BIT 6,A - Test what is the value of bit 6 """
    cpu_object.register.A = 0b01000000
    cycles = op.code_cb_77(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b01000000, F=0b10100000)

    cpu_object.register.A = 0b10111111
    cycles = op.code_cb_77(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b10111111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_78(cpu_object):
    """ BIT 7,B - Test what is the value of bit 7 """
    cpu_object.register.B = 0b10000000
    cycles = op.code_cb_78(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b10000000, F=0b10100000)

    cpu_object.register.B = 0b01111111
    cycles = op.code_cb_78(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, B=0b01111111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_79(cpu_object):
    """ BIT 7,C - Test what is the value of bit 7 """
    cpu_object.register.C = 0b10000000
    cycles = op.code_cb_79(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b10000000, F=0b10100000)

    cpu_object.register.C = 0b01111111
    cycles = op.code_cb_79(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, C=0b01111111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_7a(cpu_object):
    """ BIT 7,D - Test what is the value of bit 7 """
    cpu_object.register.D = 0b10000000
    cycles = op.code_cb_7a(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b10000000, F=0b10100000)

    cpu_object.register.D = 0b01111111
    cycles = op.code_cb_7a(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, D=0b01111111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_7b(cpu_object):
    """ BIT 7,E - Test what is the value of bit 7 """
    cpu_object.register.E = 0b10000000
    cycles = op.code_cb_7b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b10000000, F=0b10100000)

    cpu_object.register.E = 0b01111111
    cycles = op.code_cb_7b(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, E=0b01111111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_7c(cpu_object):
    """ BIT 7,H - Test what is the value of bit 7 """
    cpu_object.register.H = 0b10000000
    cycles = op.code_cb_7c(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b10000000, F=0b10100000)

    cpu_object.register.H = 0b01111111
    cycles = op.code_cb_7c(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, H=0b01111111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_7d(cpu_object):
    """ BIT 7,L - Test what is the value of bit 7 """
    cpu_object.register.L = 0b10000000
    cycles = op.code_cb_7d(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b10000000, F=0b10100000)

    cpu_object.register.L = 0b01111111
    cycles = op.code_cb_7d(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, L=0b01111111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_7e(cpu_object):
    """ BIT 7,(HL) - Test what is the value of bit 7 """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b10000000)
    cycles = op.code_cb_7e(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b10100000)
    assert_memory(cpu_object, {0x1010: 0b10000000})

    cpu_object.memory.write_8bit(0x1010, 0b01111111)
    cycles = op.code_cb_7e(cpu_object)
    assert cycles == 16
    assert_registers(cpu_object, H=0x10, L=0x10, F=0b00100000)
    assert_memory(cpu_object,{0x1010:0b01111111})


# noinspection PyShadowingNames
def test_code_cb_7f(cpu_object):
    """ BIT 7,A - Test what is the value of bit 7 """
    cpu_object.register.A = 0b10000000
    cycles = op.code_cb_7f(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b10000000, F=0b10100000)

    cpu_object.register.A = 0b01111111
    cycles = op.code_cb_7f(cpu_object)
    assert cycles == 8
    assert_registers(cpu_object, A=0b01111111, F=0b00100000)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_80(cpu_object):
    """ RES 0,B - Reset the specified bit """
    cpu_object.register.B = 0b00000000
    cycle = op.code_cb_80(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b00000000)

    cpu_object.register.B = 0b11111111
    cycle = op.code_cb_80(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b11111110)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_81(cpu_object):
    """ RES 0,C - Reset the specified bit """
    cpu_object.register.C = 0b00000000
    cycle = op.code_cb_81(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b00000000)

    cpu_object.register.C = 0b11111111
    cycle = op.code_cb_81(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b11111110)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_82(cpu_object):
    """ RES 0,D - Reset the specified bit """
    cpu_object.register.D = 0b00000000
    cycle = op.code_cb_82(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b00000000)

    cpu_object.register.D = 0b11111111
    cycle = op.code_cb_82(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b11111110)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_83(cpu_object):
    """ RES 0,E - Reset the specified bit """
    cpu_object.register.E = 0b00000000
    cycle = op.code_cb_83(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b00000000)

    cpu_object.register.E = 0b11111111
    cycle = op.code_cb_83(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b11111110)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_84(cpu_object):
    """ RES 0,H - Reset the specified bit """
    cpu_object.register.H = 0b00000000
    cycle = op.code_cb_84(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b00000000)

    cpu_object.register.H = 0b11111111
    cycle = op.code_cb_84(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b11111110)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_85(cpu_object):
    """ RES 0,L - Reset the specified bit """
    cpu_object.register.L = 0b00000000
    cycle = op.code_cb_85(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b00000000)

    cpu_object.register.L = 0b11111111
    cycle = op.code_cb_85(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b11111110)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_86(cpu_object):
    """ RES 0,(HL) - Reset the specified bit """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_86(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object)

    cpu_object.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_86(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object,{0x1010:0b11111110})


# noinspection PyShadowingNames
def test_code_cb_87(cpu_object):
    """ RES 0,A - Reset the specified bit """
    cpu_object.register.A = 0b00000000
    cycle = op.code_cb_87(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b00000000)

    cpu_object.register.A = 0b11111111
    cycle = op.code_cb_87(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b11111110)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_88(cpu_object):
    """ RES 1,B - Reset the specified bit """
    cpu_object.register.B = 0b00000000
    cycle = op.code_cb_88(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b00000000)

    cpu_object.register.B = 0b11111111
    cycle = op.code_cb_88(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b11111101)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_89(cpu_object):
    """ RES 1,C - Reset the specified bit """
    cpu_object.register.C = 0b00000000
    cycle = op.code_cb_89(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b00000000)

    cpu_object.register.C = 0b11111111
    cycle = op.code_cb_89(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b11111101)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_8a(cpu_object):
    """ RES 1,D - Reset the specified bit """
    cpu_object.register.D = 0b00000000
    cycle = op.code_cb_8a(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b00000000)

    cpu_object.register.D = 0b11111111
    cycle = op.code_cb_8a(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b11111101)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_8b(cpu_object):
    """ RES 1,E - Reset the specified bit """
    cpu_object.register.E = 0b00000000
    cycle = op.code_cb_8b(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b00000000)

    cpu_object.register.E = 0b11111111
    cycle = op.code_cb_8b(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b11111101)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_8c(cpu_object):
    """ RES 1,H - Reset the specified bit """
    cpu_object.register.H = 0b00000000
    cycle = op.code_cb_8c(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b00000000)

    cpu_object.register.H = 0b11111111
    cycle = op.code_cb_8c(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b11111101)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_8d(cpu_object):
    """ RES 1,L - Reset the specified bit """
    cpu_object.register.L = 0b00000000
    cycle = op.code_cb_8d(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b00000000)

    cpu_object.register.L = 0b11111111
    cycle = op.code_cb_8d(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b11111101)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_8e(cpu_object):
    """ RES 1,(HL) - Reset the specified bit """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_8e(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object)

    cpu_object.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_8e(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object,{0x1010:0b11111101})


# noinspection PyShadowingNames
def test_code_cb_8f(cpu_object):
    """ RES 1,A - Reset the specified bit """
    cpu_object.register.A = 0b00000000
    cycle = op.code_cb_8f(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b00000000)

    cpu_object.register.A = 0b11111111
    cycle = op.code_cb_8f(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b11111101)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_90(cpu_object):
    """ RES 2,B - Reset the specified bit """
    cpu_object.register.B = 0b00000000
    cycle = op.code_cb_90(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b00000000)

    cpu_object.register.B = 0b11111111
    cycle = op.code_cb_90(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b11111011)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_91(cpu_object):
    """ RES 2,C - Reset the specified bit """
    cpu_object.register.C = 0b00000000
    cycle = op.code_cb_91(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b00000000)

    cpu_object.register.C = 0b11111111
    cycle = op.code_cb_91(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b11111011)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_92(cpu_object):
    """ RES 2,D - Reset the specified bit """
    cpu_object.register.D = 0b00000000
    cycle = op.code_cb_92(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b00000000)

    cpu_object.register.D = 0b11111111
    cycle = op.code_cb_92(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b11111011)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_93(cpu_object):
    """ RES 2,E - Reset the specified bit """
    cpu_object.register.E = 0b00000000
    cycle = op.code_cb_93(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b00000000)

    cpu_object.register.E = 0b11111111
    cycle = op.code_cb_93(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b11111011)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_94(cpu_object):
    """ RES 2,H - Reset the specified bit """
    cpu_object.register.H = 0b00000000
    cycle = op.code_cb_94(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b00000000)

    cpu_object.register.H = 0b11111111
    cycle = op.code_cb_94(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b11111011)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_95(cpu_object):
    """ RES 2,L - Reset the specified bit """
    cpu_object.register.L = 0b00000000
    cycle = op.code_cb_95(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b00000000)

    cpu_object.register.L = 0b11111111
    cycle = op.code_cb_95(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b11111011)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_96(cpu_object):
    """ RES 2,(HL) - Reset the specified bit """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_96(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object)

    cpu_object.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_96(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object,{0x1010:0b11111011})


# noinspection PyShadowingNames
def test_code_cb_97(cpu_object):
    """ RES 2,A - Reset the specified bit """
    cpu_object.register.A = 0b00000000
    cycle = op.code_cb_97(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b00000000)

    cpu_object.register.A = 0b11111111
    cycle = op.code_cb_97(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b11111011)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_98(cpu_object):
    """ RES 3,B - Reset the specified bit """
    cpu_object.register.B = 0b00000000
    cycle = op.code_cb_98(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b00000000)

    cpu_object.register.B = 0b11111111
    cycle = op.code_cb_98(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b11110111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_99(cpu_object):
    """ RES 3,C - Reset the specified bit """
    cpu_object.register.C = 0b00000000
    cycle = op.code_cb_99(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b00000000)

    cpu_object.register.C = 0b11111111
    cycle = op.code_cb_99(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b11110111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_9a(cpu_object):
    """ RES 3,D - Reset the specified bit """
    cpu_object.register.D = 0b00000000
    cycle = op.code_cb_9a(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b00000000)

    cpu_object.register.D = 0b11111111
    cycle = op.code_cb_9a(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b11110111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_9b(cpu_object):
    """ RES 3,E - Reset the specified bit """
    cpu_object.register.E = 0b00000000
    cycle = op.code_cb_9b(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b00000000)

    cpu_object.register.E = 0b11111111
    cycle = op.code_cb_9b(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b11110111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_9c(cpu_object):
    """ RES 3,H - Reset the specified bit """
    cpu_object.register.H = 0b00000000
    cycle = op.code_cb_9c(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b00000000)

    cpu_object.register.H = 0b11111111
    cycle = op.code_cb_9c(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b11110111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_9d(cpu_object):
    """ RES 3,L - Reset the specified bit """
    cpu_object.register.L = 0b00000000
    cycle = op.code_cb_9d(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b00000000)

    cpu_object.register.L = 0b11111111
    cycle = op.code_cb_9d(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b11110111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_9e(cpu_object):
    """ RES 3,(HL) - Reset the specified bit """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_9e(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object)

    cpu_object.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_9e(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object,{0x1010:0b11110111})


# noinspection PyShadowingNames
def test_code_cb_9f(cpu_object):
    """ RES 3,A - Reset the specified bit """
    cpu_object.register.A = 0b00000000
    cycle = op.code_cb_9f(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b00000000)

    cpu_object.register.A = 0b11111111
    cycle = op.code_cb_9f(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b11110111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_a0(cpu_object):
    """ RES 4,B - Reset the specified bit """
    cpu_object.register.B = 0b00000000
    cycle = op.code_cb_a0(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b00000000)

    cpu_object.register.B = 0b11111111
    cycle = op.code_cb_a0(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b11101111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_a1(cpu_object):
    """ RES 4,C - Reset the specified bit """
    cpu_object.register.C = 0b00000000
    cycle = op.code_cb_a1(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b00000000)

    cpu_object.register.C = 0b11111111
    cycle = op.code_cb_a1(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b11101111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_a2(cpu_object):
    """ RES 4,D - Reset the specified bit """
    cpu_object.register.D = 0b00000000
    cycle = op.code_cb_a2(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b00000000)

    cpu_object.register.D = 0b11111111
    cycle = op.code_cb_a2(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b11101111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_a3(cpu_object):
    """ RES 4,E - Reset the specified bit """
    cpu_object.register.E = 0b00000000
    cycle = op.code_cb_a3(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b00000000)

    cpu_object.register.E = 0b11111111
    cycle = op.code_cb_a3(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b11101111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_a4(cpu_object):
    """ RES 4,H - Reset the specified bit """
    cpu_object.register.H = 0b00000000
    cycle = op.code_cb_a4(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b00000000)

    cpu_object.register.H = 0b11111111
    cycle = op.code_cb_a4(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b11101111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_a5(cpu_object):
    """ RES 4,L - Reset the specified bit """
    cpu_object.register.L = 0b00000000
    cycle = op.code_cb_a5(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b00000000)

    cpu_object.register.L = 0b11111111
    cycle = op.code_cb_a5(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b11101111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_a6(cpu_object):
    """ RES 4,(HL) - Reset the specified bit """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_a6(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object)

    cpu_object.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_a6(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object,{0x1010:0b11101111})


# noinspection PyShadowingNames
def test_code_cb_a7(cpu_object):
    """ RES 4,A - Reset the specified bit """
    cpu_object.register.A = 0b00000000
    cycle = op.code_cb_a7(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b00000000)

    cpu_object.register.A = 0b11111111
    cycle = op.code_cb_a7(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b11101111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_a8(cpu_object):
    """ RES 5,B - Reset the specified bit """
    cpu_object.register.B = 0b00000000
    cycle = op.code_cb_a8(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b00000000)

    cpu_object.register.B = 0b11111111
    cycle = op.code_cb_a8(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b11011111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_a9(cpu_object):
    """ RES 5,C - Reset the specified bit """
    cpu_object.register.C = 0b00000000
    cycle = op.code_cb_a9(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b00000000)

    cpu_object.register.C = 0b11111111
    cycle = op.code_cb_a9(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b11011111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_aa(cpu_object):
    """ RES 5,D - Reset the specified bit """
    cpu_object.register.D = 0b00000000
    cycle = op.code_cb_aa(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b00000000)

    cpu_object.register.D = 0b11111111
    cycle = op.code_cb_aa(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b11011111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_ab(cpu_object):
    """ RES 5,E - Reset the specified bit """
    cpu_object.register.E = 0b00000000
    cycle = op.code_cb_ab(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b00000000)

    cpu_object.register.E = 0b11111111
    cycle = op.code_cb_ab(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b11011111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_ac(cpu_object):
    """ RES 5,H - Reset the specified bit """
    cpu_object.register.H = 0b00000000
    cycle = op.code_cb_ac(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b00000000)

    cpu_object.register.H = 0b11111111
    cycle = op.code_cb_ac(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b11011111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_ad(cpu_object):
    """ RES 5,L - Reset the specified bit """
    cpu_object.register.L = 0b00000000
    cycle = op.code_cb_ad(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b00000000)

    cpu_object.register.L = 0b11111111
    cycle = op.code_cb_ad(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b11011111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_ae(cpu_object):
    """ RES 5,(HL) - Reset the specified bit """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_ae(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object)

    cpu_object.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_ae(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object,{0x1010:0b11011111})


# noinspection PyShadowingNames
def test_code_cb_af(cpu_object):
    """ RES 5,A - Reset the specified bit """
    cpu_object.register.A = 0b00000000
    cycle = op.code_cb_af(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b00000000)

    cpu_object.register.A = 0b11111111
    cycle = op.code_cb_af(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b11011111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_b0(cpu_object):
    """ RES 6,B - Reset the specified bit """
    cpu_object.register.B = 0b00000000
    cycle = op.code_cb_b0(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b00000000)

    cpu_object.register.B = 0b11111111
    cycle = op.code_cb_b0(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b10111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_b1(cpu_object):
    """ RES 6,C - Reset the specified bit """
    cpu_object.register.C = 0b00000000
    cycle = op.code_cb_b1(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b00000000)

    cpu_object.register.C = 0b11111111
    cycle = op.code_cb_b1(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b10111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_b2(cpu_object):
    """ RES 6,D - Reset the specified bit """
    cpu_object.register.D = 0b00000000
    cycle = op.code_cb_b2(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b00000000)

    cpu_object.register.D = 0b11111111
    cycle = op.code_cb_b2(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b10111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_b3(cpu_object):
    """ RES 6,E - Reset the specified bit """
    cpu_object.register.E = 0b00000000
    cycle = op.code_cb_b3(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b00000000)

    cpu_object.register.E = 0b11111111
    cycle = op.code_cb_b3(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b10111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_b4(cpu_object):
    """ RES 6,H - Reset the specified bit """
    cpu_object.register.H = 0b00000000
    cycle = op.code_cb_b4(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b00000000)

    cpu_object.register.H = 0b11111111
    cycle = op.code_cb_b4(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b10111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_b5(cpu_object):
    """ RES 6,L - Reset the specified bit """
    cpu_object.register.L = 0b00000000
    cycle = op.code_cb_b5(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b00000000)

    cpu_object.register.L = 0b11111111
    cycle = op.code_cb_b5(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b10111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_b6(cpu_object):
    """ RES 6,(HL) - Reset the specified bit """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_b6(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object)

    cpu_object.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_b6(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object,{0x1010:0b10111111})


# noinspection PyShadowingNames
def test_code_cb_b7(cpu_object):
    """ RES 6,A - Reset the specified bit """
    cpu_object.register.A = 0b00000000
    cycle = op.code_cb_b7(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b00000000)

    cpu_object.register.A = 0b11111111
    cycle = op.code_cb_b7(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b10111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_b8(cpu_object):
    """ RES 7,B - Reset the specified bit """
    cpu_object.register.B = 0b00000000
    cycle = op.code_cb_b8(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b00000000)

    cpu_object.register.B = 0b11111111
    cycle = op.code_cb_b8(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b01111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_b9(cpu_object):
    """ RES 7,C - Reset the specified bit """
    cpu_object.register.C = 0b00000000
    cycle = op.code_cb_b9(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b00000000)

    cpu_object.register.C = 0b11111111
    cycle = op.code_cb_b9(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b01111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_ba(cpu_object):
    """ RES 7,D - Reset the specified bit """
    cpu_object.register.D = 0b00000000
    cycle = op.code_cb_ba(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b00000000)

    cpu_object.register.D = 0b11111111
    cycle = op.code_cb_ba(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b01111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_bb(cpu_object):
    """ RES 7,E - Reset the specified bit """
    cpu_object.register.E = 0b00000000
    cycle = op.code_cb_bb(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b00000000)

    cpu_object.register.E = 0b11111111
    cycle = op.code_cb_bb(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b01111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_bc(cpu_object):
    """ RES 7,H - Reset the specified bit """
    cpu_object.register.H = 0b00000000
    cycle = op.code_cb_bc(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b00000000)

    cpu_object.register.H = 0b11111111
    cycle = op.code_cb_bc(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b01111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_bd(cpu_object):
    """ RES 7,L - Reset the specified bit """
    cpu_object.register.L = 0b00000000
    cycle = op.code_cb_bd(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b00000000)

    cpu_object.register.L = 0b11111111
    cycle = op.code_cb_bd(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b01111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_be(cpu_object):
    """ RES 7,(HL) - Reset the specified bit """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_be(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object)

    cpu_object.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_be(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object,{0x1010:0b01111111})


# noinspection PyShadowingNames
def test_code_cb_bf(cpu_object):
    """ RES 7,A - Reset the specified bit """
    cpu_object.register.A = 0b00000000
    cycle = op.code_cb_bf(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b00000000)

    cpu_object.register.A = 0b11111111
    cycle = op.code_cb_bf(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b01111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_c0(cpu_object):
    """ SET 0,B - Set the specified bit """
    cpu_object.register.B = 0b00000000
    cycle = op.code_cb_c0(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b00000001)

    cpu_object.register.B = 0b11111111
    cycle = op.code_cb_c0(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_c1(cpu_object):
    """ SET 0,C - Set the specified bit """
    cpu_object.register.C = 0b00000000
    cycle = op.code_cb_c1(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b00000001)

    cpu_object.register.C = 0b11111111
    cycle = op.code_cb_c1(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_c2(cpu_object):
    """ SET 0,D - Set the specified bit """
    cpu_object.register.D = 0b00000000
    cycle = op.code_cb_c2(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b00000001)

    cpu_object.register.D = 0b11111111
    cycle = op.code_cb_c2(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_c3(cpu_object):
    """ SET 0,E - Set the specified bit """
    cpu_object.register.E = 0b00000000
    cycle = op.code_cb_c3(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b00000001)

    cpu_object.register.E = 0b11111111
    cycle = op.code_cb_c3(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_c4(cpu_object):
    """ SET 0,H - Set the specified bit """
    cpu_object.register.H = 0b00000000
    cycle = op.code_cb_c4(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b00000001)

    cpu_object.register.H = 0b11111111
    cycle = op.code_cb_c4(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_c5(cpu_object):
    """ SET 0,L - Set the specified bit """
    cpu_object.register.L = 0b00000000
    cycle = op.code_cb_c5(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b00000001)

    cpu_object.register.L = 0b11111111
    cycle = op.code_cb_c5(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_c6(cpu_object):
    """ SET 0,(HL) - Set the specified bit """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_c6(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object, {0x1010: 0b00000001})

    cpu_object.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_c6(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object,{0x1010:0b11111111})


# noinspection PyShadowingNames
def test_code_cb_c7(cpu_object):
    """ SET 0,A - Set the specified bit """
    cpu_object.register.A = 0b00000000
    cycle = op.code_cb_c7(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b00000001)

    cpu_object.register.A = 0b11111111
    cycle = op.code_cb_c7(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_c8(cpu_object):
    """ SET 1,B - Set the specified bit """
    cpu_object.register.B = 0b00000000
    cycle = op.code_cb_c8(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b00000010)

    cpu_object.register.B = 0b11111111
    cycle = op.code_cb_c8(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_c9(cpu_object):
    """ SET 1,C - Set the specified bit """
    cpu_object.register.C = 0b00000000
    cycle = op.code_cb_c9(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b00000010)

    cpu_object.register.C = 0b11111111
    cycle = op.code_cb_c9(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_ca(cpu_object):
    """ SET 1,D - Set the specified bit """
    cpu_object.register.D = 0b00000000
    cycle = op.code_cb_ca(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b00000010)

    cpu_object.register.D = 0b11111111
    cycle = op.code_cb_ca(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_cb(cpu_object):
    """ SET 1,E - Set the specified bit """
    cpu_object.register.E = 0b00000000
    cycle = op.code_cb_cb(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b00000010)

    cpu_object.register.E = 0b11111111
    cycle = op.code_cb_cb(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_cc(cpu_object):
    """ SET 1,H - Set the specified bit """
    cpu_object.register.H = 0b00000000
    cycle = op.code_cb_cc(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b00000010)

    cpu_object.register.H = 0b11111111
    cycle = op.code_cb_cc(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_cd(cpu_object):
    """ SET 1,L - Set the specified bit """
    cpu_object.register.L = 0b00000000
    cycle = op.code_cb_cd(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b00000010)

    cpu_object.register.L = 0b11111111
    cycle = op.code_cb_cd(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_ce(cpu_object):
    """ SET 1,(HL) - Set the specified bit """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_ce(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object, {0x1010: 0b00000010})

    cpu_object.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_ce(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object,{0x1010:0b11111111})


# noinspection PyShadowingNames
def test_code_cb_cf(cpu_object):
    """ SET 1,A - Set the specified bit """
    cpu_object.register.A = 0b00000000
    cycle = op.code_cb_cf(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b00000010)

    cpu_object.register.A = 0b11111111
    cycle = op.code_cb_cf(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_d0(cpu_object):
    """ SET 2,B - Set the specified bit """
    cpu_object.register.B = 0b00000000
    cycle = op.code_cb_d0(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b00000100)

    cpu_object.register.B = 0b11111111
    cycle = op.code_cb_d0(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_d1(cpu_object):
    """ SET 2,C - Set the specified bit """
    cpu_object.register.C = 0b00000000
    cycle = op.code_cb_d1(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b00000100)

    cpu_object.register.C = 0b11111111
    cycle = op.code_cb_d1(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_d2(cpu_object):
    """ SET 2,D - Set the specified bit """
    cpu_object.register.D = 0b00000000
    cycle = op.code_cb_d2(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b00000100)

    cpu_object.register.D = 0b11111111
    cycle = op.code_cb_d2(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_d3(cpu_object):
    """ SET 2,E - Set the specified bit """
    cpu_object.register.E = 0b00000000
    cycle = op.code_cb_d3(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b00000100)

    cpu_object.register.E = 0b11111111
    cycle = op.code_cb_d3(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_d4(cpu_object):
    """ SET 2,H - Set the specified bit """
    cpu_object.register.H = 0b00000000
    cycle = op.code_cb_d4(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b00000100)

    cpu_object.register.H = 0b11111111
    cycle = op.code_cb_d4(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_d5(cpu_object):
    """ SET 2,L - Set the specified bit """
    cpu_object.register.L = 0b00000000
    cycle = op.code_cb_d5(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b00000100)

    cpu_object.register.L = 0b11111111
    cycle = op.code_cb_d5(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_d6(cpu_object):
    """ SET 2,(HL) - Set the specified bit """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_d6(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object, {0x1010: 0b00000100})

    cpu_object.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_d6(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object,{0x1010:0b11111111})


# noinspection PyShadowingNames
def test_code_cb_d7(cpu_object):
    """ SET 2,A - Set the specified bit """
    cpu_object.register.A = 0b00000000
    cycle = op.code_cb_d7(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b00000100)

    cpu_object.register.A = 0b11111111
    cycle = op.code_cb_d7(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_d8(cpu_object):
    """ SET 3,B - Set the specified bit """
    cpu_object.register.B = 0b00000000
    cycle = op.code_cb_d8(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b00001000)

    cpu_object.register.B = 0b11111111
    cycle = op.code_cb_d8(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_d9(cpu_object):
    """ SET 3,C - Set the specified bit """
    cpu_object.register.C = 0b00000000
    cycle = op.code_cb_d9(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b00001000)

    cpu_object.register.C = 0b11111111
    cycle = op.code_cb_d9(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_da(cpu_object):
    """ SET 3,D - Set the specified bit """
    cpu_object.register.D = 0b00000000
    cycle = op.code_cb_da(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b00001000)

    cpu_object.register.D = 0b11111111
    cycle = op.code_cb_da(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_db(cpu_object):
    """ SET 3,E - Set the specified bit """
    cpu_object.register.E = 0b00000000
    cycle = op.code_cb_db(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b00001000)

    cpu_object.register.E = 0b11111111
    cycle = op.code_cb_db(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_dc(cpu_object):
    """ SET 3,H - Set the specified bit """
    cpu_object.register.H = 0b00000000
    cycle = op.code_cb_dc(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b00001000)

    cpu_object.register.H = 0b11111111
    cycle = op.code_cb_dc(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_dd(cpu_object):
    """ SET 3,L - Set the specified bit """
    cpu_object.register.L = 0b00000000
    cycle = op.code_cb_dd(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b00001000)

    cpu_object.register.L = 0b11111111
    cycle = op.code_cb_dd(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_de(cpu_object):
    """ SET 3,(HL) - Set the specified bit """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_de(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object, {0x1010: 0b00001000})

    cpu_object.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_de(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object,{0x1010:0b11111111})


# noinspection PyShadowingNames
def test_code_cb_df(cpu_object):
    """ SET 3,A - Set the specified bit """
    cpu_object.register.A = 0b00000000
    cycle = op.code_cb_df(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b00001000)

    cpu_object.register.A = 0b11111111
    cycle = op.code_cb_df(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_e0(cpu_object):
    """ SET 4,B - Set the specified bit """
    cpu_object.register.B = 0b00000000
    cycle = op.code_cb_e0(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b00010000)

    cpu_object.register.B = 0b11111111
    cycle = op.code_cb_e0(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_e1(cpu_object):
    """ SET 4,C - Set the specified bit """
    cpu_object.register.C = 0b00000000
    cycle = op.code_cb_e1(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b00010000)

    cpu_object.register.C = 0b11111111
    cycle = op.code_cb_e1(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_e2(cpu_object):
    """ SET 4,D - Set the specified bit """
    cpu_object.register.D = 0b00000000
    cycle = op.code_cb_e2(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b00010000)

    cpu_object.register.D = 0b11111111
    cycle = op.code_cb_e2(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_e3(cpu_object):
    """ SET 4,E - Set the specified bit """
    cpu_object.register.E = 0b00000000
    cycle = op.code_cb_e3(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b00010000)

    cpu_object.register.E = 0b11111111
    cycle = op.code_cb_e3(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_e4(cpu_object):
    """ SET 4,H - Set the specified bit """
    cpu_object.register.H = 0b00000000
    cycle = op.code_cb_e4(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b00010000)

    cpu_object.register.H = 0b11111111
    cycle = op.code_cb_e4(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_e5(cpu_object):
    """ SET 4,L - Set the specified bit """
    cpu_object.register.L = 0b00000000
    cycle = op.code_cb_e5(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b00010000)

    cpu_object.register.L = 0b11111111
    cycle = op.code_cb_e5(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_e6(cpu_object):
    """ SET 4,(HL) - Set the specified bit """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_e6(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object, {0x1010: 0b00010000})

    cpu_object.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_e6(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object,{0x1010:0b11111111})


# noinspection PyShadowingNames
def test_code_cb_e7(cpu_object):
    """ SET 4,A - Set the specified bit """
    cpu_object.register.A = 0b00000000
    cycle = op.code_cb_e7(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b00010000)

    cpu_object.register.A = 0b11111111
    cycle = op.code_cb_e7(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_e8(cpu_object):
    """ SET 5,B - Set the specified bit """
    cpu_object.register.B = 0b00000000
    cycle = op.code_cb_e8(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b00100000)

    cpu_object.register.B = 0b11111111
    cycle = op.code_cb_e8(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_e9(cpu_object):
    """ SET 5,C - Set the specified bit """
    cpu_object.register.C = 0b00000000
    cycle = op.code_cb_e9(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b00100000)

    cpu_object.register.C = 0b11111111
    cycle = op.code_cb_e9(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_ea(cpu_object):
    """ SET 5,D - Set the specified bit """
    cpu_object.register.D = 0b00000000
    cycle = op.code_cb_ea(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b00100000)

    cpu_object.register.D = 0b11111111
    cycle = op.code_cb_ea(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_eb(cpu_object):
    """ SET 5,E - Set the specified bit """
    cpu_object.register.E = 0b00000000
    cycle = op.code_cb_eb(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b00100000)

    cpu_object.register.E = 0b11111111
    cycle = op.code_cb_eb(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_ec(cpu_object):
    """ SET 5,H - Set the specified bit """
    cpu_object.register.H = 0b00000000
    cycle = op.code_cb_ec(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b00100000)

    cpu_object.register.H = 0b11111111
    cycle = op.code_cb_ec(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_ed(cpu_object):
    """ SET 5,L - Set the specified bit """
    cpu_object.register.L = 0b00000000
    cycle = op.code_cb_ed(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b00100000)

    cpu_object.register.L = 0b11111111
    cycle = op.code_cb_ed(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_ee(cpu_object):
    """ SET 5,(HL) - Set the specified bit """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_ee(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object, {0x1010: 0b00100000})

    cpu_object.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_ee(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object,{0x1010:0b11111111})


# noinspection PyShadowingNames
def test_code_cb_ef(cpu_object):
    """ SET 5,A - Set the specified bit """
    cpu_object.register.A = 0b00000000
    cycle = op.code_cb_ef(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b00100000)

    cpu_object.register.A = 0b11111111
    cycle = op.code_cb_ef(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_f0(cpu_object):
    """ SET 6,B - Set the specified bit """
    cpu_object.register.B = 0b00000000
    cycle = op.code_cb_f0(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b01000000)

    cpu_object.register.B = 0b11111111
    cycle = op.code_cb_f0(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_f1(cpu_object):
    """ SET 6,C - Set the specified bit """
    cpu_object.register.C = 0b00000000
    cycle = op.code_cb_f1(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b01000000)

    cpu_object.register.C = 0b11111111
    cycle = op.code_cb_f1(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_f2(cpu_object):
    """ SET 6,D - Set the specified bit """
    cpu_object.register.D = 0b00000000
    cycle = op.code_cb_f2(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b01000000)

    cpu_object.register.D = 0b11111111
    cycle = op.code_cb_f2(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_f3(cpu_object):
    """ SET 6,E - Set the specified bit """
    cpu_object.register.E = 0b00000000
    cycle = op.code_cb_f3(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b01000000)

    cpu_object.register.E = 0b11111111
    cycle = op.code_cb_f3(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_f4(cpu_object):
    """ SET 6,H - Set the specified bit """
    cpu_object.register.H = 0b00000000
    cycle = op.code_cb_f4(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b01000000)

    cpu_object.register.H = 0b11111111
    cycle = op.code_cb_f4(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_f5(cpu_object):
    """ SET 6,L - Set the specified bit """
    cpu_object.register.L = 0b00000000
    cycle = op.code_cb_f5(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b01000000)

    cpu_object.register.L = 0b11111111
    cycle = op.code_cb_f5(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_f6(cpu_object):
    """ SET 6,(HL) - Set the specified bit """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_f6(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object, {0x1010: 0b01000000})

    cpu_object.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_f6(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object,{0x1010:0b11111111})


# noinspection PyShadowingNames
def test_code_cb_f7(cpu_object):
    """ SET 6,A - Set the specified bit """
    cpu_object.register.A = 0b00000000
    cycle = op.code_cb_f7(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b01000000)

    cpu_object.register.A = 0b11111111
    cycle = op.code_cb_f7(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_f8(cpu_object):
    """ SET 7,B - Set the specified bit """
    cpu_object.register.B = 0b00000000
    cycle = op.code_cb_f8(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b10000000)

    cpu_object.register.B = 0b11111111
    cycle = op.code_cb_f8(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, B=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_f9(cpu_object):
    """ SET 7,C - Set the specified bit """
    cpu_object.register.C = 0b00000000
    cycle = op.code_cb_f9(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b10000000)

    cpu_object.register.C = 0b11111111
    cycle = op.code_cb_f9(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, C=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_fa(cpu_object):
    """ SET 7,D - Set the specified bit """
    cpu_object.register.D = 0b00000000
    cycle = op.code_cb_fa(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b10000000)

    cpu_object.register.D = 0b11111111
    cycle = op.code_cb_fa(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, D=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_fb(cpu_object):
    """ SET 7,E - Set the specified bit """
    cpu_object.register.E = 0b00000000
    cycle = op.code_cb_fb(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b10000000)

    cpu_object.register.E = 0b11111111
    cycle = op.code_cb_fb(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, E=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_fc(cpu_object):
    """ SET 7,H - Set the specified bit """
    cpu_object.register.H = 0b00000000
    cycle = op.code_cb_fc(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b10000000)

    cpu_object.register.H = 0b11111111
    cycle = op.code_cb_fc(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, H=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_fd(cpu_object):
    """ SET 7,L - Set the specified bit """
    cpu_object.register.L = 0b00000000
    cycle = op.code_cb_fd(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b10000000)

    cpu_object.register.L = 0b11111111
    cycle = op.code_cb_fd(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, L=0b11111111)

    assert_memory(cpu_object)


# noinspection PyShadowingNames
def test_code_cb_fe(cpu_object):
    """ SET 7,(HL) - Set the specified bit """
    cpu_object.register.set_hl(0x1010)
    cpu_object.memory.write_8bit(0x1010, 0b00000000)
    cycle = op.code_cb_fe(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object, {0x1010: 0b10000000})

    cpu_object.memory.write_8bit(0x1010, 0b11111111)
    cycle = op.code_cb_fe(cpu_object)
    assert cycle == 16
    assert_registers(cpu_object, H=0x10, L=0x10)
    assert_memory(cpu_object,{0x1010:0b11111111})


# noinspection PyShadowingNames
def test_code_cb_ff(cpu_object):
    """ SET 7,A - Set the specified bit """
    cpu_object.register.A = 0b00000000
    cycle = op.code_cb_ff(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b10000000)

    cpu_object.register.A = 0b11111111
    cycle = op.code_cb_ff(cpu_object)
    assert cycle == 8
    assert_registers(cpu_object, A=0b11111111)

    assert_memory(cpu_object)
