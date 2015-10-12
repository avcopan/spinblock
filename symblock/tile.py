class Tile(object):
  def __init__(self, shape, offsets):
    self._shape   = shape
    self._offsets = offsets

  def get_shape  (self): return self._shape
  def get_offsets(self): return self._offsets
