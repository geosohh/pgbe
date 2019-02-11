"""
CPU Registers

8-bit registers (can be combined to read as 16-bit registers):
|15 ... 8 | 7 ... 0 |
|    A    |    F    |     When combining the registers to read them as a 16-bit value,
|    B    |    C    |     A/B/D/H store the most significant byte
|    D    |    E    |     F/C/E/L store the least significant byte.
|    H    |    L    |

    A - Accumulator
        Where the result of 8-bit math operations are stored.

    F - Flags
        |7|6|5|4|3|2|1|0|
        |Z|N|H|C|_|_|_|_|
            Z - Zero Flag
                This bit is set when the result of a math operation is zero or two values match when using the CP
                instruction.
            N - Subtract Flag
                This bit is set if a subtraction was performed in the last math instruction.
            H - Half Carry Flag
                This bit is set if a carry occurred from the lower nibble (i.e. lower 4 bits of the result) in the
                last math operation.
            C - Carry Flag
                This bit is set if a carry occurred from the last math operation (i.e. when the result of an
                addition became bigger than FFh (8bit) or FFFFh (16bit). Or when the result of a subtraction or
                comparison became less than zero) or if register A is the smaller value when executing the CP
                instruction.
            _ - Not used, always zero

16-bit registers
|15 ... 0|
|   SP   |
|   PC   |

    SP - Stack Pointer
        Points to the current stack position.
        The GameBoy Stack Pointer is used to keep track of the top of the "stack". The stack is used for saving
        variables, saving return addresses, passing arguments to subroutines, and various other uses that might be
        conceived by the individual programmer.
        As information is put onto the stack, the stack grows downward in RAM memory. As a result, the Stack Pointer
        should always be initialized at the highest location of RAM space that has been allocated for use by the
        stack. For instance, if a programmer wishes to locate the Stack Pointer at the top of low RAM space
        ($C000-$DFFF) he would set the Stack Pointer to $E000 using the command LD SP,$E000. (The Stack Pointer
        automatically decrements before it puts something onto the stack so it is perfectly acceptable to assign it
        a value which points to a memory address which is one location past the end of available RAM.)
        The GameBoy stack pointer is initialized to $FFFE on power up but a programmer should not rely on this
        setting and rather should explicitly set its value.
    PC - Program Counter
        Points to the next instruction to be executed in the GameBoy memory.
        On power up, the GameBoy Program Counter is initialized to $0100 and the instruction found at this location
        in ROM is executed. The Program Counter from this point on is controlled, indirectly, by the program
        instructions themselves that were generated by the programmer of the ROM cart.

See:
- http://www.pastraiser.com/cpu/gameboy/gameboy_opcodes.html
- https://realboyemulator.files.wordpress.com/2013/01/gbcpuman.pdf (pages 61-64)
- http://gameboy.mongenel.com/dmg/lesson1.html
- http://gbdev.gg8.se/wiki/articles/CPU_Registers_and_Flags
- https://stackoverflow.com/questions/21639597/z80-register-endianness
"""
import logging


class Register:
    """
    GB Registers
    """
    def __init__(self):
        # 8-bit registers (can be combined to read as 16-bit registers)
        self.A = 0x00  # Accumulator
        self.F = 0x00  # Flags

        self.B = 0x00
        self.C = 0x00

        self.D = 0x00
        self.E = 0x00

        self.H = 0x00
        self.L = 0x00

        # 16-bit registers
        self.SP = 0xFFFE  # Stack Pointer
        self.PC = 0x0000  # Program Counter

        # Logger
        self.logger = logging.getLogger("pgbe")

    def skip_boot_rom(self):
        """
        If the GameBoy boot ROM is skipped, set registers as if the boot process completed successfully.
        """
        self.set_af(0x01B0)
        self.set_bc(0x0013)
        self.set_de(0x00D8)
        self.set_hl(0x014D)
        self.SP = 0xFFFE
        self.PC = 0x0100

    # Get Flags
    def _get_flag(self, bit_position: int):
        """
        Get specified flag bit.
        :param bit_position: Flag to return
        """
        mask = 1 << bit_position
        return (self.F & mask) >> bit_position

    def get_z_flag(self):
        """ Get Zero flag. """
        return self._get_flag(7)

    def get_n_flag(self):
        """ Get Subtract flag. """
        return self._get_flag(6)

    def get_h_flag(self):
        """ Get Half Carry flag. """
        return self._get_flag(5)

    def get_c_flag(self):
        """ Get Carry flag. """
        return self._get_flag(4)

    # Set/reset Flags
    def _set_flag(self, bit_position: int, new_value: bool):
        """
        Change specified flag bit in register F.
        :param bit_position: Bit to change
        :param new_value: New value for specified bit
        """
        new_value = int(new_value)  # True == 1; False == 0
        mask = 1 << bit_position
        if (self.F & mask) != (new_value << bit_position):  # If current value is != from new_value, flip current value
            self.F = self.F ^ mask

    def set_z_flag(self, new_value: bool):
        """
        Set Zero flag to given value.
        :param new_value:  New value for Zero flag.
        """
        self._set_flag(7,new_value)

    def set_n_flag(self, new_value: bool):
        """
        Set Subtract flag to given value.
        :param new_value:  New value for Subtract flag.
        """
        self._set_flag(6,new_value)

    def set_h_flag(self, new_value: bool):
        """
        Set Half Carry flag to given value.
        :param new_value:  New value for Half Carry flag.
        """
        self._set_flag(5,new_value)

    def set_c_flag(self, new_value: bool):
        """
        Set Carry flag to given value.
        :param new_value:  New value for Carry flag.
        """
        self._set_flag(4,new_value)

    # GET methods for 16-bit register combinations
    def get_af(self):
        """
        Get AF value.
        :return: AF values as single 16-bit value
        """
        return (self.A << 8) | self.F  # A==high / F==low

    def get_bc(self):
        """
        Get BC value.
        :return: BC values as single 16-bit value
        """
        return (self.B << 8) | self.C  # B==high / C==low

    def get_de(self):
        """
        Get DE value.
        :return: DE values as single 16-bit value
        """
        return (self.D << 8) | self.E  # D==high / E==low

    def get_hl(self):
        """
        Get HL value.
        :return: HL values as single 16-bit value
        """
        return (self.H << 8) | self.L  # H==high / L==low

    def set_a(self, d8: int):
        """
        Sets A to d8
        :param d8: Hex value to set
        """
        self.A = d8 & 0xFF
        self.logger.debug("set register A = 0x{:02X}".format(self.A))

    def set_f(self, d8: int):
        """
        Sets F to d8
        :param d8: Hex value to set
        """
        self.F = d8 & 0xFF
        self.logger.debug("set register F = 0x{:02X}".format(self.F))

    # SET methods for 16-bit register combinations
    def set_af(self, d16: int):
        """
        Sets AF values to d16
        :param d16: Hex value to set (assumes it is in big endian format)
        """
        self.set_f(d16 & 0x00ff)  # A==high / F==low
        self.set_a((d16 >> 8) & 0x00ff)

    def set_b(self, d8: int):
        """
        Sets B to d8
        :param d8: Hex value to set
        """
        self.B = d8 & 0xFF
        self.logger.debug("set register B = 0x{:02X}".format(self.B))

    def set_c(self, d8: int):
        """
        Sets C to d8
        :param d8: Hex value to set
        """
        self.C = d8 & 0xFF
        self.logger.debug("set register C = 0x{:02X}".format(self.C))

    def set_bc(self, d16: int):
        """
        Sets BC values to d16
        :param d16: Hex value to set (assumes it is in big endian format)
        """
        self.set_c(d16 & 0x00ff)  # B==high / C==low
        self.set_b((d16 >> 8) & 0x00ff)

    def set_d(self, d8: int):
        """
        Sets D to d8
        :param d8: Hex value to set
        """
        self.D = d8 & 0xFF
        self.logger.debug("set register D = 0x{:02X}".format(self.D))

    def set_e(self, d8: int):
        """
        Sets E to d8
        :param d8: Hex value to set
        """
        self.E = d8 & 0xFF
        self.logger.debug("set register E = 0x{:02X}".format(self.E))

    def set_de(self, d16: int):
        """
        Sets DE values to d16
        :param d16: Hex value to set (assumes it is in big endian format)
        """
        self.set_e(d16 & 0x00ff)  # D==high / E==low
        self.set_d((d16 >> 8) & 0x00ff)

    def set_h(self, d8: int):
        """
        Sets H to d8
        :param d8: Hex value to set
        """
        self.H = d8 & 0xFF
        self.logger.debug("set register H = 0x{:02X}".format(self.H))

    def set_l(self, d8: int):
        """
        Sets L to d8
        :param d8: Hex value to set
        """
        self.L = d8 & 0xFF
        self.logger.debug("set register L = 0x{:02X}".format(self.L))

    def set_hl(self, d16: int):
        """
        Sets HL values to d16
        :param d16: Hex value to set (assumes it is in big endian format)
        """
        self.set_l(d16 & 0x00ff)  # H==high / L==low
        self.set_h((d16 >> 8) & 0x00ff)

    def set_sp(self, d16: int):
        """
        Sets SP to d16
        :param d16: Hex value to set (assumes it is in big endian format)
        """
        self.SP = d16 & 0xFFFF
        self.logger.debug("set register SP = 0x{:04X}".format(self.SP))

    def set_pc(self, d16: int):
        """
        Sets PC to d16
        :param d16: Hex value to set (assumes it is in big endian format)
        """
        self.PC = d16 & 0xFFFF
        self.logger.debug("set register PC = 0x{:04X}".format(self.PC))

    def debug(self):
        """
        Prints debug info to console.
        """
        af = "{:04X}".format(self.get_af())
        bc = "{:04X}".format(self.get_bc())
        de = "{:04X}".format(self.get_de())
        hl = "{:04X}".format(self.get_hl())
        sp = "{:04X}".format(self.SP)
        pc = "{:04X}".format(self.PC)
        z = self.get_z_flag()
        n = self.get_n_flag()
        h = self.get_h_flag()
        c = self.get_c_flag()
        self.logger.debug("AF: %s\tBC: %s\tDE: %s\tHL: %s\tSP: %s\tPC: %s\tz: %s\tn: %s\th: %s\tc: %s",
                           af,      bc,    de,     hl,     sp,     pc,     z,     n,     h,     c)
