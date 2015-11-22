import numpy as np
import os.path
from tempfile import mkdtemp

class diskarray(np.memmap):

  def __new__(cls, shape):
    filename = os.path.join(mkdtemp(), 'diskarray.bin')
    return super(diskarray, cls).__new__(cls, filename, dtype=np.float64, mode='w+', shape=shape)

if __name__ == "__main__":
  a = diskarray((5, 5))
  a.fill(1)
  print a
  b = diskarray((5, 5))
  b.fill(2)
  print b
  print type(b)
  c = a + b
  print type(c)
  c[0,0] = 13
  c[1,1] = 7
  print c
  import test_disk as tst
  tst.testV__init__V01()
  tst.testV__init__V02()
  tst.testV__init__V03()
  tst.testV__init__V04()
  tst.testV__init__V05()
  tst.testV__init__V06()
  tst.testV__init__V07()
