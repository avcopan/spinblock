from tensor import TiledTensor

from axis import PartitionedAxis
ax1 = PartitionedAxis((4,0,1,2))
ax2 = PartitionedAxis((4,1,0,2))
ax3 = PartitionedAxis(7)

def test___init_____01():
  T = TiledTensor((ax1, ax1))
  print T._tiles
  T[0,0] = 5
  print T._tiles
  T += 1
  print T._tiles
  G = T + T
  print G._tiles
