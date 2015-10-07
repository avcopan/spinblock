from spinblock.spinblock import SpinBlockedArray

def test___getitem__():
  A = SpinBlockedArray(2,2)
  for i in range(4):
    for j in range(4):
      assert A[i,j] == 0.

def test___setitem__():
  import numpy as np
  A = SpinBlockedArray(2,2)
  A[0,0] = 5
  A[0:2,2:4] = np.array([[1., 2.], [3., 4.]])
  assert ( A[0:2,0:2] == np.array([[5., 0.], [0., 0.]]) ).all()
  assert ( A[0:2,2:4] == np.array([[1., 2.], [3., 4.]]) ).all()

def test___add__1():
  import numpy as np
  A = SpinBlockedArray(2,2)
  A[0:2,2:4] = np.array([[1., 2.], [3., 4.]])
  B = A + 1
  C = 1 + A
  D = A + B + C
  assert ( B[0:2,2:4] == np.array([[2., 3.], [ 4.,  5.]]) ).all()
  assert ( C[0:2,2:4] == np.array([[2., 3.], [ 4.,  5.]]) ).all()
  assert ( D[0:2,2:4] == np.array([[5., 8.], [11., 14.]]) ).all()

def test___add__2():
  import numpy as np
  A = SpinBlockedArray(2,2)
  B = SpinBlockedArray(2,2)
  C = SpinBlockedArray(2,2)
  D = SpinBlockedArray(2,2)
  A[0:2,0:2] = np.ones((2,2))
  B[0:2,2:4] = np.ones((2,2))
  C[2:4,0:2] = np.ones((2,2))
  D[2:4,2:4] = np.ones((2,2))
  E = A + B + C + D
  for i in range(4):
    for j in range(4):
      assert E[i,j] == 1.

def test___sub__():
  A = SpinBlockedArray(2,2)
  B = SpinBlockedArray(2,2)
  C = SpinBlockedArray(2,2)
  D = SpinBlockedArray(2,2)
