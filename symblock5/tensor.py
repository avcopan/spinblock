import numpy   as np
import os.path as osp
from tempfile import mkdtemp

class tensor(object):

  def __mod__ (self, other):
    return self.matmul(other)

  def __rmod__(self, other):
    return other.matmul(self)

  def matmul(self, other):
    return np.tensordot(self, other, axes = (self.ndim - 1, 0))

  def broadcast(self, shape, axes=None):
    ndim = len(shape)
    if axes is None: axes = range(ndim - self.ndim, ndim)
    pmt = tuple(key for key in range(ndim) if not key in axes) + tuple(axes)
    inv, _ = zip(*sorted(enumerate(pmt), key=lambda x: x[1]))
    return np.broadcast_to(self, tuple(shape[key] for key in pmt)).transpose(inv)


class coretensor(tensor, np.ndarray):

  def __new__(cls, shape):
    return np.ndarray.__new__(cls, shape)


class disktensor(tensor, np.memmap):

  def __new__(cls, shape, name = 'tmp'):
    if name is 'tmp': filename = osp.join(mkdtemp(), 'tmp.bin')
    else:             filename = osp.join('/tmp', name + '.bin')
    if osp.isfile(filename):
      return np.memmap.__new__(cls, filename, dtype=np.float64, mode='r+', shape=shape)
    else:
      return np.memmap.__new__(cls, filename, dtype=np.float64, mode='w+', shape=shape)

if __name__ == "__main__":
  d = disktensor((5, 5), name='myarray')
  d.fill(0)
  print d
  e = disktensor((5, 5), name='myarray')
  e.fill(7)
  print d

  a = disktensor((3, 7))
  b = disktensor((7, 2))
  a.fill(1)
  b.fill(1)
  c = a % b
  print c

  d = coretensor((5,))
  for i in range(5): d[i] = i
  print d.broadcast((5, 5))
  print d.broadcast((5, 5), axes=(0,))
