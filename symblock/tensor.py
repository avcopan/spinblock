import numpy     as np
import itertools as it
import axis      as ax
import tile      as tl

def tensordot(L, R, axis_keys=([0],[0])):
  sum_axis_keys_L, sum_axis_keys_R = axis_keys
  ncontracted = len(sum_axis_keys_L)
  L = L.transpose(sum_axis_keys_L + [axis_key for axis_key in L.iter_axis_keys() if not axis_key in sum_axis_keys_L])
  R = R.transpose(sum_axis_keys_R + [axis_key for axis_key in R.iter_axis_keys() if not axis_key in sum_axis_keys_R])
  sum_axes = L.get_axis(slice(None,ncontracted))
  row_axes = L.get_axis(slice(ncontracted,None))
  col_axes = R.get_axis(slice(ncontracted,None))

  contract_tiles = lambda tile1, tile2: tl.tensordot(tile1, tile2, axis_keys=(range(ncontracted), range(ncontracted)))
  T = TiledTensor(row_axes + col_axes)
  o = (0,) * ncontracted
  for r in multi_axis_iter(row_axes):
    for c in multi_axis_iter(col_axes):
      for s in multi_axis_iter(sum_axes):
        T._tiles[r+c] += contract_tiles(L.get_tile(s+r), R.get_tile(s+c))
  return T


def multi_axis_getattr(method, axes, args = None):
  if   args is None: return tuple(getattr(ax.PartitionedAxis, method)(axis      ) for axis       in     axes       )
  else             : return tuple(getattr(ax.PartitionedAxis, method)(axis, args) for axis, args in zip(axes, args))

def multi_axis_iter(axes): return it.product(*multi_axis_getattr("get_partition_keys", axes))

class TiledTensor(object):

  def __init__(self, axes, tiles = None):
    self._ndim  = len(axes)
    self._axes  = axes
    self._shape = self.get_tile_container_shape()
    if not tiles is None:
      if   not (isinstance(tiles, np.ndarray) and tiles.dtype == np.dtype(tl.Tile)):
        raise TypeError ("Cannot initialize TiledTensor with this object of type '{:s}'".format(type(tiles).__name__))
      elif not tiles.shape == self._shape:
        raise ValueError("Cannot initialize {:s}-blocked TiledTensor with Tile array of shape {:s}".format(str(self._shape), str(tiles.shape)))
      self._tiles = tiles
    else:
      self._tiles = np.empty(self._shape, dtype = np.dtype(tl.Tile))
      for tile_key in self.iter_tile_keys():
        self._tiles[tile_key] = tl.Tile(self.get_tile_shape(tile_key))

  def get_tile       (self, tile_key  ): return self._tiles[tile_key]
  def get_tile_container_shape(self   ): return multi_axis_getattr("get_npartitions"    , self._axes          )
  def get_subkey     (self, index     ): return multi_axis_getattr("get_subkey"         , self._axes, index   )
  def get_tile_key   (self, index     ): return multi_axis_getattr("get_partition_key"  , self._axes, index   )
  def get_tile_shape (self, tile_key  ): return multi_axis_getattr("get_partition_size" , self._axes, tile_key)
  def get_tile_offset(self, tile_key  ): return multi_axis_getattr("get_partition_start", self._axes, tile_key)
  def iter_tile_keys (self, slc=slice(None)):  return multi_axis_iter(self._axes[slc])
  def iter_axes      (self            ): return (axis     for axis     in self._axes       )
  def iter_axis_keys (self            ): return (axis_key for axis_key in range(self._ndim))
  def get_axis       (self, axis_key  ): return self._axes[axis_key]

  def __repr__(self): from prettyprint import TiledTensor_to_str; return TiledTensor_to_str(self)

  def __getitem__(self, *args): return self._tiles[self.get_tile_key(args[0])][self.get_subkey(args[0])]
  def __setitem__(self, *args):        self._tiles[self.get_tile_key(args[0])][self.get_subkey(args[0])] = args[1]

  def transpose(self, axis_keys = None):
    if axis_keys is None: axis_keys = tuple(reversed(range(self._ndim)))
    tiles = self._tiles.transpose(axis_keys)
    axes  = tuple(self._axes[axis_key] for axis_key in axis_keys)
    for tile_key in multi_axis_iter(axes):
      tiles[tile_key] = tiles[tile_key].transpose(axis_keys)
    return TiledTensor(axes, tiles)

  def __pos__ (self       ): return TiledTensor(self._axes, +self._tiles)
  def __neg__ (self       ): return TiledTensor(self._axes, -self._tiles)
  def __add__ (self, other): return self.binary_operation(other, np.ndarray.__add__ )
  def __sub__ (self, other): return self.binary_operation(other, np.ndarray.__sub__ )
  def __mul__ (self, other): return self.binary_operation(other, np.ndarray.__mul__ )
  def __div__ (self, other): return self.binary_operation(other, np.ndarray.__div__ )
  def __radd__(self, other): return self.binary_operation(other, np.ndarray.__radd__)
  def __rsub__(self, other): return self.binary_operation(other, np.ndarray.__rsub__)
  def __rmul__(self, other): return self.binary_operation(other, np.ndarray.__rmul__)
  def __rdiv__(self, other): return self.binary_operation(other, np.ndarray.__rdiv__)

  def binary_operation(self, other, operation):
    return TiledTensor(self._axes, operation(self._tiles, other)) if not isinstance(other, TiledTensor) else\
           TiledTensor(self._axes, operation(self._tiles, other._tiles))


