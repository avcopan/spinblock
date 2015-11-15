import numpy as np

def broadcast_to(a, newaxes):
  if isinstance(a, np.ndarray):
    return np.broadcast_to(a, newaxes)
  elif hasattr(a, "multiaxis"):
    if not a.multiaxis == np.prod(newaxes[-a.ndim:]):
      raise Exception("Cannot broadcast array with axes\n{:s}\nalong axes\n{:s}".format(str(a.multiaxis), str(np.prod(newaxes[-a.ndim:]))))
    tmp = type(a)(newaxes)
    for keytup in tmp.iter_keytups():
      subaxes = tuple(arg[key] for arg, key in zip(tmp.multiaxis.init_args, keytup))
      tmp.array[keytup] = broadcast_to(a.array[keytup[-a.ndim:]], subaxes)
    return tmp

def broadcast(a, newaxes, axis_keys = None):
  ndim = len(newaxes)
  if axis_keys is None: axis_keys = range(ndim - a.ndim, ndim)
  pmt = tuple(key for key in range(ndim) if not key in axis_keys) + tuple(axis_keys)
  inv, _ = zip(*sorted(enumerate(pmt), key=lambda x:x[1]))
  tmp = broadcast_to(a, tuple(newaxes[key] for key in pmt)).transpose(inv)
  return tmp
