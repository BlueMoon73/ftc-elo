from flask import Flask, request, render_template
from util import elo
from util import main

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('page.html')


@app.route('/elo', methods=['GET'])
def elo():
    teamnumber = request.args.get('teamnumber')
    if teamnumber is None:
        return "teamnumber parameter is missing", 400
    rating = main.getAvgElo(int(teamnumber))
    return str(int(teamnumber)) + " rating: " + str(rating)


@app.route('/elo/<teamnum>')
def elo2(teamnum):
    rating = main.getAvgElo(int(teamnum))
    return str(int(teamnum)) + " rating: " + str(rating)


@app.route('/matchup/<team1>&<team2>/<team3>&<team4>')
def matchup(team1, team2, team3, team4):
    predictions = main.predictMatches(int(team1), int(team2), int(team3), int(team4))

    ret = str(team1) + " and " + str(team2) + " (" + str(round(predictions[-2] * 100, 2)) + "%)"
    ret += " vs. "
    ret += str(team3) + " and " + str(team4) + " (" + str(round(predictions[-1] * 100, 2)) + "%)"
    return ret


@app.route('/matchup?team1=<team1>&team2=<team2>&team3=<team3>&team4=<team4>', methods=['GET'])
def matchup2(team1, team2, team3, team4):
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')
    team3 = request.args.get('team3')
    team4 = request.args.get('team4')
    if team1 or team3 is None:
        return "teamnumber parameter is missing", 400
    if team2 is None:
        team2 = team1
    if team4 is None:
        team4 = team3

    predictions = main.predictMatches(int(team1), int(team2), int(team3), int(team4))

    ret = str(team1) + " and " + str(team2) + " (" + str(round(predictions[-2] * 100, 2)) + "%)"
    ret += " vs. "
    ret += str(team3) + " and " + str(team4) + " (" + str(round(predictions[-1] * 100, 2)) + "%)"
    return ret
