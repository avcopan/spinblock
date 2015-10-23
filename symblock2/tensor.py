
class TiledTensor(object):

  def __init__(self, axes, tiles = None):
    self.ndim = len(axes)
    self.axes = axes
    """
    the axes should provide constructor arguments for each tile
    self.shape = ...
    self._tiles = np.empty(self.shape, dtype = np.object)

    for tile_key in iter_tile_keys():
      self._tiles[tile_key] = Constructor( args[tile_key] )
    """
