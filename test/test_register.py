"""
Tests for cpu/register.py
"""

import pytest

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
    from register import Register
    return Register()


"""
Tests
"""


def assert_registers(reg, A=0x00, F=0x00, B=0x00, C=0x00, D=0x00, E=0x00, H=0x00, L=0x00, SP=0xFFFE, PC=0x0100):
    """
    Helper function to assert registers values.
    By default will check if values are the default, unless parameter is received.
    """
    assert reg.A == A
    assert reg.F == F
    assert reg.B == B
    assert reg.C == C
    assert reg.D == D
    assert reg.E == E
    assert reg.H == H
    assert reg.L == L
    assert reg.SP == SP
    assert reg.PC == PC


# noinspection PyShadowingNames
def test_default_initial_values(register):
    assert_registers(register)


# noinspection PyShadowingNames
def test_get_zero_flag(register):
    register.F = 0b11110000
    flag = register.get_z_flag()
    assert flag == 1

    register.F = 0b01110000
    flag = register.get_z_flag()
    assert flag == 0

    register.F = 0b00000000
    flag = register.get_z_flag()
    assert flag == 0

    register.F = 0b10000000
    flag = register.get_z_flag()
    assert flag == 1


# noinspection PyShadowingNames
def test_get_subtract_flag(register):
    register.F = 0b11110000
    flag = register.get_n_flag()
    assert flag == 1

    register.F = 0b10110000
    flag = register.get_n_flag()
    assert flag == 0

    register.F = 0b00000000
    flag = register.get_n_flag()
    assert flag == 0

    register.F = 0b01000000
    flag = register.get_n_flag()
    assert flag == 1


# noinspection PyShadowingNames
def test_get_half_carry_flag(register):
    register.F = 0b11110000
    flag = register.get_h_flag()
    assert flag == 1

    register.F = 0b11010000
    flag = register.get_h_flag()
    assert flag == 0

    register.F = 0b00000000
    flag = register.get_h_flag()
    assert flag == 0

    register.F = 0b00100000
    flag = register.get_h_flag()
    assert flag == 1


# noinspection PyShadowingNames
def test_get_carry_flag(register):
    register.F = 0b11110000
    flag = register.get_c_flag()
    assert flag == 1

    register.F = 0b11100000
    flag = register.get_c_flag()
    assert flag == 0

    register.F = 0b00000000
    flag = register.get_c_flag()
    assert flag == 0

    register.F = 0b00010000
    flag = register.get_c_flag()
    assert flag == 1


# noinspection PyShadowingNames
def test_set_zero_flag(register):
    register.F = 0b11110000
    register.set_z_flag(True)
    assert_registers(register, F=0b11110000)

    register.F = 0b11110000
    register.set_z_flag(False)
    assert_registers(register, F=0b01110000)

    register.F = 0b00000000
    register.set_z_flag(True)
    assert_registers(register, F=0b10000000)

    register.F = 0b00000000
    register.set_z_flag(False)
    assert_registers(register, F=0b00000000)


# noinspection PyShadowingNames
def test_set_subtract_flag(register):
    register.F = 0b11110000
    register.set_n_flag(True)
    assert_registers(register, F=0b11110000)

    register.F = 0b11110000
    register.set_n_flag(False)
    assert_registers(register, F=0b10110000)

    register.F = 0b00000000
    register.set_n_flag(True)
    assert_registers(register, F=0b01000000)

    register.F = 0b00000000
    register.set_n_flag(False)
    assert_registers(register, F=0b00000000)


# noinspection PyShadowingNames
def test_set_half_carry_flag(register):
    register.F = 0b11110000
    register.set_h_flag(True)
    assert_registers(register, F=0b11110000)

    register.F = 0b11110000
    register.set_h_flag(False)
    assert_registers(register, F=0b11010000)

    register.F = 0b00000000
    register.set_h_flag(True)
    assert_registers(register, F=0b00100000)

    register.F = 0b00000000
    register.set_h_flag(False)
    assert_registers(register, F=0b00000000)


# noinspection PyShadowingNames
def test_set_carry_flag(register):
    register.F = 0b11110000
    register.set_c_flag(True)
    assert_registers(register, F=0b11110000)

    register.F = 0b11110000
    register.set_c_flag(False)
    assert_registers(register, F=0b11100000)

    register.F = 0b00000000
    register.set_c_flag(True)
    assert_registers(register, F=0b00010000)

    register.F = 0b00000000
    register.set_c_flag(False)
    assert_registers(register, F=0b00000000)


# noinspection PyShadowingNames
def test_get_af(register):
    register.A = 0xFE
    register.F = 0x15
    af = register.get_af()
    assert af == 0xFE15


# noinspection PyShadowingNames
def test_get_bc(register):
    register.B = 0xFE
    register.C = 0x15
    bc = register.get_bc()
    assert bc == 0xFE15


# noinspection PyShadowingNames
def test_get_de(register):
    register.D = 0xFE
    register.E = 0x15
    de = register.get_de()
    assert de == 0xFE15


# noinspection PyShadowingNames
def test_get_hl(register):
    register.H = 0xFE
    register.L = 0x15
    hl = register.get_hl()
    assert hl == 0xFE15


# noinspection PyShadowingNames
def test_set_af(register):
    register.A = 0x01
    register.F = 0x01
    register.set_af(0xFE15)
    assert_registers(register, A=0xFE, F=0x15)


# noinspection PyShadowingNames
def test_set_bc(register):
    register.B = 0x01
    register.C = 0x01
    register.set_bc(0xFE15)
    assert_registers(register, B=0xFE, C=0x15)


# noinspection PyShadowingNames
def test_set_de(register):
    register.D = 0x01
    register.E = 0x01
    register.set_de(0xFE15)
    assert_registers(register, D=0xFE, E=0x15)


# noinspection PyShadowingNames
def test_set_hl(register):
    register.H = 0x01
    register.L = 0x01
    register.set_hl(0xFE15)
    assert_registers(register, H=0xFE, L=0x15)
