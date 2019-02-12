"""
Interrupts

IME - Interrupt Master Enable
    Global enable/disable of interrupts, no matter what the ENABLED_FLAG says. Hardware clears the IME flag as a
    result of servicing an interrupt, and sets it as a result of returning from an interrupt.

ENABLED_FLAG - Tells the CPU what devices the game is interested in receiving interrupts from.

REQUESTS_FLAG - Set to 1 by the hardware to signal that an interrupt occurred.

See:
- http://gbdev.gg8.se/wiki/articles/Interrupts
- http://gbdev.gg8.se/files/docs/mirrors/pandocs.html#interrupts
- https://realboyemulator.wordpress.com/2013/01/18/emulating-the-core-2/
- https://realboyemulator.wordpress.com/2013/07/01/interrupt-processing-a-real-world-example/
"""
import logging


class Interrupts:
    """ Interrupts """
    
    REQUESTS_FLAG_ADDRESS = 0xFF0F
    ENABLED_FLAG_ADDRESS = 0xFFFF
    
    V_BLANK_HANDLER = 0x0040
    LCD_STAT_HANDLER = 0x0048
    TIMER_HANDLER = 0x0050
    SERIAL_HANDLER = 0x0058
    JOYPAD_HANDLER = 0x0060
    
    def __init__(self, gb):
        """
        :type gb: gb.GB
        """
        # Logger
        self.logger = logging.getLogger("pgbe")

        # Communication with other components
        self.gb = gb

        # State initialization
        self.IME = False
        self.enable_IME_after_next_instruction = False
        self.disable_IME_after_next_instruction = False

    def update(self, opcode_executed: int):
        """
        Executed after each instruction. Update the status of interrupts and makes the required changes when an
        interrupt must be fired.

        :param opcode_executed: Used to update IME flag
        :return Number of cycles spent
        """
        cycles_spent = 0
        if self.enable_IME_after_next_instruction or opcode_executed == 0xD9:  # RETI - Same as EI,RET
            self.enable_IME_after_next_instruction = False
            self.IME = True
        if self.disable_IME_after_next_instruction:
            self.disable_IME_after_next_instruction = False
            self.IME = False
        
        if self.IME:
            if self.v_blank_requested() and self.v_blank_enabled():
                self.IME = False  # Disable interrupts
                self.set_v_blank_requested_flag(False)  # Interrupt request is being handled, so disable flag
                self._push_current_address_to_stack()
                self.gb.cpu.register.PC = self.V_BLANK_HANDLER
                self.gb.cpu.halted = False
                cycles_spent = 5
            elif self.lcd_stat_requested() and self.lcd_stat_enabled():
                self.IME = False  # Disable interrupts
                self.set_lcd_stat_requested_flag(False)  # Interrupt request is being handled, so disable flag
                self._push_current_address_to_stack()
                self.gb.cpu.register.PC = self.LCD_STAT_HANDLER
                self.gb.cpu.halted = False
                cycles_spent = 5
            elif self.timer_requested() and self.timer_enabled():
                self.IME = False  # Disable interrupts
                self.set_timer_requested_flag(False)  # Interrupt request is being handled, so disable flag
                self._push_current_address_to_stack()
                self.gb.cpu.register.PC = self.TIMER_HANDLER
                self.gb.cpu.halted = False
                cycles_spent = 5
            elif self.serial_requested() and self.serial_enabled():
                self.IME = False  # Disable interrupts
                self.set_serial_requested_flag(False)  # Interrupt request is being handled, so disable flag
                self._push_current_address_to_stack()
                self.gb.cpu.register.PC = self.SERIAL_HANDLER
                self.gb.cpu.halted = False
                cycles_spent = 5
            elif self.joypad_requested() and self.joypad_enabled():
                self.IME = False  # Disable interrupts
                self.set_joypad_requested_flag(False)  # Interrupt request is being handled, so disable flag
                self._push_current_address_to_stack()
                self.gb.cpu.register.PC = self.JOYPAD_HANDLER
                self.gb.cpu.halted = False
                cycles_spent = 5

        # Prepare for next update cycle
        if opcode_executed == 0xFB:  # EI - Enable interrupts after next instruction is executed
            self.enable_IME_after_next_instruction = True
        if opcode_executed == 0xF3:  # DI - Disable interrupts after next instruction is executed
            self.disable_IME_after_next_instruction = True

        return cycles_spent

    # Get Flags

    def _get_flag(self, address: int, bit_position: int):
        """
        Get specified flag bit.
        :param address: Address to read from memory
        :param bit_position: Flag to return
        """
        interrupt_flag_byte = self.gb.memory.read_8bit(address)
        mask = 1 << bit_position
        return (interrupt_flag_byte & mask) >> bit_position

    def v_blank_requested(self):
        """ Get V-Blank interrupt requested flag """
        return self._get_flag(self.REQUESTS_FLAG_ADDRESS,0)

    def lcd_stat_requested(self):
        """ Get LCD STAT interrupt requested flag """
        return self._get_flag(self.REQUESTS_FLAG_ADDRESS,1)

    def timer_requested(self):
        """ Get Timer interrupt requested flag """
        return self._get_flag(self.REQUESTS_FLAG_ADDRESS,2)

    def serial_requested(self):
        """ Get Serial interrupt requested flag """
        return self._get_flag(self.REQUESTS_FLAG_ADDRESS,3)

    def joypad_requested(self):
        """ Get Joypad interrupt requested flag """
        return self._get_flag(self.REQUESTS_FLAG_ADDRESS,4)

    def v_blank_enabled(self):
        """ Get V-Blank interrupt enabled flag """
        return self._get_flag(self.ENABLED_FLAG_ADDRESS,0)

    def lcd_stat_enabled(self):
        """ Get LCD STAT interrupt enabled flag """
        return self._get_flag(self.ENABLED_FLAG_ADDRESS,1)

    def timer_enabled(self):
        """ Get Timer interrupt enabled flag """
        return self._get_flag(self.ENABLED_FLAG_ADDRESS,2)

    def serial_enabled(self):
        """ Get Serial interrupt enabled flag """
        return self._get_flag(self.ENABLED_FLAG_ADDRESS,3)

    def joypad_enabled(self):
        """ Get Joypad interrupt enabled flag """
        return self._get_flag(self.ENABLED_FLAG_ADDRESS,4)

    # Set Flags

    def _set_flag(self, address: int, bit_position: int, new_value: int):
        """
        Change specified flag bit in register F.
        :param address: Address to write in memory
        :param bit_position: Bit to change
        :param new_value: New value for specified bit
        """
        interrupt_flag_byte = self.gb.memory.read_8bit(address)
        new_value = int(new_value)  # True == 1; False == 0
        mask = 1 << bit_position
        if (interrupt_flag_byte & mask) != (new_value << bit_position):  # If current value != new_value, flip current
            interrupt_flag_byte = interrupt_flag_byte ^ mask
            self.gb.memory.write_8bit(address,interrupt_flag_byte)

    def set_v_blank_requested_flag(self, new_value: int):
        """ Set V-Blank interrupt requested flag """
        self._set_flag(self.REQUESTS_FLAG_ADDRESS,0,new_value)

    def set_lcd_stat_requested_flag(self, new_value: int):
        """ Set LCD STAT interrupt requested flag """
        self._set_flag(self.REQUESTS_FLAG_ADDRESS,1,new_value)

    def set_timer_requested_flag(self, new_value: int):
        """ Set Timer interrupt requested flag """
        self._set_flag(self.REQUESTS_FLAG_ADDRESS,2,new_value)

    def set_serial_requested_flag(self, new_value: int):
        """ Set Serial interrupt requested flag """
        self._set_flag(self.REQUESTS_FLAG_ADDRESS,3,new_value)

    def set_joypad_requested_flag(self, new_value: int):
        """ Set Joypad interrupt requested flag """
        self._set_flag(self.REQUESTS_FLAG_ADDRESS,4,new_value)

    def set_v_blank_enabled_flag(self,  new_value: int):
        """ Set V-Blank interrupt enabled flag """
        self._set_flag(self.ENABLED_FLAG_ADDRESS,0,new_value)

    def set_lcd_stat_enabled_flag(self,  new_value: int):
        """ Set LCD STAT interrupt enabled flag """
        self._set_flag(self.ENABLED_FLAG_ADDRESS,1,new_value)

    def set_timer_enabled_flag(self,  new_value: int):
        """ Set Timer interrupt enabled flag """
        self._set_flag(self.ENABLED_FLAG_ADDRESS,2,new_value)

    def set_serial_enabled_flag(self,  new_value: int):
        """ Set Serial interrupt enabled flag """
        self._set_flag(self.ENABLED_FLAG_ADDRESS,3,new_value)

    def set_joypad_enabled_flag(self,  new_value: int):
        """ Set Joypad interrupt enabled flag """
        self._set_flag(self.ENABLED_FLAG_ADDRESS,4,new_value)

    # Interrupt handling util

    def _push_current_address_to_stack(self):
        """ Push current address to stack so game knows where to return to after handling interrupt """
        self.gb.cpu.register.SP = (self.gb.cpu.register.SP - 2) & 0xFFFF  # Increase stack
        self.gb.memory.write_16bit(
            self.gb.cpu.register.SP, self.gb.cpu.register.PC)  # Store PC into new stack element

    def debug(self):
        """
        Prints debug info to console.
        """
        requests_byte = "{:08b}".format(self.gb.memory.read_8bit(self.REQUESTS_FLAG_ADDRESS))
        enabled_byte = "{:08b}".format(self.gb.memory.read_8bit(self.ENABLED_FLAG_ADDRESS))
        self.logger.debug("IEM: %s\tRequests(IF@FF0F): %s\tEnabled(IE@FFFF): %s\tEnable_next: %s\tDisable_next: %s",
                          self.IME,requests_byte,enabled_byte,self.enable_IME_after_next_instruction,
                          self.disable_IME_after_next_instruction)
