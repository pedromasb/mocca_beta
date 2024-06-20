import scripts.inputs as inputs
import scripts.rv_functions as rv_functions
import scripts.outputs as outputs
import numpy as np
from astropy.time import Time


dic_inputs = inputs.get()


if 'file' in dic_inputs.keys():
    print('TO BE DONE: leer file, etc')
    # TO BE DONE. por aquí, un modulo que lea el fichero si lo hay y haga las inferencias de K, erv, etc
else:
    K = rv_functions.RV_semiamplitude(dic_inputs) # m/s
    erv = dic_inputs['erv']
    jd_i = Time(Time.now(), scale = 'utc').jd # initilizing the observing dates


# Observational strategy info
nrv = dic_inputs['nrv']
cad = dic_inputs['cad']


# Planetary info
num_pl = dic_inputs['num_pl']
per = dic_inputs['per']
t0 = dic_inputs['t0']
ecc = dic_inputs['ecc']
w = dic_inputs['w']
c = ecc * np.cos(np.radians(w))
d = ecc * np.sin(np.radians(w))


# Add trojans?
if 'mtr' in dic_inputs.keys(): # alpha parameter as defined in Leleu et al. (2017)
    print('TO BE DONE!!') # tener cuidado si hay más de un planeta en el rv_model. # mtr/mp * np.sin(60) y el signo segun l4 o l5
else:
    alpha = np.full(num_pl, np.nan)


# Let's create those Mock RVs!!!
mocca_rvs = np.array([])
mocca_ervs = np.array([])
mocca_jds = np.array([])
for ndp in range(nrv):

    rv_i = rv_functions.rv_model(np.array([jd_i]), num_pl, K, per, t0, c, d, alpha)
    noise_i = np.random.normal(0., erv/1.3)
    rv_i += noise_i
    erv_i = np.random.normal(erv, 0.15 * erv)

    # store the mock values in arrays
    mocca_rvs = np.append(mocca_rvs, rv_i)
    mocca_ervs = np.append(mocca_ervs, erv_i)
    mocca_jds = np.append(mocca_jds, jd_i)

    jd_i += np.random.normal(cad, 2.) # new date for the next iteration


# Outputs
dir = dic_inputs['dir']
star = dic_inputs['star']
outputs.save_arrays(mocca_rvs, mocca_ervs, mocca_jds, dir, star)
outputs.plot_RV_jd(mocca_jds, num_pl, mocca_rvs, mocca_ervs, K, per, t0, c, d, alpha, dir, star)