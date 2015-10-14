import numpy     as np
import itertools as it
from axis import PartitionedAxis
from tile import Tile

def multi_axis_getattr(method, axes, args = None):
  if   args is None: return tuple(getattr(PartitionedAxis, method)(axis      ) for axis       in     axes       )
  else             : return tuple(getattr(PartitionedAxis, method)(axis, args) for axis, args in zip(axes, args))

class TiledTensor:

  def __init__(self, axes):
    self._ndim  = len(axes)
    self._axes  = axes
    self._tiles = np.empty(self.get_tile_container_shape(), dtype = np.dtype(Tile))
    for tile_key in self.iter_tile_keys():
      self._tiles[tile_key] = Tile(self.get_tile_shape(tile_key), self.get_tile_offset(tile_key))

  def get_tile_container_shape(self): return multi_axis_getattr("get_npartitions", self._axes)
  def iter_tile_keys          (self): return it.product(*multi_axis_getattr("get_partition_keys", self._axes))
  def get_tile_key   (self, index     ): return multi_axis_getattr("get_partition_key"  , self._axes, index   )
  def get_tile_shape (self, tile_key  ): return multi_axis_getattr("get_partition_size" , self._axes, tile_key)
  def get_tile_offset(self, tile_key  ): return multi_axis_getattr("get_partition_start", self._axes, tile_key)

  def __getitem__(self, *args):
    index,   = args
    tile_key = self.get_tile_key(index)
    return self._tiles[tile_key][index]

  def __setitem__(self, *args):
    index, value = args
    tile_key = self.get_tile_key(index)
    self._tiles[tile_key][index] = value

