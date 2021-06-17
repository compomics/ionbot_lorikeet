import numpy as np

from pyteomics import mgf, auxiliary

# Get spectrum, pepmass and charge using pyteomics IndexedMGF
def get_spectrum_with_mgf(mgf_file, title):
    # read mgf
    f = mgf.IndexedMGF(mgf_file)

    spectrum = f[title]
    mz_array = f[title]['m/z array']
    intensity_array = f[title]['intensity array']
    pepmass = f[title]['params']['pepmass'][0]
    charge = str(f[title]['params']['charge']).replace('+', '')

    # parse m/z array and intensity array to create a data structure
    # [['m/z', 'intensity']]
    spectrum_s = []
    for x, y in np.nditer([mz_array, intensity_array]):
        spectrum_s.append([float(x), float(y)])
    return spectrum_s, charge, pepmass

def get_varmods(sequence, modifications):
    if modifications == "0|":
        return "[]"
    mods = "["
    tmp = modifications.split("|")
    for i in range(0,len(tmp),2):
        mods += "{index: %s, modMass: %s, aminoAcid: '%s'}"%(tmp[i],tmp[i+1],sequence[int(tmp[i])-1])
    return mods + "]"