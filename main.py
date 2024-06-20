import streamlit as st
import pandas as pd
import numpy as np
import scripts.inputs as inputs
import scripts.rv_functions as rv_functions
import scripts.outputs as outputs
import scripts.st_to_mass as st_to_mass
from astropy.time import Time
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib import rcParams
from io import BytesIO

st.set_page_config(
    page_title="Mocca",
    page_icon="☕",
    layout='wide')

st.title('Mocca')
st.subheader('by Olga Balsalobre-Ruza & Jorge Lillo-Box & Pedro Mas-Buitrago &nbsp; [![pedro](https://img.shields.io/badge/%20Click_me!-red?style=social&logo=github&label=Remote%20Worlds&labelColor=grey)](https://remote-worlds-lab.cab.inta-csic.es/)')
st.markdown('---')

cols_full = st.columns(2)

with cols_full[0]:

    cols_pl = st.columns(6)
    with cols_pl[0]:
        num_pl = st.number_input('Number of planets',value=2,min_value=1,max_value=15)
        alpha = np.full(num_pl, np.nan)

    cols_lay = st.columns(num_pl+1)
    with cols_lay[0]:

        st.subheader('Star')

        star_list = ['Stellar mass','Spectral type']

        star_input = st.selectbox("Choose your input", star_list)

        if star_input == 'Stellar mass':
            
            ms = st.number_input(r'Stellar mass [$M_\odot$]',value=0.6,min_value=0.1,max_value=10.0,step=0.1)

        elif star_input == 'Spectral type':

            dic_ms = {'O3': 59., 'O4': 48., 'O5': 43., 'O6': 35., 'O7': 28., 'O8': 23.6, 'O9': 20.2,
                'B0': 17.7, 'B1': 11.8, 'B2': 7.3, 'B3': 5.4, 'B4': 5.1, 'B5': 4.7, 'B6': 4.3, 'B7': 3.92, 'B8': 3.38, 'B9': 2.75,
                'A0': 2.18, 'A1': 2.05, 'A2': 1.98, 'A3': 1.86, 'A4': 1.93, 'A5': 1.88, 'A6': 1.83, 'A7': 1.77, 'A8': 1.81, 'A9': 1.75,
                'F0': 1.61, 'F1': 1.5, 'F2': 1.46, 'F3': 1.44, 'F4': 1.38, 'F5': 1.33, 'F6': 1.25, 'F7': 1.21, 'F8': 1.18, 'F9': 1.13,
                'G0': 1.06, 'G1': 1.03, 'G2': 1., 'G3': 0.99, 'G4': 0.985, 'G5': 0.98, 'G6': 0.97, 'G7': 0.95, 'G8': 0.94, 'G9': 0.9,
                'K0': 0.88, 'K1': 0.86, 'K2': 0.82, 'K3': 0.78, 'K4': 0.73, 'K5': 0.70, 'K6': 0.69, 'K7': 0.646,
                'M0': 0.622, 'M1': 0.556, 'M2': 0.475, 'M3': 0.386, 'M4': 0.302, 'M5': 0.195, 'M6': 0.121, 'M7': 0.101, 'M8': 0.104, 'M9': 0.077}

            sp_list = ['O3','O4','O5','O6','O7','O8','O9']

            for l in ['B','A','F','G']:
                for n in range(10):

                    sp_list.append(l+str(n))

            for n in range(8):

                sp_list.append('K'+str(n))         

            for n in range(10):

                sp_list.append('M'+str(n))
            

            spt = st.selectbox("Spectral type", sp_list)
            ms = st_to_mass.get_ms(spt)
            st.write(f'Stellar mass adopted: {ms} $M_\odot$')

        st.markdown('#### Observational strategy')
        nrv = st.number_input('Number of RVs',value=30,min_value=2,max_value=50,step=1)
        erv = st.number_input('Uncertainty of RVs',value=2.,min_value=0.5,max_value=50.,step=1.)
        cad = st.number_input('Mean cadence',value=6,min_value=1,max_value=20,step=1)


    per = np.array([])
    t0 = np.array([])
    ecc = np.array([])
    inc = np.array([])
    w = np.array([])
    c = np.array([])
    d = np.array([])
    mp = np.array([])
    alpha = np.full(num_pl, np.nan)

    for i in np.arange(1,num_pl+1):

        with cols_lay[i]:

            st.subheader(f'Planet #{i}')

            p = st.slider('Period [d]',key='slp'+str(i),value=12.3,min_value=0.3,max_value=300.0,step=0.2)
            t = st.number_input('Transit time [BJD]',key='ntr'+str(i),value=2459921.5,min_value=2458849.5,max_value=2460310.5,step=1.)
            e = st.slider('Eccentricity',key='sle'+str(i),value=0.05,min_value=0.,max_value=1.0,step=0.1)
            inci = st.slider('Orbital inclination [deg]',key='slinc'+str(i),value=89.,min_value=0.,max_value=180.,step=1.)
            wi = st.slider('Argument of periapsis [deg]',key='slwi'+str(i),value=266.,min_value=0.,max_value=360.,step=1.)
            ci = e * np.cos(np.radians(wi))
            di= e * np.sin(np.radians(wi))
            m = st.number_input(r'Planetary mass [$M_{\oplus}$]',key='nm'+str(i),value=135.,min_value=1.,max_value=200.,step=5.)

            per = np.append(per,p)
            t0 = np.append(t0,t)
            ecc = np.append(ecc,e)
            inc = np.append(inc,inci)
            w = np.append(w,wi)
            c = np.append(c,ci)
            d = np.append(d,di)
            mp = np.append(mp,m)
            
    # We gather the planetary information
        
    # RV_semiamplitude definition
        
    cte_G = 6.6743e-11 # m**3/(kg**2 * s**2)
    me_to_kg = 5.9722e24
    ms_to_kg = 1.9891e30
    d_to_s = 24 * 3600

    K = mp * me_to_kg * np.sin(np.radians(inc)) * (1 - ecc**2)**(-1/2) * (mp * me_to_kg + ms * ms_to_kg)**(-2/3) * (2 * np.pi * cte_G / (per * d_to_s))**(1/3)

    # Let's create those Mock RVs!!!

    jd_i = Time(Time.now(), scale = 'utc').jd # initializing the observing dates

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

# PLOT

with cols_full[1]:
        
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

    tn = Time.now().isot[:16]

    fig = plt.figure(figsize = (13.9, 6. + 4 * num_pl))
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
    ax0.scatter(mocca_jds, mocca_rvs, c = '#6DC5D1', edgecolor = 'w', lw = 0.5, s = 100)
    ax0.errorbar(mocca_jds, mocca_rvs, yerr = mocca_ervs, c = '#6DC5D1', lw = 1.5, alpha = 0.4, linestyle = 'none')

    ax0.set_title(r'Time [JD $-$ 2$\,$459$\,$400]', pad = 12, fontsize = 16)
    ax0.tick_params(bottom = False, labelbottom = False)
    ax0.tick_params(top = True, labeltop = True)
    ax0.axhline(0, lw = 1, alpha =  0.1, color = 'k', ls = '-')
    ax0.grid(alpha = 0.1, which = 'both')
    ax0.set_ylabel(r'$\Delta$RV [m/s]', labelpad = 10)

    # RV vs phase
    rvc = mocca_rvs.copy()
    for pl in range(num_pl):
        per_pl = per[pl]
        t0_pl = t0[pl]
        phase = ((np.array(mocca_jds) - t0_pl) % per_pl) / per_pl

        # substract the signal of the other planets
        K_npl = np.delete(K, pl)
        per_npl = np.delete(per, pl)
        t0_npl = np.delete(t0, pl)
        c_npl = np.delete(c, pl)
        d_npl = np.delete(d, pl)
        alpha_npl = np.delete(alpha, pl)
        rvi = rvc - rv_functions.rv_model(mocca_jds, num_pl - 1, K_npl, per_npl, t0_npl, c_npl, d_npl, alpha_npl)

        axi = plt.subplot(gs[pl + 1])
        axi.scatter(phase, rvi, c = '#ff9156', edgecolor = 'w', lw = 0.5, s = 100)
        axi.errorbar(phase, rvi, yerr = erv, c = '#ff9156', lw = 1.5, alpha = 0.4, linestyle = 'none')

        axi.set_title(f'P = {per_pl} d', pad = 12, fontsize = 16)
        axi.axhline(0, lw = 1, alpha =  0.1, color = 'k', ls = '-')
        axi.grid(alpha = 0.1, which = 'both')
        axi.set_ylabel(r'$\Delta$RV [m/s]', labelpad = 10)

        if pl == num_pl -1:
            axi.set_xlabel('Orbital phase')

    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.image(buf)