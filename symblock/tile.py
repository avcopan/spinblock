import numpy as np

class Tile(object):

  def __init__(self, shape, array = None):
    if not array is None:
      if not isinstance(array, np.ndarray):
        raise Exception("Cannot initialize Tile with object of type '{:s}'".format(type(array).__name__))
      elif not array.shape == shape:
        raise Exception("Cannot initialize {:s}-shaped Tile with an array of shape {:s}".format(str(shape), str(array.shape)))
    self._shape   = shape
    self._array   = array

  def get_shape  (self): return self._shape
  def __nonzero__(self): return not self._array is None

  def __repr__(self):
    if self._array is None: return "Empty Tile"
    return self._array.__repr__()

  def __getitem__(self, *args):
    if self._array is None: return 0.0
    return self._array.__getitem__(*args)

  def __setitem__(self, *args):
    if self._array is None: self._array = np.zeros(self._shape)
    self._array.__setitem__(*args)

  def __add__ (self, other): return self.binary_operation(other, np.ndarray.__add__ )
  def __sub__ (self, other): return self.binary_operation(other, np.ndarray.__sub__ )
  def __mul__ (self, other): return self.binary_operation(other, np.ndarray.__mul__ )
  def __div__ (self, other): return self.binary_operation(other, np.ndarray.__div__ )
  def __radd__(self, other): return self.binary_operation(other, np.ndarray.__radd__)
  def __rsub__(self, other): return self.binary_operation(other, np.ndarray.__rsub__)
  def __rmul__(self, other): return self.binary_operation(other, np.ndarray.__rmul__)
  def __rdiv__(self, other): return self.binary_operation(other, np.ndarray.__rdiv__)

  def binary_operation(self, other, operation):
    if not self and (not other or not isinstance(other, Tile)):
      return Tile(self._shape, None)
    larray = self._array if self else np.zeros(self._shape)
    rarray = other
    if isinstance(other, Tile):
      if not self._shape == other._shape:
        raise Exception("Cannot {:s} Tiles with mismatched shapes {:s} and {:s}".format(operation.__name__, self._shape, other._shape))
      rarray = other._array if other else 0.0
    return Tile(self._shape, operation(larray, rarray))

'''
  def binary_operation(self, other, operation):
    if bool(self) and bool(other):
       operation(self._array, other._array)
    else: return operation(self._array, 0.0) if bool(self) else 
'''
