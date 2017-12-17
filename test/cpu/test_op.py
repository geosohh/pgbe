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
def test_code_06(register):
    assert register.B == 0x00
    cpu.op.code_06(register,0x10)
    assert register.B == 0x10


# noinspection PyShadowingNames
def test_code_0e(register):
    assert register.C == 0x00
    cpu.op.code_0e(register,0x10)
    assert register.C == 0x10


# noinspection PyShadowingNames
def test_code_16(register):
    assert register.D == 0x00
    cpu.op.code_16(register,0x10)
    assert register.D == 0x10


# noinspection PyShadowingNames
def test_code_1e(register):
    assert register.E == 0x00
    cpu.op.code_1e(register,0x10)
    assert register.E == 0x10


# noinspection PyShadowingNames
def test_code_26(register):
    assert register.H == 0x00
    cpu.op.code_26(register,0x10)
    assert register.H == 0x10


# noinspection PyShadowingNames
def test_code_2e(register):
    assert register.L == 0x00
    cpu.op.code_2e(register,0x10)
    assert register.L == 0x10
