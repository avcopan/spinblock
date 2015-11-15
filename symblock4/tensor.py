import numpy     as np
import printer   as pt
from multiaxis import MultiAxis
from contract  import tensordot

class MultiMap(object):

  def __init__(self, multiaxis, array = None, **kwargs):
    if not isinstance(multiaxis, MultiAxis):
      if hasattr(multiaxis, "__len__") and multiaxis.__len__() is 0: multiaxis = MultiAxis(())
      else:
        try:    multiaxis = np.prod(multiaxis)
        except: raise ValueError("Array must be initialized with MultiAxis or a tuple of Axis objects")
    self.multiaxis = multiaxis
    self.kwargs    = kwargs
    self.array     = array
    self.ndim      = multiaxis.ndim
    self.shape     = multiaxis.shape
    self.dtype     = multiaxis.dtype
    if array is None: self.array = np.empty(self.shape, self.dtype)
    elif not (isinstance(array, np.ndarray) and array.shape == self.shape and array.dtype == self.dtype):
      raise ValueError("Array must be initialized with ndarray object of shape {:s} and dtype {:s}".format(str(self.shape), type(self.dtype).__name__))

  def iter_keytups(self):
    for keytup in self.multiaxis.iter_array_keytups():
      if self.has_data_at(keytup):
        yield keytup

  def has_data_at(self, keytup): return not self.array[keytup] is None and not 0 in self.array[keytup].shape
  def put_data_at(self, keytup):
    if hasattr(self.dtype, "fill"):
      self.array[keytup] = self.dtype(tuple(arg[key] for arg, key in zip(self.multiaxis.init_args, keytup)))
      self.array[keytup].fill(0)
    else:
      self.array[keytup] = self.dtype(tuple(arg[key] for arg, key in zip(self.multiaxis.init_args, keytup)), **self.kwargs)

  def __getitem__(self, *args): return self.array[args[0]]
  def __setitem__(self, *args):
    if not self.has_data_at(args[0]): self.put_data_at(args[0])
    self.array[args[0]] = args[1]

  def __iter__(self): return (self.array[keytup] for keytup in self.iter_keytups())
  def __str__ (self): return pt.Array2str(self)
  def __repr__(self): return pt.Array2str(self)
  def __pos__ (self): return self
  def __neg__ (self):
    tmp = self.__new__(type(self))
    tmp.__init__(self.multiaxis, self.transform(lambda arr, kt: -arr[kt]), **self.kwargs)
    return tmp

  def __add__ (self, other): return self.elementwise_operation(other, "__add__" )
  def __sub__ (self, other): return self.elementwise_operation(other, "__sub__" )
  def __mul__ (self, other): return self.elementwise_operation(other, "__mul__" )
  def __div__ (self, other): return self.elementwise_operation(other, "__div__" )
  def __radd__(self, other): return self.elementwise_operation(other, "__radd__")
  def __rsub__(self, other): return self.elementwise_operation(other, "__rsub__")
  def __rmul__(self, other): return self.elementwise_operation(other, "__rmul__")
  def __rdiv__(self, other): return self.elementwise_operation(other, "__rdiv__")

  def elementwise_operation(self, other, operation):
    if hasattr(other, "multiaxis"):
      if other.multiaxis == self.multiaxis:
        array = self.transform(lambda arr, kt: getattr(arr[kt], operation)(other.array[kt]))
      else: raise TypeError("Cannot {:s} Arrays with inconsistent axes\n{:s}\nand\n{:s}".format(operation, str(self.multiaxis), str(other.multiaxis)))
    else:
      try:
        array = self.transform(lambda arr, kt: getattr(arr[kt], operation)(other))
      except: raise ValueError("Cannot {:s} Array and {:s}".format(operation, type(other).__name__))
    tmp = self.__new__(type(self))
    tmp.__init__(self.multiaxis, array, **self.kwargs)
    return tmp

  def transform(self, transformer):
    array = np.empty(self.multiaxis.shape, self.multiaxis.dtype)
    for keytup in self.iter_keytups():
      if self.has_data_at(keytup):
        array[keytup] = transformer(self.array, keytup)
    return array

class Array(MultiMap):

  def __init__(self, multiaxis, array = None, **kwargs):
    MultiMap.__init__(self, multiaxis, array, **kwargs)
    if array is None:
      for keytup in self.iter_keytups():
        self.put_data_at(keytup)

  def iter_keytups(self):
    if 'diagonal' in self.kwargs and self.kwargs['diagonal'] is True: return self.multiaxis.iter_keytups()
    else: return self.multiaxis.iter_array_keytups()

  def has_data_at(self, keytup): return not self.array[keytup] is None and not 0 in self.array[keytup].shape

  def __getitem__(self, *args): return self.array[args[0]]
  def __setitem__(self, *args):        self.array[args[0]] = args[1]

  def __mod__ (self, other): return tensordot(self, other)
  def __rmod__(self, other): return tensordot(other, self)

  def transform(self, transformer):
    array = np.empty(self.multiaxis.shape, self.multiaxis.dtype)
    for keytup in self.iter_keytups():
      array[keytup] = transformer(self.array, keytup)
    return array

  def transpose(self, axis_keys = None):
    return Array(self.multiaxis.transpose(axis_keys), self.transform(lambda arr, kt: arr[kt].transpose(axis_keys)).transpose(axis_keys))
  T = property(transpose, None)


if __name__ == "__main__":
  import axis as ax
  import broadcast as bd
  a = ax.IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  A = Array((a,), None, diagonal=True)
  B = bd.broadcast(A, (a,a), axis_keys=(0,))
  print B.multiaxis
  B += 1
  for blk in B:
    print blk
