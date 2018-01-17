"""
Video function
"""


class GPU:
    """
    Game Boy GPU

    Drawing begins on the top left, and is done one line at a time.

    See:
    - https://realboyemulator.files.wordpress.com/2013/01/gbcpuman.pdf
    - http://imrannazar.com/GameBoy-Emulation-in-JavaScript:-GPU-Timings
    """

    LCD_STAT_IO_ADDRESS = 0xFF41  # also called STAT
    SCROLL_Y_ADDRESS = 0xFF42  # also called SCY
    SCROLL_X_ADDRESS = 0xFF43  # also called SCX
    LCD_Y_COORDINATE_ADDRESS = 0xFF44  # also called LY

    def __init__(self,cpu):
        self.cpu = cpu  # To access/modify gpu-related memory
        self.cpu_cycles = 0  # Used as a unit of measurement for gpu timing

        self.set_lcd_controller_mode(2)

    def update(self,cpu_cycles_spent):
        """
        Executed after each instruction. Update the status of gpu and makes the required changes.

        Display update progress according to LCD controller mode (0, 1, 2 or 3):
        Mode 2  ...2_____2_____2_____2_____... one cycle ...2______________________________... mode 1 ...2_____...
        Mode 3  ..._33____33____33____33___... for each  ..._33____________________________... lasts  ..._33___...
        Mode 0  ...___000___000___000___000...  of the   ...___000_________________________... for 10 ...___000...
        Mode 1  ...________________________... 144 lines ...______1111111111111111111111111... loops  ...______...

        See:
        - http://imrannazar.com/GameBoy-Emulation-in-JavaScript:-GPU-Timings
        - http://gbdev.gg8.se/files/docs/mirrors/pandocs.html#videodisplay

        :param cpu_cycles_spent: Number of cycles executed during last CPU update.
        """
        self.cpu_cycles += cpu_cycles_spent

        mode = self.lcd_controller_mode()
        if mode == 2:
            # The LCD controller is reading from OAM memory.
            # The CPU <cannot> access OAM memory (FE00h-FE9Fh) during this period.
            if self.cpu_cycles >= 80:
                self.set_lcd_controller_mode(3)
                self.cpu_cycles -= 80
        elif mode == 3:
            # The LCD controller is reading from both OAM and VRAM.
            # The CPU <cannot> access OAM and VRAM during this period.
            if self.cpu_cycles >= 172:
                # TODO: write the current display line to the framebuffer
                self.set_lcd_controller_mode(0)
                self.cpu_cycles -= 172
        elif mode == 0:
            # H-Blank: the controller is moving to the beginning of the next display line.
            # The CPU can access both the display RAM (8000h-9FFFh) and OAM (FE00h-FE9Fh).
            if self.cpu_cycles >= 204:
                next_line = self.go_to_next_lcd_y_line()
                if next_line == 143:  # Last screen line (144 to 153 only happen during V-Blank state)
                    # TODO: draw framebuffer to screen
                    self.set_lcd_controller_mode(1)
                else:
                    self.set_lcd_controller_mode(2)
                self.cpu_cycles -= 204
        elif mode == 1:
            # V-Blank: the controller finished drawing the frame and is now moving back to the display's top-left.
            # The CPU can access both the display RAM (8000h-9FFFh) and OAM (FE00h-FE9Fh).
            if self.cpu_cycles >= 456:  # takes 4560 cpu cycles, but divided as 10 gpu loops
                next_line = self.go_to_next_lcd_y_line()
                if next_line == 0:  # First line, so restart drawing cycle
                    self.set_lcd_controller_mode(2)
                self.cpu_cycles -= 456

    # STAT register
    def lcd_controller_mode(self):
        """ :return Current state of the LCD controller. Goes from 0 to 3. """
        lcd_stat_byte = self.cpu.memory.read_8bit(self.LCD_STAT_IO_ADDRESS)
        return lcd_stat_byte & 0b00000011

    def set_lcd_controller_mode(self,new_mode):
        """ Simulate display processing mode change """
        lcd_stat_byte = self.cpu.memory.read_8bit(self.LCD_STAT_IO_ADDRESS)
        new_lcd_stat_byte = (lcd_stat_byte & 0b11111100) | new_mode
        self.cpu.memory.write_8bit(self.LCD_STAT_IO_ADDRESS,new_lcd_stat_byte)

    # LY register
    def go_to_next_lcd_y_line(self):
        """
        Simulate display processing line change.
        :return Number of the next line that will start processing now
        """
        current_line = self.cpu.memory.read_8bit(self.LCD_Y_COORDINATE_ADDRESS)
        if current_line == 153:
            new_line = 0
        else:
            new_line = current_line + 1
        self.cpu.memory.write_8bit(self.LCD_Y_COORDINATE_ADDRESS,new_line)
        return new_line

    # SCY register
    def scroll_y(self):
        """
        Used to scroll the background image, i.e. select the part of it that will be shown on screen.
        :return: Current Y offset
        """
        return self.cpu.memory.read_8bit(self.SCROLL_Y_ADDRESS)

    # SCX register
    def scroll_x(self):
        """
        Used to scroll the background image, i.e. select the part of it that will be shown on screen.
        :return: Current X offset
        """
        return self.cpu.memory.read_8bit(self.SCROLL_X_ADDRESS)

    def debug(self):
        """
        Prints debug info to console.
        """
        current_lcd_line = self.cpu.memory.read_8bit(self.LCD_Y_COORDINATE_ADDRESS)
        mode = self.lcd_controller_mode()
        self.cpu.logger.debug("Mode: %i\tLY(FF44): %i\tCycles: %i",mode,current_lcd_line,self.cpu_cycles)


import tkinter


def create_window():
    top = tkinter.Tk()
    w = tkinter.Canvas(top,width=160,height=144)
    top.mainloop()


if __name__ == '__main__':
    create_window()