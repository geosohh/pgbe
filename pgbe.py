"""
Python GameBoy Emulator
"""
from gb import GB
import sys


def print_rom_data(data: bytes):
    """ Print a few lines from the ROM """
    # lines_to_print = len(rom_data)
    lines_to_print = 1000
    for i in range(0, lines_to_print, 16):
        mem_str = "0x{:04X} | ".format(i)
        for j in range(0, 16):
            mem_str += "{:02X} ".format((data[i + j]))
        mem_str += "|"
        print(mem_str)


if __name__ == '__main__':
    rom_file = sys.argv[1]
    debug = bool(int(sys.argv[2]))
    step = bool(int(sys.argv[3]))
    f = open(rom_file, "rb")
    cartridge_data = f.read()
    f.close()
    # print_rom_data(cartridge_data)

    gb = GB()
    gb.execute(cartridge_data, debug, step)
