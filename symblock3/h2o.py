def water_mp2_script(scfwfn, mints):
  nirrep = scfwfn.nirrep()
  nsopi  = tuple(scfwfn.nsopi()[h] for h in range(nirrep))
  nso    = scfwfn.nso()


  import psi4
  import numpy as np
  import axis as ax
  import tensor as tn
  pg_c1  = ax.Axis(nso, np.ndarray)
  pg_c2v = ax.IrrepAxis("C2v", nsopi, np.ndarray)

  U00 = tn.Array((pg_c2v, pg_c1))
  smtrzr = mints.petite_list().sotoao()
  for h in range(nirrep):
    for i in range(smtrzr.rows(h)):
      for j in range(smtrzr.cols(h)):
        U00[h,0][i,j] = smtrzr.get(h, i, j)

  sp_c1  = ax.SpinAxis("U", (pg_c1, pg_c1)  , tn.Array)
  sp_c2v = ax.SpinAxis("U", (pg_c2v, pg_c2v), tn.Array)
  U = tn.Array((sp_c2v, sp_c1))
  for keytup in U.multiaxis.iter_array_keytups():
    U[keytup] = U00

  Ca = scfwfn.Ca()
  Cb = scfwfn.Cb()
  C = tn.Array((sp_c2v, sp_c2v))
  for h in range(nirrep):
    for i in range(Ca.rows(h)):
      for j in range(Ca.cols(h)):
        C[0,0][h,h][i,j] = Ca.get(h, i, j)
        C[1,1][h,h][i,j] = Cb.get(h, i, j)

  Ca_ref = psi4.Matrix(nso, nso)
  Cb_ref = psi4.Matrix(nso, nso)
  Ca_ref.remove_symmetry(Ca, smtrzr)
  Cb_ref.remove_symmetry(Cb, smtrzr)
  C_c1_ref = tn.Array((sp_c1, sp_c1))
  for i in range(7):
    for j in range(7):
      C_c1_ref[0,0][0,0][i,j] = Ca_ref.get(i,j)
      C_c1_ref[1,1][0,0][i,j] = Cb_ref.get(i,j)

  Cref = U % C_c1_ref % U.T
  D = Cref - C

  G = np.empty((1,1,1,1), dtype=np.ndarray)
  G[0,0,0,0] = np.array(mints.ao_eri())
  g_c1 = tn.Array((sp_c1, sp_c1, sp_c1, sp_c1))
  for w1,w2,w3,w4 in g_c1.multiaxis.iter_array_keytups():
    if w1==w2 and w3==w4:
      g_c1[w1,w2,w3,w4] = tn.Array(g_c1[w1,w2,w3,w4].multiaxis, G)


  g_c2v = U % (U % g_c1 % U.T).transpose((1,0,3,2)) % U.T
