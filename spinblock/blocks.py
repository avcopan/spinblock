import numpy as np
import itertools as it

class BlockedAxis:

  def __init__(self, block_dims):
    if isinstance(block_dims, int): block_dims = (block_dims,)
    self.block_dims   = block_dims
    self.dim          = sum(block_dims)
    self.nblocks      = len(block_dims)
    self.block_keys   = range(self.nblocks)
    self.block_starts = [sum(block_dims[:i]) for i in range(len(block_dims))]
    block_stops       = self.block_starts[1:] + [self.dim]
    self.block_ranges = tuple(range(start, stop) for start, stop in zip(self.block_starts, block_stops))

  def get_dim         (self           ):  return self.dim
  def get_nblocks     (self           ):  return self.nblocks
  def get_block_keys  (self           ):  return self.block_keys
  def get_block_dim   (self, block_key):  return self.block_dims  [block_key]
  def get_block_start (self, block_key):  return self.block_starts[block_key]

  def get_block_key(self, key):
    block_key = next((i for i, r in enumerate(self.block_ranges) if fits_in(key, r)), None)
    if not isinstance(block_key, int): raise Exception("Invalid key {:s} used for {:s}-blocked axis.".format(str(key), str(self.blockdims)))
    else: return block_key

  def get_array_key(self, key):
    block_start = self.block_starts[self.get_block_key(key)]
    if   isinstance(key,   int): return key - block_start
    elif isinstance(key, slice): return slice(key.start - block_start, key.stop - block_start)

def fits_in(key, arange):
  if   isinstance(key,   int): return (key in arange)
  elif isinstance(key, slice): return (key.start in arange and key.stop - 1 in arange)

def axes_getattr(method, axes, args = None):
  if args == None: return tuple(getattr(BlockedAxis, method)(axis)      for axis      in     axes       )
  else:            return tuple(getattr(BlockedAxis, method)(axis, arg) for axis, arg in zip(axes, args))

class BlockedArray:

  def __init__(self, shape):
    self._ndim   = len(shape)
    self._axes   = tuple(BlockedAxis(blockdims) for blockdims in shape)
    self._blocks = {block_keys: 0. for block_keys in it.product(*axes_getattr("get_block_keys",self._axes))}

  def __getitem__(self, *args):
    keys, = args
    block_keys = axes_getattr("get_block_key", self._axes, keys)
    array_keys = axes_getattr("get_array_key", self._axes, keys)
    block = self._blocks[block_keys]
    return block if not hasattr(block,'__getitem__') else block[array_keys]

  def __setitem__(self, *args):
    keys, value = args
    block_keys = axes_getattr("get_block_key", self._axes, keys)
    array_keys = axes_getattr("get_array_key", self._axes, keys)
    if not hasattr(self._blocks[block_keys], '__setitem__'):
      self._blocks[block_keys] = np.zeros(axes_getattr("get_block_dim", self._axes, block_keys))
    self._blocks[block_keys][array_keys] = value

  def get_block_string(self, block_keys):
    key    = str(block_keys)
    offset = str(axes_getattr("get_block_start", self._axes, block_keys))
    shape  = str(axes_getattr("get_block_dim"  , self._axes, block_keys))
    block  = str(self._blocks[block_keys])
    fillstr = "Block # {:s}:\n  {:15s} = {:s}\n  {:15s} = {:s}\n{:s}\n"
    return fillstr.format(key, "offset", offset, "shape", shape, block)

  def __repr__(self):
    dtype         = np.dtype([('active',np.bool_), ('shape',np.uint64,(self.ndim,))])
    structure     = np.zeros(axes_getattr("get_nblocks", self._axes), dtype)
    active_blocks = []
    for block_keys in it.product(*axes_getattr("get_block_keys", self._axes))
      
    return ''.join(self.get_block_string(block_keys) for block_keys in it.product(*axes_getattr("get_block_keys",self._axes)))


'''
  def __repr__(self):
    return ''.join("Block {:s}:\n{:s}\n".format(str(block_keys), str(self._blocks[block_keys]))
                   for block_keys in it.product(*(axis.keys for axis in self._axes)))

class BlockedArray:

  def __init__(self, blocks_by_axis):
    ndim = len(blocks_by_axis)
    block_shape  = tuple(len(axis_blocks) for axis_blocks in blocks_by_axis)
    dtype = np.dtype([('active',np.bool_), ('shape',np.uint64,(ndim,))])
    block_struct = np.zeros(block_shape, dtype=dtype)
    for x in it.product(*tuple(enumerate(axis_blocks) for axis_blocks in blocks_by_axis)):
      index, shape = zip(*x)
      for i, dim in enumerate(shape):
        block_struct[index]['shape'][i] = dim

      print np.zeros(block_struct[index]['shape'])

    print block_struct

'''
