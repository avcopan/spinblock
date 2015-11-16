import numpy   as np
import printer

class Axis(object):

  def __init__(self, elem_init, elem_dtype):
    if not hasattr(elem_init, "__getitem__"):
      try:    elem_init = tuple(elem_init)
      except: elem_init = (elem_init,)
    self.nelem      = len(elem_init)
    self.elem_init  = tuple(elem_init)
    self.elem_dtype = elem_dtype
    if elem_dtype is np.ndarray:
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




import pytest

def testV__init__V01():
  ax = Axis((4,0,1,2), np.ndarray)
  assert( ax.nelem      == 4            )
  assert( ax.elem_init  == (4, 0, 1, 2) )
  assert( ax.elem_dtype == np.ndarray   )
  assert( ax.elem_keys  == (0, 2, 3)    )

def testV__eq__V01():
  ax1 = Axis((4,0,1,2), np.ndarray)
  ax2 = Axis((4,0,1,2), np.ndarray)
  assert( ax1 == ax2 )

def testV__getitem__V01():
  ax = Axis((4,0,1,2), np.ndarray)
  assert( ax[0] == 4 )
  assert( ax[1] == 0 )
  assert( ax[2] == 1 )
  assert( ax[3] == 2 )

def testV__init__V02():
  ax = IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  assert( ax.label      == "C2v"        ) 
  assert( ax.nelem      == 4            )
  assert( ax.elem_init  == (4, 0, 1, 2) )
  assert( ax.elem_dtype == np.ndarray   )
  assert( ax.elem_keys  == (0, 2, 3)    )

def testV__init__V03():
  with pytest.raises(ValueError) as message:
    ax = IrrepAxis("C2v", (4,1,2), np.ndarray)
  assert str(message).endswith("Can't make C2v IrrepAxis with 3 elements.")

def testV__ne__V01():
  ax1 = IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  ax2 = IrrepAxis("C2h", (4,0,1,2), np.ndarray)
  assert( ax1 != ax2 )

def testV__eq__V02():
  ax1 = IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  ax2 = IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  assert( ax1 == ax2 )
  
def testV__getitem__V02():
  ax = IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  assert( ax[0] == 4 )
  assert( ax[1] == 0 )
  assert( ax[2] == 1 )
  assert( ax[3] == 2 )

if __name__ == "__main__":
  testV__init__V01()
  testV__eq__V01()
  testV__getitem__V01()
  testV__init__V02()
  testV__init__V03()
  testV__ne__V01()
  testV__eq__V02()
  testV__getitem__V02()

  
