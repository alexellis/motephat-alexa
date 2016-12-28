import motephat

class MoteInterface:
  def __init__(self):
    pass
  def setup(self):
    pass
  def set_colour(self, r, g, b):
    pass

class LiveMote(MoteInterface):
  def __init__(self):
    pass
  def setup(self):
    motephat.set_brightness(1)
    motephat.set_clear_on_exit(True)
  def set_colour(self, r, g, b):
    MAX_CHANNELS = 4
    MAX_PIXELS = 16
    for channel in range(MAX_CHANNELS):
      for pixel in range(MAX_PIXELS):
        motephat.set_pixel(channel + 1, pixel, r, g, b)
    motephat.show()

class StubMote(MoteInterface):
  def __init__(self):
    pass
  def setup(self):
    pass
  def set_colour(self,r,g,b):
    pass
