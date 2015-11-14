import numpy  as np

def tensordot(l, r, axis_keys=None):
  if isinstance(l, np.ndarray) and isinstance(r, np.ndarray):
    return np.tensordot(l, r, axes=axis_keys)
  if not hasattr(l, "multiaxis") or not hasattr(r, "multiaxis"):
    raise TypeError("Cannot tensordot objects of type(s): {:s} and {:s}".format(type(l).__name__, type(r).__name__))
  if axis_keys is None: axis_keys = ((l.ndim - 1,), (0,))
  ltrc_keys, rtrc_keys = axis_keys
  if not len(ltrc_keys) == len(rtrc_keys): raise ValueError("Invalid argument {:s} passed to tensordot".format(str(axis_keys)))
  # transpose contraction into matrix multiplication format: T_{col, row} = sum_{trc} L_{trc, col} * R_{trc, row}
  L = l.transpose(list(ltrc_keys) + sorted(set(range(l.ndim)) - set(ltrc_keys)))
  R = r.transpose(list(rtrc_keys) + sorted(set(range(r.ndim)) - set(rtrc_keys)))
  ntrc = len(ltrc_keys)
  col_axes,  trc_axes = L.multiaxis.axes[ntrc:], L.multiaxis.axes[:ntrc]
  row_axes, rtrc_axes = R.multiaxis.axes[ntrc:], R.multiaxis.axes[:ntrc]
  T = type(L)(col_axes + row_axes)
  if not trc_axes == rtrc_axes: raise ValueError("Cannot trace {:s} with {:s}".format(str(trc_axes), str(rtrc_axes)))
  multiaxis_type = type(np.prod(l.multiaxis.axes + r.multiaxis.axes))
  col_multiaxis = multiaxis_type(col_axes)
  trc_multiaxis = multiaxis_type(trc_axes)
  row_multiaxis = multiaxis_type(row_axes)
  transposed_axis_keys = (range(ntrc), range(ntrc))
  for col in col_multiaxis.iter_keytups():
    for row in row_multiaxis.iter_keytups_against(col):
      for trc in trc_multiaxis.iter_keytups_against(col):
        if T.has_data_at(col+row) and L.has_data_at(trc+col) and R.has_data_at(trc+row):
          T[col + row] += tensordot(L[trc + col], R[trc + row], transposed_axis_keys)
  return T


def indexdot((array1, index1), (array2, index2)):
  keys1 = [index1.index(char) for char in index1 if char in index2]
  keys2 = [index2.index(char) for char in index1 if char in index2]
  array = tensordot(array1, array2, axis_keys=(keys1, keys2))
  index = ''.join(char for char in index1+index2 if not (char in index1 and char in index2))
  return array, index

def eindot(targetindex, *arrayindexpairs):
  pairs = list(arrayindexpairs)
  array, index = pairs.pop(0)
  for pair in pairs: array, index = indexdot((array, index), pair)
  pmt = tuple(index.index(char) for char in targetindex)
  print pmt
  return array.transpose(pmt)


if __name__ == "__main__":
  pass
