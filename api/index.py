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
    teamnumber = teamnumber.replace(" ", "")
    if teamnumber is None:
        return "teamnumber parameter is missing", 400
    if teamnumber.isnumeric():
        rating = main.getAvgElo(int(teamnumber))
        name = main.getTeamName(int(teamnumber))
        return render_template('elo.html', teamnumber=teamnumber, rating=round(rating,2), teamName = name )
    else:
        return render_template('error.html')
    # return str(int(teamnumber)) + " rating: " + str(rating)


@app.route('/matchup', methods=['GET'])
def matchup():

    team1 = request.args.get('team1')
    team2 = request.args.get('team2')
    team3 = request.args.get('team3')
    team4 = request.args.get('team4')
    team1 = team1.replace(" ", "")
    team2 = team2.replace(" ", "")
    team3 = team3.replace(" ", "")
    team4 = team4.replace(" ", "")


    if team2 is "":
        team2 = team1
    if team4 is "":
        team4 = team3

    if team1.isnumeric() and team2.isnumeric() and team3.isnumeric() and team4.isnumeric():

        team1 = int(team1)
        team2 = int(team2)
        team3 = int(team3)
        team4 = int(team4)
        predictions = main.predictMatches(team1, team2, team3, team4)
        name1= main.getTeamName(team1)
        name2= main.getTeamName(team2)
        name3= main.getTeamName(team3)
        name4= main.getTeamName(team4)
        return render_template('matchup.html', team1=team1, team2=team2, team3=team3, team4=team4, bluePred = round(predictions[-2] * 100, 2), redPred = round(predictions[-1] * 100, 2),
                               team1Name = name1,
                               team2Name = name2,
                               team3Name = name3,
                               team4Name = name4)
    else:
        return render_template('error.html')