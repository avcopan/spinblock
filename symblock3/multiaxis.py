import itertools as it
import numpy     as np
import printer   as pt

class MultiAxis(object):

  def __init__(self, axes):
    if not hasattr(axes, "__getitem__"): axes = (axes,)
    self.axes      = axes
    self.ndim      = len(axes)
    self.dtype     = self.select_common_attribute("elem_dtype")
    self.shape     = tuple(axis.nelem          for axis in axes)
    self.keys      = tuple(axis.elem_keys      for axis in axes)
    self.init_args = tuple(axis.elem_init_args for axis in axes)

  def __eq__(self, other): return self.axes == other.axes
  def __ne__(self, other): return self.axes != other.axes

  def __str__(self): return pt.MultiAxis2str(self)

  def transpose(self, axis_keys = None):
    if axis_keys is None: axis_keys = tuple(reversed(range(self.ndim)))
    return np.prod([self.axes[axis_key] for axis_key in axis_keys])

  def iter_array_keytups(self):           return it.product(*self.keys)
  def iter_keytups(self):                 return it.product(*self.keys)
  def iter_keytups_against(self, keytup): return it.product(*self.keys)

  def select_common_attribute(self, attr_name):
    attrs = set(getattr(axis, attr_name) for axis in self.axes)
    try:    attr, = attrs; return attr
    except: raise ValueError("Can't make MultiAxis from axes with mismatched {:s} values {:s}".format(attr_name, tuple(attrs)))

from symmetry import XOR, PG_DIM

class IrrepMultiAxis(MultiAxis):

  def __init__(self, axes):
    MultiAxis.__init__(self, axes)
    self.pg_label  = MultiAxis.select_common_attribute(self, "pg_label")

  def __eq__(self, other): return self.axes == other.axes
  def __ne__(self, other): return self.axes != other.axes

  def __str__(self): return pt.IrrepMultiAxis2str(self)

  def iter_array_keytups(self): return it.ifilter(lambda keytup: XOR(keytup) == 0, it.product(*self.keys))
  def iter_keytups(self):       return it.product(*self.keys)
  def iter_keytups_against(self, keytup):
    irrep = XOR(col_keytup)
    return it.ifilter(lambda keytup: XOR(keytup) == irrep, it.product(*self.keys))


class SpinMultiAxis(MultiAxis):

  def __init__(self, axes):
    MultiAxis.__init__(self, axes)
    self.sp_label = MultiAxis.select_common_attribute(self, "sp_label")

  def __eq__(self, other): return self.axes == other.axes
  def __ne__(self, other): return self.axes != other.axes

  def __str__(self): return pt.SpinMultiAxis2str(self)

  def iter_array_keytups(self): return it.ifilter(lambda keytup: XOR(keytup) == 0, it.product(*self.keys))
  def iter_keytups(self):       return it.product(*self.keys)
  def iter_keytups_against(self, keytup):
    spin = XOR(col_keytup)
    return it.ifilter(lambda keytup: XOR(keytup) == spin, it.product(*self.keys))


if __name__ == "__main__":
  import axis as ax
  import numpy as np
  a = ax.IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  b = ax.SpinAxis("U", (5,5), np.ndarray)
  c = ax.Axis(7, np.ndarray)

  print a*a*a
  print b*b*b
  print c*c*c*c
  print a*b*c

  print type(a*a*a)
  print type(a*a*a) == type(a*a*a)
