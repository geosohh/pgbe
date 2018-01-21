"""
CPU
"""

from register import Register
from memory import Memory
from interrupts import Interrupts
from gpu import GPU
import op
import logging


class CPU:
    """
    CPU

    Main processing class, responsible for executing every instruction, checking interrupts, timing, etc.

    The Game Boy CPU runs at 4194304hz, i.e. 4194304 cycles per second.
    The special Divider Register (DIV, 0xFF04) must be incremented 16384 times per second, i.e. every 256 CPU cycles.
    """

    CLOCK_HZ = 4194304

    DIV_ADDRESS = 0xFF04

    def __init__(self):
        self.register = Register()
        self.memory = Memory(self)
        self.interrupts = Interrupts(self)
        self.gpu = GPU(self)
        self.halted = False  # for 76 (HALT)
        self.stopped = False  # for 10 (STOP)
        self._cartridge_data = None

        self.logger = logging.getLogger("pgbe")
        hdlr = logging.FileHandler('test.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.DEBUG)

    def execute(self, cartridge_data, debug=False, step=False):
        """
        Execution main loop.
        :param cartridge_data: game to execute
        :param debug: If will run in debug mode or not
        :param step: If it will stop after executing each loop or not. Requires debug==True.
        """
        self._cartridge_data = cartridge_data

        self.print_cartridge_info()

        debug = bool(int(debug))
        step = bool(int(step))
        self.logger.info("Debug: %s\tStep: %s",debug,step)

        while True:
            opcode = None
            cycles_spent = 0
            if not self.halted and not self.stopped:
                opcode = self.read_next_byte_from_cartridge()

                plus1 = "{:02X}".format(self._cartridge_data[self.register.PC])
                plus2 = "{:02X}".format(self._cartridge_data[self.register.PC+1])
                self.logger.debug("Executing 0x%04X: %02X  [ %s , %s ]",self.register.PC-1,opcode,plus1,plus2)
                cycles_spent += op.execute(self, opcode)
            cycles_spent += self.interrupts.update(opcode)
            self.gpu.update(cycles_spent)

            if debug:
                self.debug()
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
        self.memory.debug()  # Makes execution really slow
        self.interrupts.debug()
        self.gpu.debug()
        self.logger.debug("---")

    def print_cartridge_info(self):
        """
        Prints the cartridge header info.
        See: http://gbdev.gg8.se/files/docs/mirrors/pandocs.html#thecartridgeheader
        """
        title = self._cartridge_data[0x0134:0x143].replace(b'\x00', b'').decode("ascii")
        self.logger.info("Title: %s", title)

        cartridge_type_dict = {0x00:"ROM ONLY",0x01:"MBC1",0x02:"MBC1+RAM",0x03:"MBC1+RAM+BATTERY",
                               0x05:"MBC2",0x06:"MBC2+BATTERY",0x08:"ROM+RAM",0x09:"ROM+RAM+BATTERY",
                               0x0B:"MMM01",0x0C:"MMM01+RAM",0x0D:"MMM01+RAM+BATTERY",
                               0x0F:"MBC3+TIMER+BATTERY",0x10:"MBC3+TIMER+RAM+BATTERY",0x11:"MBC3",
                               0x12:"MBC3+RAM",0x13:"MBC3+RAM+BATTERY",0x15:"MBC4",0x16:"MBC4+RAM",
                               0x17:"MBC4+RAM+BATTERY",0x19:"MBC5",0x1A:"MBC5+RAM",0x1B:"MBC5+RAM+BATTERY",
                               0x1C:"MBC5+RUMBLE",0x1D:"MBC5+RUMBLE+RAM",0x001E:"MBC5+RUMBLE+RAM+BATTERY",
                               0xFC:"POCKET CAMERA",0xFD:"BANDAI TAMA5",0xFE:"HuC3",0xFF:"HuC1+RAM+BATTERY"}
        self.logger.info("Cartridge: %s",cartridge_type_dict[self._cartridge_data[0x0147]])

        rom_size = {0x00:"32KByte (no ROM banking)",0x01:"64KByte (4 banks)",0x02:"128KByte (8 banks)",
                    0x03:"256KByte (16 banks)",0x04:"512KByte (32 banks)",
                    0x05:"1MByte (64 banks) - only 63 banks used by MBC1",
                    0x06:"2MByte (128 banks) - only 125 banks used by MBC1",
                    0x07:"4MByte (256 banks)",0x52:"1.1MByte (72 banks)",0x53:"1.2MByte (80 banks)",
                    0x54:"1.5MByte (96 banks)"}
        self.logger.info("ROM Size: %s", rom_size[self._cartridge_data[0x0148]])

        ram_size = {0x00:"None",0x01:"2 KBytes",0x02:"8 Kbytes",0x03:"32 KBytes (4 banks of 8KBytes each)"}
        self.logger.info("RAM Size: %s", ram_size[self._cartridge_data[0x0149]])

        destination = {0x00:"Japanese",0x01:"Non-Japanese"}
        self.logger.info("Destination: %s", destination[self._cartridge_data[0x014A]])

        self.logger.info("Version: %d", self._cartridge_data[0x014C])
