import numpy as np

def broadcast_to(a, newaxes):
  if isinstance(a, np.ndarray):
    return np.broadcast_to(a, newaxes)
  elif hasattr(a, "multiaxis"):
    if not a.multiaxis == np.prod(newaxes[a.ndim:]):
      raise Exception("BAAAD")
    tmp = type(a)(newaxes)
    for keytup in tmp.iter_keytups():
      subaxes = tuple(arg[key] for arg, key in zip(tmp.multiaxis.init_args, keytup))
      tmp.array[keytup] = broadcast_to(a.array[keytup[a.ndim:]], subaxes)
    return tmp

def broadcast(a, newaxes, axis_keys = None):
  newndim = len(newaxes)
  if axis_keys is None: axis_keys = range(newndim - a.ndim, newndim)
  tmp = type(a)(newaxes)
  pmt, _ = zip(*sorted(enumerate(axis_keys), key=lambda x:x[1]))

def broadcast(a, newaxes, axis_keys = None):
  if axis_keys is None: axis_keys = range(a.ndim)
  pmt, _ = zip(*sorted(enumerate(axis_keys), key=lambda x:x[1]))
  A = a.transpose(pmt)
  if isinstance(a, np.ndarray):
    shape = newaxes
    slc = tuple(slice(None) if key in axis_keys else np.newaxis for key in range(len(shape)))
    return np.broadcast_to(A[slc], shape)
