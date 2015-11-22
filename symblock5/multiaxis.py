import printer
import itertools  as it
import numpy      as np
from symmetry import XOR
from axis     import Axis

class MultiAxis(object):

  def __init__(self, axes):
    if isinstance(axes, Axis):
      axes = (axes,)
    self.axes = tuple(axes)
    self.ndim = len(self.axes)
    self.dtype = self.select_common_attribute("elem_dtype")
    if self.dtype is None: self.dtype = np.ndarray
    self.pgsym = self.select_common_attribute("label") is not None
    self.shape = tuple(axis.nelem     for axis in self.axes)
    self.keys  = tuple(axis.elem_keys for axis in self.axes)
    self.inits = tuple(axis.elem_init for axis in self.axes)

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


if __name__ == "__main__":
  import test_multiaxis as tst
  tst.testV__init__V01()
  tst.testV__init__V02()
  tst.testV__init__V03()
  tst.testV__init__V04()
  tst.testV__transpose__V01()
  tst.testV__getitem__V01()
  tst.testV__iter__V01()
  tst.testViter_arrayV01()
  tst.testViter_complementV01()
  tst.testV__iter__V02()
  tst.testViter_arrayV02()
  tst.testViter_complementV02()
