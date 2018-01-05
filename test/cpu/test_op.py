import pytest
import cpu.op

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
def test_code_01(register):
    cycles = cpu.op.code_01(register, 0x9933)  # Little-endian
    assert cycles == 8
    assert_registers(register,b=0x33, c=0x99)


# noinspection PyShadowingNames
def test_code_02(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_06(register):
    cycles = cpu.op.code_06(register, 0x99)
    assert cycles == 8
    assert_registers(register,b=0x99)


# noinspection PyShadowingNames
def test_code_08(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_0a(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_0e(register):
    cycles = cpu.op.code_0e(register, 0x99)
    assert cycles == 8
    assert_registers(register,c=0x99)


# noinspection PyShadowingNames
def test_code_11(register):
    cycles = cpu.op.code_11(register, 0x9933)  # Little-endian
    assert cycles == 12
    assert_registers(register,d=0x33,e=0x99)


# noinspection PyShadowingNames
def test_code_12(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_16(register):
    cycles = cpu.op.code_16(register, 0x99)
    assert cycles == 8
    assert_registers(register,d=0x99)


# noinspection PyShadowingNames
def test_code_1a(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_1e(register):
    cycles = cpu.op.code_1e(register, 0x99)
    assert cycles == 8
    assert_registers(register,e=0x99)


# noinspection PyShadowingNames
def test_code_21(register):
    cycles = cpu.op.code_21(register, 0x9933)  # Little-endian
    assert cycles == 12
    assert_registers(register,h=0x33,l=0x99)


# noinspection PyShadowingNames
def test_code_22(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_26(register):
    cycles = cpu.op.code_26(register, 0x99)
    assert cycles == 8
    assert_registers(register,h=0x99)


# noinspection PyShadowingNames
def test_code_2a(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_2e(register):
    cycles = cpu.op.code_2e(register, 0x99)
    assert cycles == 8
    assert_registers(register,l=0x99)


# noinspection PyShadowingNames
def test_code_31(register):
    cycles = cpu.op.code_31(register, 0x9933)
    assert cycles == 12
    assert_registers(register,sp=0x3399)


# noinspection PyShadowingNames
def test_code_32(register):
    # TODO after memory is implemented
    pass


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
    cycles = cpu.op.code_3e(register, 0x99)
    assert cycles == 8
    assert_registers(register,a=0x99)


# noinspection PyShadowingNames
def test_code_40(register):
    register.B = 0x99
    cycles = cpu.op.code_40(register)
    assert cycles == 4
    assert_registers(register,b=0x99)


# noinspection PyShadowingNames
def test_code_41(register):
    register.C = 0x99
    cycles = cpu.op.code_41(register)
    assert cycles == 4
    assert_registers(register,b=0x99,c=0x99)


# noinspection PyShadowingNames
def test_code_42(register):
    register.D = 0x99
    cycles = cpu.op.code_42(register)
    assert cycles == 4
    assert_registers(register,b=0x99,d=0x99)


# noinspection PyShadowingNames
def test_code_43(register):
    register.E = 0x99
    cycles = cpu.op.code_43(register)
    assert cycles == 4
    assert_registers(register,b=0x99,e=0x99)


# noinspection PyShadowingNames
def test_code_44(register):
    register.H = 0x99
    cycles = cpu.op.code_44(register)
    assert cycles == 4
    assert_registers(register,b=0x99,h=0x99)


# noinspection PyShadowingNames
def test_code_45(register):
    register.L = 0x99
    cycles = cpu.op.code_45(register)
    assert cycles == 4
    assert_registers(register,b=0x99,l=0x99)


# noinspection PyShadowingNames
def test_code_46(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_47(register):
    register.A = 0x99
    cycles = cpu.op.code_47(register)
    assert cycles == 4
    assert_registers(register,a=0x99,b=0x99)


# noinspection PyShadowingNames
def test_code_48(register):
    register.B = 0x99
    cycles = cpu.op.code_48(register)
    assert cycles == 4
    assert_registers(register,b=0x99,c=0x99)


# noinspection PyShadowingNames
def test_code_49(register):
    register.C = 0x99
    cycles = cpu.op.code_49(register)
    assert cycles == 4
    assert_registers(register,c=0x99)


# noinspection PyShadowingNames
def test_code_4a(register):
    register.D = 0x99
    cycles = cpu.op.code_4a(register)
    assert cycles == 4
    assert_registers(register,c=0x99,d=0x99)


# noinspection PyShadowingNames
def test_code_4b(register):
    register.E = 0x99
    cycles = cpu.op.code_4b(register)
    assert cycles == 4
    assert_registers(register,c=0x99,e=0x99)


# noinspection PyShadowingNames
def test_code_4c(register):
    register.H = 0x99
    cycles = cpu.op.code_4c(register)
    assert cycles == 4
    assert_registers(register,c=0x99,h=0x99)


# noinspection PyShadowingNames
def test_code_4d(register):
    register.L = 0x99
    cycles = cpu.op.code_4d(register)
    assert cycles == 4
    assert_registers(register,c=0x99,l=0x99)


# noinspection PyShadowingNames
def test_code_4e(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_4f(register):
    register.A = 0x99
    cycles = cpu.op.code_4f(register)
    assert cycles == 4
    assert_registers(register,a=0x99,c=0x99)


# noinspection PyShadowingNames
def test_code_50(register):
    register.B = 0x99
    cycles = cpu.op.code_50(register)
    assert cycles == 4
    assert_registers(register,b=0x99,d=0x99)


# noinspection PyShadowingNames
def test_code_51(register):
    register.C = 0x99
    cycles = cpu.op.code_51(register)
    assert cycles == 4
    assert_registers(register,c=0x99,d=0x99)


# noinspection PyShadowingNames
def test_code_52(register):
    register.D = 0x99
    cycles = cpu.op.code_52(register)
    assert cycles == 4
    assert_registers(register,d=0x99)


# noinspection PyShadowingNames
def test_code_53(register):
    register.E = 0x99
    cycles = cpu.op.code_53(register)
    assert cycles == 4
    assert_registers(register,d=0x99,e=0x99)


# noinspection PyShadowingNames
def test_code_54(register):
    register.H = 0x99
    cycles = cpu.op.code_54(register)
    assert cycles == 4
    assert_registers(register,d=0x99,h=0x99)


# noinspection PyShadowingNames
def test_code_55(register):
    register.L = 0x99
    cycles = cpu.op.code_55(register)
    assert cycles == 4
    assert_registers(register,d=0x99,l=0x99)


# noinspection PyShadowingNames
def test_code_56(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_57(register):
    register.A = 0x99
    cycles = cpu.op.code_57(register)
    assert cycles == 4
    assert_registers(register,a=0x99,d=0x99)


# noinspection PyShadowingNames
def test_code_58(register):
    register.B = 0x99
    cycles = cpu.op.code_58(register)
    assert cycles == 4
    assert_registers(register,b=0x99,e=0x99)


# noinspection PyShadowingNames
def test_code_59(register):
    register.C = 0x99
    cycles = cpu.op.code_59(register)
    assert cycles == 4
    assert_registers(register,c=0x99,e=0x99)


# noinspection PyShadowingNames
def test_code_5a(register):
    register.D = 0x99
    cycles = cpu.op.code_5a(register)
    assert cycles == 4
    assert_registers(register,d=0x99,e=0x99)


# noinspection PyShadowingNames
def test_code_5b(register):
    register.E = 0x99
    cycles = cpu.op.code_5b(register)
    assert cycles == 4
    assert_registers(register,e=0x99)


# noinspection PyShadowingNames
def test_code_5c(register):
    register.H = 0x99
    cycles = cpu.op.code_5c(register)
    assert cycles == 4
    assert_registers(register,e=0x99,h=0x99)


# noinspection PyShadowingNames
def test_code_5d(register):
    register.L = 0x99
    cycles = cpu.op.code_5d(register)
    assert cycles == 4
    assert_registers(register,e=0x99,l=0x99)


# noinspection PyShadowingNames
def test_code_5e(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_5f(register):
    register.A = 0x99
    cycles = cpu.op.code_5f(register)
    assert cycles == 4
    assert_registers(register,a=0x99,e=0x99)


# noinspection PyShadowingNames
def test_code_60(register):
    register.B = 0x99
    cycles = cpu.op.code_60(register)
    assert cycles == 4
    assert_registers(register, b=0x99, h=0x99)


# noinspection PyShadowingNames
def test_code_61(register):
    register.C = 0x99
    cycles = cpu.op.code_61(register)
    assert cycles == 4
    assert_registers(register, c=0x99, h=0x99)


# noinspection PyShadowingNames
def test_code_62(register):
    register.D = 0x99
    cycles = cpu.op.code_62(register)
    assert cycles == 4
    assert_registers(register, d=0x99, h=0x99)


# noinspection PyShadowingNames
def test_code_63(register):
    register.E = 0x99
    cycles = cpu.op.code_63(register)
    assert cycles == 4
    assert_registers(register, e=0x99, h=0x99)


# noinspection PyShadowingNames
def test_code_64(register):
    register.H = 0x99
    cycles = cpu.op.code_64(register)
    assert cycles == 4
    assert_registers(register, h=0x99)


# noinspection PyShadowingNames
def test_code_65(register):
    register.L = 0x99
    cycles = cpu.op.code_65(register)
    assert cycles == 4
    assert_registers(register, h=0x99, l=0x99)


# noinspection PyShadowingNames
def test_code_66(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_67(register):
    register.A = 0x99
    cycles = cpu.op.code_67(register)
    assert cycles == 4
    assert_registers(register, a=0x99, h=0x99)


# noinspection PyShadowingNames
def test_code_68(register):
    register.B = 0x99
    cycles = cpu.op.code_68(register)
    assert cycles == 4
    assert_registers(register, b=0x99, l=0x99)


# noinspection PyShadowingNames
def test_code_69(register):
    register.C = 0x99
    cycles = cpu.op.code_69(register)
    assert cycles == 4
    assert_registers(register, c=0x99, l=0x99)


# noinspection PyShadowingNames
def test_code_6a(register):
    register.D = 0x99
    cycles = cpu.op.code_6a(register)
    assert cycles == 4
    assert_registers(register, d=0x99, l=0x99)


# noinspection PyShadowingNames
def test_code_6b(register):
    register.E = 0x99
    cycles = cpu.op.code_6b(register)
    assert cycles == 4
    assert_registers(register, e=0x99, l=0x99)


# noinspection PyShadowingNames
def test_code_6c(register):
    register.H = 0x99
    cycles = cpu.op.code_6c(register)
    assert cycles == 4
    assert_registers(register, h=0x99, l=0x99)


# noinspection PyShadowingNames
def test_code_6d(register):
    register.L = 0x99
    cycles = cpu.op.code_6d(register)
    assert cycles == 4
    assert_registers(register, l=0x99)


# noinspection PyShadowingNames
def test_code_6e(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_6f(register):
    register.A = 0x99
    cycles = cpu.op.code_6f(register)
    assert cycles == 4
    assert_registers(register, a=0x99, l=0x99)


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
    cycles = cpu.op.code_78(register)
    assert cycles == 4
    assert_registers(register, a=0x99, b=0x99)


# noinspection PyShadowingNames
def test_code_79(register):
    register.C = 0x99
    cycles = cpu.op.code_79(register)
    assert cycles == 4
    assert_registers(register, a=0x99, c=0x99)


# noinspection PyShadowingNames
def test_code_7a(register):
    register.D = 0x99
    cycles = cpu.op.code_7a(register)
    assert cycles == 4
    assert_registers(register, a=0x99, d=0x99)


# noinspection PyShadowingNames
def test_code_7b(register):
    register.E = 0x99
    cycles = cpu.op.code_7b(register)
    assert cycles == 4
    assert_registers(register, a=0x99, e=0x99)


# noinspection PyShadowingNames
def test_code_7c(register):
    register.H = 0x99
    cycles = cpu.op.code_7c(register)
    assert cycles == 4
    assert_registers(register, a=0x99, h=0x99)


# noinspection PyShadowingNames
def test_code_7d(register):
    register.L = 0x99
    cycles = cpu.op.code_7d(register)
    assert cycles == 4
    assert_registers(register, a=0x99, l=0x99)


# noinspection PyShadowingNames
def test_code_7e(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_7f(register):
    register.A = 0x99
    cycles = cpu.op.code_7f(register)
    assert cycles == 4
    assert_registers(register, a=0x99)


# noinspection PyShadowingNames
def test_code_80(register):
    register.A = 0x00
    register.B = 0x00
    cycles = cpu.op.code_80(register)
    assert cycles == 4
    assert_registers(register, a=0x00, b=0x00, f=0b10000000)

    register.A = 0x00
    register.B = 0x01
    cycles = cpu.op.code_80(register)
    assert cycles == 4
    assert_registers(register, a=0x01, b=0x01, f=0b00000000)

    register.A = 0x0F
    register.B = 0x01
    cycles = cpu.op.code_80(register)
    assert cycles == 4
    assert_registers(register, a=0x10, b=0x01, f=0b00100000)

    register.A = 0xF0
    register.B = 0x10
    cycles = cpu.op.code_80(register)
    assert cycles == 4
    assert_registers(register, a=0x00, b=0x10, f=0b10010000)

    register.A = 0xFF
    register.B = 0x01
    cycles = cpu.op.code_80(register)
    assert cycles == 4
    assert_registers(register, a=0x00, b=0x01, f=0b10110000)

    register.A = 0xFF
    register.B = 0x02
    cycles = cpu.op.code_80(register)
    assert cycles == 4
    assert_registers(register, a=0x01, b=0x02, f=0b00110000)


# noinspection PyShadowingNames
def test_code_81(register):
    register.A = 0x00
    register.C = 0x00
    cycles = cpu.op.code_81(register)
    assert cycles == 4
    assert_registers(register, a=0x00, c=0x00, f=0b10000000)

    register.A = 0x00
    register.C = 0x01
    cycles = cpu.op.code_81(register)
    assert cycles == 4
    assert_registers(register, a=0x01, c=0x01, f=0b00000000)

    register.A = 0x0F
    register.C = 0x01
    cycles = cpu.op.code_81(register)
    assert cycles == 4
    assert_registers(register, a=0x10, c=0x01, f=0b00100000)

    register.A = 0xF0
    register.C = 0x10
    cycles = cpu.op.code_81(register)
    assert cycles == 4
    assert_registers(register, a=0x00, c=0x10, f=0b10010000)

    register.A = 0xFF
    register.C = 0x01
    cycles = cpu.op.code_81(register)
    assert cycles == 4
    assert_registers(register, a=0x00, c=0x01, f=0b10110000)

    register.A = 0xFF
    register.C = 0x02
    cycles = cpu.op.code_81(register)
    assert cycles == 4
    assert_registers(register, a=0x01, c=0x02, f=0b00110000)


# noinspection PyShadowingNames
def test_code_82(register):
    register.A = 0x00
    register.D = 0x00
    cycles = cpu.op.code_82(register)
    assert cycles == 4
    assert_registers(register, a=0x00, d=0x00, f=0b10000000)

    register.A = 0x00
    register.D = 0x01
    cycles = cpu.op.code_82(register)
    assert cycles == 4
    assert_registers(register, a=0x01, d=0x01, f=0b00000000)

    register.A = 0x0F
    register.D = 0x01
    cycles = cpu.op.code_82(register)
    assert cycles == 4
    assert_registers(register, a=0x10, d=0x01, f=0b00100000)

    register.A = 0xF0
    register.D = 0x10
    cycles = cpu.op.code_82(register)
    assert cycles == 4
    assert_registers(register, a=0x00, d=0x10, f=0b10010000)

    register.A = 0xFF
    register.D = 0x01
    cycles = cpu.op.code_82(register)
    assert cycles == 4
    assert_registers(register, a=0x00, d=0x01, f=0b10110000)

    register.A = 0xFF
    register.D = 0x02
    cycles = cpu.op.code_82(register)
    assert cycles == 4
    assert_registers(register, a=0x01, d=0x02, f=0b00110000)


# noinspection PyShadowingNames
def test_code_83(register):
    register.A = 0x00
    register.E = 0x00
    cycles = cpu.op.code_83(register)
    assert cycles == 4
    assert_registers(register, a=0x00, e=0x00, f=0b10000000)

    register.A = 0x00
    register.E = 0x01
    cycles = cpu.op.code_83(register)
    assert cycles == 4
    assert_registers(register, a=0x01, e=0x01, f=0b00000000)

    register.A = 0x0F
    register.E = 0x01
    cycles = cpu.op.code_83(register)
    assert cycles == 4
    assert_registers(register, a=0x10, e=0x01, f=0b00100000)

    register.A = 0xF0
    register.E = 0x10
    cycles = cpu.op.code_83(register)
    assert cycles == 4
    assert_registers(register, a=0x00, e=0x10, f=0b10010000)

    register.A = 0xFF
    register.E = 0x01
    cycles = cpu.op.code_83(register)
    assert cycles == 4
    assert_registers(register, a=0x00, e=0x01, f=0b10110000)

    register.A = 0xFF
    register.E = 0x02
    cycles = cpu.op.code_83(register)
    assert cycles == 4
    assert_registers(register, a=0x01, e=0x02, f=0b00110000)


# noinspection PyShadowingNames
def test_code_84(register):
    register.A = 0x00
    register.H = 0x00
    cycles = cpu.op.code_84(register)
    assert cycles == 4
    assert_registers(register, a=0x00, h=0x00, f=0b10000000)

    register.A = 0x00
    register.H = 0x01
    cycles = cpu.op.code_84(register)
    assert cycles == 4
    assert_registers(register, a=0x01, h=0x01, f=0b00000000)

    register.A = 0x0F
    register.H = 0x01
    cycles = cpu.op.code_84(register)
    assert cycles == 4
    assert_registers(register, a=0x10, h=0x01, f=0b00100000)

    register.A = 0xF0
    register.H = 0x10
    cycles = cpu.op.code_84(register)
    assert cycles == 4
    assert_registers(register, a=0x00, h=0x10, f=0b10010000)

    register.A = 0xFF
    register.H = 0x01
    cycles = cpu.op.code_84(register)
    assert cycles == 4
    assert_registers(register, a=0x00, h=0x01, f=0b10110000)

    register.A = 0xFF
    register.H = 0x02
    cycles = cpu.op.code_84(register)
    assert cycles == 4
    assert_registers(register, a=0x01, h=0x02, f=0b00110000)


# noinspection PyShadowingNames
def test_code_85(register):
    register.A = 0x00
    register.L = 0x00
    cycles = cpu.op.code_85(register)
    assert cycles == 4
    assert_registers(register, a=0x00, l=0x00, f=0b10000000)

    register.A = 0x00
    register.L = 0x01
    cycles = cpu.op.code_85(register)
    assert cycles == 4
    assert_registers(register, a=0x01, l=0x01, f=0b00000000)

    register.A = 0x0F
    register.L = 0x01
    cycles = cpu.op.code_85(register)
    assert cycles == 4
    assert_registers(register, a=0x10, l=0x01, f=0b00100000)

    register.A = 0xF0
    register.L = 0x10
    cycles = cpu.op.code_85(register)
    assert cycles == 4
    assert_registers(register, a=0x00, l=0x10, f=0b10010000)

    register.A = 0xFF
    register.L = 0x01
    cycles = cpu.op.code_85(register)
    assert cycles == 4
    assert_registers(register, a=0x00, l=0x01, f=0b10110000)

    register.A = 0xFF
    register.L = 0x02
    cycles = cpu.op.code_85(register)
    assert cycles == 4
    assert_registers(register, a=0x01, l=0x02, f=0b00110000)


# noinspection PyShadowingNames
def test_code_86(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_87(register):
    register.A = 0x00
    cycles = cpu.op.code_87(register)
    assert cycles == 4
    assert_registers(register, a=0x00, f=0b10000000)

    register.A = 0x01
    cycles = cpu.op.code_87(register)
    assert cycles == 4
    assert_registers(register, a=0x02, f=0b00000000)

    register.A = 0x08
    cycles = cpu.op.code_87(register)
    assert cycles == 4
    assert_registers(register, a=0x10, f=0b00100000)

    register.A = 0x80
    cycles = cpu.op.code_87(register)
    assert cycles == 4
    assert_registers(register, a=0x00, f=0b10010000)

    register.A = 0x88
    cycles = cpu.op.code_87(register)
    assert cycles == 4
    assert_registers(register, a=0x10, f=0b00110000)


# noinspection PyShadowingNames
def test_code_88(register):
    register.A = 0x00
    register.B = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_88(register)
    assert cycles == 4
    assert_registers(register, a=0x00, b=0x00, f=0b10000000)

    register.A = 0x00
    register.B = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_88(register)
    assert cycles == 4
    assert_registers(register, a=0x01, b=0x00, f=0b00000000)

    register.A = 0x00
    register.B = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_88(register)
    assert cycles == 4
    assert_registers(register, a=0x02, b=0x01, f=0b00000000)

    register.A = 0x0E
    register.B = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_88(register)
    assert cycles == 4
    assert_registers(register, a=0x10, b=0x01, f=0b00100000)

    register.A = 0xF0
    register.B = 0x0F
    register.F = 0b00010000
    cycles = cpu.op.code_88(register)
    assert cycles == 4
    assert_registers(register, a=0x00, b=0x0F, f=0b10110000)

    register.A = 0xFE
    register.B = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_88(register)
    assert cycles == 4
    assert_registers(register, a=0x00, b=0x01, f=0b10110000)

    register.A = 0xFE
    register.B = 0x02
    register.F = 0b00010000
    cycles = cpu.op.code_88(register)
    assert cycles == 4
    assert_registers(register, a=0x01, b=0x02, f=0b00110000)


# noinspection PyShadowingNames
def test_code_89(register):
    register.A = 0x00
    register.C = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_89(register)
    assert cycles == 4
    assert_registers(register, a=0x00, c=0x00, f=0b10000000)

    register.A = 0x00
    register.C = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_89(register)
    assert cycles == 4
    assert_registers(register, a=0x01, c=0x00, f=0b00000000)

    register.A = 0x00
    register.C = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_89(register)
    assert cycles == 4
    assert_registers(register, a=0x02, c=0x01, f=0b00000000)

    register.A = 0x0E
    register.C = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_89(register)
    assert cycles == 4
    assert_registers(register, a=0x10, c=0x01, f=0b00100000)

    register.A = 0xF0
    register.C = 0x0F
    register.F = 0b00010000
    cycles = cpu.op.code_89(register)
    assert cycles == 4
    assert_registers(register, a=0x00, c=0x0F, f=0b10110000)

    register.A = 0xFE
    register.C = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_89(register)
    assert cycles == 4
    assert_registers(register, a=0x00, c=0x01, f=0b10110000)

    register.A = 0xFE
    register.C = 0x02
    register.F = 0b00010000
    cycles = cpu.op.code_89(register)
    assert cycles == 4
    assert_registers(register, a=0x01, c=0x02, f=0b00110000)


# noinspection PyShadowingNames
def test_code_8a(register):
    register.A = 0x00
    register.D = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_8a(register)
    assert cycles == 4
    assert_registers(register, a=0x00, d=0x00, f=0b10000000)

    register.A = 0x00
    register.D = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_8a(register)
    assert cycles == 4
    assert_registers(register, a=0x01, d=0x00, f=0b00000000)

    register.A = 0x00
    register.D = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_8a(register)
    assert cycles == 4
    assert_registers(register, a=0x02, d=0x01, f=0b00000000)

    register.A = 0x0E
    register.D = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_8a(register)
    assert cycles == 4
    assert_registers(register, a=0x10, d=0x01, f=0b00100000)

    register.A = 0xF0
    register.D = 0x0F
    register.F = 0b00010000
    cycles = cpu.op.code_8a(register)
    assert cycles == 4
    assert_registers(register, a=0x00, d=0x0F, f=0b10110000)

    register.A = 0xFE
    register.D = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_8a(register)
    assert cycles == 4
    assert_registers(register, a=0x00, d=0x01, f=0b10110000)

    register.A = 0xFE
    register.D = 0x02
    register.F = 0b00010000
    cycles = cpu.op.code_8a(register)
    assert cycles == 4
    assert_registers(register, a=0x01, d=0x02, f=0b00110000)


# noinspection PyShadowingNames
def test_code_8b(register):
    register.A = 0x00
    register.E = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_8b(register)
    assert cycles == 4
    assert_registers(register, a=0x00, e=0x00, f=0b10000000)

    register.A = 0x00
    register.E = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_8b(register)
    assert cycles == 4
    assert_registers(register, a=0x01, e=0x00, f=0b00000000)

    register.A = 0x00
    register.E = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_8b(register)
    assert cycles == 4
    assert_registers(register, a=0x02, e=0x01, f=0b00000000)

    register.A = 0x0E
    register.E = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_8b(register)
    assert cycles == 4
    assert_registers(register, a=0x10, e=0x01, f=0b00100000)

    register.A = 0xF0
    register.E = 0x0F
    register.F = 0b00010000
    cycles = cpu.op.code_8b(register)
    assert cycles == 4
    assert_registers(register, a=0x00, e=0x0F, f=0b10110000)

    register.A = 0xFE
    register.E = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_8b(register)
    assert cycles == 4
    assert_registers(register, a=0x00, e=0x01, f=0b10110000)

    register.A = 0xFE
    register.E = 0x02
    register.F = 0b00010000
    cycles = cpu.op.code_8b(register)
    assert cycles == 4
    assert_registers(register, a=0x01, e=0x02, f=0b00110000)


# noinspection PyShadowingNames
def test_code_8c(register):
    register.A = 0x00
    register.H = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_8c(register)
    assert cycles == 4
    assert_registers(register, a=0x00, h=0x00, f=0b10000000)

    register.A = 0x00
    register.H = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_8c(register)
    assert cycles == 4
    assert_registers(register, a=0x01, h=0x00, f=0b00000000)

    register.A = 0x00
    register.H = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_8c(register)
    assert cycles == 4
    assert_registers(register, a=0x02, h=0x01, f=0b00000000)

    register.A = 0x0E
    register.H = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_8c(register)
    assert cycles == 4
    assert_registers(register, a=0x10, h=0x01, f=0b00100000)

    register.A = 0xF0
    register.H = 0x0F
    register.F = 0b00010000
    cycles = cpu.op.code_8c(register)
    assert cycles == 4
    assert_registers(register, a=0x00, h=0x0F, f=0b10110000)

    register.A = 0xFE
    register.H = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_8c(register)
    assert cycles == 4
    assert_registers(register, a=0x00, h=0x01, f=0b10110000)

    register.A = 0xFE
    register.H = 0x02
    register.F = 0b00010000
    cycles = cpu.op.code_8c(register)
    assert cycles == 4
    assert_registers(register, a=0x01, h=0x02, f=0b00110000)


# noinspection PyShadowingNames
def test_code_8d(register):
    register.A = 0x00
    register.L = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_8d(register)
    assert cycles == 4
    assert_registers(register, a=0x00, l=0x00, f=0b10000000)

    register.A = 0x00
    register.L = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_8d(register)
    assert cycles == 4
    assert_registers(register, a=0x01, l=0x00, f=0b00000000)

    register.A = 0x00
    register.L = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_8d(register)
    assert cycles == 4
    assert_registers(register, a=0x02, l=0x01, f=0b00000000)

    register.A = 0x0E
    register.L = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_8d(register)
    assert cycles == 4
    assert_registers(register, a=0x10, l=0x01, f=0b00100000)

    register.A = 0xF0
    register.L = 0x0F
    register.F = 0b00010000
    cycles = cpu.op.code_8d(register)
    assert cycles == 4
    assert_registers(register, a=0x00, l=0x0F, f=0b10110000)

    register.A = 0xFE
    register.L = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_8d(register)
    assert cycles == 4
    assert_registers(register, a=0x00, l=0x01, f=0b10110000)

    register.A = 0xFE
    register.L = 0x02
    register.F = 0b00010000
    cycles = cpu.op.code_8d(register)
    assert cycles == 4
    assert_registers(register, a=0x01, l=0x02, f=0b00110000)


# noinspection PyShadowingNames
def test_code_8e(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_8f(register):
    register.A = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_8f(register)
    assert cycles == 4
    assert_registers(register, a=0x00, f=0b10000000)

    register.A = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_8f(register)
    assert cycles == 4
    assert_registers(register, a=0x01, f=0b00000000)

    register.A = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_8f(register)
    assert cycles == 4
    assert_registers(register, a=0x03, f=0b00000000)

    register.A = 0x08
    register.F = 0b00010000
    cycles = cpu.op.code_8f(register)
    assert cycles == 4
    assert_registers(register, a=0x11, f=0b00100000)

    register.A = 0x80
    register.F = 0b00000000
    cycles = cpu.op.code_8f(register)
    assert cycles == 4
    assert_registers(register, a=0x00, f=0b10010000)

    register.A = 0x80
    register.F = 0b00010000
    cycles = cpu.op.code_8f(register)
    assert cycles == 4
    assert_registers(register, a=0x01, f=0b00010000)

    register.A = 0xFF
    register.F = 0b00010000
    cycles = cpu.op.code_8f(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, f=0b00110000)


# noinspection PyShadowingNames
def test_code_90(register):
    register.A = 0x00
    register.B = 0x00
    cycles = cpu.op.code_90(register)
    assert cycles == 4
    assert_registers(register, a=0x00, b=0x00, f=0b11000000)

    register.A = 0x00
    register.B = 0x01
    cycles = cpu.op.code_90(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, b=0x01, f=0b01110000)

    register.A = 0x0F
    register.B = 0x01
    cycles = cpu.op.code_90(register)
    assert cycles == 4
    assert_registers(register, a=0x0E, b=0x01, f=0b01000000)

    register.A = 0xF0
    register.B = 0x10
    cycles = cpu.op.code_90(register)
    assert cycles == 4
    assert_registers(register, a=0xE0, b=0x10, f=0b01000000)

    register.A = 0xFF
    register.B = 0x01
    cycles = cpu.op.code_90(register)
    assert cycles == 4
    assert_registers(register, a=0xFE, b=0x01, f=0b01000000)

    register.A = 0xFF
    register.B = 0xFE
    cycles = cpu.op.code_90(register)
    assert cycles == 4
    assert_registers(register, a=0x01, b=0xFE, f=0b01000000)


# noinspection PyShadowingNames
def test_code_91(register):
    register.A = 0x00
    register.C = 0x00
    cycles = cpu.op.code_91(register)
    assert cycles == 4
    assert_registers(register, a=0x00, c=0x00, f=0b11000000)

    register.A = 0x00
    register.C = 0x01
    cycles = cpu.op.code_91(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, c=0x01, f=0b01110000)

    register.A = 0x0F
    register.C = 0x01
    cycles = cpu.op.code_91(register)
    assert cycles == 4
    assert_registers(register, a=0x0E, c=0x01, f=0b01000000)

    register.A = 0xF0
    register.C = 0x10
    cycles = cpu.op.code_91(register)
    assert cycles == 4
    assert_registers(register, a=0xE0, c=0x10, f=0b01000000)

    register.A = 0xFF
    register.C = 0x01
    cycles = cpu.op.code_91(register)
    assert cycles == 4
    assert_registers(register, a=0xFE, c=0x01, f=0b01000000)

    register.A = 0xFF
    register.C = 0xFE
    cycles = cpu.op.code_91(register)
    assert cycles == 4
    assert_registers(register, a=0x01, c=0xFE, f=0b01000000)


# noinspection PyShadowingNames
def test_code_92(register):
    register.A = 0x00
    register.D = 0x00
    cycles = cpu.op.code_92(register)
    assert cycles == 4
    assert_registers(register, a=0x00, d=0x00, f=0b11000000)

    register.A = 0x00
    register.D = 0x01
    cycles = cpu.op.code_92(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, d=0x01, f=0b01110000)

    register.A = 0x0F
    register.D = 0x01
    cycles = cpu.op.code_92(register)
    assert cycles == 4
    assert_registers(register, a=0x0E, d=0x01, f=0b01000000)

    register.A = 0xF0
    register.D = 0x10
    cycles = cpu.op.code_92(register)
    assert cycles == 4
    assert_registers(register, a=0xE0, d=0x10, f=0b01000000)

    register.A = 0xFF
    register.D = 0x01
    cycles = cpu.op.code_92(register)
    assert cycles == 4
    assert_registers(register, a=0xFE, d=0x01, f=0b01000000)

    register.A = 0xFF
    register.D = 0xFE
    cycles = cpu.op.code_92(register)
    assert cycles == 4
    assert_registers(register, a=0x01, d=0xFE, f=0b01000000)


# noinspection PyShadowingNames
def test_code_93(register):
    register.A = 0x00
    register.E = 0x00
    cycles = cpu.op.code_93(register)
    assert cycles == 4
    assert_registers(register, a=0x00, e=0x00, f=0b11000000)

    register.A = 0x00
    register.E = 0x01
    cycles = cpu.op.code_93(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, e=0x01, f=0b01110000)

    register.A = 0x0F
    register.E = 0x01
    cycles = cpu.op.code_93(register)
    assert cycles == 4
    assert_registers(register, a=0x0E, e=0x01, f=0b01000000)

    register.A = 0xF0
    register.E = 0x10
    cycles = cpu.op.code_93(register)
    assert cycles == 4
    assert_registers(register, a=0xE0, e=0x10, f=0b01000000)

    register.A = 0xFF
    register.E = 0x01
    cycles = cpu.op.code_93(register)
    assert cycles == 4
    assert_registers(register, a=0xFE, e=0x01, f=0b01000000)

    register.A = 0xFF
    register.E = 0xFE
    cycles = cpu.op.code_93(register)
    assert cycles == 4
    assert_registers(register, a=0x01, e=0xFE, f=0b01000000)


# noinspection PyShadowingNames
def test_code_94(register):
    register.A = 0x00
    register.H = 0x00
    cycles = cpu.op.code_94(register)
    assert cycles == 4
    assert_registers(register, a=0x00, h=0x00, f=0b11000000)

    register.A = 0x00
    register.H = 0x01
    cycles = cpu.op.code_94(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, h=0x01, f=0b01110000)

    register.A = 0x0F
    register.H = 0x01
    cycles = cpu.op.code_94(register)
    assert cycles == 4
    assert_registers(register, a=0x0E, h=0x01, f=0b01000000)

    register.A = 0xF0
    register.H = 0x10
    cycles = cpu.op.code_94(register)
    assert cycles == 4
    assert_registers(register, a=0xE0, h=0x10, f=0b01000000)

    register.A = 0xFF
    register.H = 0x01
    cycles = cpu.op.code_94(register)
    assert cycles == 4
    assert_registers(register, a=0xFE, h=0x01, f=0b01000000)

    register.A = 0xFF
    register.H = 0xFE
    cycles = cpu.op.code_94(register)
    assert cycles == 4
    assert_registers(register, a=0x01, h=0xFE, f=0b01000000)


# noinspection PyShadowingNames
def test_code_95(register):
    register.A = 0x00
    register.L = 0x00
    cycles = cpu.op.code_95(register)
    assert cycles == 4
    assert_registers(register, a=0x00, l=0x00, f=0b11000000)

    register.A = 0x00
    register.L = 0x01
    cycles = cpu.op.code_95(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, l=0x01, f=0b01110000)

    register.A = 0x0F
    register.L = 0x01
    cycles = cpu.op.code_95(register)
    assert cycles == 4
    assert_registers(register, a=0x0E, l=0x01, f=0b01000000)

    register.A = 0xF0
    register.L = 0x10
    cycles = cpu.op.code_95(register)
    assert cycles == 4
    assert_registers(register, a=0xE0, l=0x10, f=0b01000000)

    register.A = 0xFF
    register.L = 0x01
    cycles = cpu.op.code_95(register)
    assert cycles == 4
    assert_registers(register, a=0xFE, l=0x01, f=0b01000000)

    register.A = 0xFF
    register.L = 0xFE
    cycles = cpu.op.code_95(register)
    assert cycles == 4
    assert_registers(register, a=0x01, l=0xFE, f=0b01000000)


# noinspection PyShadowingNames
def test_code_96(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_97(register):
    register.A = 0x00
    cycles = cpu.op.code_97(register)
    assert cycles == 4
    assert_registers(register, a=0x00, f=0b11000000)

    register.A = 0x01
    cycles = cpu.op.code_97(register)
    assert cycles == 4
    assert_registers(register, a=0x00, f=0b11000000)

    register.A = 0xFF
    cycles = cpu.op.code_97(register)
    assert cycles == 4
    assert_registers(register, a=0x00, f=0b11000000)


# noinspection PyShadowingNames
def test_code_98(register):
    register.A = 0x00
    register.B = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_98(register)
    assert cycles == 4
    assert_registers(register, a=0x00, b=0x00, f=0b11000000)

    register.A = 0x02
    register.B = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_98(register)
    assert cycles == 4
    assert_registers(register, a=0x01, b=0x00, f=0b01000000)

    register.A = 0x00
    register.B = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_98(register)
    assert cycles == 4
    assert_registers(register, a=0xFE, b=0x01, f=0b01110000)

    register.A = 0x13
    register.B = 0x04
    register.F = 0b00010000
    cycles = cpu.op.code_98(register)
    assert cycles == 4
    assert_registers(register, a=0x0E, b=0x04, f=0b01100000)


# noinspection PyShadowingNames
def test_code_99(register):
    register.A = 0x00
    register.C = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_99(register)
    assert cycles == 4
    assert_registers(register, a=0x00, c=0x00, f=0b11000000)

    register.A = 0x02
    register.C = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_99(register)
    assert cycles == 4
    assert_registers(register, a=0x01, c=0x00, f=0b01000000)

    register.A = 0x00
    register.C = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_99(register)
    assert cycles == 4
    assert_registers(register, a=0xFE, c=0x01, f=0b01110000)

    register.A = 0x13
    register.C = 0x04
    register.F = 0b00010000
    cycles = cpu.op.code_99(register)
    assert cycles == 4
    assert_registers(register, a=0x0E, c=0x04, f=0b01100000)


# noinspection PyShadowingNames
def test_code_9a(register):
    register.A = 0x00
    register.D = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_9a(register)
    assert cycles == 4
    assert_registers(register, a=0x00, d=0x00, f=0b11000000)

    register.A = 0x02
    register.D = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_9a(register)
    assert cycles == 4
    assert_registers(register, a=0x01, d=0x00, f=0b01000000)

    register.A = 0x00
    register.D = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_9a(register)
    assert cycles == 4
    assert_registers(register, a=0xFE, d=0x01, f=0b01110000)

    register.A = 0x13
    register.D = 0x04
    register.F = 0b00010000
    cycles = cpu.op.code_9a(register)
    assert cycles == 4
    assert_registers(register, a=0x0E, d=0x04, f=0b01100000)


# noinspection PyShadowingNames
def test_code_9b(register):
    register.A = 0x00
    register.E = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_9b(register)
    assert cycles == 4
    assert_registers(register, a=0x00, e=0x00, f=0b11000000)

    register.A = 0x02
    register.E = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_9b(register)
    assert cycles == 4
    assert_registers(register, a=0x01, e=0x00, f=0b01000000)

    register.A = 0x00
    register.E = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_9b(register)
    assert cycles == 4
    assert_registers(register, a=0xFE, e=0x01, f=0b01110000)

    register.A = 0x13
    register.E = 0x04
    register.F = 0b00010000
    cycles = cpu.op.code_9b(register)
    assert cycles == 4
    assert_registers(register, a=0x0E, e=0x04, f=0b01100000)


# noinspection PyShadowingNames
def test_code_9c(register):
    register.A = 0x00
    register.H = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_9c(register)
    assert cycles == 4
    assert_registers(register, a=0x00, h=0x00, f=0b11000000)

    register.A = 0x02
    register.H = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_9c(register)
    assert cycles == 4
    assert_registers(register, a=0x01, h=0x00, f=0b01000000)

    register.A = 0x00
    register.H = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_9c(register)
    assert cycles == 4
    assert_registers(register, a=0xFE, h=0x01, f=0b01110000)

    register.A = 0x13
    register.H = 0x04
    register.F = 0b00010000
    cycles = cpu.op.code_9c(register)
    assert cycles == 4
    assert_registers(register, a=0x0E, h=0x04, f=0b01100000)


# noinspection PyShadowingNames
def test_code_9d(register):
    register.A = 0x00
    register.L = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_9d(register)
    assert cycles == 4
    assert_registers(register, a=0x00, l=0x00, f=0b11000000)

    register.A = 0x02
    register.L = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_9d(register)
    assert cycles == 4
    assert_registers(register, a=0x01, l=0x00, f=0b01000000)

    register.A = 0x00
    register.L = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_9d(register)
    assert cycles == 4
    assert_registers(register, a=0xFE, l=0x01, f=0b01110000)

    register.A = 0x13
    register.L = 0x04
    register.F = 0b00010000
    cycles = cpu.op.code_9d(register)
    assert cycles == 4
    assert_registers(register, a=0x0E, l=0x04, f=0b01100000)


# noinspection PyShadowingNames
def test_code_9e(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_9f(register):
    register.A = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_9f(register)
    assert cycles == 4
    assert_registers(register, a=0x00, f=0b11000000)

    register.A = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_9f(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, f=0b01110000)

    register.A = 0xFF
    register.F = 0b00010000
    cycles = cpu.op.code_9f(register)
    assert cycles == 4
    assert_registers(register, a=0xFF, f=0b01110000)


# noinspection PyShadowingNames
def test_code_c1(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_c5(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_c6(register):
    register.A = 0x00
    d8 = 0x00
    cycles = cpu.op.code_c6(register, d8)
    assert cycles == 8
    assert_registers(register, a=0x00, f=0b10000000)

    register.A = 0x00
    d8 = 0x01
    cycles = cpu.op.code_c6(register, d8)
    assert cycles == 8
    assert_registers(register, a=0x01, f=0b00000000)

    register.A = 0x0F
    d8 = 0x01
    cycles = cpu.op.code_c6(register, d8)
    assert cycles == 8
    assert_registers(register, a=0x10, f=0b00100000)

    register.A = 0xF0
    d8 = 0x10
    cycles = cpu.op.code_c6(register, d8)
    assert cycles == 8
    assert_registers(register, a=0x00, f=0b10010000)

    register.A = 0xFF
    d8 = 0x01
    cycles = cpu.op.code_c6(register, d8)
    assert cycles == 8
    assert_registers(register, a=0x00, f=0b10110000)

    register.A = 0xFF
    d8 = 0x02
    cycles = cpu.op.code_c6(register, d8)
    assert cycles == 8
    assert_registers(register, a=0x01, f=0b00110000)


# noinspection PyShadowingNames
def test_code_ce(register):
    register.A = 0x00
    d8 = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_ce(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x00, f=0b10000000)

    register.A = 0x00
    d8 = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_ce(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x01, f=0b00000000)

    register.A = 0x00
    d8 = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_ce(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x02, f=0b00000000)

    register.A = 0x0E
    d8 = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_ce(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x10, f=0b00100000)

    register.A = 0xF0
    d8 = 0x0F
    register.F = 0b00010000
    cycles = cpu.op.code_ce(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x00, f=0b10110000)

    register.A = 0xFE
    d8 = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_ce(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x00, f=0b10110000)

    register.A = 0xFE
    d8 = 0x02
    register.F = 0b00010000
    cycles = cpu.op.code_ce(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x01, f=0b00110000)


# noinspection PyShadowingNames
def test_code_d1(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_d5(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_d6(register):
    register.A = 0x00
    d8 = 0x00
    cycles = cpu.op.code_d6(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x00, f=0b11000000)

    register.A = 0x00
    d8 = 0x01
    cycles = cpu.op.code_d6(register,d8)
    assert cycles == 8
    assert_registers(register, a=0xFF, f=0b01110000)

    register.A = 0x0F
    d8 = 0x01
    cycles = cpu.op.code_d6(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x0E, f=0b01000000)

    register.A = 0xF0
    d8 = 0x10
    cycles = cpu.op.code_d6(register,d8)
    assert cycles == 8
    assert_registers(register, a=0xE0, f=0b01000000)

    register.A = 0xFF
    d8 = 0x01
    cycles = cpu.op.code_d6(register,d8)
    assert cycles == 8
    assert_registers(register, a=0xFE, f=0b01000000)

    register.A = 0xFF
    d8 = 0xFE
    cycles = cpu.op.code_d6(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x01, f=0b01000000)


# noinspection PyShadowingNames
def test_code_de(register):
    register.A = 0x00
    d8 = 0x00
    register.F = 0b00000000
    cycles = cpu.op.code_de(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x00, f=0b11000000)

    register.A = 0x02
    d8 = 0x00
    register.F = 0b00010000
    cycles = cpu.op.code_de(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x01, f=0b01000000)

    register.A = 0x00
    d8 = 0x01
    register.F = 0b00010000
    cycles = cpu.op.code_de(register,d8)
    assert cycles == 8
    assert_registers(register, a=0xFE, f=0b01110000)

    register.A = 0x13
    d8 = 0x04
    register.F = 0b00010000
    cycles = cpu.op.code_de(register,d8)
    assert cycles == 8
    assert_registers(register, a=0x0E, f=0b01100000)


# noinspection PyShadowingNames
def test_code_e0(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_e1(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_e2(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_e5(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_ea(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_f0(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_f1(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_f2(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_f5(register):
    # TODO after memory is implemented
    pass


# noinspection PyShadowingNames
def test_code_f8(register):
    register.SP = 0x0000
    cycles = cpu.op.code_f8(register, 0x0F)
    assert cycles == 12
    assert_registers(register, h=0x00, l=0x0F, sp=0x0000, f=0b00000000)

    register.SP = 0x0101
    cycles = cpu.op.code_f8(register, 0x7F)
    assert cycles == 12
    assert_registers(register, h=0x01, l=0x80, sp=0x0101, f=0b00100000)

    register.SP = 0xFFFF
    cycles = cpu.op.code_f8(register, 0x01)
    assert cycles == 12
    assert_registers(register, h=0x00, l=0x00, sp=0xFFFF, f=0b00110000)

    register.SP = 0xFFFF
    cycles = cpu.op.code_f8(register, 0x80)  # negative value, -128
    assert cycles == 12
    assert_registers(register, h=0xFF, l=0x7F, sp=0xFFFF, f=0b00000000)


# noinspection PyShadowingNames
def test_code_f9(register):
    register.set_hl(0x9933)
    cycles = cpu.op.code_f9(register)
    assert cycles == 8
    assert_registers(register, h=0x99, l=0x33, sp=0x9933)


# noinspection PyShadowingNames
def test_code_fa(register):
    # TODO after memory is implemented
    pass
