"""
Memory

As in the cartridge, data in memory is also stored in little endian format (i.e. least significant byte first)

See:
- https://realboyemulator.files.wordpress.com/2013/01/gbcpuman.pdf - page 8
- http://gameboy.mongenel.com/dmg/asmmemmap.html
- http://gameboy.mongenel.com/dmg/lesson5.html
- https://realboyemulator.wordpress.com/2013/01/02/the-nintendo-game-boy-part-3/
"""


import array


class Memory:
    """
    Memory
    TODO: description
    """
    def __init__(self):
        self._memory_map = self._generate_memory_map()

    @staticmethod
    def _generate_memory_map():
        """
        Generate the Game Boy memory map.
        See: https://docs.python.org/3/library/array.html
        :return:
        """
        byte_array = array.array('B')  # 'B' == "unsigned char" in C / "int" in Python, minimum size is 1 byte
        byte_array.extend((0x00,) * (0xFFFF + 1))
        return byte_array

    def write_8bit(self,address,value):
        """
        Writes the given value at the given memory address.
        :param address: Address to write
        :param value: Value to write
        """
        self._memory_map[address] = value

        # According to [https://realboyemulator.files.wordpress.com/2013/01/gbcpuman.pdf, page 9]:
        # The addresses E000-FE00 appear to access the internal RAM the same as C000-DE00. (i.e. If you write a byte to
        # address E000 it will appear at C000 and E000. Similarly, writing a byte to C000 will appear at C000 and E000.)
        if 0xE000 <= address <= 0xFE00:
            self._memory_map[address-0x2000] = value
        elif 0xC000 <= address <= 0xDE00:
            self._memory_map[address+0x2000] = value

    def write_16bit(self, address, value):
        """
        Writes 16-bit value at the given memory address. Memory is little-endian, so least significant byte goes at
        address, most significant byte goes at address+1.
        :param address: Address to write
        :param value: Value to write
        """
        lsb = value & 0x00ff
        msb = (value >> 8) & 0x00ff
        self.write_8bit(address, lsb)
        self.write_8bit(address+1, msb)

    def read_8bit(self,address):
        """
        Reads 8-bit value from the given address in the memory.
        :param address: Memory address to read data from
        :return: 8-bit value at the given memory address
        """
        return self._memory_map[address]

    @staticmethod
    def print_memory_map():
        """
        Prints the current memory map to console
        """
        for i in range(0, len(memory._memory_map), 16):
            mem_str = "0x{:04X} | ".format(i)
            for j in range(0, 16):
                mem_str += "{:02X} ".format((memory._memory_map[i + j]))
            mem_str += "|"
            print(mem_str)


if __name__ == '__main__':
    memory = Memory()
    print("Memory length =", len(memory._memory_map), "bytes")

    memory._memory_map[0xFF92] = 0xAA
    memory._memory_map[0xFF94] = 0xBB
    memory._memory_map[0xFF96] = 0xCC
    memory._memory_map[0xFF98] = 0xDD
    memory._memory_map[0xFF9a] = 0xEE
    memory._memory_map[0xFF9c] = 0xFF

    memory.print_memory_map()
    print(str(memory._memory_map[10:15]))
