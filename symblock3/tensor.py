import numpy     as np
import printer   as pt
from multiaxis import MultiAxis

class Array(object):

  def __init__(self, multiaxis, array = None):
    if not isinstance(multiaxis, MultiAxis):
      try:    multiaxis = np.prod(multiaxis)
      except: raise ValueError("Array must be initialized with MultiAxis or a tuple of Axis objects")
    self.multiaxis = multiaxis
    self.array     = array
    self.shape     = multiaxis.shape
    self.dtype     = multiaxis.dtype
    if array is None:
      self.array = np.empty(self.shape, self.dtype)
      for keytup in multiaxis.iter_array_keytups():
        self.array[keytup] = self.dtype(tuple(init_arg[key] for init_arg, key in zip(multiaxis.init_args, keytup)))
        if hasattr(self.dtype, "fill"): self.array[keytup].fill(0)
    elif not isinstance(array, np.ndarray) and array.shape == multiaxis.shape and array.dtype == multiaxis.dtype:
      raise ValueError("Array must be initialized with ndarray object of shape {:s} and dtype {:s}".format(str(multiaxis.shape), type(multiaxis.dtype).__name__))

  def __getitem__(self, *args): return self.array[args[0]]
  def __setitem__(self, *args):        self.array[args[0]] = args[1]

  def __iter__(self): return (self.array[keytup] for keytup in self.multiaxis.iter_array_keytups())
  def __str__ (self): return pt.Array2str(self)
  def __pos__ (self): return self
  def __neg__ (self): return Array(self.multiaxis, self.transform(lambda arr, kt: -arr[kt]))

  def __add__ (self, other): return self.elementwise_operation(other, np.ndarray.__add__ )
  def __sub__ (self, other): return self.elementwise_operation(other, np.ndarray.__sub__ )
  def __mul__ (self, other): return self.elementwise_operation(other, np.ndarray.__mul__ )
  def __div__ (self, other): return self.elementwise_operation(other, np.ndarray.__div__ )
  def __radd__(self, other): return self.elementwise_operation(other, np.ndarray.__radd__)
  def __rsub__(self, other): return self.elementwise_operation(other, np.ndarray.__rsub__)
  def __rmul__(self, other): return self.elementwise_operation(other, np.ndarray.__rmul__)
  def __rdiv__(self, other): return self.elementwise_operation(other, np.ndarray.__rdiv__)

  def elementwise_operation(self, other, operation):
    if isinstance(other, Array):
      if other.multiaxis == self.multiaxis:
        array = self.transform(lambda arr, kt: operation(arr[kt], other.array[kt]))
      else: raise TypeError("Cannot {:s} Arrays with inconsistent axes\n{:s}\nand\n{:s}".format(operation.__name__, str(self.multiaxis), str(other.multiaxis)))
    else:
      try:
        array = self.transform(lambda arr, kt: operation(arr[kt], other))
      except: raise ValueError("Cannot {:s} Array and {:s}".format(operation.__name__, type(other).__name__))
    return Array(self.multiaxis, array)

  def transform(self, transformer):
    array = np.empty(self.multiaxis.shape, self.multiaxis.dtype)
    for keytup in self.multiaxis.iter_array_keytups(): array[keytup] = transformer(self.array, keytup)
    return array

  def transpose(self, axis_keys = None):
    return Array(self.multiaxis.transpose(axis_keys), self.transform(lambda arr, kt: arr[kt].transpose(axis_keys)).transpose(axis_keys))
  T = property(transpose, None)

  def dot(self, other, axis_keys = None):
    if not isinstance(other, Array):
      raise TypeError ("dot (matrix muliplication) of Array with {:s} is undefined.".format(type(other).__name__))
    col_multiaxis = np.prod(self.multiaxis.axes[:-1])
    row_multiaxis = np.prod(other.multiaxis.axes[:-2] + other.multiaxis.axes[-2:][1:])
    dot_axis = other.multiaxis.axes[-1] if other.multiaxis.ndim is 1 else other.multiaxis.axes[-2]
    if not self.multiaxis.axes[-1] == dot_axis:
      raise ValueError("dot (matrix multiplication): cannot dot {:s} against {:s}.".format(str(self.multiaxis.axes[-1]), str(dot_axis)))

    


def test1():
  import axis as ax
  import numpy as np
  a = ax.Axis((7,), np.ndarray)
  ia = ax.IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  A = Array(a*a*ia*ia)
  B = Array(ia*ia*a*a)

  a = np.random.rand(7,7,7,7)
  b = np.random.rand(7,7,7,7)
  c = np.tensordot(a, b, axes=((2,3),(0,1)))

  it_a  = zip(range(1),(slice(7),),(slice(7),))
  it_ia = zip(range(4),(slice(4),slice(0),slice(1),slice(2)),(slice(0,4),slice(4,4),slice(4,5),slice(5,7)))

  for h1, i1, j1 in it_a:
    for h2, i2, j2 in it_a:
      for h3, i3, j3 in it_ia:
        for h4, i4, j4 in it_ia:
          A[h1,h2,h3,h4][i1,i2,i3,i4] = a[j1,j2,j3,j4]
          B[h3,h4,h1,h2][i3,i4,i1,i2] = b[j3,j4,j1,j2]

  col_axes = A.multiaxis.axes[:2]
  trc_axes = A.multiaxis.axes[2:]
  row_axes = B.multiaxis.axes[2:]

  C = Array(col_axes + row_axes)

  for col in np.prod(col_axes).iter_array_keytups():
    for row in np.prod(row_axes).iter_array_keytups():
      for trc in MultiAxis(trc_axes).iter_array_keytups():
        if not (0 in A[col+trc].shape or 0 in B[trc+row].shape):
          C[col+row] += np.tensordot(A[col+trc], B[trc+row], axes=((2,3),(0,1)))

  print np.linalg.norm(C[0,0,0,0] - c)



if __name__ == "__main__":
  test1()
