import itertools as it
import numpy as np
import operator

class SpinBlockedArray:

  def __init__(self, norb, ndim):
    self.norb, self.ndim = norb, ndim
    self.shape  = ((5,5),) * ndim
    self.ranges = [range(0, norb), range(norb, 2*norb)]
    self.blocks = {blkindex: 0. for blkindex in it.product([0,1], repeat=ndim)}

  # implement operator[] for accessing elements or slices and setting element values
  def __getitem__(self, *args):
    keys, = args
    block_keys = tuple(self.get_block_key(key) for key in keys)
    array_keys = tuple(self.get_array_key(key) for key in keys)
    block = self.blocks[block_keys]
    return block[array_keys] if hasattr(block,'__getitem__') else block

  def __setitem__(self, *args):
    keys, value = args
    block_keys = tuple(self.get_block_key(key) for key in keys)
    array_keys = tuple(self.get_array_key(key) for key in keys)
    if not hasattr(self.blocks[block_keys], '__setitem__'):
      self.blocks[block_keys] = np.zeros(tuple(len(self.ranges[key]) for key in block_keys))
    self.blocks[block_keys][array_keys] = value

  def get_block_key(self, key):
    try:    return next(i for i, r in enumerate(self.ranges) if fits_in(key, r))
    except: raise Exception("Invalid key {:s} used with SpinBlockedArray object".format(str(key)))

  def get_array_key(self, key):
    try:    return next(to_block_index(key, r) for r in self.ranges if fits_in(key, r))
    except: raise Exception("Invalid key {:s} used with SpinBlockedArray object".format(str(key)))

  # implement basic tensor algebra
  def __add__ (self, other): return self.binary_operation(other, operator.__add__)
  def __sub__ (self, other): return self.binary_operation(other, operator.__sub__)
  def __mul__ (self, other): return self.binary_operation(other, operator.__mul__)
  def __div__ (self, other): return self.binary_operation(other, operator.__div__)
  def __radd__(self, other): return self.binary_operation(other, operator.__add__, swap=True)
  def __rsub__(self, other): return self.binary_operation(other, operator.__sub__, swap=True)
  def __rmul__(self, other): return self.binary_operation(other, operator.__mul__, swap=True)
  def __rdiv__(self, other): return self.binary_operation(other, operator.__div__, swap=True)

  def binary_operation(self, other, operation, swap=False):
    result = SpinBlockedArray(self.norb, self.ndim)
    if swap: self, other = other, self
    try:
      for key in result.blocks:
        left  = self  if not isinstance(self , SpinBlockedArray) else  self.blocks[key]
        right = other if not isinstance(other, SpinBlockedArray) else other.blocks[key]
        if not (isinstance(left, float) and isinstance(right, float)):
          result.blocks[key] = operation(left, right)
    except:
      raise Exception("Cannot {:s} object of type {:s} with this SpinBlockedArray.".format(operation.__name__, other.__class__.__name__))
    return result

def fits_in(key, blockrange):
  if   isinstance(key,   int): return (key in blockrange)
  elif isinstance(key, slice): return (key.start in blockrange and key.stop - 1 in blockrange)

def to_block_index(key, blockrange):
  blockstart = blockrange[0]
  if   isinstance(key,   int): return key - blockstart
  elif isinstance(key, slice): return slice(key.start - blockstart, key.stop - blockstart)
