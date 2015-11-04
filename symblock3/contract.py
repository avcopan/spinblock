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
    T = tn.Array(col_axes + row_axes)
    if not trc_axes == rtrc_axes: raise ValueError("Cannot trace {:s} with {:s}".format(str(trc_axes), str(rtrc_axes)))
    multiaxis_type = type(np.prod(l.multiaxis.axes + r.multiaxis.axes))
    print multiaxis_type
    col_multiaxis = multiaxis_type(col_axes)
    trc_multiaxis = multiaxis_type(trc_axes)
    row_multiaxis = multiaxis_type(row_axes)
    transposed_axis_keys = (range(ntrc), range(ntrc))
    for col in col_multiaxis.iter_keytups():
      for row in row_multiaxis.iter_keytups_against(col):
        for trc in trc_multiaxis.iter_keytups_against(col):
          if T.has_data(col+row) and L.has_data(trc+col) and R.has_data(trc+row):
            T[col + row] += tensordot(L[trc + col], R[trc + row], transposed_axis_keys)
    return T
  else:
    raise TypeError("Cannot tensordot objects of type(s): {:s} and {:s}".format(type(l).__name__, type(r).__name__))



def test1():
  import axis as ax
  ia = ax.IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  A = tn.Array(ia*ia)
  B = tn.Array(ia*ia)
  C = tn.Array(ia*ia)
  Cref = tn.Array(ia*ia)

  from symmetry import XOR
  for col in ax.MultiAxis(ia).iter_keytups():
    for row in ax.IrrepMultiAxis(ia).iter_keytups_against(col):
      a = np.random.rand(*A[col+row].shape)
      b = np.random.rand(*B[col+row].shape)
      A[col+row] = a
      B[col+row] = b
      Cref[col+row] = np.dot(a, b)

  C = tensordot(A, B, axis_keys=((1,),(0,)))

  for blk in Cref:
    print blk

  for blk in C:
    print blk

  print C
  D = C - Cref
  for blk in D:
    print blk

def test2():
  import axis as ax
  import numpy as np
  a = ax.Axis((4,0,1,2), np.ndarray)
  L = tn.Array(a*a)
  R = tn.Array(a*a)
  Tref = tn.Array(a*a)

  l = np.random.rand(7,7)
  r = np.random.rand(7,7)
  t = np.dot(l, r)

  it = zip(range(4),(slice(4),slice(0),slice(1),slice(2)),(slice(0,4),slice(4,4),slice(4,5),slice(5,7)))

  for h1, i1, j1 in it:
    for h2, i2, j2 in it:
      L[h1,h2][i1,i2] = l[j1,j2]
      R[h1,h2][i1,i2] = r[j1,j2]
      Tref[h1,h2][i1,i2] = t[j1,j2]

  T = tensordot(L, R, axis_keys=((1,),(0,)))
  S = T - Tref
  for blk in S:
    print blk

def test3():
  import axis as ax
  ia = ax.IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  a  = ax.Axis(7, np.ndarray)
  L = tn.Array(ia*a)
  R = tn.Array(a*ia)
  Tref = tn.Array(ia*ia)

  l = np.random.rand(7,7)
  r = np.random.rand(7,7)
  t = np.dot(l, r)

  it = zip(range(1), (slice(7),), (slice(7),))
  iit = zip(range(4),(slice(4),slice(0),slice(1),slice(2)),(slice(0,4),slice(4,4),slice(4,5),slice(5,7)))

  for h1, i1, j1 in iit:
    Tref[h1,h1][i1,i1] = t[j1,j1]
    for h2, i2, j2 in it:
      L[h1,h2][i1,i2] = l[j1,j2]
      R[h2,h1][i2,i1] = r[j2,j1]

  T = tensordot(L, R, axis_keys=((1,),(0,)))
  print Tref
  print T

  E = T - Tref
  for blk in E:
    print blk


if __name__ == "__main__":
  test3()
