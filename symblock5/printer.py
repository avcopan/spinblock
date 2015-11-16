import itertools as it

def Array2str(array):
  import itertools as it
  rows   = list(it.product(*array.multiaxis.keys[:-1]))
  cols   = list(it.product(*array.multiaxis.keys[-1:]))
  rowlbs = [str(row).replace(',','').rstrip(")") for row in rows]
  collbs = [str(col).replace(',','').lstrip("(") for col in cols]
  lbwd   = max(len(rowlb) for rowlb in rowlbs)
  colwd  = max(len(collb) for collb in collbs)
  fmt = lambda lb, it: ("  {:{wd1}s}"+" {:{wd2}s}"*len(cols)+"\n").format(lb, *it, wd1=lbwd, wd2=colwd)
  ret = fmt('', collbs)
  for lb, r in zip(rowlbs, rows): ret += fmt(lb, ('-' if array.array[r+c] is None else '#' for c in cols))
  return "Array {{\n{:s}dtype = {:s}}}".format(ret, array.multiaxis.dtype.__name__)

def Axis2str(axis):
  return "Axis({:s}, {:s})".format(str(axis.elem_init), axis.elem_dtype.__name__)

def IrrepAxis2str(irrepaxis):
  return "IrrepAxis({:s}, {:s}, {:s})".format(irrepaxis.label, str(irrepaxis.elem_init), irrepaxis.elem_dtype.__name__)

def MultiAxis2str(multiaxis):
  return "MultiAxis {{\n{:s}}}".format(''.join("  {:s}\n".format(str(axis)) for axis in multiaxis.axes))
