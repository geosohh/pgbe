import pytest
import cpu.op

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
def test_code_02(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_06(register):
    cpu.op.code_06(register,0x99)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x99
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_0a(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_0e(register):
    cpu.op.code_0e(register,0x99)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x99
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_12(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_16(register):
    cpu.op.code_16(register,0x99)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x99
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_1a(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_1e(register):
    cpu.op.code_1e(register,0x99)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x99
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_26(register):
    cpu.op.code_26(register,0x99)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x99
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_2e(register):
    cpu.op.code_2e(register,0x99)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x99
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_36(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_3a(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_3e(register):
    cpu.op.code_3e(register,0x99)
    assert register.A == 0x99
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_40(register):
    register.B = 0x99
    cpu.op.code_40(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x99
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_41(register):
    register.C = 0x99
    cpu.op.code_41(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x99
    assert register.C == 0x99
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_42(register):
    register.D = 0x99
    cpu.op.code_42(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x99
    assert register.C == 0x00
    assert register.D == 0x99
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_43(register):
    register.E = 0x99
    cpu.op.code_43(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x99
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x99
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_44(register):
    register.H = 0x99
    cpu.op.code_44(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x99
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x99
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_45(register):
    register.L = 0x99
    cpu.op.code_45(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x99
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x99
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_46(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_47(register):
    register.A = 0x99
    cpu.op.code_47(register)
    assert register.A == 0x99
    assert register.F == 0x00
    assert register.B == 0x99
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_48(register):
    register.B = 0x99
    cpu.op.code_48(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x99
    assert register.C == 0x99
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_49(register):
    register.C = 0x99
    cpu.op.code_49(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x99
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_4a(register):
    register.D = 0x99
    cpu.op.code_4a(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x99
    assert register.D == 0x99
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_4b(register):
    register.E = 0x99
    cpu.op.code_4b(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x99
    assert register.D == 0x00
    assert register.E == 0x99
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_4c(register):
    register.H = 0x99
    cpu.op.code_4c(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x99
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x99
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_4d(register):
    register.L = 0x99
    cpu.op.code_4d(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x99
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x99
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_4e(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_4f(register):
    register.A = 0x99
    cpu.op.code_4f(register)
    assert register.A == 0x99
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x99
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_50(register):
    register.B = 0x99
    cpu.op.code_50(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x99
    assert register.C == 0x00
    assert register.D == 0x99
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_51(register):
    register.C = 0x99
    cpu.op.code_51(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x99
    assert register.D == 0x99
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_52(register):
    register.D = 0x99
    cpu.op.code_52(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x99
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_53(register):
    register.E = 0x99
    cpu.op.code_53(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x99
    assert register.E == 0x99
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_54(register):
    register.H = 0x99
    cpu.op.code_54(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x99
    assert register.E == 0x00
    assert register.H == 0x99
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_55(register):
    register.L = 0x99
    cpu.op.code_55(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x99
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x99
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_56(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_57(register):
    register.A = 0x99
    cpu.op.code_57(register)
    assert register.A == 0x99
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x99
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_58(register):
    register.B = 0x99
    cpu.op.code_58(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x99
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x99
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_59(register):
    register.C = 0x99
    cpu.op.code_59(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x99
    assert register.D == 0x00
    assert register.E == 0x99
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_5a(register):
    register.D = 0x99
    cpu.op.code_5a(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x99
    assert register.E == 0x99
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_5b(register):
    register.E = 0x99
    cpu.op.code_5b(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x99
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_5c(register):
    register.H = 0x99
    cpu.op.code_5c(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x99
    assert register.H == 0x99
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_5d(register):
    register.L = 0x99
    cpu.op.code_5d(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x99
    assert register.H == 0x00
    assert register.L == 0x99
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_5e(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_5f(register):
    register.A = 0x99
    cpu.op.code_5f(register)
    assert register.A == 0x99
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x99
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_60(register):
    register.B = 0x99
    cpu.op.code_60(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x99
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x99
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_61(register):
    register.C = 0x99
    cpu.op.code_61(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x99
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x99
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_62(register):
    register.D = 0x99
    cpu.op.code_62(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x99
    assert register.E == 0x00
    assert register.H == 0x99
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_63(register):
    register.E = 0x99
    cpu.op.code_63(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x99
    assert register.H == 0x99
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_64(register):
    register.H = 0x99
    cpu.op.code_64(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x99
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_65(register):
    register.L = 0x99
    cpu.op.code_65(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x99
    assert register.L == 0x99
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_66(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_67(register):
    register.A = 0x99
    cpu.op.code_67(register)
    assert register.A == 0x99
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x99
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_68(register):
    register.B = 0x99
    cpu.op.code_68(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x99
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x99
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_69(register):
    register.C = 0x99
    cpu.op.code_69(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x99
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x99
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_6a(register):
    register.D = 0x99
    cpu.op.code_6a(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x99
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x99
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_6b(register):
    register.E = 0x99
    cpu.op.code_6b(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x99
    assert register.H == 0x00
    assert register.L == 0x99
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_6c(register):
    register.H = 0x99
    cpu.op.code_6c(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x99
    assert register.L == 0x99
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_6d(register):
    register.L = 0x99
    cpu.op.code_6d(register)
    assert register.A == 0x00
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x99
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_6e(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_6f(register):
    register.A = 0x99
    cpu.op.code_6f(register)
    assert register.A == 0x99
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x99
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_70(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_71(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_72(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_73(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_74(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_75(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_77(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_78(register):
    register.B = 0x99
    cpu.op.code_78(register)
    assert register.A == 0x99
    assert register.F == 0x00
    assert register.B == 0x99
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_79(register):
    register.C = 0x99
    cpu.op.code_79(register)
    assert register.A == 0x99
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x99
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_7a(register):
    register.D = 0x99
    cpu.op.code_7a(register)
    assert register.A == 0x99
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x99
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_7b(register):
    register.E = 0x99
    cpu.op.code_7b(register)
    assert register.A == 0x99
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x99
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_7c(register):
    register.H = 0x99
    cpu.op.code_7c(register)
    assert register.A == 0x99
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x99
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_7d(register):
    register.L = 0x99
    cpu.op.code_7d(register)
    assert register.A == 0x99
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x99
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_7e(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_7f(register):
    register.A = 0x99
    cpu.op.code_7f(register)
    assert register.A == 0x99
    assert register.F == 0x00
    assert register.B == 0x00
    assert register.C == 0x00
    assert register.D == 0x00
    assert register.E == 0x00
    assert register.H == 0x00
    assert register.L == 0x00
    assert register.SP == 0xFFFE
    assert register.PC == 0x0100


# noinspection PyShadowingNames
def test_code_e2(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_ea(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_f2(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_fa(register):
    # TODO after memory is implemented
    pass

