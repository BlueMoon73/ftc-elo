from flask import Flask
from util import elo
from util import main

app = Flask(__name__)

@app.route('/')
def home():

    rating = main.getAvgElo(22012)
    return str(22012) + " rating: " + str(rating)

@app.route('/about')
def about():
    return 'About'
