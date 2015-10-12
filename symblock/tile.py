import numpy as np

class Tile(object):
  def __init__(self, shape, offsets):
    self._shape   = shape
    self._offsets = offsets
    self._array   = None

  def get_shape  (self              ): return self._shape
  def get_offsets(self              ): return self._offsets
  def get_index  (self, offset_index): return tuple(offset_key - offset for offset_key, offset in zip(offset_index, self._offsets))
  def __bool__(self):    return self._array is None

  def __getitem__(self, *args):
    if self._array is None: return 0.0
    return self._array[self.get_index(args[0])]

  def __setitem__(self, *args):
    if self._array is None: self._array = np.zeros(self._shape)
    self._array[self.get_index(args[0])] = args[1]
