"""
Emulator UI using Pyglet
"""
import pyglet


# noinspection PyAbstractClass
class Screen(pyglet.window.Window):
    """ Pyglet GUI """

    RGB = "RGB"

    # TODO: It is running in the main thread and locking the application
    def __init__(self, gb):
        """
        :type gb: gb.GB
        """
        super(Screen, self).__init__(gb.gpu.SCREEN_WIDTH, gb.gpu.SCREEN_HEIGHT)
        self.set_minimum_size(gb.gpu.SCREEN_WIDTH, gb.gpu.SCREEN_HEIGHT)

        self.gb = gb
        pyglet.clock.schedule_interval(self.gb.cpu.execute, 1/(self.gb.cpu.CLOCK_HZ/self.gb.gpu.UPDATE_HZ))
        pyglet.app.run()

    # noinspection PyMethodOverriding
    def on_draw(self):
        """
        Pyglet method to redraw the screen
        """
        self.clear()
        # TODO: This method of drawing is slow, max speed of 10fps
        pyglet.image.ImageData(width=self.gb.gpu.SCREEN_WIDTH,
                               height=self.gb.gpu.SCREEN_HEIGHT,
                               format=self.RGB,
                               data=self.convert_to_pyglet_format(self.gb.gpu.screen),
                               pitch=-self.gb.gpu.SCREEN_WIDTH * self.gb.gpu.RGB_SIZE).blit(0,0)

    @staticmethod
    def convert_to_pyglet_format(array: list):
        """
        See: https://gamedev.stackexchange.com/questions/55945/how-to-draw-image-in-memory-manually-in-pyglet
        :param array: List containing screen data (i.e. RGB values)
        :return: The list converted to 'c_ubyte' format, used by pyglet
        """
        # noinspection PyCallingNonCallable,PyTypeChecker
        return (pyglet.gl.GLubyte * len(array))(*array)
