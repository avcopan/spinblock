from multiaxis import MultiAxis

class BlockTensor(object):

  kwtypes = {'keys'    : (lambda arg: hasattr   (arg, "__iter__")),
             'diagonal': (lambda arg: isinstance(arg, bool      ))}

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
    for keytup in self.iter_keytups():
      self.blkmap[keytup] = self.dtype( self.mltx[keytup] )
      if hasattr(self.dtype, "fill"): self.blkmap[keytup].fill(0.0)

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

