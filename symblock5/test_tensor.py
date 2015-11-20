from tensor import BlockTensor



import pytest

def testV__init__V01():
  import numpy as np
  from multiaxis import MultiAxis
  T = BlockTensor(())
  assert( T.mltx   == MultiAxis(()) )
  assert( T.kwargs == {}            )
  assert( T.ndim   == 0             )
  assert( T.shape  == ()            )
  assert( T.dtype  == np.ndarray    )
  assert( T.blkmap == {(): 0.0}     )

def testV__init__V02():
  import axis as ax
  import numpy as np
  from multiaxis import MultiAxis
  a = ax.Axis((4,0,1,2), np.ndarray)
  T = BlockTensor((a, a))
  blkmap = {(0, 0): np.zeros((4, 4)),
            (0, 2): np.zeros((4, 1)),
            (0, 3): np.zeros((4, 2)),
            (2, 0): np.zeros((1, 4)),
            (2, 2): np.zeros((1, 1)),
            (2, 3): np.zeros((1, 2)),
            (3, 0): np.zeros((2, 4)),
            (3, 2): np.zeros((2, 1)),
            (3, 3): np.zeros((2, 2))}
  assert( T.mltx        == MultiAxis((a, a)) )
  assert( T.kwargs      == {}                )
  assert( T.ndim        == 2                 )
  assert( T.shape       == (4, 4)            )
  assert( T.dtype       == np.ndarray        )
  assert( len(T.blkmap) == len(blkmap)       )
  assert( all((T.blkmap[key] == blk).all() for key, blk in blkmap.iteritems()) )

def testV__init__V03():
  import axis as ax
  import numpy as np
  from multiaxis import MultiAxis
  a = ax.IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  T = BlockTensor((a, a))
  blkmap = {(0, 0): np.zeros((4, 4)),
            (2, 2): np.zeros((1, 1)),
            (3, 3): np.zeros((2, 2))}
  assert( T.mltx        == MultiAxis((a, a)) )
  assert( T.kwargs      == {}                )
  assert( T.ndim        == 2                 )
  assert( T.shape       == (4, 4)            )
  assert( T.dtype       == np.ndarray        )
  assert( len(T.blkmap) == len(blkmap)       )
  assert( all((T.blkmap[key] == blk).all() for key, blk in blkmap.iteritems()) )

def testV__init__V04():
  import axis as ax
  import numpy as np
  from multiaxis import MultiAxis
  a = ax.IrrepAxis("C2v", (4,0,1,2), np.ndarray)
  T = BlockTensor((a,), diagonal=True)
  blkmap = {(0,): np.zeros((4,)),
            (2,): np.zeros((1,)),
            (3,): np.zeros((2,))}
  assert( T.mltx   == MultiAxis((a,))    )
  assert( T.kwargs == {'diagonal': True} )
  assert( T.ndim   == 1                  )
  assert( T.shape  == (4,)               )
  assert( T.dtype  == np.ndarray         )
  assert( len(T.blkmap)   == len(blkmap)       )
  assert( all((T.blkmap[key] == blk).all() for key, blk in blkmap.iteritems()) )

def testV__init__V05():
  import axis as ax
  import numpy as np
  from multiaxis import MultiAxis
  a = ax.Axis((4,0,1,2), np.ndarray)
  T = BlockTensor((a, a), keys=[(0, 0), (0, 3), (3, 0)])
  blkmap = {(0, 0): np.zeros((4, 4)),
            (0, 3): np.zeros((4, 2)),
            (3, 0): np.zeros((2, 4))}
  assert( T.mltx        == MultiAxis((a, a))                  )
  assert( T.kwargs      == {'keys': [(0, 0), (0, 3), (3, 0)]} )
  assert( T.ndim        == 2                                  )
  assert( T.shape       == (4, 4)                             )
  assert( T.dtype       == np.ndarray                         )
  assert( len(T.blkmap) == len(blkmap)                        )
  assert( all((T.blkmap[key] == blk).all() for key, blk in blkmap.iteritems()) )
