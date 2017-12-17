class Register:
    """
    
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
