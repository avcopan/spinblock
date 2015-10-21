
BINARY_IRREPS = {
#                         E,C2x,C2y,C2z, i, sx,sy,sz
 'D2h': [0b000,  # 'Ag' , 1,  1,  1,  1, 1,  1, 1, 1
         0b001,  # 'B1g', 1, -1, -1,  1, 1, -1,-1, 1
         0b010,  # 'B2g', 1, -1,  1, -1, 1, -1, 1,-1
         0b011,  # 'B3g', 1,  1, -1, -1, 1,  1,-1,-1
         0b100,  # 'Au' , 1,  1,  1,  1,-1, -1,-1,-1
         0b101,  # 'B1u', 1, -1, -1,  1,-1,  1, 1,-1
         0b110,  # 'B2u', 1, -1,  1, -1,-1,  1,-1, 1
         0b111 ],# 'B3u', 1,  1, -1, -1,-1, -1, 1, 1
#                         E,C2, i,sh
 'C2h': [ 0b00,  # 'Ag' , 1, 1, 1, 1
          0b01,  # 'Bg' , 1,-1, 1,-1
          0b10,  # 'Au' , 1, 1,-1,-1
          0b11 ],# 'Bu' , 1,-1,-1, 1
#                         E,C2,sx,sy
 'C2v': [ 0b00,  # 'A1' , 1, 1, 1, 1
          0b01,  # 'A2' , 1, 1,-1,-1
          0b10,  # 'B1' , 1,-1,-1, 1
          0b11 ],# 'B2' , 1,-1, 1,-1
#                         E,C2x,C2y,C2z
 'D2' : [ 0b00,  # 'A'  , 1,  1,  1,  1
          0b01,  # 'B1' , 1, -1, -1,  1
          0b10,  # 'B2' , 1, -1,  1, -1
          0b11 ],# 'B3' , 1,  1, -1, -1
#                        E,sh
 'Cs' : [  0b0,  # 'Ap' ,1, 1
           0b1 ],# 'App',1,-1
#                         E, i
 'Ci' : [  0b0,  # 'Ag' , 1, 1
           0b1 ],# 'Au' , 1,-1
#                         E,C2
 'C2' : [  0b0,  # 'A'  , 1, 1
           0b1 ],# 'B'  , 1,-1
#                         E
 'C1' : [  0b0 ] # 'A'  , 1
}



class SymmetryHelper:

  def __init__(self, binary_irreps, irrep_lookup):
    self._binary_irreps = binary_irreps
    self._irrep_lookup  = irrep_lookup

  def evaluate_product(self, element_list):
    return reduce(lambda i, j: self._irrep_lookup[i] ^ self._irrep_lookup[j], element_list)

def water_mp2_script(scfwfn, mints):
  sh = SymmetryHelper(BINARY_IRREPS["C2v"], [0, 1, 2, 3])
  nirrep = scfwfn.nirrep()
  nsopi  = tuple(scfwfn.nsopi()[h] for h in range(nirrep))
  nso    = scfwfn.nso()

  import axis as ax
  c1_axis  = ax.PartitionedAxis(nso)
  c2v_axis = ax.PartitionedAxis(nsopi)

  symmetrizer = mints.petite_list().sotoao()

  import tensor as tn
  U = tn.TiledTensor((c2v_axis, c1_axis))
  for h in range(nirrep):
    for i in range(symmetrizer.rows(h)):
      for j in range(symmetrizer.cols(h)):
        offset = c2v_axis.get_partition_start(h)
        U[i+offset, j] = symmetrizer.get(h, i, j)

  import numpy as np
  c2v_g = tn.TiledTensor((c2v_axis, c2v_axis, c2v_axis, c2v_axis))
  c1_g  = tn.TiledTensor(( c1_axis,  c1_axis,  c1_axis,  c1_axis))
  c1_g[0:7,0:7,0:7,0:7] = np.array(mints.ao_eri())
  g1    = tn.tensordot(U, c1_g, axis_keys=([1],[3]))
  print g1.get_axis(0)
  print g1.get_axis(1)
  print g1.get_axis(2)
  print g1.get_axis(3)
  g2    = tn.tensordot(U,   g1, axis_keys=([1],[3]))
  g1    = tn.tensordot(U,   g2, axis_keys=([1],[3]))
  c2v_g = tn.tensordot(U,   g1, axis_keys=([1],[3]))
