import psi4
import numpy as np
from blocks import BlockedArray

class Orbital:

  def __init__(self, scfwfn, mints):
    nirrep = scfwfn.nirrep()
    nsopi  = tuple(scfwfn.nsopi()[h] for h in range(nirrep))
    nso    = scfwfn.nso()
    pgU    = BlockedArray((nsopi, nso))
    print nirrep
    print nsopi
    print nso


"""
    nAocc = scfwfn.nalpha()
    nBocc = scfwfn.nbeta()
    nbf  = mints.basisset().nbf()
    Ca = psi4.Matrix(nbf, nbf)
    Cb = psi4.Matrix(nbf, nbf)
    Ca.remove_symmetry(scfwfn.Ca(), mints.petite_list().sotoao())
    Cb.remove_symmetry(scfwfn.Cb(), mints.petite_list().sotoao())
    self.Ca = np.matrix(Ca)
    self.Cb = np.matrix(Cb)

    print self.Ca

    print "symm:"

    M = mints.petite_list().sotoao()
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
