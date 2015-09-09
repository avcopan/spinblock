import itertools as it
import numpy as np

class SpinBlockedArray:

  def __init__(self, norb, ndim):
    self.dim = 2*norb
    self.ranges = [range(0, norb), range(norb, self.dim)]
    self.blocks = {blkindex: 0 for blkindex in it.product([0,1], repeat=ndim)}

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
    if   isinstance(key,   int) and 0 <= key < self.dim:
      return next(i for i, r in enumerate(self.ranges) if key in r)
    elif isinstance(key, slice) and 0 <= key.start <= key.stop <= self.dim:
      return next(i for i, r in enumerate(self.ranges) if (key.start in r and key.stop in r))
    else: raise Exception("Invalid key %s used with SpinBlockedArray object".format(str(key)))

  def get_array_key(self, key):
    if   isinstance(key,   int) and 0 <= key < self.dim:
      return next(key - r[0] for r in self.ranges if key in r)
    elif isinstance(key, slice) and 0 <= key.start <= key.stop <= self.dim:
      return next(slice(key.start-r[0], key.stop-r[0]) for r in self.ranges if (key.start in r and key.stop in r))
    else: raise Exception("Invalid key %s used with SpinBlockedArray object".format(str(key)))

