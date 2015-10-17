import numpy as np
import operator

class Tile(object):

  def __init__(self, shape, array = None):
    if not array is None:
      if not isinstance(array, np.ndarray):
        raise TypeError ("Cannot initialize Tile with object of type '{:s}'".format(type(array).__name__))
      elif not array.shape == shape:
        raise ValueError("Cannot initialize {:s}-shaped Tile with an array of shape {:s}".format(str(shape), str(array.shape)))
    self._shape   = shape
    self._array   = array

  def get_shape  (self       ): return self._shape
  def is_empty   (self       ): return self._array is None
  def __repr__   (self       ): return self._array.__str__()          if not self.is_empty() else "Empty Tile"
  def __getitem__(self, *args): return self._array.__getitem__(*args) if not self.is_empty() else 0.0
  def __setitem__(self, *args):
    if self.is_empty(): self._array = np.zeros(self._shape)
    self._array.__setitem__(*args)

  def __add__ (self, other): print('__add__ '); return self.binary_operation(other, operator.__add__)
  def __sub__ (self, other): print('__sub__ '); return self.binary_operation(other, operator.__sub__)
  def __mul__ (self, other): print('__mul__ '); return self.binary_operation(other, operator.__mul__)
  def __div__ (self, other): print('__div__ '); return self.binary_operation(other, operator.__div__)
  def __radd__(self, other): print('__radd__'); return self.binary_operation(other, operator.__add__, swap=True)
  def __rsub__(self, other): print('__rsub__'); return self.binary_operation(other, operator.__sub__, swap=True)
  def __rmul__(self, other): print('__rmul__'); return self.binary_operation(other, operator.__mul__, swap=True)
  def __rdiv__(self, other): print('__rdiv__'); return self.binary_operation(other, operator.__div__, swap=True)

  def binary_operation(self, other, operation, swap=False):
    if isinstance(other, Tile) and not self._shape == other._shape:
      raise ValueError("Cannot {:s} Tiles with mismatched shapes {:s} and {:s}".format(operation.__name__, self._shape, other._shape))
    if self.is_empty() and (not isinstance(other, Tile) or other.is_empty()):
      return Tile(self._shape, None)
    larray = self._array if not self.is_empty() else 0.0
    rarray = other if not isinstance(other, Tile) else (other._array if not other.is_empty() else 0.0)
    oarray = operation(larray, rarray) if not swap else operation(rarray, larray)
    return Tile(self._shape, oarray)

