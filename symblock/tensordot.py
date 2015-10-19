from tensor import multi_axis_iter

def tensordot(L, R, axes=([0],[0])):
  sum_L, sum_R = axes
  row_axes = [L._axes[i] for i in range(L._ndim) if not i in sum_L]
  col_axes = [R._axes[i] for i in range(R._ndim) if not i in sum_R]
  sum_axes = [L._axes[i] for i in sum_L]
  print [x for x in  multi_axis_iter(row_axes)]
  print [x for x in  multi_axis_iter(col_axes)]
  print [x for x in  multi_axis_iter(sum_axes)]
