import argparse
import scripts.st_to_mass as st_to_mass
import numpy as np
import sys


def get():

    parser = argparse.ArgumentParser()

    parser.add_argument("-dir", "--output_dir", default = None, help = "Output directory path")

    # Star info
    parser.add_argument("-star", "--star_name", default = None, help = "Name of the star to custom the outputs")
    parser.add_argument("-ms", "--stellar_mass", default = None, help = "Stellar mass in solar units")
    parser.add_argument("-st", "--spectral_type", default = None, help = "Stellar spectral type to get the mass for main sequence stars only (do nor include 'V')")

    # Planet info
    parser.add_argument("-np", "--number_planets", default = 1, help = "Number of planets.")
    parser.add_argument("-p", "--orbital_period", nargs = '+', default = None, help = "Orbital period of the planet(s) in days.")
    parser.add_argument("-t0", "--transiting_time", nargs = '+', default = None, help = "Transiting time of the planet(s) in BJD.")
    parser.add_argument("-e", "--eccentricity", nargs = '+', default = None, help = "Orbital eccentricity(/ies)")
    parser.add_argument("-w", "--arg_periastron", nargs = '+', default = None, help = "Argument(s) of periastron in degrees") 
    parser.add_argument("-i", "--inclination", nargs = '+', default = None, help = "Orbital inclination(s) in degrees")
    
    parser.add_argument("-mp", "--planetary_mass", nargs = '+', default = None, help = "Planetary mass(es) in Earth units")
    parser.add_argument("-rp", "--planetary_radius", nargs = '+', default = None, help = "Planetary radius in Earth units to infer the mass if not given")

    # Add trojan
    parser.add_argument("-mtr", "--trojan_mass", nargs = '+', default = None, help = "Trojan mass in Earth units.")
    parser.add_argument("-ltr", "--lagrangian_region", nargs = '+', default = None, help = "Specify l4 or l5.")

    # Previous RVs dataset
    parser.add_argument("-file", "--file_path_rvs", default = None, help = "Path of previous RVs. Columns must be jd, rv, erv, instrument. Separated by commas ','")

    # Observational strategy
    parser.add_argument("-nrv", "--number_rvs", default = None, help = "Number of RV measurements to be simulated")
    parser.add_argument("-cad", "--cadence", default = None, help = "Median cadence to observe the target")
    parser.add_argument("-erv", "--rv_uncertainty", default = None, help = "Median of the RV uncertainties to be simulated")
    parser.add_argument("-ins", "--instrument_name", default = None, help = "Instrument name. This is only mandatory if a file has been provided with more than one instrument and you want simulations from one of those")
    
    args = parser.parse_args()


    # Initialise a dictionary to store all the inputs #
    dic_inputs = {}
    
    #--------------------#
    # Getting output dir #
    #--------------------#
    dir = args.output_dir
    if not dir:
        print('WARNING: Not output directory path provided. The outputs will be stored in the working directory.')
    dic_inputs['dir'] = dir


    #-------------------#
    # Getting Star info #
    #-------------------#
    ms = args.stellar_mass
    st = args.spectral_type
    star = args.star_name

    if ms:
        ms = float(ms)
        if st:
            print('WARNING: The Stellar Mass has been provided, so the Spectral Type of the star is ignored.')
            print('')
        
        # check the given value for the stellar mass is reasonable
        if ms < 0.077:
            print('WARNING: The provided Stellar Mass is below 0.077 Masses of the Sun, which is a substellar object!')
            print('Make sure -ms is in sollar mass units.')
            print('')
        elif ms > 2.5:
            print('WARNING: The provided Stellar Mass is above 2.5 Masses of the Sun, which is hoter than a B9 ST!')
            print('Make sure -ms is in sollar mass units.')
            print('')

    elif st:
        ms = st_to_mass.get_ms(st) # ST is used to infer the stellar mass [Msun]

    else:
        print('WARNING: The Stellar Mass or Spectral Type have NOT been provided.')
        print('We continue using a K7 main-sequence star (0.646 Msun) as default.')
        print('')
        ms = 0.646

    dic_inputs['ms'] = ms 
    
    if not star:
        print('WARNING: A name for the star is not given. "Unknown_Star" is going to be used instead in the outputs.')
        print('')
        star = 'Unknown_Star'
    
    dic_inputs['star'] = star 

    #------------------------#
    # Getting Planetary info #
    #------------------------#
    num_pl = args.number_planets
    per = args.orbital_period
    t0 = args.transiting_time
    ecc = args.eccentricity
    w = args.arg_periastron
    inc = args.inclination
    mp = args.planetary_mass
    rp = args.planetary_radius

    if not num_pl:
        print('ERROR: NUMBER OF PLANETS must be given (e.g., -np 3).')
        sys.exit()
    num_pl = int(num_pl)
    dic_inputs['num_pl'] = num_pl

    if not per:
        print('WARNING: not period has been given')
        print(f'We use random value(s) between 0.3 and 50 days.')
        print('')
        per = np.random.uniform(0.3, 50., num_pl)
    elif 'nan' in per:
        print('WARNING: not period has been given for at least one planet.')
        print(f'We use for it/them (a) random value(s) between 0.3 and 50 days.')
        print('')
        per = [np.round(np.random.uniform(0.3, 50.), 3) if p == 'nan' else p for p in per]
    dic_inputs['per'] = list(map(float, per))

    if not t0:
        print('WARNING: No transiting time has been given.')
        print(f'We use random t0 for {num_pl} planets.')
        print('')
        t0 = np.random.uniform(2458849.5, 2460310.5, size = num_pl)
    elif 'nan' in t0:
        print('WARNING: not transiting has been given for at least one planet.')
        print(f'We use for it/them (a) random value(s).')
        print('')
        t0 = [np.round(np.random.uniform(2458849.5, 2460310.5), 8) if t0i == 'nan' else t0i for t0i in t0]
    dic_inputs['t0'] = list(map(float, t0))

    if not ecc:
        print('WARNING: No eccentricity has been given.')
        print(f'We use random ecc from a normal districution N(0, 0.2) for {num_pl} planets.')
        print('')
        ecc = np.random.normal(0., 0.2, size = num_pl)
    elif 'nan' in ecc:
        print('WARNING: not eccentricity has been given for at least one planet.')
        print(f'We use for it/them (a) random value(s) from a normal districution N(0, 0.2).')
        print('')
        ecc = [np.round(np.random.normal(0., 0.2), 3) if e == 'nan' else e for e in ecc]
    dic_inputs['ecc'] = list(map(float, ecc))

    if not w:
        print('WARNING: No argument of periastron has been given.')
        print(f'We use random w for {num_pl} planets.')
        print('')
        w = np.random.uniform(0., 360., size = num_pl)
    elif 'nan' in w:
        print('WARNING: not argument of periastron has been given for at least one planet.')
        print(f'We use for it/them (a) random value(s).')
        print('')
        w = [np.round(np.random.uniform(0., 360.), 3) if wi == 'nan' else wi for wi in w]
    dic_inputs['w'] = list(map(float, w))

    if not inc:
        print('WARNING: No inclination has been given.')
        print(f'We use random inc from a normal districution N(90, 0.2) for {num_pl} planets.')
        print('')
        inc = np.random.normal(90., 0.2, size = num_pl)
    elif 'nan' in inc:
        print('WARNING: not inclination has been given for at least one planet.')
        print(f'We use for it/them (a) random value(s) from a normal districution N(90, 0.2).')
        print('')
        inc = [np.round(np.random.normal(90., 0.), 3) if i == 'nan' else i for i in inc]
    dic_inputs['inc'] = list(map(float, inc))

    # check that all parametes CALLED in the inputs have the same length 
    if not all([len(param) == num_pl for param in [per, t0, ecc, w, inc]]):
        print('ERROR: not all the given planetary parameters have the same length.')
        print('If you want to use a random value for a given parameter of a given planet use "nan" (e.g., -p 2.3 nan -e nan 0.3).')
        print('If a parameter is not called in the inputs, random values are generated for all the planets (e.g., "-np 2" will generate random values for all the orbital parameters for two planets).')
        print('')
        sys.exit()

    # Planetary mass [ALL OF THIS TO BE DONE. que se pueda dar un mp y un rp para distinto planeta. Por ahora solo mp.]
    if not mp:
        if not rp:
            print('WARNING: No planetary mass or radius has been given.')
            print('We use a random value between 1 and 200 masses of the Earth for {num_pl} planets.')
            print('')
            mp = np.random.uniform(1., 200., size = num_pl)
        #else:
        #    print('TO BE DONE: use the Chen & Kipping (2017) empirical relation to get the mass.')
        #        sys.exit()
        #    if 'nan' in rp:
        #        print('TO BE DONE')
        #    else:
        #        print('TO BE DONE')
    else:
        if 'nan' in mp:
            print('WARNING: not planetary mass has been given for at least one planet.')
            print(f'We use for it/them (a) random value(s) fbetween 1 and 200 masses of the Earth.')
            print('')
            mp = [np.round(np.random.uniform(1., 200.), 3) if m == 'nan' else m for m in mp]
    
    dic_inputs['mp'] = list(map(float, mp))


    #---------------------#
    # Getting trojan info #
    #---------------------#
    mtr = args.trojan_mass
    ltr = args.lagrangian_region
    if mtr:
        if len(mtr) != num_pl:
            print('ERROR: the number of trojans and main planets does not match. If there are 2 planets and the outer is the one with trojan the input has to be of the form "-p 3.4 7.6 -mtr nan 0.7"')
            sys.exit()
        dic_inputs['mtr'] = list(map(float, mtr))

        if not ltr:
            print('WARNING: a trojan has been included without specifying the Lagrangian region. L5 is used as default.')
            mtr = dic_inputs['mtr']
            ltr = ['l5' if not np.isnan(m) else np.nan for m in mtr]
        dic_inputs['ltr'] = ltr


    #--------------------------------#
    # Getting file with previous RVs #
    #--------------------------------#
    file = args.file_path_rvs
    if file:
        dic_inputs['file'] = file

    #--------------------------------------------#
    # Getting info of the observational strategy #
    #--------------------------------------------#
    nrv = args.number_rvs
    cad = args.cadence
    erv = args.rv_uncertainty
    ins = args.instrument_name

    if not nrv:
        print('WARNING: Number of mock RVs not given. Using the default value: 30')
        print('')
        nrv = 30
    dic_inputs['nrv'] = int(nrv)

    if not cad:
        print('WARNING: Mean cadence is given. Using the default value: 6 days')
        print('')
        cad = 6
    dic_inputs['cad'] = int(cad)

    if not erv:
        if file:
            print('WARNING: As -erv is not specified, the uncertainty of the mock RVs will be computed using the mean of the eRV from your file.')
            print('')
        else:
            print('WARNING: The mean uncertainty of the mock RVs has not been specified and no file is given to infer it. Using the default value: 2 m/s.')
            print('')
            erv = 2.
    dic_inputs['erv'] = float(erv)

    if ins:
        dic_inputs['ins'] = ins

    return dic_inputs