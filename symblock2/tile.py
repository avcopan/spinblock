import numpy as np

class Tile(object):

  def __init__(self, shape, array = None):
    if isinstance(shape, int): shape = (shape,)
    self.ndim  = len  (shape)
    self.shape = tuple(shape)
    if not array is None:
      if not isinstance(array, np.ndarray):
        raise TypeError ("Cannot initialize Tile with object of type '{:s}'".format(type(array).__name__))
      elif not array.shape == self.shape:
        raise ValueError("Cannot initialize {:s}-shaped Tile with an array of shape {:s}".format(str(shape), str(array.shape)))
    self._array = array

  def is_empty(self): return self._array is None

  def __repr__   (self       ): return self._array.__str__()          if not self.is_empty() else "Empty Tile"
  def __getitem__(self, *args): return self._array.__getitem__(*args) if not self.is_empty() else 0.0
  def __setitem__(self, *args):
    if self.is_empty(): self._array = np.zeros(self.shape)
    self._array.__setitem__(*args)

  def transpose(self, axis_keys = None):
    if axis_keys is None: axis_keys = tuple(reversed(range(self.ndim)))
    shape = [self.shape[axis_key] for axis_key in axis_keys]
    return Tile(shape, None) if self.is_empty() else Tile(shape, self._array.transpose(axis_keys))

  T = property(transpose, None)

  def __pos__(self): return self if self.is_empty() else Tile(self._shape, +self._array)
  def __neg__(self): return self if self.is_empty() else Tile(self._shape, -self._array)

  def __add__ (self, other): return self.additive_operation(other, np.ndarray.__add__ )
  def __sub__ (self, other): return self.additive_operation(other, np.ndarray.__sub__ )
  def __radd__(self, other): return self.additive_operation(other, np.ndarray.__radd__)
  def __rsub__(self, other): return self.additive_operation(other, np.ndarray.__rsub__)

  def __mul__ (self, other): return self.multiplicative_operation(other, np.ndarray.__mul__ )
  def __div__ (self, other): return self.multiplicative_operation(other, np.ndarray.__div__ )
  def __rmul__(self, other): return self.multiplicative_operation(other, np.ndarray.__rmul__)
  def __rdiv__(self, other): return self.multiplicative_operation(other, np.ndarray.__rdiv__)

  def __mod__ (self, other): return self.dot(other, swap=False)
  def __rmod__(self, other): return self.dot(other, swap=True )

  def additive_operation(self, other, operation):
    if isinstance(other, Tile) and not self.shape == other.shape:
      raise ValueError("Cannot {:s} Tiles with mismatched shapes {:s} and {:s}".format(operation.__name__, self.shape, other.shape))
    if   self.is_empty() and isinstance(other, Tile): return +other if not operation == np.ndarray.__sub__ else -other
    elif self.is_empty()                            : return Tile(self.shape, None)
    operand = other if not isinstance(other, Tile) else (other._array if not other.is_empty() else 0.0)
    return Tile(self.shape, operation(self._array, operand))

  def multiplicative_operation(self, other, operation):
    if isinstance(other, Tile) and not self.shape == other.shape:
      raise ValueError("Cannot {:s} Tiles with mismatched shapes {:s} and {:s}".format(operation.__name__, self.shape, other.shape))
    if self.is_empty() or (isinstance(other, Tile) and other.is_empty()):
      return Tile(self.shape, None)
    operand = other if not isinstance(other, Tile) else other._array
    return Tile(self.shape, operation(self._array, operand))

  def dot(self, other, swap=False):
    if not isinstance(other, Tile):
      raise TypeError ("Matrix multiplication of Tile with '{:s}' is undefined.".format(type(array).__name__))
    if swap: self, other = other, self
    if not self.shape[-1:None] == other.shape[-2:][0:1]:
      raise ValueError("Cannot matrix multiply Tiles with shapes {:s} and {:s}".format(self.shape, other.shape))
    if self.is_empty() or other.is_empty(): return Tile(self.shape[:-1] + other.shape[:-2] + other.shape[-2:][1:], None)
    ret = np.dot(self._array, other._array)
    return Tile(ret.shape, ret)
