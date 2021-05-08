# Lorikeet_spectrum_viewer (https://uwpr.github.io/Lorikeet/)

Python script to annotate MS2 spectra from MGF spectrum and ionbot result files.

Example (for Ionbot (https://ionbot.cloud)) output:

```
$ python.exe .\script.py .\unimodptms.txt .\Velos005137.mgf "1000.01232910156_4098.94489999998" EAWVIAWEIGTAPIEGEK N
```

This generates EAWVIAWEIGTAPIEGEK.html that needs to be run from the cloned folder.  

## Create executable with PyInstaller

Inspired from [Using PyInstaller to Easily Distribute Python Applications] 
(https://realpython.com/pyinstaller-python/)

Install PyInstaller
```
$ pip install pyinstaller
```
In the top level directory **IONBOT_LORIKEET** run
```
$ pyinstaller cli.py
```

These will be created
* A *.spec file
* A build/ folder
* A dist/ folder

The executable is in `dist/cli` folder called `dist/cli/cli` for Linux and MacOS, `dist/cli/cli.exe` for Windows

The executable file can be renamed.

To run the executable
```
$ dist/cli/cli lorikeet/unimodptms.txt lorikeet/Velos005137.mgf "715.879455566406_6431.19139999998" EAWVIAWEIGTAPIEGEK N
``` 

To run the application to debug
```
$ python cli.py lorikeet/unimodptms.txt lorikeet/Velos005137.mgf "715.879455566406_6431.19139999998" EAWVIAWEIGTAPIEGEK N
```



