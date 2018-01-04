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


# noinspection PyShadowingNames
def test_default_initial_values(register):
    assert_registers(register)


# noinspection PyShadowingNames
def test_get_zero_flag(register):
    register.F = 0b11110000
    flag = register.get_zero_flag()
    assert flag == 1

    register.F = 0b01110000
    flag = register.get_zero_flag()
    assert flag == 0

    register.F = 0b00000000
    flag = register.get_zero_flag()
    assert flag == 0

    register.F = 0b10000000
    flag = register.get_zero_flag()
    assert flag == 1


# noinspection PyShadowingNames
def test_get_subtract_flag(register):
    register.F = 0b11110000
    flag = register.get_subtract_flag()
    assert flag == 1

    register.F = 0b10110000
    flag = register.get_subtract_flag()
    assert flag == 0

    register.F = 0b00000000
    flag = register.get_subtract_flag()
    assert flag == 0

    register.F = 0b01000000
    flag = register.get_subtract_flag()
    assert flag == 1


# noinspection PyShadowingNames
def test_get_half_carry_flag(register):
    register.F = 0b11110000
    flag = register.get_half_carry_flag()
    assert flag == 1

    register.F = 0b11010000
    flag = register.get_half_carry_flag()
    assert flag == 0

    register.F = 0b00000000
    flag = register.get_half_carry_flag()
    assert flag == 0

    register.F = 0b00100000
    flag = register.get_half_carry_flag()
    assert flag == 1


# noinspection PyShadowingNames
def test_get_carry_flag(register):
    register.F = 0b11110000
    flag = register.get_carry_flag()
    assert flag == 1

    register.F = 0b11100000
    flag = register.get_carry_flag()
    assert flag == 0

    register.F = 0b00000000
    flag = register.get_carry_flag()
    assert flag == 0

    register.F = 0b00010000
    flag = register.get_carry_flag()
    assert flag == 1


# noinspection PyShadowingNames
def test_set_zero_flag(register):
    register.F = 0b11110000
    register.set_zero_flag(True)
    assert_registers(register, f=0b11110000)

    register.F = 0b11110000
    register.set_zero_flag(False)
    assert_registers(register, f=0b01110000)

    register.F = 0b00000000
    register.set_zero_flag(True)
    assert_registers(register, f=0b10000000)

    register.F = 0b00000000
    register.set_zero_flag(False)
    assert_registers(register, f=0b00000000)


# noinspection PyShadowingNames
def test_set_subtract_flag(register):
    register.F = 0b11110000
    register.set_subtract_flag(True)
    assert_registers(register, f=0b11110000)

    register.F = 0b11110000
    register.set_subtract_flag(False)
    assert_registers(register, f=0b10110000)

    register.F = 0b00000000
    register.set_subtract_flag(True)
    assert_registers(register, f=0b01000000)

    register.F = 0b00000000
    register.set_subtract_flag(False)
    assert_registers(register, f=0b00000000)


# noinspection PyShadowingNames
def test_set_half_carry_flag(register):
    register.F = 0b11110000
    register.set_half_carry_flag(True)
    assert_registers(register, f=0b11110000)

    register.F = 0b11110000
    register.set_half_carry_flag(False)
    assert_registers(register, f=0b11010000)

    register.F = 0b00000000
    register.set_half_carry_flag(True)
    assert_registers(register, f=0b00100000)

    register.F = 0b00000000
    register.set_half_carry_flag(False)
    assert_registers(register, f=0b00000000)


# noinspection PyShadowingNames
def test_set_carry_flag(register):
    register.F = 0b11110000
    register.set_carry_flag(True)
    assert_registers(register, f=0b11110000)

    register.F = 0b11110000
    register.set_carry_flag(False)
    assert_registers(register, f=0b11100000)

    register.F = 0b00000000
    register.set_carry_flag(True)
    assert_registers(register, f=0b00010000)

    register.F = 0b00000000
    register.set_carry_flag(False)
    assert_registers(register, f=0b00000000)


# noinspection PyShadowingNames
def test_add_af_zeros(register):
    register.add_af(0xFE15)
    assert_registers(register, a=0xFE, f=0x15)


# noinspection PyShadowingNames
def test_add_af_non_zeros(register):
    register.A = 0x01
    register.F = 0x02
    register.add_af(0xFE15)
    assert_registers(register, a=0xFF, f=0x17)


# noinspection PyShadowingNames
def test_add_af_over_ff(register):
    register.A = 0xFF
    register.F = 0x00
    register.add_af(0xFF15)
    assert_registers(register, a=0xFE, f=0x15)

    register.A = 0x00
    register.F = 0xFF
    register.add_af(0x15FF)
    assert_registers(register, a=0x16, f=0xFE)

    register.A = 0xFF
    register.F = 0xFF
    register.add_af(0xFFFF)
    assert_registers(register, a=0xFF, f=0xFE)


# noinspection PyShadowingNames
def test_add_bc_zeros(register):
    register.add_bc(0xFE15)
    assert_registers(register, b=0xFE, c=0x15)


# noinspection PyShadowingNames
def test_add_bc_non_zeros(register):
    register.B = 0x01
    register.C = 0x02
    register.add_bc(0xFE15)
    assert_registers(register, b=0xFF, c=0x17)


# noinspection PyShadowingNames
def test_add_bc_over_ff(register):
    register.B = 0xFF
    register.C = 0x00
    register.add_bc(0xFF15)
    assert_registers(register, b=0xFE, c=0x15)

    register.B = 0x00
    register.C = 0xFF
    register.add_bc(0x15FF)
    assert_registers(register, b=0x16, c=0xFE)

    register.B = 0xFF
    register.C = 0xFF
    register.add_bc(0xFFFF)
    assert_registers(register, b=0xFF, c=0xFE)


# noinspection PyShadowingNames
def test_add_de_zeros(register):
    register.add_de(0xFE15)
    assert_registers(register, d=0xFE, e=0x15)


# noinspection PyShadowingNames
def test_add_de_non_zeros(register):
    register.D = 0x01
    register.E = 0x02
    register.add_de(0xFE15)
    assert_registers(register, d=0xFF, e=0x17)


# noinspection PyShadowingNames
def test_add_de_over_ff(register):
    register.D = 0xFF
    register.E = 0x00
    register.add_de(0xFF15)
    assert_registers(register, d=0xFE, e=0x15)

    register.D = 0x00
    register.E = 0xFF
    register.add_de(0x15FF)
    assert_registers(register, d=0x16, e=0xFE)

    register.D = 0xFF
    register.E = 0xFF
    register.add_de(0xFFFF)
    assert_registers(register, d=0xFF, e=0xFE)


# noinspection PyShadowingNames
def test_add_hl_zeros(register):
    register.add_hl(0xFE15)
    assert_registers(register, h=0xFE, l=0x15)


# noinspection PyShadowingNames
def test_add_hl_non_zeros(register):
    register.H = 0x01
    register.L = 0x02
    register.add_hl(0xFE15)
    assert_registers(register, h=0xFF, l=0x17)


# noinspection PyShadowingNames
def test_add_hl_over_ff(register):
    register.H = 0xFF
    register.L = 0x00
    register.add_hl(0xFF15)
    assert_registers(register, h=0xFE, l=0x15)

    register.H = 0x00
    register.L = 0xFF
    register.add_hl(0x15FF)
    assert_registers(register, h=0x16, l=0xFE)

    register.H = 0xFF
    register.L = 0xFF
    register.add_hl(0xFFFF)
    assert_registers(register, h=0xFF, l=0xFE)


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
    assert_registers(register, a=0xFE, f=0x15)


# noinspection PyShadowingNames
def test_set_bc(register):
    register.B = 0x01
    register.C = 0x01
    register.set_bc(0xFE15)
    assert_registers(register, b=0xFE, c=0x15)


# noinspection PyShadowingNames
def test_set_de(register):
    register.D = 0x01
    register.E = 0x01
    register.set_de(0xFE15)
    assert_registers(register, d=0xFE, e=0x15)


# noinspection PyShadowingNames
def test_set_hl(register):
    register.H = 0x01
    register.L = 0x01
    register.set_hl(0xFE15)
    assert_registers(register, h=0xFE, l=0x15)


# noinspection PyShadowingNames
def test_sub_af_ffff(register):
    register.A = 0xFF
    register.F = 0xFF
    register.sub_af(0xFE15)
    assert_registers(register, a=0x01, f=0xEA)


# noinspection PyShadowingNames
def test_sub_af_below_0000(register):
    register.A = 0x10
    register.F = 0xFE
    register.sub_af(0x00FF)
    assert_registers(register, a=0x0F, f=0xFF)

    register.A = 0x00
    register.F = 0x01
    register.sub_af(0x0100)
    assert_registers(register, a=0x00, f=0xFF)

    register.A = 0x00
    register.F = 0x00
    register.sub_af(0xFFFF)
    assert_registers(register, a=0xFF, f=0xFF)


# noinspection PyShadowingNames
def test_sub_bc_ffff(register):
    register.B = 0xFF
    register.C = 0xFF
    register.sub_bc(0xFE15)
    assert_registers(register, b=0x01, c=0xEA)


# noinspection PyShadowingNames
def test_sub_bc_below_0000(register):
    register.B = 0x10
    register.C = 0xFE
    register.sub_bc(0x00FF)
    assert_registers(register, b=0x0F, c=0xFF)

    register.B = 0x00
    register.C = 0x01
    register.sub_bc(0x0100)
    assert_registers(register, b=0x00, c=0xFF)

    register.B = 0x00
    register.C = 0x00
    register.sub_bc(0xFFFF)
    assert_registers(register, b=0xFF, c=0xFF)


# noinspection PyShadowingNames
def test_sub_de_ffff(register):
    register.D = 0xFF
    register.E = 0xFF
    register.sub_de(0xFE15)
    assert_registers(register, d=0x01, e=0xEA)


# noinspection PyShadowingNames
def test_sub_de_below_0000(register):
    register.D = 0x10
    register.E = 0xFE
    register.sub_de(0x00FF)
    assert_registers(register, d=0x0F, e=0xFF)

    register.D = 0x00
    register.E = 0x01
    register.sub_de(0x0100)
    assert_registers(register, d=0x00, e=0xFF)

    register.D = 0x00
    register.E = 0x00
    register.sub_de(0xFFFF)
    assert_registers(register, d=0xFF, e=0xFF)


# noinspection PyShadowingNames
def test_sub_hl_ffff(register):
    register.H = 0xFF
    register.L = 0xFF
    register.sub_hl(0xFE15)
    assert_registers(register, h=0x01, l=0xEA)


# noinspection PyShadowingNames
def test_sub_hl_below_0000(register):
    register.H = 0x10
    register.L = 0xFE
    register.sub_hl(0x00FF)
    assert_registers(register, h=0x0F, l=0xFF)

    register.H = 0x00
    register.L = 0x01
    register.sub_hl(0x0100)
    assert_registers(register, h=0x00, l=0xFF)

    register.H = 0x00
    register.L = 0x00
    register.sub_hl(0xFFFF)
    assert_registers(register, h=0xFF, l=0xFF)
