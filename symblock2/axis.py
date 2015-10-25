import itertools as it
import tile      as tl

class Axis(object):

  def __init__(self, elem_init_args, elem_dtype):
    self.nelem          = len(elem_init_args)
    self.elem_keys      = tuple(range(self.nelem))
    self.elem_init_args = elem_init_args
    self.elem_dtype     = elem_dtype

IRREPS = {
        #  'Ag'  'B1g'  'B2g'  'B3g'   'Au'  'B1u'  'B2u'  'B3u'
 'D2h': [0b000, 0b001, 0b010, 0b011, 0b100, 0b101, 0b110, 0b111],
        #  'Ag'   'Bg'   'Au'   'Bu'
 'C2h': [ 0b00,  0b01,  0b10,  0b11                            ],
        #  'A1'   'A2'   'B1'   'B2'
 'C2v': [ 0b00,  0b01,  0b10,  0b11                            ],
        #   'A'   'B1'   'B2'   'B3'
 'D2' : [ 0b00,  0b01,  0b10,  0b11                            ],
        #  'Ap'  'App'
 'Cs' : [  0b0,   0b1                                          ],
        #  'Ag'   'Au'
 'Ci' : [  0b0,   0b1                                          ],
        #   'A'    'B'
 'C2' : [  0b0,   0b1                                          ],
        #   'A'
 'C1' : [  0b0                                                 ]
}

class IrrepAxis(Axis):

  def __init__(self, point_group_label, irrep_tile_init_args, container_dtype = tl.Tile):
    super(IrrepAxis, self).__init__(irrep_tile_init_args, irrep_tile_dtype)
    self.point_group_label = point_group_label
    self.irreps            = IRREPS[point_group_label]

class UnrestrictedSpinAxis(Axis):

  def __init__(self, spin_tile_init_args, container_dtype = tn.TiledTensor):
    super(UnrestrictedSpinAxis, self).__init__(spin_tile_init_args, container_dtype)
    self.spins = [0, 1]

def multi_attr_tup(objects, attr_name, args = None):
  if args is None: return tuple(getattr(obj, attr_name)      for obj      in     objects       )
  else           : return tuple(getattr(obj, attr_name)(arg) for obj, arg in zip(objects, args))

class MultiAxis(object):

  def __init__(self, axes):
    dtypes = set(multi_attr_tup(axes, "elem_dtype"))
    if not len(dtypes) is 1:
      raise ValueError("Cannot construct MultiAxis with multiple datatypes {:s}".format(str(multi_attr_tup(dtypes, "__name__"))))
    self.axes   = axes
    self.shape  = multi_attr_tup(axes, "nelem")
    self.dtype, = dtypes

  def iter_elem_keytups(self): return it.product(*multi_attr_tup(self.axes, "elem_keys"))

  def iter_elem_init_args(self):
    for key_arg_pairs in it.product(*(enumerate(args) for args in multi_attr_tup(self.axes, "elem_init_args"))):
      yield zip(*key_arg_pairs)


if __name__ == "__main__":
  import numpy as np
  ax = Axis((4,1,2), np.ndarray)
  multiax = MultiAxis((ax, ax, ax))
  print [x for x in multiax.iter_elem_keytups()]
  print [x for x in multiax.iter_elem_init_args()]

