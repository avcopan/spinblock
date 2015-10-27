import itertools as it
import multiaxis as ma

class Axis(ma.MultiAxis):

  def __init__(self, elem_init_args, elem_dtype):
    if not hasattr(elem_init_args, "__getitem__"): elem_init_args = (elem_init_args,)
    self.nelem          = len(elem_init_args)
    self.elem_keys      = tuple(range(self.nelem))
    self.elem_init_args = tuple(elem_init_args)
    self.elem_dtype     = elem_dtype
    ma.MultiAxis.__init__(self, (self,))

  def __mul__ (self, other): return self.prod(other, False)
  def __rmul__(self, other): return self.prod(other, True )

  def prod(self, other, swap = False):
    self, other = (self,), (other,) if not hasattr(other, "axes") else other.axes
    return ma.MultiAxis(other + self) if swap else ma.MultiAxis(self + other)


from symmetry import IRREPS

class IrrepAxis(Axis, ma.IrrepMultiAxis):

  def __init__(self, pg_label, irrep_tile_init_args, container_dtype):
    Axis.__init__(self, irrep_tile_init_args, container_dtype)
    self.pg_label = pg_label
    self.irreps   = IRREPS[pg_label]
    ma.IrrepMultiAxis.__init__(self, (self,))

  def __mul__ (self, other): return self.prod(other, False)
  def __rmul__(self, other): return self.prod(other, True )

  def prod(self, other, swap = False):
    self, other = (self,), (other,) if not hasattr(other, "axes") else other.axes
    try   : return ma.IrrepMultiAxis(other + self) if swap else ma.IrrepMultiAxis(self + other)
    except: return      ma.MultiAxis(other + self) if swap else      ma.MultiAxis(self + other)

class SpinAxis(Axis, ma.SpinMultiAxis):

  def __init__(self, sp_label, spin_tile_init_args, container_dtype):
    Axis.__init__(self, spin_tile_init_args, container_dtype)
    if not sp_label is "U": raise ValueError("{:s}-type spin axis not yet implemented.".format(str(sp_label)))
    self.sp_label = "U"
    ma.SpinMultiAxis.__init__(self, (self,))

  def __mul__ (self, other): return self.prod(other, False)
  def __rmul__(self, other): return self.prod(other, True )

  def prod(self, other, swap = False):
    self, other = (self,), (other,) if not hasattr(other, "axes") else other.axes
    try   : return ma.SpinMultiAxis(other + self) if swap else ma.SpinMultiAxis(self + other)
    except: return     ma.MultiAxis(other + self) if swap else     ma.MultiAxis(self + other)


if __name__ == "__main__":
  import numpy  as np
  import tile   as tl
  import tensor as tn
  a = Axis((4,0,1,2), np.ndarray)
  print "Axis"
  print a.nelem         
  print a.elem_keys     
  print a.elem_init_args
  print a.elem_dtype    
  ia = IrrepAxis("C2v", (4,0,1,2), tl.Tile)
  print "IrrepAxis"
  print ia.nelem         
  print ia.elem_keys     
  print ia.elem_init_args
  print ia.elem_dtype    
  print ia.pg_label
  print ia.irreps
  sa = SpinAxis("U", (ia, ia), tn.Array)
  print "SpinAxis"
  print sa.nelem         
  print sa.elem_keys     
  print sa.elem_init_args
  print sa.elem_dtype    
  print sa.sp_label
