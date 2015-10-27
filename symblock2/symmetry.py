def XOR(target_irrep):
  return lambda irreps: reduce(lambda a, b: a^b, irreps) == target_irrep

IRREPS = {
        #  'Ag'  'B1g'  'B2g'  'B3g'   'Au'  'B1u'  'B2u'  'B3u'
 'D2h': (0b000, 0b001, 0b010, 0b011, 0b100, 0b101, 0b110, 0b111),
        #  'Ag'   'Bg'   'Au'   'Bu'
 'C2h': ( 0b00,  0b01,  0b10,  0b11                            ),
        #  'A1'   'A2'   'B1'   'B2'
 'C2v': ( 0b00,  0b01,  0b10,  0b11                            ),
        #   'A'   'B1'   'B2'   'B3'
 'D2' : ( 0b00,  0b01,  0b10,  0b11                            ),
        #  'Ap'  'App'
 'Cs' : (  0b0,   0b1                                          ),
        #  'Ag'   'Au'
 'Ci' : (  0b0,   0b1                                          ),
        #   'A'    'B'
 'C2' : (  0b0,   0b1                                          ),
        #   'A'
 'C1' : (  0b0                                                 )
}

if __name__ == "__main__":
  irreps = (1,1,1,3)
  prod_irrep = reduce(lambda a, b: a^b, irreps)
  print prod_irrep
  print XOR(prod_irrep^1)(irreps)
