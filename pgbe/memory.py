"""
Memory

Although it is called "memory", do not think of it as like a computer RAM module. In reality, it is a continuous
addressable space where each area is actually located in a separate place. An "address decoder" is the one responsible
for mapping the continuous addresses and their real location (e.g. game cartridge data banks, actual RAM, etc.).

0x0000 - 0x3FFF: Cartridge ROM, bank 0
                 The first 16KB of the cartridge ROM must always be mapped to these addresses. The only exception is:
                    0x0000 - 0x00FF: Boot ROM - Mapped to these addresses on GameBoy startup. Once it is unmapped (by
                                     writing 1 to 0xFF50) it can never be mapped again until the device is restarted
                                     (i.e. changing 0xFF50 again does nothing).

0x4000 - 0x7FFF: Cartridge ROM, bank 1..N
                 By default the next 16KB of the cartridge ROM are mapped here. However, if the cartridge has more than
                 2 banks (32KB) a Memory Bank Controller (MBC) is responsible for switching the bank currently mapped.
                 The MBC is a physical component included in the game cartridge, so it must be emulated as well.

0x8000 - 0x9FFF: Video RAM (VRAM)
                 Memory for tile sets and maps to be displayed on screen.

0xA000 - 0xBFFF: External RAM
                 8KB of RAM located in the physical cartridge. Not all cartridges have this extra RAM; if a cartridge
                 does not have it than these addresses are unused.

0xC000 - 0xDFFF: Internal RAM
                 8KB of RAM located in the GameBoy itself.

0xE000 - 0xFDFF: Internal RAM "Echo"
                 A mirror of the internal RAM 0xC000-0xDE00 due to how the GameBoy is wired. Typically not used.

0xFE00 - 0xFE9F: Sprite Attribute Table (Object Attribute Memory - OAM)
                 Data (position + attributes) of up to 40 sprites (4 bytes each) to be rendered by the GPU.

0xFEA0 - 0xFEFF: EMPTY
                 These addresses are not used for anything.

0xFF00 - 0xFF7F: I/O
                 Control values for all the GameBoy's subsystems (buttons, sound, screen, etc.).

0xFF80 - 0xFFFE: High RAM (HRAM)
                 High-speed memory. Some of the GameBoy OpCode instructions are made specially for this area, allowing
                 data here to be accessed faster.

     0xFFFF    : Interrupts Enable Register (IE)
                 Separate I/O register used to enable/disable interrupts by specific subsystems.

All data in memory is stored in little endian format (i.e. least significant byte first).

See:
- https://realboyemulator.files.wordpress.com/2013/01/gbcpuman.pdf
- http://gbdev.gg8.se/wiki/articles/Memory_Map
- http://imrannazar.com/GameBoy-Emulation-in-JavaScript:-Memory
- http://gameboy.mongenel.com/dmg/lesson5.html
- https://www.gamedev.net/forums/topic/689286-game-boy-data-bus-memory-selector-circuit-confusion/
- https://stackoverflow.com/questions/21639597/z80-register-endianness
"""
import array
from log import Log


class Memory:
    """ Memory """

    def __init__(self, gb):
        """
        :type gb: gb.GB
        """
        # Logger
        self.logger = Log()

        # Communication with other components
        self.gb = gb

        # State initialization
        self.tile_set_1_only = None  # These will be initialized
        self.tile_set_shared = None  # below, this is just to
        self.tile_set_0_only = None  # have them declared in
        self.tile_maps = None        # the __init__ method

        # Cartridge bank 0, so nothing to initialize:  0x3FFF - 0x0000
        # Cartridge bank N, so nothing to initialize:  0x7FFF - 0x4000
        self._generate_tile_set_memory()  # VRAM sets: 0x97FF - 0x8000
        self._generate_tile_map_memory()  # VRAM maps: 0x9FFF - 0x9800
        self.external_ram = self._generate_memory_map((0xBFFF - 0xA000 + 1) * 4)  # Maximum RAM size, with 4 banks
        self.internal_ram = self._generate_memory_map( 0xDFFF - 0xC000 + 1)
        # Internal RAM echo, so nothing to initialize: 0xFDFF - 0xE000
        self.oam          = self._generate_memory_map( 0xFE9F - 0xFE00 + 1)
        # Empty, so nothing to initialize:             0xFEFF - 0xFEA0
        self.io           = self._generate_memory_map( 0xFF7F - 0xFF00 + 1)
        self.hram         = self._generate_memory_map( 0xFFFE - 0xFF80 + 1)
        self.ie = 0x00  # Single address, no array:    0xFFFF

        self.cartridge: bytes = None
        self.boot_rom: bytes = None
        self.boot_rom_loaded = False

        self.mbc: MBC = None

    def _generate_tile_set_memory(self):
        """
        GameBoy VRAM memory stores 2 tile sets. Each tile set contains 255 tiles (8x8 images). However, the GameBoy does
        not have enough memory for two full sets, so they share half (128) their tiles. This method generates the data
        structure to handle this.
        """
        self.tile_set_1_only = [self._generate_blank_tile() for _ in range(128)]  # 8000-87FF
        self.tile_set_shared = [self._generate_blank_tile() for _ in range(128)]  # 8800-8FFF
        self.tile_set_0_only = [self._generate_blank_tile() for _ in range(128)]  # 9000-97FF

    @staticmethod
    def _generate_blank_tile():
        """ Creates an empty matrix, representing one tile (8x8 pixels) """
        return [[0]*8 for _ in range(8)]

    def _generate_tile_map_memory(self):
        """
        GameBoy VRAM memory stores 2 tile maps. Each tile map contains 32x32 tile IDs, and differently from the tile
        sets, there is enough memory for two separate maps. This method generates the data structure to handle this.
        """
        self.tile_maps = [
            [[0]*32 for _ in range(32)],  # Tile 0 comes first, uses memory 9800-9BFF
            [[0]*32 for _ in range(32)]   # Tile 1 comes later, uses memory 9C00-9FFF
        ]

    def load_cartridge(self, cartridge_data: bytes):
        """
        Stores reference to cartridge data, to be accessed later. Also instantiates the MBC specified in cartridge.
        :param cartridge_data: Cartridge data as bytes
        """
        self.cartridge = cartridge_data
        mbc_type = self.cartridge[0x0147]
        self.mbc = MBC(mbc_type)

        self.load_boot_rom()
        self.boot_rom_loaded = (self.boot_rom is not None)

    def _read(self, address: int):
        """
        Read a byte from a location mapped in memory, wherever it is.
        :param address: Address to read
        :return: Value at specified address
        """
        if address <= 0x3FFF:    # 0x0000 - 0x3FFF: Cartridge bank 0
            if 0x0000 <= address <= 0x00FF and self.boot_rom_loaded:
                return self.boot_rom[address]
            return self.cartridge[address]

        elif address <= 0x7FFF:  # 0x4000 - 0x7FFF: Cartridge bank N
            return self.cartridge[self.mbc.cartridge_bank_offset() + (address-0x4000)]

        elif address <= 0x9FFF:  # 0x8000 - 0x9FFF: Video RAM
            if address <= 0x97FF:  # Tile sets memory
                return self._read_tile_set(address)
            else:  # Tile maps memory
                return self._read_tile_map(address)

        elif address <= 0xBFFF:  # 0xA000 - 0xBFFF: External RAM
            if self.mbc.external_ram_is_enabled:
                return self.external_ram[self.mbc.external_ram_bank_offset() + (address-0xA000)]
            else:
                return 0x00  # TODO: Is this the correct behavior?

        elif address <= 0xDFFF:  # 0xC000 - 0xDFFF: Internal RAM
            return self.internal_ram[address - 0xC000]

        elif address <= 0xFDFF:  # 0xE000 - 0xFDFF: Internal RAM Echo
            return self.internal_ram[address - 0xE000]

        elif address <= 0xFE9F:  # 0xFE00 - 0xFE9F: Object Attribute Memory (OAM)
            return self.oam[address - 0xFE00]

        elif address <= 0xFEFF:  # 0xFEA0 - 0xFEFF: Empty area
            return 0x00

        elif address <= 0xFF7F:  # 0xFF00 - 0xFF7F: I/O Memory
            return self.io[address - 0xFF00]

        elif address <= 0xFFFE:  # 0xFF80 - 0xFFFE: High RAM
            return self.hram[address - 0xFF80]

        elif address == 0xFFFF:  # 0xFFFF: Interrupts Enable Register (IE)
            return self.ie

    def _read_tile_set(self, address: int):
        tile_line, tile_line_byte_to_read = self._find_tile_set(address)

        byte = 0x00
        for pixel_value in tile_line:  # pixel_value is 0-3, and we want the binary value from the desired position
            byte = (byte << 1) | ((pixel_value >> tile_line_byte_to_read) & 0b00000001)
        return byte

    def _read_tile_map(self, address: int):
        tile_map_line, tile_map_pos_number = self._find_tile_map(address)
        return tile_map_line[tile_map_pos_number]

    def _write(self, address: int, value: int):
        """
        Writes a byte to a location mapped in memory, wherever it is.
        :param address: Address where data will be written
        :param value:   Data to write
        """
        if address <= 0x1FFF:    # 0x0000 - 0x1FFF: MBC - Enable/Disable external RAM
            self.mbc.change_external_ram_status(value)

        if address <= 0x3FFF:    # 0x2000 - 0x3FFF: MBC - Change cartridge bank mapped to N
            self.mbc.change_cartridge_bank(value)

        if address <= 0x5FFF:    # 0x4000 - 0x5FFF: MBC - Change external RAM bank mapped
            self.mbc.change_ram_bank(value)

        if address <= 0x7FFF:    # 0x6000 - 0x7FFF: MBC - Change ROM/RAM Mode
            self.mbc.change_banking_mode(value)

        if address <= 0x9FFF:    # 0x8000 - 0x9FFF: Video RAM
            if address <= 0x97FF:  # Tile sets memory
                return self._write_tile_set(address, value)
            else:  # Tile maps memory
                return self._write_tile_map(address, value)

        elif address <= 0xBFFF:  # 0xA000 - 0xBFFF: External RAM
            if self.mbc.external_ram_is_enabled:
                self.external_ram[address - 0xA000] = value

        elif address <= 0xDFFF:  # 0xC000 - 0xDFFF: Internal RAM
            self.internal_ram[address - 0xC000] = value

        elif address <= 0xFDFF:  # 0xE000 - 0xFDFF: Internal RAM Echo
            self.internal_ram[address - 0xE000] = value

        elif address <= 0xFE9F:  # 0xFE00 - 0xFE9F: Object Attribute Memory (OAM)
            self.oam[address - 0xFE00] = value

        elif address <= 0xFEFF:  # 0xFEA0 - 0xFEFF: Empty area is empty, so nothing to do
            return

        elif address <= 0xFF7F:  # 0xFF00 - 0xFF7F: I/O Memory
            self.io[address - 0xFF00] = value
            if 0xFF40 <= address <= 0xFF47:
                self.gb.gpu.update_gpu_register(address, value)
            elif address == 0xFF50 and value == 1:
                self.boot_rom_loaded = False  # Once the boot rom is unmapped it cannot be mapped again, so no "= True"

        elif address <= 0xFFFE:  # 0xFF80 - 0xFFFE: High RAM
            self.hram[address - 0xFF80] = value

        elif address == 0xFFFF:  # 0xFFFF: Interrupts Enable Register (IE)
            self.ie = value

    def _write_tile_set(self, address: int, value: int):
        tile_line, tile_line_byte_to_change = self._find_tile_set(address)

        # For each value in the tile line, retrieve the byte that will not be modified, and sum with the byte received
        for i in range(8):
            bit_to_keep = (tile_line[i] >> int(not tile_line_byte_to_change)) & 0b00000001
            bit_to_change = (value >> (7-i)) & 0b00000001
            new_value = (bit_to_keep << int(not tile_line_byte_to_change)) | (bit_to_change << tile_line_byte_to_change)
            tile_line[i] = new_value  # Edit the existing list, not replace it, so shared tiles keep working

    def _write_tile_map(self, address: int, value: int):
        tile_map_line, tile_map_pos_number = self._find_tile_map(address)
        tile_map_line[tile_map_pos_number] = value

    def _find_tile_set(self, address: int):
        v_address = address - 0x8000
        tile_number = v_address // 16  # length of each tile (8 lines * 2 bytes each = 16 bytes)
        if tile_number < 128:
            tile_number_fixed = tile_number
            tile_set = self.tile_set_1_only
        elif tile_number < 256:
            tile_number_fixed = tile_number - 128
            tile_set = self.tile_set_shared
        else:
            tile_number_fixed = tile_number - 256
            tile_set = self.tile_set_0_only
        tile_byte_number = v_address - (tile_number * 16)  # Will get a value 0-15, since each GameBoy tile has 8 lines,
        tile_line_number = tile_byte_number // 2           # each made from 2 bytes. We are storing the tile line final
        tile_line_byte_to_change = tile_byte_number % 2    # value instead, so we need to convert it back to 2 bytes.

        tile_line = tile_set[tile_number_fixed][tile_line_number]
        return tile_line, tile_line_byte_to_change

    def _find_tile_map(self, address: int):
        v_address = address - 0x9800
        tile_map_number = v_address // 32
        if tile_map_number < 32:
            tile_map_number_fixed = tile_map_number
            tile_map = self.tile_maps[0]
        else:
            tile_map_number_fixed = tile_map_number - 32
            tile_map = self.tile_maps[1]
        tile_map_pos_number = v_address - (tile_map_number * 32)
        return tile_map[tile_map_number_fixed], tile_map_pos_number

    @staticmethod
    def _generate_memory_map(size: int):
        """
        Generate a memory area.
        See: https://docs.python.org/3/library/array.html
        :return:
        """
        byte_array = array.array('B')  # 'B' == "unsigned char" in C / "int" in Python, minimum size is 1 byte
        byte_array.extend((0x00,) * size)
        return byte_array

    def get_map(self, map_number: int):
        """ Helper method to retrieve a tile map """
        return self.tile_maps[map_number]

    def get_tile(self, tile_set_number: int, tile_number: int):
        """ Helper method to retrieve a tile from a set """
        if tile_number < 128:
            if tile_set_number == 0:
                return self.tile_set_0_only[tile_number]
            else:
                return self.tile_set_1_only[tile_number]
        else:
            # It's in the shared area; 'tile_number' is unsigned so we do not need to worry about that
            return self.tile_set_shared[tile_number-128]

    def load_boot_rom(self):
        """
        Adds the GameBoy boot ROM to the beginning of the memory, so it is executed when the emulator starts.

        The boot ROM prepares the device by clearing memory areas and setting up some initial values. We could set the
        appropriate memory values without using the boot ROM and skip directly to game ROM execution, but it is more
        fun like this :)

        See:  http://gbdev.gg8.se/wiki/articles/Gameboy_Bootstrap_ROM
        """
        try:
            f = open("boot.rom", "rb")
            boot_rom = f.read()
            f.close()
            return boot_rom
        except FileNotFoundError:
            self.logger.info("Boot ROM not found, skipping it")
            self.write_8bit(0xFF05, 0x00)  # TIMA
            self.write_8bit(0xFF06, 0x00)  # TMA
            self.write_8bit(0xFF07, 0x00)  # TAC
            self.write_8bit(0xFF10, 0x80)  # NR10
            self.write_8bit(0xFF11, 0xBF)  # NR11
            self.write_8bit(0xFF12, 0xF3)  # NR12
            self.write_8bit(0xFF14, 0xBF)  # NR14
            self.write_8bit(0xFF16, 0x3F)  # NR21
            self.write_8bit(0xFF17, 0x00)  # NR22
            self.write_8bit(0xFF19, 0xBF)  # NR24
            self.write_8bit(0xFF1A, 0x7F)  # NR30
            self.write_8bit(0xFF1B, 0xFF)  # NR31
            self.write_8bit(0xFF1C, 0x9F)  # NR32
            self.write_8bit(0xFF1E, 0xBF)  # NR33
            self.write_8bit(0xFF20, 0xFF)  # NR41
            self.write_8bit(0xFF21, 0x00)  # NR42
            self.write_8bit(0xFF22, 0x00)  # NR43
            self.write_8bit(0xFF23, 0xBF)  # NR30
            self.write_8bit(0xFF24, 0x77)  # NR50
            self.write_8bit(0xFF25, 0xF3)  # NR51
            self.write_8bit(0xFF26, 0xF1)  # NR52
            self.write_8bit(0xFF40, 0x91)  # LCDC
            self.write_8bit(0xFF42, 0x00)  # SCY
            self.write_8bit(0xFF43, 0x00)  # SCX
            self.write_8bit(0xFF45, 0x00)  # LYC
            self.write_8bit(0xFF47, 0xFC)  # BGP
            self.write_8bit(0xFF48, 0xFF)  # 0BP0
            self.write_8bit(0xFF49, 0xFF)  # 0BP1
            self.write_8bit(0xFF50, 0x01)  # Boot ROM unmap
            self.write_8bit(0xFF4A, 0x00)  # WY
            self.write_8bit(0xFF4B, 0x00)  # WX
            self.write_8bit(0xFFFF, 0x00)  # IE
            return None

    def write_8bit(self, address: int, value: int):
        """
        Writes the given value at the given memory address.
        :param address: Address to write
        :param value: Value to write
        """
        self.logger.debug("writing 8-bit value %02X at address 0x%04X",value,address)
        self._write(address, value)

    def write_16bit(self, address: int, value: int):
        """
        Writes 16-bit big-endian value at the given memory address. Memory is little-endian, so least significant byte
        goes at address, most significant byte goes at address+1.
        :param address: Address to write
        :param value: Value to write
        """
        lsb = value & 0x00ff
        msb = (value >> 8) & 0x00ff
        self.write_8bit(address, lsb)
        self.write_8bit(address+1, msb)

    def read_8bit(self, address: int):
        """
        Reads 8-bit value from the given address in the memory.
        :param address: Memory address to read data from
        :return: 8-bit value at the given memory address
        """
        return self._read(address)

    def read_16bit(self, address: int):
        """
        Reads 16-bit value from the given address in the memory. Least significant byte in address, most significant
        byte in address+1.
        :param address: Memory address to read data from
        :return: 16-bit value at the given memory address
        """
        lsb = self._read(address)
        msb = self._read(address+1)
        return (msb << 8) | lsb

    @staticmethod
    def print_memory_map(memory_map: array):
        """
        Prints the current memory map to console
        """
        for i in range(0, len(memory_map), 16):
            mem_str = "0x{:04X} | ".format(i)
            for j in range(0, 16):
                mem_str += "{:02X} ".format((memory_map[i + j]))
            mem_str += "|"
            print(mem_str)

    def debug(self):
        """
        Prints debug info to console.
        """
        # self.logger.debug("VRAM:")
        # self._debug_memory_map(self.vram)
        # self.logger.debug("External RAM:")
        # self._debug_memory_map(self.external_ram)
        # self.logger.debug("Internal RAM:")
        # self._debug_memory_map(self.internal_ram)
        # self.logger.debug("OAM:")
        # self._debug_memory_map(self.oam)
        self.logger.debug("I/O:")
        self._debug_memory_map(self.io)
        # self.logger.debug("HRAM:")
        # self._debug_memory_map(self.hram)

    def _debug_memory_map(self, memory_map: array):
        custom_dict = {}
        for i in range(0, len(memory_map)):
            if memory_map[i] != 0:
                custom_dict["0x{:04X}".format(i)] = "{:02X}".format(memory_map[i])
        self.logger.debug(custom_dict)


class MBC:
    """ Memory Bank Controller """

    def __init__(self, mbc_type: int):
        self.external_ram_bank = 0x00
        self.cartridge_bank = 0x01

        self.in_rom_banking_mode = True
        self.external_ram_is_enabled = False

    def change_cartridge_bank(self, value: int):
        """
        Change cartridge bank selected
        :param value: Value that the program/game tried to write to MBC. Only the first 5 bits matter.
        """
        if self.in_rom_banking_mode:
            rom_bank_number = self.external_ram_bank << 5
        else:
            rom_bank_number = 0x00
        rom_bank_number |= (value & 0b00011111)

        if rom_bank_number == 0x00:  # Attempts to read banks 0x00, 0x20, 0x40 or 0x60 will read the next bank instead
            rom_bank_number = 0x01
        elif rom_bank_number == 0x20:
            rom_bank_number = 0x21
        elif rom_bank_number == 0x40:
            rom_bank_number = 0x41
        elif rom_bank_number == 0x60:
            rom_bank_number = 0x61
        self.cartridge_bank = rom_bank_number

    def change_ram_bank(self, value: int):
        """
        Change RAM bank OR upper bits of cartridge bank, depending on the banking mode selected.
        :param value: Value that the program/game tried to write to MBC. Only the first 2 bits matter.
        """
        self.external_ram_bank = value & 0b00000011
        if self.in_rom_banking_mode:
            self.change_cartridge_bank(self.cartridge_bank)

    def change_banking_mode(self, value: int):
        """
        If value is 0, then it goes into ROM banking mode, otherwise goes into RAM banking mode.

        In ROM banking mode, the RAM bank number bits are used as upper bits (positions 5 and 6) in the cartridge bank
        number, increasing the number of cartridge banks accessible. On the other hand, doing this will prevent access
        to external RAM banks 1-3.

        :param value: Value with banking mode selected. Only the first bit matters.
        """
        self.in_rom_banking_mode = (value & 0b00000001) == 0
        self.change_cartridge_bank(self.cartridge_bank)

    def cartridge_bank_offset(self):
        """
        :return: Offset required in order to read data from the correct cartridge bank
        """
        return self.cartridge_bank * 0x4000

    def external_ram_bank_offset(self):
        """
        :return: Offset required in order to read data from the correct cartridge bank
        """
        if self.in_rom_banking_mode:
            return 0x00
        else:
            return self.external_ram_bank * 0x2000

    def change_external_ram_status(self, value: int):
        """
        Enable or disable external RAM read/write access. Disabling it after accessing the data needed protects its
        contents from damage/lost on GameBoy power off.
        :param value: New external RAM status
        """
        self.external_ram_is_enabled = (value & 0b00001111) == 0x0A
