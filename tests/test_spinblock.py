import numpy as np
from spinblock.spinblock import SpinBlockedArray

def test___getitem__():
  A = SpinBlockedArray(2,2)
  for i in range(4):
    for j in range(4):
      assert A[i,j] == 0

def test___setitem__():
  A = SpinBlockedArray(2,2)
  A[0,0] = 5
  A[3,3] = 7
  assert ( A.blocks[(0,0)] == np.array([[5., 0.], [0., 0.]]) ).all()
  assert ( A.blocks[(1,1)] == np.array([[0., 0.], [0., 7.]]) ).all()
  

