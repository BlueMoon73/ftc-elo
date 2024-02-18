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
    if teamnumber.isnumeric():
        rating = main.getAvgElo(int(teamnumber))
        return render_template('elo.html', teamnumber=teamnumber, rating=round(rating,2))
    else:
        return render_template('error.html')
    # return str(int(teamnumber)) + " rating: " + str(rating)


@app.route('/matchup', methods=['GET'])
def matchup():

    team1 = request.args.get('team1')
    team2 = request.args.get('team2')
    team3 = request.args.get('team3')
    team4 = request.args.get('team4')
    if team1 is None or team3 is None:
        return "teamnumber parameter is missing", 400
    if team2 is None:
        team2 = team1
        retyu
    if team4 is None:
        team4 = team3

    predictions = main.predictMatches(int(team1), int(team2), int(team3), int(team4))

    return render_template('matchup.html', team1=team1, team2=team2, team3=team3, team4=team4, bluePred = round(predictions[-2] * 100, 2), redPred = round(predictions[-1] * 100, 2))
