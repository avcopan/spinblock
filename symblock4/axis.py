from multiaxis import MultiAxis, IrrepMultiAxis, SpinMultiAxis
import printer as pt

class Axis(MultiAxis):

  def __init__(self, elem_init_args, elem_dtype):
    if not hasattr(elem_init_args, "__getitem__"): elem_init_args = (elem_init_args,)
    self.nelem          = len(elem_init_args)
    self.elem_keys      = tuple(range(self.nelem))
    self.elem_init_args = tuple(elem_init_args)
    self.elem_dtype     = elem_dtype
    MultiAxis.__init__(self, (self,))

  def __eq__  (self, other): return isinstance(other, Axis) and other.elem_init_args == self.elem_init_args and other.elem_dtype == self.elem_dtype
  def __ne__  (self, other): return not self.__eq__(other)

  def __mul__ (self, other): return self.prod(other, False)
  def __rmul__(self, other): return self.prod(other, True )

  def __str__ (self): return pt.Axis2str(self)
  def __repr__(self): return pt.Axis2str(self)

  def __getitem__(self, args): return self.elem_init_args.__getitem__(args)

  def prod(self, other, swap = False):
    self, other = (self,), (other,) if not hasattr(other, "axes") else other.axes
    return MultiAxis(other + self) if swap else MultiAxis(self + other)


from symmetry import PG_DIM

class IrrepAxis(Axis, IrrepMultiAxis):

  def __init__(self, pg_label, elem_init_args, elem_dtype):
    Axis.__init__(self, elem_init_args, elem_dtype)
    self.pg_label = pg_label
    if self.nelem != PG_DIM[pg_label]: raise ValueError("Can't make {:s} axis with {:d} elements.".format(pg_label, self.nelem))
    IrrepMultiAxis.__init__(self, (self,))

  def __eq__  (self, other): return isinstance(other, IrrepAxis) and other.pg_label == self.pg_label and Axis.__eq__(self, other)
  def __ne__  (self, other): return not self.__eq__(other)

  def __mul__ (self, other): return self.prod(other, False)
  def __rmul__(self, other): return self.prod(other, True )

  def __str__ (self): return pt.IrrepAxis2str(self)
  def __repr__(self): return pt.IrrepAxis2str(self)

  def prod(self, other, swap = False):
    self, other = (self,), (other,) if not hasattr(other, "axes") else other.axes
    try   : return IrrepMultiAxis(other + self) if swap else IrrepMultiAxis(self + other)
    except: return      MultiAxis(other + self) if swap else      MultiAxis(self + other)

class SpinAxis(Axis, SpinMultiAxis):

  def __init__(self, sp_label, elem_init_args, elem_dtype):
    Axis.__init__(self, elem_init_args, elem_dtype)
    if not sp_label is "U": raise ValueError("Unknown SpinAxis type {:s}.".format(str(sp_label)))
    self.sp_label = "U"
    SpinMultiAxis.__init__(self, (self,))

  def __eq__  (self, other): return isinstance(other, SpinAxis) and other.sp_label == self.sp_label and Axis.__eq__(self, other)
  def __ne__  (self, other): return not self.__eq__(other)

  def __mul__ (self, other): return self.prod(other, False)
  def __rmul__(self, other): return self.prod(other, True )

  def __str__ (self): return pt.SpinAxis2str(self)
  def __repr__(self): return pt.SpinAxis2str(self)

  def prod(self, other, swap = False):
    self, other = (self,), (other,) if not hasattr(other, "axes") else other.axes
    try   : return SpinMultiAxis(other + self) if swap else SpinMultiAxis(self + other)
    except: return     MultiAxis(other + self) if swap else     MultiAxis(self + other)



if __name__ == "__main__":
  import numpy as np
  a  = Axis(7, np.ndarray)
  ia = IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  sa = SpinAxis("U", (5,5), np.ndarray)

  print a
  print ia
  print sa
