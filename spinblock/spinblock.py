import itertools as it
import numpy as np

class SpinBlockedArray:

  def __init__(self, norb, ndim):
    self.ranges = [range(0, norb), range(norb, 2*norb)]
    self.blocks = {blkindex: 0 for blkindex in it.product([0,1], repeat=ndim)}

  def get_block_keys(self, keys):
    return tuple(i for key in keys for i, r in enumerate(self.ranges) if key in r)

  def get_array_keys(self, keys):
    return tuple(i - r[0] for key in keys for i, r in enumerate(self.ranges) if key in r)

  def __getitem__(self, *args):
    keys, = args
    block_keys, array_keys = self.get_block_keys(keys), self.get_array_keys(keys)
    block = self.blocks[block_keys]
    return block[array_keys] if hasattr(block,'__getitem__') else block

  def __setitem__(self, *args):
    keys, value = args
    block_keys, array_keys = self.get_block_keys(keys), self.get_array_keys(keys)
    if not hasattr(self.blocks[block_keys], '__setitem__'):
      self.blocks[block_keys] = np.zeros(tuple(len(self.ranges[key]) for key in block_keys))
    self.blocks[block_keys][array_keys] = value

