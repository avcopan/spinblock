import numpy     as np
import itertools as it
from axis import PartitionedAxis
from tile import Tile

def multi_axis_getattr(method, axes, args = None):
  if   args is None: return tuple(getattr(PartitionedAxis, method)(axis      ) for axis       in     axes       )
  else             : return tuple(getattr(PartitionedAxis, method)(axis, args) for axis, args in zip(axes, args))

class TiledTensor(object):

  def __init__(self, axes, tiles = None):
    self._ndim  = len(axes)
    self._axes  = axes
    self._shape = self.get_tile_container_shape()
    if not tiles is None:
      if   not (isinstance(tiles, np.ndarray) and tiles.dtype == np.dtype(Tile)):
        raise TypeError ("Cannot initialize TiledTensor with this object of type '{:s}'".format(type(tiles).__name__))
      elif not tiles.shape == self._shape:
        raise ValueError("Cannot initialize {:s}-blocked TiledTensor with Tile array of shape {:s}".format(str(self._shape), str(tiles.shape)))
      self._tiles = tiles
    else:
      self._tiles = np.empty(self._shape, dtype = np.dtype(Tile))
      for tile_key in self.iter_tile_keys():
        self._tiles[tile_key] = Tile(self.get_tile_shape(tile_key))

  def get_tile       (self, tile_key  ): return self._tiles[tile_key]
  def get_tile_container_shape(self   ): return multi_axis_getattr("get_npartitions"    , self._axes          )
  def get_subkey     (self, index     ): return multi_axis_getattr("get_subkey"         , self._axes, index   )
  def get_tile_key   (self, index     ): return multi_axis_getattr("get_partition_key"  , self._axes, index   )
  def get_tile_shape (self, tile_key  ): return multi_axis_getattr("get_partition_size" , self._axes, tile_key)
  def get_tile_offset(self, tile_key  ): return multi_axis_getattr("get_partition_start", self._axes, tile_key)
  def iter_tile_keys (self, slc=slice(None)): return it.product(*multi_axis_getattr("get_partition_keys", self._axes[slc]))

  def __repr__(self): from prettyprint import TiledTensor_to_str; return TiledTensor_to_str(self)

  def __getitem__(self, *args): return self._tiles[self.get_tile_key(args[0])][self.get_subkey(args[0])]
  def __setitem__(self, *args):        self._tiles[self.get_tile_key(args[0])][self.get_subkey(args[0])] = args[1]

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
