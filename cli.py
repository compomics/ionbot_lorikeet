import sys
import os
from lorikeet.__main__ import main
from lorikeet.data_parser import get_spectrum_with_mgf, get_varmods
from flask import Flask
from flask.templating import render_template

def get_varmods(sequence, modifications):
    if modifications == "0|":
        return "[]"
    mods = "["
    tmp = modifications.split("|")
    for i in range(0,len(tmp),2):
        mods += "{index: %s, modMass: %s, aminoAcid: '%s'}"%(tmp[i],tmp[i+1],sequence[int(tmp[i])-1])
    return mods + "]"

template_folder = ''
if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)

@app.before_first_request
def before_first_request():
    if getattr(sys, 'frozen', False) and not template_folder == '':
        print('stuff')

@app.route('/')
def main_route():
    return render_template('landrick copy.html')

@app.route("/sequence/<name>")
def getSpectrumBySequence(name=None):
    print(name + '.html')
    return render_template(name + '.html')

@app.route("/mgf/<mgf_name>/spectrum/<spectrum_title>/sequence/<sequence>/mods/<mods>")
def getSpectrum(mgf_name=None, sequence=None, spectrum_title=None, mods=None):
    print(sys.argv[1])
    mgf_file_dir = sys.argv[1]
    modifications = get_varmods(sequence, mods)
    spectrum, charge, parent_mz = get_spectrum_with_mgf(os.path.join(mgf_file_dir,mgf_name), spectrum_title)
    return render_template('spectrum_viewer.html',
        spectrum = spectrum,
        charge = charge,
        parent_mz = parent_mz,
        sequence = sequence,
        mods = modifications,
        spectrum_title = spectrum_title
        )

if __name__ == '__main__':
    main()
    app.run()

