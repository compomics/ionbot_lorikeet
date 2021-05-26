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
        spectrum_s.append(float(x), float(y))
    return spectrum_s, charge, pepmass

# Here the "matched_peptide" and "modifications" columns
# in the ionbot result file are passed to create the data
# for the varMods javascript variable
def get_varmods(peptide, modifications, deltas):
    tmp = x.split("|")
    #check ragging to correct modification positions
    rag = 0
    for i in range(0,len(x),2):
        if tmp[i+1] == "ragging": 
            rag = int(tmp[i])
    mods = []
    for i in range(0,len(x),2):
        if tmp[i] == "x": 
            continue #unlocalized
        if not tmp[i+1].startswith("["):
            continue #ragging or mutation
        mod_pos = int(tmp[i])-rag
        unimod = int(tmp[i+1].split("]")[0][1:])
        mods.append("{index: %i, modMass: %f, aminoAcid: '%s'}"%(mod_pos,deltas[unimod],peptide[mod_pos-1]))
    return mods
