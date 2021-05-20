import sys
import os
from pathlib import Path
from lorikeet.__main__ import main
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
def hello(name=None):
    print(name + '.html')
    return render_template(name + '.html')

if __name__ == '__main__':
    print('cli')
    print(template_folder)
    print(Path(template_folder).exists())
    main()
    app.run()

