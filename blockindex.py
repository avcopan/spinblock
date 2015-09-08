import itertools as it

class ArrayBlock:

  def __init__(self, array, ranges):
    self.array  = array
    self.ndim   = array.ndim
    self.ranges = ranges

class SpinBlockedArray:

  def __init__(self, norb, ndim):
    self.norb = norb
    self.ndim = ndim
    self.sliceA = slice(0, norb)
    self.sliceB = slice(norb, 2*norb)
    self.blocks = {x:0 for x in it.product([sliceA, sliceB], repeat=ndim)}


  def get_block_key(self, key):
    if   fits_in_range(key, self.sliceA): return self.sliceA
    elif fits_in_range(key, self.sliceB): return self.sliceB
    else: raise Exception("Invalid key %s passed to SpinBlockedArray".format(str(key)))

  def get_array_key(self, key):
    sliceA, sliceB = self.sliceA, self.sliceB
    if   fits_in_range(key, self.sliceA)
      if   isinstance(key, slice): return slice(key.start - sliceA.start, key.stop - sliceA.start)
      elif isinstance(key, int  ): return key - sliceA.start
    elif fits_in_range(key, self.sliceB):
      if   isinstance(key, slice): return slice(key.start - sliceB.start, key.stop - sliceB.start)
      elif isinstance(key, int  ): return key - sliceB.start

  def __getitem__(self, keys):
    block_keys = tuple(self.get_block_key(key) for key in keys)
    array_keys = tuple(self.get_array_key(key) for key in keys)
    return self.blocks[block_keys][array_keys]

  

  def __add__ (self, other): return self.binary_operation(other, np.ndarray.__add__ )
  def __sub__ (self, other): return self.binary_operation(other, np.ndarray.__sub__ )
  def __mul__ (self, other): return self.binary_operation(other, np.ndarray.__mul__ )
  def __div__ (self, other): return self.binary_operation(other, np.ndarray.__div__ )
  def __radd__(self, other): return self.binary_operation(other, np.ndarray.__radd__)
  def __rsub__(self, other): return self.binary_operation(other, np.ndarray.__rsub__)
  def __rmul__(self, other): return self.binary_operation(other, np.ndarray.__rmul__)
  def __rdiv__(self, other): return self.binary_operation(other, np.ndarray.__rdiv__)

  def binary_operation(self, other, operation):
    out = SpinBlockedArray(self.norb, self.ndim)
    if   isinstance(other, ArrayBlock):
    elif isinstance(
      

  def __add__ (self, other):
    if isinstance(other, ArrayBlock):
      added = SpinBlockedArray(self.norb, self.ndim)
      added.blocks[other.ranges] = self.blocks[other.ranges] + other.array
      return added



def fits_in_range(key, sliceobj):
  if   isinstance(key, slice): return sliceobj.start <= key.start <= key.stop <= sliceobj.stop
  elif isinstance(key, int  ): return sliceobj.start <= key < sliceobj.stop

