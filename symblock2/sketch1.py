import numpy as np
import tile  as tl

class TileCollection(object):

  def __init__(self, constructor_args, Constructor):
    self.dim = len(constructor_args)
    self.tiles = np.empty(self.dim, dtype=np.object)
    for i in range(self.dim):
      self.tiles[i] = Constructor( constructor_args[i] )

    if Constructor == tl.Tile:
      for i in range(self.dim):
        for j in range(constructor_args[i]):
          self.tiles[i][j] = j

  def __repr__(self):
    return self.tiles.__str__()


l1_dtype = tl.Tile
l1_constructor_args = (4,0,1,2)
l1 = TileCollection(l1_constructor_args, l1_dtype)

print l1.tiles

l2_Constructor = TileCollection
l2_constructor_args = (((4,0,1,2), tl.Tile), (4,0,1,2), tl.Tile))

l2_dim = len(l2_constructor_args)
l2_tiles = np.empty(l2_dim, dtype=l2_Constructor)
for i in range(l2_dim):
  l2_tiles[i] = l2_Constructor( *l2_constructor_args[i] )

print l2_tiles
