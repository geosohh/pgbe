import pytest

"""
Fixtures act as test setup/teardown in py.test.
For each test method with a parameter, the parameter name is the setup method that will be called.
"""


@pytest.fixture
def register():
    from cpu.register import Register
    return Register()


"""
Tests
"""


# noinspection PyShadowingNames
def test_default_initial_values(register):
    assert register.A  == 0x00
    assert register.F  == 0x00
    assert register.B  == 0x00
    assert register.C  == 0x00
    assert register.D  == 0x00
    assert register.E  == 0x00
    assert register.H  == 0x00
    assert register.L  == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_add_af_zeros(register):
    register.add_af(0xFE15)
    assert register.A == 0xFE
    assert register.F == 0x15
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_add_af_non_zeros(register):
    register.A = 0x01
    register.F = 0x02
    register.add_af(0xFE15)
    assert register.A == 0xFF
    assert register.F == 0x17
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_add_af_over_ff(register):
    register.A = 0xFF
    register.F = 0x00
    register.add_af(0xFF15)
    assert register.A == 0xFE
    assert register.F == 0x15
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100

    register.A = 0x00
    register.F = 0xFF
    register.add_af(0x15FF)
    assert register.A == 0x16
    assert register.F == 0xFE
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100

    register.A = 0xFF
    register.F = 0xFF
    register.add_af(0xFFFF)
    assert register.A == 0xFF
    assert register.F == 0xFE
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_add_bc_zeros(register):
    register.add_bc(0xFE15)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0xFE
    assert register.C == 0x15
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_add_bc_non_zeros(register):
    register.B = 0x01
    register.C = 0x02
    register.add_bc(0xFE15)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0xFF
    assert register.C == 0x17
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_add_bc_over_ff(register):
    register.B = 0xFF
    register.C = 0x00
    register.add_bc(0xFF15)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0xFE
    assert register.C == 0x15
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100

    register.B = 0x00
    register.C = 0xFF
    register.add_bc(0x15FF)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x16
    assert register.C == 0xFE
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100

    register.B = 0xFF
    register.C = 0xFF
    register.add_bc(0xFFFF)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0xFF
    assert register.C == 0xFE
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_add_de_zeros(register):
    register.add_de(0xFE15)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0xFE
    assert register.E == 0x15
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_add_de_non_zeros(register):
    register.D = 0x01
    register.E = 0x02
    register.add_de(0xFE15)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0xFF
    assert register.E == 0x17
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_add_de_over_ff(register):
    register.D = 0xFF
    register.E = 0x00
    register.add_de(0xFF15)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0xFE
    assert register.E == 0x15
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100

    register.D = 0x00
    register.E = 0xFF
    register.add_de(0x15FF)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x16
    assert register.E == 0xFE
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100

    register.D = 0xFF
    register.E = 0xFF
    register.add_de(0xFFFF)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0xFF
    assert register.E == 0xFE
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_add_hl_zeros(register):
    register.add_hl(0xFE15)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0xFE
    assert register.L == 0x15
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_add_hl_non_zeros(register):
    register.H = 0x01
    register.L = 0x02
    register.add_hl(0xFE15)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0xFF
    assert register.L == 0x17
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_add_hl_over_ff(register):
    register.H = 0xFF
    register.L = 0x00
    register.add_hl(0xFF15)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0xFE
    assert register.L == 0x15
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100

    register.H = 0x00
    register.L = 0xFF
    register.add_hl(0x15FF)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x16
    assert register.L == 0xFE
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100

    register.H = 0xFF
    register.L = 0xFF
    register.add_hl(0xFFFF)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0xFF
    assert register.L == 0xFE
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_set_af(register):
    register.A = 0x01
    register.F = 0x01
    register.set_af(0xFE15)
    assert register.A == 0xFE
    assert register.F == 0x15
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_set_bc(register):
    register.B = 0x01
    register.C = 0x01
    register.set_bc(0xFE15)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0xFE
    assert register.C == 0x15
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_set_de(register):
    register.D = 0x01
    register.E = 0x01
    register.set_de(0xFE15)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0xFE
    assert register.E == 0x15
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_set_hl(register):
    register.H = 0x01
    register.L = 0x01
    register.set_hl(0xFE15)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0xFE
    assert register.L == 0x15
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_sub_af_ffff(register):
    register.A = 0xFF
    register.F = 0xFF
    register.sub_af(0xFE15)
    assert register.A == 0x01
    assert register.F == 0xEA
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_sub_af_below_0000(register):
    register.A = 0x10
    register.F = 0xFE
    register.sub_af(0x00FF)
    assert register.A == 0x0F
    assert register.F == 0xFF
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100

    register.A = 0x00
    register.F = 0x01
    register.sub_af(0x0100)
    assert register.A == 0x00
    assert register.F == 0xFF
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100

    register.A = 0x00
    register.F = 0x00
    register.sub_af(0xFFFF)
    assert register.A == 0xFF
    assert register.F == 0xFF
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_sub_bc_ffff(register):
    register.B = 0xFF
    register.C = 0xFF
    register.sub_bc(0xFE15)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x01
    assert register.C == 0xEA
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_sub_bc_below_0000(register):
    register.B = 0x10
    register.C = 0xFE
    register.sub_bc(0x00FF)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x0F
    assert register.C == 0xFF
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100

    register.B = 0x00
    register.C = 0x01
    register.sub_bc(0x0100)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0xFF
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100

    register.B = 0x00
    register.C = 0x00
    register.sub_bc(0xFFFF)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0xFF
    assert register.C == 0xFF
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_sub_de_ffff(register):
    register.D = 0xFF
    register.E = 0xFF
    register.sub_de(0xFE15)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x01
    assert register.E == 0xEA
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_sub_de_below_0000(register):
    register.D = 0x10
    register.E = 0xFE
    register.sub_de(0x00FF)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x0F
    assert register.E == 0xFF
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100

    register.D = 0x00
    register.E = 0x01
    register.sub_de(0x0100)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0xFF
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100

    register.D = 0x00
    register.E = 0x00
    register.sub_de(0xFFFF)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0xFF
    assert register.E == 0xFF
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_sub_hl_ffff(register):
    register.H = 0xFF
    register.L = 0xFF
    register.sub_hl(0xFE15)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x01
    assert register.L == 0xEA
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_sub_hl_below_0000(register):
    register.H = 0x10
    register.L = 0xFE
    register.sub_hl(0x00FF)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x0F
    assert register.L == 0xFF
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100

    register.H = 0x00
    register.L = 0x01
    register.sub_hl(0x0100)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0xFF
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100

    register.H = 0x00
    register.L = 0x00
    register.sub_hl(0xFFFF)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0xFF
    assert register.L == 0xFF
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100
