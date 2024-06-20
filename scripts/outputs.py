import os
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from astropy.time import Time
from matplotlib import rcParams
import scripts.rv_functions as rv_functions


rcParams['font.size'] = 16.0
rcParams['axes.linewidth'] = 1

rcParams['ytick.major.size'] = 6
rcParams['ytick.major.width'] = 1.5
rcParams['ytick.minor.size'] = 3
rcParams['ytick.minor.width'] = 0.5

rcParams['xtick.major.size'] = 6
rcParams['xtick.major.width'] = 1.5
rcParams['xtick.minor.size'] = 3
rcParams['xtick.minor.width'] = 0.5

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Helvetica']



def save_arrays(mocca_rvs, mocca_ervs, mocca_jds, star):
    tn = Time.now().isot[:16]    

def plot_RV_jd(jd, num_pl, rv, erv, K, per, t0, c, d, alpha, dir, star):
    tn = Time.now().isot[:16]
    
    plt.figure(figsize = (13.9, 6. + 4 * num_pl))
    gs = gridspec.GridSpec(nrows = num_pl + 1, ncols = 1, wspace = 0.45)

    for i in range(num_pl + 1):
        axi = plt.subplot(gs[i])
    
        axi.xaxis.set_minor_locator(AutoMinorLocator())
        axi.yaxis.set_minor_locator(AutoMinorLocator())
        axi.tick_params('both', direction = 'in', length = 10, width = 1.5, which = 'major', labelsize = 16)
        axi.tick_params('both', direction = 'in', length = 5, width = 0.5, which = 'minor')
        axi.tick_params('x', top = True, labeltop = True, bottom = False, labelbottom = False, which = 'minor')

    # RV vs JD
    ax0 = plt.subplot(gs[0])
    ax0.scatter(jd, rv, c = 'salmon', edgecolor = 'w', lw = 0.5, s = 80)
    ax0.errorbar(jd, rv, yerr = erv, c = 'salmon', lw = 1, alpha = 0.4, linestyle = 'none')

    ax0.set_title(r'Time [JD $-$ 2$\,$459$\,$400]', pad = 12, fontsize = 16)
    ax0.tick_params(bottom = False, labelbottom = False)
    ax0.tick_params(top = True, labeltop = True)
    ax0.axhline(0, lw = 1, alpha =  0.1, color = 'k', ls = '-')
    ax0.grid(alpha = 0.1, which = 'both')
    ax0.set_ylabel(r'$\Delta$RV [m/s]', labelpad = 10)

    # RV vs phase
    rvc = rv.copy()
    for pl in range(num_pl):
        per_pl = per[pl]
        t0_pl = t0[pl]
        phase = ((np.array(jd) - t0_pl) % per_pl) / per_pl

        # substract the signal of the other planets
        K_npl = np.delete(K, pl)
        per_npl = np.delete(per, pl)
        t0_npl = np.delete(t0, pl)
        c_npl = np.delete(c, pl)
        d_npl = np.delete(d, pl)
        alpha_npl = np.delete(alpha, pl)
        rvi = rvc - rv_functions.rv_model(jd, num_pl - 1, K_npl, per_npl, t0_npl, c_npl, d_npl, alpha_npl)

        axi = plt.subplot(gs[pl + 1])
        axi.scatter(phase, rvi, c = 'royalblue', edgecolor = 'w', lw = 0.5, s = 80)
        axi.errorbar(phase, rvi, yerr = erv, c = 'royalblue', lw = 1, alpha = 0.4, linestyle = 'none')

        axi.set_title(f'P = {per_pl} d', pad = 12, fontsize = 16)
        axi.axhline(0, lw = 1, alpha =  0.1, color = 'k', ls = '-')
        axi.grid(alpha = 0.1, which = 'both')
        axi.set_ylabel(r'$\Delta$RV [m/s]', labelpad = 10)

        if pl == num_pl -1:
            axi.set_xlabel('Orbital phase')
