from flask import Flask
from flask.templating import render_template
app = Flask(__name__)

@app.route('/')
def main():
    return 'hello'

@app.route("/sequence/<name>")
def hello(name=None):
    print(name + '.html')
    return render_template(name + '.html')