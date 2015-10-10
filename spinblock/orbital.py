import psi4
import numpy as np
from blocks import BlockedArray

class Orbital:

  def __init__(self, scfwfn, mints):
    nirrep = scfwfn.nirrep()
    nsopi  = tuple(scfwfn.nsopi()[h] for h in range(nirrep))
    nso    = scfwfn.nso()
    pgU    = BlockedArray((nsopi, nso))
    sotoao = mints.petite_list().sotoao()
    for h in range(nirrep):
      for i in range(sotoao.rows(h)):
        for j in range(sotoao.cols(h)):
          offset = pgU.get_axis(0).get_block_start(h)
          pgU[i+offset,j] = sotoao.get(h, i, j)
    print pgU

    fock_alpha = scfwfn.Fa()
    Fa = BlockedArray((nsopi, nsopi))
    for h in range(nirrep):
      for i in range(fock_alpha.rows(h)):
        for j in range(fock_alpha.cols(h)):
          row_offset = Fa.get_axis(0).get_block_start(h)
          col_offset = Fa.get_axis(1).get_block_start(h)
          Fa[i+row_offset, j+col_offset] = fock_alpha.get(h, i, j)
    print Fa


"""
    nAocc = scfwfn.nalpha()
    nBocc = scfwfn.nbeta()
    nbf  = mints.basisset().nbf()
    Ca = psi4.Matrix(nbf, nbf)
    Cb = psi4.Matrix(nbf, nbf)
    Ca.remove_symmetry(scfwfn.Ca(), mints.petite_list().aotoso())
    Cb.remove_symmetry(scfwfn.Cb(), mints.petite_list().aotoso())
    self.Ca = np.matrix(Ca)
    self.Cb = np.matrix(Cb)

    print self.Ca

    print "symm:"

    M = mints.petite_list().aotoso()
    irreps = []
    for h in range(4):
      rows = M.rows(h)
      cols = M.cols(h)
      U = np.zeros((rows, cols)).view(np.matrix)
      for i in range(rows):
        for j in range(cols):
          U[i,j] = M.get(h, i, j)
      irreps.append(U)

    for h in range(4):
      for i in range(scfwfn.Ca().rows(h)):
        for j in range(scfwfn.Ca().cols(h)):
          print("{:15.7f}".format(scfwfn.Ca().get(h,i,j))),
        print
    for h in range(4):
      print irreps[h]*self.Ca*irreps[h].T

    

"""
