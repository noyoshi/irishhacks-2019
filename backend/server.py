import sys
from flask import Flask, render_template

sys.path.append('../frontend')

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to Volunteerer'

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='41001')
