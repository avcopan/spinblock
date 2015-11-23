import numpy as np

class corearray(np.ndarray):

  def __new__(cls, shape):
    return super(corearray, cls).__new__(cls, shape)

  def __mod__ (self, other):
    return self.dot(other)

  def __rmod__(self, other):
    return other.dot(self)

  def dot     (self, other):
    return np.tensordot(self, other, axes = (self.ndim - 1, 0))

  def broadcast(self, shape, axes):
    ndim = len(shape)
    if axes is None: axes = range(ndim - self.ndim, ndim)
    pmt = tuple(key for key in range(ndim) if not key in axes) + tuple(axes)
    inv, _ = zip(*sorted(enumerate(pmt), key=lambda x:x[1]))
    return np.broadcast_to(self, tuple(axes[key] for key in pmt)).transpose(inv)


if __name__ == "__main__":
  a = corearray((5, 5))
  a.fill(1)
  print a
  b = corearray((5, 5))
  b.fill(2)
  print b
  print type(b)
  c = a + b
  print type(c)
  c[0,0] = 13
  c[1,1] = 7
  print c
  import test_core as tst
  tst.testV__init__V01()
  tst.testV__init__V02()
  tst.testV__init__V03()
  tst.testV__init__V04()
  tst.testV__init__V05()
  tst.testV__init__V06()
  tst.testV__init__V07()
  
