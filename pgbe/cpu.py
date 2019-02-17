"""
CPU

Main processing class, responsible for executing every instruction, checking interrupts, timing, etc.
"""
from register import Register
import op
from log import Log


from datetime import datetime


class CPU:
    """ CPU """

    # The GameBoy CPU runs at 4194304hz, i.e. 4194304 cycles per second
    CLOCK_HZ = 4194304

    # The special Divider Register (DIV, 0xFF04) must be incremented 16384 times per second, i.e. every 256 CPU cycles
    DIV_ADDRESS = 0xFF04

    def __init__(self, gb):
        """
        :type gb: gb.GB
        """
        # Logger
        self.logger = Log()

        # Communication with other components
        self.gb = gb

        # Components exclusive to CPU
        self.register = Register()

        # State initialization
        self.halted = False  # for OP 76 (HALT)
        self.stopped = False  # for OP 10 (STOP)

    def execute(self):
        """
        Execution main loop
        """
        if self.gb.debug_mode:
            start = datetime.now()
        full_update_cycle_completed = False
        while not full_update_cycle_completed:
            opcode: int = None
            cycles_spent = 0
            if not self.halted and not self.stopped:
                opcode = self.read_next_byte_from_cartridge()

                if self.gb.debug_mode:
                    plus1 = "{:02X}".format(self.gb.memory.read_8bit(self.register.PC))
                    plus2 = "{:02X}".format(self.gb.memory.read_8bit(self.register.PC+1))
                    self.logger.debug("Executing 0x%04X: %02X  [ %s , %s ]",self.register.PC-1,opcode,plus1,plus2)
                cycles_spent += op.execute(self.gb, opcode)
            cycles_spent += self.gb.interrupts.update(opcode)
            full_update_cycle_completed = self.gb.gpu.update(cycles_spent)

            if self.gb.debug_mode:
                self.gb.debug()
                if self.gb.step_mode:
                    input()

            # TODO: redo
            # if cycles_spent >= 256:
            #     current_div = self.memory.read_8bit(self.DIV_ADDRESS)
            #     new_div = (current_div + (cycles_spent/256)) & 0xFF  # TODO: what if value > FF?
            #     self.memory.write_8bit(self.DIV_ADDRESS,new_div)
            #     cycles_spent = cycles_spent % 256
        if self.gb.debug_mode:
            end = datetime.now()
            delta = self.delta(start, end)
            print("total:", delta, "\tFPS:",1000.0/delta)

    def read_next_byte_from_cartridge(self):
        """
        Read the next data from the ROM, increment Program Counter
        :return: 8-bit data read from ROM
        """
        data = self.gb.memory.read_8bit(self.register.PC)
        self.register.PC += 1
        return data

    def delta(self, a, b):
        diff = b-a
        return (diff.seconds * 1000.0) + (diff.microseconds / 1000.0)

    def debug(self):
        """
        Prints debug info to console.
        """
        self.register.debug()
