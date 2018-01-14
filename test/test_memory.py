"""
Tests for memory/memory.py
"""

import pytest

"""
Fixtures act as test setup/teardown in py.test.
For each test method with a parameter, the parameter name is the setup method that will be called.
"""


@pytest.fixture
def memory():
    """
    Create Memory instance for testing.
    :return: new memory instance
    """
    from memory import Memory
    return Memory()


"""
Tests
"""


# noinspection PyProtectedMember,PyShadowingNames
def assert_memory(memory, custom_address=None):
    """
    Helper function to assert memory values.
    If an address is not in the custom_address dictionary, will check for default value.
    :param memory:          Memory instance to access memory
    :param custom_address:  dict with format address:value
    """
    for address in range(0,len(memory._memory_map)):
        if custom_address is not None and address in custom_address:
            if memory._memory_map[address] != custom_address[address]:
                print("Memory address", hex(address), "contains", hex(memory._memory_map[address]),
                      "instead of",hex(custom_address[address]))
            assert memory._memory_map[address] == custom_address[address]
        else:
            if memory._memory_map[address] != 0:
                print("Memory address", hex(address), "contains", hex(memory._memory_map[address]),
                      "instead of",0)
            assert memory._memory_map[address] == 0


# noinspection PyShadowingNames
def test_default_initial_values(memory):
    assert_memory(memory)


# noinspection PyShadowingNames
def test_write_8bit(memory):
    memory.write_8bit(0x1010,0x55)
    assert_memory(memory,{0x1010:0x55})


# noinspection PyShadowingNames
def test_write_16bit(memory):
    memory.write_16bit(0x1010, 0x5566)
    assert_memory(memory, {0x1010: 0x66,0x1011:0x55})


# noinspection PyShadowingNames
def test_read_8bit(memory):
    memory._memory_map[0x1010] = 0x55
    assert memory.read_8bit(0x1010) == 0x55


# noinspection PyShadowingNames
def test_read_16bit(memory):
    memory._memory_map[0x1010] = 0x66
    memory._memory_map[0x1011] = 0x55
    assert memory.read_16bit(0x1010) == 0x5566
