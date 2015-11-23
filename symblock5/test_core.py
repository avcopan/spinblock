from tensor import BlockTensor



import pytest

def testV__init__V01():
  import numpy as np
  from multiaxis import MultiAxis
  T = BlockTensor(())
  print T
  print T()
  assert( T.mltx   == MultiAxis(()) )
  assert( T.kwargs == {}            )
  assert( T.ndim   == 0             )
  assert( T.shape  == ()            )
  assert( T.dtype  == np.ndarray    )
  assert( T.blkmap == {(): 0.0}     )

def testV__init__V02():
  import axis as ax
  import numpy as np
  from core      import corearray
  from multiaxis import MultiAxis
  a = ax.Axis((4,0,1,2), corearray )
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
  assert( T.mltx             == MultiAxis((a, a))                              )
  assert( T.kwargs           == {}                                             )
  assert( T.ndim             == 2                                              )
  assert( T.shape            == (4, 4)                                         )
  assert( T.dtype            == corearray                                      )
  assert( len(T.blkmap)      == len(blkmap)                                    )
  assert( all((T.blkmap[key] == blk).all() for key, blk in blkmap.iteritems()) )

def testV__init__V03():
  import axis as ax
  import numpy as np
  from core      import corearray
  from multiaxis import MultiAxis
  a = ax.IrrepAxis("C2v", (4,0,1,2), corearray )
  T = BlockTensor((a, a))
  blkmap = {(0, 0): np.zeros((4, 4)),
            (2, 2): np.zeros((1, 1)),
            (3, 3): np.zeros((2, 2))}
  assert( T.mltx             == MultiAxis((a, a))                              )
  assert( T.kwargs           == {}                                             )
  assert( T.ndim             == 2                                              )
  assert( T.shape            == (4, 4)                                         )
  assert( T.dtype            == corearray                                      )
  assert( len(T.blkmap)      == len(blkmap)                                    )
  assert( all((T.blkmap[key] == blk).all() for key, blk in blkmap.iteritems()) )

def testV__init__V04():
  import axis as ax
  import numpy as np
  from core      import corearray
  from multiaxis import MultiAxis
  a = ax.IrrepAxis("C2v", (4,0,1,2), corearray )
  T = BlockTensor((a,), diagonal=True)
  blkmap = {(0,): np.zeros((4,)),
            (2,): np.zeros((1,)),
            (3,): np.zeros((2,))}
  assert( T.mltx             == MultiAxis((a,))                                )
  assert( T.kwargs           == {'diagonal': True}                             )
  assert( T.ndim             == 1                                              )
  assert( T.shape            == (4,)                                           )
  assert( T.dtype            == corearray                                      )
  assert( len(T.blkmap)      == len(blkmap)                                    )
  assert( all((T.blkmap[key] == blk).all() for key, blk in blkmap.iteritems()) )

def testV__init__V05():
  import axis as ax
  import numpy as np
  from core      import corearray
  from multiaxis import MultiAxis
  a = ax.Axis((4,0,1,2), corearray )
  T = BlockTensor((a, a), keys=[(0, 0), (0, 3), (3, 0)])
  blkmap = {(0, 0): np.zeros((4, 4)),
            (0, 3): np.zeros((4, 2)),
            (3, 0): np.zeros((2, 4))}
  assert( T.mltx             == MultiAxis((a, a))                              )
  assert( T.kwargs           == {'keys': [(0, 0), (0, 3), (3, 0)]}             )
  assert( T.ndim             == 2                                              )
  assert( T.shape            == (4, 4)                                         )
  assert( T.dtype            == corearray                                      )
  assert( len(T.blkmap)      == len(blkmap)                                    )
  assert( all((T.blkmap[key] == blk).all() for key, blk in blkmap.iteritems()) )


def testV__init__V06():
  import axis as ax
  import numpy as np
  from core      import corearray
  from multiaxis import MultiAxis
  pg = ax.IrrepAxis("C2v", (4,0,1,2), corearray )
  sp = ax.Axis((pg, pg), BlockTensor)
  T = BlockTensor((sp, sp), keys=[(0, 0), (1, 1)])
  print T
  print T(0,0)
  print T(1,1)
  blkmap = {(0, 0): np.zeros((4, 4)),
            (2, 2): np.zeros((1, 1)),
            (3, 3): np.zeros((2, 2))}
  assert( T.mltx             == MultiAxis((sp, sp))                            )
  assert( T.kwargs           == {'keys': [(0, 0), (1, 1)]}                     )
  assert( T.ndim             == 2                                              )
  assert( T.shape            == (2, 2)                                         )
  assert( T.dtype            == BlockTensor                                    )
  assert( len(T.blkmap)      == 2                                              )
  assert( T(0,0).mltx        == MultiAxis((pg, pg))                            )
  assert( T(0,0).kwargs      == {}                                             )
  assert( T(0,0).ndim        == 2                                              )
  assert( T(0,0).shape       == (4, 4)                                         ) 
  assert( T(0,0).dtype       == corearray                                      )
  assert( T(1,1).mltx        == MultiAxis((pg, pg))                            )
  assert( T(1,1).kwargs      == {}                                             )
  assert( T(1,1).ndim        == 2                                              )
  assert( T(1,1).shape       == (4, 4)                                         )
  assert( T(1,1).dtype       == corearray                                      )
  assert( len(T(0,0).blkmap) == len(blkmap)                                    )
  assert( len(T(1,1).blkmap) == len(blkmap)                                    )
  assert( all((T(0,0)(key)   == blk).all() for key, blk in blkmap.iteritems()) )
  assert( all((T(1,1)(key)   == blk).all() for key, blk in blkmap.iteritems()) )


def testV__init__V07():
  import axis as ax
  import numpy as np
  from core      import corearray
  from multiaxis import MultiAxis
  pg = ax.IrrepAxis("C2v", (4,0,1,2), corearray )
  sp = ax.Axis((pg, pg), BlockTensor)
  T = BlockTensor(sp, diagonal=True)
  print T
  print T(0)
  print T(1)
  blkmap = {(0,): np.zeros((4,)),
            (2,): np.zeros((1,)),
            (3,): np.zeros((2,))}
  assert( T.mltx           == MultiAxis(sp)                                  )
  assert( T.kwargs         == {'diagonal': True}                             )
  assert( T.ndim           == 1                                              )
  assert( T.shape          == (2,)                                           )
  assert( T.dtype          == BlockTensor                                    )
  assert( len(T.blkmap)    == 2                                              )
  assert( T(0).mltx        == MultiAxis(pg)                                  )
  assert( T(0).kwargs      == {'diagonal': True}                             )
  assert( T(0).ndim        == 1                                              )
  assert( T(0).shape       == (4,)                                           )
  assert( T(0).dtype       == corearray                                      )
  assert( T(1).mltx        == MultiAxis(pg)                                  )
  assert( T(1).kwargs      == {'diagonal': True}                             )
  assert( T(1).ndim        == 1                                              )
  assert( T(1).shape       == (4,)                                           )
  assert( T(1).dtype       == corearray                                      ) 
  assert( len(T(0).blkmap) == len(blkmap)                                    )
  assert( len(T(1).blkmap) == len(blkmap)                                    )
  assert( all((T(0)(key)   == blk).all() for key, blk in blkmap.iteritems()) )
  assert( all((T(1)(key)   == blk).all() for key, blk in blkmap.iteritems()) )
