import numpy  as np
import tensor as tn

def tensordot(l, r, axis_keys=((0,),(0,))):
  if isinstance(l, np.ndarray) and isinstance(r, np.ndarray):
    return np.tensordot(l, r, axes=axis_keys)
  elif isinstance(l, tn.Array) and isinstance(r, tn.Array):
    ltrc_keys, rtrc_keys = axis_keys
    if not len(ltrc_keys) == len(rtrc_keys): raise ValueError("Invalid argument {:s} passed to tensordot".format(str(axis_keys)))
    # transpose contraction into matrix multiplication format: T_{col, row} = sum_{trc} L_{trc, col} * R_{trc, row}
    L = l.transpose(list(ltrc_keys) + sorted(set(range(l.ndim)) - set(ltrc_keys)))
    R = r.transpose(list(rtrc_keys) + sorted(set(range(r.ndim)) - set(rtrc_keys)))
    ntrc = len(ltrc_keys)
    col_axes,  trc_axes = L.multiaxis.axes[ntrc:], L.multiaxis.axes[:ntrc]
    row_axes, rtrc_axes = R.multiaxis.axes[ntrc:], R.multiaxis.axes[:ntrc]
    T = Array(col_axes + row_axes)
    if not trc_axes == rtrc_axes: raise ValueError("Cannot trace {:s} with {:s}".format(str(trc_axes), str(rtrc_axes)))
    multiaxis_type = type(np.prod(l.multiaxis.axes + r.multiaxis.axes))
    col_multiaxis = multiaxis_type(col_axes)
    trc_multiaxis = multiaxis_type(trc_axes)
    row_multiaxis = multiaxes_type(row_axes)
    transposed_axis_keys = (range(ntrc), range(ntrc))
    for col in col_multiaxis.iter_keytups():
      for row in row_multiaxis.iter_keytups(col_keytup):
        for trc in trc_multiaxis.iter_keytups(col_keytup):
          T[col + row] = tensordot(L[trc + col], R[trc + row], transposed_axis_keys)
  else:
    raise TypeError("Cannot tensordot objects of type(s): {:s} and {:s}".format(type(l).__name__, type(r).__name__))


if __name__ == "__main__":
  import axis as ax
  ia = ax.IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  A = Array(ia*ia)
  B = Array(ia*ia)
  C = Array(ia*ia)
  Cref = Array(ia*ia)

  from symmetry import XOR
  for col in ax.MultiAxis(ia).iter_keytups():
    for row in ax.IrrepMultiAxis(ia).iter_keytups(XOR(col)):
      a = np.random.rand(*A[col+row].shape)
      b = np.random.rand(*B[col+row].shape)
      A[col+row] = a
      B[col+row] = b
      Cref[col+row] = np.dot(a, b)

  for col in ax.MultiAxis(ia).iter_keytups():
    for row in ax.IrrepMultiAxis(ia).iter_keytups(XOR(col)):
      for trc in ax.IrrepMultiAxis(ia).iter_keytups(XOR(col)):
        if not (0 in A[col+trc] or 0 in B[trc+row]):
          C[col+row] += np.dot(A[col+trc], B[trc+row])

  print C
  D = C - Cref
  for blk in D:
    print blk
