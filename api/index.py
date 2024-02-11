from flask import Flask
import elo 
import main

app = Flask(__name__)

@app.route('/')
def home():
    return elo.ratingDiff

@app.route('/about')
def about():
    return 'About'
