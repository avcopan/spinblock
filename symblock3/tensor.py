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
    if array is None:
      self.array = np.empty(multiaxis.shape, multiaxis.dtype)
      for keytup in multiaxis.iter_keytups():
        self.array[keytup] = multiaxis.dtype(tuple(init_arg[key] for init_arg, key in zip(multiaxis.init_args, keytup)))
        if hasattr(multiaxis.dtype, "fill"): self.array[keytup].fill(0)
    elif not isinstance(array, np.ndarray) and array.shape == multiaxis.shape and array.dtype == multiaxis.dtype:
      raise ValueError("Array must be initialized with ndarray object of shape {:s} and dtype {:s}".format(str(multiaxis.shape), type(multiaxis.dtype).__name__))

  def __getitem__(self, *args): return self.array[args[0]]
  def __setitem__(self, *args):        self.array[args[0]] = args[1]

  def __iter__(self): return (self.array[keytup] for keytup in self.multiaxis.iter_keytups())
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
    for keytup in self.multiaxis.iter_keytups(): array[keytup] = transformer(self.array, keytup)
    return array

  def transpose(self, axis_keys = None):
    return Array(self.multiaxis.transpose(axis_keys), self.transform(lambda arr, kt: arr[kt].transpose(axis_keys)).transpose(axis_keys))
  T = property(transpose, None)



if __name__ == "__main__":
  import axis as ax
  ia = ax.IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  print Array(ia*ia*ia)

  a1 = ax.Axis(7, np.ndarray)
  a2 = ax.Axis((4,0,1,2), np.ndarray)
  A = Array((a1, a2))
  print A
  print A[0,0].shape
  B = A.T
  print B
  print B[0,0].shape
  print A
  print A[0,0].shape

  C = 1 + A

  for blk in C:
    print blk

  D = C + C
  for blk in D:
    print blk

  E = -D

  for blk in E:
    print blk

  F = 1 / E

  for blk in F:
    print blk
