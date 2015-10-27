import itertools as it

class MultiAxis(object):

  def __init__(self, axes):
    if not hasattr(axes, "__getitem__"): axes = (axes,)
    self.axes              = axes
    self.elem_dtype        = self.select_common_axis_attribute("elem_dtype")
    self.nelemtup          = tuple(axis.nelem          for axis in axes)
    self.elem_keystup      = tuple(axis.elem_keys      for axis in axes)
    self.elem_init_argstup = tuple(axis.elem_init_args for axis in axes)

  def iter_elem_keytups(self): return it.product(*self.elem_keystup)

  def select_common_axis_attribute(self, attr_name):
    attrs = set(getattr(axis, attr_name) for axis in self.axes)
    if not len(attrs) is 1:
      raise ValueError ("Cannot construct MultiAxis from axes with mismatched {:s} values {:s}".format(attr_name, tuple(attrs)))
    attr, = attrs
    return attr

from symmetry import XOR

class IrrepMultiAxis(MultiAxis):

  def __init__(self, axes):
    super(IrrepMultiAxis, self).__init__(axes)
    self.pg_label  = super(IrrepMultiAxis, self).select_common_axis_attribute("pg_label")
    self.irrepstup = tuple(axis.irreps for axis in axes)

  def iter_elem_keytups(self): return it.ifilter(XOR(0), it.product(*self.elem_keystup))

class SpinMultiAxis(MultiAxis):

  def __init__(self, axes):
    super(SpinMultiAxis, self).__init__(axes)
    self.sp_label = super(SpinMultiAxis, self).select_common_axis_attribute("sp_label")

  def iter_elem_keytups(self): return it.ifilter(XOR(0), it.product(*self.elem_keystup))


if __name__ == "__main__":
  import axis   as ax
  import tile   as tl
  import tensor as tn

  a = ax.Axis((4,0,1,2), tl.Tile)
  ma = a*a*a
  print "MultiAxis"
  print ma.axes                
  print ma.elem_dtype          
  print ma.nelemtup         
  print ma.elem_keystup     
  print ma.elem_init_argstup
  ia = ax.IrrepAxis("C2v", (4,0,1,2), tl.Tile)
  ima = ia * ia * ia
  print "IrrepMultiAxis"
  print ima.axes                
  print ima.elem_dtype          
  print ima.nelemtup         
  print ima.elem_keystup     
  print ima.elem_init_argstup
  print ima.pg_label
  print ima.irrepstup
  sa = ax.SpinAxis("U", (ia, ia), tn.Array)
  sma = sa * sa * sa
  print "SpinMultiAxis"
  print sma.axes                
  print sma.elem_dtype          
  print sma.nelemtup         
  print sma.elem_keystup     
  print sma.elem_init_argstup
  print sma.sp_label
