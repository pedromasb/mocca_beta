import radvel
import numpy as np

def dummy_npwarn_decorator_factory():
  def npwarn_decorator(x):
    return x
  return npwarn_decorator
np._no_nep50_warning = getattr(np, '_no_nep50_warning', dummy_npwarn_decorator_factory)


def RV_semiamplitude(dic_inputs): # units [m/s]

    ms = dic_inputs['ms']
    mp = np.array(dic_inputs['mp'])
    per = np.array(dic_inputs['per'])
    ecc = np.array(dic_inputs['ecc'])
    inc = np.array(dic_inputs['inc'])

    cte_G = 6.6743e-11 # m**3/(kg**2 * s**2)
    me_to_kg = 5.9722e24
    ms_to_kg = 1.9891e30
    d_to_s = 24 * 3600

    K = mp * me_to_kg * np.sin(np.radians(inc)) * (1 - ecc**2)**(-1/2) * (mp * me_to_kg + ms * ms_to_kg)**(-2/3) * (2 * np.pi * cte_G / (per * d_to_s))**(1/3)
    return K


def rv_model(jd, num_pl, K, per, t0, c, d, alpha):
    
    rv_model = np.full(len(jd), 0.0)
    params = radvel.model.Parameters(num_planets = np.sum(np.isnan(alpha)), basis = 'per tc ecosw esinw k')
    nkep = 1

    for i in range(int(num_pl)):
        if np.isnan(alpha[i]): # Keplerian
            params[f'per{nkep}'].value = per[i]
            params[f'k{nkep}'].value = K[i]
            params[f'tc{nkep}'].value = t0[i]
            params[f'ecosw{nkep}'].value = c[i]
            params[f'esinw{nkep}'].value = d[i]
            nkep += 1

    
    keplerian = radvel.model._standard_rv_calc(jd, params, radvel.model.Vector(params))
    rv_model += keplerian
    return rv_model
