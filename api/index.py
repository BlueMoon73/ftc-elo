from flask import Flask
from util import elo

app = Flask(__name__)

@app.route('/')
def home():
    return 'asd'

@app.route('/about')
def about():
    return 'About'
