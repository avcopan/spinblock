import numpy   as np
import printer

class Axis(object):

  def __init__(self, elem_init, elem_dtype):
    if isinstance(elem_init, int) or isinstance(elem_init, Axis):
      elem_init = (elem_init,)
    self.nelem      = len(elem_init)
    self.elem_init  = tuple(elem_init)
    self.elem_dtype = elem_dtype
    if issubclass(elem_dtype, np.ndarray):
      self.elem_keys = tuple(key for key in range(self.nelem) if not elem_init[key] is 0)
    else:
      self.elem_keys = tuple(range(self.nelem))

  def __eq__  (self, other): return isinstance(other, type(self)) and other.elem_init == self.elem_init and other.elem_dtype == self.elem_dtype
  def __ne__  (self, other): return not self.__eq__(other)

  def __str__ (self): return printer.Axis2str(self)
  def __repr__(self): return printer.Axis2str(self)

  def __getitem__(self, key): return self.elem_init[key]


from symmetry import PG_DIM

class IrrepAxis(Axis):

  def __init__(self, label, elem_init, elem_dtype):
    Axis.__init__(self, elem_init, elem_dtype)
    self.label = label
    if self.nelem != PG_DIM[label]: raise ValueError("Can't make {:s} IrrepAxis with {:d} elements.".format(label, self.nelem))

  def __eq__ (self, other): return Axis.__eq__(self, other) and other.label == self.label
  def __ne__ (self, other): return not self.__eq__(other)

  def __str__ (self): return printer.IrrepAxis2str(self)
  def __repr__(self): return printer.IrrepAxis2str(self)



if __name__ == "__main__":
  import test_axis as tst
  tst.testV__init__V01()
  tst.testV__eq__V01()
  tst.testV__getitem__V01()
  tst.testV__init__V02()
  tst.testV__init__V03()
  tst.testV__ne__V01()
  tst.testV__eq__V02()
  tst.testV__getitem__V02()
