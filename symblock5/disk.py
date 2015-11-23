import numpy as np
import os.path
from tempfile import mkdtemp

class diskarray(np.memmap):

  def __new__(cls, shape, name = 'tmp'):
    if name is 'tmp': filename = os.path.join(mkdtemp(), 'diskarray.bin')
    else:             filename = os.path.join('/tmp', name + '.bin')
    if os.path.isfile(filename):
      return super(diskarray, cls).__new__(cls, filename, dtype=np.float64, mode='r+', shape=shape)
    else:
      return super(diskarray, cls).__new__(cls, filename, dtype=np.float64, mode='w+', shape=shape)

  def __mod__ (self, other):
    return self.dot(other)

  def __rmod__(self, other):
    return other.dot(self)

  def dot     (self, other):
    return np.tensordot(self, other, axes = (self.ndim - 1, 0))


if __name__ == "__main__":
  c = diskarray((2, 3), name = 'myarray')
  d = diskarray((2, 3), name = 'myarray')
  print c
  c.fill(1)
  print d
  
  import test_disk as tst
  tst.testV__init__V01()
  tst.testV__init__V02()
  tst.testV__init__V03()
  tst.testV__init__V04()
  tst.testV__init__V05()
  tst.testV__init__V06()
  tst.testV__init__V07()
