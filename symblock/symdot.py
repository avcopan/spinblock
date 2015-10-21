
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
  print nirrep
  print nsopi
  print nso
