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
    mem = Memory()
    mem.load_cartridge(cartridge_data=bytes.fromhex("00")*0x8000)
    return mem


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
    if custom_address is None:
        custom_address = {}

    if memory.boot_rom_loaded:
        for i in range(0x0000,len(memory.boot_rom)+1):
            custom_address.setdefault(i, memory.boot_rom[i])
    else:
        custom_address.setdefault(0xFF05, 0x00)  # TIMA
        custom_address.setdefault(0xFF06, 0x00)  # TMA
        custom_address.setdefault(0xFF07, 0x00)  # TAC
        custom_address.setdefault(0xFF10, 0x80)  # NR10
        custom_address.setdefault(0xFF11, 0xBF)  # NR11
        custom_address.setdefault(0xFF12, 0xF3)  # NR12
        custom_address.setdefault(0xFF14, 0xBF)  # NR14
        custom_address.setdefault(0xFF16, 0x3F)  # NR21
        custom_address.setdefault(0xFF17, 0x00)  # NR22
        custom_address.setdefault(0xFF19, 0xBF)  # NR24
        custom_address.setdefault(0xFF1A, 0x7F)  # NR30
        custom_address.setdefault(0xFF1B, 0xFF)  # NR31
        custom_address.setdefault(0xFF1C, 0x9F)  # NR32
        custom_address.setdefault(0xFF1E, 0xBF)  # NR33
        custom_address.setdefault(0xFF20, 0xFF)  # NR41
        custom_address.setdefault(0xFF21, 0x00)  # NR42
        custom_address.setdefault(0xFF22, 0x00)  # NR43
        custom_address.setdefault(0xFF23, 0xBF)  # NR30
        custom_address.setdefault(0xFF24, 0x77)  # NR50
        custom_address.setdefault(0xFF25, 0xF3)  # NR51
        custom_address.setdefault(0xFF26, 0xF1)  # NR52
        custom_address.setdefault(0xFF40, 0x91)  # LCDC
        custom_address.setdefault(0xFF42, 0x00)  # SCY
        custom_address.setdefault(0xFF43, 0x00)  # SCX
        custom_address.setdefault(0xFF45, 0x00)  # LYC
        custom_address.setdefault(0xFF47, 0xFC)  # BGP
        custom_address.setdefault(0xFF48, 0xFF)  # 0BP0
        custom_address.setdefault(0xFF49, 0xFF)  # 0BP1
        custom_address.setdefault(0xFF50, 0x01)  # Boot ROM unmap
        custom_address.setdefault(0xFF4A, 0x00)  # WY
        custom_address.setdefault(0xFF4B, 0x00)  # WX
        custom_address.setdefault(0xFFFF, 0x00)  # IE

    for address in range(0x0000,0xFFFF + 1):
        value = memory._read(address)
        expected_value = 0
        if address in custom_address:
            expected_value = custom_address[address]

        if value != expected_value:
            print("Memory address", hex(address), "contains", hex(value), "instead of", hex(expected_value))
        assert value == expected_value


# noinspection PyShadowingNames
def test_default_initial_values(memory):
    assert_memory(memory)


# noinspection PyShadowingNames
def test_write_8bit(memory):
    memory.write_8bit(0x8010,0x55)
    assert_memory(memory,{0x8010:0x55})


# noinspection PyShadowingNames
def test_write_16bit(memory):
    memory.write_16bit(0x8010, 0x5566)
    assert_memory(memory, {0x8010: 0x66, 0x8011:0x55})


# noinspection PyShadowingNames
def test_read_8bit(memory):
    memory._write(0x8010, 0x55)
    assert memory.read_8bit(0x8010) == 0x55


# noinspection PyShadowingNames
def test_read_16bit(memory):
    memory._write(0x8010, 0x66)
    memory._write(0x8011, 0x55)
    assert memory.read_16bit(0x8010) == 0x5566
