"""
CPU
"""

from register import Register
from memory import Memory
from interrupts import Interrupts
import op


class CPU:
    """
    CPU

    Main processing class, responsible for executing every instruction, checking interrupts, timing, etc.

    The Game Boy CPU runs at 4194304hz, i.e. 4194304 cycles per second.
    The special Divider Register (DIV, 0xFF04) must be incremented 16384 times per second, i.e. every 256 CPU cycles.
    """

    DIV_ADDRESS = 0xFF04

    def __init__(self):
        self.register = Register()
        self.memory = Memory()
        self.interrupts = Interrupts(self)
        self.halted = False  # for 76 (HALT)
        self.stopped = False  # for 10 (STOP)
        self._cartridge_data = None

    def execute(self, cartridge_data, debug=False):
        """
        Execution main loop.
        :param cartridge_data: game to execute
        :param debug: If will run in debug mode or not
        """
        self._cartridge_data = cartridge_data

        self.print_cartridge_info()

        cycles_spent = 0
        while True:
            opcode = None
            if not self.halted and not self.stopped:
                opcode = self.read_next_byte_from_cartridge()

                plus1 = "{:02X}".format(self._cartridge_data[self.register.PC])
                plus2 = "{:02X}".format(self._cartridge_data[self.register.PC+1])
                print("Executing", "0x{:04X}: {:02X} ".format(self.register.PC-1,opcode),"[",plus1,",",plus2,"]")
                cycles_spent += op.execute(self, opcode)
            cycles_spent += self.interrupts.update(opcode)

            if cycles_spent >= 256:
                current_div = self.memory.read_8bit(self.DIV_ADDRESS)
                self.memory.write_8bit(self.DIV_ADDRESS,current_div+1)
                cycles_spent = cycles_spent-256

            if debug:
                self.debug()
                input()

    def read_next_byte_from_cartridge(self):
        """
        Read the next data from the ROM, increment Program Counter
        :return: 8-bit data read from ROM
        """
        data = self._cartridge_data[self.register.PC]
        self.register.PC += 1
        return data

    def debug(self):
        self.register.debug()
        self.memory.debug()

    def print_cartridge_info(self):
        """
        Prints the cartridge header info.
        See: http://gbdev.gg8.se/files/docs/mirrors/pandocs.html#thecartridgeheader
        """
        title = self._cartridge_data[0x0134:0x143].replace(b'\x00', b'').decode("ascii")
        print("Title:", title)

        cartridge_type_dict = {0x00:"ROM ONLY",0x01:"MBC1",0x02:"MBC1+RAM",0x03:"MBC1+RAM+BATTERY",
                               0x05:"MBC2",0x06:"MBC2+BATTERY",0x08:"ROM+RAM",0x09:"ROM+RAM+BATTERY",
                               0x0B:"MMM01",0x0C:"MMM01+RAM",0x0D:"MMM01+RAM+BATTERY",
                               0x0F:"MBC3+TIMER+BATTERY",0x10:"MBC3+TIMER+RAM+BATTERY",0x11:"MBC3",
                               0x12:"MBC3+RAM",0x13:"MBC3+RAM+BATTERY",0x15:"MBC4",0x16:"MBC4+RAM",
                               0x17:"MBC4+RAM+BATTERY",0x19:"MBC5",0x1A:"MBC5+RAM",0x1B:"MBC5+RAM+BATTERY",
                               0x1C:"MBC5+RUMBLE",0x1D:"MBC5+RUMBLE+RAM",0x001E:"MBC5+RUMBLE+RAM+BATTERY",
                               0xFC:"POCKET CAMERA",0xFD:"BANDAI TAMA5",0xFE:"HuC3",0xFF:"HuC1+RAM+BATTERY"}
        print("Cartridge:",cartridge_type_dict[self._cartridge_data[0x0147]])

        rom_size = {0x00:"32KByte (no ROM banking)",0x01:"64KByte (4 banks)",0x02:"128KByte (8 banks)",
                    0x03:"256KByte (16 banks)",0x04:"512KByte (32 banks)",
                    0x05:"1MByte (64 banks) - only 63 banks used by MBC1",
                    0x06:"2MByte (128 banks) - only 125 banks used by MBC1",
                    0x07:"4MByte (256 banks)",0x52:"1.1MByte (72 banks)",0x53:"1.2MByte (80 banks)",
                    0x54:"1.5MByte (96 banks)"}
        print("ROM Size:", rom_size[self._cartridge_data[0x0148]])

        ram_size = {0x00:"None",0x01:"2 KBytes",0x02:"8 Kbytes",0x03:"32 KBytes (4 banks of 8KBytes each)"}
        print("RAM Size:", ram_size[self._cartridge_data[0x0149]])

        destination = {0x00:"Japanese",0x01:"Non-Japanese"}
        print("Destination:", destination[self._cartridge_data[0x014A]])

        print("Version:", self._cartridge_data[0x014C])
