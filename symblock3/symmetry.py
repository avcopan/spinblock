def XOR(target_irrep):
  return lambda irreps: reduce(lambda a, b: a^b, irreps) == target_irrep

PG_DIM = {
 'D2h': 8,
 'C2h': 4,
 'C2v': 4,
 'D2' : 4,
 'Cs' : 2,
 'Ci' : 2,
 'C2' : 2,
 'C1' : 1
}

