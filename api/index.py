from flask import Flask
from util import elo
from util import main
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('page.html')

@app.route('/elo/?teamnumber=<teamnum>')
def elo(teamnum):
    rating = main.getAvgElo(int(teamnum))
    return str(int(teamnum)) + " rating: " + str(rating)

@app.route('/matchup/?team1=<team1>&team2=<team2>&team3=<team3>&team4=<team4>')
def matchup(team1, team2, team3, team4):
    predictions = main.predictMatches(int(team1), int(team2), int(team3), int(team4))

    ret = str(team1) + " and " + str(team2) + " (" + str(round(predictions[-2] * 100, 2)) + "%)"
    ret += " vs. "
    ret += str(team3) + " and " + str(team4) + " (" + str(round(predictions[-1] * 100, 2)) + "%)"
    return ret
