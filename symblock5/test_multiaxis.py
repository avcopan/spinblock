from multiaxis import MultiAxis


import pytest

def testV__init__V01():
  import axis as ax
  import numpy as np
  a = ax.Axis((4,0,1,2), np.ndarray)
  ma = MultiAxis((a, a, a))
  assert( ma.axes  == (ax.Axis((4, 0, 1, 2), np.ndarray),)*3    )
  assert( ma.ndim  == 3                                         )
  assert( ma.dtype == np.ndarray                                )
  assert( ma.pgsym == False                                     )
  assert( ma.shape == (4, 4, 4)                                 )
  assert( ma.keys  == ((0, 2, 3), (0, 2, 3), (0, 2, 3))         )
  assert( ma.inits == ((4, 0, 1, 2), (4, 0, 1, 2), (4, 0, 1, 2)))

def testV__init__V02():
  ma = MultiAxis(())
  assert( ma.axes  == ()   )
  assert( ma.ndim  == 0    )
  assert( ma.dtype == None )
  assert( ma.pgsym == False)
  assert( ma.shape == ()   )
  assert( ma.keys  == ()   )
  assert( ma.inits == ()   )

def testV__init__V03():
  import axis as ax
  import numpy as np
  a = ax.IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  ma = MultiAxis((a, a, a))
  assert( ma.axes  == (ax.IrrepAxis("C2v", (4,0,1,2), np.ndarray),)*3 )
  assert( ma.ndim  == 3                                               )
  assert( ma.dtype == np.ndarray                                      )
  assert( ma.pgsym == True                                            )
  assert( ma.shape == (4, 4, 4)                                       )
  assert( ma.keys  == ((0, 2, 3), (0, 2, 3), (0, 2, 3))               )
  assert( ma.inits == ((4, 0, 1, 2), (4, 0, 1, 2), (4, 0, 1, 2))      )

def testV__init__V04():
  import axis as ax
  import numpy as np
  a = ax.Axis((4,0,1,2), np.ndarray)
  b = ax.IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  ma = MultiAxis((a, b, a, b))

  assert( ma.axes  == (ax.Axis((4,0,1,2), np.ndarray), ax.IrrepAxis("C2v", (4,0,1,2), np.ndarray))*2 )
  assert( ma.ndim  == 4                                                                              )
  assert( ma.dtype == np.ndarray                                                                     )
  assert( ma.pgsym == False                                                                          )
  assert( ma.shape == (4, 4, 4, 4)                                                                   )
  assert( ma.keys  == ((0, 2, 3), (0, 2, 3), (0, 2, 3), (0, 2, 3))                                   )
  assert( ma.inits == ((4, 0, 1, 2), (4, 0, 1, 2), (4, 0, 1, 2), (4, 0, 1, 2))                       )

def testV__transpose__V01():
  import axis as ax
  import numpy as np
  a = ax.Axis((3,   ), np.ndarray)
  b = ax.Axis((3,4  ), np.ndarray)
  c = ax.Axis((3,4,5), np.ndarray)
  ma1 = MultiAxis((a, b, c))
  ma2 = ma1.transpose()
  ma3 = ma1.transpose((0,2,1))
  ma4 = ma1.transpose().transpose()

  assert( ma1 == ma4 )

  assert( ma2.axes  == (c, b, a)                 )
  assert( ma2.ndim  == 3                         )
  assert( ma2.dtype == np.ndarray                )
  assert( ma2.pgsym == False                     )
  assert( ma2.shape == (3, 2, 1)                 )
  assert( ma2.keys  == ((0, 1, 2), (0, 1), (0,)) )
  assert( ma2.inits == ((3, 4, 5), (3, 4), (3,)) )

  assert( ma3.axes  == (a, c, b)                 )
  assert( ma3.ndim  == 3                         )
  assert( ma3.dtype == np.ndarray                )
  assert( ma3.pgsym == False                     )
  assert( ma3.shape == (1, 3, 2)                 )
  assert( ma3.keys  == ((0,), (0, 1, 2), (0, 1)) )
  assert( ma3.inits == ((3,), (3, 4, 5), (3, 4)) )

def testV__getitem__V01():
  import axis as ax
  import numpy as np
  a = ax.Axis((4,0,1,2), np.ndarray)
  ma = MultiAxis((a, a))

  assert( ma[0,0] == (4, 4) )
  assert( ma[0,1] == (4, 0) )
  assert( ma[0,2] == (4, 1) )
  assert( ma[0,3] == (4, 2) )
  assert( ma[1,0] == (0, 4) )
  assert( ma[1,1] == (0, 0) )
  assert( ma[1,2] == (0, 1) )
  assert( ma[1,3] == (0, 2) )
  assert( ma[2,0] == (1, 4) )
  assert( ma[2,1] == (1, 0) )
  assert( ma[2,2] == (1, 1) )
  assert( ma[2,3] == (1, 2) )
  assert( ma[3,0] == (2, 4) )
  assert( ma[3,1] == (2, 0) )
  assert( ma[3,2] == (2, 1) )
  assert( ma[3,3] == (2, 2) )

def testV__iter__V01():
  import axis as ax
  import numpy as np
  a = ax.Axis((4,0,1,2), np.ndarray)
  ma = MultiAxis((a, a))
  assert( list(ma.__iter__()) == [(0, 0), (0, 2), (0, 3), (2, 0), (2, 2), (2, 3), (3, 0), (3, 2), (3, 3)] )

def testViter_arrayV01():
  import axis as ax
  import numpy as np
  a = ax.IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  ma = MultiAxis((a, a))
  assert( list(ma.iter_array()) == [(0, 0), (2, 2), (3, 3)] )

def testViter_complementV01():
  import axis as ax
  import numpy as np
  a = ax.IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  ma = MultiAxis((a, a))

  assert( list(ma.iter_complement((0,))) == [(0, 0), (2, 2), (3, 3)] )
  assert( list(ma.iter_complement((1,))) == [(2, 3), (3, 2)]         )
  assert( list(ma.iter_complement((2,))) == [(0, 2), (2, 0)]         )
  assert( list(ma.iter_complement((3,))) == [(0, 3), (3, 0)]         )

def testV__iter__V02():
  ma = MultiAxis(())
  assert( list(ma.__iter__()) == [()] )

def testViter_arrayV02():
  ma = MultiAxis(())
  assert( list(ma.iter_array()) == [()] )

def testViter_complementV02():
  ma = MultiAxis(())
  assert( list(ma.iter_complement('chicken')) == [()] )

