"""
CPU
"""

from cpu.register import Register
from memory.memory import Memory
import cpu.op


class CPU:
    def __init__(self):
        self.register = Register()
        self.memory = Memory()
        self._cartridge_data = None

        self.halted = False  # for 76 (HALT)
        self.stopped = False  # for 10 (STOP)
        self.interrupts_enabled = False  # for F3 (DI) and FB (EI)
        self.disable_interrupts_requested = False  # for F3 (DI) and FB (EI)

    def execute(self, cartridge_data):
        self._cartridge_data = cartridge_data

        while(True):
            opcode = self.read_next_byte_from_cartridge()
            print("Executing", "0x{:04X}: {:02X} ".format(self.register.PC-1,opcode))
            cpu.op.execute(self,opcode)

    def read_next_byte_from_cartridge(self):
        """
        Read the next data from the ROM, increment Program Counter
        :return: 8-bit data read from ROM
        """
        data = self._cartridge_data[self.register.PC]
        self.register.PC += 1
        return data


if __name__ == '__main__':
    cpu = CPU()
