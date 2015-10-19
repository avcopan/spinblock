from tensor import TiledTensor

import numpy  as np
import pytest as pt
from tile import Tile
from axis import PartitionedAxis
ax1 = PartitionedAxis(7)
ax2 = PartitionedAxis((4,0,1,2))
ax3 = PartitionedAxis((4,1,0,2))

def test___init___________________01():
  T = TiledTensor((ax1,))
  assert T._ndim  == 1
  assert T._axes  == (ax1,)
  assert T._shape == (1,)
  assert T._tiles.shape == T._shape
  for tile in np.nditer(T._tiles, flags=['refs_ok']):
    assert isinstance(tile[()], Tile)

def test___init___________________02():
  T = TiledTensor((ax2,))
  assert T._ndim  == 1
  assert T._axes  == (ax2,)
  assert T._shape == (4,)
  assert T._tiles.shape == T._shape
  for tile in np.nditer(T._tiles, flags=['refs_ok']):
    assert isinstance(tile[()], Tile)

def test___init___________________03():
  T = TiledTensor((ax1, ax2, ax2, ax3,))
  assert T._ndim  == 4
  assert T._axes  == (ax1, ax2, ax2, ax3)
  assert T._shape == (  1,   4,   4,   4)
  assert T._tiles.shape == T._shape
  for tile in np.nditer(T._tiles, flags=['refs_ok']):
    assert isinstance(tile[()], Tile)

def test___init___________________04():
  T = TiledTensor((ax2, ax2), np.empty((4, 4), dtype=np.dtype(Tile)))
  assert T._ndim  == 2
  assert T._axes  == (ax2, ax2)
  assert T._shape == (  4,   4)

def test___init___________________05():
  with pt.raises(ValueError) as message:
    T = TiledTensor((ax2, ax2), np.empty((4, 5), dtype=np.dtype(Tile)))
  assert str(message).endswith("Cannot initialize (4, 4)-blocked TiledTensor with Tile array of shape (4, 5)")

def test___init___________________06():
  with pt.raises(TypeError ) as message:
    T = TiledTensor((ax2, ax2), np.empty((4, 4), dtype=np.float))
  assert str(message).endswith("Cannot initialize TiledTensor with this object of type 'ndarray'")

def test___init___________________07():
  with pt.raises(TypeError ) as message:
    T = TiledTensor((ax2, ax2), "this is a string, not a numpy array")
  assert str(message).endswith("Cannot initialize TiledTensor with this object of type 'str'")

def test___getitem________________01():
  T = TiledTensor((ax2, ax2))
  assert T[0,0] == 0.0


if __name__ == "__main__":
  L = TiledTensor((ax2, ax2))
  for i in range(7):
    L[i,i] = i
  R = TiledTensor((ax2, ax2))
  print L + R
  print R + L

  a1 = PartitionedAxis(2)
  a2 = PartitionedAxis((1,2))
  a3 = PartitionedAxis((2,1,1))
  T = TiledTensor((a1, a2, a3))
  for i in range(2):
    for j in range(3):
      for k in range(4):
        T[i,j,k] = i*3*4 + j*4 + k
  G = T.transpose()
  for i in range(2):
    for j in range(3):
      for k in range(4):
        print G[k,j,i] == i*3*4 + j*4 + k
  print G
  print G.transpose()

  from tensordot import tensordot
  tensordot(T, T, axis_keys=([0,1],[0,1]))
