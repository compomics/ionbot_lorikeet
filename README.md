# ionbot.tableau

The ionbot.tableau local webserver extends the functionality of Tableau Reader specificly for the ionbot result file. It allows you to view MS2 spectrum annotations by providing the full path to the spectrum files that correspond to the ionbot result file.

### Windows/Mac

Please donwload the executable here. Double click will open ionbot.tableau in your default webbrowser. After setting the full path to the spectrum files ionbot.tableau will listen to incomming calls from Tableau Reader.

### Compilation

Compilation requires PyInstaller. First compile ionbot.tableau.py:

```
pyinstaller.exe --exclude matplotlib --exclude scipy --exclude pandas  --onefile .\ionbot.tableau.py
```

Next, open ionbot.tableau.spec and replace

```
datas=[],
```

with

```
datas=[('templates', 'templates'),('static', 'static'),('unimodptms.txt', '.')],
```

and compile gain:

```
pyinstaller.exe --exclude matplotlib --exclude scipy --exclude pandas  --onefile .\ionbot.tableau.spec
```

The binary is written in the `dist` folder.
