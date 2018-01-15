"""
Python Game Boy Emulator
"""

from cpu import CPU
import sys


def print_rom_data(rom_data):
    """ Print a few lines from the ROM """
    # lines_to_print = len(rom_data)
    lines_to_print = 1000
    for i in range(0, lines_to_print, 16):
        mem_str = "0x{:04X} | ".format(i)
        for j in range(0, 16):
            mem_str += "{:02X} ".format((rom_data[i + j]))
        mem_str += "|"
        print(mem_str)


if __name__ == '__main__':
    rom_file = sys.argv[1]
    debug = sys.argv[2]
    step = sys.argv[3]
    f = open(rom_file, "rb")
    cartridge_data = f.read()
    f.close()
    # print_rom_data(rom_data)

    cpu = CPU()
    cpu.execute(cartridge_data,debug,step)
