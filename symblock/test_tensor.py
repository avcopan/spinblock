import tensor as tn

import numpy     as np
import pytest    as pt
import itertools as it
import tile      as tl
import axis      as ax
ax1 = ax.PartitionedAxis(7)
ax2 = ax.PartitionedAxis((4,0,1,2))
ax3 = ax.PartitionedAxis((4,1,0,2))

def test___init___________________01():
  T = tn.TiledTensor((ax1,))
  assert T._ndim  == 1
  assert T._axes  == (ax1,)
  assert T._shape == (1,)
  assert T._tiles.shape == T._shape
  for tile in np.nditer(T._tiles, flags=['refs_ok']):
    assert isinstance(tile[()], tl.Tile)

def test___init___________________02():
  T = tn.TiledTensor((ax2,))
  assert T._ndim  == 1
  assert T._axes  == (ax2,)
  assert T._shape == (4,)
  assert T._tiles.shape == T._shape
  for tile in np.nditer(T._tiles, flags=['refs_ok']):
    assert isinstance(tile[()], tl.Tile)

def test___init___________________03():
  T = tn.TiledTensor((ax1, ax2, ax2, ax3,))
  assert T._ndim  == 4
  assert T._axes  == (ax1, ax2, ax2, ax3)
  assert T._shape == (  1,   4,   4,   4)
  assert T._tiles.shape == T._shape
  for tile in np.nditer(T._tiles, flags=['refs_ok']):
    assert isinstance(tile[()], tl.Tile)

def test___init___________________04():
  T = tn.TiledTensor((ax2, ax2), np.empty((4, 4), dtype=np.dtype(tl.Tile)))
  assert T._ndim  == 2
  assert T._axes  == (ax2, ax2)
  assert T._shape == (  4,   4)

def test___init___________________05():
  with pt.raises(ValueError) as message:
    T = tn.TiledTensor((ax2, ax2), np.empty((4, 5), dtype=np.dtype(tl.Tile)))
  assert str(message).endswith("Cannot initialize (4, 4)-blocked TiledTensor with Tile array of shape (4, 5)")

def test___init___________________06():
  with pt.raises(TypeError ) as message:
    T = tn.TiledTensor((ax2, ax2), np.empty((4, 4), dtype=np.float))
  assert str(message).endswith("Cannot initialize TiledTensor with this object of type 'ndarray'")

def test___init___________________07():
  with pt.raises(TypeError ) as message:
    T = tn.TiledTensor((ax2, ax2), "this is a string, not a numpy array")
  assert str(message).endswith("Cannot initialize TiledTensor with this object of type 'str'")

def test___getitem________________01():
  T = tn.TiledTensor((ax2, ax2))
  assert T[0,0] == 0.0

def test_tensordot________________01():
  larray = np.random.rand(5,5)
  rarray = np.random.rand(5,5)
  tarray = np.tensordot(larray, rarray, axes=([1],[0]))

  a1 = ax.PartitionedAxis((5,5))
  L = tn.TiledTensor((a1,a1))
  R = tn.TiledTensor((a1,a1))
  L[0:5,0:5] = L[5:10,5:10] = larray
  R[0:5,0:5] = R[5:10,5:10] = rarray
  T = tn.tensordot(L, R, axis_keys=([1],[0]))

  assert (T[0: 5,0: 5] == tarray).all()
  assert (T[5:10,5:10] == tarray).all()

def test_tensordot________________02():
  a2 = ax.PartitionedAxis(2)
  a3 = ax.PartitionedAxis((1,2))
  a4 = ax.PartitionedAxis((2,1,1))
  a5 = ax.PartitionedAxis((3,2))
  a6 = ax.PartitionedAxis((3,0,1,2))

  larray = np.random.rand(2,3,4,5,6)
  rarray = np.random.rand(6,4,5,3,3)
  tarray = np.tensordot(larray, rarray, axes=([1,2,3,4],[3,1,2,0]))

  L = tn.TiledTensor((a2,a3,a4,a5,a6))
  R = tn.TiledTensor((a6,a4,a5,a3,a3))
  for coord in it.product(*(range(dim) for dim in larray.shape)):
    L[coord] = larray[coord]
  for coord in it.product(*(range(dim) for dim in rarray.shape)):
    R[coord] = rarray[coord]
  T = tn.tensordot(L, R, axis_keys=([1,2,3,4],[3,1,2,0]))
  for coord in it.product(*(range(dim) for dim in tarray.shape)):
    assert abs(T[coord] - tarray[coord]) < 1e-13


if __name__ == "__main__":
  larray = np.random.rand(5,5)
  rarray = np.random.rand(5,5)
  tarray = np.tensordot(larray, rarray, axes=([1],[0]))
  print tarray
  a1 = ax.PartitionedAxis((5,5))
  L = tn.TiledTensor((a1,a1))
  R = tn.TiledTensor((a1,a1))
  L[0:5,0:5] = L[5:10,5:10] = larray
  R[0:5,0:5] = R[5:10,5:10] = rarray
  T = tn.tensordot(L, R, axis_keys=([1],[0]))
  print T
