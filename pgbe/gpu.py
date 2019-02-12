"""
GameBoy GPU

Drawing begins on the top left, and is done one line at a time.

See:
- https://realboyemulator.files.wordpress.com/2013/01/gbcpuman.pdf
- http://imrannazar.com/GameBoy-Emulation-in-JavaScript:-GPU-Timings
- http://imrannazar.com/GameBoy-Emulation-in-JavaScript:-Graphics
"""
import logging
import util


class GPU:
    """ GB GPU """

    # Helper values
    SCREEN_WIDTH = 160
    SCREEN_HEIGHT = 144
    RGB_SIZE = 3  # R, G and B = 3
    DISPLAY_COLORS = {0: [255, 255, 255],
                      1: [192, 192, 192],
                      2: [96, 96, 96],
                      3: [0, 0, 0]}  # colors displayed by the GameBoy
    TILE_MAP_ADDRESS = {0: 0x9800,
                        1: 0x9C00}  # Memory address where each tile map begins
    TILE_SET_ADDRESS = {0: 0x8800,
                        1: 0x8000}  # Memory address where each tile set begins
    UPDATE_HZ = 70224  # (Modes 2, 3 and 0 * 144 lines) + (Mode 1 * 10 loops)

    # GB Memory addresses
    LCD_CONTROL_ADDRESS = 0xFF40  # also called LCDC
    LCD_STATUS_ADDRESS = 0xFF41  # also called STAT
    SCROLL_Y_ADDRESS = 0xFF42  # also called SCY
    SCROLL_X_ADDRESS = 0xFF43  # also called SCX
    LCD_Y_COORDINATE_ADDRESS = 0xFF44  # also called LY
    BACKGROUND_PALETTE_DATA_ADDRESS = 0xFF47  # also called BGP

    def __init__(self, gb):
        """
        :type gb: gb.GB
        """
        # Logger
        self.logger = logging.getLogger("pgbe")

        # Communication with other components
        self.gb = gb

        # State initialization
        self.cpu_cycles = 0  # Used as a unit of measurement for gpu timing
        self._set_lcd_controller_mode(2)

        self.framebuffer = [0, 0, 0] * (self.SCREEN_WIDTH * self.SCREEN_HEIGHT)  # Data being prepared to show on UI
        self.screen = self.framebuffer.copy()  # Data to show on UI

    def update(self, cpu_cycles_spent: int):
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

        :return If the full GPU update cycle has finished executing (i.e. a frame is ready to be shown on screen)
        """
        full_update_cycle_completed = False
        self.cpu_cycles += cpu_cycles_spent

        mode = self._lcd_controller_mode()
        if mode == 2:
            # The LCD controller is reading from OAM memory.
            # The CPU <cannot> access OAM memory (FE00h-FE9Fh) during this period.
            if self.cpu_cycles >= 80:
                self._set_lcd_controller_mode(3)
                self.cpu_cycles -= 80
        elif mode == 3:
            # The LCD controller is reading from both OAM and VRAM.
            # The CPU <cannot> access OAM and VRAM during this period.
            if self.cpu_cycles >= 172:
                self.copy_current_display_line_to_framebuffer()
                self._set_lcd_controller_mode(0)
                self.cpu_cycles -= 172
        elif mode == 0:
            # H-Blank: the controller is moving to the beginning of the next display line.
            # The CPU can access both the VRAM (8000h-9FFFh) and OAM (FE00h-FE9Fh).
            if self.cpu_cycles >= 204:
                next_line = self._go_to_next_lcd_y_line()
                if next_line == 144:  # Last screen line (144 to 153 only happen during V-Blank state)
                    self.screen = self.framebuffer.copy()  # Draw framebuffer to screen
                    self._set_lcd_controller_mode(1)
                else:
                    self._set_lcd_controller_mode(2)
                self.cpu_cycles -= 204
        elif mode == 1:
            # V-Blank: the controller finished drawing the frame and is now moving back to the display's top-left.
            # The CPU can access both the display RAM (8000h-9FFFh) and OAM (FE00h-FE9Fh).
            if self.cpu_cycles >= 456:  # takes 4560 cpu cycles, but divided as 10 gpu loops
                next_line = self._go_to_next_lcd_y_line()
                if next_line == 0:  # First line, so restart drawing cycle
                    self._set_lcd_controller_mode(2)
                    full_update_cycle_completed = True
                self.cpu_cycles -= 456

        return full_update_cycle_completed

    def copy_current_display_line_to_framebuffer(self):
        """
        Calculates and adds to framebuffer the pixels that must be drawn in a specific display line.

        What is drawn depends on the flags set in the LCDC memory address. There are 3 elements: background, window and
        sprites. Background is 32x32 tiles (256x256 pixels). Since it is larger than the screen it is possible to scroll
        around the image in order to show what is needed. Also, the background wraps around if the input coordinates go
        over the image size. This method only adds to the framebuffer a single pixel line, so we need to calculate the
        offsets required in order to draw the correct data.

        See:
        - http://imrannazar.com/GameBoy-Emulation-in-JavaScript:-Graphics
        - https://realboyemulator.files.wordpress.com/2013/01/gbcpuman.pdf
        - http://www.codeslinger.co.uk/pages/projects/gameboy/graphics.html
        """
        # TODO: This method works but is WAY TOO SLOW... Process for all 144 lines is taking about 3s...
        current_display_line = self.gb.memory.read_8bit(self.LCD_Y_COORDINATE_ADDRESS)
        if not self._lcd_display_enabled():
            # LCD is disabled, so to avoid confusion we will display a blue screen
            new_line = [0, 0, 255] * self.SCREEN_WIDTH
        else:
            tile_set = self._tile_set_selected()
            if not self._display_background():
                # If background drawing is disabled, it must be draw as white
                new_line = [255, 255, 255] * self.SCREEN_WIDTH
            else:
                display_vertical_offset = self._scroll_y()
                total_y = display_vertical_offset + current_display_line
                temp_tile_row = int(total_y/8)
                if temp_tile_row >= 32:
                    tile_row = temp_tile_row - 32  # To wrap the image on screen
                else:
                    tile_row = temp_tile_row
                bitmap_vertical_offset = total_y - temp_tile_row*8  # Define which line in the bitmap needs to be drawn
                tile_row_start_address_in_map = self.TILE_MAP_ADDRESS[self._background_tile_map()] + (tile_row * 32)

                display_horizontal_offset = self._scroll_x()
                tile_column = int(display_horizontal_offset/8)
                new_line = []
                while len(new_line) < self.SCREEN_WIDTH * self.RGB_SIZE:
                    tile = self.gb.memory.read_8bit(tile_row_start_address_in_map + tile_column)
                    if tile_set == 0:
                        # Tile set 0 is indexed from -128 to 127, so we need to transform it into a positive value
                        tile = util.convert_unsigned_integer_to_signed(tile) + 128
                    # Each full tile is 16 bytes and each tile line is 2 bytes, so skip to the proper address
                    tile_line_address = self.TILE_SET_ADDRESS[tile_set] + (tile*16) + (bitmap_vertical_offset*2)
                    tile_line_data_lsb = self.gb.memory.read_8bit(tile_line_address)
                    tile_line_data_msb = self.gb.memory.read_8bit(tile_line_address + 1)
                    for bit_index in range(7, -1, -1):
                        pixel_msb = (tile_line_data_msb >> bit_index) & 0b00000001
                        pixel_lsb = (tile_line_data_lsb >> bit_index) & 0b00000001
                        pixel_value = (pixel_msb << 1) | pixel_lsb
                        new_line += self._apply_palette_transformation(pixel_value)
                    tile_column += 1
                    if tile_column == 32:
                        tile_column = 0

        rgb_line_size = self.SCREEN_WIDTH*self.RGB_SIZE
        current_framebuffer_pos = current_display_line * rgb_line_size
        self.framebuffer[current_framebuffer_pos:current_framebuffer_pos+rgb_line_size] = new_line

    # LCD Control register
    def _lcd_display_enabled(self):
        """ :return: True if LCD is enabled, False otherwise """
        lcd_control_byte = self.gb.memory.read_8bit(self.LCD_CONTROL_ADDRESS)
        return ((lcd_control_byte & 0b10000000) >> 7) == 1  # 0=Off, 1=On

    def _window_tile_map(self):
        """ :return: Tile map selected for window """
        lcd_control_byte = self.gb.memory.read_8bit(self.LCD_CONTROL_ADDRESS)
        return (lcd_control_byte & 0b01000000) >> 6

    def _display_window(self):
        """ :return: True if window must be drawn, False otherwise """
        lcd_control_byte = self.gb.memory.read_8bit(self.LCD_CONTROL_ADDRESS)
        return ((lcd_control_byte & 0b00100000) >> 5) == 1  # 0=Off, 1=On

    def _tile_set_selected(self):
        """ :return: Tile set selected for background/window (sprites always use tile set 0) """
        lcd_control_byte = self.gb.memory.read_8bit(self.LCD_CONTROL_ADDRESS)
        return (lcd_control_byte & 0b00010000) >> 4

    def _background_tile_map(self):
        """ :return: Tile map selected for background """
        lcd_control_byte = self.gb.memory.read_8bit(self.LCD_CONTROL_ADDRESS)
        return (lcd_control_byte & 0b00001000) >> 3

    def _sprite_size(self):
        """ :return: Size of sprites """
        lcd_control_byte = self.gb.memory.read_8bit(self.LCD_CONTROL_ADDRESS)
        return (lcd_control_byte & 0b00000100) >> 2

    def _display_sprites(self):
        """ :return: True if sprites must be drawn, False otherwise """
        lcd_control_byte = self.gb.memory.read_8bit(self.LCD_CONTROL_ADDRESS)
        return ((lcd_control_byte & 0b00000010) >> 1) == 1  # 0=Off, 1=On

    def _display_background(self):
        """ :return: True if background must be drawn, False otherwise """
        lcd_control_byte = self.gb.memory.read_8bit(self.LCD_CONTROL_ADDRESS)
        return (lcd_control_byte & 0b00000001) == 1  # 0=Off, 1=On

    # LCD Status register
    def _lcd_controller_mode(self):
        """ :return Current state of the LCD controller. Goes from 0 to 3. """
        lcd_stat_byte = self.gb.memory.read_8bit(self.LCD_STATUS_ADDRESS)
        return lcd_stat_byte & 0b00000011

    def _set_lcd_controller_mode(self, new_mode: int):
        """ Simulate display processing mode change """
        lcd_stat_byte = self.gb.memory.read_8bit(self.LCD_STATUS_ADDRESS)
        new_lcd_stat_byte = (lcd_stat_byte & 0b11111100) | new_mode
        self.gb.memory.write_8bit(self.LCD_STATUS_ADDRESS,new_lcd_stat_byte)

    # LY register
    def _go_to_next_lcd_y_line(self):
        """
        Simulate display processing line change.
        :return Number of the next line that will start processing now
        """
        current_line = self.gb.memory.read_8bit(self.LCD_Y_COORDINATE_ADDRESS)
        if current_line == 153:
            new_line = 0
        else:
            new_line = current_line + 1
        self.gb.memory.write_8bit(self.LCD_Y_COORDINATE_ADDRESS,new_line)
        return new_line

    # SCY register
    def _scroll_y(self):
        """
        Used to scroll the background image, i.e. select the part of it that will be shown on screen.
        :return: Current Y offset
        """
        return self.gb.memory.read_8bit(self.SCROLL_Y_ADDRESS)

    # SCX register
    def _scroll_x(self):
        """
        Used to scroll the background image, i.e. select the part of it that will be shown on screen.
        :return: Current X offset
        """
        return self.gb.memory.read_8bit(self.SCROLL_X_ADDRESS)

    def _apply_palette_transformation(self, base_color: int):
        """
        Converts the default color value from a pixel into the correct one based on the palette being applied.
        Bit 7-6 - Shade for Color Number 3
        Bit 5-4 - Shade for Color Number 2
        Bit 3-2 - Shade for Color Number 1
        Bit 1-0 - Shade for Color Number 0
        The four possible gray shades are: 0=White, 1=Light gray, 2=Dark gray, 3=Black
        :return:  Tuple with correct color based on palette
        """
        palette = self.gb.memory.read_8bit(self.BACKGROUND_PALETTE_DATA_ADDRESS)
        correct_color = (palette >> (base_color*2)) & 0b00000011
        return self.DISPLAY_COLORS[correct_color]

    def debug(self):
        """
        Prints debug info to console.
        """
        current_lcd_line = self.gb.memory.read_8bit(self.LCD_Y_COORDINATE_ADDRESS)
        mode = self._lcd_controller_mode()
        self.logger.debug("Mode: %i\tLY(FF44): %i\tCycles: %i",mode,current_lcd_line,self.cpu_cycles)
