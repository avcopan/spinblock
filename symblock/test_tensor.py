from tensor import TiledTensor

from axis import PartitionedAxis
ax1 = PartitionedAxis((4,0,1,2))
ax2 = PartitionedAxis(7)

def test___init__():
  T = TiledTensor((ax1, ax2))
