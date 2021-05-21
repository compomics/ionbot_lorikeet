import sys
import os
import numpy as np
import subprocess, linecache
import datetime
import time
import re
import shutil
from pathlib import Path
import http.server
# import pyteomics

from pyteomics import mgf, auxiliary
template_folder = ''
if getattr(sys, 'frozen', False):
    print('bundled')
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    # static_folder = os.path.join(sys._MEIPASS, 'static')
    if not os.path.exists(template_folder):
        os.makedirs(template_folder)
else:
    template_folder = os.path.join(os.getcwd(), 'templates')
print(template_folder)

htmlpage = '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
 <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    
    <title>Lorikeet Spectrum Viewer</title>
    
    <!--[if IE]><script language="javascript" type="text/javascript" src="/static/js/excanvas.min.js"></script><![endif]-->
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.4/jquery-ui.min.js"></script>
    <script type="text/javascript" src="/static/js/jquery.flot.js"></script>
    <script type="text/javascript" src="/static/js/jquery.flot.selection.js"></script>
    
    <script type="text/javascript" src="/static/js/specview.js"></script>
    <script type="text/javascript" src="/static/js/peptide.js"></script>
    <script type="text/javascript" src="/static/js/aminoacid.js"></script>
    <script type="text/javascript" src="/static/js/ion.js"></script>
    
    <link REL="stylesheet" TYPE="text/css" HREF="/static/css/lorikeet.css">
    
</head>

<body>

<h1>Lorikeet Plugin Example</h1>

<!-- PLACE HOLDER DIV FOR THE SPECTRUM -->
<div id="lorikeet1"></div>

<script type="text/javascript">

$(document).ready(function () {

    /* render the spectrum with the given options */
    $("#lorikeet1").specview({sequence: sequence, 
                            charge: charge,
                            massError: 0.02,
                            precursorMz: precursorMz,
                            variableMods: varMods, 
                            //ctermMod: ctermMod,
                            peaks: peaks
                            });
});

'''

# Read unimod modifications file
def read_deltas(unimod_file):
    deltas = {}
    with open(unimod_file)  as f:
        for row in f:
            l = row.rstrip().split(',')
            unimod = l[0].split('[')[1].split(']')[0]
            deltas[unimod] = float(l[1])
    return deltas

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
    spectrum_s = '['
    for x, y in np.nditer([mz_array, intensity_array]):
        spectrum_s = spectrum_s + "[%s,%s]," % (x,y)
    # remove last comma
    spectrum_s = spectrum_s[:-1]
    spectrum_s = spectrum_s + ']'
    return spectrum_s, charge, pepmass

# Parsing an MS2 spectrum (title) from an MGF file (mgf)
# As spectrum files can be quite large, I use findstr to read the lines first
# This only really speeds up things if the next query is on the same MGF file
# TODO: We should think about how to optimize this for ionbot.cloud
def get_spectrum(mgf_file, title):
    #TODO: We might want to put this loading outside

    # Windows specific
    #line = subprocess.check_output(['findstr', '/N', title, mgf])

    # Linux and macOS specific
    # for macOS ggrep can be used, much faster, but no guarantee the user will have it installed
    line = subprocess.check_output(['grep', '-n', 'TITLE='+title, mgf_file])
    line = int(line.rstrip().decode("utf-8").split(":")[0])
    spectrum = "["
    while True:
        c = linecache.getline(mgf_file, line)
        c = c.rstrip()
        if c == "": 
            line+=1
            continue
        if "END IONS" in c: break
        if "PEPMASS=" in c:
            parent_mz = c[8:]
        if "CHARGE" in c:
            charge = c[7:9].replace("+","")
        if not "=" in c:
            tmp = c.split(" ")
            spectrum += "[%s,%s],"%(tmp[0],tmp[1])
        line+=1
    spectrum = spectrum[:-1]
    spectrum += "]"
    return spectrum, charge, parent_mz

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

def main():
    unimod_file     = sys.argv[1]
    mgf_file        = sys.argv[2]
    title           = sys.argv[3]
    sequence        = sys.argv[4]
    modifications   = sys.argv[5]

    print('title', title)

    deltas = read_deltas(unimod_file)

    spectrum, charge, parent_mz = get_spectrum_with_mgf(mgf_file, title)
    if spectrum == "]":
        print("spectrum not found")
        exit()

    varmods_list = []
    if modifications != "N":
        varmods_list = get_varmods(sequence, modifications, deltas)
    
    with open(os.path.join(template_folder,sequence+'.html'),'w') as f:
        f.write(htmlpage+'\n')
        f.write('var sequence = "%s";\n'%sequence)
        f.write('var peaks = %s;\n'%spectrum)
        f.write('var charge = %s;\n'%charge)
        f.write('var precursorMz = %s;\n'%parent_mz)
        f.write('var varMods = [];\n')
        for i,mod in enumerate(varmods_list):
            f.write("varMods[%i] = %s\n"%(i,mod))
        f.write('</script></body></html>\n')

if __name__ == "__main__":
    main()