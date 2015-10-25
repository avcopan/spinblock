import numpy as np

class Container(object):

  def __init__(self, axis):
    self.axis  = axis
    self.array = np.empty(axis.dim, dtype=np.object)
    for i in range(axis.dim):
      self.array[i] = axis.dtype(axis.constructor_args[i])

  def __repr__(self):
    return self.array.__str__()

class Axis(object):

  def __init__(self, constructor_args, dtype):
    self.dim = len(constructor_args)
    self.constructor_args = constructor_args
    self.dtype = dtype

l1_ax = Axis(( 4, 0,  1, 2), np.ndarray)
l2_ax = Axis((l1_ax, l1_ax), Container)
l3_ax = Axis((l2_ax, l2_ax), Container)
l4_ax = Axis((l3_ax, l3_ax), Container)

l4 = Container(l4_ax)

print l4.array
