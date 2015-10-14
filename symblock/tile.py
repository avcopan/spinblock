import numpy as np

class Tile(object):
  def __init__(self, shape, offsets):
    self._shape   = shape
    self._offsets = offsets
    self._array   = None

  def get_shape  (self): return self._shape
  def get_offsets(self): return self._offsets
  def __bool__   (self): return self._array is None
  def get_subkey (self, index): return tuple(remove_offset(axindex, axoffset) for axindex, axoffset in zip(index, self._offsets))

  def __getitem__(self, *args):
    if self._array is None: return 0.0
    return self._array[self.get_subkey(args[0])]

  def __setitem__(self, *args):
    if self._array is None: self._array = np.zeros(self._shape)
    self._array[self.get_subkey(args[0])] = args[1]

def remove_offset(axindex, axoffset):
  if   isinstance(axindex,   int): return int  (axindex - axoffset)
  elif isinstance(axindex, slice): return slice(axindex.start - axoffset, axindex.stop - axoffset)
