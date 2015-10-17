from tile import Tile
import numpy as np

def test___getitem__1():
  T = Tile((5, 7))
  for i in range(5):
    for j in range(7):
      assert T[i,j] == 0.0

def test___setitem__1():
  T = Tile((5, 7))
  for i in range(5):
    for j in range(7):
      T[i,j] = 7*i + j
  for i in range(5):
    for j in range(7):
      assert T[i,j] == 7*i + j

def test___nonzero__1():
  T = Tile((5, 7))
  assert bool(T) == False

def test___repr_____1():
  T = Tile((5, 7))
  assert str(T) == 'Empty Tile'

def test___getitem__2():
  T = Tile((5, 7), np.arange(5*7).reshape((5,7)))
  for i in range(5):
    for j in range(7):
      assert T[i,j] == 7*i + j

def test___getitem__2():
  T = Tile((5, 7), np.arange(5*7).reshape((5,7)))
  for i in range(5):
    for j in range(7):
      T[i,j] = i - j
  for i in range(5):
    for j in range(7):
      assert T[i,j] == i - j

def test___nonzero__2():
  T = Tile((5, 7), np.arange(5*7).reshape((5,7)))
  assert bool(T) == True

def test___repr_____2():
  T = Tile((5, 7), np.arange(5*7).reshape((5,7)))
  assert str(T) == """\
array([[ 0,  1,  2,  3,  4,  5,  6],
       [ 7,  8,  9, 10, 11, 12, 13],
       [14, 15, 16, 17, 18, 19, 20],
       [21, 22, 23, 24, 25, 26, 27],
       [28, 29, 30, 31, 32, 33, 34]])\
"""
