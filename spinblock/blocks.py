import numpy as np
import itertools as it
from blockprinter import prettyprint

'''
This needs a rewrite:
Data object of BlockedArray should be
  tiles = np.empty( (outer shape), dtype = np.dtype(Tile) )
where Tile is a sublcass of python object
  class Tile(object):
I think that should substantially simplify things

'''

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
  def get_block_dims  (self           ):  return self.block_dims
  def get_block_starts(self           ):  return self.block_starts
  def get_block_dim   (self, block_key):  return self.block_dims  [block_key]
  def get_block_start (self, block_key):  return self.block_starts[block_key]

  def get_block_key(self, key):
    block_key = next((i for i, r in enumerate(self.block_ranges) if fits_in(key, r)), None)
    if not isinstance(block_key, int): raise Exception("Invalid key {:s} used for {:s}-blocked axis.".format(str(key), str(self.block_dims)))
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
    self._blocks = {block_keys: 0. for block_keys in self.iter_block_keys()}

  def get_block       (self, block_keys): return self._blocks[block_keys]
  def get_axis        (self,  axis_key ): return self._axes  [ axis_key ]
  def get_block_keys  (self,       keys): return axes_getattr("get_block_key"  , self._axes,       keys)
  def get_array_keys  (self,       keys): return axes_getattr("get_array_key"  , self._axes,       keys)
  def get_block_shape (self, block_keys): return axes_getattr("get_block_dim"  , self._axes, block_keys)
  def get_block_offset(self, block_keys): return axes_getattr("get_block_start", self._axes, block_keys)
  def iter_axes       (self, slc=slice(None)): return (ax for ax in self._axes[slc])
  def iter_block_keys (self, slc=slice(None)): return it.product(*axes_getattr("get_block_keys", self._axes[slc]))

  def __getitem__(self, *args):
    keys, = args
    block_keys, array_keys = self.get_block_keys(keys), self.get_array_keys(keys)
    block = self._blocks[block_keys]
    return block if not hasattr(block,'__getitem__') else block[array_keys]

  def __setitem__(self, *args):
    keys, value = args
    block_keys = axes_getattr("get_block_key", self._axes, keys)
    array_keys = axes_getattr("get_array_key", self._axes, keys)
    if not hasattr(self._blocks[block_keys], '__setitem__'):
      self._blocks[block_keys] = np.zeros(axes_getattr("get_block_dim", self._axes, block_keys))
    self._blocks[block_keys][array_keys] = value

  def __repr__(self):
    return prettyprint(self)
