import axis   as ax
import tensor as tn
import numpy  as np

class AxisFactory(object):

  def __init__(self, pg_label, sp_label, nao_pi, nocc_alph_pi, nocc_beta_pi):
    self.nao_pi       = nao_pi
    self.nocc_alph_pi = nocc_alph_pi
    self.nocc_beta_pi = nocc_beta_pi
    self.nvir_alph_pi = tuple(nao-nalph for nao, nalph in zip(nao_pi, nocc_alph_pi))
    self.nvir_beta_pi = tuple(nao-nbeta for nao, nbeta in zip(nao_pi, nocc_beta_pi))

    self.nirrep       = len(nao_pi)

    self.nao          = sum(self.nao_pi      )
    self.nocc         = sum(self.nocc_alph_pi)
    self.nocc         = sum(self.nocc_beta_pi)
    self.nvir         = sum(self.nvir_alph_pi)
    self.nvir         = sum(self.nvir_beta_pi)

    c1_gen_alph = ax.Axis(self.nao , np.ndarray)
    c1_occ_alph = ax.Axis(self.nocc, np.ndarray)
    c1_occ_beta = ax.Axis(self.nocc, np.ndarray)
    c1_vir_alph = ax.Axis(self.nvir, np.ndarray)
    c1_vir_beta = ax.Axis(self.nvir, np.ndarray)

    sy_gen_alph = ax.IrrepAxis(pg_label, self.nao_pi      , np.ndarray)
    sy_occ_alph = ax.IrrepAxis(pg_label, self.nocc_alph_pi, np.ndarray)
    sy_occ_beta = ax.IrrepAxis(pg_label, self.nocc_beta_pi, np.ndarray)
    sy_vir_alph = ax.IrrepAxis(pg_label, self.nvir_alph_pi, np.ndarray)
    sy_vir_beta = ax.IrrepAxis(pg_label, self.nvir_beta_pi, np.ndarray)

    c1_gen = ax.SpinAxis(sp_label, (c1_gen_alph, c1_gen_alph), tn.Array)
    c1_occ = ax.SpinAxis(sp_label, (c1_occ_alph, c1_occ_beta), tn.Array)
    c1_vir = ax.SpinAxis(sp_label, (c1_vir_alph, c1_vir_beta), tn.Array)
    sy_gen = ax.SpinAxis(sp_label, (sy_gen_alph, sy_gen_alph), tn.Array)
    sy_occ = ax.SpinAxis(sp_label, (sy_occ_alph, sy_occ_beta), tn.Array)
    sy_vir = ax.SpinAxis(sp_label, (sy_vir_alph, sy_vir_beta), tn.Array)

    self.c1_ao = ax.Axis((c1_gen,       ), tn.Array)
    self.c1_mo = ax.Axis((c1_occ, c1_vir), tn.Array)
    self.sy_ao = ax.Axis((sy_gen,       ), tn.Array)
    self.sy_mo = ax.Axis((sy_occ, sy_vir), tn.Array)
