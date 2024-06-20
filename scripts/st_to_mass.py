# Spectral type - Stellar mass correspondance 
# Sources:  - from O3 V to K6 V we use Table 5 of Pecaut & Mamajek (2013) [https://www.pas.rochester.edu/~emamajek/EEM_dwarf_UBVIJHK_colors_Teff.txt]
#           - from K7 V to M9 V we use Table 6 of C. Cifuentes et al. (2020) [https://ui.adsabs.harvard.edu/abs/2020A%26A...642A.115C/abstract]


import sys


# dictionary with the structure 'ST': mass [Solas masses]
dic_ms = {'O3': 59., 'O4': 48., 'O5': 43., 'O6': 35., 'O7': 28., 'O8': 23.6, 'O9': 20.2,
          'B0': 17.7, 'B1': 11.8, 'B2': 7.3, 'B3': 5.4, 'B4': 5.1, 'B5': 4.7, 'B6': 4.3, 'B7': 3.92, 'B8': 3.38, 'B9': 2.75,
          'A0': 2.18, 'A1': 2.05, 'A2': 1.98, 'A3': 1.86, 'A4': 1.93, 'A5': 1.88, 'A6': 1.83, 'A7': 1.77, 'A8': 1.81, 'A9': 1.75,
          'F0': 1.61, 'F1': 1.5, 'F2': 1.46, 'F3': 1.44, 'F4': 1.38, 'F5': 1.33, 'F6': 1.25, 'F7': 1.21, 'F8': 1.18, 'F9': 1.13,
          'G0': 1.06, 'G1': 1.03, 'G2': 1., 'G3': 0.99, 'G4': 0.985, 'G5': 0.98, 'G6': 0.97, 'G7': 0.95, 'G8': 0.94, 'G9': 0.9,
          'K0': 0.88, 'K1': 0.86, 'K2': 0.82, 'K3': 0.78, 'K4': 0.73, 'K5': 0.70, 'K6': 0.69, 'K7': 0.646,
          'M0': 0.622, 'M1': 0.556, 'M2': 0.475, 'M3': 0.386, 'M4': 0.302, 'M5': 0.195, 'M6': 0.121, 'M7': 0.101, 'M8': 0.104, 'M9': 0.077}


def get_ms(st):

    if st not in dic_ms.keys():
        print('ERROR: The given ST does not appear in our database. Please, make sure it is of the format "K4" without decimals or roman numerals. Only ST from main sequence stars are allowed.')
        sys.exit()

    return dic_ms[st] # Msun