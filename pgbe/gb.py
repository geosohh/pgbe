"""
Responsible for instancing all necessary objects, so all GB components can communicate with one another.
"""
from cpu import CPU
from memory import Memory
from interrupts import Interrupts
from gpu import GPU
from screen import Screen
import logging


class GB:
    """ GB components instantiation """

    def __init__(self):
        self.logger = logging.getLogger("pgbe")
        # log_handler = logging.NullHandler()
        log_handler = logging.FileHandler("test.log", mode="w")
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        log_handler.setFormatter(formatter)
        self.logger.addHandler(log_handler)
        self.logger.setLevel(logging.DEBUG)

        self.cpu = CPU(self)
        self.memory = Memory()
        self.interrupts = Interrupts(self)
        self.gpu = GPU(self)

        self.debug_mode = False
        self.step_mode = False

    def execute(self, cartridge_data: bytes, debug: bool = False, step: bool = False):
        """
        Execution main loop.
        :param cartridge_data: game to execute
        :param debug: If will run in debug mode or not
        :param step: If it will stop after executing each loop or not. Requires debug==True.
        """
        self.print_cartridge_info(cartridge_data)
        self.debug_mode = debug
        self.step_mode = step
        self.logger.info("Debug: %s\tStep: %s",self.debug_mode,self.step_mode)
        self.memory.load_cartridge(cartridge_data)
        if self.memory.boot_rom is None:
            self.cpu.register.skip_boot_rom()

        # Instantiates the emulator screen. It will assume control of the main thread, so the emulator main loop must be
        # triggered by the Screen itself, as a scheduled method call.
        Screen(self)

    def print_cartridge_info(self, cartridge_data: bytes):
        """
        Prints the cartridge header info.
        See: http://gbdev.gg8.se/files/docs/mirrors/pandocs.html#thecartridgeheader
        """
        title = cartridge_data[0x0134:0x143].replace(b'\x00', b'').decode("ascii")
        self.logger.info("Title: %s", title)

        cartridge_type_dict = {0x00:"ROM ONLY",0x01:"MBC1",0x02:"MBC1+RAM",0x03:"MBC1+RAM+BATTERY",
                               0x05:"MBC2",0x06:"MBC2+BATTERY",0x08:"ROM+RAM",0x09:"ROM+RAM+BATTERY",
                               0x0B:"MMM01",0x0C:"MMM01+RAM",0x0D:"MMM01+RAM+BATTERY",
                               0x0F:"MBC3+TIMER+BATTERY",0x10:"MBC3+TIMER+RAM+BATTERY",0x11:"MBC3",
                               0x12:"MBC3+RAM",0x13:"MBC3+RAM+BATTERY",0x15:"MBC4",0x16:"MBC4+RAM",
                               0x17:"MBC4+RAM+BATTERY",0x19:"MBC5",0x1A:"MBC5+RAM",0x1B:"MBC5+RAM+BATTERY",
                               0x1C:"MBC5+RUMBLE",0x1D:"MBC5+RUMBLE+RAM",0x001E:"MBC5+RUMBLE+RAM+BATTERY",
                               0xFC:"POCKET CAMERA",0xFD:"BANDAI TAMA5",0xFE:"HuC3",0xFF:"HuC1+RAM+BATTERY"}
        self.logger.info("Cartridge: %s",cartridge_type_dict[cartridge_data[0x0147]])

        rom_size = {0x00:"32KByte (no ROM banking)",0x01:"64KByte (4 banks)",0x02:"128KByte (8 banks)",
                    0x03:"256KByte (16 banks)",0x04:"512KByte (32 banks)",
                    0x05:"1MByte (64 banks) - only 63 banks used by MBC1",
                    0x06:"2MByte (128 banks) - only 125 banks used by MBC1",
                    0x07:"4MByte (256 banks)",0x52:"1.1MByte (72 banks)",0x53:"1.2MByte (80 banks)",
                    0x54:"1.5MByte (96 banks)"}
        self.logger.info("ROM Size: %s", rom_size[cartridge_data[0x0148]])

        ram_size = {0x00:"None",0x01:"2 KBytes",0x02:"8 Kbytes",0x03:"32 KBytes (4 banks of 8KBytes each)"}
        self.logger.info("RAM Size: %s", ram_size[cartridge_data[0x0149]])

        destination = {0x00:"Japanese",0x01:"Non-Japanese"}
        self.logger.info("Destination: %s", destination[cartridge_data[0x014A]])

        self.logger.info("Version: %d", cartridge_data[0x014C])

    def debug(self):
        """
        Prints debug info to console.
        """
        self.cpu.debug()
        self.memory.debug()  # Makes execution really slow
        self.interrupts.debug()
        self.gpu.debug()
        self.logger.debug("---")
