"""
Memory
TODO: description
"""


import array


class Memory:
    """
    Memory
    TODO: description
    """
    def __init__(self):
        self.memory_map = self._generate_memory_map()

    @staticmethod
    def _generate_memory_map():
        """
        Generate the Game Boy memory map.
        See: https://docs.python.org/3/library/array.html
        :return:
        """
        byte_array = array.array('B')  # 'B' == "unsigned char" in C, "int" in Python, minimum size is 1 byte
        byte_array.extend((0x0000,) * (0xFFFF + 1))
        return byte_array

    @staticmethod
    def print_memory_map():
        """
        Prints the current memory map to console
        """
        for i in range(0, len(memory.memory_map), 16):
            mem_str = "0x{:04X} | ".format(i)
            for j in range(0, 16):
                mem_str += "{:02X} ".format((memory.memory_map[i + j]))
            mem_str += "|"
            print(mem_str)


if __name__ == '__main__':
    memory = Memory()
    print("Memory length =",len(memory.memory_map),"bytes")

    memory.memory_map[0xFF92] = 0xAA
    memory.memory_map[0xFF94] = 0xBB
    memory.memory_map[0xFF96] = 0xCC
    memory.memory_map[0xFF98] = 0xDD
    memory.memory_map[0xFF9a] = 0xEE
    memory.memory_map[0xFF9c] = 0xFF

    memory.print_memory_map()
