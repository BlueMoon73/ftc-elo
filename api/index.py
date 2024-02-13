from flask import Flask
from util import elo

app = Flask(__name__)

@app.route('/')
def home():
    val = elo.ratingDiff
    return val

@app.route('/about')
def about():
    return 'About'
