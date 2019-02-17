"""
Emulator UI using Pyglet
"""
import pyglet
from datetime import datetime


# noinspection PyAbstractClass
class Screen(pyglet.window.Window):
    """ Pyglet GUI """

    RGB = "RGB"

    def __init__(self, gb):
        """
        :type gb: gb.GB
        """
        super(Screen, self).__init__(1, 1)
        self.set_visible(False)

        self.gb = gb
        self.vertex_list = None

    def run(self):
        self.set_size(self.gb.gpu.SCREEN_WIDTH-1, self.gb.gpu.SCREEN_HEIGHT-1)
        self.set_visible(True)

        self.vertex_list = pyglet.graphics.vertex_list(self.gb.gpu.SCREEN_WIDTH * self.gb.gpu.SCREEN_HEIGHT,
                                                       'v2i/stream',  # each vertice is 2D int
                                                       'c3B/stream')  # each color is RGB byte
        pos = 0
        for y in range(143,-1,-1):  # By default (0,0) is bottom left; by inverting the range() we make (0,0) top left
            for x in range(self.gb.gpu.SCREEN_WIDTH):
                self.vertex_list.vertices[pos:pos + 2] = [x, y]
                pos += 2

        pyglet.clock.schedule_interval(self.execute_cycle, 1 / (self.gb.cpu.CLOCK_HZ / self.gb.gpu.UPDATE_HZ))
        pyglet.app.run()

    def execute_cycle(self, _):
        start = datetime.now()
        self.gb.cpu.execute()
        end = datetime.now()
        delta = self.delta(start, end)
        self.set_caption(str(1000.0 / delta))

    def update(self, new_color_list):
        self.vertex_list.colors = new_color_list

    # noinspection PyMethodOverriding
    def on_draw(self):
        """
        Pyglet method to redraw the screen
        """
        self.clear()
        self.vertex_list.draw(pyglet.gl.GL_POINTS)

    def delta(self, a, b):
        diff = b-a
        return (diff.seconds * 1000.0) + (diff.microseconds / 1000.0)
