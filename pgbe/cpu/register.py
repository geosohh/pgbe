class Register:
    """
    Registers

    TODO: Description.
    TODO: Little or Big endian?
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
        self.PC = 0x0100  # Program Counter

    # SET methods for 16-bit register combinations
    def set_af(self, d16):
        """
        Sets AF values to d16
        :param d16: Hex value to set
        """
        self.F = d16 & 0x00ff  # TODO: Little or Big-Endian? Currently A=high/F=low, but it might be the opposite
        self.A = (d16 >> 8) & 0x00ff

    def set_bc(self, d16):
        """
        Sets BC values to d16
        :param d16: Hex value to set
        """
        self.C = d16 & 0x00ff  # TODO: Little or Big-Endian? Currently B=high/C=low, but it might be the opposite
        self.B = (d16 >> 8) & 0x00ff

    def set_de(self, d16):
        """
        Sets DE values to d16
        :param d16: Hex value to set
        """
        self.E = d16 & 0x00ff  # TODO: Little or Big-Endian? Currently D=high/E=low, but it might be the opposite
        self.D = (d16 >> 8) & 0x00ff

    def set_hl(self, d16):
        """
        Sets HL values to d16
        :param d16: Hex value to set
        """
        self.L = d16 & 0x00ff  # TODO: Little or Big-Endian? Currently H=high/L=low, but it might be the opposite
        self.H = (d16 >> 8) & 0x00ff

    # ADD methods for 16-bit register combinations
    def add_af(self, d16):
        """
        Adds d16 to the current AF values.
        :param d16: Hex value to add
        """
        af = (self.A << 8) | self.F  # TODO: Little or Big-Endian? Currently A=high/F=low, but it might be the opposite

        af_inc = af + d16  # TODO: what if the result goes above 0xFFFF?

        self.F = af_inc & 0x00ff
        self.A = (af_inc >> 8) & 0x00ff

    def add_bc(self, d16):
        """
        Adds d16 to the current BC values.
        :param d16: Hex value to add
        """
        bc = (self.B << 8) | self.C  # TODO: Little or Big-Endian? Currently B=high/C=low, but it might be the opposite

        bc_inc = bc + d16  # TODO: what if the result goes above 0xFFFF?

        self.C = bc_inc & 0x00ff
        self.B = (bc_inc >> 8) & 0x00ff

    def add_de(self, d16):
        """
        Adds d16 to the current DE values.
        :param d16: Hex value to add
        """
        de = (self.D << 8) | self.E  # TODO: Little or Big-Endian? Currently D=high/E=low, but it might be the opposite

        de_inc = de + d16  # TODO: what if the result goes above 0xFFFF?

        self.E = de_inc & 0x00ff
        self.D = (de_inc >> 8) & 0x00ff

    def add_hl(self, d16):
        """
        Adds d16 to the current HL values.
        :param d16: Hex value to add
        """
        hl = (self.H << 8) | self.L  # TODO: Little or Big-Endian? Currently H=high/L=low, but it might be the opposite

        hl_inc = hl + d16  # TODO: what if the result goes above 0xFFFF?

        self.L = hl_inc & 0x00ff
        self.H = (hl_inc >> 8) & 0x00ff

    # SUB methods for 16-bit register combinations
    def sub_af(self, d16):
        """
        Subtracts d16 of the current AF values.
        :param d16: Hex value to subtract
        """
        af = (self.A << 8) | self.F  # TODO: Little or Big-Endian? Currently A=high/F=low, but it might be the opposite

        af_sub = abs(af - d16)  # TODO: what if the result goes below 0x0000?

        self.F = af_sub & 0x00ff
        self.A = (af_sub >> 8) & 0x00ff

    def sub_bc(self, d16):
        """
        Subtracts d16 of the current BC values.
        :param d16: Hex value to subtract
        """
        bc = (self.B << 8) | self.C  # TODO: Little or Big-Endian? Currently B=high/C=low, but it might be the opposite

        bc_sub = abs(bc - d16)  # TODO: what if the result goes below 0x0000?

        self.C = bc_sub & 0x00ff
        self.B = (bc_sub >> 8) & 0x00ff

    def sub_de(self, d16):
        """
        Subtracts d16 of the current DE values.
        :param d16: Hex value to subtract
        """
        de = (self.D << 8) | self.E  # TODO: Little or Big-Endian? Currently D=high/E=low, but it might be the opposite

        de_sub = abs(de - d16)  # TODO: what if the result goes below 0x0000?

        self.E = de_sub & 0x00ff
        self.D = (de_sub >> 8) & 0x00ff

    def sub_hl(self, d16):
        """
        Subtracts d16 of the current HL values.
        :param d16: Hex value to subtract
        """
        hl = (self.H << 8) | self.L  # TODO: Little or Big-Endian? Currently H=high/L=low, but it might be the opposite

        hl_sub = abs(hl - d16)  # TODO: what if the result goes below 0x0000?

        self.L = hl_sub & 0x00ff
        self.H = (hl_sub >> 8) & 0x00ff
