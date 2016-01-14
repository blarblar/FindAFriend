from flask import render_template
from flask import Flask

app = Flask(__name__)

@app.route('/')

def hello(name=None):
    name="Dave"
    return render_template('main.html', name=name)

if __name__ == '__main__':
    app.run('0.0.0.0', port=80)
