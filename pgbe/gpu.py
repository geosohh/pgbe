"""
Video function
"""


import pyglet


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
    BACKGROUND_PALETTE_DATA_ADDRESS = 0xFF47  # also called BGP

    DISPLAY_COLORS = {0:(255,255,255), 1:(192,192,192), 2:(96,96,96), 3:(0,0,0)}  # colors displayed by the game boy

    def __init__(self,cpu):
        self.cpu = cpu  # To access/modify gpu-related memory
        self.cpu_cycles = 0  # Used as a unit of measurement for gpu timing

        self.tile_data_set = self._init_tile_set(255)
        self.tile_image_set = self._init_tile_set(None)
        self.outdated_tile_image = self._init_outdated_tile_images()
        self._update_tile_images()

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
            # The CPU can access both the VRAM (8000h-9FFFh) and OAM (FE00h-FE9Fh).
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

    # Tile set
    @staticmethod
    def _init_tile_set(init_value):
        """
        Create data structure to store tile data.
        :param init_value: Value used to initialize all tiles
        :return: Dictionary with all tiles from both sets filed with init_value.
        """
        blank_tile_set = {0: {}, 1: {}}
        for t in range(0, 256):  # Tile set 1 is accessed by indexes 0 through 255
            blank_tile_set[1][t] = [init_value] * 8 * 8  # 8*8=Tile dimensions
        for t in range(-128, 128):  # Tile set 0 is accessed by indexes -128 through 127
            blank_tile_set[0][t] = [init_value] * 8 * 8  # 8*8=Tile dimensions
        return blank_tile_set

    @staticmethod
    def _init_outdated_tile_images():
        """
        Create data structure to store information about outdated tile images.
        :return: Dictionary with all tiles from both sets added, meaning that all tile images must be generated again.
        """
        blank_tile_set = {0:set(), 1:set()}
        for t in range(0, 256):  # Tile set 1 is accessed by indexes 0 through 255
            blank_tile_set[1].add(t)
        for t in range(-128, 128):  # Tile set 0 is accessed by indexes -128 through 127
            blank_tile_set[0].add(t)
        return blank_tile_set

    def update_tile_set(self,set_index):
        """
        Update all tiles from the given tile set. Used after loading a save state.
        :param set_index: Tile set to be updated.
        """
        for tile_index in range(256):
            for line_index in range(8):
                self._update_tile(set_index,tile_index,line_index)

    def update_tile_at_address(self,address):
        """
        Given a memory address in VRAM, calculate which tile has been modified and request it to be updated.
        :param address:
        :return:
        """
        set_index = 1 if address <= 0x8BFF else 0
        offset = 0x8000 if set_index == 1 else 0x8800
        address -= offset
        tile_index = address / 16  # 16 == 2*8 -> number_of_bytes_per_line * lines_in_a_tile
        line_index = (address - (tile_index * 16)) / 2
        self._update_tile(set_index,tile_index,line_index)

    def _update_tile(self,set_index, tile_index, line_index):
        """
        Update the emulator's tile data. Called after the VRAM memory is modified. The specified tile will be added to
        the list of outdated tiles, so that the tile image is generated again later.

        :param set_index: Which set to update
        :param tile_index: Which tile to update
        :param line_index: Which line to update
        """
        memory_offset = 0x8000 if set_index == 1 else 0x8800
        line_lsb_address = memory_offset + (tile_index*16) + (line_index*2)
        line_msb_address = line_lsb_address + 1
        line_lsb = self.cpu.memory.read_8bit(line_lsb_address)
        line_msb = self.cpu.memory.read_8bit(line_msb_address)

        if set_index == 0:  # tile_set contains a value from 0 to 255, but tile set 0 indexes are from -128 to 127
            tile_index -= 128

        pixel_count = 0
        for bit_index in range(7,-1,-1):
            pixel_msb = (line_msb >> bit_index) & 0b00000001
            pixel_lsb = (line_lsb >> bit_index) & 0b00000001
            pixel_value = (pixel_msb << 1) | pixel_lsb
            self.tile_data_set[set_index][tile_index][(8*line_index) + pixel_count] = pixel_value
            pixel_count += 1

        self.outdated_tile_image[set_index].add(tile_index)

    def _update_tile_images(self):
        """
        Convert tiles data into images using pyglet image structure.
        See: https://gamedev.stackexchange.com/questions/55945/how-to-draw-image-in-memory-manually-in-pyglet
        """
        for set_index in self.outdated_tile_image:
            for tile_index in self.outdated_tile_image[set_index]:
                updated_tile = self.tile_data_set[set_index][tile_index]
                rgb_tile = [0]*(len(updated_tile)*3)  # *3 == RGB
                for i in range(len(updated_tile)):
                    rgb_i = i*3
                    rgb_tile[rgb_i:rgb_i+3] = self._apply_palette_transformation(updated_tile[i])
                # noinspection PyCallingNonCallable,PyTypeChecker
                raw_data = (pyglet.gl.GLubyte * len(rgb_tile))(*rgb_tile)
                image_data = pyglet.image.ImageData(8,8,'RGB',raw_data)
                self.tile_image_set[set_index][tile_index] = image_data

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

    def _apply_palette_transformation(self, base_color):
        """
        Converts the default color value from a pixel into the correct one based on the palette being applied.
        Bit 7-6 - Shade for Color Number 3
        Bit 5-4 - Shade for Color Number 2
        Bit 3-2 - Shade for Color Number 1
        Bit 1-0 - Shade for Color Number 0
        The four possible gray shades are: 0=White, 1=Light gray, 2=Dark gray, 3=Black
        :return:  Tuple with correct color based on palette
        """
        palette = self.cpu.memory.read_8bit(self.BACKGROUND_PALETTE_DATA_ADDRESS)
        correct_color = (palette >> (base_color*2)) & 0b00000011
        return self.DISPLAY_COLORS[correct_color]

    def debug(self):
        """
        Prints debug info to console.
        """
        current_lcd_line = self.cpu.memory.read_8bit(self.LCD_Y_COORDINATE_ADDRESS)
        mode = self.lcd_controller_mode()
        self.cpu.logger.debug("Mode: %i\tLY(FF44): %i\tCycles: %i",mode,current_lcd_line,self.cpu_cycles)
