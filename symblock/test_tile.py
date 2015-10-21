import tile   as tl
import numpy     as np
import pytest    as pt
import itertools as it

def test___init_____01():
  T = tl.Tile((5, 7))
  assert T._shape == (5, 7)

def test___init_____02():
  T = tl.Tile((5, 7), np.zeros((5, 7)))
  assert T._shape == T._array.shape

def test___init_____03():
  with pt.raises(TypeError ) as message:
    tl.Tile((5, 7), "this is a string, not a numpy array")
  assert str(message).endswith("Cannot initialize Tile with object of type 'str'")

def test___init_____04():
  with pt.raises(ValueError) as message:
    tl.Tile((5, 7), np.zeros((7, 5)))
  assert str(message).endswith("Cannot initialize (5, 7)-shaped Tile with an array of shape (7, 5)")

def test_get_shape__01():
  T = tl.Tile((5, 7))
  assert T.get_shape() == (5, 7)

def test___getitem__01():
  T = tl.Tile((5, 7))
  for i in range(5):
    for j in range(7):
      assert T[i,j] == 0.0

def test___setitem__01():
  T = tl.Tile((5, 7))
  for i in range(5):
    for j in range(7):
      T[i,j] = 7*i + j
  for i in range(5):
    for j in range(7):
      assert T[i,j] == 7*i + j

def test_is_empty___01():
  T = tl.Tile((5, 7))
  assert T.is_empty() == True

def test___repr_____01():
  T = tl.Tile((5, 7))
  assert str(T) == 'Empty Tile'

def test___getitem__02():
  T = tl.Tile((5, 7), np.arange(5*7).reshape((5,7)))
  for i in range(5):
    for j in range(7):
      assert T[i,j] == 7*i + j

def test___getitem__02():
  T = tl.Tile((5, 7), np.arange(5*7).reshape((5,7)))
  for i in range(5):
    for j in range(7):
      T[i,j] = i - j
  for i in range(5):
    for j in range(7):
      assert T[i,j] == i - j

def test_is_empty___02():
  T = tl.Tile((5, 7), np.arange(5*7).reshape((5,7)))
  assert T.is_empty() == False

def test___repr_____02():
  T = tl.Tile((5, 7), np.arange(5*7).reshape((5,7)))
  assert str(T) == """\
[[ 0  1  2  3  4  5  6]
 [ 7  8  9 10 11 12 13]
 [14 15 16 17 18 19 20]
 [21 22 23 24 25 26 27]
 [28 29 30 31 32 33 34]]\
"""

def test___radd_____01():
  L = 2.0
  R = tl.Tile((5, 7))
  T = L + R
  assert isinstance(T, tl.Tile)
  assert T.is_empty()

def test___radd_____02():
  L = 2.0
  R = tl.Tile((5, 7), np.ones((5, 7)))
  T = L + R
  assert isinstance(T, tl.Tile)
  for i in range(5):
    for j in range(7):
      assert T[i,j] == 3.0

def test___add______01():
  L = tl.Tile((5, 7))
  R = 2.0
  T = L + R
  assert isinstance(T, tl.Tile)
  assert T.is_empty()

def test___add______02():
  L = tl.Tile((5, 7), np.ones((5, 7)))
  R = 2.0
  T = L + R
  assert isinstance(T, tl.Tile)
  for i in range(5):
    for j in range(7):
      assert T[i,j] == 3.0

def test___add______03():
  L = tl.Tile((5, 7))
  R = tl.Tile((5, 7))
  T = L + R
  assert isinstance(T, tl.Tile)
  assert T.is_empty()

def test___add______04():
  L = tl.Tile((5, 7))
  R = tl.Tile((5, 7), np.ones((5, 7)))
  T = L + R
  assert isinstance(T, tl.Tile)
  for i in range(5):
    for j in range(7):
      assert T[i,j] == 1.0

def test___add______05():
  L = tl.Tile((5, 7), np.ones((5, 7)))
  R = tl.Tile((5, 7))
  T = L + R
  assert isinstance(T, tl.Tile)
  for i in range(5):
    for j in range(7):
      assert T[i,j] == 1.0

def test___add______06():
  L = tl.Tile((5, 7))
  R = tl.Tile((7, 5))
  with pt.raises(ValueError) as message:
    T = L + R
  assert str(message).endswith("Cannot __add__ Tiles with mismatched shapes (5, 7) and (7, 5)")

def test___add______07():
  L = tl.Tile((5, 7))
  R = tl.Tile((7, 5), np.ones((7, 5)))
  with pt.raises(ValueError) as message:
    T = L + R
  assert str(message).endswith("Cannot __add__ Tiles with mismatched shapes (5, 7) and (7, 5)")

def test___add______08():
  L = tl.Tile((7, 5), np.ones((7, 5)))
  R = tl.Tile((5, 7))
  with pt.raises(ValueError) as message:
    T = L + R
  assert str(message).endswith("Cannot __add__ Tiles with mismatched shapes (7, 5) and (5, 7)")

def test___add______09():
  L = tl.Tile((5, 7),   np.ones((5, 7)))
  R = tl.Tile((5, 7), 2*np.ones((5, 7)))
  T = L + R
  assert isinstance(T, tl.Tile)
  for i in range(5):
    for j in range(7):
      assert T[i,j] == 3.0

def test___add______10():
  L = tl.Tile((5, 7), 2*np.ones((5, 7)))
  R = tl.Tile((5, 7),   np.ones((5, 7)))
  T = L + R
  assert isinstance(T, tl.Tile)
  for i in range(5):
    for j in range(7):
      assert T[i,j] == 3.0

def test___rsub_____01():
  L = 2.0
  R = tl.Tile((5, 7))
  T = L - R
  assert isinstance(T, tl.Tile)
  assert T.is_empty()

def test___rsub_____02():
  L = 2.0
  R = tl.Tile((5, 7), np.ones((5, 7)))
  T = L - R
  assert isinstance(T, tl.Tile)
  for i in range(5):
    for j in range(7):
      assert T[i,j] == 1.0

def test___sub______01():
  L = tl.Tile((5, 7))
  R = 2.0
  T = L - R
  assert isinstance(T, tl.Tile)
  assert T.is_empty()

def test___sub______02():
  L = tl.Tile((5, 7), np.ones((5, 7)))
  R = 2.0
  T = L - R
  assert isinstance(T, tl.Tile)
  for i in range(5):
    for j in range(7):
      assert T[i,j] == -1.0

def test___sub______03():
  L = tl.Tile((5, 7))
  R = tl.Tile((5, 7))
  T = L - R
  assert isinstance(T, tl.Tile)
  assert T.is_empty()

def test___sub______04():
  L = tl.Tile((5, 7))
  R = tl.Tile((5, 7), np.ones((5, 7)))
  T = L - R
  assert isinstance(T, tl.Tile)
  for i in range(5):
    for j in range(7):
      assert T[i,j] == -1.0

def test___sub______05():
  L = tl.Tile((5, 7), np.ones((5, 7)))
  R = tl.Tile((5, 7))
  T = L - R
  assert isinstance(T, tl.Tile)
  for i in range(5):
    for j in range(7):
      assert T[i,j] == 1.0

def test___sub______06():
  L = tl.Tile((5, 7))
  R = tl.Tile((7, 5))
  with pt.raises(ValueError) as message:
    T = L - R
  assert str(message).endswith("Cannot __sub__ Tiles with mismatched shapes (5, 7) and (7, 5)")

def test___sub______07():
  L = tl.Tile((5, 7))
  R = tl.Tile((7, 5), np.ones((7, 5)))
  with pt.raises(ValueError) as message:
    T = L - R
  assert str(message).endswith("Cannot __sub__ Tiles with mismatched shapes (5, 7) and (7, 5)")

def test___sub______08():
  L = tl.Tile((7, 5), np.ones((7, 5)))
  R = tl.Tile((5, 7))
  with pt.raises(ValueError) as message:
    T = L - R
  assert str(message).endswith("Cannot __sub__ Tiles with mismatched shapes (7, 5) and (5, 7)")

def test___sub______09():
  L = tl.Tile((5, 7),   np.ones((5, 7)))
  R = tl.Tile((5, 7), 2*np.ones((5, 7)))
  T = L - R
  assert isinstance(T, tl.Tile)
  for i in range(5):
    for j in range(7):
      assert T[i,j] == -1.0

def test___sub______10():
  L = tl.Tile((5, 7), 2*np.ones((5, 7)))
  R = tl.Tile((5, 7),   np.ones((5, 7)))
  T = L - R
  assert isinstance(T, tl.Tile)
  for i in range(5):
    for j in range(7):
      assert T[i,j] == 1.0

def test___rmul_____01():
  L = 2.0
  R = tl.Tile((5, 7))
  T = L * R
  assert isinstance(T, tl.Tile)
  assert T.is_empty()

def test___rmul_____02():
  L = 2.0
  R = tl.Tile((5, 7), np.ones((5, 7)))
  T = L * R
  assert isinstance(T, tl.Tile)
  for i in range(5):
    for j in range(7):
      assert T[i,j] == 2.0

def test___mul______01():
  L = tl.Tile((5, 7))
  R = 2.0
  T = L * R
  assert isinstance(T, tl.Tile)
  assert T.is_empty()

def test___mul______02():
  L = tl.Tile((5, 7), np.ones((5, 7)))
  R = 2.0
  T = L * R
  assert isinstance(T, tl.Tile)
  for i in range(5):
    for j in range(7):
      assert T[i,j] == 2.0

def test___mul______03():
  L = tl.Tile((5, 7))
  R = tl.Tile((5, 7))
  T = L * R
  assert isinstance(T, tl.Tile)
  assert T.is_empty()

def test___mul______04():
  L = tl.Tile((5, 7))
  R = tl.Tile((5, 7), np.ones((5, 7)))
  T = L * R
  assert isinstance(T, tl.Tile)
  for i in range(5):
    for j in range(7):
      assert T[i,j] == 0.0

def test___mul______05():
  L = tl.Tile((5, 7), np.ones((5, 7)))
  R = tl.Tile((5, 7))
  T = L * R
  assert isinstance(T, tl.Tile)
  for i in range(5):
    for j in range(7):
      assert T[i,j] == 0.0

def test___mul______06():
  L = tl.Tile((5, 7))
  R = tl.Tile((7, 5))
  with pt.raises(ValueError) as message:
    T = L * R
  assert str(message).endswith("Cannot __mul__ Tiles with mismatched shapes (5, 7) and (7, 5)")

def test___mul______07():
  L = tl.Tile((5, 7))
  R = tl.Tile((7, 5), np.ones((7, 5)))
  with pt.raises(ValueError) as message:
    T = L * R
  assert str(message).endswith("Cannot __mul__ Tiles with mismatched shapes (5, 7) and (7, 5)")

def test___mul______08():
  L = tl.Tile((7, 5), np.ones((7, 5)))
  R = tl.Tile((5, 7))
  with pt.raises(ValueError) as message:
    T = L * R
  assert str(message).endswith("Cannot __mul__ Tiles with mismatched shapes (7, 5) and (5, 7)")

def test___mul______09():
  L = tl.Tile((5, 7),   np.ones((5, 7)))
  R = tl.Tile((5, 7), 2*np.ones((5, 7)))
  T = L * R
  assert isinstance(T, tl.Tile)
  for i in range(5):
    for j in range(7):
      assert T[i,j] == 2.0

def test___mul______10():
  L = tl.Tile((5, 7), 2*np.ones((5, 7)))
  R = tl.Tile((5, 7),   np.ones((5, 7)))
  T = L * R
  assert isinstance(T, tl.Tile)
  for i in range(5):
    for j in range(7):
      assert T[i,j] == 2.0

def test___rdiv_____01():
  L = 2.0
  R = tl.Tile((5, 7))
  T = L / R
  assert isinstance(T, tl.Tile)
  assert T.is_empty()

def test___rdiv_____02():
  L = 2.0
  R = tl.Tile((5, 7), np.ones((5, 7)))
  T = L / R
  assert isinstance(T, tl.Tile)
  for i in range(5):
    for j in range(7):
      assert T[i,j] == 2.0

def test___div______01():
  L = tl.Tile((5, 7))
  R = 2.0
  T = L / R
  assert isinstance(T, tl.Tile)
  assert T.is_empty()

def test___div______02():
  L = tl.Tile((5, 7), np.ones((5, 7)))
  R = 2.0
  T = L / R
  assert isinstance(T, tl.Tile)
  for i in range(5):
    for j in range(7):
      assert T[i,j] == 0.5

def test___div______03():
  L = tl.Tile((5, 7))
  R = tl.Tile((5, 7))
  T = L / R
  assert isinstance(T, tl.Tile)
  assert T.is_empty()

def test___div______04():
  L = tl.Tile((5, 7))
  R = tl.Tile((5, 7), np.ones((5, 7)))
  T = L / R
  assert isinstance(T, tl.Tile)
  for i in range(5):
    for j in range(7):
      assert T[i,j] == 0.0

def test___div______05():
  L = tl.Tile((5, 7), np.ones((5, 7)))
  R = tl.Tile((5, 7))
  T = L / R
  assert isinstance(T, tl.Tile)
  assert T.is_empty()

def test___div______06():
  L = tl.Tile((5, 7))
  R = tl.Tile((7, 5))
  with pt.raises(ValueError) as message:
    T = L / R
  assert str(message).endswith("Cannot __div__ Tiles with mismatched shapes (5, 7) and (7, 5)")

def test___div______07():
  L = tl.Tile((5, 7))
  R = tl.Tile((7, 5), np.ones((7, 5)))
  with pt.raises(ValueError) as message:
    T = L / R
  assert str(message).endswith("Cannot __div__ Tiles with mismatched shapes (5, 7) and (7, 5)")

def test___div______08():
  L = tl.Tile((7, 5), np.ones((7, 5)))
  R = tl.Tile((5, 7))
  with pt.raises(ValueError) as message:
    T = L / R
  assert str(message).endswith("Cannot __div__ Tiles with mismatched shapes (7, 5) and (5, 7)")

def test___div______09():
  L = tl.Tile((5, 7),   np.ones((5, 7)))
  R = tl.Tile((5, 7), 2*np.ones((5, 7)))
  T = L / R
  assert isinstance(T, tl.Tile)
  for i in range(5):
    for j in range(7):
      assert T[i,j] == 0.5

def test___div______10():
  L = tl.Tile((5, 7), 2*np.ones((5, 7)))
  R = tl.Tile((5, 7),   np.ones((5, 7)))
  T = L / R
  assert isinstance(T, tl.Tile)
  for i in range(5):
    for j in range(7):
      assert T[i,j] == 2.0

def test_transpose__01():
  T = tl.Tile((2,3,4))
  T = T.transpose()
  assert T.get_shape() == (4,3,2)

def test_transpose__02():
  T = tl.Tile((2,3,4))
  T = T.transpose((0,2,1))
  assert T.get_shape() == (2,4,3)

def test_transpose__03():
  T = tl.Tile((2,3,4), np.arange(2*3*4).reshape((2,3,4)))
  T = T.transpose()
  assert T.get_shape()  == (4,3,2)
  assert T._array.shape == (4,3,2)
  for i in range(2):
    for j in range(3):
      for k in range(4):
        assert T[k,j,i] == i*3*4 + j*4 + k

def test_transpose__04():
  T = tl.Tile((2,3,4), np.arange(2*3*4).reshape((2,3,4)))
  T = T.transpose((0,2,1))
  assert T.get_shape()  == (2,4,3)
  assert T._array.shape == (2,4,3)
  for i in range(2):
    for j in range(3):
      for k in range(4):
        assert T[i,k,j] == i*3*4 + j*4 + k

def test_tensordot__01():
  larray = np.random.rand(2,3,4,5,6)
  rarray = np.random.rand(6,4,5,3,3)
  tarray = np.tensordot(larray, rarray, axes=([1,2,3,4],[3,1,2,0]))
  ltile  = tl.Tile((2,3,4,5,6), larray)
  rtile  = tl.Tile((6,4,5,3,3), rarray)
  ttile  = tl.tensordot(ltile, rtile, axis_keys=([1,2,3,4],[3,1,2,0]))
  assert tarray.shape == ttile.get_shape()
  for coord in it.product(*(range(dim) for dim in tarray.shape)):
    assert ttile[coord] == tarray[coord]

def test_tensordot__02():
  larray = np.random.rand(2,3,4,5,6)
  rarray = np.random.rand(6,4,5,3,3)
  tarray = np.tensordot(larray, rarray, axes=([1,2,3,4],[3,1,2,0]))
  ltile  = tl.Tile((2,3,4,5,6), larray)
  rtile  = tl.Tile((6,4,5,3,3), None  )
  ttile  = tl.tensordot(ltile, rtile, axis_keys=([1,2,3,4],[3,1,2,0]))
  assert tarray.shape == ttile.get_shape()
  assert ttile.is_empty()

def test_tensordot__03():
  larray = np.random.rand(2,3,4,5,6)
  rarray = np.random.rand(6,4,5,3,3)
  tarray = np.tensordot(larray, rarray, axes=([1,2,3,4],[3,1,2,0]))
  ltile  = tl.Tile((2,3,4,5,6), None  )
  rtile  = tl.Tile((6,4,5,3,3), rarray)
  ttile  = tl.tensordot(ltile, rtile, axis_keys=([1,2,3,4],[3,1,2,0]))
  assert tarray.shape == ttile.get_shape()
  assert ttile.is_empty()


if __name__ == "__main__":
  L = tl.Tile((5, 7), np.ones((5, 7)))
  R = tl.Tile((5, 7))
  T = L + R
  print T
  T = tl.Tile((2,3,4), np.arange(2*3*4).reshape((2,3,4)))
  print T.get_shape()
  print T
  print T.transpose().get_shape()
  print T.transpose()

  larray = np.random.rand(2,3,4,5,6)
  rarray = np.random.rand(6,4,5,3,3)
  print [larray.shape[ax] for ax in [1,2,3,4]]
  print [rarray.shape[ax] for ax in [3,1,2,0]]
  tarray = np.tensordot(larray, rarray, axes=([1,2,3,4],[3,1,2,0]))
  print tarray
  L = tl.Tile((2,3,4,5,6), larray)
  R = tl.Tile((6,4,5,3,3), rarray)
  contract_tiles = lambda tile1, tile2: tl.tensordot(tile1, tile2, axis_keys=([1,2,3,4],[3,1,2,0]))
  T = contract_tiles(L, R)
  print T._array
