from axisfactory import AxisFactory
from tensor import Array

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
  e = Array(af.sy_mo, array=None, diagonal=True)
  for h in range(nirrep):
    for i in range(af.nocc_alph_pi[h]):
      e[0][0][h][i] = epsilon_a.get(h, i)
    for a in range(af.nvir_alph_pi[h]):                       
      e[1][0][h][a] = epsilon_a.get(h, af.nocc_alph_pi[h] + a)
    for i in range(af.nocc_beta_pi[h]):                       
      e[0][1][h][i] = epsilon_b.get(h, i)
    for a in range(af.nvir_beta_pi[h]):                       
      e[1][1][h][a] = epsilon_b.get(h, af.nocc_beta_pi[h] + a)

  import numpy as np
  import broadcast as bd

  bcast_axes = (af.sy_mo[0], af.sy_mo[0], af.sy_mo[1], af.sy_mo[1])
  D = 1./( bd.broadcast(e[0], bcast_axes, axis_keys=(0,)) + bd.broadcast(e[0], bcast_axes, axis_keys=(1,)) \
         - bd.broadcast(e[1], bcast_axes, axis_keys=(2,)) - bd.broadcast(e[1], bcast_axes, axis_keys=(3,)))



  G = np.empty((1,1,1,1), dtype=np.ndarray)
  G[0,0,0,0] = np.array(mints.ao_eri())
  g_c1_ao = Array((af.c1_ao, af.c1_ao, af.c1_ao, af.c1_ao))
  for w1,w2,w3,w4 in g_c1_ao[0,0,0,0].iter_keytups():
    if w1==w2 and w3==w4:
      g_c1_ao[0,0,0,0][w1,w2,w3,w4] = Array((af.c1_ao[0][w1], af.c1_ao[0][w2], af.c1_ao[0][w3], af.c1_ao[0][w4]), array=G)

  import contract as ct
  g_sy_ao = ct.eindot('pqrs', (g_c1_ao,'PQRS'), (U,'pP'), (U,'qQ'), (U,'rR'), (U,'sS'))
  g       = ct.eindot('pqrs', (g_sy_ao,'PQRS'), (C,'Pp'), (C,'Qq'), (C,'Rr'), (C,'Ss'))

  g = g.transpose((0,2,1,3)) # phys. notation

  T = (g[0,0,1,1] - g[0,0,1,1].transpose((0,1,3,2)))*g[0,0,1,1]*D

  E = 0.0

  for alpha_ss in T[0,0,0,0]:
    E += 0.5*np.sum(alpha_ss)

  for beta_ss  in T[1,1,1,1]:
    E += 0.5*np.sum(beta_ss)

  for os in T[0,1,0,1]:
    E += np.sum(os)

  print E
