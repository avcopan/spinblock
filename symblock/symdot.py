class SymmetryHelper:

  def __init__(self, product_table):
    self._product_table = product_table

  def evaluate_product(self, irreps):
    product_irrep = 0
    for irrep in irreps: product_irrep = self._product_table[irrep][product_irrep]
    return product_irrep


def water_mp2_script(scfwfn, mints):
  c2v_product_table = [[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]]
  sh = SymmetryHelper(c2v_product_table)
  nirrep = scfwfn.nirrep()
  nsopi  = tuple(scfwfn.nsopi()[h] for h in range(nirrep))
  nso    = scfwfn.nso()
