import printer
import itertools as it
from symmetry import XOR

class MultiAxis(object):

  def __init__(self, axes):
    if not hasattr(axes, "__getitem__"):
      try:    axes = tuple(axes)
      except: axes = (axes,)
    self.axes = axes
    self.ndim = len(axes)
    self.dtype = self.select_common_attribute("elem_dtype")
    self.pgsym = self.select_common_attribute("label") is not None
    self.shape = tuple(axis.nelem     for axis in axes)
    self.keys  = tuple(axis.elem_keys for axis in axes)
    self.inits = tuple(axis.elem_init for axis in axes)

  def select_common_attribute(self, attr_name):
    if all(hasattr(axis, attr_name) for axis in self.axes): attrs = set(getattr(axis, attr_name) for axis in self.axes)
    else: attrs = set()
    if   len(attrs) is 0: return None
    elif len(attrs) is 1: return attrs.pop()
    else: raise ValueError("Can't make MultiAxis from axes with mismatched {:s} values {:s}".format(attr_name, tuple(attrs)))

  def __str__ (self): return printer.MultiAxis2str(self)
  def __repr__(self): return printer.MultiAxis2str(self)

  def __eq__(self, other): return self.axes == other.axes
  def __ne__(self, other): return self.axes != other.axes

  def transpose(self, axis_keys = None):
    if axis_keys is None: axis_keys = reversed(range(self.ndim))
    return self.__class__(self.axes[key] for key in axis_keys)

  def __getitem__(self, keytup): return tuple(init[key] for init, key in zip(self.inits, keytup))

  def __iter__(self): return it.product(*self.keys)

  def iter_array(self):
    if not self.pgsym: return self.__iter__()
    else:              return it.ifilter(lambda kt: XOR(kt) == 0, self.__iter__())

  def iter_complement(self, keytup):
    if not self.pgsym:         return self.__iter__()
    else: irrep = XOR(keytup); return it.ifilter(lambda kt: XOR(kt) == irrep, self.__iter__())







import pytest

def testV__init__V01():
  import axis as ax
  import numpy as np
  a = ax.Axis((4,0,1,2), np.ndarray)
  ma = MultiAxis((a, a, a))
  assert( ma.axes  == (ax.Axis((4, 0, 1, 2), np.ndarray),)*3    )
  assert( ma.ndim  == 3                                         )
  assert( ma.dtype == np.ndarray                                )
  assert( ma.pgsym == False                                     )
  assert( ma.shape == (4, 4, 4)                                 )
  assert( ma.keys  == ((0, 2, 3), (0, 2, 3), (0, 2, 3))         )
  assert( ma.inits == ((4, 0, 1, 2), (4, 0, 1, 2), (4, 0, 1, 2)))

def testV__init__V02():
  ma = MultiAxis(())
  assert( ma.axes  == ()   )
  assert( ma.ndim  == 0    )
  assert( ma.dtype == None )
  assert( ma.pgsym == False)
  assert( ma.shape == ()   )
  assert( ma.keys  == ()   )
  assert( ma.inits == ()   )

def testV__init__V03():
  import axis as ax
  import numpy as np
  a = ax.IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  ma = MultiAxis((a, a, a))
  assert( ma.axes  == (ax.IrrepAxis("C2v", (4,0,1,2), np.ndarray),)*3 )
  assert( ma.ndim  == 3                                               )
  assert( ma.dtype == np.ndarray                                      )
  assert( ma.pgsym == True                                            )
  assert( ma.shape == (4, 4, 4)                                       )
  assert( ma.keys  == ((0, 2, 3), (0, 2, 3), (0, 2, 3))               )
  assert( ma.inits == ((4, 0, 1, 2), (4, 0, 1, 2), (4, 0, 1, 2))      )

def testV__init__V04():
  import axis as ax
  import numpy as np
  a = ax.Axis((4,0,1,2), np.ndarray)
  b = ax.IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  ma = MultiAxis((a, b, a, b))

  assert( ma.axes  == (ax.Axis((4,0,1,2), np.ndarray), ax.IrrepAxis("C2v", (4,0,1,2), np.ndarray))*2 )
  assert( ma.ndim  == 4                                                                              )
  assert( ma.dtype == np.ndarray                                                                     )
  assert( ma.pgsym == False                                                                          )
  assert( ma.shape == (4, 4, 4, 4)                                                                   )
  assert( ma.keys  == ((0, 2, 3), (0, 2, 3), (0, 2, 3), (0, 2, 3))                                   )
  assert( ma.inits == ((4, 0, 1, 2), (4, 0, 1, 2), (4, 0, 1, 2), (4, 0, 1, 2))                       )

def testV__transpose__V01():
  import axis as ax
  import numpy as np
  a = ax.Axis((3,   ), np.ndarray)
  b = ax.Axis((3,4  ), np.ndarray)
  c = ax.Axis((3,4,5), np.ndarray)
  ma1 = MultiAxis((a, b, c))
  ma2 = ma1.transpose()
  ma3 = ma1.transpose((0,2,1))
  ma4 = ma1.transpose().transpose()

  assert( ma1 == ma4 )

  assert( ma2.axes  == (c, b, a)                 )
  assert( ma2.ndim  == 3                         )
  assert( ma2.dtype == np.ndarray                )
  assert( ma2.pgsym == False                     )
  assert( ma2.shape == (3, 2, 1)                 )
  assert( ma2.keys  == ((0, 1, 2), (0, 1), (0,)) )
  assert( ma2.inits == ((3, 4, 5), (3, 4), (3,)) )

  assert( ma3.axes  == (a, c, b)                 )
  assert( ma3.ndim  == 3                         )
  assert( ma3.dtype == np.ndarray                )
  assert( ma3.pgsym == False                     )
  assert( ma3.shape == (1, 3, 2)                 )
  assert( ma3.keys  == ((0,), (0, 1, 2), (0, 1)) )
  assert( ma3.inits == ((3,), (3, 4, 5), (3, 4)) )

def testV__getitem__V01():
  import axis as ax
  import numpy as np
  a = ax.Axis((4,0,1,2), np.ndarray)
  ma = MultiAxis((a, a))

  assert( ma[0,0] == (4, 4) )
  assert( ma[0,1] == (4, 0) )
  assert( ma[0,2] == (4, 1) )
  assert( ma[0,3] == (4, 2) )
  assert( ma[1,0] == (0, 4) )
  assert( ma[1,1] == (0, 0) )
  assert( ma[1,2] == (0, 1) )
  assert( ma[1,3] == (0, 2) )
  assert( ma[2,0] == (1, 4) )
  assert( ma[2,1] == (1, 0) )
  assert( ma[2,2] == (1, 1) )
  assert( ma[2,3] == (1, 2) )
  assert( ma[3,0] == (2, 4) )
  assert( ma[3,1] == (2, 0) )
  assert( ma[3,2] == (2, 1) )
  assert( ma[3,3] == (2, 2) )

def testV__iter__V01():
  import axis as ax
  import numpy as np
  a = ax.Axis((4,0,1,2), np.ndarray)
  ma = MultiAxis((a, a))
  assert( list(ma.__iter__()) == [(0, 0), (0, 2), (0, 3), (2, 0), (2, 2), (2, 3), (3, 0), (3, 2), (3, 3)] )

def testViter_arrayV01():
  import axis as ax
  import numpy as np
  a = ax.IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  ma = MultiAxis((a, a))
  assert( list(ma.iter_array()) == [(0, 0), (2, 2), (3, 3)] )

def testViter_complementV01():
  import axis as ax
  import numpy as np
  a = ax.IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  ma = MultiAxis((a, a))

  assert( list(ma.iter_complement((0,))) == [(0, 0), (2, 2), (3, 3)] )
  assert( list(ma.iter_complement((1,))) == [(2, 3), (3, 2)]         )
  assert( list(ma.iter_complement((2,))) == [(0, 2), (2, 0)]         )
  assert( list(ma.iter_complement((3,))) == [(0, 3), (3, 0)]         )

def testV__iter__V02():
  ma = MultiAxis(())
  assert( list(ma.__iter__()) == [()] )

def testViter_arrayV02():
  ma = MultiAxis(())
  assert( list(ma.iter_array()) == [()] )

def testViter_complementV02():
  ma = MultiAxis(())
  assert( list(ma.iter_complement('chicken')) == [()] )

if __name__ == "__main__":
  testV__init__V01()
  testV__init__V02()
  testV__init__V03()
  testV__init__V04()
  testV__transpose__V01()
  testV__getitem__V01()
  testV__iter__V01()
  testViter_arrayV01()
  testViter_complementV01()
  testV__iter__V02()
  testViter_arrayV02()
  testViter_complementV02()
