import psi4
import numpy as np

class Orbital:

  def __init__(self, scfwfn, mints):
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
    print self.Cb

