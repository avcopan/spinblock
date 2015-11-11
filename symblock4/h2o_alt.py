from axisfactory import AxisFactory
from tensor import Array, Vector

def water_mp2_script(scfwfn, mints):
  nirrep   = scfwfn.nirrep()
  nsopi    = tuple(scfwfn.nsopi()   [h] for h in range(nirrep))
  nalphpi  = tuple(scfwfn.nalphapi()[h] for h in range(nirrep))
  nbetapi  = tuple(scfwfn.nbetapi() [h] for h in range(nirrep))
  af = AxisFactory("C2v", "U", nsopi, nalphpi, nbetapi)
  
  U = Array((af.sy_ao, af.c1_ao))
  smtrzr = mints.petite_list().sotoao()
  for h in range(nirrep):
    for i in range(af.nao_pi[h]):
      for j in range(af.nao):
        U[0,0][0,0][h,0][i,j] = smtrzr.get(h, i, j)
        U[0,0][1,1][h,0][i,j] = smtrzr.get(h, i, j)

  Ca = scfwfn.Ca()
  Cb = scfwfn.Cb()

  C = Array((af.sy_ao, af.sy_mo))
  for h in range(nirrep):
    for mu in range(af.nao_pi[h]):
      for i in range(af.nocc_alph_pi[h]):
        C[0,0][0,0][h,h][mu,i] = Ca.get(h, mu, i)
      for a in range(af.nvir_alph_pi[h]):
        C[0,1][0,0][h,h][mu,a] = Ca.get(h, mu, af.nocc_alph_pi[h] + a)
      for i in range(af.nocc_beta_pi[h]):
        C[0,0][1,1][h,h][mu,i] = Cb.get(h, mu, i)
      for a in range(af.nvir_beta_pi[h]):
        C[0,1][1,1][h,h][mu,a] = Cb.get(h, mu, af.nocc_beta_pi[h] + a)

  epsilon_a = scfwfn.epsilon_a()
  epsilon_b = scfwfn.epsilon_b()
  print af.sy_mo
  e = Vector(af.sy_mo)
  for ov_block in e:
    for sp_block in ov_block:
      for pg_block in sp_block:
        print pg_block
  for h in range(nirrep):
    for i in range(af.nocc_alph_pi[h]):
      e[0][0][h][i] = epsilon_a.get(h, i)
    for a in range(af.nvir_alph_pi[h]):                       
      e[1][0][h][a] = epsilon_a.get(h, af.nocc_alph_pi[h] + a)
    for i in range(af.nocc_beta_pi[h]):                       
      e[0][1][h][i] = epsilon_b.get(h, i)
    for a in range(af.nvir_beta_pi[h]):                       
      e[1][1][h][a] = epsilon_b.get(h, af.nocc_beta_pi[h] + a)

  '''
  aocc_ax = ax.Axis(naoccpi, np.ndarray)
  bocc_ax = ax.Axis(nboccpi, np.ndarray)
  avir_ax = ax.Axis(navirpi, np.ndarray)
  bvir_ax = ax.Axis(nbvirpi, np.ndarray)
  occ_ax  = ax.Axis((aocc_ax, bocc_ax), Array)
  vir_ax  = ax.Axis((avir_ax, bvir_ax), Array)
  e = Array((ax.Axis((occ_ax, vir_ax), Array),))
  for h in range(nirrep):
    for i in range(naoccpi[h]):
      e[0][0][h][i] = epsilon_a.get(h, i)
    for a in range(navirpi[h]):
      e[1][0][h][a] = epsilon_a.get(h, naoccpi[h] + a)
    for i in range(nboccpi[h]):
      e[0][1][h][i] = epsilon_b.get(h, i)
    for a in range(nbvirpi[h]):
      e[1][1][h][a] = epsilon_b.get(h, nboccpi[h] + a)


  D = Array((mo, mo, mo, mo))
  for w1,w2,w3,w4 in D[0,0,1,1].multiaxis.iter_array_keytups():
    for h1,h2,h3,h4 in D[0,0,1,1][w1,w2,w3,w4].multiaxis.iter_array_keytups():
      D[0,0,1,1][w1,w2,w3,w4][h1,h2,h3,h4] = 1./(e[0][w1][h1].reshape(-1,1,1,1) + e[0][w2][h2].reshape(1,-1,1,1) - e[1][w3][h3].reshape(1,1,-1,1) - e[1][w4][h4].reshape(1,1,1,-1))

  G = np.empty((1,1,1,1), dtype=np.ndarray)
  G[0,0,0,0] = np.array(mints.ao_eri())
  g_c1 = Array((sp_c1, sp_c1, sp_c1, sp_c1))
  for w1,w2,w3,w4 in g_c1.multiaxis.iter_array_keytups():
    if w1==w2 and w3==w4:
      g_c1[w1,w2,w3,w4] = Array(g_c1[w1,w2,w3,w4].multiaxis, G)


  g_c2v = U % (U % g_c1 % U.T).transpose((1,0,3,2)) % U.T
  g_ao  = g_c2v.transpose((0,2,1,3)) # phys notation

  g = Array((mo, mo, mo, mo))
  g[0,0,1,1] = C[0,0].T % (C[0,0].T % g_ao % C[0,1]).transpose((1,0,3,2)) % C[0,1]

  T = (g[0,0,1,1] - g[0,0,1,1].transpose((0,1,3,2)))*g[0,0,1,1]*D[0,0,1,1]

  E = 0.0

  for alpha_ss in T[0,0,0,0]:
    E += 0.5*np.sum(alpha_ss)

  for beta_ss  in T[1,1,1,1]:
    E += 0.5*np.sum(beta_ss)

  for os in T[0,1,0,1]:
    E += np.sum(os)

  print E
  '''
