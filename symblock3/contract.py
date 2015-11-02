import numpy  as np
import tensor as tn

def tensordot(a, b, axis_keys=((0,),(0,))):
  if isinstance(a, np.ndarray) and isinstance(b, np.ndarray):
    return np.tensordot(a, b, axes=axis_keys)
  elif isinstance(a, tn.Array) and isinstance(b, tn.Array):
    multiaxis_type = type(np.prod(a.multiaxis.axes + b.multiaxis.axes))
  else:
    raise TypeError("Cannot tensordot objects of type(s): {:s} and {:s}".format(type(a).__name__, type(b).__name__))


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
