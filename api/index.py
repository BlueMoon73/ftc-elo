from flask import Flask
from . import elo 


app = Flask(__name__)

@app.route('/')
def home():
    return elo.ratingDiff

@app.route('/about')
def about():
    return 'About'
