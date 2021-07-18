import sys
import os
import webbrowser
from threading import Timer

from flask.helpers import url_for
#from lorikeet.__main__ import main
from lorikeet.data_parser import get_spectrum_with_mgf, get_varmods
from flask import Flask, request
from flask.templating import render_template

mgf_file_dir = ""

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
def tableau():
    global mgf_file_dir
    if mgf_file_dir == "":
        return render_template('tableau.html')
    else:
        res = "Tableau is connected to folder '%s'."%mgf_file_dir
        return render_template('tableau.html',response=res,state="alert-success")

@app.route('/setfolder', methods = ['GET', 'POST'])
def setfolder():
   global mgf_file_dir
   if request.method == 'POST':
      f = request.form['folder']
      mgf_file_dir = f
      if not os.path.isdir(mgf_file_dir):
        f = "Could not find '%s'.\nDid you specify the spectrum file(s) folder correctly?"%(mgf_file_dir)
        return render_template('tableau.html',response=f,state="alert-danger")
      res = "Tableau is connected to folder '%s'."%mgf_file_dir
      return render_template('tableau.html',response=res,state="alert-success")

@app.route("/mgf/<mgf_name>/spectrum/<spectrum_title>/sequence/<sequence>/mods/<mods>")
def getSpectrum(mgf_name=None, sequence=None, spectrum_title=None, mods=None):
    global mgf_file_dir
    if mgf_file_dir == "":
        f = "Please enter the spectrum file(s) folder below."
        return render_template('tableau.html',response=f, state="alert-danger")
    if not os.path.isfile(os.path.join(mgf_file_dir,mgf_name)):
        f = "Could not find '%s' in '%s'.\nDid you specify the spectrum file(s) folder correctly?"%(mgf_name,mgf_file_dir)
        return render_template('tableau.html',response=f,state="alert-danger")
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

def open_browser():
      webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    #main()
    print("Please wait, your browser will open soon...")
    Timer(1.5, open_browser).start();
    app.run()

