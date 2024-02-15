from flask import Flask
from util import elo
from util import main
from flask import render_template
app = Flask(__name__)


@app.route('/')
def home():
    rating = main.getAvgElo(22012)
    return str(22012) + " rating: " + str(rating)




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/elo/<teamnum>')
def elo(teamnum):
    # Process the query parameter here
    rating = main.getAvgElo(int(teamnum))
    return str(int(teamnum)) + " rating: " + str(rating)


@app.route('/matchup/<team1>&<team2>/<team3>&<team4>')
def matchup(team1, team2, team3, team4):
    # Process the query parameter here
    predictions = main.predictMatches(int(team1), int(team2), int(team3), int(team4))

    ret = str(team1) + " and " + str(team2) + " (" + str(round(predictions[-2] * 100, 2)) + "%)"
    ret += " vs. "
    ret += str(team3) + " and " + str(team4) + " (" + str(round(predictions[-1] * 100, 2)) + "%)"
    return ret
# return (str(int(team1)) + " and "  + str(int(team2)) + " ("+  predictions[-2] + ")"
#         + "vs. " + str(int(team3)) + " and "  + str(int(team4)) + " ("+  predictions[-1] + ")")
