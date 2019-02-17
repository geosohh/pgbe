"""
GameBoy GPU

Drawing begins on the top left, and is done one line at a time.

See:
- https://realboyemulator.files.wordpress.com/2013/01/gbcpuman.pdf
- http://imrannazar.com/GameBoy-Emulation-in-JavaScript:-GPU-Timings
- http://imrannazar.com/GameBoy-Emulation-in-JavaScript:-Graphics
"""
from log import Log


class GPU:
    """ GB GPU """

    # Helper values
    SCREEN_WIDTH = 160
    SCREEN_HEIGHT = 144
    RGB_SIZE = 3  # R, G and B = 3
    RGB_LINE_SIZE = SCREEN_WIDTH * RGB_SIZE
    TILE_MAP_ADDRESS = {0: 0x9800,
                        1: 0x9C00}  # Memory address where each tile map begins
    TILE_SET_ADDRESS = {0: 0x8800,
                        1: 0x8000}  # Memory address where each tile set begins
    UPDATE_HZ = 70224  # (Modes 2, 3 and 0 * 144 lines) + (Mode 1 * 10 loops)

    # Used when LCD is disabled. To avoid confusion, we will display a blue screen.
    FRAME_LINE_LCD_DISABLED = [0, 0, 255] * SCREEN_WIDTH
    FRAME_LINE_BACKGROUND_DISABLED = [255, 255, 255] * SCREEN_WIDTH

    def __init__(self, gb):
        """
        :type gb: gb.GB
        """
        # Logger
        self.logger = Log()

        # Communication with other components
        self.gb = gb

        # State initialization
        self.cpu_cycles = 0  # Used as a unit of measurement for gpu timing
        self.framebuffer = [0, 0, 0] * (self.SCREEN_WIDTH * self.SCREEN_HEIGHT)  # Data being prepared to show on UI

    def prepare(self):
        """ Init code that cannot be executed on __init__ because not everything is initialized yet """
        LCD_STATUS.set_lcd_controller_mode(self.gb.memory, 2)

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

        mode = LCD_STATUS.lcd_controller_mode
        if mode == 2:
            # The LCD controller is reading from OAM memory.
            # The CPU <cannot> access OAM memory (FE00h-FE9Fh) during this period.
            if self.cpu_cycles >= 80:
                LCD_STATUS.set_lcd_controller_mode(self.gb.memory, 3)
                self.cpu_cycles -= 80
        elif mode == 3:
            # The LCD controller is reading from both OAM and VRAM.
            # The CPU <cannot> access OAM and VRAM during this period.
            if self.cpu_cycles >= 172:
                self.copy_current_display_line_to_framebuffer()
                LCD_STATUS.set_lcd_controller_mode(self.gb.memory, 0)
                self.cpu_cycles -= 172
        elif mode == 0:
            # H-Blank: the controller is moving to the beginning of the next display line.
            # The CPU can access both the VRAM (8000h-9FFFh) and OAM (FE00h-FE9Fh).
            if self.cpu_cycles >= 204:
                next_line = LCD_Y_COORDINATE.go_to_next_line(self.gb.memory)
                if next_line == 144:  # Last screen line (144 to 153 only happen during V-Blank state)
                    self.gb.screen.update(self.framebuffer)  # Draw framebuffer to screen
                    LCD_STATUS.set_lcd_controller_mode(self.gb.memory, 1)
                else:
                    LCD_STATUS.set_lcd_controller_mode(self.gb.memory, 2)
                self.cpu_cycles -= 204
        elif mode == 1:
            # V-Blank: the controller finished drawing the frame and is now moving back to the display's top-left.
            # The CPU can access both the display RAM (8000h-9FFFh) and OAM (FE00h-FE9Fh).
            if self.cpu_cycles >= 456:  # takes 4560 cpu cycles, but divided as 10 gpu loops
                next_line = LCD_Y_COORDINATE.go_to_next_line(self.gb.memory)
                if next_line == 0:  # First line, so restart drawing cycle
                    LCD_STATUS.set_lcd_controller_mode(self.gb.memory, 2)
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
        current_display_line = LCD_Y_COORDINATE.value
        pos = current_display_line * self.RGB_LINE_SIZE
        if not LCD_CONTROL.lcd_display_enabled:
            # LCD is disabled, so to avoid confusion we will display a blue screen
            self.framebuffer[pos:pos + self.RGB_LINE_SIZE] = self.FRAME_LINE_LCD_DISABLED
        else:
            if not LCD_CONTROL.display_background:
                # If background drawing is disabled, it must be draw as white
                self.framebuffer[pos:pos + self.RGB_LINE_SIZE] = self.FRAME_LINE_BACKGROUND_DISABLED
            else:
                y_background = SCROLL_Y.value + current_display_line
                y_tile_map = y_background // 8  # Each tile is 8 pixels tall (// = return int)
                if y_tile_map >= 32:
                    y_tile_map -= 32  # To wrap the background on screen
                tile_line = y_background % 8  # Which line of the tile we need to draw

                tile_map_row = self.gb.memory.get_map(LCD_CONTROL.background_tile_map)[y_tile_map]  # unsigned int

                x_tile_map = SCROLL_X.value // 8
                x_offset = SCROLL_X.value % 8
                pixel_count = 0
                while pixel_count < self.SCREEN_WIDTH:
                    tile_number = tile_map_row[x_tile_map]
                    tile_line_data = self.gb.memory.get_tile(LCD_CONTROL.tile_set_selected, tile_number)[tile_line]
                    if x_offset > 0:
                        tile_line_data = tile_line_data[x_offset:]
                        x_offset = 0
                    for pixel_value in tile_line_data:
                        if pixel_count < self.SCREEN_WIDTH:
                            self.framebuffer[pos:pos + self.RGB_SIZE] = self._apply_palette_transformation(pixel_value)
                            pixel_count += 1
                            pos += self.RGB_SIZE
                    x_tile_map += 1
                    if x_tile_map == 32:
                        x_tile_map = 0

    @staticmethod
    def update_gpu_register(address: int, value: int):
        """ Improve performance by updating internal data structures as soon as memory is changed """
        if address == LCD_CONTROL.ADDRESS:
            LCD_CONTROL.update(value)
        elif address == LCD_STATUS.ADDRESS:
            LCD_STATUS.update(value)
        elif address == SCROLL_Y.ADDRESS:
            SCROLL_Y.update(value)
        elif address == SCROLL_X.ADDRESS:
            SCROLL_X.update(value)
        elif address == LCD_Y_COORDINATE.ADDRESS:
            LCD_Y_COORDINATE.update(value)
        elif address == BACKGROUND_PALETTE.ADDRESS:
            BACKGROUND_PALETTE.update(value)

    @staticmethod
    def _apply_palette_transformation(base_color: int):
        """
        Converts the default color value from a pixel into the correct one based on the palette being applied.
        Bit 7-6 - Shade for Color Number 3
        Bit 5-4 - Shade for Color Number 2
        Bit 3-2 - Shade for Color Number 1
        Bit 1-0 - Shade for Color Number 0
        The four possible gray shades are: 0=White, 1=Light gray, 2=Dark gray, 3=Black
        :return:  Tuple with correct color based on palette
        """
        return BACKGROUND_PALETTE.color[base_color]

    def debug(self):
        """
        Prints debug info to console.
        """
        current_lcd_line = LCD_Y_COORDINATE.value
        mode = LCD_STATUS.lcd_controller_mode
        self.logger.debug("Mode: %i\tLY(FF44): %i\tCycles: %i",mode,current_lcd_line,self.cpu_cycles)


# noinspection PyPep8Naming
class LCD_CONTROL:
    """ 0xFF40 - LCDC - LCD CONTROL register """

    ADDRESS = 0xFF40

    lcd_display_enabled = False  # 7
    window_tile_map = 0  # 6
    display_window = False  # 5
    tile_set_selected = 0  # 4
    background_tile_map = 0  # 3
    sprite_size = 0  # 2
    display_sprites = False  # 1
    display_background = False  # 0

    @staticmethod
    def update(new_register_value: int):
        """ Update internal values according to new register value set """
        LCD_CONTROL.lcd_display_enabled = LCD_CONTROL._lcd_display_enabled(new_register_value)
        LCD_CONTROL.window_tile_map = LCD_CONTROL._window_tile_map(new_register_value)
        LCD_CONTROL.display_window = LCD_CONTROL._display_window(new_register_value)
        LCD_CONTROL.tile_set_selected = LCD_CONTROL._tile_set_selected(new_register_value)
        LCD_CONTROL.background_tile_map = LCD_CONTROL._background_tile_map(new_register_value)
        LCD_CONTROL.sprite_size = LCD_CONTROL._sprite_size(new_register_value)
        LCD_CONTROL.display_sprites = LCD_CONTROL._display_sprites(new_register_value)
        LCD_CONTROL.display_background = LCD_CONTROL._display_background(new_register_value)

    @staticmethod
    def _lcd_display_enabled(lcd_control_byte: int):
        """ :return: True if LCD is enabled, False otherwise """
        return ((lcd_control_byte & 0b10000000) >> 7) == 1  # 0=Off, 1=On

    @staticmethod
    def _window_tile_map(lcd_control_byte: int):
        """ :return: Tile map selected for window """
        return (lcd_control_byte & 0b01000000) >> 6

    @staticmethod
    def _display_window(lcd_control_byte: int):
        """ :return: True if window must be drawn, False otherwise """
        return ((lcd_control_byte & 0b00100000) >> 5) == 1  # 0=Off, 1=On

    @staticmethod
    def _tile_set_selected(lcd_control_byte: int):
        """ :return: Tile set selected for background/window (sprites always use tile set 0) """
        return (lcd_control_byte & 0b00010000) >> 4

    @staticmethod
    def _background_tile_map(lcd_control_byte: int):
        """ :return: Tile map selected for background """
        return (lcd_control_byte & 0b00001000) >> 3

    @staticmethod
    def _sprite_size(lcd_control_byte: int):
        """ :return: Size of sprites """
        return (lcd_control_byte & 0b00000100) >> 2

    @staticmethod
    def _display_sprites(lcd_control_byte: int):
        """ :return: True if sprites must be drawn, False otherwise """
        return ((lcd_control_byte & 0b00000010) >> 1) == 1  # 0=Off, 1=On

    @staticmethod
    def _display_background(lcd_control_byte: int):
        """ :return: True if background must be drawn, False otherwise """
        return (lcd_control_byte & 0b00000001) == 1  # 0=Off, 1=On


# noinspection PyPep8Naming
class LCD_STATUS:
    """ 0xFF41 - STAT - LCD STATUS register """

    ADDRESS = 0xFF41

    lcd_controller_mode = 0

    @staticmethod
    def update(new_register_value: int):
        """ Update internal values according to new register value set """
        LCD_STATUS.lcd_controller_mode = LCD_STATUS._lcd_controller_mode(new_register_value)

    @staticmethod
    def _lcd_controller_mode(lcd_stat_byte: int):
        """ :return Current state of the LCD controller. Goes from 0 to 3. """
        return lcd_stat_byte & 0b00000011

    @staticmethod
    def set_lcd_controller_mode(memory, new_mode: int):
        """ Simulate display processing mode change """
        lcd_stat_byte = memory.read_8bit(LCD_STATUS.ADDRESS)
        new_lcd_stat_byte = (lcd_stat_byte & 0b11111100) | new_mode
        memory.write_8bit(LCD_STATUS.ADDRESS, new_lcd_stat_byte)  # Memory will call the update() method


# noinspection PyPep8Naming
class SCROLL_Y:
    """ 0xFF42 - SCY - SCROLL Y register """

    ADDRESS = 0xFF42

    value = 0

    @staticmethod
    def update(new_register_value: int):
        """ Update internal values according to new register value set """
        SCROLL_Y.value = new_register_value


# noinspection PyPep8Naming
class SCROLL_X:
    """ 0xFF43 - SCX - SCROLL X register """

    ADDRESS = 0xFF43

    value = 0

    @staticmethod
    def update(new_register_value: int):
        """ Update internal values according to new register value set """
        SCROLL_X.value = new_register_value


# noinspection PyPep8Naming
class LCD_Y_COORDINATE:
    """ 0xFF44 - LY - LCD Y COORDINATE register """

    ADDRESS = 0xFF44

    value = 0

    @staticmethod
    def update(new_register_value: int):
        """ Update internal values according to new register value set """
        LCD_Y_COORDINATE.value = new_register_value

    @staticmethod
    def go_to_next_line(memory):
        """
        Simulate display processing line change.
        :return Number of the next line that will start processing now
        """
        current_line = LCD_Y_COORDINATE.value
        if current_line == 153:
            new_line = 0
        else:
            new_line = current_line + 1
        memory.write_8bit(LCD_Y_COORDINATE.ADDRESS,new_line)
        return new_line


# noinspection PyPep8Naming
class BACKGROUND_PALETTE:
    """ 0xFF47 - BGP - BACKGROUND PALETTE register """

    ADDRESS = 0xFF47

    _DISPLAY_COLORS = {0: [255, 255, 255],
                       1: [192, 192, 192],
                       2: [96, 96, 96],
                       3: [0, 0, 0]}  # colors displayed by the GameBoy

    color = [_DISPLAY_COLORS[0],
             _DISPLAY_COLORS[1],
             _DISPLAY_COLORS[2],
             _DISPLAY_COLORS[3]]

    @staticmethod
    def update(new_register_value: int):
        """ Update internal values according to new register value set """
        for i in range(4):
            correct_color = (new_register_value >> (i * 2)) & 0b00000011
            BACKGROUND_PALETTE.color[i] = BACKGROUND_PALETTE._DISPLAY_COLORS[correct_color]
