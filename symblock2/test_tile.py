
if __name__ == "__main__":
  import tile as tl
  import numpy as np
  s1 = (5,7)
  s2 = (4,7)
  R = tl.Tile(s1, np.ones(s1))
  L = tl.Tile(s2, np.ones(s2))
  T = R % L.T
  print T
  print T.shape

  R = tl.Tile(s1, None)
  L = tl.Tile(s2, None)
  T = R % L.T
  print T.shape

  print np.dtype(tl.Tile)
  print np.dtype(tl.Tile) == np.object
