import numpy as np
import operator

class Tile(object):

  def __init__(self, shape, array = None):
    if not array is None:
      if not isinstance(array, np.ndarray):
        raise TypeError ("Cannot initialize Tile with object of type '{:s}'".format(type(array).__name__))
      elif not array.shape == shape:
        raise ValueError("Cannot initialize {:s}-shaped Tile with an array of shape {:s}".format(str(shape), str(array.shape)))
    self._ndim    = len(shape)
    self._shape   = shape
    self._array   = array

  def get_shape  (self       ): return self._shape
  def is_empty   (self       ): return self._array is None
  def __repr__   (self       ): return self._array.__str__()          if not self.is_empty() else "Empty Tile"
  def __getitem__(self, *args): return self._array.__getitem__(*args) if not self.is_empty() else 0.0
  def __setitem__(self, *args):
    if self.is_empty(): self._array = np.zeros(self._shape)
    self._array.__setitem__(*args)

  def transpose(self, axis_keys = None):
    if axis_keys is None: axis_keys = tuple(reversed(range(self._ndim)))
    shape = tuple(self._shape[axis_key] for axis_key in axis_keys)
    return Tile(shape, None) if self.is_empty() else Tile(shape, self._array.transpose(axis_keys))

  def __pos__ (self       ): return self if self.is_empty() else Tile(self._shape, +self._array)
  def __neg__ (self       ): return self if self.is_empty() else Tile(self._shape, -self._array)
  def __add__ (self, other): return self.binary_operation(other, operator.__add__, multp=False, swap=False)
  def __sub__ (self, other): return self.binary_operation(other, operator.__sub__, multp=False, swap=False)
  def __mul__ (self, other): return self.binary_operation(other, operator.__mul__, multp=True , swap=False)
  def __div__ (self, other): return self.binary_operation(other, operator.__div__, multp=True , swap=False)
  def __radd__(self, other): return self.binary_operation(other, operator.__add__, multp=False, swap=True )
  def __rsub__(self, other): return self.binary_operation(other, operator.__sub__, multp=False, swap=True )
  def __rmul__(self, other): return self.binary_operation(other, operator.__mul__, multp=True , swap=True )
  def __rdiv__(self, other): return self.binary_operation(other, operator.__div__, multp=True , swap=True )

  def binary_operation(self, other, operation, multp=False, swap=False):
    if isinstance(other, Tile) and not self._shape == other._shape:
      raise ValueError("Cannot {:s} Tiles with mismatched shapes {:s} and {:s}".format(operation.__name__, self._shape, other._shape))
    if self.is_empty() and (not isinstance(other, Tile) or other.is_empty()):
      return Tile(self._shape, None)
    if multp and (self.is_empty() or (isinstance(other, Tile) and other.is_empty())):
      return Tile(self._shape, None)
    larray = self._array if not self.is_empty() else 0.0
    rarray = other if not isinstance(other, Tile) else (other._array if not other.is_empty() else 0.0)
    oarray = operation(larray, rarray) if not swap else operation(rarray, larray)
    return Tile(self._shape, oarray)
