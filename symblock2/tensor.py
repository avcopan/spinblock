import axis  as ax
import numpy as np

class Container(object):

  def __init__(self, axes):
    self.ma    = ax.MultiAxis(axes)
    self.array = np.empty(self.ma.shape, dtype=self.ma.dtype)
    for elem_keytup, elem_init_args in self.ma.iter_elem_init_args():
      self.array[elem_keytup] = self.ma.dtype(elem_init_args)

  def __repr__(self): return self.array.__str__()

  def __getitem__(self, *args): return self.array.__getitem__(*args)

  def __setitem__(self, *args): self.array.__setitem__(*args)

if __name__ == "__main__":
  a1 = ax.Axis((1,2), np.ndarray)
  c1 = Container((a1, a1))

  for i in range(2):
    for j in range(2):
      c1[i,j].fill(0)

  print c1

  a2 = ax.Axis((a1, a1), Container)
  c2 = Container((a2, a2))

  for i in range(2):
    for j in range(2):
      for k in range(2):
        for l in range(2):
          c2[i,j][k,l].fill(2*i + j)

  print c2
