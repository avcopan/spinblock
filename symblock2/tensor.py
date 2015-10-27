import numpy     as np
import multiaxis as ma
# avoiding Tile objects altogether now -- just realized that it's probably not necessary

class Array(object):

  def __init__(self, axes):
    if not hasattr(axes, "__getitem__"): axes = (axes,)
    self.ma    = np.prod(axes)
    self.shape = self.ma.nelemtup
    self.dtype = self.ma.elem_dtype
    self.array = np.empty(self.shape, self.dtype)
    for elem_keytup in self.ma.iter_elem_keytups():
      init_args = tuple(elem_init_args[elem_key] for elem_init_args, elem_key in zip(self.ma.elem_init_argstup, elem_keytup))
      self.array[elem_keytup] = self.dtype( init_args )

  def __repr__(self):
    import itertools as it
    rows  , cols   = list(it.product(*self.ma.elem_keystup[:-1]))          , list(it.product(*self.ma.elem_keystup[-1:]))
    rowlbs, collbs = [str(row).replace(',','').rstrip(")") for row in rows], [str(keytup).replace(',','').lstrip("(") for keytup in cols]
    lbwd  , colwd  = max(len(rowlb) for rowlb in rowlbs)                   , max(len(collb) for collb in collbs)
    fmt = lambda lb, it: ("  {:{wd1}s}"+" {:{wd2}s}"*len(cols)+"\n").format(lb, *it, wd1=lbwd, wd2=colwd)
    ret = fmt('', collbs)
    for lb, r in zip(rowlbs, rows): ret += fmt(lb, ('-' if self.array[r+c] is None else '#' for c in cols))
    return "Array {{\n{:s}dtype = {:s}}}".format(ret, self.dtype.__name__)

  def __getitem__(self, *args): return self.array[args[0]]
  def __setitem__(self, *args):        self.array[args[0]] = args[1]

if __name__ == "__main__":
  import axis as ax
  a  = ax.Axis(7, np.ndarray)
  ia = ax.IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  sa = ax.SpinAxis("U", (ia, ia), Array)

  O = Array(ia)
  A = Array(( a,  a))
  B = Array(( a, ia))
  C = Array((ia, ia))
  D = Array((sa, sa))

  print O
  print A
  print B
  print C
  print D

  print Array((ia, ia, ia))
