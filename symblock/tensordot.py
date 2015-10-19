from tensor import TiledTensor
from tensor import multi_axis_iter

def tensordot(L, R, axis_keys=([0],[0])):
  sum_axis_keys_L, sum_axis_keys_R = axis_keys
  row_axis_keys = [axis_key for axis_key in L.iter_axis_keys() if not axis_key in sum_axis_keys_L]
  col_axis_keys = [axis_key for axis_key in R.iter_axis_keys() if not axis_key in sum_axis_keys_R]
  row_axes      = [L.get_axis(axis_key) for axis_key in row_axis_keys  ]
  col_axes      = [R.get_axis(axis_key) for axis_key in col_axis_keys  ]
  sum_axes      = [L.get_axis(axis_key) for axis_key in sum_axis_keys_L]
  T = TiledTensor(row_axes + col_axes)
  L = L.transpose(sum_axis_keys_L + row_axis_keys)
  R = R.transpose(sum_axis_keys_R + col_axis_keys)
  nsum_axes = len(sum_axis_keys_L)
  axis_keys_arg = (range(nsum_axes), range(nsum_axes))
  null = tuple(0 for _ in range(nsum_axes))
  for row in multi_axis_iter(row_axes):
    for col in multi_axis_iter(col_axes):
      T[row + col]    = tile.tensordot(L[null + row], R[null + col], axis_keys=axis_keys_arg)
    for smm in multi_axis_iter(sum_axes):
      for col in multi_axis_iter(col_axes):
        T[row + col] += tile.tensordot(L[smm + row], R[smm + col], axis_keys=axis_keys_arg)

