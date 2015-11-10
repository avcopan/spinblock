def water_mp2_script(scfwfn, mints):
  nirrep   = scfwfn.nirrep()
  nso      = scfwfn.nso()
  nsopi    = tuple(scfwfn.nsopi()   [h] for h in range(nirrep))
  naoccpi  = tuple(scfwfn.nalphapi()[h] for h in range(nirrep))
  nboccpi  = tuple(scfwfn.nbetapi() [h] for h in range(nirrep))
  navirpi  = tuple(tot - occ for tot, occ in zip(nsopi, naoccpi))
  nbvirpi  = tuple(tot - occ for tot, occ in zip(nsopi, nboccpi))


  import psi4
  import numpy as np
  import axis as ax
  import tensor as tn
  pg_c1  = ax.Axis(nso, np.ndarray)
  pg_c2v = ax.IrrepAxis("C2v", nsopi, np.ndarray);  print pg_c2v
  aocc_c2v = ax.IrrepAxis("C2v", naoccpi, np.ndarray);  print aocc_c2v
  bocc_c2v = ax.IrrepAxis("C2v", nboccpi, np.ndarray);  print bocc_c2v
  avir_c2v = ax.IrrepAxis("C2v", navirpi, np.ndarray);  print avir_c2v
  bvir_c2v = ax.IrrepAxis("C2v", nbvirpi, np.ndarray);  print bvir_c2v

  occ_c2v = ax.SpinAxis("U", (aocc_c2v, bocc_c2v), tn.Array)
  vir_c2v = ax.SpinAxis("U", (avir_c2v, bvir_c2v), tn.Array)

  print occ_c2v
  print vir_c2v

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
  oC = tn.Array((sp_c2v, occ_c2v))
  vC = tn.Array((sp_c2v, vir_c2v))
  for h in range(nirrep):
    for mu in range(Ca.rows(h)):
      for i in range(naoccpi[h]):
        oC[0,0][h,h][mu,i] = Ca.get(h, mu, i)
      for a in range(navirpi[h]):
        vC[0,0][h,h][mu,a] = Ca.get(h, mu, naoccpi[h] + a)
      for i in range(nboccpi[h]):
        oC[1,1][h,h][mu,i] = Cb.get(h, mu, i)
      for a in range(nbvirpi[h]):
        vC[1,1][h,h][mu,a] = Cb.get(h, mu, nboccpi[h] + a)


  '''# verifying C:
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
  '''

  epsilon_a = scfwfn.epsilon_a()
  epsilon_b = scfwfn.epsilon_b()
  aocc_ax = ax.Axis(naoccpi, np.ndarray)
  bocc_ax = ax.Axis(nboccpi, np.ndarray)
  avir_ax = ax.Axis(navirpi, np.ndarray)
  bvir_ax = ax.Axis(nbvirpi, np.ndarray)
  occ_ax  = ax.Axis((aocc_ax, bocc_ax), tn.Array)
  vir_ax  = ax.Axis((avir_ax, bvir_ax), tn.Array)

  oe = tn.Array(occ_ax)
  ve = tn.Array(vir_ax)
  for h in range(nirrep):
    for i in range(naoccpi[h]):
      oe[0][h][i] = epsilon_a.get(h, i)
    for a in range(navirpi[h]):
      ve[0][h][a] = epsilon_a.get(h, naoccpi[h] + a)
    for i in range(nboccpi[h]):
      oe[1][h][i] = epsilon_b.get(h, i)
    for a in range(nbvirpi[h]):
      ve[1][h][a] = epsilon_b.get(h, nboccpi[h] + a)

  e_oovv = tn.Array((occ_c2v, occ_c2v, vir_c2v, vir_c2v))
  for w1,w2,w3,w4 in e_oovv.multiaxis.iter_array_keytups():
    for h1,h2,h3,h4 in e_oovv[w1,w2,w3,w4].multiaxis.iter_array_keytups():
      e_oovv[w1,w2,w3,w4][h1,h2,h3,h4] = 1./(oe[w1][h1].reshape(-1,1,1,1) + oe[w2][h2].reshape(1,-1,1,1) - ve[w3][h3].reshape(1,1,-1,1) - ve[w4][h4].reshape(1,1,1,-1))


  G = np.empty((1,1,1,1), dtype=np.ndarray)
  G[0,0,0,0] = np.array(mints.ao_eri())
  g_c1 = tn.Array((sp_c1, sp_c1, sp_c1, sp_c1))
  for w1,w2,w3,w4 in g_c1.multiaxis.iter_array_keytups():
    if w1==w2 and w3==w4:
      g_c1[w1,w2,w3,w4] = tn.Array(g_c1[w1,w2,w3,w4].multiaxis, G)


  g_c2v = U % (U % g_c1 % U.T).transpose((1,0,3,2)) % U.T
  g_ao  = g_c2v.transpose((0,2,1,3))

  g_oovv = oC.T % (oC.T % g_ao % vC).transpose((1,0,3,2)) % vC

  T = (g_oovv - g_oovv.transpose((0,1,3,2)))*g_oovv*e_oovv

  E = 0.0

  for alpha_ss in T[0,0,0,0]:
    E += 0.5*np.sum(alpha_ss)

  for beta_ss  in T[1,1,1,1]:
    E += 0.5*np.sum(beta_ss)

  for os in T[0,1,0,1]:
    E += np.sum(os)

  print E
