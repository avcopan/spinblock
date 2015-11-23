from multiaxis import MultiAxis
import numpy as np
import printer

class BlockTensor(object):

  kwtypes = {'keys'    : (lambda arg: hasattr   (arg, "__iter__")),
             'diagonal': (lambda arg: isinstance(arg, bool      ))}

  kwrecursive = ['diagonal']

  def __init__(self, axes, blkmap = None, **kwargs):
    self.mltx   = MultiAxis(axes)
    self.kwargs = kwargs
    self.check_kwargs()
    self.blkmap = blkmap if not blkmap is None else dict()
    self.ndim   = self.mltx.ndim
    self.shape  = self.mltx.shape
    self.dtype  = self.mltx.dtype
    if blkmap is None: self.init_blocks()

  def iter_keytups(self):
    if   'keys'     in self.kwargs: return self.kwargs['keys']
    elif 'diagonal' in self.kwargs: return self.mltx.__iter__()
    else:                           return self.mltx.iter_array()

  def init_blocks(self):
    if self.dtype is BlockTensor:
      kwargs = {kw: self.kwargs[kw] for kw in self.kwrecursive if kw in self.kwargs}
      for keytup in self.iter_keytups():
        self.blkmap[keytup] = self.dtype( self.mltx[keytup], **kwargs )
    elif issubclass(self.dtype, np.ndarray):
      for keytup in self.iter_keytups():
        self.blkmap[keytup] = self.dtype( self.mltx[keytup] )
        self.blkmap[keytup].fill(0.0)
    else:
      raise ValueError('{:s} is an invalid dtype for BlockTensor'.format(self.dtype))

  def __call__(self, *keytup):
    try:    return self.blkmap.__getitem__(*keytup)
    except: return self.blkmap.__getitem__( keytup)

  def __str__(self): return printer.BlockTensor2str(self)

  def check_kwargs(self):
    for key, arg in self.kwargs.iteritems():
      if not key in self.kwtypes   : raise ValueError("Invalid kwarg '{:s}' passed to BlockedTensor.".format(key))
      if not self.kwtypes[key](arg): raise ValueError("BlockedTensor kwarg '{:s}' has incorrect type '{:s}'.".format(key, type(arg).__name__))
    


if __name__ == "__main__":
  import test_tensor as tst
  tst.testV__init__V01()
  tst.testV__init__V02()
  tst.testV__init__V03()
  tst.testV__init__V04()
  tst.testV__init__V05()
  tst.testV__init__V06()
  tst.testV__init__V07()
