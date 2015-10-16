import numpy as np
import operator

class Tile(object):

  def __init__(self, shape, array = None):
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

  def __add__ (self, other): return self.binary_operation(other, operator.__add__)
  def __sub__ (self, other): return self.binary_operation(other, operator.__sub__)
  def __mul__ (self, other): return self.binary_operation(other, operator.__mul__)
  def __div__ (self, other): return self.binary_operation(other, operator.__div__)
  def __radd__(self, other): return self.binary_operation(other, operator.__add__, swap=True)
  def __rsub__(self, other): return self.binary_operation(other, operator.__sub__, swap=True)
  def __rmul__(self, other): return self.binary_operation(other, operator.__mul__, swap=True)
  def __rdiv__(self, other): return self.binary_operation(other, operator.__div__, swap=True)

  def binary_operation(self, other, operation, swap=False):
    if not self and (not other or not isinstance(other, Tile)):
      return Tile(self._shape, None)
    if isinstance(other, Tile):
      if not self._shape == other._shape:
        raise Exception("Cannot {:s} Tiles with mismatched shapes {:s} and {:s}".format(operation.__name__, self._shape, other._shape))
      other = other._array if not other else np.zeros(other._shape)

    if   not isinstance(other, Tile):
      if self:
        return Tile(self._shape, operation(self._array, other)) if not swap else \
               Tile(self._shape, operation(other, self._array))
      else:
        return Tile(self._shape, None)
    else:
      if not self and not other:
        return Tile(self._shape, None)
      else:
        self ._array = self ._array if not self  else np.zeros(self ._shape)
        other._array = other._array if not other else np.zeros(other._shape)
        return Tile(self._shape, operation(self ._array, other._array)) if not swap else \
               Tile(self._shape, operation(other._array, self ._array))
    

'''
  def binary_operation(self, other, operation):
    if bool(self) and bool(other):
       operation(self._array, other._array)
    else: return operation(self._array, 0.0) if bool(self) else 
'''
