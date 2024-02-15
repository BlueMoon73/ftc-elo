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


@app.route('/elo/<teamnum>')
def search(teamnum):
    # Process the query parameter here
   rating = main.getAvgElo(int(teamnum))
   return str(int(teamnum)) + " rating: " + str(rating)

@app.route('/matchup/<team1>&<team2>/<team3>&<team4>')
def search(team1, team2, team3, team4):
    # Process the query parameter here
   predictions = main.predictMatches(int(team1), int(team2), int(team3), int(team4))
   return (str(int(team1)) + " and "  + str(int(team2)) + " ("+  predictions[-2] + ")"
           + "vs. " + str(int(team3)) + " and "  + str(int(team4)) + " ("+  predictions[-1] + ")")

