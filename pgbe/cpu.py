"""
CPU

Main processing class, responsible for executing every instruction, checking interrupts, timing, etc.
"""
from register import Register
import op
import logging


class CPU:
    """ CPU """

    # The Game Boy CPU runs at 4194304hz, i.e. 4194304 cycles per second
    CLOCK_HZ = 4194304

    # The special Divider Register (DIV, 0xFF04) must be incremented 16384 times per second, i.e. every 256 CPU cycles
    DIV_ADDRESS = 0xFF04

    def __init__(self, gb):
        """
        :type gb: gb.GB
        """
        # Communication with other components
        self.gb = gb

        # Components exclusive to CPU
        self.register = Register()

        # State initialization
        self.halted = False  # for OP 76 (HALT)
        self.stopped = False  # for OP 10 (STOP)
        self._cartridge_data: bytes = None

        # Logger
        self.logger = logging.getLogger("pgbe")

    def execute(self, cartridge_data: bytes, debug: bool, step: bool):
        """
        Execution main loop.
        :param cartridge_data: game to execute
        :param debug: If will run in debug mode or not
        :param step: If it will stop after executing each loop or not. Requires debug==True.
        """
        self._cartridge_data = cartridge_data

        while True:
            opcode: int = None
            cycles_spent = 0
            if not self.halted and not self.stopped:
                opcode = self.read_next_byte_from_cartridge()

                plus1 = "{:02X}".format(self._cartridge_data[self.register.PC])
                plus2 = "{:02X}".format(self._cartridge_data[self.register.PC+1])
                self.logger.debug("Executing 0x%04X: %02X  [ %s , %s ]",self.register.PC-1,opcode,plus1,plus2)
                cycles_spent += op.execute(self.gb, opcode)
            cycles_spent += self.gb.interrupts.update(opcode)
            self.gb.gpu.update(cycles_spent)

            if debug:
                self.gb.debug()
                if step:
                    input()

            # TODO: redo
            # if cycles_spent >= 256:
            #     current_div = self.memory.read_8bit(self.DIV_ADDRESS)
            #     new_div = (current_div + (cycles_spent/256)) & 0xFF  # TODO: what if value > FF?
            #     self.memory.write_8bit(self.DIV_ADDRESS,new_div)
            #     cycles_spent = cycles_spent % 256

    def read_next_byte_from_cartridge(self):
        """
        Read the next data from the ROM, increment Program Counter
        :return: 8-bit data read from ROM
        """
        data = self._cartridge_data[self.register.PC]
        self.register.PC += 1
        return data

    def debug(self):
        """
        Prints debug info to console.
        """
        self.register.debug()
