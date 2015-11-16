from axis import Axis, IrrepAxis


import pytest

def testV__init__V01():
  import numpy as np
  ax = Axis((4,0,1,2), np.ndarray)
  assert( ax.nelem      == 4            )
  assert( ax.elem_init  == (4, 0, 1, 2) )
  assert( ax.elem_dtype == np.ndarray   )
  assert( ax.elem_keys  == (0, 2, 3)    )

def testV__eq__V01():
  import numpy as np
  ax1 = Axis((4,0,1,2), np.ndarray)
  ax2 = Axis((4,0,1,2), np.ndarray)
  assert( ax1 == ax2 )

def testV__getitem__V01():
  import numpy as np
  ax = Axis((4,0,1,2), np.ndarray)
  assert( ax[0] == 4 )
  assert( ax[1] == 0 )
  assert( ax[2] == 1 )
  assert( ax[3] == 2 )

def testV__init__V02():
  import numpy as np
  ax = IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  assert( ax.label      == "C2v"        ) 
  assert( ax.nelem      == 4            )
  assert( ax.elem_init  == (4, 0, 1, 2) )
  assert( ax.elem_dtype == np.ndarray   )
  assert( ax.elem_keys  == (0, 2, 3)    )

def testV__init__V03():
  import numpy as np
  with pytest.raises(ValueError) as message:
    ax = IrrepAxis("C2v", (4,1,2), np.ndarray)
  assert str(message).endswith("Can't make C2v IrrepAxis with 3 elements.")

def testV__ne__V01():
  import numpy as np
  ax1 = IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  ax2 = IrrepAxis("C2h", (4,0,1,2), np.ndarray)
  assert( ax1 != ax2 )

def testV__eq__V02():
  import numpy as np
  ax1 = IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  ax2 = IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  assert( ax1 == ax2 )
  
def testV__getitem__V02():
  import numpy as np
  ax = IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  assert( ax[0] == 4 )
  assert( ax[1] == 0 )
  assert( ax[2] == 1 )
  assert( ax[3] == 2 )


