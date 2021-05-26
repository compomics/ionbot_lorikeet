import sys
import os
from pathlib import Path
from lorikeet.__main__ import main
from lorikeet.data_parser import get_spectrum_with_mgf, get_varmods
from flask import Flask
from flask.templating import render_template
print(getattr(sys, 'frozen', False))
template_folder = ''
if getattr(sys, 'frozen', False):
    print('bundled')
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
    return 'hello'

@app.route("/sequence/<name>")
def getSpectrumBySequence(name=None):
    print(name + '.html')
    return render_template(name + '.html')

@app.route("/mgf/<mgf_name>/spectrum/<spectrum_title>/sequence/<seqname>")
def getSpectrum(mgf_name=None, seqname=None, spectrum_title=None):
    print(seqname + '.html')
    print(sys.argv[2])
    mgf_file_dir        = sys.argv[2]
    title           = sys.argv[3]
    sequence        = sys.argv[4]
    modifications   = sys.argv[5]
    spectrum, charge, parent_mz = get_spectrum_with_mgf(os.path.join(mgf_file_dir,mgf_name), spectrum_title)
    return render_template('spectrum_viewer.html',
        spectrum = spectrum,
        charge = charge,
        parent_mz = parent_mz,
        sequence = seqname,
        spectrum_title = spectrum_title
        )

if __name__ == '__main__':
    main()
    app.run()

